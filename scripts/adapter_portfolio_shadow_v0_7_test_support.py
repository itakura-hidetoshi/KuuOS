from __future__ import annotations

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import (
    empty_bundle as empty_capability_bundle,
)
from runtime.kuuos_adapter_portfolio_shadow_model_v0_7 import empty_bundle
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
)
from scripts.adapter_capability_v0_6_test_support import (
    context as capability_context,
    registry,
    root_packet,
    source,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest


def portfolio_context(runtime_root):
    base = capability_context(runtime_root)
    return {
        "runtime_root": base["runtime_root"],
        "adapter_portfolio_shadow_enabled": True,
        "execute_one_portfolio_cycle": True,
        "allowed_domain_actions": base["allowed_domain_actions"],
    }


def capability_bundle_digest():
    return empty_capability_bundle("agent")["capability_bundle_digest"]


def portfolio_bundle_digest():
    return empty_bundle("agent")["portfolio_bundle_digest"]


def plan(
    run_id,
    sources,
    root,
    adapter_registry,
    previous_capability_state_digest,
    previous_capability_bundle_digest,
    previous_portfolio_state_digest,
    previous_portfolio_bundle_digest,
):
    packet = {
        "version": PLAN_VERSION,
        "portfolio_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "expected_previous_capability_state_digest": previous_capability_state_digest,
        "expected_previous_capability_bundle_digest": previous_capability_bundle_digest,
        "expected_previous_portfolio_state_digest": previous_portfolio_state_digest,
        "expected_previous_portfolio_bundle_digest": previous_portfolio_bundle_digest,
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
            "ticket": 0.60,
            "handover": 0.58,
            "observe": 0.48,
            "hold": 0.12,
            "freeze": 0.08
        },
        "max_shadow_candidates": 8,
        "max_pending_predictions": 256,
        "max_resolved_predictions": 256,
        "max_portfolio_holonomy": 256,
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
    packet["portfolio_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(
    plan_packet,
    sources,
    root,
    adapter_registry,
    previous_capability_bundle_digest,
    previous_portfolio_bundle_digest,
):
    packet = {
        "version": LICENSE_VERSION,
        "bound_portfolio_plan_digest": plan_packet["portfolio_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "bound_previous_capability_bundle_digest": previous_capability_bundle_digest,
        "bound_previous_portfolio_bundle_digest": previous_portfolio_bundle_digest,
        "shadow_execution_allowed": False,
        "shadow_external_actuation_allowed": False,
        "shadow_world_update_allowed": False,
        "shadow_capability_connection_update_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
        "external_network_effect_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "capability_state_read_allowed",
        "capability_bundle_read_allowed",
        "portfolio_bundle_read_allowed",
        "portfolio_selection_allowed",
        "one_live_capability_cycle_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "portfolio_bundle_write_allowed",
        "portfolio_state_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        packet[field] = True
    return packet

__all__ = [
    "portfolio_context",
    "capability_bundle_digest",
    "portfolio_bundle_digest",
    "plan",
    "license_packet",
    "registry",
    "root_packet",
    "source",
]
