from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_execution_supervisor_slice_v0_16 import run_supervisor_slice
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_execution_supervisor_worker_v0_16 import claim_background_job, commit_background_slice
from runtime.kuuos_cooperative_host_adapter_license_v0_17 import validate_host_license
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    BLOCKED,
    NON_AUTHORITY_FLAGS,
    PROJECTION_VERSION,
    READY,
    RECEIPT_VERSION,
    REPLAYED,
    REQUIRED_BOUNDARY,
    TICK_VERSION,
    invocation_digest,
    projection_digest,
    receipt_digest,
    tick_digest,
)


def _effective_policy(supervisor_policy: Mapping[str, Any], license_packet: Mapping[str, Any]) -> dict[str, Any]:
    policy = dict(supervisor_policy)
    licensed_steps = max(1, int(license_packet.get("max_steps_per_slice", 1) or 1))
    requested_steps = max(1, int(policy.get("max_steps_per_slice", licensed_steps) or licensed_steps))
    policy["max_steps_per_slice"] = min(licensed_steps, requested_steps)
    licensed_cost = max(0.0, float(license_packet.get("max_cost_per_slice", 0.0) or 0.0))
    raw_requested_cost = policy.get("max_cost_per_slice")
    requested_cost = licensed_cost if raw_requested_cost is None else max(0.0, float(raw_requested_cost))
    policy["max_cost_per_slice"] = min(licensed_cost, requested_cost)
    policy["background_worker_available"] = True
    policy["background_handoff_enabled"] = True
    return policy


def _projection_blockers(
    bundle: Mapping[str, Any],
    projection: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    registry: Mapping[str, Executor],
) -> list[str]:
    blockers: list[str] = []
    if str(projection.get("version", "")) != PROJECTION_VERSION:
        blockers.append("host_projection_version_invalid")
    digest = str(projection.get("projection_digest", ""))
    if not digest or digest != projection_digest(projection):
        blockers.append("host_projection_digest_invalid")
    source_digest = str(bundle.get("supervisor_bundle_digest", ""))
    if not source_digest or source_digest != bundle_digest(bundle):
        blockers.append("supervisor_bundle_digest_invalid")
    if str(projection.get("source_supervisor_bundle_digest", "")) != source_digest:
        blockers.append("host_projection_source_bundle_mismatch")
    if str(projection.get("adapter_state", "")) != "work_ready":
        blockers.append("host_projection_work_not_ready")
    job_id = str(projection.get("selected_job_id", ""))
    try:
        job = find_job(bundle, job_id)
    except ValueError:
        blockers.append("selected_job_not_found")
        return blockers
    if str(job.get("job_state_digest", "")) != str(projection.get("selected_job_state_digest", "")):
        blockers.append("selected_job_state_mismatch")
    ticket = dict(mapping(job.get("active_continuation_ticket")))
    if str(ticket.get("ticket_id", "")) != str(projection.get("selected_ticket_id", "")):
        blockers.append("selected_ticket_id_mismatch")
    if str(ticket.get("background_ticket_digest", "")) != str(projection.get("selected_ticket_digest", "")):
        blockers.append("selected_ticket_digest_mismatch")
    if str(ticket.get("checkpoint_digest", "")) != str(projection.get("selected_checkpoint_digest", "")):
        blockers.append("selected_checkpoint_digest_mismatch")
    step = next_step(job)
    if step is None:
        blockers.append("selected_next_step_missing")
        return blockers
    if str(step.get("step_id", "")) != str(projection.get("selected_step_id", "")):
        blockers.append("selected_step_id_mismatch")
    operation_id = str(step.get("operation_id", ""))
    if operation_id != str(projection.get("selected_operation_id", "")):
        blockers.append("selected_operation_id_mismatch")
    allowed = {str(item) for item in as_list(license_packet.get("operation_allowlist"))}
    if operation_id not in allowed:
        blockers.append("selected_operation_not_licensed")
    if not callable(registry.get(operation_id)):
        blockers.append("selected_operation_executor_unavailable")
    return blockers


def _seal_bundle_history(
    bundle: Mapping[str, Any],
    *,
    invocation: str,
    worker_id: str,
    projection: Mapping[str, Any],
    slice_packet: Mapping[str, Any],
    max_history: int = 512,
) -> dict[str, Any]:
    packet = deepcopy(dict(bundle))
    limit = max(1, int(max_history))
    processed = {str(item) for item in as_list(packet.get("processed_host_invocation_digests"))}
    processed.add(invocation)
    history = as_list(packet.get("host_adapter_history")) + [
        {
            "version": TICK_VERSION,
            "invocation_digest": invocation,
            "worker_id": str(worker_id),
            "projection_digest": projection.get("projection_digest", ""),
            "job_id": projection.get("selected_job_id", ""),
            "slice_digest": slice_packet.get("slice_digest", ""),
            "result_job_state_digest": slice_packet.get("result_job_state_digest", ""),
            "supervisor_state": slice_packet.get("supervisor_state", ""),
            "completed_step_ids_in_slice": slice_packet.get("completed_step_ids_in_slice", []),
        }
    ]
    packet["generation"] = integer(packet.get("generation"), 0) + 1
    packet["processed_host_invocation_digests"] = sorted(processed)
    packet["host_adapter_history"] = history[-limit:]
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet


