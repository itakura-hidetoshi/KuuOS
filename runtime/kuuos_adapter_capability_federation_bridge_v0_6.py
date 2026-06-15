#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    LICENSE_VERSION as FEDERATION_LICENSE_VERSION,
    PLAN_VERSION as FEDERATION_PLAN_VERSION,
    REGISTRY_VERSION,
    REQUIRED_BOUNDARY as FEDERATION_REQUIRED_BOUNDARY,
    batch_digest,
    plan_digest as federation_plan_digest,
    registry_digest,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import as_list, mapping


def derived_registry(
    registry: Mapping[str, Any],
    selection: Mapping[str, Any],
) -> dict[str, Any]:
    selected_id = str(selection.get("selected_federation_adapter_id", ""))
    adapters: list[dict[str, Any]] = []
    for raw in as_list(registry.get("adapters")):
        entry = dict(mapping(raw))
        entry["enabled"] = entry.get("federation_adapter_id") == selected_id
        entry["selected_by_capability_gauge"] = entry["enabled"]
        adapters.append(entry)
    packet = {
        "version": REGISTRY_VERSION,
        "registry_id": str(registry.get("registry_id", ""))
        + ":capability-selected",
        "parent_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "capability_selection_digest": selection.get("selection_digest", ""),
        "adapters": adapters,
    }
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def build_child_packets(
    *,
    capability_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_principles_packet: Mapping[str, Any],
    selected_entry: Mapping[str, Any],
    selection: Mapping[str, Any],
    registry: Mapping[str, Any],
    previous_federation_state: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    child_registry = derived_registry(registry, selection)
    selected_routing = mapping(selected_entry.get("capability_routing_table"))
    fallback_routing = mapping(capability_plan.get("routing_table"))
    child_plan = {
        "version": FEDERATION_PLAN_VERSION,
        "federation_run_id": str(capability_plan.get("capability_run_id", ""))
        + ":federation",
        "agent_id": str(capability_plan.get("agent_id", "")),
        "expected_source_batch_digest": batch_digest(source_packets),
        "expected_root_principles_digest": root_principles_packet.get(
            "root_principles_digest", ""
        ),
        "expected_adapter_registry_digest": child_registry.get(
            "adapter_registry_digest", ""
        ),
        "expected_previous_federation_state_digest": previous_federation_state.get(
            "federation_state_digest", ""
        ),
        "max_sources_per_cycle": int(
            capability_plan.get("max_sources_per_cycle", 8)
        ),
        "max_signals_per_source": int(
            capability_plan.get("max_signals_per_source", 8)
        ),
        "max_total_signals": int(capability_plan.get("max_total_signals", 32)),
        "max_generated_goals": int(
            capability_plan.get("max_generated_goals", 8)
        ),
        "max_selected_goals": int(
            capability_plan.get("max_selected_goals", 4)
        ),
        "min_goal_score": float(capability_plan.get("min_goal_score", 0.35)),
        "min_action_scale": float(capability_plan.get("min_action_scale", 0.12)),
        "renewal_window_steps": int(
            capability_plan.get("renewal_window_steps", 3)
        ),
        "max_bundle_sections": int(
            capability_plan.get("max_bundle_sections", 256)
        ),
        "max_new_sections_per_run": int(
            capability_plan.get("max_new_sections_per_run", 8)
        ),
        "max_transports_per_section": int(
            capability_plan.get("max_transports_per_section", 4)
        ),
        "routing_table": dict(selected_routing or fallback_routing),
        "boundary": dict(FEDERATION_REQUIRED_BOUNDARY),
    }
    child_plan["federation_plan_digest"] = federation_plan_digest(child_plan)
    child_license = {
        "version": FEDERATION_LICENSE_VERSION,
        "bound_plan_digest": child_plan["federation_plan_digest"],
        "bound_source_batch_digest": child_plan["expected_source_batch_digest"],
        "bound_root_principles_digest": child_plan[
            "expected_root_principles_digest"
        ],
        "bound_adapter_registry_digest": child_registry[
            "adapter_registry_digest"
        ],
        "external_network_effect_allowed": False,
        "source_authority_transfer_allowed": False,
        "adapter_authority_inheritance_allowed": False,
    }
    for field in (
        "source_read_allowed",
        "source_normalization_allowed",
        "adapter_selection_allowed",
        "supervisor_cycle_allowed",
        "effect_evidence_write_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        child_license[field] = True
    return child_registry, child_plan, child_license
