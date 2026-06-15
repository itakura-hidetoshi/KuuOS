#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    BUNDLE_VERSION,
    DECISION_VERSION,
    HORIZONS,
    MODES,
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

TERMINAL_SECTION_STATES = {"flat_complete", "handed_over", "superseded"}


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "horizon_holonomy": [],
        "outcomes": [],
        "processed_child_regret_outcome_digests": [],
        "processed_child_effect_digests": [],
        "last_regret_bundle_digest": "",
        "last_gauge_bundle_digest": "",
    }
    packet["horizon_bundle_digest"] = bundle_digest(packet)
    return packet


def initial_section(context_key: str) -> dict[str, Any]:
    packet: dict[str, Any] = {
        "version": SECTION_VERSION,
        "section_id": "horizon-section-" + sha(context_key)[:18],
        "context_key": context_key,
        "cycle_count": 0,
        "short_cycle_count": 0,
        "medium_cycle_count": 0,
        "long_cycle_count": 0,
        "cumulative_commitment_progress": 0.0,
        "mean_commitment_progress": 0.0,
        "cumulative_recovery_cost": 0.0,
        "mean_recovery_cost": 0.0,
        "delayed_compatible_evidence_count": 0,
        "terminal_section_observation_count": 0,
        "last_child_policy_mode": "",
        "last_child_domain_action": "",
        "last_commitment_progress_score": 0.0,
        "last_recovery_cost": 0.0,
        "last_terminal_section_ratio": 0.0,
        "last_mean_curvature_norm": 0.0,
        "last_delayed_compatible_evidence_count": 0,
        "last_child_regret_outcome_digest": "",
        "last_child_effect_receipt_digest": "",
    }
    for horizon in HORIZONS:
        for mode in MODES:
            packet[f"{horizon}_{mode}_credit"] = 0.0
    packet["horizon_section_digest"] = section_digest(packet)
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


def aggregate_mode_support(
    section: Mapping[str, Any], plan: Mapping[str, Any], mode: str
) -> float:
    return clamp(
        clamp(plan.get("short_horizon_weight"))
        * clamp(section.get(f"short_{mode}_credit"))
        + clamp(plan.get("medium_horizon_weight"))
        * clamp(section.get(f"medium_{mode}_credit"))
        + clamp(plan.get("long_horizon_weight"))
        * clamp(section.get(f"long_{mode}_credit"))
    )


