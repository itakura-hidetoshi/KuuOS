from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import LICENSE_VERSION


def build_local_license(*, local_plan: Mapping[str, Any], sources: list[Mapping[str, Any]], root_packet: Mapping[str, Any], registry: Mapping[str, Any], current: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = {
        "version": LICENSE_VERSION,
        "bound_arbitration_plan_digest": local_plan.get("arbitration_plan_digest", ""),
        "bound_source_batch_digest": batch_digest(sources),
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "bound_previous_horizon_bundle_digest": current["horizon_bundle"].get("horizon_bundle_digest", ""),
        "bound_previous_arbitration_bundle_digest": current["bundle"].get("arbitration_bundle_digest", ""),
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
        "source_read_allowed", "upstream_state_read_allowed",
        "gauge_arbitration_allowed", "parallel_transport_allowed",
        "one_child_horizon_cycle_allowed", "arbitration_bundle_write_allowed",
        "arbitration_state_write_allowed", "decision_write_allowed",
        "outcome_write_allowed", "child_packet_write_allowed",
        "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    ):
        packet[field] = True
    return packet
