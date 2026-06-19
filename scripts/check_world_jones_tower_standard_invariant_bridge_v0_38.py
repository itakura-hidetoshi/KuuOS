#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_jones_tower_standard_invariant_bridge_core_v0_38 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/JonesTowerStandardInvariantBridgeV0_38.lean"
    source = ROOT / "formal/KUOS/WORLD/JonesBasicConstructionIndexBridgeV0_37.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldJonesTowerStandardInvariantBridge",
        "tower_step",
        "projection_mem_later_stage",
        "original_projection_mem_stage_two",
        "temperleyLieb_right",
        "temperleyLieb_left",
        "distant_projections_commute",
        "projection_mem_lowerRelativeCommutant",
        "lower_standard_invariant_nesting",
        "upper_standard_invariant_nesting",
        "jonesIndex_eq_loopParameter_sq",
        "standard_invariant_package",
        "analytic_receipts_complete",
        "runtime_grants_no_tower_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-38-example",
        "source_v037_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "jones_tower_constructed_by_runtime": False,
        "temperley_lieb_executed_by_runtime": False,
        "standard_invariant_completeness_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_jones_tower_standard_invariant_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    broken = dict(plan)
    broken["standard_invariant_completeness_claimed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_jones_tower_standard_invariant_bridge(broken)
    assert blocked.status == BLOCKED
    assert "standard_invariant_completeness_claimed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_jones_tower_standard_invariant_bridge_v0_38.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_jones_tower_standard_invariant_bridge_v0_38 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
