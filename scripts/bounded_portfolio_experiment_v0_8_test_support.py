from __future__ import annotations

from runtime.kuuos_active_gauge_intervention_types_v0_3 import LOCAL_ACTIONS
from runtime.kuuos_adapter_portfolio_shadow_model_v0_7 import empty_bundle as empty_portfolio_bundle
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import empty_bundle
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    REGISTRY_VERSION,
    batch_digest,
    registry_digest,
)
from scripts.adapter_capability_v0_6_test_support import (
    full_routing,
    profile,
    root_packet,
    source,
)


def experiment_registry():
    profile_a = profile("experiment-adapter-a-profile")
    profile_b = profile("experiment-adapter-b-profile")
    packet = {
        "version": REGISTRY_VERSION,
        "registry_id": "bounded-experiment-registry-v08",
        "adapters": [
            {
                "federation_adapter_id": "adapter-a",
                "enabled": True,
                "priority": 100,
                "accepted_source_kinds": ["observation", "resource_change"],
                "accepted_source_ids": [],
                "external_network_effect_allowed": False,
                "capability_prior": 0.82,
                "capability_routing_table": full_routing("advance_tick"),
                "experiment_cost": 0.2,
                "experiment_risk_prior": 0.04,
                "experiment_recoverability_prior": 0.99,
                "adapter_profile": profile_a,
            },
            {
                "federation_adapter_id": "adapter-b",
                "enabled": True,
                "priority": 1,
                "accepted_source_kinds": ["observation", "resource_change"],
                "accepted_source_ids": [],
                "external_network_effect_allowed": False,
                "capability_prior": 0.42,
                "capability_routing_table": full_routing("advance_tick"),
                "experiment_cost": 0.2,
                "experiment_risk_prior": 0.05,
                "experiment_recoverability_prior": 0.98,
                "adapter_profile": profile_b,
            },
        ],
    }
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def experiment_context(runtime_root):
    return {
        "runtime_root": str(runtime_root),
        "bounded_portfolio_experiment_enabled": True,
        "execute_one_experiment_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def initial_portfolio_digest(agent_id="agent"):
    return empty_portfolio_bundle(agent_id)["portfolio_bundle_digest"]


def initial_experiment_bundle(source_portfolio_bundle, agent_id="agent"):
    return empty_bundle(agent_id, source_portfolio_bundle)


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
):
    packet = {
        "version": PLAN_VERSION,
        "experiment_run_id": run_id,
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
        "minimum_information_gain": 0.5,
        "maximum_trial_risk": 0.15,
        "minimum_trial_recoverability": 0.9,
        "total_trial_budget": 1.0,
        "maximum_trial_cost": 0.25,
        "default_trial_cost": 0.2,
        "default_trial_risk": 0.1,
        "default_trial_recoverability": 0.95,
        "max_live_trials_total": 1,
        "max_live_trials_per_adapter_context": 1,
        "trial_cooldown_cycles": 2,
        "max_shadow_candidates": 8,
        "max_pending_predictions": 256,
        "max_resolved_predictions": 256,
        "max_portfolio_holonomy": 256,
        "max_trial_records": 256,
        "max_decision_holonomy": 256,
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
    packet["experiment_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(
    plan_packet,
    sources,
    root,
    adapter_registry,
    previous_capability_bundle_digest,
    source_portfolio_bundle_digest,
    previous_experiment_bundle_digest,
):
    packet = {
        "version": LICENSE_VERSION,
        "bound_experiment_plan_digest": plan_packet["experiment_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "bound_previous_capability_bundle_digest": previous_capability_bundle_digest,
        "bound_source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "bound_previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "multiple_live_adapters_allowed": False,
        "unbudgeted_trial_allowed": False,
        "shadow_execution_allowed": False,
        "shadow_external_actuation_allowed": False,
        "shadow_world_update_allowed": False,
        "shadow_capability_connection_update_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
        "external_network_effect_allowed": False,
        "world_update_allowed": False,
        "memory_overwrite_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "capability_state_read_allowed",
        "capability_bundle_read_allowed",
        "portfolio_seed_read_allowed",
        "experiment_bundle_read_allowed",
        "information_gain_estimation_allowed",
        "experiment_decision_allowed",
        "licensed_live_trial_allowed",
        "baseline_exploitation_allowed",
        "one_live_capability_cycle_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "trial_budget_debit_allowed",
        "experiment_bundle_write_allowed",
        "experiment_state_write_allowed",
        "decision_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "trial_record_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet


__all__ = [
    "experiment_registry",
    "experiment_context",
    "initial_portfolio_digest",
    "initial_experiment_bundle",
    "plan",
    "license_packet",
    "root_packet",
    "source",
]
