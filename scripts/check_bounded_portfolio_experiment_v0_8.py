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
from runtime.kuuos_bounded_portfolio_experiment_core_v0_8 import (  # noqa: E402
    build_bounded_portfolio_experiment,
)
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (  # noqa: E402
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
    experiment_context,
    experiment_registry,
    initial_experiment_bundle,
    initial_portfolio_digest,
    license_packet,
    plan,
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
    )
    result = build_bounded_portfolio_experiment(
        runtime_context=experiment_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=adapter_registry,
        experiment_plan=packet,
        experiment_license=license_packet(
            packet,
            sources,
            root,
            adapter_registry,
            previous_capability_bundle_digest,
            source_portfolio_bundle_digest,
            previous_experiment_bundle_digest,
        ),
    )
    return packet, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        adapter_registry = experiment_registry()

        seed_sources = [source("experiment-seed-001")]
        seed_plan = portfolio_plan(
            "portfolio-seed-001",
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
        source_portfolio = read(
            runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json"
        )
        source_portfolio_digest = source_portfolio["portfolio_bundle_digest"]
        source_portfolio_bytes = (
            runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json"
        ).read_bytes()
        capability_state_seed = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle_seed = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert len(source_portfolio["pending_predictions"]) == 1
        assert source_portfolio["pending_predictions"][0][
            "federation_adapter_id"
        ] == "adapter-b"
        initial_experiment = initial_experiment_bundle(source_portfolio)

        sources1 = [source("experiment-event-001")]
        plan1, first = execute(
            runtime_root,
            "experiment-001",
            sources1,
            root,
            adapter_registry,
            capability_state_seed["capability_state_digest"],
            capability_bundle_seed["capability_bundle_digest"],
            source_portfolio_digest,
            "",
            initial_experiment["experiment_bundle_digest"],
        )
        assert first.status == READY, first.blockers
        assert first.decision_mode == "licensed_experiment"
        assert first.baseline_adapter_id == "adapter-a"
        assert first.live_adapter_id == "adapter-b"
        assert first.experiment_adapter_id == "adapter-b"
        assert first.expected_information_gain >= 0.5
        assert first.trial_cost == 0.2
        assert first.trial_budget_before == 1.0
        assert first.trial_budget_after == 0.8
        assert first.total_trial_count == 1
        assert first.total_exploit_count == 0
        assert first.shadow_projection_count == 1
        assert first.resolved_shadow_count == 1
        assert first.child_capability_run_id == "experiment-001:capability"
        decision1 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_decision_v0_8.json"
        )
        trial1 = read(runtime_root / "kuuos_bounded_portfolio_trial_record_v0_8.json")
        bundle1 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        state1 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        )
        capability_state1 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle1 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert decision1["candidate_experiments"][0]["eligible_for_trial"] is True
        assert trial1["trial_debited_after_live_effect"] is True
        assert trial1["shadow_execution_count"] == 0
        assert bundle1["source_portfolio_bundle_digest"] == source_portfolio_digest
        assert bundle1["trial_budget_spent"] == 0.2
        assert bundle1["total_trial_count"] == 1
        assert len(bundle1["trial_records"]) == 1
        assert len(bundle1["processed_experiment_effect_digests"]) == 1
        assert (
            runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json"
        ).read_bytes() == source_portfolio_bytes
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(runtime_root / "runtime_state.json")["tick"] == 2

        replay = build_bounded_portfolio_experiment(
            runtime_context=experiment_context(runtime_root),
            source_packets=sources1,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            experiment_plan=plan1,
            experiment_license=license_packet(
                plan1,
                sources1,
                root,
                adapter_registry,
                capability_bundle_seed["capability_bundle_digest"],
                source_portfolio_digest,
                initial_experiment["experiment_bundle_digest"],
            ),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )["trial_budget_spent"] == 0.2

        sources2 = [source("experiment-event-002")]
        _, second = execute(
            runtime_root,
            "experiment-002",
            sources2,
            root,
            adapter_registry,
            capability_state1["capability_state_digest"],
            capability_bundle1["capability_bundle_digest"],
            source_portfolio_digest,
            state1["experiment_state_digest"],
            bundle1["experiment_bundle_digest"],
        )
        assert second.status == READY, second.blockers
        assert second.decision_mode == "exploit_baseline"
        assert second.baseline_adapter_id == "adapter-a"
        assert second.live_adapter_id == "adapter-a"
        assert second.experiment_adapter_id == ""
        assert second.trial_cost == 0.0
        assert second.trial_budget_before == 0.8
        assert second.trial_budget_after == 0.8
        assert second.total_trial_count == 1
        assert second.total_exploit_count == 1
        assert second.resolved_shadow_count == 1
        decision2 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_decision_v0_8.json"
        )
        candidate_b2 = next(
            item
            for item in decision2["candidate_experiments"]
            if item["federation_adapter_id"] == "adapter-b"
        )
        assert candidate_b2["eligible_for_trial"] is False
        assert "global_trial_count_exhausted" in candidate_b2["ineligibility_reasons"]
        bundle2 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        state2 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        )
        capability_state2 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle2 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert bundle2["trial_budget_spent"] == 0.2
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 3
        assert read(runtime_root / "runtime_state.json")["tick"] == 3

        sources3 = [source("experiment-event-003")]
        _, third = execute(
            runtime_root,
            "experiment-003",
            sources3,
            root,
            adapter_registry,
            capability_state2["capability_state_digest"],
            capability_bundle2["capability_bundle_digest"],
            source_portfolio_digest,
            state2["experiment_state_digest"],
            bundle2["experiment_bundle_digest"],
        )
        assert third.status == READY, third.blockers
        assert third.decision_mode == "exploit_baseline"
        assert third.live_adapter_id == "adapter-a"
        assert third.total_trial_count == 1
        assert third.total_exploit_count == 2
        assert third.trial_budget_after == 0.8
        bundle3 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )
        state3 = read(
            runtime_root / "kuuos_bounded_portfolio_experiment_state_v0_8.json"
        )
        capability_state3 = read(
            runtime_root / "kuuos_adapter_capability_state_v0_6.json"
        )
        capability_bundle3 = read(
            runtime_root / "kuuos_adapter_capability_bundle_v0_6.json"
        )
        assert state3["total_cycles"] == 3
        assert state3["total_trial_count"] == 1
        assert state3["total_exploit_count"] == 2
        assert state3["shadow_execution_count"] == 0
        assert state3["multiple_live_adapter_count"] == 0
        assert bundle3["generation"] == 3
        assert bundle3["trial_budget_spent"] == 0.2
        assert len(bundle3["trial_records"]) == 3
        assert len(bundle3["decision_holonomy"]) == 3
        assert len(bundle3["processed_experiment_effect_digests"]) == 3
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 4
        assert read(runtime_root / "runtime_state.json")["tick"] == 4
        assert (
            runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json"
        ).read_bytes() == source_portfolio_bytes
        no_graph(bundle3)

        stale_sources = [source("experiment-stale")]
        stale_plan = plan(
            "experiment-stale",
            stale_sources,
            root,
            adapter_registry,
            capability_state3["capability_state_digest"],
            capability_bundle3["capability_bundle_digest"],
            source_portfolio_digest,
            state3["experiment_state_digest"],
            initial_experiment["experiment_bundle_digest"],
        )
        before_ledger_count = len(jsonl(runtime_root / "execution_ledger.jsonl"))
        before_budget = bundle3["trial_budget_spent"]
        stale = build_bounded_portfolio_experiment(
            runtime_context=experiment_context(runtime_root),
            source_packets=stale_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            experiment_plan=stale_plan,
            experiment_license=license_packet(
                stale_plan,
                stale_sources,
                root,
                adapter_registry,
                capability_bundle3["capability_bundle_digest"],
                source_portfolio_digest,
                initial_experiment["experiment_bundle_digest"],
            ),
        )
        assert stale.status == BLOCKED
        assert (
            "experiment_plan_expected_previous_experiment_bundle_digest_mismatch"
            in stale.blockers
        )
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before_ledger_count
        assert read(
            runtime_root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json"
        )["trial_budget_spent"] == before_budget

        committed = [
            row
            for row in jsonl(
                runtime_root / "kuuos_bounded_portfolio_experiment_ledger_v0_8.jsonl"
            )
            if row.get("phase") == "committed"
        ]
        assert len(committed) == 3
        assert [row["decision_mode"] for row in committed] == [
            "licensed_experiment",
            "exploit_baseline",
            "exploit_baseline",
        ]
        assert [row["live_adapter_id"] for row in committed] == [
            "adapter-b",
            "adapter-a",
            "adapter-a",
        ]

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/BoundedPortfolioExperimentV0_8.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "expectedInformationGain",
        "eligibleTrial",
        "debitBudget",
        "budgetDebit_monotone",
        "oneLiveAdapter",
        "shadow_non_actuation",
    ):
        assert token in formal

    manifest = read(
        ROOT / "manifests/kuuos_bounded_portfolio_experiment_v0_8.json"
    )
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS bounded portfolio experiment v0.8 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
