from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_mission_contract_types_v0_20 import sha, validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state

VERSION = "kuuos_observation_belief_state_kernel_v0_21"
OBSERVATION_VERSION = "kuuos_epistemic_observation_v0_21"
STATE_VERSION = "kuuos_observation_belief_state_v0_21"
UPDATE_RESULT_VERSION = "kuuos_observation_belief_update_result_v0_21"
REQUEST_VERSION = "kuuos_observation_request_v0_21"

EVIDENCE_RELATIONS = frozenset({"supports", "opposes", "unknown"})
CLAIM_STATUSES = frozenset(
    {"observed_positive", "observed_negative", "unknown", "contradicted", "stale"}
)

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_final_commitment_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "unknown_is_not_false": True,
    "missing_evidence_is_not_negative_evidence": True,
    "belief_is_not_truth_authority": True,
    "observation_history_is_append_only": True,
    "contradiction_residue_remains_visible": True,
    "stale_claim_is_not_silently_current": True,
    "local_chart_is_preserved": True,
    "mission_binding_is_exact": True,
    "lower_execution_authority_is_preserved": True,
    "root_overwrite_is_forbidden": True,
    "graph_semantics_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def observation_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observation_digest"))


def claim_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "claim_digest"))


def request_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observation_request_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observation_belief_state_digest"))


def update_result_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "belief_update_result_digest"))


def _require_nonempty(value: Any, name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name}_missing")
    return text


def _require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0:
        raise ValueError(f"{name}_negative")
    return result


def _require_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence_invalid") from exc
    if not math.isfinite(confidence):
        raise ValueError("confidence_not_finite")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence_out_of_range")
    return confidence


def _require_unique_strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = False
) -> list[str]:
    normalized = [_require_nonempty(value, name) for value in values]
    if not allow_empty and not normalized:
        raise ValueError(f"{name}_missing")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name}_duplicate")
    return normalized


def _source_errors(
    contract: Mapping[str, Any], mission_state: Mapping[str, Any]
) -> list[str]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    if mission_state.get("lifecycle_state") != "active":
        errors.append("mission_not_active")
    return errors


