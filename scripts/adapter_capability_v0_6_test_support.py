from __future__ import annotations

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import ROOT_VERSION, root_digest
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    ADAPTER_PROFILE_VERSION,
    LOCAL_ACTIONS,
    profile_digest,
)
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    REGISTRY_VERSION,
    SOURCE_VERSION,
    batch_digest,
    registry_digest,
    source_digest,
)
from runtime.kuuos_adapter_capability_gauge_model_v0_6 import empty_bundle
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    plan_digest,
)


def root_packet():
    packet = {
        "version": ROOT_VERSION,
        "root_id": "kuuos-root-001",
        "principles": [
            "emptiness",
            "dependent_origination",
            "harmony",
            "contemplation",
            "repairability",
            "benefit_others",
        ],
        "protected": True,
        "self_rewrite_allowed": False,
    }
    packet["root_principles_digest"] = root_digest(packet)
    return packet


def profile(adapter_id: str):
    packet = {
        "version": ADAPTER_PROFILE_VERSION,
        "adapter_id": adapter_id,
        "backend": "qi_local_execution_adapter_v0_2",
        "supported_domain_actions": sorted(LOCAL_ACTIONS),
        "result_to_curvature_mapping": "deterministic_local_effect_v0_3",
    }
    packet["adapter_profile_digest"] = profile_digest(packet)
    return packet


def full_routing(action: str):
    return {
        "covariant_advance": action,
        "covariant_micro_intervention": action,
        "curvature_probe": action,
        "effect_integration_transport": action,
        "scaled_parallel_transport": action,
        "local_repair_gauge": action,
        "chart_transition": action,
        "curvature_reobservation": action,
        "section_extension": action,
        "handover_or_redesign": action,
    }


def registry():
    profile_a = profile("adapter-a-profile")
    profile_b = profile("adapter-b-profile")
    packet = {
        "version": REGISTRY_VERSION,
        "registry_id": "capability-registry-v06",
        "adapters": [
            {
                "federation_adapter_id": "adapter-a",
                "enabled": True,
                "priority": 100,
                "accepted_source_kinds": ["observation", "resource_change"],
                "accepted_source_ids": [],
                "external_network_effect_allowed": False,
                "capability_prior": 0.72,
                "capability_routing_table": full_routing("hold"),
                "adapter_profile": profile_a,
            },
            {
                "federation_adapter_id": "adapter-b",
                "enabled": True,
                "priority": 1,
                "accepted_source_kinds": ["observation", "resource_change"],
                "accepted_source_ids": [],
                "external_network_effect_allowed": False,
                "capability_prior": 0.55,
                "capability_routing_table": full_routing("advance_tick"),
                "adapter_profile": profile_b,
            },
        ],
    }
    packet["adapter_registry_digest"] = registry_digest(packet)
    return packet


def signal(signal_id: str, target: str):
    return {
        "signal_id": signal_id,
        "kind": "opportunity",
        "target": target,
        "magnitude": 0.75,
        "urgency": 0.8,
        "evidence": 0.8,
        "uncertainty": 0.2,
        "irreversibility": 0.1,
        "recoverability": 0.9,
        "relational_benefit": 0.85,
        "autonomy_gain": 0.8,
    }


def source(event_id: str, kind: str = "observation"):
    packet = {
        "version": SOURCE_VERSION,
        "source_id": "capability-sensor",
        "source_event_id": event_id,
        "source_kind": kind,
        "priority": 0.9,
        "trust_weight": 0.9,
        "world_context_digest": "world-" + event_id,
        "process_tensor_context_digest": "process-" + event_id,
        "non_markov_context_digest": "memory-" + event_id,
        "signals": [signal("signal-" + event_id, "target-" + kind)],
        "telos_renewal_requested": True,
        "intervention_requested": True,
    }
    packet["source_packet_digest"] = source_digest(packet)
    return packet


def plan(
    run_id: str,
    sources,
    root,
    adapter_registry,
    previous_state_digest: str,
    previous_bundle_digest: str,
):
    packet = {
        "version": PLAN_VERSION,
        "capability_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "expected_previous_capability_state_digest": previous_state_digest,
        "expected_previous_capability_bundle_digest": previous_bundle_digest,
        "learning_rate": 0.7,
        "exploration_weight": 0.18,
        "max_exploration_bonus": 0.18,
        "curvature_penalty": 0.2,
        "require_effect_observation": True,
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
        "routing_table": {},
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["capability_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, sources, root, adapter_registry, previous_bundle_digest):
    packet = {
        "version": LICENSE_VERSION,
        "bound_plan_digest": plan_packet["capability_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": adapter_registry[
            "adapter_registry_digest"
        ],
        "bound_previous_capability_bundle_digest": previous_bundle_digest,
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
        packet[field] = True
    return packet


def context(runtime_root):
    return {
        "runtime_root": str(runtime_root),
        "adapter_capability_gauge_enabled": True,
        "execute_one_capability_cycle": True,
        "allowed_domain_actions": sorted(LOCAL_ACTIONS),
    }


def initial_bundle_digest():
    return empty_bundle("agent")["capability_bundle_digest"]
