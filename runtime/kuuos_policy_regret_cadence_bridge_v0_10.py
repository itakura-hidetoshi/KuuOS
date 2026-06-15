#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    LICENSE_VERSION as POLICY_LICENSE_VERSION,
    PLAN_VERSION as POLICY_PLAN_VERSION,
    REQUIRED_BOUNDARY as POLICY_REQUIRED_BOUNDARY,
    plan_digest as policy_plan_digest,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    clamp,
    integer,
    mapping,
    nonnegative,
    signed,
)


def build_child_policy_plan(
    *,
    regret_plan: Mapping[str, Any],
    regret_decision: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    previous_capability_state: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    previous_experiment_state: Mapping[str, Any],
    previous_experiment_bundle: Mapping[str, Any],
    previous_policy_state: Mapping[str, Any],
    previous_policy_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": POLICY_PLAN_VERSION,
        "policy_run_id": str(regret_plan.get("regret_run_id", "")) + ":policy",
        "agent_id": str(regret_plan.get("agent_id", "")),
        "expected_source_batch_digest": batch_digest(source_packets),
        "expected_root_principles_digest": root_packet.get(
            "root_principles_digest", ""
        ),
        "expected_adapter_registry_digest": adapter_registry.get(
            "adapter_registry_digest", ""
        ),
        "expected_previous_capability_state_digest": previous_capability_state.get(
            "capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": previous_capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "expected_source_portfolio_bundle_digest": source_portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
        "expected_previous_experiment_state_digest": previous_experiment_state.get(
            "experiment_state_digest", ""
        ),
        "expected_previous_experiment_bundle_digest": previous_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "expected_previous_policy_state_digest": previous_policy_state.get(
            "policy_state_digest", ""
        ),
        "expected_previous_policy_bundle_digest": previous_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "learning_rate": clamp(regret_plan.get("learning_rate")),
        "exploration_weight": clamp(regret_plan.get("exploration_weight")),
        "max_exploration_bonus": clamp(regret_plan.get("max_exploration_bonus")),
        "curvature_penalty": clamp(regret_plan.get("curvature_penalty")),
        "resolved_evidence_weight": clamp(
            regret_plan.get("resolved_evidence_weight")
        ),
        "max_portfolio_adjustment": clamp(
            regret_plan.get("max_portfolio_adjustment")
        ),
        "shadow_model_weight": clamp(regret_plan.get("shadow_model_weight")),
        "shadow_learning_rate": clamp(regret_plan.get("shadow_learning_rate")),
        "reliability_prior_mass": nonnegative(
            regret_plan.get("reliability_prior_mass"), 2.0
        ),
        "default_prediction_confidence": clamp(
            regret_plan.get("default_prediction_confidence")
        ),
        "shadow_action_utility": dict(
            mapping(regret_plan.get("shadow_action_utility"))
        ),
        "uncertainty_weight": clamp(regret_plan.get("uncertainty_weight")),
        "unresolved_shadow_weight": clamp(
            regret_plan.get("unresolved_shadow_weight")
        ),
        "trial_novelty_weight": clamp(regret_plan.get("trial_novelty_weight")),
        "opportunity_cost_weight": clamp(
            regret_plan.get("opportunity_cost_weight")
        ),
        "base_minimum_information_gain": clamp(
            regret_plan.get("base_minimum_information_gain")
        ),
        "hard_minimum_information_gain": clamp(
            regret_plan.get("hard_minimum_information_gain")
        ),
        "information_gain_threshold_adaptation_rate": clamp(
            regret_plan.get("information_gain_threshold_adaptation_rate")
        ),
        "maximum_trial_risk": clamp(regret_plan.get("maximum_trial_risk")),
        "minimum_trial_recoverability": clamp(
            regret_plan.get("minimum_trial_recoverability")
        ),
        "total_trial_budget": nonnegative(regret_plan.get("total_trial_budget")),
        "maximum_trial_cost": nonnegative(regret_plan.get("maximum_trial_cost")),
        "default_trial_cost": nonnegative(regret_plan.get("default_trial_cost")),
        "default_trial_risk": clamp(regret_plan.get("default_trial_risk")),
        "default_trial_recoverability": clamp(
            regret_plan.get("default_trial_recoverability"), 1.0
        ),
        "max_live_trials_total": integer(
            regret_plan.get("max_live_trials_total"), 0
        ),
        "max_live_trials_per_adapter_context": integer(
            regret_plan.get("max_live_trials_per_adapter_context"), 0
        ),
        "base_trial_cooldown_cycles": integer(
            regret_plan.get("base_trial_cooldown_cycles"), 0
        ),
        "hard_minimum_trial_cooldown_cycles": integer(
            regret_plan.get("hard_minimum_trial_cooldown_cycles"), 0
        ),
        "maximum_cooldown_reduction_cycles": integer(
            regret_plan.get("maximum_cooldown_reduction_cycles"), 0
        ),
        "policy_information_gain_weight": clamp(
            regret_plan.get("policy_information_gain_weight")
        ),
        "policy_posterior_weight": clamp(
            regret_plan.get("policy_posterior_weight")
        ),
        "policy_net_value_weight": clamp(
            regret_plan.get("policy_net_value_weight")
        ),
        "policy_pending_weight": clamp(regret_plan.get("policy_pending_weight")),
        "policy_recoverability_weight": clamp(
            regret_plan.get("policy_recoverability_weight")
        ),
        "policy_cost_penalty_weight": clamp(
            regret_plan.get("policy_cost_penalty_weight")
        ),
        "policy_risk_penalty_weight": clamp(
            regret_plan.get("policy_risk_penalty_weight")
        ),
        "prior_experiment_value": clamp(regret_plan.get("prior_experiment_value")),
        "posterior_confidence_mass": nonnegative(
            regret_plan.get("posterior_confidence_mass"), 6.0
        ),
        "experiment_pressure_threshold": clamp(
            regret_decision.get("adapted_experiment_pressure_threshold")
        ),
        "minimum_policy_cycles_between_experiments": integer(
            regret_decision.get("adapted_experiment_interval"), 0
        ),
        "reobserve_pending_weight": clamp(
            regret_plan.get("reobserve_pending_weight")
        ),
        "reobserve_resolution_debt_weight": clamp(
            regret_plan.get("reobserve_resolution_debt_weight")
        ),
        "reobserve_low_confidence_weight": clamp(
            regret_plan.get("reobserve_low_confidence_weight")
        ),
        "post_experiment_reobserve_bonus": clamp(
            regret_plan.get("post_experiment_reobserve_bonus")
        ),
        "reobserve_pressure_threshold": clamp(
            regret_decision.get("adapted_reobserve_pressure_threshold")
        ),
        "minimum_policy_cycles_between_reobservations": integer(
            regret_decision.get("adapted_reobserve_interval"), 0
        ),
        "outcome_cost_weight": clamp(regret_plan.get("outcome_cost_weight")),
        "outcome_risk_weight": clamp(regret_plan.get("outcome_risk_weight")),
        "outcome_recoverability_weight": clamp(
            regret_plan.get("outcome_recoverability_weight")
        ),
        "experiment_success_net_value_floor": signed(
            regret_plan.get("experiment_success_net_value_floor"), 0.0
        ),
        "max_shadow_candidates": integer(
            regret_plan.get("max_shadow_candidates"), 8
        ),
        "max_pending_predictions": integer(
            regret_plan.get("max_pending_predictions"), 256
        ),
        "max_resolved_predictions": integer(
            regret_plan.get("max_resolved_predictions"), 256
        ),
        "max_portfolio_holonomy": integer(
            regret_plan.get("max_portfolio_holonomy"), 256
        ),
        "max_trial_records": integer(regret_plan.get("max_trial_records"), 256),
        "max_decision_holonomy": integer(
            regret_plan.get("max_decision_holonomy"), 256
        ),
        "max_policy_outcomes": integer(
            regret_plan.get("max_policy_outcomes"), 256
        ),
        "max_policy_holonomy": integer(
            regret_plan.get("max_policy_holonomy"), 256
        ),
        "max_sources_per_cycle": integer(
            regret_plan.get("max_sources_per_cycle"), 8
        ),
        "max_signals_per_source": integer(
            regret_plan.get("max_signals_per_source"), 8
        ),
        "max_total_signals": integer(regret_plan.get("max_total_signals"), 32),
        "max_generated_goals": integer(
            regret_plan.get("max_generated_goals"), 8
        ),
        "max_selected_goals": integer(
            regret_plan.get("max_selected_goals"), 4
        ),
        "min_goal_score": clamp(regret_plan.get("min_goal_score")),
        "min_action_scale": clamp(regret_plan.get("min_action_scale")),
        "renewal_window_steps": integer(
            regret_plan.get("renewal_window_steps"), 3
        ),
        "max_bundle_sections": integer(
            regret_plan.get("max_bundle_sections"), 256
        ),
        "max_new_sections_per_run": integer(
            regret_plan.get("max_new_sections_per_run"), 8
        ),
        "max_transports_per_section": integer(
            regret_plan.get("max_transports_per_section"), 4
        ),
        "boundary": dict(POLICY_REQUIRED_BOUNDARY),
    }
    packet["policy_plan_digest"] = policy_plan_digest(packet)
    return packet


def build_child_policy_license(
    *,
    child_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    adapter_registry: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    previous_experiment_bundle: Mapping[str, Any],
    previous_policy_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": POLICY_LICENSE_VERSION,
        "bound_policy_plan_digest": child_plan.get("policy_plan_digest", ""),
        "bound_source_batch_digest": batch_digest(source_packets),
        "bound_root_principles_digest": root_packet.get(
            "root_principles_digest", ""
        ),
        "bound_adapter_registry_digest": adapter_registry.get(
            "adapter_registry_digest", ""
        ),
        "bound_previous_capability_bundle_digest": previous_capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "bound_source_portfolio_bundle_digest": source_portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
        "bound_previous_experiment_bundle_digest": previous_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "bound_previous_policy_bundle_digest": previous_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "multiple_child_cycles_allowed": False,
        "v0_8_hard_gate_bypass_allowed": False,
        "unbudgeted_trial_allowed": False,
        "shadow_execution_allowed": False,
        "external_network_effect_allowed": False,
        "world_update_allowed": False,
        "memory_overwrite_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "capability_read_allowed",
        "portfolio_read_allowed",
        "experiment_read_allowed",
        "policy_read_allowed",
        "preview_allowed",
        "policy_decision_allowed",
        "one_child_experiment_cycle_allowed",
        "reobserve_routing_allowed",
        "policy_update_allowed",
        "policy_bundle_write_allowed",
        "policy_state_write_allowed",
        "decision_write_allowed",
        "outcome_write_allowed",
        "child_packet_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet
