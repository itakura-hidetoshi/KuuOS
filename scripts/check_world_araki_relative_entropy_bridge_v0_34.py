#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_araki_relative_entropy_bridge_core_v0_34 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/ArakiRelativeEntropyBridgeV0_34.lean"
    source = ROOT / "formal/KUOS/WORLD/ModularStateKMSRelativeFlowBridgeV0_33.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldArakiRelativeEntropyBridge",
        "localRelativeEntropy_nonnegative",
        "local_data_processing",
        "local_data_processing_chain",
        "local_entropy_eq_of_order_equivalent",
        "selfRelativeEntropy_vanishes",
        "connes_chain_rule",
        "connes_chain_rule_adjoint",
        "thirdOverComparison_unitary_left",
        "entropy_analytic_receipts_complete",
        "runtime_grants_no_entropy_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-34-example",
        "source_v033_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "relative_modular_log_constructed_by_runtime": False,
        "araki_entropy_computed_by_runtime": False,
        "runtime_ucp_theorem_claimed": False,
        "petz_recovery_constructed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_araki_relative_entropy_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "world_araki_relative_entropy_bridge_ready"
    broken = dict(plan)
    broken["petz_recovery_constructed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_araki_relative_entropy_bridge(broken)
    assert blocked.status == BLOCKED
    assert "petz_recovery_constructed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_araki_relative_entropy_bridge_v0_34.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_araki_relative_entropy_bridge_v0_34 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
