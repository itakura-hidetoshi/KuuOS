from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_decision_os_types_v0_1 import (
    ACTION_CLASSES,
    ALL_DIMENSIONS,
    NEGATIVE_DIMENSIONS,
    POSITIVE_DIMENSIONS,
    QI_ALLOWED_ROLES,
    QI_FORBIDDEN_ROLES,
    ROUTES,
    clamp01,
    copy_non_authority,
    normalize_string_list,
    require_mapping,
    require_nonempty_string,
    sha,
    validate_interval,
)


def _require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name}_must_be_bool")
    return value


def _nonnegative_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name}_must_be_number")
    result = float(value)
    if result < 0.0:
        raise ValueError(f"{name}_negative")
    return result


def _option_digest(option: Mapping[str, Any]) -> str:
    value = dict(option)
    value.pop("option_digest", None)
    return sha(value)


def _normalize_option(raw: Mapping[str, Any]) -> dict[str, Any]:
    option_id = require_nonempty_string(raw.get("option_id"), "option_id")
    action_class = require_nonempty_string(raw.get("action_class"), "action_class")
    if action_class not in ACTION_CLASSES:
        raise ValueError("decision_action_class_invalid")
    dimensions_raw = require_mapping(raw.get("dimensions"), "dimensions")
    dimensions: dict[str, dict[str, float]] = {}
    for dimension in ALL_DIMENSIONS:
        dimensions[dimension] = validate_interval(
            require_mapping(dimensions_raw.get(dimension), dimension), dimension
        )
    normalized = {
        "option_id": option_id,
        "description_digest": require_nonempty_string(
            raw.get("description_digest"), "description_digest"
        ),
        "action_class": action_class,
        "requires_external_license": _require_bool(
            raw.get("requires_external_license"), "requires_external_license"
        ),
        "requires_human_review": _require_bool(
            raw.get("requires_human_review"), "requires_human_review"
        ),
        "mission_allowed": _require_bool(raw.get("mission_allowed"), "mission_allowed"),
        "prohibited": _require_bool(raw.get("prohibited"), "prohibited"),
        "authority_claimed": _require_bool(
            raw.get("authority_claimed"), "authority_claimed"
        ),
        "estimated_cost": _nonnegative_number(
            raw.get("estimated_cost"), "estimated_cost"
        ),
        "estimated_risk": clamp01(raw.get("estimated_risk"), "estimated_risk"),
        "recoverability": clamp01(raw.get("recoverability"), "recoverability"),
        "reversibility": clamp01(raw.get("reversibility"), "reversibility"),
        "required_evidence_digests": normalize_string_list(
            raw.get("required_evidence_digests", []),
            "required_evidence_digests",
        ),
        "available_evidence_digests": normalize_string_list(
            raw.get("available_evidence_digests", []),
            "available_evidence_digests",
        ),
        "supporting_evidence_digests": normalize_string_list(
            raw.get("supporting_evidence_digests", []),
            "supporting_evidence_digests",
        ),
        "opposing_evidence_digests": normalize_string_list(
            raw.get("opposing_evidence_digests", []),
            "opposing_evidence_digests",
        ),
        "stakeholder_digests": normalize_string_list(
            raw.get("stakeholder_digests", []), "stakeholder_digests"
        ),
        "dimensions": dimensions,
        "option_digest": "",
    }
    normalized["option_digest"] = _option_digest(normalized)
    supplied_digest = raw.get("option_digest")
    if supplied_digest not in (None, "", normalized["option_digest"]):
        raise ValueError("decision_option_digest_invalid")
    return normalized


