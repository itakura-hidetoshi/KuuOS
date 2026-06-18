from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_host_adapter_idempotent_tick_v0_17 import run_host_tick
from runtime.kuuos_cooperative_host_adapter_license_v0_17 import validate_host_license
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    BLOCKED as HOST_BLOCKED,
    READY as HOST_READY,
    REPLAYED as HOST_REPLAYED,
)
from runtime.kuuos_durable_host_orchestrator_dead_letter_v0_18 import observe_structural_candidates
from runtime.kuuos_durable_host_orchestrator_fairness_v0_18 import build_fair_host_projection
from runtime.kuuos_durable_host_orchestrator_policy_v0_18 import validate_orchestrator_policy
from runtime.kuuos_durable_host_orchestrator_state_v0_18 import (
    reseal_orchestrator_state,
    validate_orchestrator_state,
)
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    BLOCKED,
    CYCLE_VERSION,
    IDLE,
    NON_AUTHORITY_FLAGS,
    PLAN_VERSION,
    READY,
    RECEIPT_VERSION,
    REPLAYED,
    REQUIRED_BOUNDARY,
    cycle_digest,
    plan_digest,
    receipt_digest,
)
from runtime.kuuos_durable_host_orchestrator_worker_v0_18 import classify_worker_health


def _receipt(
    *,
    status: str,
    plan: Mapping[str, Any],
    source_bundle_digest: str,
    result_bundle_digest: str,
    source_state_digest: str,
    result_state_digest: str,
    assignments: list[dict[str, Any]],
    dead_letters_added: list[dict[str, Any]],
    blockers: list[str],
    replayed: bool,
) -> dict[str, Any]:
    packet = {
        "version": RECEIPT_VERSION,
        "status": status,
        "cycle_id": str(plan.get("cycle_id", "")),
        "orchestrator_plan_digest": str(plan.get("orchestrator_plan_digest", "")),
        "source_supervisor_bundle_digest": source_bundle_digest,
        "result_supervisor_bundle_digest": result_bundle_digest,
        "source_orchestrator_state_digest": source_state_digest,
        "result_orchestrator_state_digest": result_state_digest,
        "assignment_count": len(assignments),
        "assignments": assignments,
        "dead_letters_added": dead_letters_added,
        "backpressure_class": str(plan.get("backpressure_class", "")),
        "dispatch_capacity": int(plan.get("dispatch_capacity", 0) or 0),
        "replayed": bool(replayed),
        "blockers": blockers,
        **NON_AUTHORITY_FLAGS,
        "orchestrator_receipt_digest": "",
    }
    packet["orchestrator_receipt_digest"] = receipt_digest(packet)
    return packet