def build_horizon_decision(
    *,
    horizon_run_id: str,
    cycle_index: int,
    context_key: str,
    horizon_bundle: Mapping[str, Any],
    regret_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    section = section_for(horizon_bundle, context_key)
    experiment_support = aggregate_mode_support(section, plan, "experiment")
    reobserve_support = aggregate_mode_support(section, plan, "reobserve")
    exploit_support = aggregate_mode_support(section, plan, "exploit")

    threshold_gain = clamp(plan.get("horizon_threshold_gain"))
    resistance_gain = clamp(plan.get("horizon_exploit_resistance_gain"))
    experiment_threshold = _bounded(
        clamp(plan.get("base_experiment_pressure_threshold"))
        - threshold_gain * experiment_support
        + resistance_gain * exploit_support,
        clamp(plan.get("minimum_experiment_pressure_threshold")),
        clamp(plan.get("maximum_experiment_pressure_threshold"), 1.0),
    )
    reobserve_threshold = _bounded(
        clamp(plan.get("base_reobserve_pressure_threshold"))
        - threshold_gain * reobserve_support
        + resistance_gain * exploit_support,
        clamp(plan.get("minimum_reobserve_pressure_threshold")),
        clamp(plan.get("maximum_reobserve_pressure_threshold"), 1.0),
    )

    interval_gain = integer(plan.get("horizon_interval_gain_cycles"), 0)
    exploit_interval_gain = integer(
        plan.get("horizon_exploit_interval_gain_cycles"), 0
    )
    experiment_interval = _bounded_int(
        integer(plan.get("base_policy_cycles_between_experiments"), 0)
        - round(interval_gain * experiment_support)
        + round(exploit_interval_gain * exploit_support),
        integer(plan.get("minimum_policy_cycles_between_experiments"), 0),
        integer(plan.get("maximum_policy_cycles_between_experiments"), 100000),
    )
    reobserve_interval = _bounded_int(
        integer(plan.get("base_policy_cycles_between_reobservations"), 0)
        - round(interval_gain * reobserve_support)
        + round(exploit_interval_gain * exploit_support),
        integer(plan.get("minimum_policy_cycles_between_reobservations"), 0),
        integer(plan.get("maximum_policy_cycles_between_reobservations"), 100000),
    )

    decision = {
        "version": DECISION_VERSION,
        "horizon_run_id": horizon_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "source_regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "short_horizon_weight": round(clamp(plan.get("short_horizon_weight")), 6),
        "medium_horizon_weight": round(clamp(plan.get("medium_horizon_weight")), 6),
        "long_horizon_weight": round(clamp(plan.get("long_horizon_weight")), 6),
        "aggregate_experiment_support": round(experiment_support, 6),
        "aggregate_reobserve_support": round(reobserve_support, 6),
        "aggregate_exploit_support": round(exploit_support, 6),
        "adapted_base_experiment_threshold": round(experiment_threshold, 6),
        "adapted_base_reobserve_threshold": round(reobserve_threshold, 6),
        "adapted_base_experiment_interval": experiment_interval,
        "adapted_base_reobserve_interval": reobserve_interval,
        "short_medium_long_credits_distinct": True,
        "actual_effect_required_for_credit_update": True,
        "v0_10_regret_authority_unchanged": True,
        "v0_8_hard_gates_preserved": True,
        "horizon_decision_digest": "",
    }
    decision["horizon_decision_digest"] = decision_digest(decision)
    return decision


def gauge_metrics(
    *,
    effect: Mapping[str, Any],
    gauge_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    sections = [dict(mapping(item)) for item in as_list(gauge_bundle.get("local_sections"))]
    terminal = 0
    curvatures: list[float] = []
    for section in sections:
        state = str(
            section.get(
                "section_state",
                section.get("state", section.get("status", "")),
            )
        )
        if state in TERMINAL_SECTION_STATES:
            terminal += 1
        curvatures.append(clamp(section.get("curvature_norm"), 0.0))
    terminal_ratio = terminal / max(1.0, float(len(sections)))
    mean_curvature = sum(curvatures) / max(1.0, float(len(curvatures)))
    holonomy_depth = len(as_list(gauge_bundle.get("holonomy_trace")))
    holonomy_scale = max(1.0, nonnegative(plan.get("long_holonomy_scale"), 8.0))
    holonomy_score = clamp(holonomy_depth / holonomy_scale)

    progress_delta = clamp(effect.get("progress_delta"), 0.0)
    observed_benefit = clamp(effect.get("observed_benefit"), 0.0)
    observed_harm = clamp(effect.get("observed_harm"), 0.0)
    recoverability = clamp(effect.get("recoverability"), 1.0)
    confidence = clamp(effect.get("confidence"), 0.0)
    continuation = str(effect.get("continuation_signal", ""))

    progress_score = clamp(
        clamp(plan.get("progress_delta_weight")) * progress_delta
        + clamp(plan.get("observed_benefit_weight")) * observed_benefit
        + clamp(plan.get("terminal_ratio_weight")) * terminal_ratio
        + clamp(plan.get("effect_confidence_weight")) * confidence
    )
    continuation_cost = (
        clamp(plan.get("repair_continuation_cost"))
        if continuation in {"repair", "reobserve"}
        else 0.0
    )
    recovery_cost = clamp(
        clamp(plan.get("observed_harm_weight")) * observed_harm
        + clamp(plan.get("recoverability_deficit_weight")) * (1.0 - recoverability)
        + clamp(plan.get("curvature_cost_weight")) * mean_curvature
        + continuation_cost
    )
    return {
        "progress_delta": round(progress_delta, 6),
        "observed_benefit": round(observed_benefit, 6),
        "observed_harm": round(observed_harm, 6),
        "recoverability": round(recoverability, 6),
        "effect_confidence": round(confidence, 6),
        "continuation_signal": continuation,
        "commitment_progress_score": round(progress_score, 6),
        "recovery_cost": round(recovery_cost, 6),
        "terminal_section_ratio": round(terminal_ratio, 6),
        "mean_curvature_norm": round(mean_curvature, 6),
        "holonomy_depth": holonomy_depth,
        "holonomy_score": round(holonomy_score, 6),
    }


def _decayed_credits(section: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, float]:
    output: dict[str, float] = {}
    for horizon in HORIZONS:
        decay = clamp(plan.get(f"{horizon}_credit_decay"), 1.0)
        for mode in MODES:
            output[f"{horizon}_{mode}"] = clamp(
                clamp(section.get(f"{horizon}_{mode}_credit")) * decay
            )
    return output


def _add_credit(credits: dict[str, float], horizon: str, mode: str, value: float) -> None:
    if mode not in MODES:
        return
    key = f"{horizon}_{mode}"
    credits[key] = clamp(credits.get(key, 0.0) + max(0.0, value))


def commit_horizon_outcome(
    *,
    horizon_run_id: str,
    cycle_index: int,
    previous_bundle: Mapping[str, Any],
    child_regret_bundle: Mapping[str, Any],
    child_regret_outcome: Mapping[str, Any],
    effect: Mapping[str, Any],
    gauge_bundle: Mapping[str, Any],
    decision: Mapping[str, Any],
    plan: Mapping[str, Any],
    max_outcomes: int,
    max_holonomy: int,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    child_outcome_digest = str(child_regret_outcome.get("regret_outcome_digest", ""))
    processed = {
        str(item)
        for item in as_list(previous_bundle.get("processed_child_regret_outcome_digests"))
    }
    if child_outcome_digest in processed:
        existing = next(
            (
                dict(mapping(item))
                for item in reversed(as_list(previous_bundle.get("outcomes")))
                if mapping(item).get("child_regret_outcome_digest") == child_outcome_digest
            ),
            {},
        )
        return dict(previous_bundle), existing, True

    context_key = str(decision.get("context_key", ""))
    old = section_for(previous_bundle, context_key)
    credits = _decayed_credits(old, plan)
    chosen_mode = str(child_regret_outcome.get("child_policy_mode", ""))
    best_alternative = str(child_regret_outcome.get("best_alternative_mode", ""))
    chosen_value = clamp(max(0.0, signed(child_regret_outcome.get("chosen_value"), 0.0)))
    bounded_regret = clamp(child_regret_outcome.get("bounded_regret"), 0.0)
    delayed_count = integer(
        child_regret_outcome.get("delayed_compatible_evidence_count"), 0
    )
    delayed_scale = max(1.0, nonnegative(plan.get("delayed_evidence_scale"), 4.0))
    delayed_density = clamp(delayed_count / delayed_scale)
    metrics = gauge_metrics(effect=effect, gauge_bundle=gauge_bundle, plan=plan)
    progress = clamp(metrics.get("commitment_progress_score"))
    recovery_cost = clamp(metrics.get("recovery_cost"))
    terminal_ratio = clamp(metrics.get("terminal_section_ratio"))
    holonomy_score = clamp(metrics.get("holonomy_score"))

    _add_credit(
        credits,
        "short",
        chosen_mode,
        clamp(plan.get("short_value_learning_rate")) * chosen_value,
    )
    _add_credit(
        credits,
        "short",
        best_alternative,
        clamp(plan.get("short_regret_learning_rate")) * bounded_regret,
    )

    _add_credit(
        credits,
        "medium",
        chosen_mode,
        clamp(plan.get("medium_progress_learning_rate")) * progress,
    )
    _add_credit(
        credits,
        "medium",
        "reobserve",
        clamp(plan.get("medium_recovery_learning_rate")) * recovery_cost,
    )
    _add_credit(
        credits,
        "medium",
        best_alternative,
        clamp(plan.get("medium_delayed_learning_rate")) * delayed_density,
    )

    long_active = integer(old.get("cycle_count"), 0) + 1 >= integer(
        plan.get("long_horizon_activation_cycles"), 2
    )
    if long_active:
        _add_credit(
            credits,
            "long",
            chosen_mode,
            clamp(plan.get("long_progress_learning_rate"))
            * clamp(progress * (0.5 + 0.5 * holonomy_score)),
        )
        _add_credit(
            credits,
            "long",
            "exploit",
            clamp(plan.get("long_terminal_learning_rate")) * terminal_ratio,
        )
        _add_credit(
            credits,
            "long",
            "reobserve",
            clamp(plan.get("long_recovery_learning_rate")) * recovery_cost,
        )
        _add_credit(
            credits,
            "long",
            best_alternative,
            clamp(plan.get("long_delayed_learning_rate")) * delayed_density,
        )

    cycle_count = integer(old.get("cycle_count"), 0)
    old_progress_mean = nonnegative(old.get("mean_commitment_progress"), 0.0)
    old_recovery_mean = nonnegative(old.get("mean_recovery_cost"), 0.0)
    section = dict(old)
    section.update(
        {
            "cycle_count": cycle_count + 1,
            "short_cycle_count": integer(old.get("short_cycle_count"), 0) + 1,
            "medium_cycle_count": integer(old.get("medium_cycle_count"), 0) + 1,
            "long_cycle_count": integer(old.get("long_cycle_count"), 0)
            + (1 if long_active else 0),
            "cumulative_commitment_progress": round(
                nonnegative(old.get("cumulative_commitment_progress"), 0.0) + progress,
                6,
            ),
            "mean_commitment_progress": round(
                (old_progress_mean * cycle_count + progress) / (cycle_count + 1), 6
            ),
            "cumulative_recovery_cost": round(
                nonnegative(old.get("cumulative_recovery_cost"), 0.0) + recovery_cost,
                6,
            ),
            "mean_recovery_cost": round(
                (old_recovery_mean * cycle_count + recovery_cost) / (cycle_count + 1), 6
            ),
            "delayed_compatible_evidence_count": integer(
                old.get("delayed_compatible_evidence_count"), 0
            )
            + delayed_count,
            "terminal_section_observation_count": integer(
                old.get("terminal_section_observation_count"), 0
            )
            + (1 if terminal_ratio > 0.0 else 0),
            "last_child_policy_mode": chosen_mode,
            "last_child_domain_action": effect.get("domain_action", ""),
            "last_commitment_progress_score": round(progress, 6),
            "last_recovery_cost": round(recovery_cost, 6),
            "last_terminal_section_ratio": round(terminal_ratio, 6),
            "last_mean_curvature_norm": metrics.get("mean_curvature_norm", 0.0),
            "last_delayed_compatible_evidence_count": delayed_count,
            "last_child_regret_outcome_digest": child_outcome_digest,
            "last_child_effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        }
    )
    for horizon in HORIZONS:
        for mode in MODES:
            section[f"{horizon}_{mode}_credit"] = round(
                credits[f"{horizon}_{mode}"], 6
            )
    section["horizon_section_digest"] = section_digest(section)

    outcome = {
        "version": OUTCOME_VERSION,
        "horizon_run_id": horizon_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "child_policy_mode": chosen_mode,
        "child_live_domain_action": effect.get("domain_action", ""),
        "chosen_value": round(chosen_value, 6),
        "best_alternative_mode": best_alternative,
        "bounded_regret": round(bounded_regret, 6),
        "delayed_compatible_evidence_count": delayed_count,
        "delayed_evidence_density": round(delayed_density, 6),
        **metrics,
        "long_horizon_active": long_active,
        "credits_after": {
            horizon: {
                mode: round(credits[f"{horizon}_{mode}"], 6) for mode in MODES
            }
            for horizon in HORIZONS
        },
        "aggregate_support_after": {
            mode: round(aggregate_mode_support(section, plan, mode), 6)
            for mode in MODES
        },
        "child_regret_bundle_digest": child_regret_bundle.get(
            "regret_bundle_digest", ""
        ),
        "child_regret_outcome_digest": child_outcome_digest,
        "child_effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        "gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
        "horizon_decision_digest": decision.get("horizon_decision_digest", ""),
        "actual_effect_required_for_credit_update": True,
        "delayed_compatible_evidence_not_immediate_truth": True,
        "horizon_outcome_digest": "",
    }
    outcome["horizon_outcome_digest"] = outcome_digest(outcome)

    sections = [
        dict(mapping(item))
        for item in as_list(previous_bundle.get("sections"))
        if mapping(item).get("context_key") != context_key
    ]
    sections.append(section)
    sections.sort(key=lambda item: str(item.get("context_key", "")))
    outcomes = as_list(previous_bundle.get("outcomes")) + [outcome]
    holonomy = as_list(previous_bundle.get("horizon_holonomy")) + [
        {
            "horizon_run_id": horizon_run_id,
            "cycle_index": cycle_index,
            "context_key": context_key,
            "child_policy_mode": chosen_mode,
            "commitment_progress_score": round(progress, 6),
            "recovery_cost": round(recovery_cost, 6),
            "terminal_section_ratio": round(terminal_ratio, 6),
            "horizon_outcome_digest": outcome["horizon_outcome_digest"],
            "horizon_section_digest": section["horizon_section_digest"],
        }
    ]
    effect_digest = str(effect.get("effect_receipt_digest", ""))
    processed_effects = {
        str(item) for item in as_list(previous_bundle.get("processed_child_effect_digests"))
    }
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": previous_bundle.get("agent_id", ""),
        "generation": integer(previous_bundle.get("generation"), 0) + 1,
        "sections": sections,
        "horizon_holonomy": holonomy[-max_holonomy:],
        "outcomes": outcomes[-max_outcomes:],
        "processed_child_regret_outcome_digests": sorted(
            processed | {child_outcome_digest}
        ),
        "processed_child_effect_digests": sorted(processed_effects | {effect_digest}),
        "last_regret_bundle_digest": child_regret_bundle.get(
            "regret_bundle_digest", ""
        ),
        "last_gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
    }
    updated["horizon_bundle_digest"] = bundle_digest(updated)
    return updated, outcome, False