def _receipt(
    *,
    status: str,
    invocation: str,
    worker_id: str,
    projection: Mapping[str, Any],
    source_bundle_digest: str,
    result_bundle_digest: str,
    blockers: list[str],
    replayed: bool,
    slice_packet: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    packet = {
        "version": RECEIPT_VERSION,
        "status": status,
        "invocation_digest": invocation,
        "worker_id": str(worker_id),
        "projection_digest": str(projection.get("projection_digest", "")),
        "job_id": str(projection.get("selected_job_id", "")),
        "source_supervisor_bundle_digest": str(source_bundle_digest),
        "result_supervisor_bundle_digest": str(result_bundle_digest),
        "slice_digest": str((slice_packet or {}).get("slice_digest", "")),
        "supervisor_state": str((slice_packet or {}).get("supervisor_state", "")),
        "completed_step_ids_in_slice": list((slice_packet or {}).get("completed_step_ids_in_slice", [])),
        "replayed": bool(replayed),
        "blockers": list(blockers),
        "one_job_claimed_at_most": True,
        "one_bounded_slice_run_at_most": True,
        **NON_AUTHORITY_FLAGS,
        "host_receipt_digest": "",
    }
    packet["host_receipt_digest"] = receipt_digest(packet)
    return packet


def run_host_tick(
    *,
    supervisor_bundle: Mapping[str, Any],
    projection: Mapping[str, Any],
    host_license: Mapping[str, Any],
    worker_id: str,
    invocation_id: str,
    now_ms: int,
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
) -> dict[str, Any]:
    source_bundle_digest = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
    invocation = invocation_digest(
        invocation_id=str(invocation_id),
        source_bundle_digest=source_bundle_digest,
        projection=str(projection.get("projection_digest", "")),
        worker_id=str(worker_id),
    )
    processed = {str(item) for item in as_list(supervisor_bundle.get("processed_host_invocation_digests"))}
    if invocation in processed:
        receipt = _receipt(
            status=REPLAYED,
            invocation=invocation,
            worker_id=worker_id,
            projection=projection,
            source_bundle_digest=source_bundle_digest,
            result_bundle_digest=source_bundle_digest,
            blockers=[],
            replayed=True,
        )
        packet = {
            "version": TICK_VERSION,
            "status": REPLAYED,
            "adapter_state": "replayed",
            "invocation_digest": invocation,
            "result_supervisor_bundle": deepcopy(dict(supervisor_bundle)),
            "slice_packet": {},
            "receipt": receipt,
            "blockers": [],
            "boundary": dict(REQUIRED_BOUNDARY),
            **NON_AUTHORITY_FLAGS,
            "host_tick_digest": "",
        }
        packet["host_tick_digest"] = tick_digest(packet)
        return packet

    blockers = validate_host_license(host_license, now_ms=now_ms)
    blockers.extend(_projection_blockers(supervisor_bundle, projection, host_license, registry))
    if blockers:
        receipt = _receipt(
            status=BLOCKED,
            invocation=invocation,
            worker_id=worker_id,
            projection=projection,
            source_bundle_digest=source_bundle_digest,
            result_bundle_digest=source_bundle_digest,
            blockers=blockers,
            replayed=False,
        )
        packet = {
            "version": TICK_VERSION,
            "status": BLOCKED,
            "adapter_state": "blocked_before_claim",
            "invocation_digest": invocation,
            "result_supervisor_bundle": deepcopy(dict(supervisor_bundle)),
            "slice_packet": {},
            "receipt": receipt,
            "blockers": blockers,
            "boundary": dict(REQUIRED_BOUNDARY),
            **NON_AUTHORITY_FLAGS,
            "host_tick_digest": "",
        }
        packet["host_tick_digest"] = tick_digest(packet)
        return packet

    try:
        claimed_bundle, claimed = claim_background_job(
            supervisor_bundle,
            job_id=str(projection.get("selected_job_id", "")),
            worker_id=str(worker_id),
            now_ms=max(0, int(now_ms)),
            lease_duration_ms=int(host_license.get("lease_duration_ms", 1) or 1),
        )
        if not claimed:
            raise ValueError("selected_ticket_claim_failed")
        policy = _effective_policy(supervisor_policy, host_license)
        leased_job = find_job(claimed_bundle, str(projection.get("selected_job_id", "")))
        slice_packet = run_supervisor_slice(
            job=leased_job,
            slice_id="host-v017-" + invocation[:20],
            mode="background",
            policy=policy,
            registry=registry,
        )
        committed_bundle, slice_replayed = commit_background_slice(
            claimed_bundle,
            slice_packet,
            worker_id=str(worker_id),
        )
        if slice_replayed:
            raise ValueError("unexpected_background_slice_replay")
        result_bundle = _seal_bundle_history(
            committed_bundle,
            invocation=invocation,
            worker_id=worker_id,
            projection=projection,
            slice_packet=slice_packet,
        )
        blockers = []
        status = READY
        adapter_state = "completed" if str(slice_packet.get("supervisor_state", "")) == "completed" else "slice_committed"
    except ValueError as error:
        blockers = [str(error)]
        slice_packet = {}
        result_bundle = deepcopy(dict(supervisor_bundle))
        status = BLOCKED
        adapter_state = "blocked_during_host_tick"

    receipt = _receipt(
        status=status,
        invocation=invocation,
        worker_id=worker_id,
        projection=projection,
        source_bundle_digest=source_bundle_digest,
        result_bundle_digest=str(result_bundle.get("supervisor_bundle_digest", "")),
        blockers=blockers,
        replayed=False,
        slice_packet=slice_packet,
    )
    packet = {
        "version": TICK_VERSION,
        "status": status,
        "adapter_state": adapter_state,
        "invocation_digest": invocation,
        "effective_policy": _effective_policy(supervisor_policy, host_license) if not blockers else {},
        "result_supervisor_bundle": result_bundle,
        "slice_packet": slice_packet,
        "receipt": receipt,
        "blockers": blockers,
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "host_tick_digest": "",
    }
    packet["host_tick_digest"] = tick_digest(packet)
    return packet
