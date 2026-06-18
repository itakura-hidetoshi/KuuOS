from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step, validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    BLOCKED,
    NON_AUTHORITY_FLAGS,
    PROJECTION_VERSION,
    READY,
    REQUIRED_BOUNDARY,
    projection_digest,
)
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import ticket_digest


def _candidate(
    job: Mapping[str, Any],
    *,
    now_ms: int,
    operation_allowlist: set[str],
) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        validate_job(job)
    except ValueError as error:
        blockers.append(str(error))
    state = str(job.get("supervisor_state", ""))
    ticket = dict(mapping(job.get("active_continuation_ticket")))
    ticket_status = str(ticket.get("queue_status", ""))
    lease_expiry = int(ticket.get("lease_expires_at_ms", 0) or 0)
    queued = state == "background_queued" and ticket_status == "queued"
    expired = state == "background_leased" and ticket_status == "leased" and lease_expiry <= max(0, int(now_ms))
    if not queued and not expired:
        blockers.append("job_not_queued_or_reclaimable")
    digest = str(ticket.get("background_ticket_digest", ""))
    if not digest or digest != ticket_digest(ticket):
        blockers.append("background_ticket_digest_invalid")
    if str(ticket.get("job_id", "")) != str(job.get("job_id", "")):
        blockers.append("background_ticket_job_mismatch")
    checkpoint = str(ticket.get("checkpoint_digest", ""))
    if not checkpoint:
        blockers.append("background_ticket_checkpoint_missing")
    if checkpoint != str(job.get("latest_checkpoint_digest", "")):
        blockers.append("background_ticket_checkpoint_mismatch")
    step = next_step(job)
    if step is None:
        blockers.append("next_step_missing")
        step = {}
    operation_id = str(step.get("operation_id", ""))
    if operation_id not in operation_allowlist:
        blockers.append("operation_not_allowlisted_by_host")
    eligibility = "queued" if queued else "expired_lease" if expired else "blocked"
    return {
        "job_id": str(job.get("job_id", "")),
        "job_state_digest": str(job.get("job_state_digest", "")),
        "supervisor_state": state,
        "eligibility": eligibility,
        "eligible": not blockers,
        "ticket_id": str(ticket.get("ticket_id", "")),
        "ticket_digest": digest,
        "ticket_status": ticket_status,
        "lease_owner": str(ticket.get("lease_owner", "")),
        "lease_expires_at_ms": lease_expiry,
        "checkpoint_digest": checkpoint,
        "step_id": str(step.get("step_id", "")),
        "operation_id": operation_id,
        "estimated_cost_units": max(0.0, float(step.get("estimated_cost_units", 0.0) or 0.0)),
        "blockers": blockers,
    }


def project_host_work(
    *,
    supervisor_bundle: Mapping[str, Any],
    now_ms: int,
    operation_allowlist: Sequence[str],
) -> dict[str, Any]:
    allowed = {str(item).strip() for item in operation_allowlist if str(item).strip()}
    global_blockers: list[str] = []
    source_digest = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
    if not source_digest or source_digest != bundle_digest(supervisor_bundle):
        global_blockers.append("supervisor_bundle_digest_invalid")
    if not allowed:
        global_blockers.append("host_operation_allowlist_empty")
    candidates = [
        _candidate(mapping(raw), now_ms=now_ms, operation_allowlist=allowed)
        for raw in as_list(supervisor_bundle.get("jobs"))
    ]
    eligible = [item for item in candidates if item.get("eligible") is True]
    eligible.sort(
        key=lambda item: (
            0 if item.get("eligibility") == "queued" else 1,
            str(item.get("job_id", "")),
            str(item.get("ticket_id", "")),
        )
    )
    selected = dict(eligible[0]) if eligible and not global_blockers else {}
    adapter_state = "work_ready" if selected else "blocked" if global_blockers else "idle"
    packet = {
        "version": PROJECTION_VERSION,
        "status": READY if selected else BLOCKED if global_blockers else "KUUOS_COOPERATIVE_HOST_ADAPTER_V0_17_IDLE",
        "adapter_state": adapter_state,
        "projected_at_ms": max(0, int(now_ms)),
        "source_supervisor_bundle_digest": source_digest,
        "candidate_count": len(candidates),
        "eligible_candidate_count": len(eligible),
        "candidates": candidates,
        "selected_job_id": str(selected.get("job_id", "")),
        "selected_job_state_digest": str(selected.get("job_state_digest", "")),
        "selected_ticket_id": str(selected.get("ticket_id", "")),
        "selected_ticket_digest": str(selected.get("ticket_digest", "")),
        "selected_checkpoint_digest": str(selected.get("checkpoint_digest", "")),
        "selected_step_id": str(selected.get("step_id", "")),
        "selected_operation_id": str(selected.get("operation_id", "")),
        "selection_reason": str(selected.get("eligibility", "")),
        "blockers": global_blockers,
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "projection_digest": "",
    }
    packet["projection_digest"] = projection_digest(packet)
    return packet
