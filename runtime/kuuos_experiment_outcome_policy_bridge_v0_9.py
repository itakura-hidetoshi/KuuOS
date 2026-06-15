#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    LICENSE_VERSION as EXPERIMENT_LICENSE_VERSION,
    PLAN_VERSION as EXPERIMENT_PLAN_VERSION,
    REQUIRED_BOUNDARY as EXPERIMENT_REQUIRED_BOUNDARY,
    plan_digest as experiment_plan_digest,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    batch_digest,
    registry_digest,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    as_list,
    clamp,
    integer,
    mapping,
    nonnegative,
)


def derive_policy_registry(
    registry: Mapping[str, Any], policy_mode: str
) -> dict[str, Any]:
    packet = dict(registry)
    packet.pop("adapter_registry_digest", None)
    adapters: list[dict[str, Any]] = []
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        if policy_mode == "reobserve":
            routing = {
                str(key): "observe"
                for key in mapping(entry.get("capability_routing_table")).keys()
            }
            entry["capability_routing_table"] = routing
            entry["policy_reobserve_routing"] = True
        else:
            entry["policy_reobserve_routing"] = False
        adapters.append(entry)
    packet["adapters"] = adapters
    packet["policy_mode"] = policy_mode
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def build_experiment_plan(
    *,
    policy_plan: Mapping[str, Any],
    policy_decision: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    child_registry: Mapping[str, Any],
    previous_capability_state: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    previous_experiment_state: Mapping[str, Any],
    previous_experiment_bundle: Mapping[str, Any],
    preview: bool = False,
) -> dict[str, Any]:
    policy_mode = "preview" if preview else str(policy_decision.get("policy_mode", ""))
    current_trials = integer(previous_experiment_bundle.get("total_trial_count"), 0)
    if preview or policy_mode == "experiment":
        max_trials = integer(policy_plan.get("max_live_trials_total"), current_trials)
        minimum_information_gain = (
            clamp(policy_plan.get("base_minimum_information_gain"))
            if preview
            else clamp(policy_decision.get("adapted_minimum_information_gain"))
        )
        cooldown = (
            integer(policy_plan.get("base_trial_cooldown_cycles"), 0)
            if preview
            else integer(policy_decision.get("adapted_trial_cooldown_cycles"), 0)
        )
    else:
        max_trials = current_trials
        minimum_information_gain = 1.0
        cooldown = integer(policy_plan.get("base_trial_cooldown_cycles"), 0)
    run_suffix = ":preview" if preview else ":experiment"
    packet = {
        "version": EXPERIMENT_PLAN_VERSION,
        "experiment_run_id": str(policy_plan.get("policy_run_id", "")) + run_suffix,
        "agent_id": str(policy_plan.get("agent_id", "")),
        "expected_source_batch_digest": batch_digest(source_packets),
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": child_registry.get(
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
        "learning_rate": clamp(policy_plan.get("learning_rate")),
        "exploration_weight": clamp(policy_plan.get("exploration_weight")),
        "max_exploration_bonus": clamp(policy_plan.get("max_exploration_bonus")),
        "curvature_penalty": clamp(policy_plan.get("curvature_penalty")),
        "resolved_evidence_weight": clamp(
            policy_plan.get("resolved_evidence_weight")
        ),
        "max_portfolio_adjustment": clamp(
            policy_plan.get("max_portfolio_adjustment")
        ),
        "shadow_model_weight": clamp(policy_plan.get("shadow_model_weight")),
        "shadow_learning_rate": clamp(policy_plan.get("shadow_learning_rate")),
        "reliability_prior_mass": nonnegative(
            policy_plan.get("reliability_prior_mass"), 2.0
        ),
        "default_prediction_confidence": clamp(
            policy_plan.get("default_prediction_confidence")
        ),
        "shadow_action_utility": dict(mapping(policy_plan.get("shadow_action_utility"))),
        "uncertainty_weight": clamp(policy_plan.get("uncertainty_weight")),
        "unresolved_shadow_weight": clamp(
            policy_plan.get("unresolved_shadow_weight")
        ),
        "trial_novelty_weight": clamp(policy_plan.get("trial_novelty_weight")),
        "opportunity_cost_weight": clamp(
            policy_plan.get("opportunity_cost_weight")
        ),
        "minimum_information_gain": minimum_information_gain,
        "maximum_trial_risk": clamp(policy_plan.get("maximum_trial_risk")),
        "minimum_trial_recoverability": clamp(
            policy_plan.get("minimum_trial_recoverability")
        ),
        "total_trial_budget": nonnegative(policy_plan.get("total_trial_budget")),
        "maximum_trial_cost": nonnegative(policy_plan.get("maximum_trial_cost")),
        "default_trial_cost": nonnegative(policy_plan.get("default_trial_cost")),
        "default_trial_risk": clamp(policy_plan.get("default_trial_risk")),
        "default_trial_recoverability": clamp(
            policy_plan.get("default_trial_recoverability"), 1.0
        ),
        "max_live_trials_total": max_trials,
        "max_live_trials_per_adapter_context": integer(
            policy_plan.get("max_live_trials_per_adapter_context"), 0
        ),
        "trial_cooldown_cycles": cooldown,
        "max_shadow_candidates": integer(policy_plan.get("max_shadow_candidates"), 1),
        "max_pending_predictions": integer(
            policy_plan.get("max_pending_predictions"), 256
        ),
        "max_resolved_predictions": integer(
            policy_plan.get("max_resolved_predictions"), 256
        ),
        "max_portfolio_holonomy": integer(
            policy_plan.get("max_portfolio_holonomy"), 256
        ),
        "max_trial_records": integer(policy_plan.get("max_trial_records"), 256),
        "max_decision_holonomy": integer(
            policy_plan.get("max_decision_holonomy"), 256
        ),
        "max_sources_per_cycle": integer(
            policy_plan.get("max_sources_per_cycle"), 8
        ),
        "max_signals_per_source": integer(
            policy_plan.get("max_signals_per_source"), 8
        ),
        "max_total_signals": integer(policy_plan.get("max_total_signals"), 32),
        "max_generated_goals": integer(policy_plan.get("max_generated_goals"), 8),
        "max_selected_goals": integer(policy_plan.get("max_selected_goals"), 4),
        "min_goal_score": clamp(policy_plan.get("min_goal_score")),
        "min_action_scale": clamp(policy_plan.get("min_action_scale")),
        "renewal_window_steps": integer(
            policy_plan.get("renewal_window_steps"), 3
        ),
        "max_bundle_sections": integer(
            policy_plan.get("max_bundle_sections"), 256
        ),
        "max_new_sections_per_run": integer(
            policy_plan.get("max_new_sections_per_run"), 8
        ),
        "max_transports_per_section": integer(
            policy_plan.get("max_transports_per_section"), 4
        ),
        "boundary": dict(EXPERIMENT_REQUIRED_BOUNDARY),
    }
    packet["experiment_plan_digest"] = experiment_plan_digest(packet)
    return packet


def build_experiment_license(
    *,
    child_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    child_registry: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    previous_experiment_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    packet = {
        "version": EXPERIMENT_LICENSE_VERSION,
        "bound_experiment_plan_digest": child_plan.get(
            "experiment_plan_digest", ""
        ),
        "bound_source_batch_digest": batch_digest(source_packets),
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": child_registry.get(
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
