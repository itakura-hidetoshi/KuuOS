from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import reseal_job, validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import COMMAND_VERSION, command_digest


def _validate(job: Mapping[str, Any], command: Mapping[str, Any]) -> str:
    if str(command.get("version", "")) != COMMAND_VERSION:
        raise ValueError("supervisor_command_version_invalid")
    digest = str(command.get("command_digest", ""))
    if not digest or digest != command_digest(command):
        raise ValueError("supervisor_command_digest_invalid")
    if str(command.get("job_id", "")) != str(job.get("job_id", "")):
        raise ValueError("supervisor_command_job_mismatch")
    if str(command.get("source_job_state_digest", "")) != str(job.get("job_state_digest", "")):
        raise ValueError("supervisor_command_source_state_mismatch")
    return digest


def apply_command(job: Mapping[str, Any], command: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    validate_job(job)
    digest = _validate(job, command)
    processed = {str(item) for item in as_list(job.get("processed_command_digests"))}
    if digest in processed:
        return dict(job), True
    packet = deepcopy(dict(job))
    action = str(command.get("action", ""))
    payload = dict(mapping(command.get("payload")))
    return reseal_job(packet), False
