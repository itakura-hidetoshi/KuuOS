#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_adapter_portfolio_shadow_core_v0_7 import (  # noqa: E402
    build_adapter_portfolio_shadow,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (  # noqa: E402
    BLOCKED,
    READY,
    REPLAYED,
)
from scripts.adapter_portfolio_shadow_v0_7_test_support import (  # noqa: E402
    capability_bundle_digest,
    license_packet,
    plan,
    portfolio_bundle_digest,
    portfolio_context,
    registry,
    root_packet,
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


def execute(
    runtime_root,
    run_id,
    sources,
    root,
    adapter_registry,
    previous_capability_state_digest,
    previous_capability_bundle_digest,
    previous_portfolio_state_digest,
    previous_portfolio_bundle_digest,
):
    packet = plan(
        run_id,
        sources,
        root,
        adapter_registry,
        previous_capability_state_digest,
        previous_capability_bundle_digest,
        previous_portfolio_state_digest,
        previous_portfolio_bundle_digest,
    )
    result = build_adapter_portfolio_shadow(
        runtime_context=portfolio_context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=adapter_registry,
        portfolio_plan=packet,
        portfolio_license=license_packet(
            packet,
            sources,
            root,
            adapter_registry,
            previous_capability_bundle_digest,
            previous_portfolio_bundle_digest,
        ),
    )
    return packet, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        adapter_registry = registry()

        sources1 = [source("portfolio-event-001")]
        plan1, first = execute(
            runtime_root,
            "portfolio-001",
            sources1,
            root,
            adapter_registry,
            "",
            capability_bundle_digest(),
            "",
            portfolio_bundle_digest(),
        )
        assert first.status == READY, first.blockers
        assert first.live_adapter_id == "adapter-a"
        assert first.shadow_projection_count == 1
        assert first.resolved_shadow_count == 0
        assert first.pending_shadow_count == 1
        assert first.child_capability_run_id == "portfolio-001:capability"
        assert first.child_capability_status
        selection1 = read(runtime_root / "kuuos_adapter_portfolio_selection_v0_7.json")
        projection1 = read(runtime_root / "kuuos_adapter_shadow_projection_v0_7.json")
        resolution1 = read(runtime_root / "kuuos_adapter_shadow_resolution_v0_7.json")
        bundle1 = read(runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json")
        portfolio_state1 = read(runtime_root / "kuuos_adapter_portfolio_state_v0_7.json")
        capability_state1 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        capability_bundle1 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        assert selection1["live_adapter_id"] == "adapter-a"
        assert selection1["shadow_candidates"] == ["adapter-b"]
        assert projection1["projection_count"] == 1
        assert projection1["projections"][0]["federation_adapter_id"] == "adapter-b"
        assert projection1["projections"][0]["shadow_non_actuating"] is True
        assert projection1["projections"][0]["shadow_prediction_not_truth"] is True
        assert projection1["projections"][0]["shadow_prediction_not_capability_evidence"] is True
        assert resolution1["resolved"] is False
        assert bundle1["generation"] == 1
        assert len(bundle1["pending_predictions"]) == 1
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 1
        assert read(runtime_root / "runtime_state.json")["tick"] == 0

        replay = build_adapter_portfolio_shadow(
            runtime_context=portfolio_context(runtime_root),
            source_packets=sources1,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            portfolio_plan=plan1,
            portfolio_license=license_packet(
                plan1,
                sources1,
                root,
                adapter_registry,
                capability_bundle_digest(),
                portfolio_bundle_digest(),
            ),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 1
        assert read(runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json")["generation"] == 1

        sources2 = [source("portfolio-event-002")]
        _, second = execute(
            runtime_root,
            "portfolio-002",
            sources2,
            root,
            adapter_registry,
            capability_state1["capability_state_digest"],
            capability_bundle1["capability_bundle_digest"],
            portfolio_state1["portfolio_state_digest"],
            bundle1["portfolio_bundle_digest"],
        )
        assert second.status == READY, second.blockers
        assert second.live_adapter_id == "adapter-b"
        assert second.shadow_projection_count == 1
        bundle2 = read(runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json")
        portfolio_state2 = read(runtime_root / "kuuos_adapter_portfolio_state_v0_7.json")
        capability_state2 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        capability_bundle2 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        resolution2 = read(runtime_root / "kuuos_adapter_shadow_resolution_v0_7.json")
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 2
        assert read(runtime_root / "runtime_state.json")["tick"] == 1
        assert bundle2["generation"] == 2
        assert len(bundle2["portfolio_holonomy"]) == 2
        assert len(bundle2["processed_live_effect_digests"]) == 2
        assert all(item["shadow_non_actuating"] for item in bundle2["pending_predictions"])
        if resolution2["resolved"]:
            assert resolution2["live_adapter_id"] == "adapter-b"
            assert resolution2["resolved_prediction_id"]
            assert len(bundle2["resolved_predictions"]) == 1
            section_b = next(
                item for item in bundle2["sections"]
                if item["federation_adapter_id"] == "adapter-b"
                and item["context_key"] == second.context_key
            )
            assert section_b["resolved_shadow_count"] == 1
            assert section_b["reliability"] > 0.0

        sources3 = [source("portfolio-event-003")]
        _, third = execute(
            runtime_root,
            "portfolio-003",
            sources3,
            root,
            adapter_registry,
            capability_state2["capability_state_digest"],
            capability_bundle2["capability_bundle_digest"],
            portfolio_state2["portfolio_state_digest"],
            bundle2["portfolio_bundle_digest"],
        )
        assert third.status == READY, third.blockers
        assert third.live_adapter_id == "adapter-b"
        assert third.shadow_projection_count == 1
        selection3 = read(runtime_root / "kuuos_adapter_portfolio_selection_v0_7.json")
        bundle3 = read(runtime_root / "kuuos_adapter_portfolio_bundle_v0_7.json")
        state3 = read(runtime_root / "kuuos_adapter_portfolio_state_v0_7.json")
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == 3
        assert read(runtime_root / "runtime_state.json")["tick"] == 2
        assert state3["total_live_cycles"] == 3
        assert state3["total_shadow_projections"] == 3
        assert state3["shadow_execution_count"] == 0
        assert bundle3["generation"] == 3
        assert len(bundle3["processed_live_effect_digests"]) == 3
        candidate_b = next(
            item for item in selection3["candidates"]
            if item["federation_adapter_id"] == "adapter-b"
        )
        if resolution2["resolved"]:
            assert candidate_b["resolved_shadow_count"] == 1
            assert candidate_b["portfolio_reliability"] > 0.0
        no_graph(bundle3)

        stale_sources = [source("portfolio-event-stale")]
        stale_plan = plan(
            "portfolio-stale",
            stale_sources,
            root,
            adapter_registry,
            read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")["capability_state_digest"],
            capability_bundle_digest(),
            state3["portfolio_state_digest"],
            portfolio_bundle_digest(),
        )
        stale = build_adapter_portfolio_shadow(
            runtime_context=portfolio_context(runtime_root),
            source_packets=stale_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            portfolio_plan=stale_plan,
            portfolio_license=license_packet(
                stale_plan,
                stale_sources,
                root,
                adapter_registry,
                capability_bundle_digest(),
                portfolio_bundle_digest(),
            ),
        )
        assert stale.status == BLOCKED
        assert "portfolio_plan_expected_previous_capability_bundle_digest_mismatch" in stale.blockers
        assert "portfolio_plan_expected_previous_portfolio_bundle_digest_mismatch" in stale.blockers

        committed = [
            row for row in jsonl(runtime_root / "kuuos_adapter_portfolio_ledger_v0_7.jsonl")
            if row.get("phase") == "committed"
        ]
        assert len(committed) == 3
        assert [row["live_adapter_id"] for row in committed] == [
            "adapter-a", "adapter-b", "adapter-b"
        ]

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/AdapterPortfolioShadowV0_7.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "ShadowPrediction",
        "realizationError",
        "resolveBias",
        "shadow_non_actuation",
        "boundedPortfolioAdjustment",
        "oneLiveAdapter",
    ):
        assert token in formal

    manifest = read(ROOT / "manifests/kuuos_adapter_portfolio_shadow_v0_7.json")
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS adapter portfolio shadow v0.7 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
