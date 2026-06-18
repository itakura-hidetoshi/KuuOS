from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    STATE_VERSION,
    orchestrator_state_digest,
)


def empty_orchestrator_state(orchestrator_id: str) -> dict[str, Any]:
    packet = {
        "version": STATE_VERSION,
        "orchestrator_id": str(orchestrator_id),
        "generation": 0,
        "cycle_index": 0,
        "job_service_counts": {},
        "job_last_served_cycle": {},
        "worker_service_counts": {},
        "worker_failure_counts": {},
        "candidate_observations": {},
        "dead_letters": [],
        "dead_letter_releases": [],
        "processed_plan_digests": [],
        "cycle_history": [],
        "orchestrator_state_digest": "",
    }
    packet["orchestrator_state_digest"] = orchestrator_state_digest(packet)
    return packet


def validate_orchestrator_state(state: Mapping[str, Any]) -> None:
    if str(state.get("version", "")) != STATE_VERSION:
        raise ValueError("orchestrator_state_version_invalid")
    digest = str(state.get("orchestrator_state_digest", ""))
    if not digest or digest != orchestrator_state_digest(state):
        raise ValueError("orchestrator_state_digest_invalid")
    if not str(state.get("orchestrator_id", "")).strip():
        raise ValueError("orchestrator_id_missing")
    if int(state.get("generation", 0) or 0) < 0:
        raise ValueError("orchestrator_generation_invalid")
    if int(state.get("cycle_index", 0) or 0) < 0:
        raise ValueError("orchestrator_cycle_index_invalid")
    for field in [
        "job_service_counts",
        "job_last_served_cycle",
        "worker_service_counts",
        "worker_failure_counts",
        "candidate_observations",
    ]:
        if not isinstance(state.get(field, {}), Mapping):
            raise ValueError(f"{field}_invalid")
    for field in ["dead_letters", "dead_letter_releases", "processed_plan_digests", "cycle_history"]:
        if not isinstance(state.get(field, []), list):
            raise ValueError(f"{field}_invalid")


def reseal_orchestrator_state(state: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(state))
    packet["orchestrator_state_digest"] = ""
    packet["orchestrator_state_digest"] = orchestrator_state_digest(packet)
    return packet


def active_dead_letter_keys(state: Mapping[str, Any]) -> set[str]:
    released = {
        str(mapping(item).get("dead_letter_digest", ""))
        for item in as_list(state.get("dead_letter_releases"))
        if str(mapping(item).get("dead_letter_digest", ""))
    }
    active: set[str] = set()
    for raw in as_list(state.get("dead_letters")):
        item = mapping(raw)
        digest = str(item.get("dead_letter_digest", ""))
        key = str(item.get("candidate_key", ""))
        if digest and key and digest not in released:
            active.add(key)
    return active
