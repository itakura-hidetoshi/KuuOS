from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.v016_command_history import record
from runtime.v016_store_probe import store_command as store_job_command


def store_command(bundle: Mapping[str, Any], command: Mapping[str, Any], policy: Mapping[str, Any], max_history: int = 512) -> tuple[dict[str, Any], bool]:
    packet, replayed = store_job_command(bundle, command, policy, max_history)
    if replayed:
        return packet, True
    result_job = find_job(packet, str(command.get("job_id", "")))
    digest = str(command.get("command_digest", ""))
    return record(packet, command, result_job, digest, max_history), False
