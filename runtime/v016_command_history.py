from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest


def record(bundle: Mapping[str, Any], command: Mapping[str, Any], result_job: Mapping[str, Any], digest: str, max_history: int = 512) -> dict[str, Any]:
    limit = max(1, int(max_history))
    packet = deepcopy(dict(bundle))
    history = as_list(bundle.get("command_history")) + [
        {
            "command_id": command.get("command_id", ""),
            "command_digest": digest,
            "job_id": command.get("job_id", ""),
            "action": command.get("action", ""),
            "source_job_state_digest": command.get("source_job_state_digest", ""),
            "result_job_state_digest": result_job.get("job_state_digest", ""),
        }
    ]
    tickets = as_list(bundle.get("ticket_history"))
    active_ticket = result_job.get("active_continuation_ticket", {})
    if isinstance(active_ticket, Mapping) and active_ticket:
        tickets = tickets + [dict(active_ticket)]
    ledger = as_list(bundle.get("handoff_ledger")) + [
        {
            "phase": "command_committed",
            "job_id": command.get("job_id", ""),
            "command_digest": digest,
            "action": command.get("action", ""),
            "result_job_state_digest": result_job.get("job_state_digest", ""),
        }
    ]
    processed = {str(item) for item in as_list(bundle.get("processed_command_digests"))}
    processed.add(str(digest))
    packet["generation"] = integer(bundle.get("generation"), 0) + 1
    packet["command_history"] = history[-limit:]
    packet["ticket_history"] = tickets[-limit:]
    packet["handoff_ledger"] = ledger[-limit:]
    packet["processed_command_digests"] = sorted(processed)
    packet["supervisor_bundle_digest"] = ""
    packet["supervisor_bundle_digest"] = bundle_digest(packet)
    return packet
