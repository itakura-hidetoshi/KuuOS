from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import commit_slice, find_job
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import reseal_job, validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_resumable_execution_handoff_ticket_v0_15 import claim_background_ticket, finish_background_ticket, heartbeat_background_ticket


def _replace_job(bundle: Mapping[str, Any], job: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(bundle))
    jobs = [dict(mapping(item)) for item in as_list(bundle.get("jobs"))]
    for index, existing in enumerate(jobs):
        if str(existing.get("job_id", "")) == str(job.get("job_id", "")):
            jobs[index] = deepcopy(dict(job))
            packet["jobs"] = jobs
            return packet
    raise ValueError("supervisor_job_not_found")


def _seal_worker_update(bundle: Mapping[str, Any], job: Mapping[str, Any], ticket: Mapping[str, Any], event: str, max_history: int = 512) -> dict[str, Any]:
    limit = max(1, int(max_history))
    packet = _replace_job(bundle, job)
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["ticket_history"] = (as_list(bundle.get("ticket_history")) + [dict(ticket)])[-limit:]
    packet["handoff_ledger"] = (as_list(bundle.get("handoff_ledger")) + [{
        "phase": "background_worker_update",
        "event": str(event),
        "job_id": job.get("job_id", ""),
        "ticket_id": ticket.get("ticket_id", ""),
        "queue_status": ticket.get("queue_status", ""),
        "lease_owner": ticket.get("lease_owner", ""),
        "job_state_digest": job.get("job_state_digest", ""),
    }])[-limit:]
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet


def claim_background_job(bundle: Mapping[str, Any], *, job_id: str, worker_id: str, now_ms: int, lease_duration_ms: int) -> tuple[dict[str, Any], bool]:
    job = find_job(bundle, job_id)
    validate_job(job)
    ticket = dict(mapping(job.get("active_continuation_ticket")))
    claimed, changed = claim_background_ticket(ticket, worker_id=worker_id, now_ms=now_ms, lease_duration_ms=lease_duration_ms)
    if not changed:
        return dict(bundle), False
    job["active_continuation_ticket"] = claimed
    job["execution_mode"] = "background"
    job["supervisor_state"] = "background_leased"
    job = reseal_job(job)
    return _seal_worker_update(bundle, job, claimed, "claimed"), True


def heartbeat_background_job(bundle: Mapping[str, Any], *, job_id: str, worker_id: str, now_ms: int, lease_duration_ms: int) -> tuple[dict[str, Any], bool]:
    job = find_job(bundle, job_id)
    ticket = dict(mapping(job.get("active_continuation_ticket")))
    updated, changed = heartbeat_background_ticket(ticket, worker_id=worker_id, now_ms=now_ms, lease_duration_ms=lease_duration_ms)
    if not changed:
        return dict(bundle), False
    job["active_continuation_ticket"] = updated
    job = reseal_job(job)
    return _seal_worker_update(bundle, job, updated, "heartbeat"), True


def commit_background_slice(bundle: Mapping[str, Any], slice_packet: Mapping[str, Any], *, worker_id: str, max_history: int = 512) -> tuple[dict[str, Any], bool]:
    current = find_job(bundle, str(slice_packet.get("job_id", "")))
    ticket = dict(mapping(current.get("active_continuation_ticket")))
    if str(ticket.get("queue_status", "")) != "leased" or str(ticket.get("lease_owner", "")) != str(worker_id):
        raise ValueError("background_worker_lease_invalid")
    closed, changed = finish_background_ticket(ticket, worker_id=worker_id, final_status="completed", summary="The leased bounded slice finished and produced a persisted supervisor state.")
    if not changed:
        raise ValueError("background_worker_ticket_close_failed")
    committed, replayed = commit_slice(bundle, slice_packet, max_history)
    if replayed:
        return committed, True
    result_job = find_job(committed, str(slice_packet.get("job_id", "")))
    return _seal_worker_update(committed, result_job, closed, "slice_closed", max_history), False
