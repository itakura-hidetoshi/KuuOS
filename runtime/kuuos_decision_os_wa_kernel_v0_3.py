from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_state_v0_3 import (
    build_initial_wa_state,
    build_wa_event,
    validate_wa_event_base,
    validate_wa_state,
)
from runtime.kuuos_decision_os_wa_types_v0_3 import (
    ACTIVATION_RECEIPT_VERSION,
    ALERT_DIMENSIONS,
    APPLY_RESULT_VERSION,
    POSITIVE_DIMENSIONS,
    copy_non_authority,
    normalize_string_list,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    validate_axis_intervals,
    wa_activation_receipt_digest,
    wa_apply_result_digest,
    wa_state_digest,
)

__all__ = [
    "apply_wa_event",
    "build_initial_wa_state",
    "build_replan_wa_activation_receipt",
    "build_wa_event",
    "validate_wa_state",
]


def _require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name}_must_be_bool")
    return value


def _profile_digest(value: Mapping[str, Any]) -> str:
    item = dict(value)
    item.pop("wa_profile_digest", None)
    return sha(item)


def _normalize_profile(
    state: Mapping[str, Any], raw: Mapping[str, Any]
) -> dict[str, Any]:
    option_id = require_nonempty_string(raw.get("option_id"), "option_id")
    if option_id not in set(state["source_option_ids"]):
        raise ValueError("wa_profile_option_not_source_field")
    option_digest = require_nonempty_string(raw.get("option_digest"), "option_digest")
    if option_digest != state["source_option_digest_by_id"].get(option_id):
        raise ValueError("wa_profile_option_digest_mismatch")
    profile = {
        "option_id": option_id,
        "option_digest": option_digest,
        "positive_intervals": validate_axis_intervals(
            require_mapping(raw.get("positive_intervals"), "positive_intervals"),
            POSITIVE_DIMENSIONS,
            "positive_intervals",
        ),
        "alert_intervals": validate_axis_intervals(
            require_mapping(raw.get("alert_intervals"), "alert_intervals"),
            ALERT_DIMENSIONS,
            "alert_intervals",
        ),
        "dissent_considered": _require_bool(
            raw.get("dissent_considered"), "dissent_considered"
        ),
        "minority_preserved": _require_bool(
            raw.get("minority_preserved"), "minority_preserved"
        ),
        "dissent_evidence_digests": normalize_string_list(
            raw.get("dissent_evidence_digests", []),
            "dissent_evidence_digests",
        ),
        "minority_stakeholder_digests": normalize_string_list(
            raw.get("minority_stakeholder_digests", []),
            "minority_stakeholder_digests",
        ),
        "dialogue_receipt_digest": require_nonempty_string(
            raw.get("dialogue_receipt_digest"), "dialogue_receipt_digest"
        ),
        "indra_network_receipt_digest": require_nonempty_string(
            raw.get("indra_network_receipt_digest"),
            "indra_network_receipt_digest",
        ),
        "wa_profile_digest": "",
    }
    profile["wa_profile_digest"] = _profile_digest(profile)
    supplied = raw.get("wa_profile_digest")
    if supplied not in (None, "", profile["wa_profile_digest"]):
        raise ValueError("wa_profile_digest_invalid")
    return profile


