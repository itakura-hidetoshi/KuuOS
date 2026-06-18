from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import COMMAND_ACTIONS, COMMAND_VERSION, command_digest


def build_supervisor_command(*, job_id: str, command_id: str, action: str, payload: Mapping[str, Any], source_job_state_digest: str) -> dict[str, Any]:
    if str(action) not in COMMAND_ACTIONS:
        raise ValueError("supervisor_command_action_invalid")
    packet = {
        "version": COMMAND_VERSION,
        "job_id": str(job_id),
        "command_id": str(command_id),
        "action": str(action),
        "payload": dict(payload),
        "source_job_state_digest": str(source_job_state_digest),
        "command_digest": "",
    }
    packet["command_digest"] = command_digest(packet)
    return packet
