from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import validate_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import BUNDLE_VERSION, bundle_digest


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
