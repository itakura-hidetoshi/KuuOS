#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_adapter_capability_gauge_model_v0_6 import (  # noqa: E402
    empty_bundle as empty_capability_bundle,
)
from runtime.kuuos_adapter_portfolio_shadow_core_v0_7 import (  # noqa: E402
    build_adapter_portfolio_shadow,
)
from runtime.kuuos_policy_regret_cadence_cycle_v0_10 import (  # noqa: E402
    build_policy_regret_cadence,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (  # noqa: E402
    BLOCKED,
    READY,
    REPLAYED,
)
from scripts.adapter_portfolio_shadow_v0_7_test_support import (  # noqa: E402
    license_packet as portfolio_license,
    plan as portfolio_plan,
    portfolio_context,
)
from scripts.bounded_portfolio_experiment_v0_8_test_support import (  # noqa: E402
    initial_portfolio_digest,
)
from scripts.policy_regret_cadence_v0_10_test_support import (  # noqa: E402
    experiment_registry,
    initial_experiment,
    initial_policy,
    initial_regret,
    license_packet,
    plan,
    regret_context,
    root_packet,
    source,
)


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl(path: pathlib.Path):
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def no_graph(value):
    forbidden = {"nodes", "edges", "dependencies", "commitment_graph_digest"}
    if isinstance(value, dict):
        assert forbidden.isdisjoint(value.keys())
        for child in value.values():
            no_graph(child)
    elif isinstance(value, list):
        for child in value:
            no_graph(child)


def execute(
    runtime_root,
    run_id,
    sources,
    root,
    adapter_registry,
    previous_capability_state_digest,
    previous_capability_bundle_digest,
    source_portfolio_bundle_digest,
    previous_experiment_state_digest,
    previous_experiment_bundle_digest,
    previous_policy_state_digest,
    previous_policy_bundle_digest,
    previous_regret_state_digest,
    previous_regret_bundle_digest,
):
    packet = plan(
        run_id,
        sources,
        root,
        adapter_registry,
        previous_capability_state_digest,
        previous_capability_bundle_digest,
        source_portfolio_bundle_digest,
        previous_experiment_state_digest,
        previous_experiment_bundle_digest,
        previous_policy_state_digest,
        previous_policy_bundle_digest,
        previous_regret_state_digest,
        previous_regret_bundle_digest,
    )
    result = build_policy_regret_cadence(
        runtime_context=regret_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=adapter_registry,
        regret_plan=packet,
        regret_license=license_packet(
            packet,
            sources,
            root,
            adapter_registry,
            previous_capability_bundle_digest,
            source_portfolio_bundle_digest,
            previous_experiment_bundle_digest,
            previous_policy_bundle_digest,
            previous_regret_bundle_digest,
        ),
    )
    return packet, result


def snapshots(runtime_root):
    return {
        "capability_state": read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        ),
        "capability_bundle": read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        ),
        "experiment_state": read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        ),
        "experiment_bundle": read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        ),
        "policy_state": read(
            runtime_root / "kuuos_experiment_outcome_policy_state_v0_9.json"
        ),
        "policy_bundle": read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        ),
        "regret_state": read(
            runtime_root / "kuuos_policy_regret_cadence_state_v0_10.json"
        ),
        "regret_bundle": read(
            runtime_root / "kuuos_policy_regret_cadence_bundle_v0_10.json"
        ),
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        adapter_registry = experiment_registry()

        seed_sources = [source("regret-seed-001")]
        seed_plan = portfolio_plan(
            "regret-portfolio-seed-001",
            seed_sources,
            root,
            adapter_registry,
            "",
            empty_capability_bundle("agent")["capability_bundle_digest"],
            "",
            initial_portfolio_digest(),
        )
        seed = build_adapter_portfolio_shadow(
            runtime_context=portfolio_context(runtime_root),
            source_packets=seed_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            portfolio_plan=seed_plan,
            portfolio_license=portfolio_license(
                seed_plan,
                seed_sources,
                root,
                adapter_registry,
                empty_capability_bundle("agent")["capability_bundle_digest"],
                initial_portfolio_digest(),
            ),
        )
        assert seed.status.endswith("READY"), seed.blockers
        assert seed.live_adapter_id == "adapter-a"
        assert seed.shadow_projection_count == 1

        source_portfolio_path = (
            runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json"
        )
        source_portfolio = read(source_portfolio_path)
        source_portfolio_bytes = source_portfolio_path.read_bytes()
        source_portfolio_digest = source_portfolio["portfolio_bundle_digest"]
        capability_state0 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle0 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        experiment0 = initial_experiment(source_portfolio)
        policy0 = initial_policy()
        regret0 = initial_regret()

        sources1 = [source("regret-event-001")]
        plan1, first = execute(
            runtime_root,
            "regret-001",
            sources1,
            root,
            adapter_registry,
            capability_state0["capability_state_digest"],
            capability_bundle0["capability_bundle_digest"],
            source_portfolio_digest,
            "",
            experiment0["experiment_bundle_digest"],
            "",
            policy0["policy_bundle_digest"],
            "",
            regret0["regret_bundle_digest"],
        )
        assert first.status == READY, first.blockers
        assert first.child_policy_mode == "experiment"
        assert first.child_live_adapter_id == "adapter-b"
        assert first.child_live_domain_action == "advance_tick"
        assert first.adapted_experiment_pressure_threshold == 0.6
        assert first.adapted_reobserve_pressure_threshold == 0.65
        assert first.adapted_experiment_interval == 3
        assert first.adapted_reobserve_interval == 3
        snap1 = snapshots(runtime_root)
        child_plan1 = read(
            runtime_root / "kuuos_policy_regret_cadence_child_plan_v0_10.json"
        )
        outcome1 = read(
            runtime_root / "kuuos_policy_regret_cadence_outcome_v0_10.json"
        )
        assert child_plan1["experiment_pressure_threshold"] == 0.6
        assert child_plan1["minimum_policy_cycles_between_experiments"] == 3
        assert outcome1["counterfactual_estimate_not_truth"] is True
        assert outcome1["unexecuted_alternative_not_outcome"] is True
        assert snap1["experiment_bundle"]["total_trial_count"] == 1
        assert snap1["experiment_bundle"]["trial_budget_spent"] == 0.2
        assert snap1["policy_bundle"]["generation"] == 1
        assert snap1["regret_bundle"]["generation"] == 1
        assert source_portfolio_path.read_bytes() == source_portfolio_bytes
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(runtime_root / "runtime_state.json")["tick"] == 2

        replay = build_policy_regret_cadence(
            runtime_context=regret_context(runtime_root),
            source_packets=sources1,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            regret_plan=plan1,
            regret_license=license_packet(
                plan1,
                sources1,
                root,
                adapter_registry,
                capability_bundle0["capability_bundle_digest"],
                source_portfolio_digest,
                experiment0["experiment_bundle_digest"],
                policy0["policy_bundle_digest"],
                regret0["regret_bundle_digest"],
            ),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(
            runtime_root / "kuuos_policy_regret_cadence_bundle_v0_10.json"
        )["generation"] == 1

        sources2 = [source("regret-event-002")]
        _, second = execute(
            runtime_root,
            "regret-002",
            sources2,
            root,
            adapter_registry,
            snap1["capability_state"]["capability_state_digest"],
            snap1["capability_bundle"]["capability_bundle_digest"],
            source_portfolio_digest,
            snap1["experiment_state"]["experiment_state_digest"],
            snap1["experiment_bundle"]["experiment_bundle_digest"],
            snap1["policy_state"]["policy_state_digest"],
            snap1["policy_bundle"]["policy_bundle_digest"],
            snap1["regret_state"]["regret_state_digest"],
            snap1["regret_bundle"]["regret_bundle_digest"],
        )
        assert second.status == READY, second.blockers
        assert second.child_policy_mode == "reobserve"
        assert second.child_live_domain_action == "observe"
        assert second.best_alternative_mode == "exploit"
        assert second.best_alternative_confidence >= 0.2
        assert second.bounded_regret > 0.0
        assert second.exploit_regret_credit > 0.0
        snap2 = snapshots(runtime_root)
        outcome2 = read(
            runtime_root / "kuuos_policy_regret_cadence_outcome_v0_10.json"
        )
        assert outcome2["raw_positive_gap"] > 0.0
        assert outcome2["best_alternative_mode"] == "exploit"
        assert snap2["experiment_bundle"]["total_trial_count"] == 1
        assert snap2["experiment_bundle"]["trial_budget_spent"] == 0.2
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 3
        assert read(runtime_root / "runtime_state.json")["tick"] == 2

        sources3 = [source("regret-event-003")]
        _, third = execute(
            runtime_root,
            "regret-003",
            sources3,
            root,
            adapter_registry,
            snap2["capability_state"]["capability_state_digest"],
            snap2["capability_bundle"]["capability_bundle_digest"],
            source_portfolio_digest,
            snap2["experiment_state"]["experiment_state_digest"],
            snap2["experiment_bundle"]["experiment_bundle_digest"],
            snap2["policy_state"]["policy_state_digest"],
            snap2["policy_bundle"]["policy_bundle_digest"],
            snap2["regret_state"]["regret_state_digest"],
            snap2["regret_bundle"]["regret_bundle_digest"],
        )
        assert third.status == READY, third.blockers
        assert third.child_policy_mode == "exploit"
        assert third.child_live_domain_action == "advance_tick"
        assert third.adapted_experiment_pressure_threshold > 0.6
        assert third.adapted_reobserve_pressure_threshold > 0.65
        assert third.adapted_experiment_interval > 3
        assert third.adapted_reobserve_interval > 3
        child_plan3 = read(
            runtime_root / "kuuos_policy_regret_cadence_child_plan_v0_10.json"
        )
        assert child_plan3["experiment_pressure_threshold"] == (
            third.adapted_experiment_pressure_threshold
        )
        assert child_plan3["minimum_policy_cycles_between_experiments"] == (
            third.adapted_experiment_interval
        )
        snap3 = snapshots(runtime_root)
        assert snap3["experiment_bundle"]["trial_budget_spent"] == 0.2
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 4
        assert read(runtime_root / "runtime_state.json")["tick"] == 3

        sources4 = [source("regret-event-004")]
        _, fourth = execute(
            runtime_root,
            "regret-004",
            sources4,
            root,
            adapter_registry,
            snap3["capability_state"]["capability_state_digest"],
            snap3["capability_bundle"]["capability_bundle_digest"],
            source_portfolio_digest,
            snap3["experiment_state"]["experiment_state_digest"],
            snap3["experiment_bundle"]["experiment_bundle_digest"],
            snap3["policy_state"]["policy_state_digest"],
            snap3["policy_bundle"]["policy_bundle_digest"],
            snap3["regret_state"]["regret_state_digest"],
            snap3["regret_bundle"]["regret_bundle_digest"],
        )
        assert fourth.status == READY, fourth.blockers
        assert fourth.child_policy_mode == "exploit"
        assert fourth.child_live_domain_action == "advance_tick"
        assert fourth.adapted_experiment_interval > 3
        snap4 = snapshots(runtime_root)
        section4 = snap4["regret_bundle"]["sections"][0]
        assert section4["cycle_count"] == 4
        assert section4["positive_regret_count"] >= 1
        assert section4["exploit_alternative_count"] >= 1
        assert section4["exploit_regret_credit"] > 0.0
        assert snap4["regret_state"]["total_cycles"] == 4
        assert snap4["regret_state"]["total_experiment_children"] == 1
        assert snap4["regret_state"]["total_reobserve_children"] == 1
        assert snap4["regret_state"]["total_exploit_children"] == 2
        assert snap4["regret_state"]["counterfactual_truth_promotion_count"] == 0
        assert snap4["regret_state"]["shadow_execution_count"] == 0
        assert snap4["regret_state"]["hard_gate_bypass_count"] == 0
        assert snap4["regret_bundle"]["generation"] == 4
        assert len(snap4["regret_bundle"]["outcomes"]) == 4
        assert len(snap4["regret_bundle"]["regret_holonomy"]) == 4
        assert len(snap4["regret_bundle"]["processed_policy_outcome_digests"]) == 4
        assert snap4["experiment_bundle"]["total_trial_count"] == 1
        assert snap4["experiment_bundle"]["total_exploit_count"] == 3
        assert snap4["experiment_bundle"]["trial_budget_spent"] == 0.2
        assert snap4["policy_state"]["total_cycles"] == 4
        assert snap4["policy_state"]["total_experiment_policy_cycles"] == 1
        assert snap4["policy_state"]["total_reobserve_policy_cycles"] == 1
        assert snap4["policy_state"]["total_exploit_policy_cycles"] == 2
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 5
        assert read(runtime_root / "runtime_state.json")["tick"] == 4
        assert source_portfolio_path.read_bytes() == source_portfolio_bytes
        no_graph(snap4["regret_bundle"])

        stale_sources = [source("regret-stale")]
        stale_plan = plan(
            "regret-stale",
            stale_sources,
            root,
            adapter_registry,
            snap4["capability_state"]["capability_state_digest"],
            snap4["capability_bundle"]["capability_bundle_digest"],
            source_portfolio_digest,
            snap4["experiment_state"]["experiment_state_digest"],
            snap4["experiment_bundle"]["experiment_bundle_digest"],
            snap4["policy_state"]["policy_state_digest"],
            snap4["policy_bundle"]["policy_bundle_digest"],
            snap4["regret_state"]["regret_state_digest"],
            regret0["regret_bundle_digest"],
        )
        before_rows = len(jsonl(runtime_root / "execution_ledger.jsonl"))
        before_generation = snap4["regret_bundle"]["generation"]
        stale = build_policy_regret_cadence(
            runtime_context=regret_context(runtime_root),
            source_packets=stale_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            regret_plan=stale_plan,
            regret_license=license_packet(
                stale_plan,
                stale_sources,
                root,
                adapter_registry,
                snap4["capability_bundle"]["capability_bundle_digest"],
                source_portfolio_digest,
                snap4["experiment_bundle"]["experiment_bundle_digest"],
                snap4["policy_bundle"]["policy_bundle_digest"],
                regret0["regret_bundle_digest"],
            ),
        )
        assert stale.status == BLOCKED
        assert (
            "regret_plan_expected_previous_regret_bundle_digest_mismatch"
            in stale.blockers
        )
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before_rows
        assert read(
            runtime_root / "kuuos_policy_regret_cadence_bundle_v0_10.json"
        )["generation"] == before_generation

        committed = [
            row
            for row in jsonl(
                runtime_root / "kuuos_policy_regret_cadence_ledger_v0_10.jsonl"
            )
            if row.get("phase") == "committed"
        ]
        assert len(committed) == 4
        assert [row["child_policy_mode"] for row in committed] == [
            "experiment",
            "reobserve",
            "exploit",
            "exploit",
        ]
        assert [row["child_live_domain_action"] for row in committed] == [
            "advance_tick",
            "observe",
            "advance_tick",
            "advance_tick",
        ]

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/PolicyRegretCadenceV0_10.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "confidenceDiscountedRegret",
        "adaptThresholdBounded",
        "adaptIntervalBounded",
        "regret_nonnegative",
        "threshold_lower_bound",
        "onePolicyChild",
    ):
        assert token in formal

    manifest = read(ROOT / "manifests/kuuos_policy_regret_cadence_v0_10.json")
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS policy regret cadence v0.10 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
