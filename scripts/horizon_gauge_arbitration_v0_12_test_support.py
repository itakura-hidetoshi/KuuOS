from __future__ import annotations

from runtime.kuuos_active_gauge_intervention_types_v0_3 import LOCAL_ACTIONS
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_horizon_gauge_arbitration_basis_v0_12 import empty_bundle
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
)
from scripts.delayed_credit_multihorizon_v0_11_test_support import (
    experiment_registry,
    initial_experiment,
    initial_horizon,
    initial_policy,
    initial_regret,
    plan as horizon_template_plan,
    root_packet,
    source,
)


def arbitration_context(runtime_root):
    return {
        "runtime_root": str(runtime_root),
        "horizon_gauge_arbitration_enabled": True,
        "execute_one_arbitration_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def initial_arbitration(agent_id="agent"):
    return empty_bundle(agent_id)


def plan(run_id, sources, root, registry, current):
    base = horizon_template_plan(
        run_id + ":template",
        sources,
        root,
        registry,
        current["capability_state"].get("capability_state_digest", ""),
        current["capability_bundle"]["capability_bundle_digest"],
        current["source_portfolio_bundle"]["portfolio_bundle_digest"],
        current["experiment_state"].get("experiment_state_digest", ""),
        current["experiment_bundle"]["experiment_bundle_digest"],
        current["policy_state"].get("policy_state_digest", ""),
        current["policy_bundle"]["policy_bundle_digest"],
        current["regret_state"].get("regret_state_digest", ""),
        current["regret_bundle"]["regret_bundle_digest"],
        current["horizon_state"].get("horizon_state_digest", ""),
        current["horizon_bundle"]["horizon_bundle_digest"],
        current["gauge_state"].get("gauge_state_digest", ""),
        current["gauge_bundle"].get("gauge_bundle_digest", ""),
    )
    for field in (
        "version",
        "horizon_run_id",
        "horizon_plan_digest",
        "boundary",
    ):
        base.pop(field, None)
    packet = {
        **base,
        "version": PLAN_VERSION,
        "arbitration_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": registry["adapter_registry_digest"],
        "expected_capability_state_digest": current["capability_state"].get("capability_state_digest", ""),
        "expected_capability_bundle_digest": current["capability_bundle"]["capability_bundle_digest"],
        "expected_source_portfolio_bundle_digest": current["source_portfolio_bundle"]["portfolio_bundle_digest"],
        "expected_experiment_state_digest": current["experiment_state"].get("experiment_state_digest", ""),
        "expected_experiment_bundle_digest": current["experiment_bundle"]["experiment_bundle_digest"],
        "expected_policy_state_digest": current["policy_state"].get("policy_state_digest", ""),
        "expected_policy_bundle_digest": current["policy_bundle"]["policy_bundle_digest"],
        "expected_regret_state_digest": current["regret_state"].get("regret_state_digest", ""),
        "expected_regret_bundle_digest": current["regret_bundle"]["regret_bundle_digest"],
        "expected_horizon_state_digest": current["horizon_state"].get("horizon_state_digest", ""),
        "expected_horizon_bundle_digest": current["horizon_bundle"]["horizon_bundle_digest"],
        "expected_gauge_state_digest": current["gauge_state"].get("gauge_state_digest", ""),
        "expected_gauge_bundle_digest": current["gauge_bundle"].get("gauge_bundle_digest", ""),
        "expected_previous_arbitration_state_digest": current["arbitration_state"].get("arbitration_state_digest", ""),
        "expected_previous_arbitration_bundle_digest": current["arbitration_bundle"]["arbitration_bundle_digest"],
        "base_short_horizon_weight": 0.5,
        "base_medium_horizon_weight": 0.3,
        "base_long_horizon_weight": 0.2,
        "minimum_horizon_weight": 0.12,
        "parallel_transport_gain": 0.08,
        "curvature_temperature_gain": 0.6,
        "short_curvature_response_gain": 0.25,
        "medium_progress_response_gain": 0.35,
        "medium_recovery_response_gain": 0.35,
        "long_terminal_response_gain": 0.35,
        "long_holonomy_response_gain": 0.25,
        "outcome_memory_gain": 0.08,
        "arbitration_holonomy_scale": 8.0,
        "plural_conflict_curvature_threshold": 0.05,
        "repair_outcome_threshold": 0.25,
        "progressing_outcome_threshold": 0.25,
        "stabilizing_terminal_threshold": 0.5,
        "max_arbitration_outcomes": 256,
        "max_arbitration_holonomy": 256,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["arbitration_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, sources, root, registry, current):
    packet = {
        "version": LICENSE_VERSION,
        "bound_arbitration_plan_digest": plan_packet["arbitration_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": registry["adapter_registry_digest"],
        "bound_previous_horizon_bundle_digest": current["horizon_bundle"]["horizon_bundle_digest"],
        "bound_previous_arbitration_bundle_digest": current["arbitration_bundle"]["arbitration_bundle_digest"],
        "multiple_child_horizon_cycles_allowed": False,
        "winner_take_all_collapse_allowed": False,
        "effectless_outcome_allowed": False,
        "v0_11_authority_bypass_allowed": False,
        "v0_8_hard_gate_bypass_allowed": False,
        "shadow_execution_allowed": False,
        "external_network_effect_allowed": False,
        "world_update_allowed": False,
        "memory_overwrite_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "upstream_state_read_allowed",
        "gauge_arbitration_allowed",
        "parallel_transport_allowed",
        "one_child_horizon_cycle_allowed",
        "arbitration_bundle_write_allowed",
        "arbitration_state_write_allowed",
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
    "arbitration_context",
    "initial_arbitration",
    "initial_experiment",
    "initial_horizon",
    "initial_policy",
    "initial_regret",
    "plan",
    "license_packet",
    "experiment_registry",
    "root_packet",
    "source",
]
