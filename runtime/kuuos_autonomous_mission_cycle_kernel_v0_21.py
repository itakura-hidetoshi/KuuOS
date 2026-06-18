from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_autonomous_mission_cycle_types_v0_21 import (
    APPLY_RESULT_VERSION,
    ARTIFACT_KIND,
    EVENT_VERSION,
    NEXT_PHASE,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    VERIFICATION_VERDICTS,
    apply_result_digest,
    copy_non_authority,
    empty_artifact_digests,
    event_digest,
    require_finite_number,
    require_nonempty_string,
    require_nonnegative_int,
    require_unique_strings,
    state_digest,
)
from runtime.kuuos_mission_contract_types_v0_20 import validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state


def _validate_source(
    contract: Mapping[str, Any], mission_state: Mapping[str, Any]
) -> list[str]:
    errors = validate_mission_contract(contract)
    if errors:
        return ["contract:" + item for item in errors]
    state_errors = validate_mission_state(mission_state, contract)
    if state_errors:
        return ["mission_state:" + item for item in state_errors]
    if mission_state.get("lifecycle_state") != "active":
        errors.append("mission_not_active")
    return errors


def build_initial_mission_cycle_state(
    *, contract: Mapping[str, Any], mission_state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    errors = _validate_source(contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    now = require_nonnegative_int(now_ms, "now_ms")
    initial_cost = require_finite_number(
        mission_state.get("used_cost", 0.0), "used_cost", minimum=0.0
    )
    state = {
        "version": STATE_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "mission_state_digest": mission_state["mission_state_digest"],
        "predecessor_cycle_state_digest": "",
        "cycle_index": 0,
        "current_phase": "mission",
        "phase_index": 0,
        "event_count": 0,
        "completed_cycles": 0,
        "cycle_cost": 0.0,
        "cumulative_cost": initial_cost,
        "artifact_digests": empty_artifact_digests(
            mission_contract_digest=contract["mission_contract_digest"]
        ),
        "latest_verification_verdict": "",
        "processed_event_digests": [],
        "event_history": [],
        "cycle_summaries": [],
        "updated_at_ms": now,
        "non_authority": copy_non_authority(),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "mission_cycle_state_digest": "",
    }
    state["mission_cycle_state_digest"] = state_digest(state)
    return state


def validate_mission_cycle_state(
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
) -> list[str]:
    errors = _validate_source(contract, mission_state)
    if state.get("version") != STATE_VERSION:
        errors.append("cycle_state_version_invalid")
    if state.get("mission_id") != contract.get("mission_id"):
        errors.append("cycle_state_mission_mismatch")
    if state.get("lineage_id") != contract.get("lineage_id"):
        errors.append("cycle_state_lineage_mismatch")
    if state.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("cycle_state_contract_mismatch")
    if state.get("current_phase") not in PHASES:
        errors.append("cycle_state_phase_invalid")
    verdict = str(state.get("latest_verification_verdict", ""))
    if verdict and verdict not in VERIFICATION_VERDICTS:
        errors.append("cycle_state_verification_verdict_invalid")
    try:
        cycle_index = require_nonnegative_int(state.get("cycle_index"), "cycle_index")
        phase_index = require_nonnegative_int(state.get("phase_index"), "phase_index")
        event_count = require_nonnegative_int(state.get("event_count"), "event_count")
        completed = require_nonnegative_int(
            state.get("completed_cycles"), "completed_cycles"
        )
        cycle_cost = require_finite_number(
            state.get("cycle_cost"), "cycle_cost", minimum=0.0
        )
        cumulative_cost = require_finite_number(
            state.get("cumulative_cost"), "cumulative_cost", minimum=0.0
        )
        require_nonnegative_int(state.get("updated_at_ms"), "updated_at_ms")
        if completed != cycle_index:
            errors.append("completed_cycle_index_mismatch")
        if phase_index != event_count:
            errors.append("phase_event_index_mismatch")
        if cycle_cost > cumulative_cost:
            errors.append("cycle_cost_exceeds_cumulative")
    except ValueError as exc:
        errors.append(str(exc))
    artifacts = state.get("artifact_digests")
    if not isinstance(artifacts, Mapping) or set(artifacts) != set(PHASES):
        errors.append("artifact_digest_map_invalid")
    elif artifacts.get("mission") != contract.get("mission_contract_digest"):
        errors.append("mission_artifact_digest_invalid")
    processed = state.get("processed_event_digests")
    history = state.get("event_history")
    summaries = state.get("cycle_summaries")
    if not isinstance(processed, list):
        errors.append("processed_events_invalid")
    elif len(processed) != len(set(str(item) for item in processed)):
        errors.append("processed_events_duplicate")
    if not isinstance(history, list) or len(history) != int(state.get("event_count", -1)):
        errors.append("event_history_length_invalid")
    if not isinstance(summaries, list) or len(summaries) != int(
        state.get("completed_cycles", -1)
    ):
        errors.append("cycle_summary_length_invalid")
    if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("cycle_state_non_authority_invalid")
    if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("cycle_state_boundary_invalid")
    if state.get("mission_cycle_state_digest") != state_digest(state):
        errors.append("mission_cycle_state_digest_invalid")
    return errors


def _validate_phase_metadata(to_phase: str, metadata: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if to_phase == "act":
        for field in ("action_receipt_digest", "lower_authority_receipt_digest"):
            if not str(metadata.get(field, "")).strip():
                errors.append(f"act_{field}_missing")
        if metadata.get("licensed_effect_applied") is not True:
            errors.append("act_licensed_effect_receipt_required")
    elif to_phase == "verify":
        if metadata.get("verdict") not in VERIFICATION_VERDICTS:
            errors.append("verification_verdict_invalid")
        if not str(metadata.get("verification_evidence_digest", "")).strip():
            errors.append("verification_evidence_digest_missing")
    elif to_phase == "learn":
        if metadata.get("future_only") is not True:
            errors.append("learning_must_be_future_only")
        if metadata.get("memory_overwrite") is not False:
            errors.append("learning_memory_overwrite_forbidden")
    elif to_phase == "replan":
        if not str(metadata.get("next_plan_basis_digest", "")).strip():
            errors.append("replan_basis_digest_missing")
    return errors


def build_mission_cycle_event(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    cycle_state: Mapping[str, Any],
    artifact_digest: str,
    actor_id: str,
    actor_role: str,
    issued_at_ms: int,
    cost: float = 0.0,
    artifact_refs: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    errors = validate_mission_cycle_state(cycle_state, contract, mission_state)
    if errors:
        raise ValueError(";".join(errors))
    from_phase = str(cycle_state["current_phase"])
    to_phase = NEXT_PHASE[from_phase]
    normalized_metadata = deepcopy(dict(metadata or {}))
    metadata_errors = _validate_phase_metadata(to_phase, normalized_metadata)
    if metadata_errors:
        raise ValueError(";".join(metadata_errors))
    packet = {
        "version": EVENT_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_cycle_state_digest": cycle_state["mission_cycle_state_digest"],
        "cycle_index": int(cycle_state["cycle_index"]),
        "from_phase": from_phase,
        "to_phase": to_phase,
        "artifact_kind": ARTIFACT_KIND[to_phase],
        "artifact_digest": require_nonempty_string(
            artifact_digest, "artifact_digest"
        ),
        "artifact_refs": require_unique_strings(
            artifact_refs, "artifact_refs", allow_empty=True
        ),
        "metadata": normalized_metadata,
        "actor_id": require_nonempty_string(actor_id, "actor_id"),
        "actor_role": require_nonempty_string(actor_role, "actor_role"),
        "issued_at_ms": require_nonnegative_int(issued_at_ms, "issued_at_ms"),
        "cost": require_finite_number(cost, "cost", minimum=0.0),
        "non_authority": copy_non_authority(),
        "mission_cycle_event_digest": "",
    }
    packet["mission_cycle_event_digest"] = event_digest(packet)
    return packet


def validate_mission_cycle_event(
    event: Mapping[str, Any],
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    cycle_state: Mapping[str, Any],
) -> list[str]:
    errors = validate_mission_cycle_state(cycle_state, contract, mission_state)
    if event.get("version") != EVENT_VERSION:
        errors.append("cycle_event_version_invalid")
    if event.get("mission_id") != contract.get("mission_id"):
        errors.append("cycle_event_mission_mismatch")
    if event.get("lineage_id") != contract.get("lineage_id"):
        errors.append("cycle_event_lineage_mismatch")
    if event.get("contract_digest") != contract.get("mission_contract_digest"):
        errors.append("cycle_event_contract_mismatch")
    if event.get("source_mission_state_digest") != mission_state.get(
        "mission_state_digest"
    ):
        errors.append("cycle_event_mission_state_stale")
    if event.get("source_cycle_state_digest") != cycle_state.get(
        "mission_cycle_state_digest"
    ):
        errors.append("cycle_event_cycle_state_stale")
    from_phase = str(cycle_state.get("current_phase", ""))
    to_phase = NEXT_PHASE.get(from_phase)
    if event.get("from_phase") != from_phase:
        errors.append("cycle_event_from_phase_mismatch")
    if event.get("to_phase") != to_phase:
        errors.append("cycle_event_phase_order_invalid")
    if event.get("artifact_kind") != ARTIFACT_KIND.get(str(to_phase)):
        errors.append("cycle_event_artifact_kind_invalid")
    if int(event.get("cycle_index", -1)) != int(cycle_state.get("cycle_index", -2)):
        errors.append("cycle_event_cycle_index_mismatch")
    if not str(event.get("artifact_digest", "")).strip():
        errors.append("cycle_event_artifact_digest_missing")
    try:
        issued_at = require_nonnegative_int(event.get("issued_at_ms"), "issued_at_ms")
        if issued_at < int(cycle_state.get("updated_at_ms", 0)):
            errors.append("cycle_event_time_regression")
        require_finite_number(event.get("cost"), "cost", minimum=0.0)
        refs = event.get("artifact_refs", [])
        if not isinstance(refs, list) or len(refs) != len(set(str(x) for x in refs)):
            errors.append("cycle_event_artifact_refs_invalid")
    except ValueError as exc:
        errors.append(str(exc))
    if not str(event.get("actor_id", "")).strip() or not str(
        event.get("actor_role", "")
    ).strip():
        errors.append("cycle_event_actor_missing")
    metadata = event.get("metadata")
    if not isinstance(metadata, Mapping):
        errors.append("cycle_event_metadata_invalid")
    else:
        errors.extend(_validate_phase_metadata(str(to_phase), metadata))
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("cycle_event_non_authority_invalid")
    if event.get("mission_cycle_event_digest") != event_digest(event):
        errors.append("mission_cycle_event_digest_invalid")
    return errors


def apply_mission_cycle_event(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    cycle_state: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    digest_value = str(event.get("mission_cycle_event_digest", ""))
    processed = set(str(item) for item in cycle_state.get("processed_event_digests", []))
    if digest_value in processed:
        if event.get("mission_cycle_event_digest") != event_digest(event):
            raise ValueError("mission_cycle_event_digest_invalid")
        if event.get("mission_id") != contract.get("mission_id"):
            raise ValueError("cycle_event_mission_mismatch")
        if event.get("lineage_id") != contract.get("lineage_id"):
            raise ValueError("cycle_event_lineage_mismatch")
        if event.get("contract_digest") != contract.get("mission_contract_digest"):
            raise ValueError("cycle_event_contract_mismatch")
        result = {
            "version": APPLY_RESULT_VERSION,
            "status": "REPLAYED",
            "mission_id": contract["mission_id"],
            "event_digest": digest_value,
            "previous_state_digest": cycle_state["mission_cycle_state_digest"],
            "result_state_digest": cycle_state["mission_cycle_state_digest"],
            "mission_usage_delta": {"cost": 0.0, "completed_cycles": 0},
            "result_state": deepcopy(dict(cycle_state)),
            "mission_cycle_apply_result_digest": "",
        }
        result["mission_cycle_apply_result_digest"] = apply_result_digest(result)
        return result

    errors = validate_mission_cycle_event(event, contract, mission_state, cycle_state)
    if errors:
        raise ValueError(";".join(errors))

    event_cost = float(event["cost"])
    mission_recorded_cost = float(mission_state.get("used_cost", 0.0))
    base_cost = max(float(cycle_state["cumulative_cost"]), mission_recorded_cost)
    next_total_cost = base_cost + event_cost
    next_cycle_cost = float(cycle_state["cycle_cost"]) + event_cost
    envelope = contract["resource_envelope"]
    usable_total = float(envelope["max_total_cost"]) - float(
        envelope["reserve_floor"]
    )
    if next_total_cost > usable_total:
        raise ValueError("mission_total_budget_exceeded")
    if next_cycle_cost > float(envelope["max_cycle_cost"]):
        raise ValueError("mission_cycle_budget_exceeded")

    result_state = deepcopy(dict(cycle_state))
    previous_digest = result_state["mission_cycle_state_digest"]
    target_phase = str(event["to_phase"])
    result_state["predecessor_cycle_state_digest"] = previous_digest
    result_state["mission_state_digest"] = mission_state["mission_state_digest"]
    result_state["current_phase"] = target_phase
    result_state["phase_index"] = int(result_state["phase_index"]) + 1
    result_state["event_count"] = int(result_state["event_count"]) + 1
    result_state["cumulative_cost"] = next_total_cost
    result_state["cycle_cost"] = next_cycle_cost
    result_state["artifact_digests"] = dict(result_state["artifact_digests"])
    result_state["artifact_digests"][target_phase] = event["artifact_digest"]
    result_state["processed_event_digests"] = list(
        result_state["processed_event_digests"]
    ) + [digest_value]
    result_state["event_history"] = list(result_state["event_history"]) + [
        {
            "event_index": int(result_state["event_count"]),
            "cycle_index": int(event["cycle_index"]),
            "event_digest": digest_value,
            "from_phase": event["from_phase"],
            "to_phase": target_phase,
            "artifact_kind": event["artifact_kind"],
            "artifact_digest": event["artifact_digest"],
            "issued_at_ms": int(event["issued_at_ms"]),
            "cost": event_cost,
        }
    ]
    completed_delta = 0
    if target_phase == "replan":
        result_state["cycle_summaries"] = list(result_state["cycle_summaries"]) + [
            {
                "cycle_index": int(event["cycle_index"]),
                "closed_by_event_digest": digest_value,
                "cycle_cost": next_cycle_cost,
                "artifact_digests": deepcopy(dict(result_state["artifact_digests"])),
                "verification_verdict": str(
                    result_state["latest_verification_verdict"]
                ),
            }
        ]
        result_state["completed_cycles"] = int(result_state["completed_cycles"]) + 1
        result_state["cycle_index"] = int(result_state["cycle_index"]) + 1
        result_state["cycle_cost"] = 0.0
        result_state["latest_verification_verdict"] = ""
        completed_delta = 1
    elif target_phase == "verify":
        result_state["latest_verification_verdict"] = event["metadata"]["verdict"]
        result_state["event_history"][-1]["verification_verdict"] = event[
            "metadata"
        ]["verdict"]
    result_state["updated_at_ms"] = int(event["issued_at_ms"])
    result_state["mission_cycle_state_digest"] = ""
    result_state["mission_cycle_state_digest"] = state_digest(result_state)

    result = {
        "version": APPLY_RESULT_VERSION,
        "status": "APPLIED",
        "mission_id": contract["mission_id"],
        "event_digest": digest_value,
        "previous_state_digest": previous_digest,
        "result_state_digest": result_state["mission_cycle_state_digest"],
        "mission_usage_delta": {
            "cost": event_cost,
            "completed_cycles": completed_delta,
        },
        "result_state": result_state,
        "mission_cycle_apply_result_digest": "",
    }
    result["mission_cycle_apply_result_digest"] = apply_result_digest(result)
    return result
