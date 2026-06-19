#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_noncommutative_operator_algebra_module_core_v0_29 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/NoncommutativeOperatorAlgebraModuleV0_29.lean"
    source = ROOT / "formal/KUOS/WORLD/RealHilbertL2SelfAdjointProofReceiptBridgeV0_28.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "FaithfulNoncommutativeOperatorAlgebra",
        "commutatorSubmodule_ne_bot",
        "representedCommutatorSubmodule_ne_bot",
        "OperatorBimodule",
        "left_right_commute",
        "WorldNoncommutativeOperatorAlgebra",
        "relation_actions_commute",
        "representation_boundary_preserved",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-29-example",
        "source_v028_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "operator_executed": False,
        "world_updated": False,
        "runtime_proof_claimed": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_noncommutative_operator_algebra_module(plan)
    assert ready.status == READY
    assert ready.decision == "world_noncommutative_operator_algebra_module_ready"
    broken = dict(plan)
    broken["operator_executed"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_noncommutative_operator_algebra_module(broken)
    assert blocked.status == BLOCKED
    assert "operator_execution_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_noncommutative_operator_algebra_module_v0_29.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_noncommutative_operator_algebra_module_v0_29 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