def _constraint_reasons(state: Mapping[str, Any], option: Mapping[str, Any]) -> list[str]:
    thresholds = state["thresholds"]
    reasons: list[str] = []
    if option["mission_allowed"] is not True:
        reasons.append("mission_not_allowed")
    if option["prohibited"] is True:
        reasons.append("mission_prohibited")
    if option["authority_claimed"] is True:
        reasons.append("authority_escalation_claimed")
    if float(option["estimated_cost"]) > float(state["decision_budget"]):
        reasons.append("decision_budget_exceeded")
    if float(option["estimated_risk"]) > float(thresholds["maximum_risk"]):
        reasons.append("risk_ceiling_exceeded")
    if float(option["recoverability"]) < float(
        thresholds["minimum_recoverability"]
    ):
        reasons.append("recoverability_floor_not_met")
    if float(option["reversibility"]) < float(thresholds["minimum_reversibility"]):
        reasons.append("reversibility_floor_not_met")
    required = set(option["required_evidence_digests"])
    available = set(option["available_evidence_digests"])
    if not required.issubset(available):
        reasons.append("required_evidence_missing")
    return reasons


def _evaluate_option(state: Mapping[str, Any], option: Mapping[str, Any]) -> dict[str, Any]:
    weights = state["weights"]
    dimensions = option["dimensions"]
    positive_lower = sum(
        float(weights[name]) * float(dimensions[name]["lower"])
        for name in POSITIVE_DIMENSIONS
    )
    positive_upper = sum(
        float(weights[name]) * float(dimensions[name]["upper"])
        for name in POSITIVE_DIMENSIONS
    )
    negative_lower = sum(
        float(weights[name]) * float(dimensions[name]["lower"])
        for name in NEGATIVE_DIMENSIONS
    )
    negative_upper = sum(
        float(weights[name]) * float(dimensions[name]["upper"])
        for name in NEGATIVE_DIMENSIONS
    )
    lower = max(-1.0, min(1.0, positive_lower - negative_upper))
    upper = max(-1.0, min(1.0, positive_upper - negative_lower))
    if lower > upper + 1e-12:
        raise ValueError("decision_value_interval_inverted")
    return {
        "option_id": option["option_id"],
        "option_digest": option["option_digest"],
        "value_interval": {
            "lower": lower,
            "upper": upper,
            "width": upper - lower,
        },
        "positive_lower": positive_lower,
        "positive_upper": positive_upper,
        "negative_lower": negative_lower,
        "negative_upper": negative_upper,
        "information_gain_interval": deepcopy(dimensions["information_gain"]),
        "estimated_risk": option["estimated_risk"],
        "recoverability": option["recoverability"],
        "reversibility": option["reversibility"],
        "requires_external_license": option["requires_external_license"],
        "requires_human_review": option["requires_human_review"],
        "action_class": option["action_class"],
    }


