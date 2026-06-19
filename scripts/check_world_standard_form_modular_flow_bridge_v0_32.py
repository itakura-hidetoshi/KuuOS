#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_standard_form_modular_flow_bridge_core_v0_32 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/StandardFormModularFlowBridgeV0_32.lean"
    source = ROOT / "formal/KUOS/WORLD/VonNeumannBicommutantBridgeV0_31.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldStandardFormModularFlowBridge",
        "modularConjugation_sq",
        "commutantTransport_sq",
        "modularFlow_zero_apply",
        "modularFlow_add_apply",
        "modularFlow_right_inverse",
        "modularFlow_left_inverse",
        "modularFlow_preserves_weakClosure",
        "modularUnitary_add_apply",
        "modular_covariance",
        "naturalCone_modular_invariant",
        "analytic_receipts_complete",
        "runtime_grants_no_modular_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-32-example",
        "source_v031_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "tomita_operator_constructed_by_runtime": False,
        "modular_operator_executed": False,
        "runtime_standard_form_theorem_claimed": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_standard_form_modular_flow_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "world_standard_form_modular_flow_bridge_ready"
    broken = dict(plan)
    broken["modular_operator_executed"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_standard_form_modular_flow_bridge(broken)
    assert blocked.status == BLOCKED
    assert "modular_operator_executed_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_standard_form_modular_flow_bridge_v0_32.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_standard_form_modular_flow_bridge_v0_32 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
