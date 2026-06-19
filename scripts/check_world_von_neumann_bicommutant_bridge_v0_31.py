#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_von_neumann_bicommutant_bridge_core_v0_31 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/VonNeumannBicommutantBridgeV0_31.lean"
    source = ROOT / "formal/KUOS/WORLD/CStarLocalNetBridgeV0_30.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldVonNeumannBicommutantBridge",
        "subset_bicommutant",
        "commutant_antitone",
        "bicommutant_monotone",
        "triple_commutant_eq_commutant",
        "bicommutant_idempotent",
        "localBicommutant_isotony",
        "localBicommutants_commute",
        "weakClosure_isotony",
        "weakClosures_spacelike_commute",
        "runtime_grants_no_von_neumann_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-31-example",
        "source_v030_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "weak_operator_topology_modeled_by_runtime": False,
        "weak_closure_constructed_by_runtime": False,
        "runtime_bicommutant_theorem_claimed": False,
        "unbounded_operator_executed": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_von_neumann_bicommutant_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "world_von_neumann_bicommutant_bridge_ready"
    broken = dict(plan)
    broken["runtime_bicommutant_theorem_claimed"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_von_neumann_bicommutant_bridge(broken)
    assert blocked.status == BLOCKED
    assert "runtime_bicommutant_theorem_claimed_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_von_neumann_bicommutant_bridge_v0_31.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_von_neumann_bicommutant_bridge_v0_31 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
