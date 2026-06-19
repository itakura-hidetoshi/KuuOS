#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_cstar_local_net_bridge_core_v0_30 import *


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/CStarLocalNetBridgeV0_30.lean"
    source = ROOT / "formal/KUOS/WORLD/NoncommutativeOperatorAlgebraModuleV0_29.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldCStarLocalNetBridge",
        "cstar_identity",
        "completion_embedding_dense",
        "embedded_noncommuting",
        "closedLocal",
        "closedLocal_isotony",
        "closedLocal_isClosed",
        "source_local_mem_closedLocal",
        "local_observables_commute",
        "representation_boundary_preserved",
    ):
        assert token in text, token
    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-30-example",
        "source_v029_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "cstar_completion_constructed_by_runtime": False,
        "unbounded_operator_executed": False,
        "runtime_proof_claimed": False,
        "world_updated": False,
        "external_actuation_performed": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_cstar_local_net_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "world_cstar_local_net_bridge_ready"
    broken = dict(plan)
    broken["cstar_completion_constructed_by_runtime"] = True
    broken["plan_digest"] = plan_digest(broken)
    blocked = build_world_cstar_local_net_bridge(broken)
    assert blocked.status == BLOCKED
    assert "cstar_completion_constructed_by_runtime_forbidden" in blocked.blockers
    manifest = json.loads((ROOT / "manifests/world_cstar_local_net_bridge_v0_30.json").read_text())
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative
    print("world_cstar_local_net_bridge_v0_30 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
