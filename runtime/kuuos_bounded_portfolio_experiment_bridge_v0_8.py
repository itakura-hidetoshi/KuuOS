#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_portfolio_shadow_bridge_v0_7 import (
    build_child_capability_packets,
    derived_live_registry,
)


def build_experiment_live_registry(
    registry: Mapping[str, Any], decision: Mapping[str, Any]
) -> dict[str, Any]:
    return derived_live_registry(
        registry,
        {
            "live_adapter_id": decision.get("live_adapter_id", ""),
            "portfolio_selection_digest": decision.get("experiment_decision_digest", ""),
        },
    )


def build_experiment_child_packets(
    *,
    experiment_plan: Mapping[str, Any],
    source_packets: list[Mapping[str, Any]],
    root_packet: Mapping[str, Any],
    derived_registry: Mapping[str, Any],
    previous_capability_state: Mapping[str, Any],
    previous_capability_bundle: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    bridge_plan = dict(experiment_plan)
    bridge_plan["portfolio_run_id"] = str(
        experiment_plan.get("experiment_run_id", "")
    )
    return build_child_capability_packets(
        portfolio_plan=bridge_plan,
        source_packets=source_packets,
        root_packet=root_packet,
        derived_registry=derived_registry,
        previous_capability_state=previous_capability_state,
        previous_capability_bundle=previous_capability_bundle,
    )
