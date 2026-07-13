#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_exponential_map_normal_coordinate_ball_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_exponential_map_normal_coordinate_ball_certificate,
    compute_local_model_input_digest,
)


def coordinate_schema() -> list[str]:
    return ["x", "y"]


def base_point() -> dict:
    return {"x": 0.0, "y": 0.0}


def metric_matrix() -> dict:
    return {
        "x": {"x": 1.0, "y": 0.0},
        "y": {"x": 0.0, "y": 1.0},
    }


def christoffel_symbols() -> dict:
    return {
        "x": {
            "x": {"x": 0.0, "y": 0.0},
            "y": {"x": 0.0, "y": 0.1},
        },
        "y": {
            "x": {"x": 0.0, "y": 0.05},
            "y": {"x": 0.05, "y": 0.0},
        },
    }


def charts() -> list[dict]:
    return [
        {
            "chart_id": "normal-primary",
            "center": {"x": 0.0, "y": 0.0},
            "safe_radius": 1.0,
            "coordinate_lower_bounds": {"x": -1.0, "y": -1.0},
            "coordinate_upper_bounds": {"x": 1.0, "y": 1.0},
            "source_chart_digest": "atlas-chart-normal-primary",
        },
        {
            "chart_id": "normal-overlap",
            "center": {"x": 0.2, "y": 0.2},
            "safe_radius": 1.2,
            "coordinate_lower_bounds": {"x": -1.0, "y": -1.0},
            "coordinate_upper_bounds": {"x": 1.2, "y": 1.2},
            "source_chart_digest": "atlas-chart-normal-overlap",
        },
    ]


def candidates() -> list[dict]:
    return [
        {
            "candidate_id": "radial-a",
            "tangent_vector": {"x": 0.5, "y": 0.2},
            "expected_endpoint": {"x": 0.498, "y": 0.195},
            "expected_midpoint": {"x": 0.2495, "y": 0.09875},
            "assigned_chart_id": "normal-primary",
            "source_candidate_digest": "radial-candidate-a",
        },
        {
            "candidate_id": "radial-b",
            "tangent_vector": {"x": -0.3, "y": 0.4},
            "expected_endpoint": {"x": -0.308, "y": 0.406},
            "expected_midpoint": {"x": -0.152, "y": 0.2015},
            "assigned_chart_id": "normal-primary",
            "source_candidate_digest": "radial-candidate-b",
        },
    ]


