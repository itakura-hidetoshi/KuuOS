from __future__ import annotations

from runtime.kuuos_active_gauge_intervention_types_v0_3 import LOCAL_ACTIONS
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import (
    empty_bundle as empty_experiment_bundle,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_experiment_outcome_policy_model_v0_9 import (
    empty_bundle as empty_policy_bundle,
)
from runtime.kuuos_policy_regret_cadence_model_v0_10 import (
    empty_bundle as empty_regret_bundle,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
)
from scripts.bounded_portfolio_experiment_v0_8_test_support import (
    experiment_registry,
    root_packet,
    source,
)


def regret_context(runtime_root):
    return {
        "runtime_root": str(runtime_root),
        "policy_regret_cadence_enabled": True,
        "execute_one_regret_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def initial_experiment(source_portfolio_bundle, agent_id="agent"):
    return empty_experiment_bundle(agent_id, source_portfolio_bundle)


def initial_policy(agent_id="agent"):
    return empty_policy_bundle(agent_id)


def initial_regret(agent_id="agent"):
    return empty_regret_bundle(agent_id)


def plan(
    run_id,
    sources,
    root,
    adapter_registry,
    previous_capability_state_digest,
    previous_capability_bundle_digest,
    source_portfolio_bundle_digest,
    previous_experiment_state_digest,
    previous_experiment_bundle_digest,
    previous_policy_state_digest,
    previous_policy_bundle_digest,
    previous_regret_state_digest,
    previous_regret_bundle_digest,
):
    packet = {
        "version": PLAN_VERSION,
        "regret_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "expected_previous_capability_state_digest": previous_capability_state_digest,
        "expected_previous_capability_bundle_digest": previous_capability_bundle_digest,
        "expected_source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "expected_previous_experiment_state_digest": previous_experiment_state_digest,
        "expected_previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "expected_previous_policy_state_digest": previous_policy_state_digest,
        "expected_previous_policy_bundle_digest": previous_policy_bundle_digest,
        "expected_previous_regret_state_digest": previous_regret_state_digest,
        "expected_previous_regret_bundle_digest": previous_regret_bundle_digest,
        "learning_rate": 0.7,
        "exploration_weight": 0.18,
        "max_exploration_bonus": 0.18,
        "curvature_penalty": 0.2,
        "resolved_evidence_weight": 0.5,
        "max_portfolio_adjustment": 0.08,
        "shadow_model_weight": 0.55,
        "shadow_learning_rate": 0.7,
        "reliability_prior_mass": 2.0,
        "default_prediction_confidence": 0.8,
        "shadow_action_utility": {
            "advance_tick": 0.85,
            "notify": 0.62,
            "ticket": 0.6,
            "handover": 0.58,
            "observe": 0.48,
            "hold": 0.12,
            "freeze": 0.08,
        },
        "uncertainty_weight": 0.45,
        "unresolved_shadow_weight": 0.35,
        "trial_novelty_weight": 0.25,
        "opportunity_cost_weight": 0.1,
        "base_minimum_information_gain": 0.5,
        "hard_minimum_information_gain": 0.35,
        "information_gain_threshold_adaptation_rate": 0.2,
        "maximum_trial_risk": 0.15,
        "minimum_trial_recoverability": 0.9,
        "total_trial_budget": 1.0,
        "maximum_trial_cost": 0.25,
        "default_trial_cost": 0.2,
        "default_trial_risk": 0.1,
        "default_trial_recoverability": 0.95,
        "max_live_trials_total": 4,
        "max_live_trials_per_adapter_context": 2,
        "base_trial_cooldown_cycles": 2,
        "hard_minimum_trial_cooldown_cycles": 1,
        "maximum_cooldown_reduction_cycles": 1,
        "policy_information_gain_weight": 0.35,
        "policy_posterior_weight": 0.15,
        "policy_net_value_weight": 0.1,
        "policy_pending_weight": 0.2,
        "policy_recoverability_weight": 0.1,
        "policy_cost_penalty_weight": 0.05,
        "policy_risk_penalty_weight": 0.05,
        "prior_experiment_value": 0.6,
        "posterior_confidence_mass": 6.0,
        "base_experiment_pressure_threshold": 0.6,
        "minimum_experiment_pressure_threshold": 0.4,
        "maximum_experiment_pressure_threshold": 0.9,
        "base_policy_cycles_between_experiments": 3,
        "minimum_policy_cycles_between_experiments": 1,
        "maximum_policy_cycles_between_experiments": 8,
        "reobserve_pending_weight": 0.25,
        "reobserve_resolution_debt_weight": 0.2,
        "reobserve_low_confidence_weight": 0.2,
        "post_experiment_reobserve_bonus": 0.4,
        "base_reobserve_pressure_threshold": 0.65,
        "minimum_reobserve_pressure_threshold": 0.45,
        "maximum_reobserve_pressure_threshold": 0.95,
        "base_policy_cycles_between_reobservations": 3,
        "minimum_policy_cycles_between_reobservations": 1,
        "maximum_policy_cycles_between_reobservations": 8,
        "outcome_cost_weight": 0.2,
        "outcome_risk_weight": 0.2,
        "outcome_recoverability_weight": 0.1,
        "experiment_success_net_value_floor": 0.35,
        "regret_threshold_gain": 0.5,
        "exploit_resistance_gain": 0.5,
        "regret_interval_gain_cycles": 4,
        "exploit_interval_gain_cycles": 6,
        "minimum_counterfactual_confidence": 0.2,
        "regret_tolerance": 0.1,
        "maximum_regret_per_cycle": 0.5,
        "regret_credit_decay": 0.9,
        "regret_credit_learning_rate": 0.9,
        "chosen_mode_credit_penalty": 0.25,
        "counterfactual_credibility_mass": 2.0,
        "prior_mode_confidence": 0.6,
        "pending_shadow_discount": 0.2,
        "delayed_compatible_weight": 1.0,
        "prior_experiment_counterfactual_value": 0.6,
        "prior_reobserve_counterfactual_value": 0.45,
        "prior_exploit_counterfactual_value": 0.85,
        "max_shadow_candidates": 8,
        "max_pending_predictions": 256,
        "max_resolved_predictions": 256,
        "max_portfolio_holonomy": 256,
        "max_trial_records": 256,
        "max_decision_holonomy": 256,
        "max_policy_outcomes": 256,
        "max_policy_holonomy": 256,
        "max_regret_outcomes": 256,
        "max_regret_holonomy": 256,
        "max_sources_per_cycle": 8,
        "max_signals_per_source": 8,
        "max_total_signals": 32,
        "max_generated_goals": 8,
        "max_selected_goals": 4,
        "min_goal_score": 0.35,
        "min_action_scale": 0.12,
        "renewal_window_steps": 3,
        "max_bundle_sections": 256,
        "max_new_sections_per_run": 8,
        "max_transports_per_section": 4,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["regret_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(
    plan_packet,
    sources,
    root,
    adapter_registry,
    previous_capability_bundle_digest,
    source_portfolio_bundle_digest,
    previous_experiment_bundle_digest,
    previous_policy_bundle_digest,
    previous_regret_bundle_digest,
):
    packet = {
        "version": LICENSE_VERSION,
        "bound_regret_plan_digest": plan_packet["regret_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "bound_previous_capability_bundle_digest": previous_capability_bundle_digest,
        "bound_source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "bound_previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "bound_previous_policy_bundle_digest": previous_policy_bundle_digest,
        "bound_previous_regret_bundle_digest": previous_regret_bundle_digest,
        "multiple_child_policy_cycles_allowed": False,
        "counterfactual_truth_promotion_allowed": False,
        "unexecuted_alternative_outcome_allowed": False,
        "v0_9_authority_bypass_allowed": False,
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
        "upstream_state_read_allowed",
        "counterfactual_estimation_allowed",
        "regret_update_allowed",
        "cadence_adaptation_allowed",
        "one_child_policy_cycle_allowed",
        "regret_bundle_write_allowed",
        "regret_state_write_allowed",
        "decision_write_allowed",
        "outcome_write_allowed",
        "child_packet_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet


__all__ = [
    "regret_context",
    "initial_experiment",
    "initial_policy",
    "initial_regret",
    "plan",
    "license_packet",
    "experiment_registry",
    "root_packet",
    "source",
]
