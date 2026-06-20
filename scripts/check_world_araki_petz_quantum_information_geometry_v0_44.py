#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_araki_petz_quantum_information_geometry_core_v0_44 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_araki_petz_quantum_information_geometry,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/ArakiPetzQuantumInformationGeometryBridgeV0_44.lean"
    source = ROOT / "formal/KUOS/WORLD/InformationGeometricHigherGaugeBridgeV0_43.lean"
    text = formal.read_text(encoding="utf-8")

    for token in (
        "WorldArakiPetzQuantumInformationGeometryBridge",
        "arakiHessianShadow",
        "quantumFisherMetric",
        "coarseTangent",
        "petzRecoveryTangent",
        "recoveredTangent",
        "IsPetzRecoverable",
        "informationLoss",
        "dataProcessingDefect",
        "quantum_fisher_eq_fisher",
        "quantum_fisher_nonnegative",
        "quantum_fisher_zero_iff",
        "recoveredTangent_idempotent_apply",
        "residual_orthogonal_to_recovered",
        "recovered_pythagorean",
        "information_loss_zero_iff_recoverable",
        "data_processing_defect_nonnegative",
        "data_processing_defect_zero_iff_recoverable",
        "recovered_observable_is_operator_petz_channel",
        "quantum_fisher_gauge_invariant",
        "information_loss_gauge_invariant",
        "analytic_quantum_information_receipts_complete",
        "runtime_grants_no_quantum_information_authority",
        "quantum_information_representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-44-example",
        "source_v043_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "araki_entropy_differentiated_by_runtime": False,
        "quantum_fisher_computed_by_runtime": False,
        "bkm_metric_constructed_by_runtime": False,
        "petz_projection_executed_by_runtime": False,
        "sufficiency_inferred_by_runtime": False,
        "world_state_optimized_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_araki_petz_quantum_information_geometry(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["petz_projection_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_araki_petz_quantum_information_geometry(denied)
    assert blocked.status == BLOCKED
    assert "petz_projection_executed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"][
        "metric_recoverability_not_ontological_identity"
    ] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_araki_petz_quantum_information_geometry(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_metric_recoverability_not_ontological_identity_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_araki_petz_quantum_information_geometry_v0_44.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_araki_petz_quantum_information_geometry_v0_44 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
