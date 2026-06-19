#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_jones_basic_construction_index_bridge_core_v0_37 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/JonesBasicConstructionIndexBridgeV0_37.lean"
    source = ROOT / "formal/KUOS/WORLD/ConditionalExpectationTakesakiBridgeV0_36.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldJonesBasicConstructionIndexBridge",
        "jonesProjection_compresses_sufficient",
        "jonesProjection_corner_of_sufficient",
        "basicConstruction_contains_sandwich",
        "jonesProjection_mem_relativeCommutant",
        "indexElement_mem_relativeCommutant",
        "left_quasi_basis_reconstruction",
        "right_quasi_basis_reconstruction",
        "indexElement_quasiBasis_formula",
        "jonesIndex_pos",
        "finite_index_package",
        "analytic_receipts_complete",
        "runtime_grants_no_jones_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-37-example",
        "source_v036_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "jones_projection_constructed_by_runtime": False,
        "basic_construction_executed_by_runtime": False,
        "finite_index_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_jones_basic_construction_index_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    broken = dict(plan)
    broken["finite_index_theorem_claimed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_jones_basic_construction_index_bridge(broken)
    assert blocked.status == BLOCKED
    assert "finite_index_theorem_claimed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_jones_basic_construction_index_bridge_v0_37.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_jones_basic_construction_index_bridge_v0_37 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
