#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_canonical_endomorphism_qsystem_frobenius_bridge_core_v0_39 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_canonical_endomorphism_qsystem_frobenius_bridge,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/CanonicalEndomorphismQSystemFrobeniusBridgeV0_39.lean"
    source = ROOT / "formal/KUOS/WORLD/JonesTowerStandardInvariantBridgeV0_38.lean"
    text = formal.read_text(encoding="utf-8")
    required_tokens = (
        "WorldCanonicalEndomorphismQSystemFrobeniusBridge",
        "inclusion_injective",
        "canonical_apply_formula",
        "dual_canonical_apply_formula",
        "canonical_multiplicative",
        "dual_canonical_multiplicative",
        "canonical_preserves_star",
        "qSystem_associative",
        "qSystem_frobenius_law",
        "qSystem_specialness",
        "jonesProjection_compresses_canonical",
        "qSystemUnit_mem_tower_zero",
        "standard_invariant_connection_package",
        "analytic_receipts_complete",
        "runtime_grants_no_qSystem_authority",
        "representation_boundary_preserved",
    )
    for token in required_tokens:
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-39-example",
        "source_v038_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "canonical_endomorphism_constructed_by_runtime": False,
        "q_system_executed_by_runtime": False,
        "subfactor_reconstruction_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_canonical_endomorphism_qsystem_frobenius_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["q_system_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_canonical_endomorphism_qsystem_frobenius_bridge(denied)
    assert blocked.status == BLOCKED
    assert "q_system_executed_by_runtime_forbidden" in blocked.blockers

    manifest_path = ROOT / "manifests/world_canonical_endomorphism_qsystem_frobenius_bridge_v0_39.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_canonical_endomorphism_qsystem_frobenius_bridge_v0_39 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
