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
from runtime.kuuos_delayed_credit_multihorizon_model_v0_11 import (
    empty_bundle as empty_horizon_bundle,
)
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
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
from scripts.policy_regret_cadence_v0_10_test_support import plan as regret_template_plan


def horizon_context(runtime_root):
    return {
        "runtime_root": str(runtime_root),
        "delayed_credit_multihorizon_enabled": True,
        "execute_one_horizon_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def initial_experiment(source_portfolio_bundle, agent_id="agent"):
    return empty_experiment_bundle(agent_id, source_portfolio_bundle)


def initial_policy(agent_id="agent"):
    return empty_policy_bundle(agent_id)


def initial_regret(agent_id="agent"):
    return empty_regret_bundle(agent_id)


def initial_horizon(agent_id="agent"):
    return empty_horizon_bundle(agent_id)


def plan(
    run_id,
    sources,
    root,
    adapter_registry,
    capability_state_digest,
    capability_bundle_digest,
    source_portfolio_bundle_digest,
    experiment_state_digest,
    experiment_bundle_digest,
    policy_state_digest,
    policy_bundle_digest,
    previous_regret_state_digest,
    previous_regret_bundle_digest,
    previous_horizon_state_digest,
    previous_horizon_bundle_digest,
    gauge_state_digest,
    gauge_bundle_digest,
):
    base = regret_template_plan(
        run_id + ":template",
        sources,
        root,
        adapter_registry,
        capability_state_digest,
        capability_bundle_digest,
        source_portfolio_bundle_digest,
        experiment_state_digest,
        experiment_bundle_digest,
        policy_state_digest,
        policy_bundle_digest,
        previous_regret_state_digest,
        previous_regret_bundle_digest,
    )
    for field in (
        "version",
        "regret_run_id",
        "regret_plan_digest",
        "boundary",
        "expected_previous_capability_state_digest",
        "expected_previous_capability_bundle_digest",
        "expected_source_portfolio_bundle_digest",
        "expected_previous_experiment_state_digest",
        "expected_previous_experiment_bundle_digest",
        "expected_previous_policy_state_digest",
        "expected_previous_policy_bundle_digest",
        "expected_previous_regret_state_digest",
        "expected_previous_regret_bundle_digest",
    ):
        base.pop(field, None)
    packet = {
        **base,
        "version": PLAN_VERSION,
        "horizon_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "expected_capability_state_digest": capability_state_digest,
        "expected_capability_bundle_digest": capability_bundle_digest,
        "expected_source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "expected_experiment_state_digest": experiment_state_digest,
        "expected_experiment_bundle_digest": experiment_bundle_digest,
        "expected_policy_state_digest": policy_state_digest,
        "expected_policy_bundle_digest": policy_bundle_digest,
        "expected_previous_regret_state_digest": previous_regret_state_digest,
        "expected_previous_regret_bundle_digest": previous_regret_bundle_digest,
        "expected_previous_horizon_state_digest": previous_horizon_state_digest,
        "expected_previous_horizon_bundle_digest": previous_horizon_bundle_digest,
        "expected_gauge_state_digest": gauge_state_digest,
        "expected_gauge_bundle_digest": gauge_bundle_digest,
        "short_horizon_weight": 0.5,
        "medium_horizon_weight": 0.3,
        "long_horizon_weight": 0.2,
        "horizon_threshold_gain": 0.06,
        "horizon_exploit_resistance_gain": 0.08,
        "horizon_interval_gain_cycles": 1,
        "horizon_exploit_interval_gain_cycles": 2,
        "short_credit_decay": 0.55,
        "medium_credit_decay": 0.82,
        "long_credit_decay": 0.95,
        "short_value_learning_rate": 0.5,
        "short_regret_learning_rate": 0.6,
        "medium_progress_learning_rate": 0.5,
        "medium_recovery_learning_rate": 0.45,
        "medium_delayed_learning_rate": 0.4,
        "long_progress_learning_rate": 0.35,
        "long_terminal_learning_rate": 0.4,
        "long_recovery_learning_rate": 0.25,
        "long_delayed_learning_rate": 0.3,
        "long_horizon_activation_cycles": 2,
        "delayed_evidence_scale": 4.0,
        "long_holonomy_scale": 8.0,
        "progress_delta_weight": 0.35,
        "observed_benefit_weight": 0.25,
        "terminal_ratio_weight": 0.2,
        "effect_confidence_weight": 0.2,
        "observed_harm_weight": 0.35,
        "recoverability_deficit_weight": 0.25,
        "curvature_cost_weight": 0.25,
        "repair_continuation_cost": 0.15,
        "max_horizon_outcomes": 256,
        "max_horizon_holonomy": 256,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["horizon_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(
    plan_packet,
    sources,
    root,
    adapter_registry,
    previous_regret_bundle_digest,
    previous_horizon_bundle_digest,
):
    packet = {
        "version": LICENSE_VERSION,
        "bound_horizon_plan_digest": plan_packet["horizon_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "bound_previous_regret_bundle_digest": previous_regret_bundle_digest,
        "bound_previous_horizon_bundle_digest": previous_horizon_bundle_digest,
        "multiple_child_regret_cycles_allowed": False,
        "effectless_credit_update_allowed": False,
        "counterfactual_outcome_promotion_allowed": False,
        "v0_10_authority_bypass_allowed": False,
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
        "gauge_evidence_read_allowed",
        "horizon_credit_update_allowed",
        "cadence_adaptation_allowed",
        "one_child_regret_cycle_allowed",
        "horizon_bundle_write_allowed",
        "horizon_state_write_allowed",
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
    "horizon_context",
    "initial_experiment",
    "initial_policy",
    "initial_regret",
    "initial_horizon",
    "plan",
    "license_packet",
    "experiment_registry",
    "root_packet",
    "source",
]
