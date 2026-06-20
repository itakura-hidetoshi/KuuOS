#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_quantum_exponential_dual_affine_projection_core_v0_45 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_quantum_exponential_dual_affine_projection,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/QuantumExponentialDualAffineProjectionBridgeV0_45.lean"
    source = ROOT / "formal/KUOS/WORLD/ArakiPetzQuantumInformationGeometryBridgeV0_44.lean"
    text = formal.read_text(encoding="utf-8")

    for token in (
        "WorldQuantumExponentialDualAffineProjectionBridge",
        "naturalCoordinate",
        "expectationCoordinate",
        "logPartition",
        "dualPotential",
        "fenchelYoungGap",
        "quantumBregmanDivergence",
        "exponentialProjection",
        "mixtureProjection",
        "exponentialProjectionDefect",
        "mixtureProjectionDefect",
        "fenchel_young_nonnegative",
        "fenchel_young_zero_iff",
        "quantum_bregman_nonnegative",
        "quantum_bregman_zero_iff",
        "exponential_projection_idempotent",
        "mixture_projection_idempotent",
        "exponential_projection_defect_zero_iff_fixed",
        "mixture_projection_defect_zero_iff_fixed",
        "exponential_pythagorean",
        "mixture_pythagorean",
        "projected_coordinates_are_petz_recoverable",
        "quantum_bregman_gauge_invariant",
        "fenchel_young_gauge_invariant",
        "dual_affine_projection_package",
        "analytic_dual_affine_receipts_complete",
        "runtime_grants_no_dual_affine_authority",
        "dual_affine_representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-45-example",
        "source_v044_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "quantum_exponential_family_constructed_by_runtime": False,
        "log_partition_computed_by_runtime": False,
        "legendre_transform_executed_by_runtime": False,
        "information_projection_executed_by_runtime": False,
        "world_identity_inferred_from_projection": False,
        "world_state_optimized_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_quantum_exponential_dual_affine_projection(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["information_projection_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_quantum_exponential_dual_affine_projection(denied)
    assert blocked.status == BLOCKED
    assert "information_projection_executed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"][
        "zero_projection_defect_not_ontological_identity"
    ] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_quantum_exponential_dual_affine_projection(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_zero_projection_defect_not_ontological_identity_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_quantum_exponential_dual_affine_projection_v0_45.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_quantum_exponential_dual_affine_projection_v0_45 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
