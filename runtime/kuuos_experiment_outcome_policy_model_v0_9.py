#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
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


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "policy_holonomy": [],
        "outcomes": [],
        "processed_child_effect_digests": [],
        "last_experiment_bundle_digest": "",
    }
    packet["policy_bundle_digest"] = bundle_digest(packet)
    return packet


def initial_section(context_key: str) -> dict[str, Any]:
    packet = {
        "version": SECTION_VERSION,
        "section_id": "policy-section-" + sha(context_key)[:18],
        "context_key": context_key,
        "cycle_count": 0,
        "experiment_count": 0,
        "exploit_count": 0,
        "reobserve_count": 0,
        "experiment_success_alpha": 1.0,
        "experiment_success_beta": 1.0,
        "mean_net_experiment_value": 0.0,
        "mean_experiment_utility": 0.0,
        "mean_experiment_cost": 0.0,
        "mean_experiment_risk": 0.0,
        "mean_experiment_recoverability": 1.0,
        "mean_exploit_utility": 0.0,
        "mean_reobserve_utility": 0.0,
        "compatible_resolution_count": 0,
        "unresolved_after_live_count": 0,
        "last_policy_mode": "",
        "last_child_decision_mode": "",
        "last_live_domain_action": "",
        "last_live_observed_utility": 0.0,
        "last_net_experiment_value": 0.0,
        "last_compatible_shadow_resolved": False,
        "last_experiment_cycle": -1000000,
        "last_reobserve_cycle": -1000000,
        "last_exploit_cycle": -1000000,
        "last_child_effect_receipt_digest": "",
    }
    packet["policy_section_digest"] = section_digest(packet)
    return packet


def section_for(bundle: Mapping[str, Any], context_key: str) -> dict[str, Any]:
    for raw in as_list(bundle.get("sections")):
        section = dict(mapping(raw))
        if section.get("context_key") == context_key:
            return section
    return initial_section(context_key)


def _mean(previous: float, count: int, observed: float) -> float:
    return round((previous * count + observed) / (count + 1), 6)


def _pending_density(experiment_bundle: Mapping[str, Any], context_key: str) -> float:
    pending = sum(
        1
        for raw in as_list(experiment_bundle.get("pending_predictions"))
        if mapping(raw).get("context_key") == context_key
        and mapping(raw).get("status") == "pending"
    )
    resolved = sum(
        1
        for raw in as_list(experiment_bundle.get("resolved_predictions"))
        if mapping(raw).get("context_key") == context_key
    )
    return clamp(pending / max(1.0, float(pending + resolved)))


