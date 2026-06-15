#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_adapter_capability_gauge_core_v0_6 import (  # noqa: E402
    build_adapter_capability_gauge,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (  # noqa: E402
    BLOCKED,
    READY,
    REPLAYED,
)
from scripts.adapter_capability_v0_6_test_support import (  # noqa: E402
    context,
    initial_bundle_digest,
    license_packet,
    plan,
    registry,
    root_packet,
    source,
)


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


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
    runtime_root: pathlib.Path,
    run_id: str,
    sources,
    root,
    adapter_registry,
    previous_state_digest: str,
    previous_bundle_digest: str,
):
    packet = plan(
        run_id,
        sources,
        root,
        adapter_registry,
        previous_state_digest,
        previous_bundle_digest,
    )
    result = build_adapter_capability_gauge(
        runtime_context=context(runtime_root),
        source_packets=sources,
        root_principles_packet=root,
        adapter_registry=adapter_registry,
        capability_plan=packet,
        capability_license=license_packet(
            packet,
            sources,
            root,
            adapter_registry,
            previous_bundle_digest,
        ),
    )
    return packet, result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        adapter_registry = registry()

        sources1 = [source("event-001")]
        plan1, first = execute(
            runtime_root,
            "capability-001",
            sources1,
            root,
            adapter_registry,
            "",
            initial_bundle_digest(),
        )
        assert first.status == READY, first.blockers
        assert first.selected_federation_adapter_id == "adapter-a"
        assert first.child_federation_run_id == "capability-001:federation"
        assert first.prior_connection == 0.72
        assert first.capability_curvature < 0.0
        assert first.updated_connection < first.prior_connection
        assert first.observation_count == 1
        state1 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        bundle1 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        selection1 = read(runtime_root / "kuuos_adapter_capability_selection_v0_6.json")
        calibration1 = read(runtime_root / "kuuos_adapter_capability_calibration_v0_6.json")
        assert bundle1["generation"] == 1
        assert len(bundle1["holonomy_trace"]) == 1
        assert selection1["static_priority_used_only_as_tie_break"] is True
        assert calibration1["outcome"] == "blocked"
        runtime_state1 = read(runtime_root / "runtime_state.json")
        assert runtime_state1["held"] is True
        assert runtime_state1["tick"] == 0

        replay = build_adapter_capability_gauge(
            runtime_context=context(runtime_root),
            source_packets=sources1,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            capability_plan=plan1,
            capability_license=license_packet(
                plan1,
                sources1,
                root,
                adapter_registry,
                initial_bundle_digest(),
            ),
        )
        assert replay.status == REPLAYED
        assert replay.idempotent_replay is True
        assert read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")[
            "generation"
        ] == 1
        assert read(runtime_root / "runtime_state.json")["tick"] == 0

        sources2 = [source("event-002")]
        _, second = execute(
            runtime_root,
            "capability-002",
            sources2,
            root,
            adapter_registry,
            state1["capability_state_digest"],
            bundle1["capability_bundle_digest"],
        )
        assert second.status == READY, second.blockers
        assert second.selected_federation_adapter_id == "adapter-b"
        assert second.prior_connection == 0.55
        assert second.capability_curvature > 0.0
        assert second.updated_connection > second.prior_connection
        assert second.observation_count == 1
        assert read(runtime_root / "runtime_state.json")["tick"] == 1
        state2 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        bundle2 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        selection2 = read(runtime_root / "kuuos_adapter_capability_selection_v0_6.json")
        assert selection2["candidates"][0]["federation_adapter_id"] == "adapter-b"
        assert bundle2["generation"] == 2
        assert len(bundle2["sections"]) == 2
        assert len(bundle2["holonomy_trace"]) == 2

        sources3 = [source("event-003")]
        _, third = execute(
            runtime_root,
            "capability-003",
            sources3,
            root,
            adapter_registry,
            state2["capability_state_digest"],
            bundle2["capability_bundle_digest"],
        )
        assert third.status == READY, third.blockers
        assert third.selected_federation_adapter_id == "adapter-b"
        assert third.observation_count == 2
        assert read(runtime_root / "runtime_state.json")["tick"] == 2
        state3 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        bundle3 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        sections3 = {
            (item["federation_adapter_id"], item["context_key"]): item
            for item in bundle3["sections"]
        }
        observation_context = third.context_key
        assert sections3[("adapter-b", observation_context)]["observation_count"] == 2
        assert sections3[("adapter-a", observation_context)]["observation_count"] == 1
        assert bundle3["generation"] == 3
        assert len(bundle3["processed_evidence_digests"]) == 3

        sources4 = [source("event-004", "resource_change")]
        _, fourth = execute(
            runtime_root,
            "capability-004",
            sources4,
            root,
            adapter_registry,
            state3["capability_state_digest"],
            bundle3["capability_bundle_digest"],
        )
        assert fourth.status == READY, fourth.blockers
        assert fourth.context_key != observation_context
        assert fourth.selected_federation_adapter_id == "adapter-a"
        assert fourth.prior_connection == 0.72
        assert fourth.observation_count == 1
        assert read(runtime_root / "runtime_state.json")["tick"] == 2
        state4 = read(runtime_root / "kuuos_adapter_capability_state_v0_6.json")
        bundle4 = read(runtime_root / "kuuos_adapter_capability_bundle_v0_6.json")
        assert state4["cycle_index"] == 4
        assert state4["total_calibrations"] == 4
        assert bundle4["generation"] == 4
        assert len(bundle4["sections"]) == 3
        assert len(bundle4["holonomy_trace"]) == 4
        assert len(bundle4["processed_evidence_digests"]) == 4
        no_graph(bundle4)

        stale_sources = [source("event-005")]
        stale_plan = plan(
            "capability-stale",
            stale_sources,
            root,
            adapter_registry,
            state4["capability_state_digest"],
            initial_bundle_digest(),
        )
        stale = build_adapter_capability_gauge(
            runtime_context=context(runtime_root),
            source_packets=stale_sources,
            root_principles_packet=root,
            adapter_registry=adapter_registry,
            capability_plan=stale_plan,
            capability_license=license_packet(
                stale_plan,
                stale_sources,
                root,
                adapter_registry,
                initial_bundle_digest(),
            ),
        )
        assert stale.status == BLOCKED
        assert "expected_previous_capability_bundle_digest_mismatch" in stale.blockers

        ledger = [
            json.loads(line)
            for line in (runtime_root / "kuuos_adapter_capability_ledger_v0_6.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        committed = [row for row in ledger if row.get("phase") == "committed"]
        assert len(committed) == 4
        assert [row["selected_federation_adapter_id"] for row in committed] == [
            "adapter-a",
            "adapter-b",
            "adapter-b",
            "adapter-a",
        ]

    formal = (
        ROOT / "formal/KUOS/OpenHorizon/AdapterCapabilityGaugeV0_6.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "CapabilitySection",
        "capabilityCurvature",
        "calibrate",
        "calibrate_eq_connection_add_curvature",
        "flat_observation_preserves_connection",
        "selectedAdapterCount_eq_zero_or_one",
    ):
        assert token in formal

    manifest = read(ROOT / "manifests/kuuos_adapter_capability_gauge_v0_6.json")
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative

    print("PASS: KuuOS adapter capability gauge v0.6 checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