def build_observation(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    observation_id: str,
    chart_id: str,
    claim_id: str,
    proposition: str,
    relation: str,
    source_id: str,
    source_kind: str,
    raw_artifact_digest: str,
    provenance_digests: Sequence[str],
    observed_at_ms: int,
    valid_until_ms: int,
    confidence: float,
    inference_rule_digest: str = "",
) -> dict[str, Any]:
    errors = _source_errors(contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    normalized_relation = _require_nonempty(relation, "relation")
    if normalized_relation not in EVIDENCE_RELATIONS:
        raise ValueError("relation_invalid")
    observed_at = _require_nonnegative_int(observed_at_ms, "observed_at_ms")
    valid_until = _require_nonnegative_int(valid_until_ms, "valid_until_ms")
    if valid_until < observed_at:
        raise ValueError("validity_interval_invalid")
    packet = {
        "version": OBSERVATION_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "observation_id": _require_nonempty(observation_id, "observation_id"),
        "chart_id": _require_nonempty(chart_id, "chart_id"),
        "claim_id": _require_nonempty(claim_id, "claim_id"),
        "proposition": _require_nonempty(proposition, "proposition"),
        "relation": normalized_relation,
        "source_id": _require_nonempty(source_id, "source_id"),
        "source_kind": _require_nonempty(source_kind, "source_kind"),
        "raw_artifact_digest": _require_nonempty(
            raw_artifact_digest, "raw_artifact_digest"
        ),
        "provenance_digests": _require_unique_strings(
            provenance_digests, "provenance_digests"
        ),
        "observed_at_ms": observed_at,
        "valid_until_ms": valid_until,
        "confidence": _require_confidence(confidence),
        "inference_rule_digest": str(inference_rule_digest),
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "observation_digest": "",
    }
    packet["observation_digest"] = observation_digest(packet)
    return packet


def validate_observation(
    observation: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
) -> list[str]:
    errors = _source_errors(contract, mission_state)
    if observation.get("version") != OBSERVATION_VERSION:
        errors.append("observation_version_invalid")
    if observation.get("mission_id") != contract.get("mission_id"):
        errors.append("observation_mission_mismatch")
    if observation.get("lineage_id") != contract.get("lineage_id"):
        errors.append("observation_lineage_mismatch")
    if observation.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("observation_contract_mismatch")
    if observation.get("source_mission_state_digest") != mission_state.get(
        "mission_state_digest"
    ):
        errors.append("observation_mission_state_stale")
    for field in (
        "observation_id",
        "chart_id",
        "claim_id",
        "proposition",
        "source_id",
        "source_kind",
        "raw_artifact_digest",
    ):
        if not str(observation.get(field, "")).strip():
            errors.append(f"observation_{field}_missing")
    if observation.get("relation") not in EVIDENCE_RELATIONS:
        errors.append("observation_relation_invalid")
    try:
        observed_at = _require_nonnegative_int(
            observation.get("observed_at_ms"), "observed_at_ms"
        )
        valid_until = _require_nonnegative_int(
            observation.get("valid_until_ms"), "valid_until_ms"
        )
        if valid_until < observed_at:
            errors.append("observation_validity_interval_invalid")
        _require_confidence(observation.get("confidence"))
        provenance = observation.get("provenance_digests", [])
        if not isinstance(provenance, list) or not provenance:
            errors.append("observation_provenance_missing")
        elif len(provenance) != len(set(str(item) for item in provenance)):
            errors.append("observation_provenance_duplicate")
    except ValueError as exc:
        errors.append(str(exc))
    if dict(observation.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("observation_non_authority_invalid")
    if observation.get("observation_digest") != observation_digest(observation):
        errors.append("observation_digest_invalid")
    return errors


def build_initial_belief_state(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    chart_id: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = _source_errors(contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    state = {
        "version": STATE_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "mission_state_digest": mission_state["mission_state_digest"],
        "chart_id": _require_nonempty(chart_id, "chart_id"),
        "revision": 0,
        "claims": {},
        "observation_history": [],
        "processed_observation_digests": [],
        "contradiction_residues": [],
        "staleness_residues": [],
        "observation_requests": [],
        "updated_at_ms": _require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": deepcopy(NON_AUTHORITY_FLAGS),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "observation_belief_state_digest": "",
    }
    state["observation_belief_state_digest"] = state_digest(state)
    return state


def _validate_claim(claim: Mapping[str, Any], chart_id: str) -> list[str]:
    errors: list[str] = []
    if claim.get("chart_id") != chart_id:
        errors.append("claim_chart_mismatch")
    if claim.get("status") not in CLAIM_STATUSES:
        errors.append("claim_status_invalid")
    for field in ("claim_id", "proposition", "chart_id"):
        if not str(claim.get(field, "")).strip():
            errors.append(f"claim_{field}_missing")
    for field in (
        "support_evidence_digests",
        "oppose_evidence_digests",
        "unknown_evidence_digests",
    ):
        values = claim.get(field)
        if not isinstance(values, list):
            errors.append(f"claim_{field}_invalid")
        elif len(values) != len(set(str(item) for item in values)):
            errors.append(f"claim_{field}_duplicate")
    try:
        _require_confidence(claim.get("confidence"))
        _require_nonnegative_int(claim.get("last_observed_at_ms"), "last_observed_at_ms")
        _require_nonnegative_int(claim.get("valid_until_ms"), "valid_until_ms")
    except ValueError as exc:
        errors.append(str(exc))
    if claim.get("claim_digest") != claim_digest(claim):
        errors.append("claim_digest_invalid")
    return errors


def validate_belief_state(
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
) -> list[str]:
    errors = _source_errors(contract, mission_state)
    if state.get("version") != STATE_VERSION:
        errors.append("belief_state_version_invalid")
    for field, expected in (
        ("mission_id", contract.get("mission_id")),
        ("lineage_id", contract.get("lineage_id")),
        ("contract_digest", contract.get("mission_contract_digest")),
        ("mission_state_digest", mission_state.get("mission_state_digest")),
    ):
        if state.get(field) != expected:
            errors.append(f"belief_state_{field}_mismatch")
    if not str(state.get("chart_id", "")).strip():
        errors.append("belief_state_chart_missing")
    try:
        _require_nonnegative_int(state.get("revision"), "revision")
        _require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")
    except ValueError as exc:
        errors.append(str(exc))
    claims = state.get("claims")
    if not isinstance(claims, Mapping):
        errors.append("belief_state_claims_invalid")
    else:
        for key, claim in claims.items():
            if str(key) != str(claim.get("claim_id", "")):
                errors.append("belief_state_claim_key_mismatch")
            errors.extend(_validate_claim(claim, str(state.get("chart_id", ""))))
    history = state.get("observation_history")
    processed = state.get("processed_observation_digests")
    if not isinstance(history, list):
        errors.append("belief_state_history_invalid")
    if not isinstance(processed, list):
        errors.append("belief_state_processed_invalid")
    elif len(processed) != len(set(str(item) for item in processed)):
        errors.append("belief_state_processed_duplicate")
    if isinstance(history, list) and isinstance(processed, list):
        history_digests = [str(item.get("observation_digest", "")) for item in history]
        if history_digests != [str(item) for item in processed]:
            errors.append("belief_state_history_processed_mismatch")
        for item in history:
            errors.extend(
                "history:" + error
                for error in validate_observation(item, contract, mission_state)
            )
    for field in (
        "contradiction_residues",
        "staleness_residues",
        "observation_requests",
    ):
        if not isinstance(state.get(field), list):
            errors.append(f"belief_state_{field}_invalid")
    if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("belief_state_non_authority_invalid")
    if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("belief_state_boundary_invalid")
    if state.get("observation_belief_state_digest") != state_digest(state):
        errors.append("belief_state_digest_invalid")
    return errors


def _new_claim(observation: Mapping[str, Any]) -> dict[str, Any]:
    relation = str(observation["relation"])
    claim = {
        "claim_id": observation["claim_id"],
        "proposition": observation["proposition"],
        "chart_id": observation["chart_id"],
        "status": "unknown",
        "prior_status": "",
        "support_evidence_digests": [],
        "oppose_evidence_digests": [],
        "unknown_evidence_digests": [],
        "confidence": float(observation["confidence"]),
        "last_observed_at_ms": int(observation["observed_at_ms"]),
        "valid_until_ms": int(observation["valid_until_ms"]),
        "claim_digest": "",
    }
    target = (
        "support_evidence_digests"
        if relation == "supports"
        else "oppose_evidence_digests"
        if relation == "opposes"
        else "unknown_evidence_digests"
    )
    claim[target].append(observation["observation_digest"])
    claim["status"] = (
        "observed_positive"
        if relation == "supports"
        else "observed_negative"
        if relation == "opposes"
        else "unknown"
    )
    claim["claim_digest"] = claim_digest(claim)
    return claim


def _request_for_claim(
    *, state: Mapping[str, Any], claim: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    request = {
        "version": REQUEST_VERSION,
        "mission_id": state["mission_id"],
        "lineage_id": state["lineage_id"],
        "contract_digest": state["contract_digest"],
        "chart_id": state["chart_id"],
        "claim_id": claim["claim_id"],
        "proposition": claim["proposition"],
        "trigger_status": claim["status"],
        "requested_relation": "disambiguating_evidence",
        "created_at_ms": now_ms,
        "request_grants_execution": False,
        "observation_request_digest": "",
    }
    request["observation_request_digest"] = request_digest(request)
    return request


def _append_request_if_needed(
    state: dict[str, Any], claim: Mapping[str, Any], now_ms: int
) -> None:
    if claim.get("status") not in {"unknown", "contradicted", "stale"}:
        return
    if any(
        item.get("claim_id") == claim.get("claim_id")
        and item.get("trigger_status") == claim.get("status")
        for item in state["observation_requests"]
    ):
        return
    state["observation_requests"].append(
        _request_for_claim(state=state, claim=claim, now_ms=now_ms)
    )


def apply_observation(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> dict[str, Any]:
    state_errors = validate_belief_state(belief_state, contract, mission_state)
    if state_errors:
        raise ValueError(";".join(state_errors))
    observation_errors = validate_observation(observation, contract, mission_state)
    if observation_errors:
        raise ValueError(";".join(observation_errors))
    if observation.get("chart_id") != belief_state.get("chart_id"):
        raise ValueError("observation_chart_mismatch")
    digest_value = str(observation["observation_digest"])
    if digest_value in set(
        str(item) for item in belief_state["processed_observation_digests"]
    ):
        result = {
            "version": UPDATE_RESULT_VERSION,
            "status": "REPLAYED",
            "observation_digest": digest_value,
            "previous_state_digest": belief_state["observation_belief_state_digest"],
            "result_state_digest": belief_state["observation_belief_state_digest"],
            "result_state": deepcopy(dict(belief_state)),
            "belief_update_result_digest": "",
        }
        result["belief_update_result_digest"] = update_result_digest(result)
        return result

    state = deepcopy(dict(belief_state))
    claims = deepcopy(dict(state["claims"]))
    claim_id = str(observation["claim_id"])
    existing = deepcopy(dict(claims.get(claim_id, {})))
    if not existing:
        claim = _new_claim(observation)
    else:
        if existing.get("proposition") != observation.get("proposition"):
            raise ValueError("claim_proposition_mismatch")
        if existing.get("chart_id") != observation.get("chart_id"):
            raise ValueError("claim_chart_mismatch")
        claim = existing
        claim["prior_status"] = claim["status"]
        relation = str(observation["relation"])
        target = (
            "support_evidence_digests"
            if relation == "supports"
            else "oppose_evidence_digests"
            if relation == "opposes"
            else "unknown_evidence_digests"
        )
        claim[target] = list(claim[target]) + [digest_value]
        has_support = bool(claim["support_evidence_digests"])
        has_oppose = bool(claim["oppose_evidence_digests"])
        claim["status"] = (
            "contradicted"
            if has_support and has_oppose
            else "observed_positive"
            if has_support
            else "observed_negative"
            if has_oppose
            else "unknown"
        )
        claim["confidence"] = max(
            float(claim["confidence"]), float(observation["confidence"])
        )
        claim["last_observed_at_ms"] = max(
            int(claim["last_observed_at_ms"]), int(observation["observed_at_ms"])
        )
        claim["valid_until_ms"] = max(
            int(claim["valid_until_ms"]), int(observation["valid_until_ms"])
        )
        claim["claim_digest"] = ""
        claim["claim_digest"] = claim_digest(claim)

    claims[claim_id] = claim
    state["claims"] = claims
    state["observation_history"] = list(state["observation_history"]) + [
        deepcopy(dict(observation))
    ]
    state["processed_observation_digests"] = list(
        state["processed_observation_digests"]
    ) + [digest_value]
    state["revision"] = int(state["revision"]) + 1
    state["updated_at_ms"] = max(
        int(state["updated_at_ms"]), int(observation["observed_at_ms"])
    )
    if claim["status"] == "contradicted":
        residue = {
            "claim_id": claim_id,
            "chart_id": state["chart_id"],
            "support_evidence_digests": list(claim["support_evidence_digests"]),
            "oppose_evidence_digests": list(claim["oppose_evidence_digests"]),
            "created_at_ms": state["updated_at_ms"],
        }
        residue["contradiction_residue_digest"] = sha(residue)
        if residue["contradiction_residue_digest"] not in {
            item.get("contradiction_residue_digest")
            for item in state["contradiction_residues"]
        }:
            state["contradiction_residues"] = list(
                state["contradiction_residues"]
            ) + [residue]
    _append_request_if_needed(state, claim, state["updated_at_ms"])
    state["observation_belief_state_digest"] = ""
    state["observation_belief_state_digest"] = state_digest(state)

    result = {
        "version": UPDATE_RESULT_VERSION,
        "status": "APPLIED",
        "observation_digest": digest_value,
        "previous_state_digest": belief_state["observation_belief_state_digest"],
        "result_state_digest": state["observation_belief_state_digest"],
        "result_state": state,
        "belief_update_result_digest": "",
    }
    result["belief_update_result_digest"] = update_result_digest(result)
    return result


def mark_stale_claims(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_belief_state(belief_state, contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    now = _require_nonnegative_int(now_ms, "now_ms")
    state = deepcopy(dict(belief_state))
    changed = False
    claims = deepcopy(dict(state["claims"]))
    for claim_id, original in list(claims.items()):
        claim = deepcopy(dict(original))
        if claim["status"] != "stale" and int(claim["valid_until_ms"]) < now:
            claim["prior_status"] = claim["status"]
            claim["status"] = "stale"
            claim["claim_digest"] = ""
            claim["claim_digest"] = claim_digest(claim)
            claims[claim_id] = claim
            residue = {
                "claim_id": claim_id,
                "chart_id": state["chart_id"],
                "prior_status": claim["prior_status"],
                "valid_until_ms": claim["valid_until_ms"],
                "stale_at_ms": now,
            }
            residue["staleness_residue_digest"] = sha(residue)
            state["staleness_residues"] = list(state["staleness_residues"]) + [
                residue
            ]
            _append_request_if_needed(state, claim, now)
            changed = True
    if changed:
        state["claims"] = claims
        state["revision"] = int(state["revision"]) + 1
        state["updated_at_ms"] = max(int(state["updated_at_ms"]), now)
        state["observation_belief_state_digest"] = ""
        state["observation_belief_state_digest"] = state_digest(state)
    return {
        "status": "STALE_APPLIED" if changed else "NO_CHANGE",
        "previous_state_digest": belief_state["observation_belief_state_digest"],
        "result_state_digest": state["observation_belief_state_digest"],
        "result_state": state,
    }


__all__ = [
    "CLAIM_STATUSES",
    "EVIDENCE_RELATIONS",
    "NON_AUTHORITY_FLAGS",
    "REQUIRED_BOUNDARY",
    "VERSION",
    "apply_observation",
    "build_initial_belief_state",
    "build_observation",
    "claim_digest",
    "mark_stale_claims",
    "observation_digest",
    "state_digest",
    "validate_belief_state",
    "validate_observation",
]