def build_policy_decision(
    *,
    policy_run_id: str,
    cycle_index: int,
    policy_bundle: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
    preview_decision: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    context_key = str(preview_decision.get("context_key", ""))
    section = section_for(policy_bundle, context_key)
    alpha = nonnegative(section.get("experiment_success_alpha"), 1.0)
    beta = nonnegative(section.get("experiment_success_beta"), 1.0)
    posterior = clamp(alpha / max(1e-9, alpha + beta), 0.5)
    evidence_mass = max(0.0, alpha + beta - 2.0)
    posterior_confidence = clamp(
        evidence_mass / max(1.0, nonnegative(plan.get("posterior_confidence_mass"), 6.0))
    )
    candidates = [dict(mapping(item)) for item in as_list(preview_decision.get("candidate_experiments"))]
    max_information_gain = max(
        [float(item.get("expected_information_gain", 0.0)) for item in candidates]
        or [0.0]
    )
    eligible_count = sum(1 for item in candidates if item.get("eligible_for_trial") is True)
    preview_experiment = next(
        (item for item in candidates if item.get("eligible_for_trial") is True),
        {},
    )
    pending_density = _pending_density(experiment_bundle, context_key)
    experiment_count = integer(section.get("experiment_count"), 0)
    resolution_total = integer(section.get("compatible_resolution_count"), 0) + integer(
        section.get("unresolved_after_live_count"), 0
    )
    resolution_rate = (
        integer(section.get("compatible_resolution_count"), 0) / resolution_total
        if resolution_total > 0
        else 0.0
    )
    mean_net = signed(section.get("mean_net_experiment_value"), 0.0)
    net_unit = clamp((mean_net + 1.0) / 2.0)
    mean_cost = clamp(section.get("mean_experiment_cost"), 0.0)
    mean_risk = clamp(section.get("mean_experiment_risk"), 0.0)
    mean_recoverability = clamp(section.get("mean_experiment_recoverability"), 1.0)

    experiment_pressure = clamp(
        clamp(plan.get("policy_information_gain_weight")) * clamp(max_information_gain)
        + clamp(plan.get("policy_posterior_weight"))
        * (
            posterior_confidence * posterior
            + (1.0 - posterior_confidence) * clamp(plan.get("prior_experiment_value"), 0.5)
        )
        + clamp(plan.get("policy_net_value_weight")) * net_unit
        + clamp(plan.get("policy_pending_weight")) * pending_density
        + clamp(plan.get("policy_recoverability_weight")) * mean_recoverability
        - clamp(plan.get("policy_cost_penalty_weight")) * mean_cost
        - clamp(plan.get("policy_risk_penalty_weight")) * mean_risk
    )
    cycles_since_experiment = cycle_index - integer(
        section.get("last_experiment_cycle"), -1000000
    )
    cycles_since_reobserve = cycle_index - integer(
        section.get("last_reobserve_cycle"), -1000000
    )
    post_experiment_unresolved = (
        section.get("last_policy_mode") == "experiment"
        and section.get("last_compatible_shadow_resolved") is not True
    )
    reobserve_pressure = clamp(
        clamp(plan.get("reobserve_pending_weight")) * pending_density
        + clamp(plan.get("reobserve_resolution_debt_weight")) * (1.0 - resolution_rate)
        + clamp(plan.get("reobserve_low_confidence_weight")) * (1.0 - posterior_confidence)
        + (
            clamp(plan.get("post_experiment_reobserve_bonus"))
            if post_experiment_unresolved
            else 0.0
        )
    )

    experiment_interval_ok = cycles_since_experiment >= integer(
        plan.get("minimum_policy_cycles_between_experiments"), 0
    )
    reobserve_interval_ok = cycles_since_reobserve >= integer(
        plan.get("minimum_policy_cycles_between_reobservations"), 0
    )
    mode = "exploit"
    reason = "baseline_value_preserved"
    if (
        post_experiment_unresolved
        and reobserve_interval_ok
        and reobserve_pressure >= clamp(plan.get("reobserve_pressure_threshold"))
    ):
        mode = "reobserve"
        reason = "post_experiment_resolution_debt"
    elif (
        eligible_count > 0
        and experiment_interval_ok
        and experiment_pressure >= clamp(plan.get("experiment_pressure_threshold"))
    ):
        mode = "experiment"
        reason = "posterior_and_information_gain_support_trial"
    elif (
        reobserve_interval_ok
        and reobserve_pressure >= clamp(plan.get("reobserve_pressure_threshold"))
    ):
        mode = "reobserve"
        reason = "uncertainty_requires_local_reobservation"

    base_minimum = clamp(plan.get("base_minimum_information_gain"))
    hard_floor = clamp(plan.get("hard_minimum_information_gain"))
    adaptation = clamp(plan.get("information_gain_threshold_adaptation_rate"))
    if mode == "experiment":
        excess = max(0.0, experiment_pressure - clamp(plan.get("experiment_pressure_threshold")))
        adapted_minimum = max(hard_floor, base_minimum - adaptation * excess)
    else:
        adapted_minimum = 1.0

    base_cooldown = integer(plan.get("base_trial_cooldown_cycles"), 0)
    hard_cooldown = integer(plan.get("hard_minimum_trial_cooldown_cycles"), 0)
    cooldown_adaptation = integer(plan.get("maximum_cooldown_reduction_cycles"), 0)
    reduction = 0
    if mode == "experiment" and experiment_pressure > clamp(plan.get("experiment_pressure_threshold")):
        reduction = min(
            cooldown_adaptation,
            int(
                (experiment_pressure - clamp(plan.get("experiment_pressure_threshold")))
                * max(1, cooldown_adaptation + 1)
            ),
        )
    adapted_cooldown = max(hard_cooldown, base_cooldown - reduction)

    decision = {
        "version": DECISION_VERSION,
        "policy_run_id": policy_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "policy_bundle_digest": policy_bundle.get("policy_bundle_digest", ""),
        "source_experiment_bundle_digest": experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "preview_experiment_decision_digest": preview_decision.get(
            "experiment_decision_digest", ""
        ),
        "policy_mode": mode,
        "policy_reason": reason,
        "preview_baseline_adapter_id": preview_decision.get("baseline_adapter_id", ""),
        "preview_experiment_adapter_id": preview_decision.get(
            "experiment_adapter_id", ""
        ),
        "preview_eligible_experiment_count": eligible_count,
        "preview_max_information_gain": round(max_information_gain, 6),
        "pending_prediction_density": round(pending_density, 6),
        "compatible_resolution_rate": round(resolution_rate, 6),
        "posterior_experiment_success": round(posterior, 6),
        "posterior_confidence": round(posterior_confidence, 6),
        "mean_net_experiment_value": round(mean_net, 6),
        "experiment_pressure": round(experiment_pressure, 6),
        "reobserve_pressure": round(reobserve_pressure, 6),
        "adapted_minimum_information_gain": round(adapted_minimum, 6),
        "adapted_trial_cooldown_cycles": adapted_cooldown,
        "child_live_trial_enabled": mode == "experiment",
        "child_reobserve_routing_enabled": mode == "reobserve",
        "v0_8_hard_gates_preserved": True,
        "policy_adjustment_not_execution_authority": True,
        "preview_information_gain_not_truth": True,
        "policy_decision_digest": "",
    }
    decision["policy_decision_digest"] = decision_digest(decision)
    return decision


def commit_policy_outcome(
    *,
    policy_run_id: str,
    previous_bundle: Mapping[str, Any],
    decision: Mapping[str, Any],
    child_trial_record: Mapping[str, Any],
    child_experiment_bundle: Mapping[str, Any],
    live_effect: Mapping[str, Any],
    plan: Mapping[str, Any],
    max_outcomes: int,
    max_holonomy: int,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    effect_digest = str(live_effect.get("effect_receipt_digest", ""))
    processed = {
        str(item) for item in as_list(previous_bundle.get("processed_child_effect_digests"))
    }
    if effect_digest in processed:
        existing = next(
            (
                dict(mapping(item))
                for item in reversed(as_list(previous_bundle.get("outcomes")))
                if mapping(item).get("child_effect_receipt_digest") == effect_digest
            ),
            {},
        )
        return dict(previous_bundle), existing, True

    context_key = str(decision.get("context_key", ""))
    old = section_for(previous_bundle, context_key)
    policy_mode = str(decision.get("policy_mode", ""))
    child_mode = str(child_trial_record.get("decision_mode", ""))
    utility = clamp(child_trial_record.get("live_observed_utility"), 0.0)
    cost = clamp(child_trial_record.get("trial_cost"), 0.0)
    risk = clamp(child_trial_record.get("trial_risk"), 0.0)
    recoverability = clamp(child_trial_record.get("trial_recoverability"), 1.0)
    net_value = signed(
        utility
        - clamp(plan.get("outcome_cost_weight")) * cost
        - clamp(plan.get("outcome_risk_weight")) * risk
        + clamp(plan.get("outcome_recoverability_weight")) * recoverability
    )
    resolved = child_trial_record.get("resolved_shadow") is True
    outcome_success = (
        net_value >= signed(plan.get("experiment_success_net_value_floor"), 0.0)
        and str(live_effect.get("outcome", "")) != "blocked"
    )

    section = dict(old)
    cycle_count = integer(old.get("cycle_count"), 0)
    experiment_count = integer(old.get("experiment_count"), 0)
    exploit_count = integer(old.get("exploit_count"), 0)
    reobserve_count = integer(old.get("reobserve_count"), 0)
    section["cycle_count"] = cycle_count + 1
    if policy_mode == "experiment" and child_mode == "licensed_experiment":
        alpha = nonnegative(old.get("experiment_success_alpha"), 1.0)
        beta = nonnegative(old.get("experiment_success_beta"), 1.0)
        section["experiment_success_alpha"] = round(
            alpha + (1.0 if outcome_success else 0.0), 6
        )
        section["experiment_success_beta"] = round(
            beta + (0.0 if outcome_success else 1.0), 6
        )
        section["experiment_count"] = experiment_count + 1
        section["mean_net_experiment_value"] = _mean(
            float(old.get("mean_net_experiment_value", 0.0)), experiment_count, net_value
        )
        section["mean_experiment_utility"] = _mean(
            float(old.get("mean_experiment_utility", 0.0)), experiment_count, utility
        )
        section["mean_experiment_cost"] = _mean(
            float(old.get("mean_experiment_cost", 0.0)), experiment_count, cost
        )
        section["mean_experiment_risk"] = _mean(
            float(old.get("mean_experiment_risk", 0.0)), experiment_count, risk
        )
        section["mean_experiment_recoverability"] = _mean(
            float(old.get("mean_experiment_recoverability", 1.0)),
            experiment_count,
            recoverability,
        )
        section["last_experiment_cycle"] = integer(decision.get("cycle_index"), 0)
    elif policy_mode == "reobserve":
        section["reobserve_count"] = reobserve_count + 1
        section["mean_reobserve_utility"] = _mean(
            float(old.get("mean_reobserve_utility", 0.0)), reobserve_count, utility
        )
        section["last_reobserve_cycle"] = integer(decision.get("cycle_index"), 0)
    else:
        section["exploit_count"] = exploit_count + 1
        section["mean_exploit_utility"] = _mean(
            float(old.get("mean_exploit_utility", 0.0)), exploit_count, utility
        )
        section["last_exploit_cycle"] = integer(decision.get("cycle_index"), 0)

    if resolved:
        section["compatible_resolution_count"] = integer(
            old.get("compatible_resolution_count"), 0
        ) + 1
    else:
        section["unresolved_after_live_count"] = integer(
            old.get("unresolved_after_live_count"), 0
        ) + 1
    section.update(
        {
            "last_policy_mode": policy_mode,
            "last_child_decision_mode": child_mode,
            "last_live_domain_action": live_effect.get("domain_action", ""),
            "last_live_observed_utility": round(utility, 6),
            "last_net_experiment_value": round(net_value, 6),
            "last_compatible_shadow_resolved": resolved,
            "last_child_effect_receipt_digest": effect_digest,
        }
    )
    section["policy_section_digest"] = section_digest(section)

    sections = [
        dict(mapping(item))
        for item in as_list(previous_bundle.get("sections"))
        if mapping(item).get("context_key") != context_key
    ]
    sections.append(section)
    sections.sort(key=lambda item: str(item.get("context_key", "")))
    outcome = {
        "version": OUTCOME_VERSION,
        "policy_run_id": policy_run_id,
        "cycle_index": decision.get("cycle_index", 0),
        "context_key": context_key,
        "policy_mode": policy_mode,
        "policy_reason": decision.get("policy_reason", ""),
        "child_decision_mode": child_mode,
        "child_live_adapter_id": child_trial_record.get("live_adapter_id", ""),
        "live_observed_utility": round(utility, 6),
        "live_domain_action": live_effect.get("domain_action", ""),
        "effect_outcome": live_effect.get("outcome", ""),
        "trial_cost": round(cost, 6),
        "trial_risk": round(risk, 6),
        "trial_recoverability": round(recoverability, 6),
        "net_experiment_value": round(net_value, 6),
        "experiment_outcome_success": outcome_success,
        "compatible_shadow_resolved": resolved,
        "child_trial_record_digest": child_trial_record.get("trial_record_digest", ""),
        "child_experiment_bundle_digest": child_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "child_effect_receipt_digest": effect_digest,
        "policy_decision_digest": decision.get("policy_decision_digest", ""),
        "policy_section_digest": section.get("policy_section_digest", ""),
        "policy_outcome_digest": "",
    }
    outcome["policy_outcome_digest"] = outcome_digest(outcome)
    outcomes = as_list(previous_bundle.get("outcomes")) + [outcome]
    holonomy = as_list(previous_bundle.get("policy_holonomy")) + [
        {
            "policy_run_id": policy_run_id,
            "cycle_index": decision.get("cycle_index", 0),
            "context_key": context_key,
            "policy_mode": policy_mode,
            "child_decision_mode": child_mode,
            "child_effect_receipt_digest": effect_digest,
            "policy_outcome_digest": outcome["policy_outcome_digest"],
            "policy_section_digest": section["policy_section_digest"],
        }
    ]
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": previous_bundle.get("agent_id", ""),
        "generation": integer(previous_bundle.get("generation"), 0) + 1,
        "sections": sections,
        "policy_holonomy": holonomy[-max_holonomy:],
        "outcomes": outcomes[-max_outcomes:],
        "processed_child_effect_digests": sorted(processed | {effect_digest}),
        "last_experiment_bundle_digest": child_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
    }
    updated["policy_bundle_digest"] = bundle_digest(updated)
    return updated, outcome, False
