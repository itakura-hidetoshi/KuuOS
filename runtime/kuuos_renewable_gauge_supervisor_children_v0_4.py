#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import (
    LICENSE_VERSION as TELOS_LICENSE_VERSION,
    OBSERVATION_VERSION,
    PLAN_VERSION as TELOS_PLAN_VERSION,
    REQUIRED_BOUNDARY as TELOS_REQUIRED_BOUNDARY,
    observation_digest,
    plan_digest as telos_plan_digest,
)
from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    LICENSE_VERSION as GAUGE_LICENSE_VERSION,
    PLAN_VERSION as GAUGE_PLAN_VERSION,
    REQUIRED_BOUNDARY as GAUGE_REQUIRED_BOUNDARY,
    plan_digest as gauge_plan_digest,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    LICENSE_VERSION as INTERVENTION_LICENSE_VERSION,
    PLAN_VERSION as INTERVENTION_PLAN_VERSION,
    REQUIRED_BOUNDARY as INTERVENTION_REQUIRED_BOUNDARY,
    plan_digest as intervention_plan_digest,
)
from runtime.kuuos_renewable_gauge_supervisor_types_v0_4 import (
    NEXT_WAKE_VERSION,
    as_list,
    mapping,
    next_wake_digest,
)


def wake_to_observation(wake: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": OBSERVATION_VERSION,
        "observation_id": "wake-observation-" + str(wake.get("wake_event_id", "")),
        "world_context_digest": str(wake.get("world_context_digest", "")),
        "process_tensor_context_digest": str(wake.get("process_tensor_context_digest", "")),
        "non_markov_context_digest": str(wake.get("non_markov_context_digest", "")),
        "signals": [dict(mapping(item)) for item in as_list(wake.get("signals"))],
    }
    packet["observation_digest"] = observation_digest(packet)
    return packet


