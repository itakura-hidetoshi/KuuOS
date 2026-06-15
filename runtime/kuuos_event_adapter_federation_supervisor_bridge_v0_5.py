#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_renewable_gauge_supervisor_types_v0_4 import (
    LICENSE_VERSION as SUPERVISOR_LICENSE_VERSION,
    PLAN_VERSION as SUPERVISOR_PLAN_VERSION,
    REQUIRED_BOUNDARY as SUPERVISOR_REQUIRED_BOUNDARY,
    plan_digest as supervisor_plan_digest,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import mapping


def build_supervisor_packets(
    *,
    federation_plan: Mapping[str, Any],
    normalized_wake: Mapping[str, Any],
    root_principles_packet: Mapping[str, Any],
    adapter_profile: Mapping[str, Any],
    previous_supervisor_state: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    run_id = str(federation_plan.get("federation_run_id", "")) + ":supervisor"
    plan = {
        "version": SUPERVISOR_PLAN_VERSION,
        "supervisor_run_id": run_id,
        "agent_id": str(federation_plan.get("agent_id", "")),
        "expected_wake_event_digest": normalized_wake.get("wake_event_digest"),
        "expected_root_principles_digest": root_principles_packet.get("root_principles_digest"),
        "expected_adapter_profile_digest": adapter_profile.get("adapter_profile_digest"),
        "expected_previous_supervisor_state_digest": previous_supervisor_state.get(
            "supervisor_state_digest", ""
        ),
        "max_generated_goals": int(federation_plan.get("max_generated_goals", 8)),
        "max_selected_goals": int(federation_plan.get("max_selected_goals", 4)),
        "min_goal_score": float(federation_plan.get("min_goal_score", 0.35)),
        "min_action_scale": float(federation_plan.get("min_action_scale", 0.12)),
        "renewal_window_steps": int(federation_plan.get("renewal_window_steps", 3)),
        "max_bundle_sections": int(federation_plan.get("max_bundle_sections", 256)),
        "max_new_sections_per_run": int(
            federation_plan.get("max_new_sections_per_run", 8)
        ),
        "max_transports_per_section": int(
            federation_plan.get("max_transports_per_section", 4)
        ),
        "routing_table": dict(mapping(federation_plan.get("routing_table"))),
        "boundary": dict(SUPERVISOR_REQUIRED_BOUNDARY),
    }
    plan["supervisor_plan_digest"] = supervisor_plan_digest(plan)
    license_packet = {
        "version": SUPERVISOR_LICENSE_VERSION,
        "bound_plan_digest": plan["supervisor_plan_digest"],
        "bound_wake_event_digest": normalized_wake.get("wake_event_digest"),
        "bound_root_principles_digest": root_principles_packet.get(
            "root_principles_digest"
        ),
        "bound_adapter_profile_digest": adapter_profile.get("adapter_profile_digest"),
        "wake_consume_allowed": True,
        "telos_renewal_allowed": True,
        "gauge_sync_allowed": True,
        "local_intervention_allowed": True,
        "next_wake_write_allowed": True,
        "state_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "external_network_effect_allowed": False,
    }
    return plan, license_packet
