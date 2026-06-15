#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    REGISTRY_VERSION,
    batch_digest,
    registry_digest,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    LICENSE_VERSION as CAPABILITY_LICENSE_VERSION,
    PLAN_VERSION as CAPABILITY_PLAN_VERSION,
    REQUIRED_BOUNDARY as CAPABILITY_REQUIRED_BOUNDARY,
    as_list,
    mapping,
    plan_digest as capability_plan_digest,
)


def derived_live_registry(
    registry: Mapping[str, Any], selection: Mapping[str, Any]
) -> dict[str, Any]:
    live_id = str(selection.get("live_adapter_id", ""))
    adapters: list[dict[str, Any]] = []
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        entry["enabled"] = entry.get("federation_adapter_id") == live_id
        entry["selected_by_portfolio_shadow_v0_7"] = entry["enabled"]
        entry["shadow_non_actuating"] = not entry["enabled"]
        adapters.append(entry)
    packet = {
        "version": REGISTRY_VERSION,
        "registry_id": str(registry.get("registry_id", ""))
        + ":portfolio-live-only",
        "parent_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "portfolio_selection_digest": selection.get(
            "portfolio_selection_digest", ""
        ),
        "adapters": adapters,
    }
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def build_child_capability_packets(
    *,
    portfolio_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    derived_registry: Mapping[str, Any],
    previous_capability_state: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    plan = {
        "version": CAPABILITY_PLAN_VERSION,
        "capability_run_id": str(portfolio_plan.get("portfolio_run_id", ""))
        + ":capability",
        "agent_id": str(portfolio_plan.get("agent_id", "")),
        "expected_source_batch_digest": batch_digest(source_packets),
        "expected_root_principles_digest": root_packet.get(
            "root_principles_digest", ""
        ),
        "expected_adapter_registry_digest": derived_registry.get(
            "adapter_registry_digest", ""
        ),
        "expected_previous_capability_state_digest": previous_capability_state.get(
            "capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": previous_capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "learning_rate": float(portfolio_plan.get("learning_rate", 0.7)),
        "exploration_weight": float(
            portfolio_plan.get("exploration_weight", 0.18)
        ),
        "max_exploration_bonus": float(
            portfolio_plan.get("max_exploration_bonus", 0.18)
        ),
        "curvature_penalty": float(
            portfolio_plan.get("curvature_penalty", 0.2)
        ),
        "require_effect_observation": True,
        "max_sources_per_cycle": int(
            portfolio_plan.get("max_sources_per_cycle", 8)
        ),
        "max_signals_per_source": int(
            portfolio_plan.get("max_signals_per_source", 8)
        ),
        "max_total_signals": int(
            portfolio_plan.get("max_total_signals", 32)
        ),
        "max_generated_goals": int(
            portfolio_plan.get("max_generated_goals", 8)
        ),
        "max_selected_goals": int(
            portfolio_plan.get("max_selected_goals", 4)
        ),
        "min_goal_score": float(
            portfolio_plan.get("min_goal_score", 0.35)
        ),
        "min_action_scale": float(
            portfolio_plan.get("min_action_scale", 0.12)
        ),
        "renewal_window_steps": int(
            portfolio_plan.get("renewal_window_steps", 3)
        ),
        "max_bundle_sections": int(
            portfolio_plan.get("max_bundle_sections", 256)
        ),
        "max_new_sections_per_run": int(
            portfolio_plan.get("max_new_sections_per_run", 8)
        ),
        "max_transports_per_section": int(
            portfolio_plan.get("max_transports_per_section", 4)
        ),
        "routing_table": {},
        "boundary": dict(CAPABILITY_REQUIRED_BOUNDARY),
    }
    plan["capability_plan_digest"] = capability_plan_digest(plan)
    license_packet = {
        "version": CAPABILITY_LICENSE_VERSION,
        "bound_plan_digest": plan["capability_plan_digest"],
        "bound_source_batch_digest": plan["expected_source_batch_digest"],
        "bound_root_principles_digest": plan[
            "expected_root_principles_digest"
        ],
        "bound_adapter_registry_digest": plan[
            "expected_adapter_registry_digest"
        ],
        "bound_previous_capability_bundle_digest": plan[
            "expected_previous_capability_bundle_digest"
        ],
        "external_network_effect_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "capability_bundle_read_allowed",
        "capability_selection_allowed",
        "federation_cycle_allowed",
        "effect_receipt_read_allowed",
        "capability_calibration_allowed",
        "bundle_write_allowed",
        "selection_write_allowed",
        "calibration_write_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        license_packet[field] = True
    return plan, license_packet
