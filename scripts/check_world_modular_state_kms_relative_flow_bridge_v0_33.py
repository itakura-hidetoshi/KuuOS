#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_modular_state_kms_relative_flow_bridge_core_v0_33 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/ModularStateKMSRelativeFlowBridgeV0_33.lean"
    source = ROOT / "formal/KUOS/WORLD/StandardFormModularFlowBridgeV0_32.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldModularStateKMSRelativeFlowBridge",
        "referenceState_normalized",
        "kms_zero_lower_boundary",
        "kms_imaginary_boundary",
        "relativeModularFlow_right_inverse",
        "relativeModularFlow_left_inverse",
        "connesCocycle_twisted_right_inverse",
        "connesCocycle_twisted_left_inverse",
        "connesCocycle_isometry_left",
        "relative_modular_implementation",
        "relativeModularFlow_preserves_weakClosure",
        "state_analytic_receipts_complete",
        "runtime_grants_no_relative_modular_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-33-example",
        "source_v032_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "kms_continuation_constructed_by_runtime": False,
        "relative_tomita_constructed_by_runtime": False,
        "relative_modular_operator_executed": False,
        "runtime_connes_theorem_claimed": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_modular_state_kms_relative_flow_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "world_modular_state_kms_relative_flow_bridge_ready"
    broken = dict(plan)
    broken["runtime_connes_theorem_claimed"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_modular_state_kms_relative_flow_bridge(broken)
    assert blocked.status == BLOCKED
    assert "runtime_connes_theorem_claimed_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_modular_state_kms_relative_flow_bridge_v0_33.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_modular_state_kms_relative_flow_bridge_v0_33 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