def _evaluate_profile(
    state: Mapping[str, Any], profile: Mapping[str, Any]
) -> dict[str, Any]:
    weights = state["weights"]
    beta = float(state["thresholds"]["bottleneck_weight"])
    positive = profile["positive_intervals"]
    alerts = profile["alert_intervals"]
    weighted_lower = sum(
        float(weights[name]) * float(positive[name]["lower"])
        for name in POSITIVE_DIMENSIONS
    )
    weighted_upper = sum(
        float(weights[name]) * float(positive[name]["upper"])
        for name in POSITIVE_DIMENSIONS
    )
    weakest_lower = min(float(positive[name]["lower"]) for name in POSITIVE_DIMENSIONS)
    weakest_upper = min(float(positive[name]["upper"]) for name in POSITIVE_DIMENSIONS)
    relational_lower = (1.0 - beta) * weighted_lower + beta * weakest_lower
    relational_upper = (1.0 - beta) * weighted_upper + beta * weakest_upper
    alert_lower = max(float(alerts[name]["lower"]) for name in ALERT_DIMENSIONS)
    alert_upper = max(float(alerts[name]["upper"]) for name in ALERT_DIMENSIONS)
    wa_lower = relational_lower * (1.0 - alert_upper)
    wa_upper = relational_upper * (1.0 - alert_lower)
    if not (0.0 <= wa_lower <= wa_upper <= 1.0 + 1e-12):
        raise ValueError("wa_interval_invalid")
    return {
        "option_id": profile["option_id"],
        "option_digest": profile["option_digest"],
        "wa_profile_digest": profile["wa_profile_digest"],
        "weighted_interval": {"lower": weighted_lower, "upper": weighted_upper},
        "weakest_interval": {"lower": weakest_lower, "upper": weakest_upper},
        "relational_interval": {
            "lower": relational_lower,
            "upper": relational_upper,
        },
        "alert_interval": {"lower": alert_lower, "upper": alert_upper},
        "wa_interval": {
            "lower": wa_lower,
            "upper": min(1.0, wa_upper),
            "width": min(1.0, wa_upper) - wa_lower,
        },
        "dissent_considered": profile["dissent_considered"],
        "minority_preserved": profile["minority_preserved"],
    }


def _classify_false_harmony(
    state: Mapping[str, Any],
    profile: Mapping[str, Any],
    record: Mapping[str, Any],
) -> dict[str, Any]:
    thresholds = state["thresholds"]
    alert_lower = float(record["alert_interval"]["lower"])
    alert_upper = float(record["alert_interval"]["upper"])
    reasons: list[str] = []
    confirmed = False
    suspected = False
    if alert_lower >= float(thresholds["confirmed_false_harmony_threshold"]):
        confirmed = True
        reasons.append("confirmed_alert_floor_reached")
    if profile["minority_preserved"] is not True:
        confirmed = True
        reasons.append("minority_not_preserved")
    if not confirmed and alert_upper >= float(
        thresholds["suspected_false_harmony_threshold"]
    ):
        suspected = True
        reasons.append("alert_upper_reaches_suspicion")
    if not confirmed and profile["dissent_considered"] is not True:
        suspected = True
        reasons.append("dissent_not_considered")
    return {
        "option_id": profile["option_id"],
        "confirmed_false_harmony": confirmed,
        "suspected_false_harmony": suspected,
        "reason_codes": reasons,
        "alert_interval": deepcopy(record["alert_interval"]),
        "smooth_surface_is_not_proof": True,
        "minority_preserved": profile["minority_preserved"],
        "dissent_considered": profile["dissent_considered"],
    }


def _decide_gate(state: Mapping[str, Any]) -> tuple[str, list[str], list[str]]:
    source_route = state["source_route"]
    direct_map = {
        "NEGOTIATE": "REOBSERVE",
        "APPEAL": "REOBSERVE",
        "HANDOVER": "ESCALATE",
        "HOLD": "HOLD",
        "REJECT": "REJECT",
        "QUARANTINE": "QUARANTINE",
    }
    if source_route in direct_map:
        return direct_map[source_route], [], list(state["source_retained_alternative_ids"])
    if source_route != "CONSENSUS_CANDIDATE":
        return "QUARANTINE", [], []
    selected = str(state["source_selected_option_id"])
    if not selected:
        return "QUARANTINE", [], []
    records = {item["option_id"]: item for item in state["wa_records"]}
    false_records = {
        item["option_id"]: item for item in state["false_harmony_records"]
    }
    if selected not in records or selected not in false_records:
        return "QUARANTINE", [], [selected]
    false_record = false_records[selected]
    if false_record["confirmed_false_harmony"]:
        return "ESCALATE", [], [selected]
    if false_record["suspected_false_harmony"]:
        return "REOBSERVE", [], [selected]
    record = records[selected]
    if (
        float(record["wa_interval"]["lower"])
        < float(state["thresholds"]["minimum_wa_floor"])
        or float(record["weakest_interval"]["lower"])
        < float(state["thresholds"]["minimum_dimension_floor"])
    ):
        return "REPAIR", [], [selected]
    return "ENDORSE", [selected], []


