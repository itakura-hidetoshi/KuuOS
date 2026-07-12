#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_second_order_metric_jet_curvature_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_second_order_metric_jet_curvature_certificate,
    canonical_digest,
    compute_candidate_plane_bundle_digest,
    compute_metric_jet_digest,
    compute_plan_coordinate_schema_digest,
    compute_second_order_metric_jet_digest,
)


def coordinates() -> list[str]:
    return ["x", "y"]


def metric_matrix() -> dict:
    return {
        "x": {"x": 1.0, "y": 0.0},
        "y": {"x": 0.0, "y": 1.0},
    }


def inverse_metric_matrix() -> dict:
    return metric_matrix()


def metric_first_derivatives() -> dict:
    # g = exp(2 phi) I at phi = 0, with grad phi = (0.1, -0.05).
    return {
        "x": {
            "x": {"x": 0.20, "y": 0.0},
            "y": {"x": 0.0, "y": 0.20},
        },
        "y": {
            "x": {"x": -0.10, "y": 0.0},
            "y": {"x": 0.0, "y": -0.10},
        },
    }


def metric_second_derivatives() -> dict:
    # Hess phi = [[0.2, 0.03], [0.03, -0.1]].
    # d_a d_b g = (2 phi_ab + 4 phi_a phi_b) I at phi = 0.
    values = {
        "x": {"x": 0.44, "y": 0.04},
        "y": {"x": 0.04, "y": -0.19},
    }
    return {
        first: {
            second: {
                "x": {"x": values[first][second], "y": 0.0},
                "y": {"x": 0.0, "y": values[first][second]},
            }
            for second in coordinates()
        }
        for first in coordinates()
    }


def candidate_planes() -> list[dict]:
    return [
        {
            "candidate_id": "continue",
            "plane_u": {"x": 0.10, "y": 0.0},
            "plane_v": {"x": 0.0, "y": 0.10},
            "holonomy_vector": {"x": 0.20, "y": -0.10},
            "source_candidate_digest": "candidate-continue-digest",
        },
        {
            "candidate_id": "reroute",
            "plane_u": {"x": 0.08, "y": 0.02},
            "plane_v": {"x": -0.01, "y": 0.09},
            "holonomy_vector": {"x": -0.15, "y": 0.12},
            "source_candidate_digest": "candidate-reroute-digest",
        },
    ]


