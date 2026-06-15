#!/usr/bin/env python3
from __future__ import annotations

import math
from typing import Any, Mapping

from runtime.kuuos_adapter_portfolio_shadow_model_v0_7 import (
    build_portfolio_selection,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    BUNDLE_VERSION as PORTFOLIO_BUNDLE_VERSION,
    SELECTION_VERSION as PORTFOLIO_SELECTION_VERSION,
    bundle_digest as portfolio_bundle_digest,
    selection_digest as portfolio_selection_digest,
)
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    BUNDLE_VERSION,
    DECISION_VERSION,
    TRIAL_VERSION,
    as_list,
    bundle_digest,
    clamp,
    decision_digest,
    integer,
    mapping,
    nonnegative,
    sha,
    trial_digest,
)


def portfolio_view(bundle: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": PORTFOLIO_BUNDLE_VERSION,
        "agent_id": bundle.get("agent_id", ""),
        "generation": integer(bundle.get("portfolio_generation"), 0),
        "sections": [dict(mapping(item)) for item in as_list(bundle.get("portfolio_sections"))],
        "pending_predictions": [
            dict(mapping(item)) for item in as_list(bundle.get("pending_predictions"))
        ],
        "resolved_predictions": [
            dict(mapping(item)) for item in as_list(bundle.get("resolved_predictions"))
        ],
        "portfolio_holonomy": [
            dict(mapping(item)) for item in as_list(bundle.get("portfolio_holonomy"))
        ],
        "processed_live_effect_digests": sorted(
            {str(item) for item in as_list(bundle.get("processed_live_effect_digests"))}
        ),
    }
    packet["portfolio_bundle_digest"] = portfolio_bundle_digest(packet)
    return packet


def empty_bundle(
    agent_id: str, source_portfolio_bundle: Mapping[str, Any]
) -> dict[str, Any]:
    source = mapping(source_portfolio_bundle)
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "source_portfolio_bundle_digest": source.get("portfolio_bundle_digest", ""),
        "portfolio_generation": integer(source.get("generation"), 0),
        "portfolio_sections": [
            dict(mapping(item)) for item in as_list(source.get("sections"))
        ],
        "pending_predictions": [
            dict(mapping(item)) for item in as_list(source.get("pending_predictions"))
        ],
        "resolved_predictions": [
            dict(mapping(item)) for item in as_list(source.get("resolved_predictions"))
        ],
        "portfolio_holonomy": [
            dict(mapping(item)) for item in as_list(source.get("portfolio_holonomy"))
        ],
        "processed_live_effect_digests": sorted(
            {str(item) for item in as_list(source.get("processed_live_effect_digests"))}
        ),
        "working_portfolio_bundle_digest": source.get("portfolio_bundle_digest", ""),
        "trial_budget_spent": 0.0,
        "total_trial_count": 0,
        "total_exploit_count": 0,
        "trial_stats": [],
        "trial_records": [],
        "decision_holonomy": [],
        "processed_experiment_effect_digests": [],
    }
    packet["experiment_bundle_digest"] = bundle_digest(packet)
    return packet


def trial_stat(
    bundle: Mapping[str, Any], adapter_id: str, context_key: str
) -> dict[str, Any]:
    for raw in as_list(bundle.get("trial_stats")):
        stat = dict(mapping(raw))
        if (
            stat.get("federation_adapter_id") == adapter_id
            and stat.get("context_key") == context_key
        ):
            return stat
    return {
        "federation_adapter_id": adapter_id,
        "context_key": context_key,
        "trial_count": 0,
        "last_trial_cycle": -1000000,
        "cumulative_trial_cost": 0.0,
        "mean_trial_utility": 0.0,
        "last_trial_effect_receipt_digest": "",
    }


def _entry_by_id(registry: Mapping[str, Any], adapter_id: str) -> dict[str, Any]:
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if entry.get("federation_adapter_id") == adapter_id:
            return entry
    return {}


def _candidate_by_id(selection: Mapping[str, Any], adapter_id: str) -> dict[str, Any]:
    for raw in as_list(selection.get("candidates")):
        candidate = dict(mapping(raw))
        if candidate.get("federation_adapter_id") == adapter_id:
            return candidate
    return {}


def _pending_count(portfolio: Mapping[str, Any], adapter_id: str, context_key: str) -> int:
    return sum(
        1
        for raw in as_list(portfolio.get("pending_predictions"))
        if mapping(raw).get("federation_adapter_id") == adapter_id
        and mapping(raw).get("context_key") == context_key
        and mapping(raw).get("status") == "pending"
    )


