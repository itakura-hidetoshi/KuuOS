#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_world_information_geometric_higher_gauge_core_v0_43 import (
    BLOCKED,
    READY,
    REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS,
    VERSION,
    build_world_information_geometric_higher_gauge,
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
        "HigherInformationCurvature",
        "higherCurvature",
        "IsInformationFlatAt",
        "IsHigherGaugeFlatTriangle",
        "fisher_symmetric",
        "fisher_positive",
        "fisher_zero_iff",
        "alpha_one_is_exponential",
        "alpha_neg_one_is_mixture",
        "divergence_separates_parameters",
        "parameter_transport_injective",
        "tangent_transport_injective",
        "fisher_metric_gauge_covariant",
        "divergence_gauge_invariant",
        "alpha_connection_gauge_covariant",
        "scalar_curvature_gauge_invariant",
        "higher_curvature_retains_gauge_component",
        "information_geometry_package",
        "higher_gauge_information_package",
        "runtime_grants_no_information_geometric_authority",
        "representation_boundary_preserved",
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
        "physical_fisher_metric_computed_by_runtime": False,
        "world_identity_inferred_from_divergence": False,
        "higher_gauge_curvature_flattened_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = plan_digest(plan)
    ready = build_world_information_geometric_higher_gauge(plan)
    assert ready.status == READY
    assert ready.decision == "ready"
    assert ready.bridge_state_digest

    denied = dict(plan)
    denied["world_identity_inferred_from_divergence"] = True
    denied["plan_digest"] = plan_digest(denied)
    blocked = build_world_information_geometric_higher_gauge(denied)
    assert blocked.status == BLOCKED
    assert "world_identity_inferred_from_divergence_forbidden" in blocked.blockers

    manifest = json.loads(
        (ROOT / "manifests/world_information_geometric_higher_gauge_v0_43.json")
        .read_text(encoding="utf-8")
    )
    for values in manifest["files"].values():
        for relative in values:
            assert (ROOT / relative).is_file(), relative

    print("world_information_geometric_higher_gauge_v0_43 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
