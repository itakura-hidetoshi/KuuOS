from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_decision_os_state_v0_1 import validate_decision_state
from runtime.kuuos_decision_os_types_v0_1 import (
    NEGATIVE_DIMENSIONS,
    POSITIVE_DIMENSIONS,
)
from runtime.kuuos_decision_os_plural_types_v0_2 import (
    ACTIVATION_RECEIPT_VERSION,
    APPLY_RESULT_VERSION,
    BOUNDARY,
    EVENT_VERSION,
    NON_AUTHORITY,
    PHASES,
    ROUTES,
    STATE_VERSION,
    activation_receipt_digest,
    apply_result_digest,
    bounded,
    clamp01,
    copy_boundary,
    copy_non_authority,
    event_digest,
    next_phase,
    require_bool,
    require_mapping_field,
    require_nonempty_string,
    require_nonnegative_int,
    require_string_list,
    sha,
    state_digest,
    validate_profile_weights,
    validate_thresholds,
)


def _option_by_id(state: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(option["option_id"]): deepcopy(dict(option))
        for option in state.get("source_options", [])
    }


def _stakeholder_by_id(state: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item["stakeholder_id"]): deepcopy(dict(item))
        for item in state.get("stakeholders", [])
    }


def _validate_interval(value: Mapping[str, Any], name: str) -> dict[str, float]:
    lower = bounded(value.get("lower"), f"{name}.lower")
    upper = bounded(value.get("upper"), f"{name}.upper")
    if lower > upper:
        raise ValueError(f"{name}_interval_inverted")
    return {"lower": lower, "upper": upper}


def _normalize_veto_claim(
    value: Mapping[str, Any], stakeholder_id: str
) -> dict[str, Any]:
    return {
        "stakeholder_id": stakeholder_id,
        "option_id": require_nonempty_string(value.get("option_id"), "veto.option_id"),
        "constraint_digest": require_nonempty_string(
            value.get("constraint_digest"), "veto.constraint_digest"
        ),
        "evidence_digest": require_nonempty_string(
            value.get("evidence_digest"), "veto.evidence_digest"
        ),
        "reason_digest": require_nonempty_string(
            value.get("reason_digest"), "veto.reason_digest"
        ),
        "validated": False,
        "validation_reasons": [],
        "raw_veto_grants_authority": False,
    }


def _normalize_stakeholder(value: Mapping[str, Any]) -> dict[str, Any]:
    stakeholder_id = require_nonempty_string(
        value.get("stakeholder_id"), "stakeholder_id"
    )
    weight = clamp01(value.get("weight"), "stakeholder.weight")
    if weight <= 0.0:
        raise ValueError("stakeholder_weight_must_be_positive")
    veto_raw = value.get("veto", [])
    if not isinstance(veto_raw, list):
        raise TypeError("stakeholder_veto_must_be_list")
    return {
        "stakeholder_id": stakeholder_id,
        "role": require_nonempty_string(value.get("role"), "stakeholder.role"),
        "weight": weight,
        "profile_weights": validate_profile_weights(
            require_mapping_field(value.get("profile_weights"), "profile_weights")
        ),
        "minimum_acceptable_value": bounded(
            value.get("minimum_acceptable_value"), "minimum_acceptable_value"
        ),
        "disagreement_point": bounded(
            value.get("disagreement_point"), "disagreement_point"
        ),
        "protected_constraint_digests": require_string_list(
            value.get("protected_constraint_digests", []),
            "protected_constraint_digests",
        ),
        "veto": [
            _normalize_veto_claim(
                require_mapping_field(item, "veto_claim"), stakeholder_id
            )
            for item in veto_raw
        ],
        "appeal_right": require_bool(value.get("appeal_right"), "appeal_right"),
    }


