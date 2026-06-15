#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import PLAN_VERSION, REQUIRED_BOUNDARY, plan_digest

def build_child_horizon_plan(*, arbitration_plan: Mapping[str, Any], decision: Mapping[str, Any], source_packets: list[Mapping[str, Any]], root_packet: Mapping[str, Any], adapter_registry: Mapping[str, Any], upstream: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = dict(arbitration_plan)
    packet.pop("arbitration_plan_digest", None)
    packet.pop("expected_previous_arbitration_state_digest", None)
    packet.pop("expected_previous_arbitration_bundle_digest", None)
    packet.update({
        "version": PLAN_VERSION,
        "horizon_run_id": str(arbitration_plan.get("arbitration_run_id", "")) + ":horizon",
        "expected_source_batch_digest": batch_digest(source_packets),
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": adapter_registry.get("adapter_registry_digest", ""),
        "expected_capability_state_digest": upstream["capability_state"].get("capability_state_digest", ""),
        "expected_capability_bundle_digest": upstream["capability_bundle"].get("capability_bundle_digest", ""),
        "expected_source_portfolio_bundle_digest": upstream["source_portfolio_bundle"].get("portfolio_bundle_digest", ""),
        "expected_experiment_state_digest": upstream["experiment_state"].get("experiment_state_digest", ""),
        "expected_experiment_bundle_digest": upstream["experiment_bundle"].get("experiment_bundle_digest", ""),
        "expected_policy_state_digest": upstream["policy_state"].get("policy_state_digest", ""),
        "expected_policy_bundle_digest": upstream["policy_bundle"].get("policy_bundle_digest", ""),
        "expected_previous_regret_state_digest": upstream["regret_state"].get("regret_state_digest", ""),
        "expected_previous_regret_bundle_digest": upstream["regret_bundle"].get("regret_bundle_digest", ""),
        "expected_previous_horizon_state_digest": upstream["horizon_state"].get("horizon_state_digest", ""),
        "expected_previous_horizon_bundle_digest": upstream["horizon_bundle"].get("horizon_bundle_digest", ""),
        "expected_gauge_state_digest": upstream["gauge_state"].get("gauge_state_digest", ""),
        "expected_gauge_bundle_digest": upstream["gauge_bundle"].get("gauge_bundle_digest", ""),
        "short_horizon_weight": decision.get("transported_short_weight", 0.0),
        "medium_horizon_weight": decision.get("transported_medium_weight", 0.0),
        "long_horizon_weight": decision.get("transported_long_weight", 0.0),
        "boundary": dict(REQUIRED_BOUNDARY),
    })
    packet["horizon_plan_digest"] = plan_digest(packet)
    return packet
