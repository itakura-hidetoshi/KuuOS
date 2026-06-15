#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    BUNDLE_VERSION,
    DECISION_VERSION,
    OUTCOME_VERSION,
    SECTION_VERSION,
    as_list,
    bundle_digest,
    clamp,
    decision_digest,
    integer,
    mapping,
    nonnegative,
    outcome_digest,
    section_digest,
    sha,
    signed,
)

MODES = ("experiment", "reobserve", "exploit")


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "regret_holonomy": [],
        "outcomes": [],
        "processed_policy_outcome_digests": [],
        "processed_delayed_resolution_ids": [],
        "last_policy_bundle_digest": "",
    }
    packet["regret_bundle_digest"] = bundle_digest(packet)
    return packet


def initial_section(context_key: str) -> dict[str, Any]:
    packet = {
        "version": SECTION_VERSION,
        "section_id": "regret-section-" + sha(context_key)[:18],
        "context_key": context_key,
        "cycle_count": 0,
        "positive_regret_count": 0,
        "zero_regret_count": 0,
        "cumulative_bounded_regret": 0.0,
        "mean_bounded_regret": 0.0,
        "experiment_regret_credit": 0.0,
        "reobserve_regret_credit": 0.0,
        "exploit_regret_credit": 0.0,
        "experiment_alternative_count": 0,
        "reobserve_alternative_count": 0,
        "exploit_alternative_count": 0,
        "delayed_compatible_evidence_count": 0,
        "pending_counterfactual_evidence_count": 0,
        "last_child_policy_mode": "",
        "last_chosen_value": 0.0,
        "last_best_alternative_mode": "",
        "last_best_alternative_value": 0.0,
        "last_best_alternative_confidence": 0.0,
        "last_bounded_regret": 0.0,
        "last_adapted_experiment_pressure_threshold": 0.0,
        "last_adapted_reobserve_pressure_threshold": 0.0,
        "last_adapted_experiment_interval": 0,
        "last_adapted_reobserve_interval": 0,
        "last_child_policy_outcome_digest": "",
        "last_child_effect_receipt_digest": "",
    }
    packet["regret_section_digest"] = section_digest(packet)
    return packet


def section_for(bundle: Mapping[str, Any], context_key: str) -> dict[str, Any]:
    for raw in as_list(bundle.get("sections")):
        section = dict(mapping(raw))
        if section.get("context_key") == context_key:
            return section
    return initial_section(context_key)


