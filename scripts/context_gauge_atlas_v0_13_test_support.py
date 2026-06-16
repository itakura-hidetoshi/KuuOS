from runtime.kuuos_active_gauge_intervention_types_v0_3 import LOCAL_ACTIONS
from runtime.kuuos_context_gauge_atlas_basis_v0_13 import empty_bundle
from runtime.kuuos_context_gauge_atlas_types_v0_13 import LICENSE_VERSION, PLAN_VERSION, REQUIRED_BOUNDARY, plan_digest
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest, source_digest
from scripts.horizon_gauge_arbitration_v0_12_test_support import experiment_registry, plan as local_template_plan, root_packet, source


def atlas_context(runtime_root):
    return {"runtime_root": str(runtime_root), "context_gauge_atlas_enabled": True, "execute_one_atlas_cycle": True, "allowed_domain_actions": sorted(LOCAL_ACTIONS)}


def initial_atlas(agent_id="agent"):
    return empty_bundle(agent_id)


def source_for(event_id, source_id):
    packet = source(event_id)
    packet["source_id"] = source_id
    packet["source_packet_digest"] = source_digest(packet)
    return packet


def plan(run_id, sources, root, registry, current):
    base = local_template_plan(run_id + ":template", sources, root, registry, current)
    for field in ("version", "arbitration_run_id", "arbitration_plan_digest", "boundary"):
        base.pop(field, None)
    packet = {
        **base,
        "version": PLAN_VERSION,
        "atlas_run_id": run_id,
        "agent_id": "agent",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root["root_principles_digest"],
        "expected_adapter_registry_digest": registry["adapter_registry_digest"],
        "expected_previous_atlas_state_digest": current["atlas_state"].get("atlas_state_digest", ""),
        "expected_previous_atlas_bundle_digest": current["atlas_bundle"]["atlas_bundle_digest"],
        "minimum_chart_overlap": 0.5,
        "target_chart_retention": 0.7,
        "transition_phase_gain": 0.06,
        "plural_atlas_curvature_threshold": 0.08,
        "max_atlas_holonomy": 256,
        "max_atlas_outcomes": 256,
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    packet["atlas_plan_digest"] = plan_digest(packet)
    return packet


def license_packet(plan_packet, sources, root, registry, current):
    packet = {
        "version": LICENSE_VERSION,
        "bound_atlas_plan_digest": plan_packet["atlas_plan_digest"],
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root["root_principles_digest"],
        "bound_adapter_registry_digest": registry["adapter_registry_digest"],
        "bound_previous_atlas_bundle_digest": current["atlas_bundle"]["atlas_bundle_digest"],
        "multiple_local_cycles_allowed": False,
        "chart_locality_bypass_allowed": False,
        "cocycle_veto_allowed": False,
        "external_network_effect_allowed": False,
        "world_update_allowed": False,
        "memory_overwrite_allowed": False,
    }
    for field in ("source_read_allowed", "atlas_read_allowed", "atlas_transport_allowed", "one_local_cycle_allowed", "atlas_bundle_write_allowed", "atlas_state_write_allowed", "decision_write_allowed", "outcome_write_allowed", "child_packet_write_allowed", "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed"):
        packet[field] = True
    return packet


__all__ = ["atlas_context", "initial_atlas", "source_for", "plan", "license_packet", "experiment_registry", "root_packet"]