def _blocked_cycle(
    *,
    plan: Mapping[str, Any],
    supervisor_bundle: Mapping[str, Any],
    orchestrator_state: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    bundle_digest_value = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
    state_digest_value = str(orchestrator_state.get("orchestrator_state_digest", ""))
    receipt = _receipt(
        status=BLOCKED,
        plan=plan,
        source_bundle_digest=bundle_digest_value,
        result_bundle_digest=bundle_digest_value,
        source_state_digest=state_digest_value,
        result_state_digest=state_digest_value,
        assignments=[],
        dead_letters_added=[],
        blockers=blockers,
        replayed=False,
    )
    packet = {
        "version": CYCLE_VERSION,
        "status": BLOCKED,
        "cycle_id": str(plan.get("cycle_id", "")),
        "orchestrator_plan_digest": str(plan.get("orchestrator_plan_digest", "")),
        "result_supervisor_bundle": deepcopy(dict(supervisor_bundle)),
        "result_orchestrator_state": deepcopy(dict(orchestrator_state)),
        "assignments": [],
        "dead_letters_added": [],
        "receipt": receipt,
        "blockers": blockers,
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "orchestrator_cycle_digest": "",
    }
    packet["orchestrator_cycle_digest"] = cycle_digest(packet)
    return packet


def run_orchestrator_cycle(
    *,
    supervisor_bundle: Mapping[str, Any],
    orchestrator_state: Mapping[str, Any],
    plan: Mapping[str, Any],
    worker_reports: Sequence[Mapping[str, Any]],
    host_license: Mapping[str, Any],
    policy: Mapping[str, Any],
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
    now_ms: int,
) -> dict[str, Any]:
    plan_key = str(plan.get("orchestrator_plan_digest", ""))
    plan_integrity_valid = (
        str(plan.get("version", "")) == PLAN_VERSION
        and bool(plan_key)
        and plan_key == plan_digest(plan)
    )
    processed = {str(item) for item in as_list(orchestrator_state.get("processed_plan_digests"))}
    if plan_integrity_valid and plan_key in processed:
        bundle_digest_value = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
        state_digest_value = str(orchestrator_state.get("orchestrator_state_digest", ""))
        receipt = _receipt(
            status=REPLAYED,
            plan=plan,
            source_bundle_digest=str(plan.get("source_supervisor_bundle_digest", "")),
            result_bundle_digest=bundle_digest_value,
            source_state_digest=str(plan.get("source_orchestrator_state_digest", "")),
            result_state_digest=state_digest_value,
            assignments=[],
            dead_letters_added=[],
            blockers=[],
            replayed=True,
        )
        packet = {
            "version": CYCLE_VERSION,
            "status": REPLAYED,
            "cycle_id": str(plan.get("cycle_id", "")),
            "orchestrator_plan_digest": plan_key,
            "result_supervisor_bundle": deepcopy(dict(supervisor_bundle)),
            "result_orchestrator_state": deepcopy(dict(orchestrator_state)),
            "assignments": [],
            "dead_letters_added": [],
            "receipt": receipt,
            "blockers": [],
            "boundary": dict(REQUIRED_BOUNDARY),
            **NON_AUTHORITY_FLAGS,
            "orchestrator_cycle_digest": "",
        }
        packet["orchestrator_cycle_digest"] = cycle_digest(packet)
        return packet

    blockers: list[str] = []
    if str(plan.get("version", "")) != PLAN_VERSION:
        blockers.append("orchestrator_plan_version_invalid")
    if not plan_key or plan_key != plan_digest(plan):
        blockers.append("orchestrator_plan_digest_invalid")
    if str(plan.get("status", "")) == BLOCKED:
        blockers.append("orchestrator_plan_blocked")
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
    source_state_digest = str(orchestrator_state.get("orchestrator_state_digest", ""))
    if not source_bundle_digest or source_bundle_digest != bundle_digest(supervisor_bundle):
        blockers.append("supervisor_bundle_digest_invalid")
    if str(plan.get("source_supervisor_bundle_digest", "")) != source_bundle_digest:
        blockers.append("orchestrator_plan_source_bundle_mismatch")
    if str(plan.get("source_orchestrator_state_digest", "")) != source_state_digest:
        blockers.append("orchestrator_plan_source_state_mismatch")
    if str(plan.get("host_license_digest", "")) != str(host_license.get("host_license_digest", "")):
        blockers.append("orchestrator_plan_host_license_mismatch")
    if str(plan.get("orchestrator_policy_digest", "")) != str(policy.get("orchestrator_policy_digest", "")):
        blockers.append("orchestrator_plan_policy_mismatch")

    report_ids = [str(report.get("worker_id", "")) for report in worker_reports]
    if len(report_ids) != len(set(report_ids)):
        blockers.append("duplicate_worker_id")
    report_digests = sorted(str(report.get("worker_report_digest", "")) for report in worker_reports)
    if report_digests != sorted(str(item) for item in as_list(plan.get("worker_report_digests"))):
        blockers.append("orchestrator_plan_worker_reports_mismatch")
    if blockers:
        return _blocked_cycle(
            plan=plan,
            supervisor_bundle=supervisor_bundle,
            orchestrator_state=orchestrator_state,
            blockers=blockers,
        )

    licensed = {str(item) for item in as_list(host_license.get("operation_allowlist")) if str(item)}
    registered = {str(key) for key, value in registry.items() if callable(value)}
    union_operations = sorted(licensed & registered)
    structural_projection = project_host_work(
        supervisor_bundle=supervisor_bundle,
        now_ms=now_ms,
        operation_allowlist=union_operations,
    )
    working_state, dead_letters_added = observe_structural_candidates(
        orchestrator_state,
        candidates=[mapping(item) for item in as_list(structural_projection.get("candidates"))],
        cycle_id=str(plan.get("cycle_id", "")),
        now_ms=now_ms,
        threshold=max(1, int(policy.get("dead_letter_observation_threshold", 1) or 1)),
    )

    report_map = {str(report.get("worker_id", "")): dict(report) for report in worker_reports}
    health_map = {
        worker_id: classify_worker_health(
            report,
            now_ms=now_ms,
            policy=policy,
            licensed_operations=licensed,
            registered_operations=registered,
        )
        for worker_id, report in report_map.items()
    }
    current_bundle = deepcopy(dict(supervisor_bundle))
    assignments: list[dict[str, Any]] = []
    dispatched_jobs: set[str] = set()
    dispatched_workers: set[str] = set()
    ordered_worker_ids: list[str] = []
    for raw_worker_id in as_list(plan.get("ordered_worker_ids")):
        worker_id = str(raw_worker_id)
        if worker_id and worker_id not in ordered_worker_ids:
            ordered_worker_ids.append(worker_id)
    policy_capacity = max(1, int(policy.get("max_assignments_per_cycle", 1) or 1))
    capacity = min(
        max(0, int(plan.get("dispatch_capacity", 0) or 0)),
        policy_capacity,
        len(ordered_worker_ids),
    )
    next_cycle_index = int(working_state.get("cycle_index", 0) or 0) + 1

    job_service = dict(mapping(working_state.get("job_service_counts")))
    job_last = dict(mapping(working_state.get("job_last_served_cycle")))
    worker_service = dict(mapping(working_state.get("worker_service_counts")))
    worker_failures = dict(mapping(working_state.get("worker_failure_counts")))

    for worker_id in ordered_worker_ids:
        if len(assignments) >= capacity:
            break
        if worker_id in dispatched_workers:
            continue
        health = health_map.get(worker_id, {})
        if health.get("dispatchable") is not True:
            continue
        projection = build_fair_host_projection(
            supervisor_bundle=current_bundle,
            now_ms=now_ms,
            operation_allowlist=as_list(health.get("shared_operation_allowlist")),
            orchestrator_state={
                **working_state,
                "job_service_counts": job_service,
                "job_last_served_cycle": job_last,
            },
            policy=policy,
            excluded_job_ids=dispatched_jobs,
        )
        if projection is None:
            continue
        job_id = str(projection.get("selected_job_id", ""))
        invocation_id = f"{plan.get('cycle_id', '')}:{len(assignments) + 1}:{worker_id}:{job_id}"
        tick = run_host_tick(
            supervisor_bundle=current_bundle,
            projection=projection,
            host_license=host_license,
            worker_id=worker_id,
            invocation_id=invocation_id,
            now_ms=now_ms,
            supervisor_policy=supervisor_policy,
            registry=registry,
        )
        host_status = str(tick.get("status", ""))
        assignment = {
            "assignment_index": len(assignments),
            "worker_id": worker_id,
            "job_id": job_id,
            "step_id": str(projection.get("selected_step_id", "")),
            "operation_id": str(projection.get("selected_operation_id", "")),
            "host_projection_digest": str(projection.get("projection_digest", "")),
            "host_tick_digest": str(tick.get("host_tick_digest", "")),
            "host_status": host_status,
            "host_adapter_state": str(tick.get("adapter_state", "")),
            "host_blockers": list(as_list(tick.get("blockers"))),
        }
        assignments.append(assignment)
        dispatched_jobs.add(job_id)
        dispatched_workers.add(worker_id)
        if host_status == HOST_READY:
            current_bundle = deepcopy(dict(mapping(tick.get("result_supervisor_bundle"))))
            job_service[job_id] = int(job_service.get(job_id, 0) or 0) + 1
            job_last[job_id] = next_cycle_index
            worker_service[worker_id] = int(worker_service.get(worker_id, 0) or 0) + 1
            worker_failures[worker_id] = 0
        elif host_status == HOST_BLOCKED:
            worker_failures[worker_id] = int(worker_failures.get(worker_id, 0) or 0) + 1
        elif host_status == HOST_REPLAYED:
            pass

    working_state["job_service_counts"] = job_service
    working_state["job_last_served_cycle"] = job_last
    working_state["worker_service_counts"] = worker_service
    working_state["worker_failure_counts"] = worker_failures
    working_state["cycle_index"] = next_cycle_index
    working_state["generation"] = int(working_state.get("generation", 0) or 0) + 1
    working_state["processed_plan_digests"] = sorted(processed | {plan_key})
    limit = max(1, int(policy.get("max_history", 512) or 512))
    working_state["cycle_history"] = (
        as_list(working_state.get("cycle_history"))
        + [
            {
                "cycle_id": str(plan.get("cycle_id", "")),
                "orchestrator_plan_digest": plan_key,
                "assignment_count": len(assignments),
                "assigned_worker_ids": [item["worker_id"] for item in assignments],
                "assigned_job_ids": [item["job_id"] for item in assignments],
                "backpressure_class": str(plan.get("backpressure_class", "")),
                "dead_letter_digests_added": [item.get("dead_letter_digest", "") for item in dead_letters_added],
                "result_supervisor_bundle_digest": str(current_bundle.get("supervisor_bundle_digest", "")),
            }
        ]
    )[-limit:]
    working_state = reseal_orchestrator_state(working_state)

    status = READY if assignments else IDLE
    receipt = _receipt(
        status=status,
        plan=plan,
        source_bundle_digest=source_bundle_digest,
        result_bundle_digest=str(current_bundle.get("supervisor_bundle_digest", "")),
        source_state_digest=source_state_digest,
        result_state_digest=str(working_state.get("orchestrator_state_digest", "")),
        assignments=assignments,
        dead_letters_added=dead_letters_added,
        blockers=[],
        replayed=False,
    )
    packet = {
        "version": CYCLE_VERSION,
        "status": status,
        "cycle_id": str(plan.get("cycle_id", "")),
        "orchestrator_plan_digest": plan_key,
        "effective_dispatch_capacity": capacity,
        "result_supervisor_bundle": current_bundle,
        "result_orchestrator_state": working_state,
        "assignments": assignments,
        "dead_letters_added": dead_letters_added,
        "receipt": receipt,
        "blockers": [],
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "orchestrator_cycle_digest": "",
    }
    packet["orchestrator_cycle_digest"] = cycle_digest(packet)
    return packet
