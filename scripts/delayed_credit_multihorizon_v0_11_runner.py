from __future__ import annotations

import json
import pathlib

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import (
    empty_bundle as empty_capability_bundle,
)
from runtime.kuuos_adapter_portfolio_shadow_core_v0_7 import (
    build_adapter_portfolio_shadow,
)
from runtime.kuuos_delayed_credit_multihorizon_cycle_v0_11 import (
    build_delayed_credit_multihorizon,
)
from scripts.adapter_portfolio_shadow_v0_7_test_support import (
    license_packet as portfolio_license,
    plan as portfolio_plan,
    portfolio_context,
)
from scripts.bounded_portfolio_experiment_v0_8_test_support import (
    initial_portfolio_digest,
)
from scripts.delayed_credit_multihorizon_v0_11_test_support import (
    horizon_context,
    initial_experiment,
    initial_horizon,
    initial_policy,
    initial_regret,
    license_packet,
    plan,
    source,
)


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl(path: pathlib.Path):
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def no_graph(value):
    forbidden = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
    if isinstance(value, dict):
        assert forbidden.isdisjoint(value.keys())
        for child in value.values():
            no_graph(child)
    elif isinstance(value, list):
        for child in value:
            no_graph(child)


def snapshots(runtime_root: pathlib.Path, portfolio):
    names = {
        "capability_state": "kuuos_adapter_capability_state_v0_6.json",
        "capability_bundle": "kuuos_adapter_capability_bundle_v0_6.json",
        "experiment_state": "kuuos_bounded_portfolio_experiment_state_v0_8.json",
        "experiment_bundle": "kuuos_bounded_portfolio_experiment_bundle_v0_8.json",
        "policy_state": "kuuos_experiment_outcome_policy_state_v0_9.json",
        "policy_bundle": "kuuos_experiment_outcome_policy_bundle_v0_9.json",
        "regret_state": "kuuos_policy_regret_cadence_state_v0_10.json",
        "regret_bundle": "kuuos_policy_regret_cadence_bundle_v0_10.json",
        "horizon_state": "kuuos_delayed_credit_multihorizon_state_v0_11.json",
        "horizon_bundle": "kuuos_delayed_credit_multihorizon_bundle_v0_11.json",
        "gauge_state": "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "gauge_bundle": "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json",
    }
    result = {key: read(runtime_root / name) for key, name in names.items()}
    result["source_portfolio_bundle"] = portfolio
    return result


def seed(runtime_root: pathlib.Path, root, registry):
    sources = [source("horizon-seed-001")]
    empty_capability = empty_capability_bundle("agent")
    seed_plan = portfolio_plan(
        "horizon-portfolio-seed-001",
        sources,
        root,
        registry,
        "",
        empty_capability["capability_bundle_digest"],
        "",
        initial_portfolio_digest(),
    )
    result = build_adapter_portfolio_shadow(
        runtime_context=portfolio_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=registry,
        portfolio_plan=seed_plan,
        portfolio_license=portfolio_license(
            seed_plan,
            sources,
            root,
            registry,
            empty_capability["capability_bundle_digest"],
            initial_portfolio_digest(),
        ),
    )
    assert result.status.endswith("READY"), result.blockers
    portfolio = read(runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json")
    current = {
        "capability_state": read(runtime_root / "kuuos_adapter_capability_state_v0_6.json"),
        "capability_bundle": read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"),
        "source_portfolio_bundle": portfolio,
        "experiment_state": {},
        "experiment_bundle": initial_experiment(portfolio),
        "policy_state": {},
        "policy_bundle": initial_policy(),
        "regret_state": {},
        "regret_bundle": initial_regret(),
        "horizon_state": {},
        "horizon_bundle": initial_horizon(),
        "gauge_state": read(runtime_root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json"),
        "gauge_bundle": read(runtime_root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json"),
    }
    return result, portfolio, current


def make_plan(run_id, sources, root, registry, current):
    return plan(
        run_id,
        sources,
        root,
        registry,
        current["capability_state"].get("capability_state_digest", ""),
        current["capability_bundle"]["capability_bundle_digest"],
        current["source_portfolio_bundle"]["portfolio_bundle_digest"],
        current["experiment_state"].get("experiment_state_digest", ""),
        current["experiment_bundle"]["experiment_bundle_digest"],
        current["policy_state"].get("policy_state_digest", ""),
        current["policy_bundle"]["policy_bundle_digest"],
        current["regret_state"].get("regret_state_digest", ""),
        current["regret_bundle"]["regret_bundle_digest"],
        current["horizon_state"].get("horizon_state_digest", ""),
        current["horizon_bundle"]["horizon_bundle_digest"],
        current["gauge_state"].get("gauge_state_digest", ""),
        current["gauge_bundle"].get("gauge_bundle_digest", ""),
    )


def execute(runtime_root, run_id, sources, root, registry, current):
    packet = make_plan(run_id, sources, root, registry, current)
    result = build_delayed_credit_multihorizon(
        runtime_context=horizon_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=registry,
        horizon_plan=packet,
        horizon_license=license_packet(
            packet,
            sources,
            root,
            registry,
            current["regret_bundle"]["regret_bundle_digest"],
            current["horizon_bundle"]["horizon_bundle_digest"],
        ),
    )
    return packet, result