def _apply_phase_payload(
    state: dict[str, Any], target_phase: str, payload: Mapping[str, Any]
) -> None:
    if target_phase == "profile":
        raw_profiles = payload.get("profiles")
        if not isinstance(raw_profiles, list):
            raise TypeError("wa_profiles_must_be_list")
        profiles = [
            _normalize_profile(state, require_mapping(item, "wa_profile"))
            for item in raw_profiles
        ]
        profile_ids = [profile["option_id"] for profile in profiles]
        if len(profile_ids) != len(set(profile_ids)):
            raise ValueError("wa_profile_option_duplicate")
        if set(profile_ids) != set(state["source_option_ids"]):
            raise ValueError("wa_all_v02_source_options_must_be_profiled")
        state["profiles"] = profiles
        return
    if target_phase == "evaluate":
        require_nonempty_string(
            payload.get("evaluation_receipt_digest"), "evaluation_receipt_digest"
        )
        state["wa_records"] = [
            _evaluate_profile(state, profile) for profile in state["profiles"]
        ]
        state["evaluation_receipt_digest"] = payload["evaluation_receipt_digest"]
        return
    if target_phase == "false_harmony_check":
        require_nonempty_string(
            payload.get("false_harmony_receipt_digest"),
            "false_harmony_receipt_digest",
        )
        records = {record["option_id"]: record for record in state["wa_records"]}
        state["false_harmony_records"] = [
            _classify_false_harmony(state, profile, records[profile["option_id"]])
            for profile in state["profiles"]
        ]
        state["false_harmony_receipt_digest"] = payload[
            "false_harmony_receipt_digest"
        ]
        return
    if target_phase == "plurality_check":
        require_nonempty_string(
            payload.get("plurality_receipt_digest"), "plurality_receipt_digest"
        )
        profile_ids = {profile["option_id"] for profile in state["profiles"]}
        source_ids = set(state["source_option_ids"])
        selected = str(state["source_selected_option_id"])
        retained = set(state["source_retained_alternative_ids"])
        state["plurality"] = {
            "all_source_options_profiled": profile_ids == source_ids,
            "retained_alternatives_preserved": retained.issubset(profile_ids),
            "selected_identity_preserved": (not selected) or selected in profile_ids,
            "stakeholder_sections_preserved": bool(
                state["source_stakeholder_registry_digest"]
                and state["source_utility_records_digest"]
                and state["source_aggregate_records_digest"]
            ),
            "veto_and_appeal_history_preserved": bool(
                state["source_veto_records_digest"]
                and state["source_appeal_history_digest"]
            ),
            "silent_substitution_detected": False,
        }
        state["plurality_receipt_digest"] = payload[
            "plurality_receipt_digest"
        ]
        return
    if target_phase == "gate":
        require_nonempty_string(
            payload.get("wa_gate_rule_digest"), "wa_gate_rule_digest"
        )
        plurality = state["plurality"]
        required_true = (
            "all_source_options_profiled",
            "retained_alternatives_preserved",
            "selected_identity_preserved",
            "stakeholder_sections_preserved",
            "veto_and_appeal_history_preserved",
        )
        if (
            not all(plurality[name] is True for name in required_true)
            or plurality["silent_substitution_detected"] is True
        ):
            route, endorsed, review = "QUARANTINE", [], []
        else:
            route, endorsed, review = _decide_gate(state)
        requested_route = payload.get("requested_route")
        if requested_route not in (None, "", route):
            raise ValueError("wa_requested_route_mismatch")
        state["route"] = route
        state["endorsed_option_ids"] = endorsed
        state["review_option_ids"] = review
        state["wa_gate_rule_digest"] = payload["wa_gate_rule_digest"]
        state["wa_basis_digest"] = sha(
            {
                "wa_id": state["wa_id"],
                "source_plural_state_digest": state[
                    "source_plural_state_digest"
                ],
                "source_committed_plural_digest": state[
                    "source_committed_plural_digest"
                ],
                "source_plural_decision_basis_digest": state[
                    "source_plural_decision_basis_digest"
                ],
                "source_decision_basis_digest": state[
                    "source_decision_basis_digest"
                ],
                "source_route": state["source_route"],
                "source_selected_option_id": state[
                    "source_selected_option_id"
                ],
                "source_stakeholder_registry_digest": state[
                    "source_stakeholder_registry_digest"
                ],
                "source_utility_records_digest": state[
                    "source_utility_records_digest"
                ],
                "source_veto_records_digest": state[
                    "source_veto_records_digest"
                ],
                "source_aggregate_records_digest": state[
                    "source_aggregate_records_digest"
                ],
                "source_appeal_history_digest": state[
                    "source_appeal_history_digest"
                ],
                "wa_records": state["wa_records"],
                "false_harmony_records": state["false_harmony_records"],
                "plurality": state["plurality"],
                "route": route,
                "endorsed_option_ids": endorsed,
                "review_option_ids": review,
            }
        )
        state["pending_replan_activation"] = route not in {
            "REJECT",
            "QUARANTINE",
        }
        return
    if target_phase == "commit":
        required = {
            "future_only": True,
            "memory_overwrite": False,
            "wa_not_truth": True,
            "wa_not_execution": True,
            "wa_not_moral_veto": True,
            "activation_boundary": "mission_replan_only",
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"wa_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != copy_non_authority():
            raise ValueError("wa_commit_authority_escalation")
        if not state.get("wa_basis_digest"):
            raise ValueError("wa_basis_missing")
        return
    raise ValueError("wa_target_phase_unsupported")


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    value = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "wa_event_digest": event_id,
        "predecessor_wa_state_digest": predecessor,
        "result_wa_state_digest": state["wa_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "wa_apply_result_digest": "",
    }
    value["wa_apply_result_digest"] = wa_apply_result_digest(value)
    return value


def apply_wa_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_wa_state(state)
    if state_errors:
        raise ValueError("invalid_wa_state:" + ";".join(state_errors))
    event_id = str(event.get("wa_event_digest", ""))
    predecessor = str(state["wa_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = validate_wa_event_base(state, event)
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
        _apply_phase_payload(next_state, target, dict(event["payload"]))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_wa_state_digest"] = predecessor
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
            "wa_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if target == "commit":
        next_state["wa_version"] += 1
        next_state["completed_wa_reviews"] += 1
        next_state["latest_committed_wa_digest"] = sha(
            {
                "wa_id": next_state["wa_id"],
                "wa_version": next_state["wa_version"],
                "source_committed_plural_digest": next_state[
                    "source_committed_plural_digest"
                ],
                "source_plural_decision_basis_digest": next_state[
                    "source_plural_decision_basis_digest"
                ],
                "wa_basis_digest": next_state["wa_basis_digest"],
                "route": next_state["route"],
                "endorsed_option_ids": next_state["endorsed_option_ids"],
                "review_option_ids": next_state["review_option_ids"],
                "commit_event_digest": event_id,
            }
        )
        next_state["wa_summaries"] = list(next_state["wa_summaries"]) + [
            {
                "wa_version": next_state["wa_version"],
                "source_route": next_state["source_route"],
                "route": next_state["route"],
                "endorsed_option_ids": deepcopy(
                    next_state["endorsed_option_ids"]
                ),
                "review_option_ids": deepcopy(next_state["review_option_ids"]),
                "wa_basis_digest": next_state["wa_basis_digest"],
                "commit_artifact_digest": event["artifact_digest"],
                "commit_event_digest": event_id,
            }
        ]
    next_state["wa_state_digest"] = ""
    next_state["wa_state_digest"] = wa_state_digest(next_state)
    next_errors = validate_wa_state(next_state)
    if next_errors:
        raise ValueError("next_wa_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


def build_replan_wa_activation_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_wa_state(state)
    if errors:
        raise ValueError("invalid_wa_state:" + ";".join(errors))
    if state.get("current_phase") != "commit":
        raise ValueError("wa_not_committed")
    if state.get("pending_replan_activation") is not True:
        raise ValueError("wa_not_pending_activation")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")
    receipt = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "wa_id": state["wa_id"],
        "lineage_id": state["lineage_id"],
        "wa_state_digest": state["wa_state_digest"],
        "committed_wa_digest": state["latest_committed_wa_digest"],
        "wa_basis_digest": state["wa_basis_digest"],
        "source_plural_decision_basis_digest": state[
            "source_plural_decision_basis_digest"
        ],
        "route": state["route"],
        "endorsed_option_ids": deepcopy(state["endorsed_option_ids"]),
        "review_option_ids": deepcopy(state["review_option_ids"]),
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
        "wa_not_truth": True,
        "wa_not_execution": True,
        "wa_not_moral_veto": True,
        "host_license_granted": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "wa_activation_receipt_digest": "",
    }
    receipt["wa_activation_receipt_digest"] = wa_activation_receipt_digest(
        receipt
    )
    return receipt
