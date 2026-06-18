from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import BUNDLE_VERSION, bundle_digest, slice_digest


def empty_supervisor_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": str(agent_id),
        "generation": 0,
        "jobs": [],
        "slice_history": [],
        "command_history": [],
        "ticket_history": [],
        "handoff_ledger": [],
        "processed_slice_digests": [],
        "processed_command_digests": [],
        "supervisor_bundle_digest": "",
    }
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet


def _replace_job(bundle: Mapping[str, Any], job: Mapping[str, Any]) -> dict[str, Any]:
    jobs = [dict(mapping(item)) for item in as_list(bundle.get("jobs"))]
    job_id = str(job.get("job_id", ""))
    replaced = False
    for index, existing in enumerate(jobs):
        if str(existing.get("job_id", "")) == job_id:
            jobs[index] = deepcopy(dict(job))
            replaced = True
            break
    if not replaced:
        jobs.append(deepcopy(dict(job)))
    jobs.sort(key=lambda item: str(item.get("job_id", "")))
    packet = deepcopy(dict(bundle))
    packet["jobs"] = jobs
    return packet


def register_job(bundle: Mapping[str, Any], job: Mapping[str, Any]) -> dict[str, Any]:
    validate_job(job)
    for raw in as_list(bundle.get("jobs")):
        if str(mapping(raw).get("job_id", "")) == str(job.get("job_id", "")):
            raise ValueError("supervisor_job_already_registered")
    packet = _replace_job(bundle, job)
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["handoff_ledger"] = as_list(bundle.get("handoff_ledger")) + [
        {
            "phase": "job_registered",
            "job_id": job.get("job_id", ""),
            "job_state_digest": job.get("job_state_digest", ""),
        }
    ]
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet


def find_job(bundle: Mapping[str, Any], job_id: str) -> dict[str, Any]:
    for raw in as_list(bundle.get("jobs")):
        item = dict(mapping(raw))
        if str(item.get("job_id", "")) == str(job_id):
            return item
    raise ValueError("supervisor_job_not_found")


def commit_slice(bundle: Mapping[str, Any], slice_packet: Mapping[str, Any], max_history: int = 512) -> tuple[dict[str, Any], bool]:
    digest = str(slice_packet.get("slice_digest", ""))
    if not digest or digest != slice_digest(slice_packet):
        raise ValueError("supervisor_slice_digest_invalid")
    processed = {str(item) for item in as_list(bundle.get("processed_slice_digests"))}
    if digest in processed:
        return dict(bundle), True
    current = find_job(bundle, str(slice_packet.get("job_id", "")))
    if str(slice_packet.get("source_job_state_digest", "")) != str(current.get("job_state_digest", "")):
        raise ValueError("supervisor_slice_source_state_mismatch")
    result_job = dict(mapping(slice_packet.get("result_job")))
    validate_job(result_job)
    if str(slice_packet.get("result_job_state_digest", "")) != str(result_job.get("job_state_digest", "")):
        raise ValueError("supervisor_slice_result_state_mismatch")
    limit = max(1, int(max_history))
    packet = _replace_job(bundle, result_job)
    history = as_list(bundle.get("slice_history")) + [
        {
            "slice_id": slice_packet.get("slice_id", ""),
            "slice_digest": digest,
            "job_id": slice_packet.get("job_id", ""),
            "source_job_state_digest": slice_packet.get("source_job_state_digest", ""),
            "result_job_state_digest": slice_packet.get("result_job_state_digest", ""),
            "execution_mode": slice_packet.get("execution_mode", ""),
            "supervisor_state": slice_packet.get("supervisor_state", ""),
            "completed_step_ids_in_slice": slice_packet.get("completed_step_ids_in_slice", []),
            "spent_cost_units": slice_packet.get("spent_cost_units", 0.0),
        }
    ]
    tickets = as_list(bundle.get("ticket_history"))
    raw_ticket = slice_packet.get("background_ticket", {})
    if isinstance(raw_ticket, Mapping) and raw_ticket:
        tickets = tickets + [dict(raw_ticket)]
    ledger = as_list(bundle.get("handoff_ledger")) + [
        {
            "phase": "slice_committed",
            "job_id": slice_packet.get("job_id", ""),
            "slice_digest": digest,
            "result_job_state_digest": slice_packet.get("result_job_state_digest", ""),
            "supervisor_state": slice_packet.get("supervisor_state", ""),
        }
    ]
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["slice_history"] = history[-limit:]
    packet["ticket_history"] = tickets[-limit:]
    packet["handoff_ledger"] = ledger[-limit:]
    packet["processed_slice_digests"] = sorted(processed | {digest})
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet, False
