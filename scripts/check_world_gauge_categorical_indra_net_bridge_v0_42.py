#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_gauge_categorical_indra_net_bridge_core_v0_42 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_gauge_categorical_indra_net_bridge,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/GaugeCategoricalIndraNetBridgeV0_42.lean"
    source = ROOT / "formal/KUOS/WORLD/ModuleCategoryNimrepTubeCenterBridgeV0_41.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldGaugeCategoricalIndraNetBridge",
        "triangleHolonomy",
        "triangleCurvature",
        "IsFlatTriangle",
        "squareHolonomy",
        "algebra_transport_composes_up_to_two_cell",
        "sector_transport_composes_up_to_two_cell",
        "coherence_pentagon_shadow",
        "identity_left_triangle_flat",
        "identity_right_triangle_flat",
        "squareHolonomy_factorization",
        "tower_membership_gauge_covariant",
        "jones_projection_gauge_fixed",
        "qSystem_unit_gauge_fixed",
        "qSystem_multiplication_gauge_fixed",
        "fusion_multiplicity_gauge_covariant",
        "nimrep_gauge_covariant",
        "tube_star_gauge_covariant",
        "tube_multiplication_gauge_covariant",
        "center_idempotent_gauge_covariant",
        "branch_transport_injective",
        "gauge_categorical_covariance_package",
        "higher_gauge_package",
        "analytic_higher_gauge_receipts_complete",
        "runtime_grants_no_indra_gauge_authority",
        "representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-42-example",
        "source_v041_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "indra_gauge_connection_constructed_by_runtime": False,
        "physical_holonomy_computed_by_runtime": False,
        "ocneanu_flatness_solved_by_runtime": False,
        "bulk_topological_theory_reconstructed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_gauge_categorical_indra_net_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["physical_holonomy_computed_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_gauge_categorical_indra_net_bridge(denied)
    assert blocked.status == BLOCKED
    assert "physical_holonomy_computed_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"]["indra_net_read_only_analytic_sidecar"] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_gauge_categorical_indra_net_bridge(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_indra_net_read_only_analytic_sidecar_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT / "manifests/world_gauge_categorical_indra_net_bridge_v0_42.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_gauge_categorical_indra_net_bridge_v0_42 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