def _dominance_and_regret(
    state: Mapping[str, Any], records: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    margin = float(state["thresholds"]["dominance_margin"])
    relations: list[dict[str, Any]] = []
    records_by_id = {record["option_id"]: record for record in records}
    dominated_ids: set[str] = set()
    for left in records:
        for right in records:
            if left["option_id"] == right["option_id"]:
                continue
            robust = (
                float(left["value_interval"]["lower"])
                > float(right["value_interval"]["upper"]) + margin
            )
            if robust:
                dominated_ids.add(right["option_id"])
                relations.append(
                    {
                        "dominant_option_id": left["option_id"],
                        "dominated_option_id": right["option_id"],
                        "dominance_margin": margin,
                        "dominant_lower": left["value_interval"]["lower"],
                        "dominated_upper": right["value_interval"]["upper"],
                        "robust": True,
                    }
                )
    for record in records:
        own_lower = float(record["value_interval"]["lower"])
        record["worst_case_regret"] = max(
            (
                max(0.0, float(other["value_interval"]["upper"]) - own_lower)
                for other in records
                if other["option_id"] != record["option_id"]
            ),
            default=0.0,
        )
    frontier = [
        option_id for option_id in records_by_id if option_id not in dominated_ids
    ]
    universal_dominators = []
    for record in records:
        others = [
            other for other in records if other["option_id"] != record["option_id"]
        ]
        if all(
            float(record["value_interval"]["lower"])
            > float(other["value_interval"]["upper"]) + margin
            for other in others
        ):
            universal_dominators.append(record["option_id"])
    return records, relations, frontier if frontier else universal_dominators


def _unique_robust_winner(state: Mapping[str, Any]) -> str:
    records = list(state["evaluation_records"])
    margin = float(state["thresholds"]["dominance_margin"])
    winners: list[str] = []
    for record in records:
        others = [
            other for other in records if other["option_id"] != record["option_id"]
        ]
        if all(
            float(record["value_interval"]["lower"])
            > float(other["value_interval"]["upper"]) + margin
            for other in others
        ):
            winners.append(record["option_id"])
    return winners[0] if len(winners) == 1 else ""


def _compute_decision(state: Mapping[str, Any]) -> tuple[str, str, list[str]]:
    admissible = list(state["admissible_option_ids"])
    records = {record["option_id"]: record for record in state["evaluation_records"]}
    options = {option["option_id"]: option for option in state["options"]}
    challenge = state["challenge"]
    middle = state["middle_way"]
    thresholds = state["thresholds"]
    frontier = list(state["retained_alternative_ids"])

    if not admissible:
        return "REJECT", "", []
    if challenge["catastrophic_risk_detected"] or challenge[
        "unresolved_normative_conflict"
    ]:
        return "ESCALATE", "", frontier or admissible
    if middle["responsible_deferral_allowed"] is not True:
        return "ESCALATE", "", frontier or admissible

    winner = _unique_robust_winner(state)
    if winner:
        if options[winner]["requires_human_review"]:
            return "ESCALATE", "", [winner]
        if middle["selection_allowed"] is True:
            return "SELECT_CANDIDATE", winner, [
                option_id for option_id in admissible if option_id != winner
            ]
        if float(middle["repairability"]) >= 0.5:
            return "REPAIR", "", frontier or admissible
        return "HOLD", "", frontier or admissible

    if challenge["missing_evidence_digests"]:
        return "OBSERVE", "", frontier or admissible

    max_width = max(
        (float(records[option_id]["value_interval"]["width"]) for option_id in admissible),
        default=0.0,
    )
    if max_width >= float(thresholds["observe_width"]):
        observe_options = [
            option_id
            for option_id in admissible
            if options[option_id]["action_class"] == "observe"
        ]
        return "OBSERVE", "", observe_options or frontier or admissible

    experiment_options = [
        option_id
        for option_id in admissible
        if options[option_id]["action_class"] == "experiment"
        and float(records[option_id]["information_gain_interval"]["lower"])
        >= float(thresholds["experiment_information_gain"])
        and float(options[option_id]["estimated_risk"])
        <= float(thresholds["experiment_maximum_risk"])
        and float(options[option_id]["recoverability"])
        >= float(thresholds["experiment_minimum_recoverability"])
    ]
    if experiment_options:
        return "EXPERIMENT_RECOMMENDED", "", experiment_options
    if middle["selection_allowed"] is not True and float(middle["repairability"]) >= 0.5:
        return "REPAIR", "", frontier or admissible
    return "HOLD", "", frontier or admissible


def apply_phase_payload(
    state: dict[str, Any], target_phase: str, payload: Mapping[str, Any]
) -> None:
    if target_phase == "generate":
        raw_options = payload.get("options")
        if not isinstance(raw_options, list) or not raw_options:
            raise ValueError("decision_options_missing")
        options = [_normalize_option(require_mapping(item, "option")) for item in raw_options]
        option_ids = [option["option_id"] for option in options]
        if len(option_ids) != len(set(option_ids)):
            raise ValueError("decision_option_id_duplicate")
        state["options"] = options
        state["advisory_receipt_digests"] = normalize_string_list(
            payload.get("advisory_receipt_digests", []),
            "advisory_receipt_digests",
        )
        return

    if target_phase == "constrain":
        require_nonempty_string(
            payload.get("constraint_receipt_digest"), "constraint_receipt_digest"
        )
        admissible: list[str] = []
        excluded: list[dict[str, Any]] = []
        for option in state["options"]:
            reasons = _constraint_reasons(state, option)
            if reasons:
                excluded.append(
                    {
                        "option_id": option["option_id"],
                        "option_digest": option["option_digest"],
                        "reasons": reasons,
                    }
                )
            else:
                admissible.append(option["option_id"])
        state["admissible_option_ids"] = admissible
        state["excluded_options"] = excluded
        state["constraint_receipt_digest"] = payload["constraint_receipt_digest"]
        return

    if target_phase == "evaluate":
        require_nonempty_string(
            payload.get("evaluation_receipt_digest"), "evaluation_receipt_digest"
        )
        admissible = set(state["admissible_option_ids"])
        records = [
            _evaluate_option(state, option)
            for option in state["options"]
            if option["option_id"] in admissible
        ]
        records, relations, frontier = _dominance_and_regret(state, records)
        state["evaluation_records"] = records
        state["dominance_relations"] = relations
        state["retained_alternative_ids"] = frontier
        state["evaluation_receipt_digest"] = payload["evaluation_receipt_digest"]
        return

    if target_phase == "challenge":
        state["challenge"] = {
            "counterargument_digests": normalize_string_list(
                payload.get("counterargument_digests", []),
                "counterargument_digests",
            ),
            "missing_evidence_digests": normalize_string_list(
                payload.get("missing_evidence_digests", []),
                "missing_evidence_digests",
            ),
            "stakeholder_objection_digests": normalize_string_list(
                payload.get("stakeholder_objection_digests", []),
                "stakeholder_objection_digests",
            ),
            "alternative_option_ids": normalize_string_list(
                payload.get("alternative_option_ids", []),
                "alternative_option_ids",
            ),
            "counterfactual_receipt_digests": normalize_string_list(
                payload.get("counterfactual_receipt_digests", []),
                "counterfactual_receipt_digests",
            ),
            "catastrophic_risk_detected": _require_bool(
                payload.get("catastrophic_risk_detected"),
                "catastrophic_risk_detected",
            ),
            "unresolved_normative_conflict": _require_bool(
                payload.get("unresolved_normative_conflict"),
                "unresolved_normative_conflict",
            ),
        }
        known_ids = {option["option_id"] for option in state["options"]}
        if not set(state["challenge"]["alternative_option_ids"]).issubset(known_ids):
            raise ValueError("decision_challenge_unknown_alternative")
        return

    if target_phase == "qi_condition":
        roles = normalize_string_list(payload.get("roles", []), "qi_roles")
        role_set = set(roles)
        if role_set & QI_FORBIDDEN_ROLES:
            raise ValueError("decision_qi_forbidden_role")
        if not role_set.issubset(QI_ALLOWED_ROLES):
            raise ValueError("decision_qi_unknown_role")
        authority_source = _require_bool(
            payload.get("authority_source"), "qi_authority_source"
        )
        if authority_source:
            raise ValueError("decision_qi_authority_source_forbidden")
        state["qi_process"] = {
            "process_tensor_digest": require_nonempty_string(
                payload.get("process_tensor_digest"), "process_tensor_digest"
            ),
            "history_window_digest": require_nonempty_string(
                payload.get("history_window_digest"), "history_window_digest"
            ),
            "roles": roles,
            "flow_phase": require_nonempty_string(
                payload.get("flow_phase"), "flow_phase"
            ),
            "authority_source": False,
        }
        return

    if target_phase == "two_truths_check":
        value = require_mapping(payload.get("two_truths"), "two_truths")
        two_truths = {
            "samvrti_decision_usable": _require_bool(
                value.get("samvrti_decision_usable"),
                "samvrti_decision_usable",
            ),
            "paramartha_non_reified": _require_bool(
                value.get("paramartha_non_reified"),
                "paramartha_non_reified",
            ),
            "selected_option_not_absolute": _require_bool(
                value.get("selected_option_not_absolute"),
                "selected_option_not_absolute",
            ),
            "two_truths_separated": _require_bool(
                value.get("two_truths_separated"), "two_truths_separated"
            ),
        }
        if two_truths["paramartha_non_reified"] is not True:
            raise ValueError("decision_paramartha_reification")
        if two_truths["selected_option_not_absolute"] is not True:
            raise ValueError("decision_option_absolutization")
        if two_truths["two_truths_separated"] is not True:
            raise ValueError("decision_two_truths_collapsed")
        state["two_truths"] = two_truths
        return

    if target_phase == "middle_way_gate":
        value = require_mapping(payload.get("middle_way"), "middle_way")
        risks = {
            name: clamp01(value.get(name), name)
            for name in (
                "reification_risk",
                "nihilistic_erasure_risk",
                "premature_closure_risk",
                "responsibility_abandonment_risk",
                "stakeholder_exclusion_risk",
                "irreversibility_risk",
                "repairability",
            )
        }
        maximum = float(state["thresholds"]["middle_way_maximum_risk"])
        risks["selection_allowed"] = all(
            risks[name] <= maximum
            for name in (
                "reification_risk",
                "premature_closure_risk",
                "stakeholder_exclusion_risk",
                "irreversibility_risk",
            )
        )
        risks["responsible_deferral_allowed"] = all(
            risks[name] <= maximum
            for name in (
                "nihilistic_erasure_risk",
                "responsibility_abandonment_risk",
            )
        )
        state["middle_way"] = risks
        return

    if target_phase == "decide":
        require_nonempty_string(
            payload.get("decision_rule_digest"), "decision_rule_digest"
        )
        route, selected, recommended = _compute_decision(state)
        requested_route = payload.get("requested_route")
        if requested_route not in (None, "", route):
            raise ValueError("decision_requested_route_mismatch")
        if route not in ROUTES:
            raise ValueError("decision_route_invalid")
        state["route"] = route
        state["selected_option_id"] = selected
        state["recommended_option_ids"] = list(recommended)
        if route == "SELECT_CANDIDATE":
            state["retained_alternative_ids"] = [
                option_id
                for option_id in state["admissible_option_ids"]
                if option_id != selected
            ]
        state["decision_rule_digest"] = payload["decision_rule_digest"]
        state["decision_basis_digest"] = sha(
            {
                "decision_id": state["decision_id"],
                "mission_contract_digest": state["mission_contract_digest"],
                "mission_state_digest": state["mission_state_digest"],
                "source_belief_receipt_digest": state[
                    "source_belief_receipt_digest"
                ],
                "route": route,
                "selected_option_id": selected,
                "recommended_option_ids": recommended,
                "admissible_option_ids": state["admissible_option_ids"],
                "retained_alternative_ids": state["retained_alternative_ids"],
                "evaluation_records": state["evaluation_records"],
                "challenge": state["challenge"],
                "qi_process": state["qi_process"],
                "two_truths": state["two_truths"],
                "middle_way": state["middle_way"],
            }
        )
        state["pending_replan_activation"] = route in {
            "SELECT_CANDIDATE",
            "OBSERVE",
            "EXPERIMENT_RECOMMENDED",
            "REPAIR",
            "ESCALATE",
        }
        return

    if target_phase == "commit":
        if payload.get("future_only") is not True:
            raise ValueError("decision_commit_future_only_required")
        if payload.get("memory_overwrite") is not False:
            raise ValueError("decision_memory_overwrite_forbidden")
        if payload.get("decision_not_execution") is not True:
            raise ValueError("decision_not_execution_required")
        if payload.get("activation_boundary") != "mission_replan_only":
            raise ValueError("decision_activation_boundary_invalid")
        if dict(payload.get("non_authority", {})) != copy_non_authority():
            raise ValueError("decision_commit_authority_escalation")
        if not state.get("decision_basis_digest"):
            raise ValueError("decision_basis_missing")
        return

    raise ValueError("decision_target_phase_unsupported")
