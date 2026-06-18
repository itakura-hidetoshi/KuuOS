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


def _simple_transition(packet: dict[str, Any], action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if action == "continue_foreground":
        packet["execution_mode"] = "foreground"
        packet["supervisor_state"] = "ready"
        packet["active_continuation_ticket"] = {}
    elif action == "increase_budget":
        addition = max(0.0, float(payload.get("add_cost_units", 0.0) or 0.0))
        if addition <= 0.0:
            raise ValueError("budget_increase_must_be_positive")
        packet["remaining_budget_units"] = max(0.0, float(packet.get("remaining_budget_units", 0.0) or 0.0)) + addition
        packet["supervisor_state"] = "ready"
    elif action == "grant_permission":
        permission = str(payload.get("permission", "")).strip()
        if not permission:
            raise ValueError("permission_name_missing")
        permissions = {str(item) for item in as_list(packet.get("granted_permissions"))}
        permissions.add(permission)
        packet["granted_permissions"] = sorted(permissions)
        packet["supervisor_state"] = "ready"
    elif action == "retry_now":
        packet["supervisor_state"] = "ready"
    elif action == "retry_later":
        packet["supervisor_state"] = "retry_backoff"
    elif action == "cancel_job":
        packet["supervisor_state"] = "cancelled"
        packet["active_continuation_ticket"] = {}
    return packet


def apply_command(job: Mapping[str, Any], command: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    validate_job(job)
    digest = _validate(job, command)
    processed = {str(item) for item in as_list(job.get("processed_command_digests"))}
    if digest in processed:
        return dict(job), True
    packet = deepcopy(dict(job))
    action = str(command.get("action", ""))
    payload = dict(mapping(command.get("payload")))
    packet = _simple_transition(packet, action, payload)
    processed.add(digest)
    packet["processed_command_digests"] = sorted(processed)
    return reseal_job(packet), False