def _evaluate_stakeholder_option(
    stakeholder: Mapping[str, Any], option: Mapping[str, Any]
) -> dict[str, Any]:
    dimensions = require_mapping_field(option.get("dimensions"), "option.dimensions")
    weights = stakeholder["profile_weights"]
    positive_lower = 0.0
    positive_upper = 0.0
    negative_lower = 0.0
    negative_upper = 0.0
    for name in POSITIVE_DIMENSIONS:
        interval = require_mapping_field(dimensions.get(name), f"dimension.{name}")
        lower = clamp01(interval.get("lower"), f"dimension.{name}.lower")
        upper = clamp01(interval.get("upper"), f"dimension.{name}.upper")
        if lower > upper:
            raise ValueError("source_option_dimension_interval_inverted")
        positive_lower += float(weights[name]) * lower
        positive_upper += float(weights[name]) * upper
    for name in NEGATIVE_DIMENSIONS:
        interval = require_mapping_field(dimensions.get(name), f"dimension.{name}")
        lower = clamp01(interval.get("lower"), f"dimension.{name}.lower")
        upper = clamp01(interval.get("upper"), f"dimension.{name}.upper")
        if lower > upper:
            raise ValueError("source_option_dimension_interval_inverted")
        negative_lower += float(weights[name]) * lower
        negative_upper += float(weights[name]) * upper
    utility_lower = max(-1.0, min(1.0, positive_lower - negative_upper))
    utility_upper = max(-1.0, min(1.0, positive_upper - negative_lower))
    if utility_lower > utility_upper + 1e-12:
        raise ValueError("stakeholder_utility_interval_inverted")
    minimum = float(stakeholder["minimum_acceptable_value"])
    if utility_lower >= minimum:
        stance = "support"
    elif utility_upper < minimum:
        stance = "oppose"
    else:
        stance = "uncertain"
    disagreement = float(stakeholder["disagreement_point"])
    lower_surplus = max(0.0, utility_lower - disagreement)
    upper_surplus = max(0.0, utility_upper - disagreement)
    return {
        "stakeholder_id": stakeholder["stakeholder_id"],
        "option_id": option["option_id"],
        "stakeholder_weight": stakeholder["weight"],
        "utility_interval": {
            "lower": utility_lower,
            "upper": utility_upper,
            "midpoint": (utility_lower + utility_upper) / 2.0,
            "width": utility_upper - utility_lower,
        },
        "minimum_acceptable_value": minimum,
        "disagreement_point": disagreement,
        "stance": stance,
        "lower_surplus": lower_surplus,
        "upper_surplus": upper_surplus,
    }


def _weighted_median(points: Sequence[tuple[float, float]]) -> float:
    if not points:
        return 0.0
    ordered = sorted((float(value), float(weight)) for value, weight in points)
    total = sum(weight for _, weight in ordered)
    if total <= 0.0:
        raise ValueError("weighted_median_zero_total_weight")
    threshold = total / 2.0
    cumulative = 0.0
    for value, weight in ordered:
        cumulative += weight
        if cumulative >= threshold:
            return value
    return ordered[-1][0]


def _nash_product(records: Sequence[Mapping[str, Any]], field: str) -> float:
    if not records:
        return 0.0
    product = 1.0
    for record in records:
        surplus = max(0.0, float(record[field]))
        weight = float(record["stakeholder_weight"])
        if surplus <= 0.0:
            return 0.0
        product *= surplus**weight
    return product