def _bounded(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _bounded_int(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def build_regret_decision(
    *,
    regret_run_id: str,
    cycle_index: int,
    context_key: str,
    regret_bundle: Mapping[str, Any],
    policy_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    section = section_for(regret_bundle, context_key)
    experiment_credit = clamp(section.get("experiment_regret_credit"), 0.0)
    reobserve_credit = clamp(section.get("reobserve_regret_credit"), 0.0)
    exploit_credit = clamp(section.get("exploit_regret_credit"), 0.0)
    threshold_gain = clamp(plan.get("regret_threshold_gain"), 0.0)
    exploit_resistance_gain = clamp(plan.get("exploit_resistance_gain"), 0.0)
    interval_gain = integer(plan.get("regret_interval_gain_cycles"), 0)
    exploit_interval_gain = integer(plan.get("exploit_interval_gain_cycles"), 0)

    base_experiment_threshold = clamp(plan.get("base_experiment_pressure_threshold"))
    base_reobserve_threshold = clamp(plan.get("base_reobserve_pressure_threshold"))
    experiment_threshold = _bounded(
        base_experiment_threshold
        - threshold_gain * experiment_credit
        + exploit_resistance_gain * exploit_credit,
        clamp(plan.get("minimum_experiment_pressure_threshold")),
        clamp(plan.get("maximum_experiment_pressure_threshold"), 1.0),
    )
    reobserve_threshold = _bounded(
        base_reobserve_threshold
        - threshold_gain * reobserve_credit
        + exploit_resistance_gain * exploit_credit,
        clamp(plan.get("minimum_reobserve_pressure_threshold")),
        clamp(plan.get("maximum_reobserve_pressure_threshold"), 1.0),
    )

    base_experiment_interval = integer(
        plan.get("base_policy_cycles_between_experiments"), 0
    )
    base_reobserve_interval = integer(
        plan.get("base_policy_cycles_between_reobservations"), 0
    )
    experiment_interval = _bounded_int(
        base_experiment_interval
        - round(interval_gain * experiment_credit)
        + round(exploit_interval_gain * exploit_credit),
        integer(plan.get("minimum_policy_cycles_between_experiments"), 0),
        integer(plan.get("maximum_policy_cycles_between_experiments"), 100000),
    )
    reobserve_interval = _bounded_int(
        base_reobserve_interval
        - round(interval_gain * reobserve_credit)
        + round(exploit_interval_gain * exploit_credit),
        integer(plan.get("minimum_policy_cycles_between_reobservations"), 0),
        integer(plan.get("maximum_policy_cycles_between_reobservations"), 100000),
    )

    decision = {
        "version": DECISION_VERSION,
        "regret_run_id": regret_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "source_policy_bundle_digest": policy_bundle.get("policy_bundle_digest", ""),
        "experiment_regret_credit_before": round(experiment_credit, 6),
        "reobserve_regret_credit_before": round(reobserve_credit, 6),
        "exploit_regret_credit_before": round(exploit_credit, 6),
        "adapted_experiment_pressure_threshold": round(experiment_threshold, 6),
        "adapted_reobserve_pressure_threshold": round(reobserve_threshold, 6),
        "adapted_experiment_interval": experiment_interval,
        "adapted_reobserve_interval": reobserve_interval,
        "counterfactual_estimate_not_truth": True,
        "unexecuted_alternative_not_outcome": True,
        "v0_9_policy_authority_unchanged": True,
        "v0_8_hard_gates_preserved": True,
        "regret_decision_digest": "",
    }
    decision["regret_decision_digest"] = decision_digest(decision)
    return decision


def _mode_from_shadow(prediction: Mapping[str, Any]) -> str:
    action = str(prediction.get("predicted_domain_action", ""))
    if action in {"observe", "hold", "freeze"}:
        return "reobserve"
    return "experiment"


def _historical_mode_value(
    policy_section: Mapping[str, Any], mode: str, plan: Mapping[str, Any]
) -> tuple[float, float, int]:
    mass = max(1.0, nonnegative(plan.get("counterfactual_credibility_mass"), 3.0))
    prior_confidence = clamp(plan.get("prior_mode_confidence"), 0.15)
    if mode == "experiment":
        count = integer(policy_section.get("experiment_count"), 0)
        value = signed(
            policy_section.get("mean_net_experiment_value"),
            signed(plan.get("prior_experiment_counterfactual_value"), 0.5),
        )
        if count == 0:
            value = signed(plan.get("prior_experiment_counterfactual_value"), 0.5)
    elif mode == "reobserve":
        count = integer(policy_section.get("reobserve_count"), 0)
        value = clamp(
            policy_section.get("mean_reobserve_utility"),
            clamp(plan.get("prior_reobserve_counterfactual_value"), 0.45),
        )
        if count == 0:
            value = clamp(plan.get("prior_reobserve_counterfactual_value"), 0.45)
    else:
        count = integer(policy_section.get("exploit_count"), 0)
        value = clamp(
            policy_section.get("mean_exploit_utility"),
            clamp(plan.get("prior_exploit_counterfactual_value"), 0.65),
        )
        if count == 0:
            value = clamp(plan.get("prior_exploit_counterfactual_value"), 0.65)
    confidence = count / (count + mass) if count > 0 else prior_confidence
    return float(value), clamp(confidence), count


def _combine_estimate(
    historical_value: float,
    historical_confidence: float,
    evidence: list[tuple[float, float, str]],
) -> tuple[float, float, list[str]]:
    weighted_sum = historical_value * historical_confidence
    total_weight = historical_confidence
    evidence_ids: list[str] = []
    for value, confidence, evidence_id in evidence:
        weighted_sum += value * confidence
        total_weight += confidence
        evidence_ids.append(evidence_id)
    if total_weight <= 0.0:
        return 0.0, 0.0, evidence_ids
    value = weighted_sum / total_weight
    confidence = min(1.0, total_weight / max(1.0, len(evidence) + 1.0))
    return round(value, 6), round(confidence, 6), evidence_ids


def build_counterfactual_outcome(
    *,
    regret_run_id: str,
    cycle_index: int,
    previous_regret_bundle: Mapping[str, Any],
    previous_policy_bundle: Mapping[str, Any],
    child_policy_bundle: Mapping[str, Any],
    child_policy_outcome: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
    decision: Mapping[str, Any],
    plan: Mapping[str, Any],
    max_outcomes: int,
    max_holonomy: int,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    policy_outcome_digest = str(child_policy_outcome.get("policy_outcome_digest", ""))
    processed_outcomes = {
        str(item)
        for item in as_list(previous_regret_bundle.get("processed_policy_outcome_digests"))
    }
    if policy_outcome_digest in processed_outcomes:
        existing = next(
            (
                dict(mapping(item))
                for item in reversed(as_list(previous_regret_bundle.get("outcomes")))
                if mapping(item).get("child_policy_outcome_digest")
                == policy_outcome_digest
            ),
            {},
        )
        return dict(previous_regret_bundle), existing, True

    context_key = str(decision.get("context_key", ""))
    chosen_mode = str(child_policy_outcome.get("policy_mode", ""))
    if chosen_mode == "experiment":
        chosen_value = signed(child_policy_outcome.get("net_experiment_value"), 0.0)
    else:
        chosen_value = clamp(child_policy_outcome.get("live_observed_utility"), 0.0)
    policy_section = {}
    for raw in as_list(previous_policy_bundle.get("sections")):
        candidate = dict(mapping(raw))
        if candidate.get("context_key") == context_key:
            policy_section = candidate
            break

    processed_resolutions = {
        str(item)
        for item in as_list(previous_regret_bundle.get("processed_delayed_resolution_ids"))
    }
    pending_discount = clamp(plan.get("pending_shadow_discount"), 0.25)
    delayed_weight = clamp(plan.get("delayed_compatible_weight"), 1.0)
    pending_evidence: dict[str, list[tuple[float, float, str]]] = {
        mode: [] for mode in MODES
    }
    delayed_evidence: dict[str, list[tuple[float, float, str]]] = {
        mode: [] for mode in MODES
    }
    pending_count = 0
    delayed_count = 0
    newly_processed_resolution_ids: set[str] = set()

    for raw in as_list(experiment_bundle.get("pending_predictions")):
        prediction = mapping(raw)
        if prediction.get("context_key") != context_key or prediction.get("status") != "pending":
            continue
        mode = _mode_from_shadow(prediction)
        evidence_id = str(prediction.get("prediction_id", ""))
        confidence = clamp(prediction.get("prediction_confidence")) * pending_discount
        value = clamp(prediction.get("predicted_utility"), 0.0)
        if evidence_id and confidence > 0.0:
            pending_evidence[mode].append((value, confidence, evidence_id))
            pending_count += 1

    for raw in as_list(experiment_bundle.get("resolved_predictions")):
        prediction = mapping(raw)
        if prediction.get("context_key") != context_key or prediction.get("status") != "resolved":
            continue
        resolution_id = str(prediction.get("prediction_id", ""))
        if not resolution_id or resolution_id in processed_resolutions:
            continue
        mode = _mode_from_shadow(prediction)
        confidence = clamp(prediction.get("prediction_confidence")) * delayed_weight
        value = clamp(prediction.get("live_observed_utility"), 0.0)
        delayed_evidence[mode].append((value, confidence, resolution_id))
        newly_processed_resolution_ids.add(resolution_id)
        delayed_count += 1

    alternatives: list[dict[str, Any]] = []
    for mode in MODES:
        historical_value, historical_confidence, historical_count = _historical_mode_value(
            policy_section, mode, plan
        )
        evidence = pending_evidence[mode] + delayed_evidence[mode]
        value, confidence, evidence_ids = _combine_estimate(
            historical_value, historical_confidence, evidence
        )
        alternatives.append(
            {
                "mode": mode,
                "estimated_value": value,
                "confidence": confidence,
                "historical_count": historical_count,
                "historical_value": round(historical_value, 6),
                "historical_confidence": round(historical_confidence, 6),
                "pending_evidence_count": len(pending_evidence[mode]),
                "delayed_compatible_evidence_count": len(delayed_evidence[mode]),
                "evidence_ids": evidence_ids,
                "credible": confidence
                >= clamp(plan.get("minimum_counterfactual_confidence"), 0.35),
                "counterfactual_not_truth": True,
            }
        )

    credible = [
        item
        for item in alternatives
        if item.get("mode") != chosen_mode and item.get("credible") is True
    ]
    credible.sort(
        key=lambda item: (
            -float(item.get("estimated_value", 0.0)),
            -float(item.get("confidence", 0.0)),
            str(item.get("mode", "")),
        )
    )
    best = credible[0] if credible else {}
    tolerance = clamp(plan.get("regret_tolerance"), 0.0)
    gap = max(0.0, float(best.get("estimated_value", 0.0)) - chosen_value - tolerance)
    bounded_regret = min(
        clamp(plan.get("maximum_regret_per_cycle"), 1.0),
        gap * float(best.get("confidence", 0.0)),
    )
    best_mode = str(best.get("mode", "")) if bounded_regret > 0.0 else ""

    previous_section = section_for(previous_regret_bundle, context_key)
    decay = clamp(plan.get("regret_credit_decay"), 0.85)
    learning_rate = clamp(plan.get("regret_credit_learning_rate"), 0.8)
    credits = {
        "experiment": clamp(previous_section.get("experiment_regret_credit")) * decay,
        "reobserve": clamp(previous_section.get("reobserve_regret_credit")) * decay,
        "exploit": clamp(previous_section.get("exploit_regret_credit")) * decay,
    }
    if best_mode:
        credits[best_mode] = clamp(credits[best_mode] + learning_rate * bounded_regret)
        chosen_penalty = clamp(plan.get("chosen_mode_credit_penalty"), 0.25)
        if chosen_mode in credits:
            credits[chosen_mode] = clamp(
                max(0.0, credits[chosen_mode] - chosen_penalty * bounded_regret)
            )

    cycle_count = integer(previous_section.get("cycle_count"), 0)
    old_mean = nonnegative(previous_section.get("mean_bounded_regret"), 0.0)
    section = dict(previous_section)
    section.update(
        {
            "cycle_count": cycle_count + 1,
            "positive_regret_count": integer(
                previous_section.get("positive_regret_count"), 0
            )
            + (1 if bounded_regret > 0.0 else 0),
            "zero_regret_count": integer(previous_section.get("zero_regret_count"), 0)
            + (1 if bounded_regret <= 0.0 else 0),
            "cumulative_bounded_regret": round(
                nonnegative(previous_section.get("cumulative_bounded_regret"), 0.0)
                + bounded_regret,
                6,
            ),
            "mean_bounded_regret": round(
                (old_mean * cycle_count + bounded_regret) / (cycle_count + 1), 6
            ),
            "experiment_regret_credit": round(credits["experiment"], 6),
            "reobserve_regret_credit": round(credits["reobserve"], 6),
            "exploit_regret_credit": round(credits["exploit"], 6),
            "experiment_alternative_count": integer(
                previous_section.get("experiment_alternative_count"), 0
            )
            + (1 if best_mode == "experiment" else 0),
            "reobserve_alternative_count": integer(
                previous_section.get("reobserve_alternative_count"), 0
            )
            + (1 if best_mode == "reobserve" else 0),
            "exploit_alternative_count": integer(
                previous_section.get("exploit_alternative_count"), 0
            )
            + (1 if best_mode == "exploit" else 0),
            "delayed_compatible_evidence_count": integer(
                previous_section.get("delayed_compatible_evidence_count"), 0
            )
            + delayed_count,
            "pending_counterfactual_evidence_count": integer(
                previous_section.get("pending_counterfactual_evidence_count"), 0
            )
            + pending_count,
            "last_child_policy_mode": chosen_mode,
            "last_chosen_value": round(chosen_value, 6),
            "last_best_alternative_mode": best_mode,
            "last_best_alternative_value": round(
                float(best.get("estimated_value", 0.0)), 6
            ),
            "last_best_alternative_confidence": round(
                float(best.get("confidence", 0.0)), 6
            ),
            "last_bounded_regret": round(bounded_regret, 6),
            "last_adapted_experiment_pressure_threshold": decision.get(
                "adapted_experiment_pressure_threshold", 0.0
            ),
            "last_adapted_reobserve_pressure_threshold": decision.get(
                "adapted_reobserve_pressure_threshold", 0.0
            ),
            "last_adapted_experiment_interval": decision.get(
                "adapted_experiment_interval", 0
            ),
            "last_adapted_reobserve_interval": decision.get(
                "adapted_reobserve_interval", 0
            ),
            "last_child_policy_outcome_digest": policy_outcome_digest,
            "last_child_effect_receipt_digest": child_policy_outcome.get(
                "child_effect_receipt_digest", ""
            ),
        }
    )
    section["regret_section_digest"] = section_digest(section)

    outcome = {
        "version": OUTCOME_VERSION,
        "regret_run_id": regret_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "child_policy_mode": chosen_mode,
        "child_policy_reason": child_policy_outcome.get("policy_reason", ""),
        "chosen_value": round(chosen_value, 6),
        "counterfactual_alternatives": alternatives,
        "best_alternative_mode": best_mode,
        "best_alternative_value": round(float(best.get("estimated_value", 0.0)), 6),
        "best_alternative_confidence": round(float(best.get("confidence", 0.0)), 6),
        "raw_positive_gap": round(gap, 6),
        "bounded_regret": round(bounded_regret, 6),
        "delayed_compatible_evidence_count": delayed_count,
        "pending_counterfactual_evidence_count": pending_count,
        "newly_processed_delayed_resolution_ids": sorted(
            newly_processed_resolution_ids
        ),
        "experiment_regret_credit_after": round(credits["experiment"], 6),
        "reobserve_regret_credit_after": round(credits["reobserve"], 6),
        "exploit_regret_credit_after": round(credits["exploit"], 6),
        "child_policy_bundle_digest": child_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "child_policy_outcome_digest": policy_outcome_digest,
        "child_effect_receipt_digest": child_policy_outcome.get(
            "child_effect_receipt_digest", ""
        ),
        "regret_decision_digest": decision.get("regret_decision_digest", ""),
        "regret_section_digest": section.get("regret_section_digest", ""),
        "counterfactual_estimate_not_truth": True,
        "unexecuted_alternative_not_outcome": True,
        "regret_outcome_digest": "",
    }
    outcome["regret_outcome_digest"] = outcome_digest(outcome)

    sections = [
        dict(mapping(item))
        for item in as_list(previous_regret_bundle.get("sections"))
        if mapping(item).get("context_key") != context_key
    ]
    sections.append(section)
    sections.sort(key=lambda item: str(item.get("context_key", "")))
    outcomes = as_list(previous_regret_bundle.get("outcomes")) + [outcome]
    holonomy = as_list(previous_regret_bundle.get("regret_holonomy")) + [
        {
            "regret_run_id": regret_run_id,
            "cycle_index": cycle_index,
            "context_key": context_key,
            "child_policy_mode": chosen_mode,
            "chosen_value": round(chosen_value, 6),
            "best_alternative_mode": best_mode,
            "bounded_regret": round(bounded_regret, 6),
            "regret_outcome_digest": outcome["regret_outcome_digest"],
            "regret_section_digest": section["regret_section_digest"],
        }
    ]
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": previous_regret_bundle.get("agent_id", ""),
        "generation": integer(previous_regret_bundle.get("generation"), 0) + 1,
        "sections": sections,
        "regret_holonomy": holonomy[-max_holonomy:],
        "outcomes": outcomes[-max_outcomes:],
        "processed_policy_outcome_digests": sorted(
            processed_outcomes | {policy_outcome_digest}
        ),
        "processed_delayed_resolution_ids": sorted(
            processed_resolutions | newly_processed_resolution_ids
        ),
        "last_policy_bundle_digest": child_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
    }
    updated["regret_bundle_digest"] = bundle_digest(updated)
    return updated, outcome, False
