#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import LICENSE_VERSION

def build_child_horizon_license(*, child_plan: Mapping[str, Any], source_packets: list[Mapping[str, Any]], root_packet: Mapping[str, Any], adapter_registry: Mapping[str, Any], upstream: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = {
        "version": LICENSE_VERSION,
        "bound_horizon_plan_digest": child_plan.get("horizon_plan_digest", ""),
        "bound_source_batch_digest": batch_digest(source_packets),
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": adapter_registry.get("adapter_registry_digest", ""),
        "bound_previous_regret_bundle_digest": upstream["regret_bundle"].get("regret_bundle_digest", ""),
        "bound_previous_horizon_bundle_digest": upstream["horizon_bundle"].get("horizon_bundle_digest", ""),
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
        "source_read_allowed", "upstream_state_read_allowed",
        "gauge_evidence_read_allowed", "horizon_credit_update_allowed",
        "cadence_adaptation_allowed", "one_child_regret_cycle_allowed",
        "horizon_bundle_write_allowed", "horizon_state_write_allowed",
        "decision_write_allowed", "outcome_write_allowed",
        "child_packet_write_allowed", "ledger_append_allowed",
        "receipt_write_allowed", "audit_append_allowed",
    ):
        packet[field] = True
    return packet
