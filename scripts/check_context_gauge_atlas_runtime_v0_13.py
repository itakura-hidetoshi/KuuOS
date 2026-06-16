#!/usr/bin/env python3
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.kuuos_context_gauge_atlas_core_v0_13 import build_context_gauge_atlas
from scripts.context_gauge_atlas_v0_13_runner import execute, seed_current, snapshots
from scripts.context_gauge_atlas_v0_13_test_support import atlas_context, experiment_registry, initial_atlas, license_packet, root_packet, source_for
from scripts.delayed_credit_multihorizon_v0_11_runner import jsonl


def main():
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        registry = experiment_registry()
        seed_result, portfolio, current = seed_current(runtime_root, root, registry)
        assert seed_result.live_adapter_id == "adapter-a"
        sources_a = [source_for("atlas-a-001", "sensor-a")]
        plan_a, first = execute(runtime_root, "atlas-001", sources_a, root, registry, current)
        assert first.status.endswith("READY"), first.blockers
        assert first.atlas_class == "isolated_chart"
        assert first.compatible_chart_count == 0
        snap1 = snapshots(runtime_root, portfolio)
        assert snap1["atlas_bundle"]["generation"] == 1
        assert len(snap1["atlas_bundle"]["charts"]) == 1
        rows = len(jsonl(runtime_root / "execution_ledger.jsonl"))
        replay = build_context_gauge_atlas(runtime_context=atlas_context(runtime_root), source_packets=sources_a, root_principles_packet=root, adapter_registry=registry, atlas_plan=plan_a, atlas_license=license_packet(plan_a, sources_a, root, registry, current))
        assert replay.status.endswith("REPLAYED")
        assert replay.idempotent_replay is True
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == rows
        sources_b = [source_for("atlas-b-001", "sensor-b")]
        _, second = execute(runtime_root, "atlas-002", sources_b, root, registry, snap1)
        assert second.status.endswith("READY"), second.blockers
        assert second.compatible_chart_count == 1
        assert second.atlas_class in {"compatible_chart_transport", "plural_atlas_transport"}
        assert second.cocycle_defect > 0.0
        weights = [second.transported_short_weight, second.transported_medium_weight, second.transported_long_weight]
        assert abs(sum(weights) - 1.0) < 1e-5
        assert min(weights) >= 0.12
        snap2 = snapshots(runtime_root, portfolio)
        assert snap2["atlas_bundle"]["generation"] == 2
        assert len(snap2["atlas_bundle"]["charts"]) == 2
        assert len(snap2["atlas_bundle"]["atlas_holonomy"]) == 2
        assert snap2["atlas_state"]["total_cycles"] == 2
        assert snap2["atlas_state"]["total_transitions"] == 1
        stale = dict(snap2)
        stale["atlas_bundle"] = initial_atlas()
        before = len(jsonl(runtime_root / "execution_ledger.jsonl"))
        _, blocked = execute(runtime_root, "atlas-stale", [source_for("atlas-c-001", "sensor-c")], root, registry, stale)
        assert blocked.status.endswith("BLOCKED")
        assert "atlas_plan_expected_previous_atlas_bundle_digest_mismatch" in blocked.blockers
        assert len(jsonl(runtime_root / "execution_ledger.jsonl")) == before
        text = repr(snap2["atlas_bundle"]).lower()
        for token in ("'nodes'", "'edges'", "'graph'", "'dependencies'"):
            assert token not in text
    print("PASS: context gauge atlas v0.13 runtime")


if __name__ == "__main__":
    main()
