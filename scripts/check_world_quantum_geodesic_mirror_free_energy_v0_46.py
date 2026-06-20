#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_quantum_geodesic_mirror_free_energy_core_v0_46 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_quantum_geodesic_mirror_free_energy,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/QuantumGeodesicMirrorDescentFreeEnergyBridgeV0_46.lean"
    source = ROOT / "formal/KUOS/WORLD/QuantumExponentialDualAffineProjectionBridgeV0_45.lean"
    text = formal.read_text(encoding="utf-8")
    required_tokens = (
        "WorldQuantumGeodesicMirrorDescentFreeEnergyBridge",
        "quantumGeodesicAction",
        "variationalFreeEnergy",
        "mirrorDescentStep",
        "mirrorDescentDissipation",
        "projectedMirrorDefect",
        "variational_free_energy_nonnegative",
        "mirror_descent_free_energy_nonincrease",
        "mirror_descent_bregman_certificate",
        "projected_mirror_defect_zero_iff_fixed",
        "mirror_descent_dissipation_gauge_invariant",
        "runtime_grants_no_variational_flow_authority",
        "variational_flow_representation_boundary_preserved",
    )
    for token in required_tokens:
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-46-example",
        "source_v045_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "quantum_geodesic_constructed_by_runtime": False,
        "physical_free_energy_computed_by_runtime": False,
        "mirror_descent_executed_by_runtime": False,
        "truth_inferred_from_low_free_energy": False,
        "execution_granted_from_descent": False,
        "world_state_optimized_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_quantum_geodesic_mirror_free_energy(plan)
    assert ready.status == READY and ready.bridge_state_digest

    denied = dict(plan)
    denied["mirror_descent_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_quantum_geodesic_mirror_free_energy(denied)
    assert blocked.status == BLOCKED

    manifest_path = ROOT / "manifests/world_quantum_geodesic_mirror_free_energy_v0_46.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_quantum_geodesic_mirror_free_energy_v0_46 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
