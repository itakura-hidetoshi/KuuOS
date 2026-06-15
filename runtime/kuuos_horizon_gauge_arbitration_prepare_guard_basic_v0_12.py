#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import contains_graph_keys


def apply_basic_guards(data):
    context = data["context"]
    values = data["values"]
    blockers = data["blockers"]
    if context.get("horizon_gauge_arbitration_enabled") is not True:
        blockers.append("horizon_gauge_arbitration_enabled_not_true")
    if context.get("execute_one_arbitration_cycle") is not True:
        blockers.append("execute_one_arbitration_cycle_not_true")
    if contains_graph_keys(data["sources"]) or contains_graph_keys(data["registry"]):
        blockers.append("graph_semantics_present")
    for name in (
        "capability_bundle",
        "source_portfolio_bundle",
        "experiment_bundle",
        "policy_bundle",
        "regret_bundle",
        "horizon_bundle",
    ):
        if not values[name]:
            blockers.append(f"source_{name}_missing")
    return data
