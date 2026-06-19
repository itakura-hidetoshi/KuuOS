#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_module_category_nimrep_tube_center_bridge_core_v0_41 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_module_category_nimrep_tube_center_bridge,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/ModuleCategoryNimrepTubeCenterBridgeV0_41.lean"
    source = ROOT / "formal/KUOS/WORLD/BimoduleSectorFusionCategoryBridgeV0_40.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldModuleCategoryNimrepTubeCenterBridge",
        "moduleAction_unit_at_self",
        "nimrep_fusion_representation",
        "nimrep_dual_is_transpose",
        "moduleDimension_eigenvector_formula",
        "ocneanuCell_conjugation_symmetry",
        "tubeStar_involution",
        "tube_associative",
        "tubeStar_reverses_multiplication",
        "centralIdempotent_is_central",
        "centralIdempotent_is_idempotent",
        "centralIdempotents_are_orthogonal",
        "centralIdempotents_complete",
        "centerDimension_forgetful_formula",
        "drinfeldCenter_dimension_square",
        "nimrep_module_package",
        "tube_star_algebra_package",
        "tube_center_package",
        "analytic_categorical_receipts_complete",
        "runtime_grants_no_module_tube_center_authority",
        "representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-41-example",
        "source_v040_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "module_category_constructed_by_runtime": False,
        "ocneanu_cells_solved_by_runtime": False,
        "tube_algebra_built_by_runtime": False,
        "drinfeld_center_reconstructed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_module_category_nimrep_tube_center_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["tube_algebra_built_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_module_category_nimrep_tube_center_bridge(denied)
    assert blocked.status == BLOCKED
    assert "tube_algebra_built_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"][
        "module_tube_center_read_only_analytic_sidecar"
    ] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_module_category_nimrep_tube_center_bridge(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_module_tube_center_read_only_analytic_sidecar_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_module_category_nimrep_tube_center_bridge_v0_41.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_module_category_nimrep_tube_center_bridge_v0_41 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
