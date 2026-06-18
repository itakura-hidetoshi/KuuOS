from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, mapping
from runtime.kuuos_durable_host_orchestrator_state_v0_18 import active_dead_letter_keys, reseal_orchestrator_state
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    DEAD_LETTER_RELEASE_VERSION,
    DEAD_LETTER_VERSION,
    PERMANENT_CANDIDATE_BLOCKERS,
    candidate_key,
    dead_letter_digest,
    dead_letter_release_digest,
)


def observe_structural_candidates(
    state: Mapping[str, Any],
    *,
    candidates: Sequence[Mapping[str, Any]],
    cycle_id: str,
    now_ms: int,
    threshold: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    packet = deepcopy(dict(state))
    observations = {str(key): dict(mapping(value)) for key, value in mapping(packet.get("candidate_observations")).items()}
    active = active_dead_letter_keys(packet)
    added: list[dict[str, Any]] = []
    limit = max(1, int(threshold))

    for raw in candidates:
        item = mapping(raw)
        state_name = str(item.get("supervisor_state", ""))
        eligibility = str(item.get("eligibility", ""))
        if state_name not in {"background_queued", "background_leased"}:
            continue
        if eligibility not in {"queued", "expired_lease", "blocked"}:
            continue
        reasons = sorted({str(reason) for reason in as_list(item.get("blockers")) if str(reason) in PERMANENT_CANDIDATE_BLOCKERS})
        if not reasons:
            continue
        job_id = str(item.get("job_id", ""))
        job_state = str(item.get("job_state_digest", ""))
        key = candidate_key(job_id=job_id, job_state_digest_value=job_state)
        current = dict(observations.get(key, {}))
        count = int(current.get("observation_count", 0) or 0) + 1
        current.update(
            {
                "candidate_key": key,
                "job_id": job_id,
                "job_state_digest": job_state,
                "observation_count": count,
                "first_seen_cycle_id": str(current.get("first_seen_cycle_id", cycle_id)),
                "last_seen_cycle_id": str(cycle_id),
                "last_seen_at_ms": max(0, int(now_ms)),
                "reasons": sorted(set(as_list(current.get("reasons"))) | set(reasons)),
            }
        )
        observations[key] = current
        if count < limit or key in active:
            continue
        record = {
            "version": DEAD_LETTER_VERSION,
            "candidate_key": key,
            "job_id": job_id,
            "job_state_digest": job_state,
            "observation_count": count,
            "threshold": limit,
            "reasons": current["reasons"],
            "created_cycle_id": str(cycle_id),
            "created_at_ms": max(0, int(now_ms)),
            "dead_letter_digest": "",
        }
        record["dead_letter_digest"] = dead_letter_digest(record)
        packet["dead_letters"] = as_list(packet.get("dead_letters")) + [record]
        active.add(key)
        added.append(record)

    packet["candidate_observations"] = observations
    return reseal_orchestrator_state(packet), added


def build_dead_letter_release(
    *,
    dead_letter: Mapping[str, Any],
    operator_command_digest: str,
    reason: str,
    released_at_ms: int,
) -> dict[str, Any]:
    digest = str(dead_letter.get("dead_letter_digest", ""))
    if not digest or digest != dead_letter_digest(dead_letter):
        raise ValueError("dead_letter_digest_invalid")
    if not str(operator_command_digest).strip():
        raise ValueError("operator_command_digest_missing")
    packet = {
        "version": DEAD_LETTER_RELEASE_VERSION,
        "dead_letter_digest": digest,
        "candidate_key": str(dead_letter.get("candidate_key", "")),
        "job_id": str(dead_letter.get("job_id", "")),
        "job_state_digest": str(dead_letter.get("job_state_digest", "")),
        "operator_command_digest": str(operator_command_digest),
        "reason": str(reason),
        "released_at_ms": max(0, int(released_at_ms)),
        "dead_letter_release_digest": "",
    }
    packet["dead_letter_release_digest"] = dead_letter_release_digest(packet)
    return packet


def apply_dead_letter_release(
    state: Mapping[str, Any],
    release: Mapping[str, Any],
) -> tuple[dict[str, Any], bool]:
    digest = str(release.get("dead_letter_release_digest", ""))
    if not digest or digest != dead_letter_release_digest(release):
        raise ValueError("dead_letter_release_digest_invalid")
    existing = {
        str(mapping(item).get("dead_letter_release_digest", ""))
        for item in as_list(state.get("dead_letter_releases"))
    }
    if digest in existing:
        return dict(state), True
    target = str(release.get("dead_letter_digest", ""))
    known = {
        str(mapping(item).get("dead_letter_digest", ""))
        for item in as_list(state.get("dead_letters"))
    }
    if target not in known:
        raise ValueError("dead_letter_release_target_unknown")
    packet = deepcopy(dict(state))
    packet["dead_letter_releases"] = as_list(packet.get("dead_letter_releases")) + [dict(release)]
    packet["generation"] = int(packet.get("generation", 0) or 0) + 1
    return reseal_orchestrator_state(packet), False