def build(**overrides):
    coords = overrides.pop("coordinate_schema", coordinate_schema())
    base = overrides.pop("base_point", base_point())
    metric = overrides.pop("metric_matrix", metric_matrix())
    connection = overrides.pop("christoffel_symbols", christoffel_symbols())
    chart_records = overrides.pop("chart_records", charts())
    radial_candidates = overrides.pop(
        "radial_geodesic_candidates", candidates()
    )
    digest = overrides.pop(
        "local_model_input_digest",
        compute_local_model_input_digest(
            coordinate_schema=coords,
            base_point=base,
            metric_matrix=metric,
            christoffel_symbols=connection,
            chart_records=chart_records,
            radial_geodesic_candidates=radial_candidates,
        ),
    )
    args = {
        "source_injectivity_radius_certificate_digest": (
            "planos-v1-11-injectivity-radius-certificate"
        ),
        "source_atlas_certificate_digest": "planos-v1-08-atlas-certificate",
        "local_model_input_digest": digest,
        "coordinate_schema": coords,
        "base_point": base,
        "metric_matrix": metric,
        "christoffel_symbols": connection,
        "chart_records": chart_records,
        "radial_geodesic_candidates": radial_candidates,
        "source_injectivity_radius_lower_bound": 1.5,
        "normal_coordinate_ball_radius": 0.8,
        "maximum_exponential_map_residual": 1e-10,
        "maximum_midpoint_residual": 1e-10,
        "minimum_distinct_endpoint_separation": 0.1,
    }
    args.update(overrides)
    return build_exponential_map_normal_coordinate_ball_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["normal_coordinate_ball_radius"] == 0.8
    assert cert["source_injectivity_radius_lower_bound"] == 1.5
    assert cert["computed_maximum_endpoint_residual"] < 1e-12
    assert cert["computed_maximum_midpoint_residual"] < 1e-12
    assert cert["computed_minimum_endpoint_separation"] > 0.1
    for name in (
        "finite_second_order_exponential_model_recomputed",
        "normal_ball_strictly_inside_injectivity_bound",
        "radial_geodesic_unique_from_basepoint",
        "finite_sample_exponential_map_injective",
        "normal_coordinate_candidates_retained",
        "chart_safe_geodesic_ball_covering",
        "chart_boundaries_respected",
        "atlas_transition_authority_not_extended",
        "local_model_only",
        "global_exponential_map_not_claimed",
        "strong_convexity_not_claimed",
        "pairwise_endpoint_geodesic_uniqueness_not_claimed",
        "candidate_identity_retained",
        "source_injectivity_certificate_not_mutated",
        "source_atlas_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "exponential_map_grants_no_authority",
        "normal_ball_grants_no_authority",
        "chart_cover_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False
    for candidate in cert["radial_geodesic_candidates"]:
        assert candidate["radial_geodesic_unique_from_basepoint_witness"] is True
        assert candidate["assigned_chart_safe"] is True

    blocked = [
        build(source_injectivity_radius_certificate_digest=""),
        build(source_atlas_certificate_digest=""),
        build(local_model_input_digest="stale"),
        build(coordinate_schema=["x", "x"]),
        build(normal_coordinate_ball_radius=1.5),
        build(source_injectivity_radius_lower_bound=0.0),
        build(radial_geodesic_candidates=[]),
        build(chart_records=[]),
    ]

    nonsymmetric_metric = metric_matrix()
    nonsymmetric_metric["x"]["y"] = 0.2
    blocked.append(build(metric_matrix=nonsymmetric_metric))

    indefinite_metric = metric_matrix()
    indefinite_metric["y"]["y"] = -1.0
    blocked.append(build(metric_matrix=indefinite_metric))

    outside_candidate = candidates()
    outside_candidate[0]["tangent_vector"] = {"x": 0.9, "y": 0.0}
    blocked.append(build(radial_geodesic_candidates=outside_candidate))

    wrong_endpoint = candidates()
    wrong_endpoint[0]["expected_endpoint"]["x"] += 0.1
    blocked.append(build(radial_geodesic_candidates=wrong_endpoint))

    wrong_midpoint = candidates()
    wrong_midpoint[0]["expected_midpoint"]["y"] += 0.1
    blocked.append(build(radial_geodesic_candidates=wrong_midpoint))

    missing_chart = candidates()
    missing_chart[0]["assigned_chart_id"] = "missing"
    blocked.append(build(radial_geodesic_candidates=missing_chart))

    duplicate_candidate = candidates()
    duplicate_candidate[1]["candidate_id"] = duplicate_candidate[0][
        "candidate_id"
    ]
    blocked.append(build(radial_geodesic_candidates=duplicate_candidate))

    duplicate_digest = candidates()
    duplicate_digest[1]["source_candidate_digest"] = duplicate_digest[0][
        "source_candidate_digest"
    ]
    blocked.append(build(radial_geodesic_candidates=duplicate_digest))

    narrow_chart = charts()
    narrow_chart[0]["safe_radius"] = 0.1
    blocked.append(build(chart_records=narrow_chart))

    invalid_bounds = charts()
    invalid_bounds[0]["coordinate_lower_bounds"]["x"] = 2.0
    blocked.append(build(chart_records=invalid_bounds))

    near_duplicate = candidates()
    near_duplicate[1]["tangent_vector"] = {"x": 0.500001, "y": 0.2}
    near_duplicate[1]["expected_endpoint"] = {
        "x": 0.498001,
        "y": 0.19499999,
    }
    near_duplicate[1]["expected_midpoint"] = {
        "x": 0.2500005,
        "y": 0.0987499975,
    }
    blocked.append(
        build(
            radial_geodesic_candidates=near_duplicate,
            minimum_distinct_endpoint_separation=0.1,
        )
    )

    nonfinite_connection = christoffel_symbols()
    nonfinite_connection["x"]["x"]["x"] = float("nan")
    blocked.append(build(christoffel_symbols=nonfinite_connection))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(candidates())
    stale_digest = compute_local_model_input_digest(
        coordinate_schema=coordinate_schema(),
        base_point=base_point(),
        metric_matrix=metric_matrix(),
        christoffel_symbols=christoffel_symbols(),
        chart_records=charts(),
        radial_geodesic_candidates=tampered,
    )
    tampered[0]["tangent_vector"]["x"] += 0.01
    item = build(
        radial_geodesic_candidates=tampered,
        local_model_input_digest=stale_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Exponential Map and Normal Coordinate Ball Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
