#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_information_geometric_higher_gauge_bridge_core_v0_43 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_information_geometric_higher_gauge_bridge,
    plan_digest,
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    formal = ROOT / "formal/KUOS/WORLD/InformationGeometricHigherGaugeBridgeV0_43.lean"
    source = ROOT / "formal/KUOS/WORLD/GaugeCategoricalIndraNetBridgeV0_42.lean"
    text = formal.read_text(encoding="utf-8")
    for token in (
        "WorldInformationGeometricHigherGaugeBridge",
        "alphaConnection",
        "IsDuallyFlatAt",
        "informationTriangleHolonomy",
        "IsInformationFlatTriangle",
        "probability_mass_normalized",
        "score_expectation_zero",
        "fisher_metric_is_score_covariance",
        "fisher_metric_positive",
        "fisher_metric_zero_iff",
        "alphaConnection_one",
        "alphaConnection_neg_one",
        "alphaConnection_zero",
        "dual_connection_metric_compatibility",
        "information_divergence_nonnegative",
        "information_divergence_zero_iff",
        "information_projection_idempotent",
        "information_projection_pythagorean",
        "statistical_transport_injective",
        "tangent_transport_injective",
        "fisher_metric_gauge_invariant",
        "divergence_gauge_invariant",
        "information_projection_gauge_covariant",
        "statistical_transport_composes_up_to_two_cell",
        "identity_left_information_triangle_flat",
        "identity_right_information_triangle_flat",
        "branch_information_transport",
        "branch_information_embedding_injective",
        "fisher_dual_connection_package",
        "information_projection_package",
        "higher_gauge_information_geometry_package",
        "analytic_information_geometry_receipts_complete",
        "runtime_grants_no_information_geometric_authority",
        "information_geometric_representation_boundary_preserved",
    ):
        assert token in text, token

    plan = {
        "version": VERSION,
        "world_model_id": "world-v0-43-example",
        "source_v042_sha256": sha(source),
        "formal_module_sha256": sha(formal),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": dict(REQUIRED_BOUNDARY),
        "statistical_manifold_constructed_by_runtime": False,
        "fisher_metric_computed_by_runtime": False,
        "information_projection_performed_by_runtime": False,
        "belief_optimized_by_runtime": False,
        "policy_executed_by_runtime": False,
        "chentsov_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_information_geometric_higher_gauge_bridge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["belief_optimized_by_runtime"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_information_geometric_higher_gauge_bridge(denied)
    assert blocked.status == BLOCKED
    assert "belief_optimized_by_runtime_forbidden" in blocked.blockers

    denied_boundary = dict(plan)
    denied_boundary["boundary"] = dict(REQUIRED_BOUNDARY)
    denied_boundary["boundary"][
        "information_distance_not_ontological_distance"
    ] = False
    denied_boundary["plan_digest"] = plan_digest(denied_boundary)
    blocked_boundary = build_world_information_geometric_higher_gauge_bridge(
        denied_boundary
    )
    assert blocked_boundary.status == BLOCKED
    assert (
        "boundary_information_distance_not_ontological_distance_invalid"
        in blocked_boundary.blockers
    )

    manifest = json.loads(
        (
            ROOT
            / "manifests/world_information_geometric_higher_gauge_bridge_v0_43.json"
        ).read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_information_geometric_higher_gauge_bridge_v0_43 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