def _aggregate_option(
    state: Mapping[str, Any], option_id: str, records: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    thresholds = state["thresholds"]
    support_weight = sum(
        float(record["stakeholder_weight"])
        for record in records
        if record["stance"] == "support"
    )
    opposition_weight = sum(
        float(record["stakeholder_weight"])
        for record in records
        if record["stance"] == "oppose"
    )
    uncertainty_weight = sum(
        float(record["stakeholder_weight"])
        for record in records
        if record["stance"] == "uncertain"
    )
    weighted_median = _weighted_median(
        [
            (
                float(record["utility_interval"]["midpoint"]),
                float(record["stakeholder_weight"]),
            )
            for record in records
        ]
    )
    worst_case_lower = min(
        (float(record["utility_interval"]["lower"]) for record in records),
        default=-1.0,
    )
    nash_lower = _nash_product(records, "lower_surplus")
    nash_upper = _nash_product(records, "upper_surplus")
    vetoed = option_id in set(state["veto_excluded_option_ids"])
    broadly_acceptable = (
        not vetoed
        and support_weight + 1e-12
        >= float(thresholds["minimum_support_weight"])
        and opposition_weight
        <= float(thresholds["maximum_opposition_weight"]) + 1e-12
        and worst_case_lower + 1e-12
        >= float(thresholds["minimum_worst_case_value"])
    )
    return {
        "option_id": option_id,
        "support_weight": support_weight,
        "opposition_weight": opposition_weight,
        "uncertainty_weight": uncertainty_weight,
        "weighted_median": weighted_median,
        "nash_product_lower": nash_lower,
        "nash_product_upper": nash_upper,
        "worst_case_lower": worst_case_lower,
        "validated_veto_present": vetoed,
        "broadly_acceptable": broadly_acceptable,
        "ranking_tuple": [worst_case_lower, nash_lower, weighted_median],
    }


def _rank_aggregates(aggregates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        (deepcopy(dict(item)) for item in aggregates),
        key=lambda item: (
            -float(item["worst_case_lower"]),
            -float(item["nash_product_lower"]),
            -float(item["weighted_median"]),
            str(item["option_id"]),
        ),
    )


def _ablation_explanation(
    utility_records: Sequence[Mapping[str, Any]],
    aggregate_records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    baseline = {str(item["option_id"]): item for item in aggregate_records}
    stakeholder_ids = sorted(
        {str(record["stakeholder_id"]) for record in utility_records}
    )
    option_ids = sorted({str(record["option_id"]) for record in utility_records})
    result: list[dict[str, Any]] = []
    for option_id in option_ids:
        option_records = [
            record for record in utility_records if record["option_id"] == option_id
        ]
        base = baseline[option_id]
        for stakeholder_id in stakeholder_ids:
            remaining = [
                record
                for record in option_records
                if record["stakeholder_id"] != stakeholder_id
            ]
            if remaining:
                median_without = _weighted_median(
                    [
                        (
                            float(record["utility_interval"]["midpoint"]),
                            float(record["stakeholder_weight"]),
                        )
                        for record in remaining
                    ]
                )
                nash_without = _nash_product(remaining, "lower_surplus")
                worst_without = min(
                    float(record["utility_interval"]["lower"])
                    for record in remaining
                )
            else:
                median_without = 0.0
                nash_without = 0.0
                worst_without = 0.0
            result.append(
                {
                    "option_id": option_id,
                    "stakeholder_id": stakeholder_id,
                    "weighted_median_delta": float(base["weighted_median"])
                    - median_without,
                    "nash_lower_delta": float(base["nash_product_lower"])
                    - nash_without,
                    "worst_case_lower_delta": float(base["worst_case_lower"])
                    - worst_without,
                    "explanation_not_causal_truth": True,
                }
            )
    return result


def _normalize_appeal(
    value: Mapping[str, Any], state: Mapping[str, Any]
) -> dict[str, Any]:
    stakeholder_id = require_nonempty_string(
        value.get("stakeholder_id"), "appeal.stakeholder_id"
    )
    stakeholders = _stakeholder_by_id(state)
    if stakeholder_id not in stakeholders:
        raise ValueError("appeal_stakeholder_unknown")
    if stakeholders[stakeholder_id]["appeal_right"] is not True:
        raise ValueError("appeal_right_missing")
    target_option_id = require_nonempty_string(
        value.get("target_option_id"), "appeal.target_option_id"
    )
    if target_option_id not in set(state["source_option_ids"]):
        raise ValueError("appeal_target_option_unknown")
    materiality = clamp01(value.get("materiality"), "appeal.materiality")
    protected = require_bool(
        value.get("protected_boundary_claimed"),
        "appeal.protected_boundary_claimed",
    )
    source_inconsistency = require_bool(
        value.get("source_inconsistency_claimed"),
        "appeal.source_inconsistency_claimed",
    )
    return {
        "appeal_id": require_nonempty_string(value.get("appeal_id"), "appeal_id"),
        "stakeholder_id": stakeholder_id,
        "target_option_id": target_option_id,
        "reason_digest": require_nonempty_string(
            value.get("reason_digest"), "appeal.reason_digest"
        ),
        "evidence_digests": require_string_list(
            value.get("evidence_digests", []), "appeal.evidence_digests"
        ),
        "protected_boundary_claimed": protected,
        "source_inconsistency_claimed": source_inconsistency,
        "materiality": materiality,
        "material": (
            materiality >= float(state["thresholds"]["material_appeal_threshold"])
            or protected
            or source_inconsistency
        ),
        "future_only": True,
        "rewrites_prior_decision": False,
    }


def _raw_unvalidated_veto_for_option(
    state: Mapping[str, Any], option_id: str
) -> bool:
    return any(
        claim["option_id"] == option_id and claim["validated"] is not True
        for claim in state["veto_records"]
    )


def _top_separated(
    top: Mapping[str, Any], second: Mapping[str, Any], margin: float
) -> bool:
    keys = ("worst_case_lower", "nash_product_lower", "weighted_median")
    for key in keys:
        left = float(top[key])
        right = float(second[key])
        if abs(left - right) <= 1e-12:
            continue
        return left > right + margin
    return False


def _adjudicate(state: Mapping[str, Any], payload: Mapping[str, Any]) -> tuple[str, str, list[str]]:
    if require_bool(payload.get("handover_required"), "handover_required"):
        return "HANDOVER", "", list(state["broadly_acceptable_option_ids"])
    if any(appeal["material"] for appeal in state["appeal_history"]):
        return "APPEAL", "", list(state["broadly_acceptable_option_ids"])
    broad = [
        record
        for record in state["ranked_aggregates"]
        if record["broadly_acceptable"] is True
    ]
    if broad:
        top = broad[0]
        top_id = str(top["option_id"])
        if _raw_unvalidated_veto_for_option(state, top_id):
            return "NEGOTIATE", "", [str(item["option_id"]) for item in broad]
        if len(broad) == 1:
            return "CONSENSUS_CANDIDATE", top_id, [
                option_id
                for option_id in state["source_option_ids"]
                if option_id != top_id
            ]
        margin = float(state["thresholds"]["consensus_separation_margin"])
        if _top_separated(top, broad[1], margin):
            return "CONSENSUS_CANDIDATE", top_id, [
                str(item["option_id"]) for item in broad[1:]
            ]
        return "NEGOTIATE", "", [str(item["option_id"]) for item in broad]

    remaining = [
        record
        for record in state["ranked_aggregates"]
        if record["validated_veto_present"] is not True
    ]
    if not remaining:
        return "REJECT", "", []
    if any(float(record["support_weight"]) > 0.0 for record in remaining):
        return "NEGOTIATE", "", [str(item["option_id"]) for item in remaining]
    return "HOLD", "", [str(item["option_id"]) for item in remaining]


def build_initial_plural_state(
    *,
    source_decision_state: Mapping[str, Any],
    plural_id: str,
    lineage_id: str,
    thresholds: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    source_errors = validate_decision_state(source_decision_state)
    if source_errors:
        raise ValueError("source_decision_state_invalid:" + ";".join(source_errors))
    if source_decision_state.get("current_phase") != "commit":
        raise ValueError("source_decision_not_committed")
    source_option_ids = list(source_decision_state.get("admissible_option_ids", []))
    source_options = [
        deepcopy(dict(option))
        for option in source_decision_state.get("options", [])
        if option.get("option_id") in set(source_option_ids)
    ]
    if {option["option_id"] for option in source_options} != set(source_option_ids):
        raise ValueError("source_decision_option_field_incomplete")
    state = {
        "version": STATE_VERSION,
        "plural_id": require_nonempty_string(plural_id, "plural_id"),
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "source_decision_state_digest": require_nonempty_string(
            source_decision_state.get("decision_state_digest"),
            "source_decision_state_digest",
        ),
        "source_decision_basis_digest": require_nonempty_string(
            source_decision_state.get("decision_basis_digest"),
            "source_decision_basis_digest",
        ),
        "source_committed_decision_digest": require_nonempty_string(
            source_decision_state.get("latest_committed_decision_digest"),
            "source_committed_decision_digest",
        ),
        "mission_contract_digest": require_nonempty_string(
            source_decision_state.get("mission_contract_digest"),
            "mission_contract_digest",
        ),
        "source_route": require_nonempty_string(
            source_decision_state.get("route"), "source_route"
        ),
        "source_selected_option_id": str(
            source_decision_state.get("selected_option_id", "")
        ),
        "source_option_ids": source_option_ids,
        "source_options": source_options,
        "source_options_digest": sha(source_options),
        "thresholds": validate_thresholds(
            require_mapping_field(thresholds, "thresholds")
        ),
        "predecessor_plural_state_digest": "",
        "plural_state_digest": "",
        "current_phase": "bind_v01",
        "event_index": 0,
        "plural_version": 0,
        "completed_plural_deliberations": 0,
        "updated_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "source_binding_receipt_digest": "",
        "stakeholders": [],
        "stakeholder_registry_digest": "",
        "utility_records": [],
        "veto_records": [],
        "validated_veto_records": [],
        "unvalidated_veto_records": [],
        "veto_excluded_option_ids": [],
        "aggregate_records": [],
        "ranked_aggregates": [],
        "broadly_acceptable_option_ids": [],
        "explanation": {},
        "appeal_history": [],
        "route": "HOLD",
        "selected_option_id": "",
        "retained_alternative_ids": list(source_option_ids),
        "plural_decision_basis_digest": "",
        "pending_replan_activation": False,
        "latest_committed_plural_digest": "",
        "processed_event_digests": [],
        "event_history": [],
        "plural_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["plural_state_digest"] = state_digest(state)
    return state


def validate_plural_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("plural_state_version_invalid")
        for field in (
            "plural_id",
            "lineage_id",
            "source_decision_state_digest",
            "source_decision_basis_digest",
            "source_committed_decision_digest",
            "mission_contract_digest",
            "source_route",
            "source_options_digest",
        ):
            require_nonempty_string(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("plural_state_phase_invalid")
        for field in (
            "event_index",
            "plural_version",
            "completed_plural_deliberations",
            "updated_at_ms",
        ):
            require_nonnegative_int(state.get(field), field)
        validate_thresholds(
            require_mapping_field(state.get("thresholds"), "thresholds")
        )
        if state.get("route") not in ROUTES:
            errors.append("plural_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("plural_authority_escalation")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("plural_boundary_invalid")
        if state.get("source_options_digest") != sha(state.get("source_options", [])):
            errors.append("plural_source_options_digest_invalid")
        source_ids = list(state.get("source_option_ids", []))
        if len(source_ids) != len(set(source_ids)):
            errors.append("plural_source_option_duplicate")
        option_ids = [
            str(option.get("option_id", "")) for option in state.get("source_options", [])
        ]
        if set(option_ids) != set(source_ids):
            errors.append("plural_source_option_field_mismatch")
        stakeholder_ids = [
            str(item.get("stakeholder_id", ""))
            for item in state.get("stakeholders", [])
        ]
        if len(stakeholder_ids) != len(set(stakeholder_ids)):
            errors.append("plural_stakeholder_duplicate")
        if stakeholder_ids:
            total_weight = sum(float(item["weight"]) for item in state["stakeholders"])
            if abs(total_weight - 1.0) > 1e-9:
                errors.append("plural_stakeholder_weights_must_sum_to_one")
        selected = str(state.get("selected_option_id", ""))
        if selected and selected not in set(source_ids):
            errors.append("plural_selected_option_unknown")
        if state.get("route") == "CONSENSUS_CANDIDATE" and not selected:
            errors.append("plural_consensus_selected_option_missing")
        if selected and state.get("route") != "CONSENSUS_CANDIDATE":
            errors.append("plural_selected_option_route_mismatch")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("plural_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("plural_event_history_count_mismatch")
        if state.get("plural_state_digest") != state_digest(state):
            errors.append("plural_state_digest_invalid")
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def build_plural_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "plural_id": require_nonempty_string(state.get("plural_id"), "plural_id"),
        "lineage_id": require_nonempty_string(state.get("lineage_id"), "lineage_id"),
        "expected_plural_state_digest": require_nonempty_string(
            state.get("plural_state_digest"), "expected_plural_state_digest"
        ),
        "source_phase": require_nonempty_string(
            state.get("current_phase"), "source_phase"
        ),
        "target_phase": require_nonempty_string(target_phase, "target_phase"),
        "event_index": require_nonnegative_int(
            state.get("event_index"), "event_index"
        )
        + 1,
        "artifact_digest": require_nonempty_string(
            artifact_digest, "artifact_digest"
        ),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "plural_event_digest": "",
    }
    event["plural_event_digest"] = event_digest(event)
    return event


def _validate_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if event.get("version") != EVENT_VERSION:
            errors.append("plural_event_version_invalid")
        if event.get("plural_id") != state.get("plural_id"):
            errors.append("plural_event_id_mismatch")
        if event.get("lineage_id") != state.get("lineage_id"):
            errors.append("plural_event_lineage_mismatch")
        if event.get("plural_event_digest") != event_digest(event):
            errors.append("plural_event_digest_invalid")
        if dict(event.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("plural_event_authority_escalation")
        source = str(event.get("source_phase", ""))
        if source != state.get("current_phase"):
            errors.append("plural_event_source_phase_stale")
        if event.get("target_phase") != next_phase(source):
            errors.append("plural_event_phase_order_invalid")
        if event.get("event_index") != int(state.get("event_index", -1)) + 1:
            errors.append("plural_event_index_invalid")
        if event.get("expected_plural_state_digest") != state.get(
            "plural_state_digest"
        ):
            errors.append("plural_event_state_digest_stale")
        if int(event.get("created_at_ms", -1)) < int(
            state.get("updated_at_ms", 0)
        ):
            errors.append("plural_event_time_regression")
        require_nonempty_string(event.get("artifact_digest"), "artifact_digest")
        require_mapping_field(event.get("payload"), "payload")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _apply_phase(state: dict[str, Any], target: str, payload: Mapping[str, Any]) -> None:
    if target == "register_stakeholders":
        state["source_binding_receipt_digest"] = require_nonempty_string(
            payload.get("source_binding_receipt_digest"),
            "source_binding_receipt_digest",
        )
        if payload.get("source_decision_state_digest") != state[
            "source_decision_state_digest"
        ]:
            raise ValueError("plural_source_state_digest_mismatch")
        if payload.get("source_decision_basis_digest") != state[
            "source_decision_basis_digest"
        ]:
            raise ValueError("plural_source_basis_digest_mismatch")
        raw_stakeholders = payload.get("stakeholders")
        if not isinstance(raw_stakeholders, list) or not raw_stakeholders:
            raise ValueError("plural_stakeholders_missing")
        stakeholders = [
            _normalize_stakeholder(
                require_mapping_field(item, "stakeholder")
            )
            for item in raw_stakeholders
        ]
        ids = [item["stakeholder_id"] for item in stakeholders]
        if len(ids) != len(set(ids)):
            raise ValueError("plural_stakeholder_duplicate")
        if abs(sum(float(item["weight"]) for item in stakeholders) - 1.0) > 1e-9:
            raise ValueError("plural_stakeholder_weights_must_sum_to_one")
        state["stakeholders"] = stakeholders
        state["stakeholder_registry_digest"] = sha(stakeholders)
        return

    if target == "evaluate_plurality":
        require_nonempty_string(
            payload.get("evaluation_receipt_digest"),
            "evaluation_receipt_digest",
        )
        option_map = _option_by_id(state)
        records: list[dict[str, Any]] = []
        for stakeholder in state["stakeholders"]:
            for option_id in state["source_option_ids"]:
                records.append(
                    _evaluate_stakeholder_option(stakeholder, option_map[option_id])
                )
        state["utility_records"] = records
        state["plural_evaluation_receipt_digest"] = payload[
            "evaluation_receipt_digest"
        ]
        return

    if target == "validate_vetoes":
        mission_bound = set(
            require_string_list(
                payload.get("mission_bound_constraint_digests", []),
                "mission_bound_constraint_digests",
            )
        )
        source_options = set(state["source_option_ids"])
        all_records: list[dict[str, Any]] = []
        validated: list[dict[str, Any]] = []
        unvalidated: list[dict[str, Any]] = []
        for stakeholder in state["stakeholders"]:
            protected = set(stakeholder["protected_constraint_digests"])
            for raw_claim in stakeholder["veto"]:
                claim = deepcopy(dict(raw_claim))
                reasons: list[str] = []
                if claim["option_id"] not in source_options:
                    reasons.append("veto_option_outside_source_field")
                if claim["constraint_digest"] not in mission_bound:
                    reasons.append("veto_constraint_not_mission_bound")
                if claim["constraint_digest"] not in protected:
                    reasons.append("veto_constraint_not_stakeholder_protected")
                if not claim["evidence_digest"]:
                    reasons.append("veto_evidence_missing")
                claim["validation_reasons"] = reasons
                claim["validated"] = not reasons
                all_records.append(claim)
                if claim["validated"]:
                    validated.append(claim)
                else:
                    unvalidated.append(claim)
        state["veto_records"] = all_records
        state["validated_veto_records"] = validated
        state["unvalidated_veto_records"] = unvalidated
        state["veto_excluded_option_ids"] = sorted(
            {str(claim["option_id"]) for claim in validated}
        )
        state["veto_validation_receipt_digest"] = require_nonempty_string(
            payload.get("veto_validation_receipt_digest"),
            "veto_validation_receipt_digest",
        )
        return

    if target == "aggregate":
        require_nonempty_string(
            payload.get("aggregation_receipt_digest"),
            "aggregation_receipt_digest",
        )
        aggregates: list[dict[str, Any]] = []
        for option_id in state["source_option_ids"]:
            records = [
                record
                for record in state["utility_records"]
                if record["option_id"] == option_id
            ]
            aggregates.append(_aggregate_option(state, option_id, records))
        ranked = _rank_aggregates(aggregates)
        state["aggregate_records"] = aggregates
        state["ranked_aggregates"] = ranked
        state["broadly_acceptable_option_ids"] = [
            str(record["option_id"])
            for record in ranked
            if record["broadly_acceptable"] is True
        ]
        state["aggregation_receipt_digest"] = payload[
            "aggregation_receipt_digest"
        ]
        return

    if target == "explain":
        method = require_nonempty_string(
            payload.get("method"), "explanation.method"
        )
        if method != "stakeholder_ablation":
            raise ValueError("plural_explanation_method_invalid")
        state["explanation"] = {
            "method": method,
            "utility_records": deepcopy(state["utility_records"]),
            "aggregate_records": deepcopy(state["aggregate_records"]),
            "veto_records": deepcopy(state["veto_records"]),
            "stakeholder_ablation": _ablation_explanation(
                state["utility_records"], state["aggregate_records"]
            ),
            "explanation_not_truth": True,
            "explanation_not_moral_worth": True,
            "explanation_receipt_digest": require_nonempty_string(
                payload.get("explanation_receipt_digest"),
                "explanation_receipt_digest",
            ),
        }
        return

    if target == "appeal_window":
        raw_appeals = payload.get("appeals", [])
        if not isinstance(raw_appeals, list):
            raise TypeError("plural_appeals_must_be_list")
        appeals = [
            _normalize_appeal(require_mapping_field(item, "appeal"), state)
            for item in raw_appeals
        ]
        existing_ids = {appeal["appeal_id"] for appeal in state["appeal_history"]}
        incoming_ids = [appeal["appeal_id"] for appeal in appeals]
        if len(incoming_ids) != len(set(incoming_ids)):
            raise ValueError("plural_appeal_id_duplicate")
        if existing_ids & set(incoming_ids):
            raise ValueError("plural_appeal_replay_in_payload")
        state["appeal_history"] = list(state["appeal_history"]) + appeals
        state["appeal_window_receipt_digest"] = require_nonempty_string(
            payload.get("appeal_window_receipt_digest"),
            "appeal_window_receipt_digest",
        )
        return

    if target == "adjudicate":
        require_nonempty_string(
            payload.get("adjudication_rule_digest"),
            "adjudication_rule_digest",
        )
        route, selected, retained = _adjudicate(state, payload)
        requested = payload.get("requested_route")
        if requested not in (None, "", route):
            raise ValueError("plural_requested_route_mismatch")
        state["route"] = route
        state["selected_option_id"] = selected
        state["retained_alternative_ids"] = list(retained)
        state["plural_decision_basis_digest"] = sha(
            {
                "plural_id": state["plural_id"],
                "source_decision_state_digest": state[
                    "source_decision_state_digest"
                ],
                "source_decision_basis_digest": state[
                    "source_decision_basis_digest"
                ],
                "stakeholder_registry_digest": state[
                    "stakeholder_registry_digest"
                ],
                "utility_records": state["utility_records"],
                "veto_records": state["veto_records"],
                "ranked_aggregates": state["ranked_aggregates"],
                "appeal_history": state["appeal_history"],
                "route": route,
                "selected_option_id": selected,
                "retained_alternative_ids": retained,
            }
        )
        state["pending_replan_activation"] = route in {
            "CONSENSUS_CANDIDATE",
            "NEGOTIATE",
            "APPEAL",
            "HANDOVER",
            "HOLD",
        }
        state["adjudication_rule_digest"] = payload[
            "adjudication_rule_digest"
        ]
        return

    if target == "commit":
        if payload.get("future_only") is not True:
            raise ValueError("plural_commit_future_only_required")
        if payload.get("memory_overwrite") is not False:
            raise ValueError("plural_memory_overwrite_forbidden")
        if payload.get("plural_decision_not_execution") is not True:
            raise ValueError("plural_non_execution_required")
        if payload.get("consensus_not_truth") is not True:
            raise ValueError("plural_consensus_not_truth_required")
        if payload.get("activation_boundary") != "mission_replan_only":
            raise ValueError("plural_activation_boundary_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY:
            raise ValueError("plural_commit_authority_escalation")
        if not state.get("plural_decision_basis_digest"):
            raise ValueError("plural_decision_basis_missing")
        return

    raise ValueError("plural_target_phase_unsupported")


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: Sequence[str],
) -> dict[str, Any]:
    value = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "plural_event_digest": event_id,
        "predecessor_plural_state_digest": predecessor,
        "result_plural_state_digest": state["plural_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "plural_apply_result_digest": "",
    }
    value["plural_apply_result_digest"] = apply_result_digest(value)
    return value


def apply_plural_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_plural_state(state)
    if state_errors:
        raise ValueError("invalid_plural_state:" + ";".join(state_errors))
    event_id = str(event.get("plural_event_digest", ""))
    predecessor = str(state["plural_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = _validate_event(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    target = str(event["target_phase"])
    try:
        _apply_phase(next_state, target, dict(event["payload"]))
    except (TypeError, ValueError, KeyError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_plural_state_digest"] = predecessor
    next_state["current_phase"] = target
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": target,
            "artifact_digest": event["artifact_digest"],
            "plural_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if target == "commit":
        next_state["plural_version"] += 1
        next_state["completed_plural_deliberations"] += 1
        next_state["latest_committed_plural_digest"] = sha(
            {
                "plural_id": next_state["plural_id"],
                "plural_version": next_state["plural_version"],
                "source_decision_basis_digest": next_state[
                    "source_decision_basis_digest"
                ],
                "plural_decision_basis_digest": next_state[
                    "plural_decision_basis_digest"
                ],
                "route": next_state["route"],
                "selected_option_id": next_state["selected_option_id"],
                "commit_event_digest": event_id,
            }
        )
        next_state["plural_summaries"] = list(next_state["plural_summaries"]) + [
            {
                "plural_version": next_state["plural_version"],
                "route": next_state["route"],
                "selected_option_id": next_state["selected_option_id"],
                "broadly_acceptable_option_ids": deepcopy(
                    next_state["broadly_acceptable_option_ids"]
                ),
                "retained_alternative_ids": deepcopy(
                    next_state["retained_alternative_ids"]
                ),
                "appeal_count": len(next_state["appeal_history"]),
                "plural_decision_basis_digest": next_state[
                    "plural_decision_basis_digest"
                ],
                "commit_event_digest": event_id,
            }
        ]
    next_state["plural_state_digest"] = ""
    next_state["plural_state_digest"] = state_digest(next_state)
    next_errors = validate_plural_state(next_state)
    if next_errors:
        raise ValueError("next_plural_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


def build_plural_replan_activation_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_plural_state(state)
    if errors:
        raise ValueError("invalid_plural_state:" + ";".join(errors))
    if state.get("current_phase") != "commit":
        raise ValueError("plural_decision_not_committed")
    if state.get("pending_replan_activation") is not True:
        raise ValueError("plural_decision_not_pending_activation")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")
    receipt = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "plural_id": state["plural_id"],
        "lineage_id": state["lineage_id"],
        "plural_state_digest": state["plural_state_digest"],
        "committed_plural_digest": state["latest_committed_plural_digest"],
        "source_decision_basis_digest": state["source_decision_basis_digest"],
        "plural_decision_basis_digest": state["plural_decision_basis_digest"],
        "route": state["route"],
        "selected_option_id": state["selected_option_id"],
        "mission_cycle_phase": "replan",
        "mission_cycle_state_digest": require_nonempty_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "replan_receipt_digest": require_nonempty_string(
            replan_receipt_digest, "replan_receipt_digest"
        ),
        "next_plan_basis_digest": require_nonempty_string(
            next_plan_basis_digest, "next_plan_basis_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "plural_decision_not_execution": True,
        "consensus_not_truth": True,
        "host_license_granted": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "plural_activation_receipt_digest": "",
    }
    receipt["plural_activation_receipt_digest"] = activation_receipt_digest(receipt)
    return receipt


__all__ = [
    "apply_plural_event",
    "build_initial_plural_state",
    "build_plural_event",
    "build_plural_replan_activation_receipt",
    "validate_plural_state",
]