def build(**overrides):
    metric = overrides.pop("metric_matrix", metric_matrix())
    inverse = overrides.pop("inverse_metric_matrix", inverse_metric_matrix())
    first = overrides.pop("metric_first_derivatives", metric_first_derivatives())
    second = overrides.pop("metric_second_derivatives", metric_second_derivatives())
    planes = overrides.pop("candidate_planes", candidate_planes())

    try:
        coordinate_order = sorted(metric)
    except (TypeError, AttributeError):
        coordinate_order = []

    def safe_digest(function, **kwargs):
        try:
            return function(**kwargs)
        except (KeyError, TypeError, ValueError):
            return canonical_digest(kwargs)

    source_metric_digest = overrides.pop(
        "source_metric_jet_digest",
        safe_digest(
            compute_metric_jet_digest,
            metric_matrix=metric,
            inverse_metric_matrix=inverse,
            metric_first_derivatives=first,
        ),
    )
    args = {
        "source_levi_civita_certificate_digest": (
            "planos-v1-06-levi-civita-certificate"
        ),
        "plan_coordinate_schema_digest": safe_digest(
            compute_plan_coordinate_schema_digest,
            metric_matrix=metric,
        ),
        "state_context_digest": "planos-state-context-digest",
        "source_metric_jet_digest": source_metric_digest,
        "metric_matrix": metric,
        "inverse_metric_matrix": inverse,
        "metric_first_derivatives": first,
        "second_order_metric_jet_digest": safe_digest(
            compute_second_order_metric_jet_digest,
            source_metric_jet_digest=source_metric_digest,
            metric_second_derivatives=second,
            coordinates=coordinate_order,
        ),
        "metric_second_derivatives": second,
        "candidate_plane_bundle_digest": safe_digest(
            compute_candidate_plane_bundle_digest,
            candidate_planes=planes,
            coordinates=coordinate_order,
        ),
        "candidate_planes": planes,
        "maximum_absolute_second_metric_derivative": 0.50,
        "maximum_absolute_connection_derivative": 0.25,
        "maximum_absolute_riemann": 0.20,
        "maximum_absolute_ricci": 0.20,
        "maximum_absolute_scalar_curvature": 0.30,
        "maximum_absolute_sectional_curvature": 0.20,
        "minimum_plane_gram_determinant": 1e-6,
        "maximum_loop_edge_component": 0.12,
        "maximum_absolute_holonomy_increment": 0.001,
    }
    args.update(overrides)
    return build_second_order_metric_jet_curvature_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    certificate = result.certificate

    for name in (
        "second_order_metric_jet_present",
        "metric_symmetric",
        "metric_positive_definite",
        "inverse_metric_exact",
        "metric_first_derivative_symmetric",
        "metric_second_derivative_metric_indices_symmetric",
        "mixed_partial_derivatives_symmetric",
        "inverse_metric_derivative_identity_preserved",
        "connection_derivative_recomputed",
        "riemann_curvature_recomputed",
        "riemann_last_pair_antisymmetric",
        "riemann_first_bianchi",
        "lower_riemann_pair_symmetries",
        "ricci_curvature_recomputed",
        "ricci_symmetric",
        "scalar_curvature_recomputed",
        "sectional_curvature_retained",
        "infinitesimal_holonomy_retained",
        "curvature_bounded",
        "holonomy_bounded",
        "source_levi_civita_not_mutated",
        "persistent_world_state_unchanged",
        "candidate_plane_field_retained",
        "history_read_only",
        "qi_grants_no_authority",
        "world_projection_grants_no_authority",
        "connection_grants_no_authority",
        "curvature_grants_no_authority",
        "future_only",
    ):
        assert certificate[name] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    assert abs(certificate["computed_scalar_curvature"] + 0.2) < 1e-10
    assert abs(certificate["computed_maximum_absolute_riemann"] - 0.1) < 1e-10
    assert abs(certificate["computed_maximum_absolute_ricci"] - 0.1) < 1e-10
    assert certificate["maximum_inverse_metric_derivative_residual"] < 1e-10
    assert len(certificate["plane_curvature_records"]) == 2
    for record in certificate["plane_curvature_records"]:
        assert record["plane_gram_determinant"] > 0.0
        assert abs(record["sectional_curvature"] - 0.1) < 1e-10
        assert any(
            abs(value) > 0.0
            for value in record["infinitesimal_holonomy_increment"].values()
        )

    nonsymmetric_metric = metric_matrix()
    nonsymmetric_metric["x"]["y"] = 0.1

    indefinite_metric = metric_matrix()
    indefinite_metric["y"]["y"] = -1.0

    wrong_inverse = inverse_metric_matrix()
    wrong_inverse["x"]["x"] = 2.0

    nonsymmetric_first = metric_first_derivatives()
    nonsymmetric_first["x"]["x"]["y"] = 0.1

    nonsymmetric_second_metric = metric_second_derivatives()
    nonsymmetric_second_metric["x"]["x"]["x"]["y"] = 0.1

    nonsymmetric_mixed = metric_second_derivatives()
    nonsymmetric_mixed["x"]["y"]["x"]["x"] += 0.01

    zero_second = metric_second_derivatives()
    for first in coordinates():
        for second in coordinates():
            for i in coordinates():
                for j in coordinates():
                    zero_second[first][second][i][j] = 0.0

    oversized_second = metric_second_derivatives()
    oversized_second["x"]["x"]["x"]["x"] = 1.0
    oversized_second["x"]["x"]["y"]["y"] = 1.0

    empty_planes: list[dict] = []

    duplicate_candidate = candidate_planes()
    duplicate_candidate[1]["candidate_id"] = duplicate_candidate[0]["candidate_id"]

    duplicate_source = candidate_planes()
    duplicate_source[1]["source_candidate_digest"] = duplicate_source[0][
        "source_candidate_digest"
    ]

    degenerate_plane = candidate_planes()
    degenerate_plane[0]["plane_v"] = {
        key: 2.0 * value for key, value in degenerate_plane[0]["plane_u"].items()
    }

    oversized_edge = candidate_planes()
    oversized_edge[0]["plane_u"]["x"] = 0.20

    nonfinite_plane = candidate_planes()
    nonfinite_plane[0]["plane_u"]["x"] = float("nan")

    blocked = [
        build(source_levi_civita_certificate_digest=""),
        build(state_context_digest=""),
        build(plan_coordinate_schema_digest="wrong"),
        build(source_metric_jet_digest="wrong"),
        build(second_order_metric_jet_digest="wrong"),
        build(candidate_plane_bundle_digest="wrong"),
        build(metric_matrix={}),
        build(metric_matrix=nonsymmetric_metric),
        build(metric_matrix=indefinite_metric),
        build(inverse_metric_matrix=wrong_inverse),
        build(metric_first_derivatives=nonsymmetric_first),
        build(metric_second_derivatives=nonsymmetric_second_metric),
        build(metric_second_derivatives=nonsymmetric_mixed),
        build(metric_second_derivatives=zero_second),
        build(metric_second_derivatives=oversized_second),
        build(candidate_planes=empty_planes),
        build(candidate_planes=duplicate_candidate),
        build(candidate_planes=duplicate_source),
        build(candidate_planes=degenerate_plane),
        build(candidate_planes=oversized_edge),
        build(candidate_planes=nonfinite_plane),
        build(maximum_absolute_second_metric_derivative=0.0),
        build(maximum_absolute_connection_derivative=0.1),
        build(maximum_absolute_riemann=0.05),
        build(maximum_absolute_ricci=0.05),
        build(maximum_absolute_scalar_curvature=0.1),
        build(maximum_absolute_sectional_curvature=0.05),
        build(minimum_plane_gram_determinant=0.001),
        build(maximum_loop_edge_component=0.05),
        build(maximum_absolute_holonomy_increment=0.00005),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered_second = deepcopy(metric_second_derivatives())
    stale_second_digest = compute_second_order_metric_jet_digest(
        source_metric_jet_digest=compute_metric_jet_digest(
            metric_matrix=metric_matrix(),
            inverse_metric_matrix=inverse_metric_matrix(),
            metric_first_derivatives=metric_first_derivatives(),
        ),
        metric_second_derivatives=tampered_second,
        coordinates=coordinates(),
    )
    tampered_second["x"]["x"]["x"]["x"] += 0.01
    item = build(
        metric_second_derivatives=tampered_second,
        second_order_metric_jet_digest=stale_second_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    tampered_planes = deepcopy(candidate_planes())
    stale_plane_digest = compute_candidate_plane_bundle_digest(
        tampered_planes, coordinates()
    )
    tampered_planes[0]["plane_u"]["x"] += 0.01
    item = build(
        candidate_planes=tampered_planes,
        candidate_plane_bundle_digest=stale_plane_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print("PASS: PlanOS Second-Order Metric Jet Curvature Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
