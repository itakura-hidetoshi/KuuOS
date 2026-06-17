from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping, sha
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import (
    JOB_VERSION,
    job_state_digest,
    manifest_digest,
)


def normalize_step(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
    step = dict(mapping(raw))
    step_id = str(step.get("step_id", "")).strip() or f"step-{index + 1}"
    operation_id = str(step.get("operation_id", "")).strip()
    if not operation_id:
        raise ValueError("operation_id_missing")
    estimated = max(0.0, float(step.get("estimated_cost_units", 0.0) or 0.0))
    maximum_attempts = max(1, integer(step.get("max_attempts"), 1))
    operation_input = dict(mapping(step.get("operation_input")))
    return {
        "step_id": step_id,
        "operation_id": operation_id,
        "operation_input": operation_input,
        "operation_input_digest": sha(operation_input),
        "estimated_cost_units": estimated,
        "max_attempts": maximum_attempts,
        "required_permission": str(step.get("required_permission", "")),
    }


def create_supervised_job(
    *,
    job_id: str,
    source_parent_digest: str,
    steps: Sequence[Mapping[str, Any]],
    initial_budget_units: float,
    granted_permissions: Sequence[str] = (),
) -> dict[str, Any]:
    key = str(job_id).strip()
    if not key:
        raise ValueError("job_id_missing")
    normalized = [normalize_step(step, index) for index, step in enumerate(steps)]
    if not normalized:
        raise ValueError("job_steps_missing")
    step_ids = [step["step_id"] for step in normalized]
    if len(step_ids) != len(set(step_ids)):
        raise ValueError("duplicate_step_id")
    packet = {
        "version": JOB_VERSION,
        "job_id": key,
        "source_parent_digest": str(source_parent_digest),
        "manifest_revision": 1,
        "steps": normalized,
        "manifest_digest": "",
        "current_step_index": 0,
        "completed_step_ids": [],
        "step_receipts": [],
        "step_attempts": {},
        "execution_mode": "foreground",
        "supervisor_state": "ready",
        "remaining_budget_units": max(0.0, float(initial_budget_units)),
        "granted_permissions": sorted({str(item) for item in granted_permissions if str(item)}),
        "latest_checkpoint_digest": "",
        "latest_feedback_digest": "",
        "active_continuation_ticket": {},
        "last_slice_digest": "",
        "last_slice_summary": {},
        "processed_command_digests": [],
        "generation": 0,
        "job_state_digest": "",
    }
    packet["manifest_digest"] = manifest_digest(packet)
    packet["job_state_digest"] = job_state_digest(packet)
    return packet


def validate_job(job: Mapping[str, Any]) -> None:
    if str(job.get("version", "")) != JOB_VERSION:
        raise ValueError("job_version_invalid")
    if str(job.get("manifest_digest", "")) != manifest_digest(job):
        raise ValueError("job_manifest_digest_invalid")
    if str(job.get("job_state_digest", "")) != job_state_digest(job):
        raise ValueError("job_state_digest_invalid")
    steps = [dict(mapping(item)) for item in as_list(job.get("steps"))]
    index = integer(job.get("current_step_index"), 0)
    if index < 0 or index > len(steps):
        raise ValueError("job_current_step_index_invalid")
    completed = [str(item) for item in as_list(job.get("completed_step_ids"))]
    if completed != [str(step.get("step_id", "")) for step in steps[:index]]:
        raise ValueError("job_completed_prefix_invalid")


def reseal_job(job: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(job))
    packet["generation"] = integer(packet.get("generation"), 0) + 1
    packet["job_state_digest"] = ""
    packet["job_state_digest"] = job_state_digest(packet)
    return packet


def next_step(job: Mapping[str, Any]) -> dict[str, Any] | None:
    steps = [dict(mapping(item)) for item in as_list(job.get("steps"))]
    index = integer(job.get("current_step_index"), 0)
    if index >= len(steps):
        return None
    return steps[index]
