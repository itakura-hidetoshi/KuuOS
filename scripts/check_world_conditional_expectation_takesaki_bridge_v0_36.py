#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_conditional_expectation_takesaki_bridge_core_v0_36 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/ConditionalExpectationTakesakiBridgeV0_36.lean"
    source = ROOT / "formal/KUOS/WORLD/PetzRecoverySufficiencyBridgeV0_35.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldConditionalExpectationTakesakiBridge",
        "conditionalExpectation_idempotent",
        "mem_sufficientSubalgebra_iff_fixed",
        "mem_sufficientSubalgebra_iff_exists_image",
        "conditionalExpectation_two_sided_module",
        "distinguished_state_pair_preserved",
        "recoveredChannel_eq_conditionalExpectation_apply",
        "recoveredChannel_fixed_points_are_sufficient",
        "sufficient_subalgebra_entropy_equality",
        "modularFlow_preserves_sufficientSubalgebra",
        "analytic_receipts_complete",
        "runtime_grants_no_conditional_expectation_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-36-example",
        "source_v035_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "conditional_expectation_constructed_by_runtime": False,
        "takesaki_theorem_claimed_by_runtime": False,
        "sufficient_subalgebra_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_conditional_expectation_takesaki_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    broken = dict(plan)
    broken["takesaki_theorem_claimed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_conditional_expectation_takesaki_bridge(broken)
    assert blocked.status == BLOCKED
    assert "takesaki_theorem_claimed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_conditional_expectation_takesaki_bridge_v0_36.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_conditional_expectation_takesaki_bridge_v0_36 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
