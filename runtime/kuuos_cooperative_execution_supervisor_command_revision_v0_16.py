from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping, sha
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import next_step, reseal_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import manifest_digest


def _reseal_manifest(job: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(job))
    packet["manifest_revision"] = int(packet.get("manifest_revision", 0) or 0) + 1
    packet["manifest_digest"] = ""
    packet["manifest_digest"] = manifest_digest(packet)
    return reseal_job(packet)


def revise_future_input(job: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(job))
    steps = [dict(mapping(item)) for item in as_list(packet.get("steps"))]
    index = int(packet.get("current_step_index", 0) or 0)
    target_id = str(payload.get("step_id", "")) or str((next_step(packet) or {}).get("step_id", ""))
    new_input = dict(mapping(payload.get("operation_input")))
    changed = False
    for position in range(index, len(steps)):
        if str(steps[position].get("step_id", "")) != target_id:
            continue
        steps[position]["operation_input"] = new_input
        steps[position]["operation_input_digest"] = sha(new_input)
        changed = True
        break
    if not changed:
        raise ValueError("future_step_for_revision_not_found")
    packet["steps"] = steps
    packet["supervisor_state"] = "ready"
    return _reseal_manifest(packet)


def reduce_future_scope(job: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(job))
    steps = [dict(mapping(item)) for item in as_list(packet.get("steps"))]
    index = int(packet.get("current_step_index", 0) or 0)
    completed_prefix = steps[:index]
    remaining = steps[index:]
    keep = {str(item) for item in as_list(payload.get("keep_step_ids"))}
    drop = {str(item) for item in as_list(payload.get("drop_step_ids"))}
    if keep:
        remaining = [step for step in remaining if str(step.get("step_id", "")) in keep]
    if drop:
        remaining = [step for step in remaining if str(step.get("step_id", "")) not in drop]
    if not keep and not drop:
        raise ValueError("scope_change_selector_missing")
    packet["steps"] = completed_prefix + remaining
    packet["supervisor_state"] = "ready"
    return _reseal_manifest(packet)