def build_telos_packets(
    *,
    wake: Mapping[str, Any],
    root_packet: Mapping[str, Any],
    supervisor_plan: Mapping[str, Any],
    current_telos_state: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    observation = wake_to_observation(wake)
    plan = {
        "version": TELOS_PLAN_VERSION,
        "telos_run_id": str(supervisor_plan.get("supervisor_run_id")) + ":telos",
        "agent_id": str(supervisor_plan.get("agent_id")),
        "expected_root_principles_digest": root_packet.get("root_principles_digest"),
        "expected_observation_digest": observation.get("observation_digest"),
        "expected_previous_state_digest": current_telos_state.get("telos_state_digest", ""),
        "max_generated_goals": int(supervisor_plan.get("max_generated_goals", 8)),
        "max_selected_goals": int(supervisor_plan.get("max_selected_goals", 4)),
        "min_goal_score": float(supervisor_plan.get("min_goal_score", 0.35)),
        "min_action_scale": float(supervisor_plan.get("min_action_scale", 0.12)),
        "renewal_window_steps": int(supervisor_plan.get("renewal_window_steps", 3)),
        "boundary": dict(TELOS_REQUIRED_BOUNDARY),
    }
    plan["telos_plan_digest"] = telos_plan_digest(plan)
    license_packet = {
        "version": TELOS_LICENSE_VERSION,
        "bound_plan_digest": plan["telos_plan_digest"],
        "bound_observation_digest": observation["observation_digest"],
        "bound_root_principles_digest": root_packet.get("root_principles_digest"),
        "goal_generation_allowed": True,
        "subgoal_synthesis_allowed": True,
        "goal_selection_allowed": True,
        "commitment_seed_write_allowed": True,
        "state_write_allowed": True,
        "ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "domain_action_preparation_allowed": True,
        "root_principles_rewrite_allowed": False,
    }
    return observation, plan, license_packet


def build_gauge_packets(
    *,
    runtime_root: pathlib.Path,
    supervisor_plan: Mapping[str, Any],
    telos_state: Mapping[str, Any],
    goal_set: Mapping[str, Any],
    seed: Mapping[str, Any],
    current_gauge_state: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    plan = {
        "version": GAUGE_PLAN_VERSION,
        "gauge_run_id": str(supervisor_plan.get("supervisor_run_id")) + ":gauge",
        "agent_id": str(supervisor_plan.get("agent_id")),
        "expected_telos_state_digest": telos_state.get("telos_state_digest"),
        "expected_goal_set_digest": goal_set.get("goal_set_digest"),
        "expected_commitment_seed_digest": seed.get("commitment_seed_digest"),
        "expected_previous_gauge_state_digest": current_gauge_state.get("gauge_state_digest", ""),
        "expected_effect_receipt_digest": "",
        "max_bundle_sections": int(supervisor_plan.get("max_bundle_sections", 256)),
        "max_new_sections_per_run": int(supervisor_plan.get("max_new_sections_per_run", 8)),
        "max_transports_per_section": int(supervisor_plan.get("max_transports_per_section", 4)),
        "min_action_scale": float(supervisor_plan.get("min_action_scale", 0.02)),
        "boundary": dict(GAUGE_REQUIRED_BOUNDARY),
    }
    plan["gauge_plan_digest"] = gauge_plan_digest(plan)
    license_packet = {
        "version": GAUGE_LICENSE_VERSION,
        "bound_plan_digest": plan["gauge_plan_digest"],
        "bound_telos_state_digest": telos_state.get("telos_state_digest"),
        "bound_goal_set_digest": goal_set.get("goal_set_digest"),
        "bound_commitment_seed_digest": seed.get("commitment_seed_digest"),
        "bound_effect_receipt_digest": "",
    }
    for field in (
        "source_read_allowed", "bundle_initialize_allowed", "telos_section_extension_allowed",
        "parallel_transport_allowed", "curvature_update_allowed", "local_gauge_correction_allowed",
        "holonomy_append_allowed", "covariant_action_prepare_allowed", "state_write_allowed",
        "bundle_write_allowed", "action_write_allowed", "ledger_append_allowed",
        "receipt_write_allowed", "audit_append_allowed",
    ):
        license_packet[field] = True
    return plan, license_packet


def build_intervention_packets(
    *,
    supervisor_plan: Mapping[str, Any],
    adapter_profile: Mapping[str, Any],
    gauge_state: Mapping[str, Any],
    bundle: Mapping[str, Any],
    action: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    plan = {
        "version": INTERVENTION_PLAN_VERSION,
        "intervention_run_id": str(supervisor_plan.get("supervisor_run_id")) + ":intervention",
        "gauge_reentry_run_id": str(supervisor_plan.get("supervisor_run_id")) + ":gauge-reentry",
        "agent_id": str(supervisor_plan.get("agent_id")),
        "adapter_id": str(adapter_profile.get("adapter_id")),
        "expected_gauge_state_digest": gauge_state.get("gauge_state_digest"),
        "expected_gauge_bundle_digest": bundle.get("gauge_bundle_digest"),
        "expected_covariant_action_digest": action.get("covariant_action_digest"),
        "auto_reenter_gauge": True,
        "reentry_max_bundle_sections": int(supervisor_plan.get("max_bundle_sections", 256)),
        "reentry_max_new_sections_per_run": int(supervisor_plan.get("max_new_sections_per_run", 8)),
        "reentry_max_transports_per_section": int(supervisor_plan.get("max_transports_per_section", 4)),
        "reentry_min_action_scale": float(supervisor_plan.get("min_action_scale", 0.02)),
        "routing_table": dict(mapping(supervisor_plan.get("routing_table"))),
        "boundary": dict(INTERVENTION_REQUIRED_BOUNDARY),
    }
    plan["intervention_plan_digest"] = intervention_plan_digest(plan)
    license_packet = {
        "version": INTERVENTION_LICENSE_VERSION,
        "bound_plan_digest": plan["intervention_plan_digest"],
        "bound_adapter_profile_digest": adapter_profile.get("adapter_profile_digest"),
        "bound_gauge_state_digest": gauge_state.get("gauge_state_digest"),
        "bound_gauge_bundle_digest": bundle.get("gauge_bundle_digest"),
        "bound_covariant_action_digest": action.get("covariant_action_digest"),
    }
    for field in (
        "route_action_allowed", "domain_intervention_allowed", "local_adapter_execution_allowed",
        "effect_receipt_write_allowed", "gauge_reentry_allowed", "next_action_continue_allowed",
        "state_write_allowed", "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    ):
        license_packet[field] = True
    return plan, license_packet


def derive_next_wake(
    *,
    supervisor_run_id: str,
    cycle_index: int,
    action: Mapping[str, Any],
    commitment_seed: Mapping[str, Any],
) -> dict[str, Any]:
    action_ready = action.get("action_ready") is True
    packet = {
        "version": NEXT_WAKE_VERSION,
        "source_supervisor_run_id": supervisor_run_id,
        "source_cycle_index": cycle_index,
        "wake_kind": "effect_followup" if action_ready else "observation",
        "telos_renewal_requested": not action_ready,
        "intervention_requested": action_ready,
        "trigger": "next_covariant_action_ready" if action_ready else "new_context_signal_required",
        "source_action_digest": action.get("covariant_action_digest", ""),
        "source_section_id": action.get("section_id", ""),
        "accepted_events": as_list(mapping(commitment_seed.get("next_wake")).get("events")),
        "local_invocation_only": True,
    }
    packet["next_wake_digest"] = next_wake_digest(packet)
    return packet
