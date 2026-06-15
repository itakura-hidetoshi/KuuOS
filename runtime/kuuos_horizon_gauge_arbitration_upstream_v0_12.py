#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import empty_bundle as empty_experiment_bundle
from runtime.kuuos_experiment_outcome_policy_model_v0_9 import empty_bundle as empty_policy_bundle
from runtime.kuuos_policy_regret_cadence_model_v0_10 import empty_bundle as empty_regret_bundle
from runtime.kuuos_delayed_credit_multihorizon_model_v0_11 import empty_bundle as empty_horizon_bundle
from runtime.kuuos_horizon_gauge_arbitration_basis_v0_12 import empty_bundle as empty_arbitration_bundle
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import read_json, write_json

def load_upstream(paths: Mapping[str, Any], agent_id: str) -> dict[str, dict[str, Any]]:
    values = {name: read_json(paths[name]) for name in (
        "capability_state", "capability_bundle", "source_portfolio_bundle",
        "experiment_state", "experiment_bundle", "policy_state", "policy_bundle",
        "regret_state", "regret_bundle", "horizon_state", "horizon_bundle",
        "gauge_state", "gauge_bundle", "state", "bundle",
    )}
    if not values["experiment_bundle"] and values["source_portfolio_bundle"]:
        values["experiment_bundle"] = empty_experiment_bundle(agent_id, values["source_portfolio_bundle"])
        write_json(paths["experiment_bundle"], values["experiment_bundle"])
    if not values["policy_bundle"]:
        values["policy_bundle"] = empty_policy_bundle(agent_id)
        write_json(paths["policy_bundle"], values["policy_bundle"])
    if not values["regret_bundle"]:
        values["regret_bundle"] = empty_regret_bundle(agent_id)
        write_json(paths["regret_bundle"], values["regret_bundle"])
    if not values["horizon_bundle"]:
        values["horizon_bundle"] = empty_horizon_bundle(agent_id)
        write_json(paths["horizon_bundle"], values["horizon_bundle"])
    if not values["bundle"]:
        values["bundle"] = empty_arbitration_bundle(agent_id)
    return values

def child_upstream(values: Mapping[str, Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {
        "capability_state": values["capability_state"],
        "capability_bundle": values["capability_bundle"],
        "source_portfolio_bundle": values["source_portfolio_bundle"],
        "experiment_state": values["experiment_state"],
        "experiment_bundle": values["experiment_bundle"],
        "policy_state": values["policy_state"],
        "policy_bundle": values["policy_bundle"],
        "regret_state": values["regret_state"],
        "regret_bundle": values["regret_bundle"],
        "horizon_state": values["horizon_state"],
        "horizon_bundle": values["horizon_bundle"],
        "gauge_state": values["gauge_state"],
        "gauge_bundle": values["gauge_bundle"],
    }
