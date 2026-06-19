#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_petz_recovery_sufficiency_bridge_core_v0_35 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/PetzRecoverySufficiencyBridgeV0_35.lean"
    source = ROOT / "formal/KUOS/WORLD/ArakiRelativeEntropyBridgeV0_34.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldPetzRecoverySufficiencyBridge",
        "recoveredChannel_unital",
        "distinguished_state_pair_sufficient",
        "recoveredChannel_idempotent",
        "recoveredChannel_preserves_weakClosure",
        "entropy_equality_case",
        "reverse_data_processing_bound",
        "equality_case_package",
        "channel_receipts_complete",
        "recovery_receipts_complete",
        "runtime_grants_no_recovery_authority",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-35-example",
        "source_v034_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "channel_constructed_by_runtime": False,
        "recovery_constructed_by_runtime": False,
        "equality_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_petz_recovery_sufficiency_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    broken = dict(plan)
    broken["recovery_constructed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_petz_recovery_sufficiency_bridge(broken)
    assert blocked.status == BLOCKED
    assert "recovery_constructed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_petz_recovery_sufficiency_bridge_v0_35.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_petz_recovery_sufficiency_bridge_v0_35 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
