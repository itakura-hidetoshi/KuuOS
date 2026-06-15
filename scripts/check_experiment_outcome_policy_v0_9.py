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
from runtime.kuuos_experiment_outcome_policy_core_v0_9 import (  # noqa: E402
    build_experiment_outcome_policy,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (  # noqa: E402
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
from scripts.experiment_outcome_policy_v0_9_test_support import (  # noqa: E402
    experiment_registry,
    initial_experiment,
    initial_policy,
    license_packet,
    plan,
    policy_context,
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
    )
    result = build_experiment_outcome_policy(
        runtime_context=policy_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=adapter_registry,
        policy_plan=packet,
        policy_license=license_packet(
            packet,
            sources,
            root,
            adapter_registry,
            previous_capability_bundle_digest,
            source_portfolio_bundle_digest,
            previous_experiment_bundle_digest,
            previous_policy_bundle_digest,
        ),
    )
    return packet, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        adapter_registry = experiment_registry()

        seed_sources = [source("policy-seed-001")]
        seed_plan = portfolio_plan(
            "policy-portfolio-seed-001",
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

        sources1 = [source("policy-event-001")]
        plan1, first = execute(
            runtime_root,
            "policy-001",
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
        )
        assert first.status == READY, first.blockers
        assert first.policy_mode == "experiment"
        assert first.preview_baseline_adapter_id == "adapter-a"
        assert first.preview_experiment_adapter_id == "adapter-b"
        assert first.child_decision_mode == "licensed_experiment"
        assert first.child_live_adapter_id == "adapter-b"
        assert first.experiment_pressure >= 0.6
        assert 0.35 <= first.adapted_minimum_information_gain <= 0.5
        assert first.live_domain_action == "advance_tick"
        assert first.compatible_shadow_resolved is False
        assert first.posterior_experiment_success > 0.5
        assert first.mean_net_experiment_value > 0.35
        decision1 = read(
            runtime_root / "kuuos_experiment_outcome_policy_decision_v0_9.json"
        )
        outcome1 = read(
            runtime_root / "kuuos_experiment_outcome_policy_outcome_v0_9.json"
        )
        bundle1 = read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        )
        state1 = read(
            runtime_root / "kuuos_experiment_outcome_policy_state_v0_9.json"
        )
        experiment_bundle1 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        experiment_state1 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        )
        capability_state1 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle1 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        child_plan1 = read(
            runtime_root / "kuuos_experiment_outcome_policy_child_plan_v0_9.json"
        )
        assert decision1["policy_reason"] == "posterior_and_information_gain_support_trial"
        assert child_plan1["max_live_trials_total"] == 4
        assert child_plan1["minimum_information_gain"] <= 0.5
        assert outcome1["experiment_outcome_success"] is True
        assert experiment_bundle1["total_trial_count"] == 1
        assert experiment_bundle1["trial_budget_spent"] == 0.2
        assert bundle1["generation"] == 1
        section1 = bundle1["sections"][0]
        assert section1["experiment_count"] == 1
        assert section1["experiment_success_alpha"] == 2.0
        assert section1["experiment_success_beta"] == 1.0
        assert section1["last_compatible_shadow_resolved"] is False
        assert source_portfolio_path.read_bytes() == source_portfolio_bytes
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(runtime_root / "runtime_state.json")["tick"] == 2

        replay = build_experiment_outcome_policy(
            runtime_context=policy_context(runtime_root),
            source_packets=sources1,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            policy_plan=plan1,
            policy_license=license_packet(
                plan1,
                sources1,
                root,
                adapter_registry,
                capability_bundle0["capability_bundle_digest"],
                source_portfolio_digest,
                experiment0["experiment_bundle_digest"],
                policy0["policy_bundle_digest"],
            ),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        )["generation"] == 1
        assert read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )["trial_budget_spent"] == 0.2

        sources2 = [source("policy-event-002")]
        _, second = execute(
            runtime_root,
            "policy-002",
            sources2,
            root,
            adapter_registry,
            capability_state1["capability_state_digest"],
            capability_bundle1["capability_bundle_digest"],
            source_portfolio_digest,
            experiment_state1["experiment_state_digest"],
            experiment_bundle1["experiment_bundle_digest"],
            state1["policy_state_digest"],
            bundle1["policy_bundle_digest"],
        )
        assert second.status == READY, second.blockers
        assert second.policy_mode == "reobserve"
        assert second.policy_reason == "post_experiment_resolution_debt"
        assert second.child_decision_mode == "exploit_baseline"
        assert second.live_domain_action == "observe"
        assert second.reobserve_pressure >= 0.65
        decision2 = read(
            runtime_root / "kuuos_experiment_outcome_policy_decision_v0_9.json"
        )
        child_plan2 = read(
            runtime_root / "kuuos_experiment_outcome_policy_child_plan_v0_9.json"
        )
        child_registry2 = read(
            runtime_root / "kuuos_experiment_outcome_policy_child_registry_v0_9.json"
        )
        bundle2 = read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        )
        state2 = read(
            runtime_root / "kuuos_experiment_outcome_policy_state_v0_9.json"
        )
        experiment_bundle2 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        experiment_state2 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        )
        capability_state2 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle2 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert decision2["child_live_trial_enabled"] is False
        assert decision2["child_reobserve_routing_enabled"] is True
        assert child_plan2["max_live_trials_total"] == 1
        assert child_plan2["minimum_information_gain"] == 1.0
        assert all(
            set(item["capability_routing_table"].values()) == {"observe"}
            for item in child_registry2["adapters"]
        )
        assert experiment_bundle2["total_trial_count"] == 1
        assert experiment_bundle2["trial_budget_spent"] == 0.2
        section2 = bundle2["sections"][0]
        assert section2["reobserve_count"] == 1
        assert section2["last_live_domain_action"] == "observe"
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 3
        assert read(runtime_root / "runtime_state.json")["tick"] == 2

        sources3 = [source("policy-event-003")]
        _, third = execute(
            runtime_root,
            "policy-003",
            sources3,
            root,
            adapter_registry,
            capability_state2["capability_state_digest"],
            capability_bundle2["capability_bundle_digest"],
            source_portfolio_digest,
            experiment_state2["experiment_state_digest"],
            experiment_bundle2["experiment_bundle_digest"],
            state2["policy_state_digest"],
            bundle2["policy_bundle_digest"],
        )
        assert third.status == READY, third.blockers
        assert third.policy_mode == "exploit"
        assert third.child_decision_mode == "exploit_baseline"
        assert third.live_domain_action == "advance_tick"
        child_plan3 = read(
            runtime_root / "kuuos_experiment_outcome_policy_child_plan_v0_9.json"
        )
        child_registry3 = read(
            runtime_root / "kuuos_experiment_outcome_policy_child_registry_v0_9.json"
        )
        bundle3 = read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        )
        state3 = read(
            runtime_root / "kuuos_experiment_outcome_policy_state_v0_9.json"
        )
        experiment_bundle3 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        capability_state3 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle3 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert child_plan3["max_live_trials_total"] == 1
        assert child_plan3["minimum_information_gain"] == 1.0
        assert all(
            item["policy_reobserve_routing"] is False
            for item in child_registry3["adapters"]
        )
        section3 = bundle3["sections"][0]
        assert section3["cycle_count"] == 3
        assert section3["experiment_count"] == 1
        assert section3["reobserve_count"] == 1
        assert section3["exploit_count"] == 1
        assert section3["experiment_success_alpha"] == 2.0
        assert section3["experiment_success_beta"] == 1.0
        assert state3["total_cycles"] == 3
        assert state3["total_experiment_policy_cycles"] == 1
        assert state3["total_reobserve_policy_cycles"] == 1
        assert state3["total_exploit_policy_cycles"] == 1
        assert state3["shadow_execution_count"] == 0
        assert state3["hard_gate_bypass_count"] == 0
        assert bundle3["generation"] == 3
        assert len(bundle3["outcomes"]) == 3
        assert len(bundle3["policy_holonomy"]) == 3
        assert len(bundle3["processed_child_effect_digests"]) == 3
        assert experiment_bundle3["total_trial_count"] == 1
        assert experiment_bundle3["total_exploit_count"] == 2
        assert experiment_bundle3["trial_budget_spent"] == 0.2
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 4
        assert read(runtime_root / "runtime_state.json")["tick"] == 3
        assert source_portfolio_path.read_bytes() == source_portfolio_bytes
        no_graph(bundle3)

        stale_sources = [source("policy-stale")]
        stale_plan = plan(
            "policy-stale",
            stale_sources,
            root,
            adapter_registry,
            capability_state3["capability_state_digest"],
            capability_bundle3["capability_bundle_digest"],
            source_portfolio_digest,
            read(
                runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
            )["experiment_state_digest"],
            experiment_bundle3["experiment_bundle_digest"],
            state3["policy_state_digest"],
            policy0["policy_bundle_digest"],
        )
        before_execution_rows = len(jsonl(runtime_root / "execution_ledger.jsonl"))
        before_generation = bundle3["generation"]
        stale = build_experiment_outcome_policy(
            runtime_context=policy_context(runtime_root),
            source_packets=stale_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            policy_plan=stale_plan,
            policy_license=license_packet(
                stale_plan,
                stale_sources,
                root,
                adapter_registry,
                capability_bundle3["capability_bundle_digest"],
                source_portfolio_digest,
                experiment_bundle3["experiment_bundle_digest"],
                policy0["policy_bundle_digest"],
            ),
        )
        assert stale.status == BLOCKED
        assert (
            "policy_plan_expected_previous_policy_bundle_digest_mismatch"
            in stale.blockers
        )
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before_execution_rows
        assert read(
            runtime_root / "kuuos_experiment_outcome_policy_bundle_v0_9.json"
        )["generation"] == before_generation

        committed = [
            row
            for row in jsonl(
                runtime_root / "kuuos_experiment_outcome_policy_ledger_v0_9.jsonl"
            )
            if row.get("phase") == "committed"
        ]
        assert len(committed) == 3
        assert [row["policy_mode"] for row in committed] == [
            "experiment",
            "reobserve",
            "exploit",
        ]
        assert [row["live_domain_action"] for row in committed] == [
            "advance_tick",
            "observe",
            "advance_tick",
        ]

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/ExperimentOutcomePolicyV0_9.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "posteriorSuccess",
        "netExperimentValue",
        "adaptThreshold",
        "hardFloor_preserved",
        "PolicyMode",
        "oneChildCycle",
    ):
        assert token in formal

    manifest = read(
        ROOT / "manifests/kuuos_experiment_outcome_policy_v0_9.json"
    )
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS experiment outcome policy v0.9 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