def build_experiment_decision(
    *,
    experiment_run_id: str,
    cycle_index: int,
    capability_bundle: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    normalized_wake: Mapping[str, Any],
    plan: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    portfolio = portfolio_view(experiment_bundle)
    baseline, _ = build_portfolio_selection(
        portfolio_run_id=experiment_run_id + ":baseline",
        capability_bundle=capability_bundle,
        portfolio_bundle=portfolio,
        registry=registry,
        source_packets=source_packets,
        normalized_wake=normalized_wake,
        exploration_weight=clamp(plan.get("exploration_weight")),
        max_exploration_bonus=clamp(plan.get("max_exploration_bonus")),
        curvature_penalty=clamp(plan.get("curvature_penalty")),
        resolved_evidence_weight=clamp(plan.get("resolved_evidence_weight")),
        max_portfolio_adjustment=clamp(plan.get("max_portfolio_adjustment")),
        blockers=blockers,
    )
    if blockers:
        return {}, {}

    baseline_id = str(baseline.get("live_adapter_id", ""))
    context_key = str(baseline.get("context_key", ""))
    baseline_score = float(baseline.get("live_adjusted_score", 0.0))
    total_trials = integer(experiment_bundle.get("total_trial_count"), 0)
    spent = nonnegative(experiment_bundle.get("trial_budget_spent"), 0.0)
    total_budget = nonnegative(plan.get("total_trial_budget"), 0.0)
    remaining = max(0.0, total_budget - spent)
    max_total = integer(plan.get("max_live_trials_total"), 0)
    max_per_context = integer(plan.get("max_live_trials_per_adapter_context"), 0)
    cooldown = integer(plan.get("trial_cooldown_cycles"), 0)

    scored: list[dict[str, Any]] = []
    for raw in as_list(baseline.get("candidates")):
        candidate = dict(mapping(raw))
        adapter_id = str(candidate.get("federation_adapter_id", ""))
        if adapter_id == baseline_id:
            continue
        entry = _entry_by_id(registry, adapter_id)
        stat = trial_stat(experiment_bundle, adapter_id, context_key)
        observations = integer(candidate.get("observation_count"), 0)
        reliability = clamp(candidate.get("portfolio_reliability"), 0.0)
        resolved = integer(candidate.get("resolved_shadow_count"), 0)
        pending = _pending_count(portfolio, adapter_id, context_key)
        trial_count = integer(stat.get("trial_count"), 0)
        last_trial_cycle = integer(stat.get("last_trial_cycle"), -1000000)

        observation_uncertainty = min(1.0, 1.0 / math.sqrt(observations + 1.0))
        prediction_uncertainty = 1.0 - reliability
        uncertainty = 0.5 * observation_uncertainty + 0.5 * prediction_uncertainty
        unresolved_signal = min(1.0, pending / max(1.0, float(resolved + 1)))
        novelty = min(1.0, 1.0 / math.sqrt(trial_count + 1.0))
        score_gap = max(
            0.0,
            baseline_score - float(candidate.get("adjusted_selection_score", 0.0)),
        )
        information_gain = max(
            0.0,
            min(
                1.5,
                clamp(plan.get("uncertainty_weight")) * uncertainty
                + clamp(plan.get("unresolved_shadow_weight")) * unresolved_signal
                + clamp(plan.get("trial_novelty_weight")) * novelty
                - clamp(plan.get("opportunity_cost_weight")) * score_gap,
            ),
        )
        cost = nonnegative(
            entry.get("experiment_cost"),
            nonnegative(plan.get("default_trial_cost"), 0.0),
        )
        risk = clamp(
            entry.get("experiment_risk_prior"),
            clamp(plan.get("default_trial_risk"), 0.0),
        )
        recoverability = clamp(
            entry.get("experiment_recoverability_prior"),
            clamp(plan.get("default_trial_recoverability"), 1.0),
        )
        reasons: list[str] = []
        if total_trials >= max_total:
            reasons.append("global_trial_count_exhausted")
        if trial_count >= max_per_context:
            reasons.append("adapter_context_trial_count_exhausted")
        if cycle_index - last_trial_cycle <= cooldown:
            reasons.append("trial_cooldown_active")
        if information_gain < clamp(plan.get("minimum_information_gain")):
            reasons.append("information_gain_below_threshold")
        if cost > nonnegative(plan.get("maximum_trial_cost"), 0.0):
            reasons.append("trial_cost_above_per_trial_limit")
        if cost > remaining:
            reasons.append("trial_budget_insufficient")
        if risk > clamp(plan.get("maximum_trial_risk")):
            reasons.append("trial_risk_above_limit")
        if recoverability < clamp(plan.get("minimum_trial_recoverability")):
            reasons.append("trial_recoverability_below_floor")
        if entry.get("external_network_effect_allowed") is not False:
            reasons.append("adapter_external_network_boundary_invalid")
        if license_packet.get("licensed_live_trial_allowed") is not True:
            reasons.append("licensed_live_trial_not_allowed")
        scored.append(
            {
                "federation_adapter_id": adapter_id,
                "adapter_profile_digest": candidate.get("adapter_profile_digest", ""),
                "observation_count": observations,
                "portfolio_reliability": round(reliability, 6),
                "resolved_shadow_count": resolved,
                "pending_shadow_count": pending,
                "prior_trial_count": trial_count,
                "last_trial_cycle": last_trial_cycle,
                "observation_uncertainty": round(observation_uncertainty, 6),
                "prediction_uncertainty": round(prediction_uncertainty, 6),
                "combined_uncertainty": round(uncertainty, 6),
                "unresolved_shadow_signal": round(unresolved_signal, 6),
                "trial_novelty": round(novelty, 6),
                "baseline_score_gap": round(score_gap, 6),
                "expected_information_gain": round(information_gain, 6),
                "trial_cost": round(cost, 6),
                "trial_risk": round(risk, 6),
                "trial_recoverability": round(recoverability, 6),
                "eligible_for_trial": not reasons,
                "ineligibility_reasons": reasons,
                "adjusted_selection_score": candidate.get("adjusted_selection_score", 0.0),
            }
        )

    eligible = [item for item in scored if item.get("eligible_for_trial") is True]
    eligible.sort(
        key=lambda item: (
            -float(item.get("expected_information_gain", 0.0)),
            -float(item.get("adjusted_selection_score", 0.0)),
            str(item.get("federation_adapter_id", "")),
        )
    )
    selected_trial = eligible[0] if eligible else {}
    mode = "licensed_experiment" if selected_trial else "exploit_baseline"
    live_id = str(selected_trial.get("federation_adapter_id", baseline_id))
    live_candidate = _candidate_by_id(baseline, live_id)
    entry = _entry_by_id(registry, live_id)
    trial_cost = float(selected_trial.get("trial_cost", 0.0)) if selected_trial else 0.0
    decision = {
        "version": DECISION_VERSION,
        "experiment_run_id": experiment_run_id,
        "cycle_index": cycle_index,
        "source_batch_digest": baseline.get("source_batch_digest", ""),
        "normalized_wake_digest": baseline.get("normalized_wake_digest", ""),
        "capability_bundle_digest": capability_bundle.get("capability_bundle_digest", ""),
        "experiment_bundle_digest": experiment_bundle.get("experiment_bundle_digest", ""),
        "working_portfolio_bundle_digest": portfolio.get("portfolio_bundle_digest", ""),
        "baseline_portfolio_selection_digest": baseline.get("portfolio_selection_digest", ""),
        "context_key": context_key,
        "context_signature": baseline.get("context_signature", {}),
        "decision_mode": mode,
        "baseline_adapter_id": baseline_id,
        "live_adapter_id": live_id,
        "experiment_adapter_id": live_id if selected_trial else "",
        "live_adapter_profile_digest": live_candidate.get("adapter_profile_digest", ""),
        "baseline_adjusted_score": round(baseline_score, 6),
        "live_adjusted_score": live_candidate.get("adjusted_selection_score", 0.0),
        "expected_information_gain": selected_trial.get("expected_information_gain", 0.0),
        "trial_cost": round(trial_cost, 6),
        "trial_risk": selected_trial.get("trial_risk", 0.0),
        "trial_recoverability": selected_trial.get("trial_recoverability", 1.0),
        "trial_budget_total": round(total_budget, 6),
        "trial_budget_spent_before": round(spent, 6),
        "trial_budget_remaining_before": round(remaining, 6),
        "trial_budget_after_if_committed": round(max(0.0, remaining - trial_cost), 6),
        "total_trial_count_before": total_trials,
        "candidate_experiments": scored,
        "one_live_adapter": True,
        "experiment_override_requires_live_effect": True,
        "shadow_candidates_non_actuating": True,
        "information_gain_estimate_not_truth": True,
        "static_priority_used_only_as_tie_break": True,
    }
    decision["experiment_decision_digest"] = decision_digest(decision)
    return decision, entry


def build_execution_selection(
    *,
    experiment_run_id: str,
    decision: Mapping[str, Any],
    capability_bundle: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
    registry: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    normalized_wake: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    baseline, _ = build_portfolio_selection(
        portfolio_run_id=experiment_run_id + ":execution-selection",
        capability_bundle=capability_bundle,
        portfolio_bundle=portfolio_view(experiment_bundle),
        registry=registry,
        source_packets=source_packets,
        normalized_wake=normalized_wake,
        exploration_weight=clamp(plan.get("exploration_weight")),
        max_exploration_bonus=clamp(plan.get("max_exploration_bonus")),
        curvature_penalty=clamp(plan.get("curvature_penalty")),
        resolved_evidence_weight=clamp(plan.get("resolved_evidence_weight")),
        max_portfolio_adjustment=clamp(plan.get("max_portfolio_adjustment")),
        blockers=blockers,
    )
    if blockers:
        return {}
    live_id = str(decision.get("live_adapter_id", ""))
    candidate = _candidate_by_id(baseline, live_id)
    if not candidate:
        blockers.append("experiment_live_candidate_missing")
        return {}
    packet = dict(baseline)
    packet.update(
        {
            "version": PORTFOLIO_SELECTION_VERSION,
            "portfolio_run_id": experiment_run_id + ":realized-live",
            "live_adapter_id": live_id,
            "live_adapter_profile_digest": candidate.get("adapter_profile_digest", ""),
            "live_base_score": candidate.get("selection_score", 0.0),
            "live_portfolio_adjustment": candidate.get("portfolio_adjustment", 0.0),
            "live_adjusted_score": candidate.get("adjusted_selection_score", 0.0),
            "shadow_candidates": [
                mapping(item).get("federation_adapter_id", "")
                for item in as_list(baseline.get("candidates"))
                if mapping(item).get("federation_adapter_id") != live_id
            ],
            "baseline_live_adapter_id": decision.get("baseline_adapter_id", ""),
            "selected_by_v0_8_experiment_scheduler": True,
            "experiment_decision_mode": decision.get("decision_mode", ""),
            "experiment_decision_digest": decision.get("experiment_decision_digest", ""),
            "licensed_experiment_override": decision.get("decision_mode") == "licensed_experiment",
        }
    )
    packet.pop("portfolio_selection_digest", None)
    packet["portfolio_selection_digest"] = portfolio_selection_digest(packet)
    return packet


def commit_cycle(
    *,
    experiment_run_id: str,
    previous_bundle: Mapping[str, Any],
    updated_portfolio: Mapping[str, Any],
    decision: Mapping[str, Any],
    live_observed_utility: float,
    live_effect_receipt_digest: str,
    effect_outcome: str,
    resolved_shadow: bool,
    max_trial_records: int,
    max_decision_holonomy: int,
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    processed = {
        str(item)
        for item in as_list(previous_bundle.get("processed_experiment_effect_digests"))
    }
    if live_effect_receipt_digest in processed:
        existing = next(
            (
                dict(mapping(item))
                for item in reversed(as_list(previous_bundle.get("trial_records")))
                if mapping(item).get("live_effect_receipt_digest") == live_effect_receipt_digest
            ),
            {},
        )
        return dict(previous_bundle), existing, True

    mode = str(decision.get("decision_mode", ""))
    is_trial = mode == "licensed_experiment"
    cost = nonnegative(decision.get("trial_cost"), 0.0) if is_trial else 0.0
    before = nonnegative(previous_bundle.get("trial_budget_spent"), 0.0)
    after = before + cost
    live_id = str(decision.get("live_adapter_id", ""))
    context_key = str(decision.get("context_key", ""))
    stats = [dict(mapping(item)) for item in as_list(previous_bundle.get("trial_stats"))]
    stat = trial_stat(previous_bundle, live_id, context_key)
    if is_trial:
        old_count = integer(stat.get("trial_count"), 0)
        old_mean = float(stat.get("mean_trial_utility", 0.0))
        stat.update(
            {
                "trial_count": old_count + 1,
                "last_trial_cycle": integer(decision.get("cycle_index"), 0),
                "cumulative_trial_cost": round(
                    nonnegative(stat.get("cumulative_trial_cost"), 0.0) + cost, 6
                ),
                "mean_trial_utility": round(
                    (old_mean * old_count + live_observed_utility) / (old_count + 1), 6
                ),
                "last_trial_effect_receipt_digest": live_effect_receipt_digest,
            }
        )
        stats = [
            item
            for item in stats
            if not (
                item.get("federation_adapter_id") == live_id
                and item.get("context_key") == context_key
            )
        ]
        stats.append(stat)
        stats.sort(
            key=lambda item: (
                str(item.get("context_key", "")),
                str(item.get("federation_adapter_id", "")),
            )
        )

    record = {
        "version": TRIAL_VERSION,
        "experiment_run_id": experiment_run_id,
        "cycle_index": decision.get("cycle_index", 0),
        "decision_mode": mode,
        "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
        "live_adapter_id": live_id,
        "experiment_adapter_id": decision.get("experiment_adapter_id", ""),
        "context_key": context_key,
        "expected_information_gain": decision.get("expected_information_gain", 0.0),
        "trial_cost": round(cost, 6),
        "trial_risk": decision.get("trial_risk", 0.0),
        "trial_recoverability": decision.get("trial_recoverability", 1.0),
        "trial_budget_spent_before": round(before, 6),
        "trial_budget_spent_after": round(after, 6),
        "live_observed_utility": round(live_observed_utility, 6),
        "effect_outcome": effect_outcome,
        "resolved_shadow": bool(resolved_shadow),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "experiment_decision_digest": decision.get("experiment_decision_digest", ""),
        "trial_debited_after_live_effect": is_trial,
        "shadow_execution_count": 0,
        "trial_record_digest": "",
    }
    record["trial_record_digest"] = trial_digest(record)

    holonomy = as_list(previous_bundle.get("decision_holonomy")) + [
        {
            "experiment_run_id": experiment_run_id,
            "cycle_index": decision.get("cycle_index", 0),
            "decision_mode": mode,
            "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
            "live_adapter_id": live_id,
            "expected_information_gain": decision.get("expected_information_gain", 0.0),
            "live_effect_receipt_digest": live_effect_receipt_digest,
            "trial_record_digest": record["trial_record_digest"],
            "working_portfolio_bundle_digest": updated_portfolio.get(
                "portfolio_bundle_digest", ""
            ),
        }
    ]
    records = as_list(previous_bundle.get("trial_records")) + [record]
    updated = {
        "version": BUNDLE_VERSION,
        "agent_id": previous_bundle.get("agent_id", ""),
        "generation": integer(previous_bundle.get("generation"), 0) + 1,
        "source_portfolio_bundle_digest": previous_bundle.get(
            "source_portfolio_bundle_digest", ""
        ),
        "portfolio_generation": integer(updated_portfolio.get("generation"), 0),
        "portfolio_sections": [
            dict(mapping(item)) for item in as_list(updated_portfolio.get("sections"))
        ],
        "pending_predictions": [
            dict(mapping(item))
            for item in as_list(updated_portfolio.get("pending_predictions"))
        ],
        "resolved_predictions": [
            dict(mapping(item))
            for item in as_list(updated_portfolio.get("resolved_predictions"))
        ],
        "portfolio_holonomy": [
            dict(mapping(item))
            for item in as_list(updated_portfolio.get("portfolio_holonomy"))
        ],
        "processed_live_effect_digests": sorted(
            {
                str(item)
                for item in as_list(updated_portfolio.get("processed_live_effect_digests"))
            }
        ),
        "working_portfolio_bundle_digest": updated_portfolio.get(
            "portfolio_bundle_digest", ""
        ),
        "trial_budget_spent": round(after, 6),
        "total_trial_count": integer(previous_bundle.get("total_trial_count"), 0)
        + (1 if is_trial else 0),
        "total_exploit_count": integer(previous_bundle.get("total_exploit_count"), 0)
        + (0 if is_trial else 1),
        "trial_stats": stats,
        "trial_records": records[-max_trial_records:],
        "decision_holonomy": holonomy[-max_decision_holonomy:],
        "processed_experiment_effect_digests": sorted(
            processed | {live_effect_receipt_digest}
        ),
    }
    updated["experiment_bundle_digest"] = bundle_digest(updated)
    return updated, record, False
