from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_cooperative_execution_command_apply_v016 import apply_command
from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest, command_digest


def _replace_job(bundle: Mapping[str, Any], job: Mapping[str, Any]) -> dict[str, Any]:
    jobs = [dict(mapping(item)) for item in as_list(bundle.get("jobs"))]
    job_id = str(job.get("job_id", ""))
    for index, existing in enumerate(jobs):
        if str(existing.get("job_id", "")) == job_id:
            jobs[index] = deepcopy(dict(job))
            break
    else:
        jobs.append(deepcopy(dict(job)))
    jobs.sort(key=lambda item: str(item.get("job_id", "")))
    packet = deepcopy(dict(bundle))
    packet["jobs"] = jobs
    return packet


def store_command(bundle: Mapping[str, Any], command: Mapping[str, Any], policy: Mapping[str, Any], max_history: int = 512) -> tuple[dict[str, Any], bool]:
    digest = str(command.get("command_digest", ""))
    if not digest or digest != command_digest(command):
        raise ValueError("supervisor_command_digest_invalid")
    processed = {str(item) for item in as_list(bundle.get("processed_command_digests"))}
    if digest in processed:
        return dict(bundle), True

    current = find_job(bundle, str(command.get("job_id", "")))
    result_job, replayed = apply_command(current, command, policy)
    if replayed:
        return dict(bundle), True
    validate_job(result_job)

    limit = max(1, int(max_history))
    packet = _replace_job(bundle, result_job)
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["command_history"] = (as_list(bundle.get("command_history")) + [{
        "command_id": command.get("command_id", ""),
        "command_digest": digest,
        "job_id": command.get("job_id", ""),
        "action": command.get("action", ""),
        "source_job_state_digest": command.get("source_job_state_digest", ""),
        "result_job_state_digest": result_job.get("job_state_digest", ""),
    }])[-limit:]
    tickets = as_list(bundle.get("ticket_history"))
    active_ticket = result_job.get("active_continuation_ticket", {})
    if isinstance(active_ticket, Mapping) and active_ticket:
        tickets = tickets + [dict(active_ticket)]
    packet["ticket_history"] = tickets[-limit:]
    packet["handoff_ledger"] = (as_list(bundle.get("handoff_ledger")) + [{
        "phase": "command_committed",
        "job_id": command.get("job_id", ""),
        "command_digest": digest,
        "action": command.get("action", ""),
        "result_job_state_digest": result_job.get("job_state_digest", ""),
    }])[-limit:]
    packet["processed_command_digests"] = sorted(processed | {digest})
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet, False
