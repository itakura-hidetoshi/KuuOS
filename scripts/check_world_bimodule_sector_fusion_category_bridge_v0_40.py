#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_bimodule_sector_fusion_category_bridge_core_v0_40 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_bimodule_sector_fusion_category_bridge,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/BimoduleSectorFusionCategoryBridgeV0_40.lean"
    source = ROOT / "formal/KUOS/WORLD/CanonicalEndomorphismQSystemFrobeniusBridgeV0_39.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldBimoduleSectorFusionCategoryBridge",
        "sector_dual_involution",
        "fusion_left_unit_at_self",
        "fusion_associative",
        "fusion_dual_symmetry",
        "fusion_left_frobenius_reciprocity",
        "fusion_right_frobenius_reciprocity",
        "fusion_dimension_formula",
        "jonesIndex_eq_fundamentalDimension_sq",
        "dualCanonicalMultiplicity_fusion_formula",
        "dualCanonical_dimension_fusion_sum",
        "qSystemSpecialnessScalar_eq_fundamentalDimension_sq",
        "principalGraph_edge_formula",
        "dualPrincipalGraph_edge_formula",
        "principalGraphTwoStep_symmetric",
        "fusion_ring_package",
        "statistical_dimension_package",
        "qSystem_standardInvariant_sector_package",
        "analytic_receipts_complete",
        "runtime_grants_no_sector_fusion_authority",
        "representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-40-example",
        "source_v039_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "bimodules_constructed_by_runtime": False,
        "connes_fusion_executed_by_runtime": False,
        "fusion_category_reconstruction_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_bimodule_sector_fusion_category_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["connes_fusion_executed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_bimodule_sector_fusion_category_bridge(denied)
    assert blocked.status == BLOCKED
    assert "connes_fusion_executed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"]["sector_fusion_read_only_analytic_sidecar"] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_bimodule_sector_fusion_category_bridge(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_sector_fusion_read_only_analytic_sidecar_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_bimodule_sector_fusion_category_bridge_v0_40.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_bimodule_sector_fusion_category_bridge_v0_40 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
