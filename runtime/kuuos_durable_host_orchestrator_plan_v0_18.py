from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_host_adapter_license_v0_17 import validate_host_license
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_durable_host_orchestrator_fairness_v0_18 import ordered_workers
from runtime.kuuos_durable_host_orchestrator_policy_v0_18 import validate_orchestrator_policy
from runtime.kuuos_durable_host_orchestrator_state_v0_18 import (
    active_dead_letter_keys,
    validate_orchestrator_state,
)
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    BLOCKED,
    IDLE,
    NON_AUTHORITY_FLAGS,
    PLAN_VERSION,
    READY,
    REQUIRED_BOUNDARY,
    candidate_key,
    plan_digest,
)
from runtime.kuuos_durable_host_orchestrator_worker_v0_18 import classify_worker_health


def _backpressure(
    *,
    queued_count: int,
    eligible_count: int,
    healthy_worker_count: int,
    dispatch_capacity: int,
    high_watermark: int,
) -> str:
    if queued_count == 0:
        return "idle"
    if healthy_worker_count == 0:
        return "no_healthy_workers"
    if eligible_count == 0:
        return "capability_gap_or_blocked"
    deferred = max(0, eligible_count - dispatch_capacity)
    if deferred > 0 and eligible_count >= max(1, int(high_watermark)):
        return "saturated"
    if deferred > 0:
        return "throttled"
    return "normal"


def _queued_or_reclaimable(candidate: Mapping[str, Any], now_ms: int) -> bool:
    state = str(candidate.get("supervisor_state", ""))
    if state == "background_queued":
        return True
    return (
        state == "background_leased"
        and str(candidate.get("ticket_status", "")) == "leased"
        and int(candidate.get("lease_expires_at_ms", 0) or 0) <= max(0, int(now_ms))
    )


def build_orchestrator_plan(
    *,
    cycle_id: str,
    supervisor_bundle: Mapping[str, Any],
    orchestrator_state: Mapping[str, Any],
    worker_reports: Sequence[Mapping[str, Any]],
    host_license: Mapping[str, Any],
    policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
    now_ms: int,
) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        validate_orchestrator_state(orchestrator_state)
    except ValueError as error:
        blockers.append(str(error))
    try:
        validate_orchestrator_policy(policy)
    except ValueError as error:
        blockers.append(str(error))
    blockers.extend(validate_host_license(host_license, now_ms=now_ms))

    source_bundle_digest = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
    if not source_bundle_digest or source_bundle_digest != bundle_digest(supervisor_bundle):
        blockers.append("supervisor_bundle_digest_invalid")
    if not str(cycle_id).strip():
        blockers.append("orchestrator_cycle_id_missing")

    licensed = {str(item) for item in as_list(host_license.get("operation_allowlist")) if str(item)}
    registered = {str(key) for key, value in registry.items() if callable(value)}
    reports = [dict(report) for report in worker_reports]
    worker_ids = [str(report.get("worker_id", "")) for report in reports]
    if len(worker_ids) != len(set(worker_ids)):
        blockers.append("duplicate_worker_id")

    health = [
        classify_worker_health(
            report,
            now_ms=now_ms,
            policy=policy,
            licensed_operations=licensed,
            registered_operations=registered,
        )
        for report in reports
    ]
    worker_order = ordered_workers(health, orchestrator_state)
    union_operations = sorted(licensed & registered)
    base_projection = project_host_work(
        supervisor_bundle=supervisor_bundle,
        now_ms=now_ms,
        operation_allowlist=union_operations,
    )
    candidates = [dict(mapping(item)) for item in as_list(base_projection.get("candidates"))]
    queued_count = sum(1 for item in candidates if _queued_or_reclaimable(item, now_ms))

    dead_letters = active_dead_letter_keys(orchestrator_state)
    worker_eligible_job_ids: dict[str, list[str]] = {}
    assignable_job_ids: set[str] = set()
    for worker in worker_order:
        worker_id = str(worker.get("worker_id", ""))
        worker_projection = project_host_work(
            supervisor_bundle=supervisor_bundle,
            now_ms=now_ms,
            operation_allowlist=as_list(worker.get("shared_operation_allowlist")),
        )
        worker_jobs: set[str] = set()
        for raw in as_list(worker_projection.get("candidates")):
            item = mapping(raw)
            if item.get("eligible") is not True:
                continue
            job_id = str(item.get("job_id", ""))
            state_digest = str(item.get("job_state_digest", ""))
            key = candidate_key(job_id=job_id, job_state_digest_value=state_digest)
            if job_id and key not in dead_letters:
                worker_jobs.add(job_id)
        worker_eligible_job_ids[worker_id] = sorted(worker_jobs)
        assignable_job_ids.update(worker_jobs)

    max_assignments = max(1, int(policy.get("max_assignments_per_cycle", 1) or 1))
    healthy_worker_count = len(worker_order)
    eligible_count = len(assignable_job_ids)
    capacity = min(max_assignments, healthy_worker_count, eligible_count)
    deferred = max(0, eligible_count - capacity)
    pressure = _backpressure(
        queued_count=queued_count,
        eligible_count=eligible_count,
        healthy_worker_count=healthy_worker_count,
        dispatch_capacity=capacity,
        high_watermark=max(1, int(policy.get("queue_high_watermark", 1) or 1)),
    )

    status = BLOCKED if blockers else IDLE if queued_count == 0 else READY
    packet = {
        "version": PLAN_VERSION,
        "status": status,
        "cycle_id": str(cycle_id),
        "planned_at_ms": max(0, int(now_ms)),
        "source_supervisor_bundle_digest": source_bundle_digest,
        "source_orchestrator_state_digest": str(orchestrator_state.get("orchestrator_state_digest", "")),
        "host_license_digest": str(host_license.get("host_license_digest", "")),
        "orchestrator_policy_digest": str(policy.get("orchestrator_policy_digest", "")),
        "worker_report_digests": sorted(str(report.get("worker_report_digest", "")) for report in reports),
        "worker_health": health,
        "ordered_worker_ids": [str(item.get("worker_id", "")) for item in worker_order],
        "worker_eligible_job_ids": worker_eligible_job_ids,
        "queued_or_reclaimable_job_count": queued_count,
        "eligible_job_count": eligible_count,
        "healthy_worker_count": healthy_worker_count,
        "dispatch_capacity": capacity,
        "deferred_eligible_count": deferred,
        "backpressure_class": pressure,
        "base_projection_digest": str(base_projection.get("projection_digest", "")),
        "blockers": blockers,
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "orchestrator_plan_digest": "",
    }
    packet["orchestrator_plan_digest"] = plan_digest(packet)
    return packet
