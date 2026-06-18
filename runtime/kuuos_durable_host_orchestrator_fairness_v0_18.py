from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import READY as HOST_READY, projection_digest
from runtime.kuuos_durable_host_orchestrator_state_v0_18 import active_dead_letter_keys
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import candidate_key


def ordered_workers(
    worker_health: Sequence[Mapping[str, Any]],
    orchestrator_state: Mapping[str, Any],
) -> list[dict[str, Any]]:
    service = dict(mapping(orchestrator_state.get("worker_service_counts")))
    failures = dict(mapping(orchestrator_state.get("worker_failure_counts")))
    dispatchable = [dict(item) for item in worker_health if item.get("dispatchable") is True]
    dispatchable.sort(
        key=lambda item: (
            int(service.get(str(item.get("worker_id", "")), 0) or 0),
            int(failures.get(str(item.get("worker_id", "")), 0) or 0),
            str(item.get("worker_id", "")),
        )
    )
    return dispatchable


def _job_weight(job_id: str, policy: Mapping[str, Any]) -> float:
    weights = mapping(policy.get("job_weights"))
    try:
        weight = float(weights.get(job_id, 1.0))
    except (TypeError, ValueError):
        weight = 1.0
    return weight if weight > 0.0 else 1.0


def choose_fair_candidate(
    candidates: Sequence[Mapping[str, Any]],
    *,
    orchestrator_state: Mapping[str, Any],
    policy: Mapping[str, Any],
    excluded_job_ids: set[str] | None = None,
) -> dict[str, Any] | None:
    service = dict(mapping(orchestrator_state.get("job_service_counts")))
    last_served = dict(mapping(orchestrator_state.get("job_last_served_cycle")))
    dead_letters = active_dead_letter_keys(orchestrator_state)
    excluded = set(excluded_job_ids or set())
    eligible: list[dict[str, Any]] = []
    for raw in candidates:
        item = dict(raw)
        if item.get("eligible") is not True:
            continue
        job_id = str(item.get("job_id", ""))
        state_digest = str(item.get("job_state_digest", ""))
        if not job_id or job_id in excluded:
            continue
        if candidate_key(job_id=job_id, job_state_digest_value=state_digest) in dead_letters:
            continue
        eligible.append(item)
    if not eligible:
        return None
    eligible.sort(
        key=lambda item: (
            float(service.get(str(item.get("job_id", "")), 0) or 0)
            / _job_weight(str(item.get("job_id", "")), policy),
            int(last_served.get(str(item.get("job_id", "")), -1) or -1),
            str(item.get("job_id", "")),
        )
    )
    return eligible[0]


def build_fair_host_projection(
    *,
    supervisor_bundle: Mapping[str, Any],
    now_ms: int,
    operation_allowlist: Sequence[str],
    orchestrator_state: Mapping[str, Any],
    policy: Mapping[str, Any],
    excluded_job_ids: set[str] | None = None,
) -> dict[str, Any] | None:
    base = project_host_work(
        supervisor_bundle=supervisor_bundle,
        now_ms=now_ms,
        operation_allowlist=operation_allowlist,
    )
    selected = choose_fair_candidate(
        as_list(base.get("candidates")),
        orchestrator_state=orchestrator_state,
        policy=policy,
        excluded_job_ids=excluded_job_ids,
    )
    if selected is None:
        return None
    packet = deepcopy(dict(base))
    packet.update(
        {
            "status": HOST_READY,
            "adapter_state": "work_ready",
            "selected_job_id": str(selected.get("job_id", "")),
            "selected_job_state_digest": str(selected.get("job_state_digest", "")),
            "selected_ticket_id": str(selected.get("ticket_id", "")),
            "selected_ticket_digest": str(selected.get("ticket_digest", "")),
            "selected_checkpoint_digest": str(selected.get("checkpoint_digest", "")),
            "selected_step_id": str(selected.get("step_id", "")),
            "selected_operation_id": str(selected.get("operation_id", "")),
            "selection_reason": "v018_weighted_least_served:" + str(selected.get("eligibility", "")),
            "projection_digest": "",
        }
    )
    packet["projection_digest"] = projection_digest(packet)
    return packet
