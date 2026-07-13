#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_normal_ball_cover_hopf_rinow_witness_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_normal_ball_cover_hopf_rinow_witness_certificate,
    compute_finite_cover_input_digest,
)


def coordinate_schema() -> list[str]:
    return ["x", "y"]


def balls() -> list[dict]:
    return [
        {
            "ball_id": "normal-ball-a",
            "center": {"x": 0.0, "y": 0.0},
            "radius": 0.8,
            "source_injectivity_radius_lower_bound": 1.5,
            "chart_id": "normal-primary",
            "source_normal_ball_digest": "planos-v1-12-normal-ball-a",
        },
        {
            "ball_id": "normal-ball-b",
            "center": {"x": 0.9, "y": 0.0},
            "radius": 0.8,
            "source_injectivity_radius_lower_bound": 1.4,
            "chart_id": "normal-overlap",
            "source_normal_ball_digest": "planos-v1-12-normal-ball-b",
        },
    ]


def samples() -> list[dict]:
    return [
        {
            "sample_id": "sample-start",
            "point": {"x": 0.0, "y": 0.0},
            "assigned_ball_id": "normal-ball-a",
            "source_sample_digest": "sample-start-digest",
        },
        {
            "sample_id": "sample-junction",
            "point": {"x": 0.6, "y": 0.1},
            "assigned_ball_id": "normal-ball-a",
            "source_sample_digest": "sample-junction-digest",
        },
        {
            "sample_id": "sample-end",
            "point": {"x": 1.2, "y": 0.0},
            "assigned_ball_id": "normal-ball-b",
            "source_sample_digest": "sample-end-digest",
        },
    ]


def overlaps() -> list[dict]:
    return [
        {
            "overlap_id": "overlap-a-b",
            "left_ball_id": "normal-ball-a",
            "right_ball_id": "normal-ball-b",
            "witness_point": {"x": 0.6, "y": 0.1},
            "source_overlap_digest": "overlap-a-b-digest",
        }
    ]


def segments() -> list[dict]:
    return [
        {
            "segment_id": "extension-segment-0",
            "start_parameter": 0.0,
            "end_parameter": 0.7,
            "length": 0.7,
            "start_point": {"x": 0.0, "y": 0.0},
            "end_point": {"x": 0.6, "y": 0.1},
            "start_tangent": {"x": 0.8, "y": 0.1},
            "end_tangent": {"x": 0.8, "y": 0.1},
            "normal_ball_id": "normal-ball-a",
            "source_segment_digest": "extension-segment-0-digest",
        },
        {
            "segment_id": "extension-segment-1",
            "start_parameter": 0.7,
            "end_parameter": 1.4,
            "length": 0.7,
            "start_point": {"x": 0.6, "y": 0.1},
            "end_point": {"x": 1.2, "y": 0.0},
            "start_tangent": {"x": 0.8, "y": 0.1},
            "end_tangent": {"x": 0.8, "y": -0.1},
            "normal_ball_id": "normal-ball-b",
            "source_segment_digest": "extension-segment-1-digest",
        },
    ]


def build(**overrides):
    coords = overrides.pop("coordinate_schema", coordinate_schema())
    ball_records = overrides.pop("normal_ball_records", balls())
    sample_records = overrides.pop("cover_sample_points", samples())
    overlap_records = overrides.pop("overlap_records", overlaps())
    extension_segments = overrides.pop("geodesic_extension_segments", segments())
    digest = overrides.pop(
        "finite_cover_input_digest",
        compute_finite_cover_input_digest(
            coordinate_schema=coords,
            normal_ball_records=ball_records,
            cover_sample_points=sample_records,
            overlap_records=overlap_records,
            geodesic_extension_segments=extension_segments,
        ),
    )
    args = {
        "source_exponential_map_certificate_digest": (
            "planos-v1-12-exponential-map-certificate"
        ),
        "source_atlas_certificate_digest": "planos-v1-08-atlas-certificate",
        "finite_cover_input_digest": digest,
        "coordinate_schema": coords,
        "normal_ball_records": ball_records,
        "cover_sample_points": sample_records,
        "overlap_records": overlap_records,
        "geodesic_extension_segments": extension_segments,
        "finite_window_start": 0.0,
        "finite_window_end": 1.4,
        "maximum_segment_length_fraction": 0.95,
        "minimum_overlap_margin": 0.15,
        "maximum_junction_position_residual": 1e-10,
        "maximum_junction_tangent_jump": 0.25,
    }
    args.update(overrides)
    return build_finite_normal_ball_cover_hopf_rinow_witness_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["finite_window_length"] == 1.4
    assert abs(cert["computed_total_extension_length"] - 1.4) < 1e-12
    assert cert["computed_minimum_overlap_clearance"] > 0.15
    assert cert["computed_maximum_segment_radius_fraction"] < 0.95
    assert cert["computed_maximum_junction_position_residual"] < 1e-12
    assert cert["computed_maximum_junction_tangent_jump"] <= 0.25
    assert cert["finite_cover_coordinate_diameter_bound"] > 0.0
    for name in (
        "finite_normal_ball_cover_certified",
        "all_retained_samples_covered",
        "normal_ball_overlap_chain_certified",
        "local_geodesic_extension_chain_certified",
        "finite_window_fully_extended",
        "finite_cover_coordinate_bound_certified",
        "bounded_hopf_rinow_finite_window_witness",
        "classical_hopf_rinow_equivalence_not_claimed",
        "global_geodesic_completeness_not_claimed",
        "global_metric_completeness_not_claimed",
        "global_compactness_not_claimed",
        "global_minimizing_geodesic_not_claimed",
        "local_finite_witness_only",
        "source_exponential_map_certificate_not_mutated",
        "source_atlas_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "candidate_identity_retained",
        "history_read_only",
        "finite_cover_grants_no_authority",
        "geodesic_extension_grants_no_authority",
        "hopf_rinow_witness_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False
    assert all(
        sample["covered_by_assigned_normal_ball"]
        for sample in cert["cover_sample_points"]
    )
    assert all(
        segment["locally_extendible_inside_normal_ball"]
        for segment in cert["geodesic_extension_segments"]
    )

    blocked = [
        build(source_exponential_map_certificate_digest=""),
        build(source_atlas_certificate_digest=""),
        build(finite_cover_input_digest="stale"),
        build(coordinate_schema=["x", "x"]),
        build(normal_ball_records=[]),
        build(cover_sample_points=[]),
        build(geodesic_extension_segments=[]),
        build(finite_window_end=0.0),
        build(maximum_segment_length_fraction=1.0),
        build(minimum_overlap_margin=-0.1),
    ]

    invalid_radius = balls()
    invalid_radius[0]["radius"] = 1.5
    blocked.append(build(normal_ball_records=invalid_radius))

    duplicate_ball = balls()
    duplicate_ball[1]["ball_id"] = duplicate_ball[0]["ball_id"]
    blocked.append(build(normal_ball_records=duplicate_ball))

    sample_outside = samples()
    sample_outside[0]["point"] = {"x": -1.0, "y": 0.0}
    blocked.append(build(cover_sample_points=sample_outside))

    sample_missing_ball = samples()
    sample_missing_ball[0]["assigned_ball_id"] = "missing"
    blocked.append(build(cover_sample_points=sample_missing_ball))

    weak_overlap = overlaps()
    weak_overlap[0]["witness_point"] = {"x": 0.79, "y": 0.0}
    blocked.append(build(overlap_records=weak_overlap, minimum_overlap_margin=0.2))

    missing_overlap = segments()
    missing_overlap[1]["normal_ball_id"] = "normal-ball-b"
    blocked.append(build(overlap_records=[], geodesic_extension_segments=missing_overlap))

    wrong_length = segments()
    wrong_length[0]["length"] = 0.6
    blocked.append(build(geodesic_extension_segments=wrong_length))

    too_long = segments()
    too_long[0]["end_parameter"] = 0.78
    too_long[0]["length"] = 0.78
    too_long[1]["start_parameter"] = 0.78
    blocked.append(
        build(
            geodesic_extension_segments=too_long,
            finite_window_end=1.48,
            maximum_segment_length_fraction=0.95,
        )
    )

    parameter_gap = segments()
    parameter_gap[1]["start_parameter"] = 0.71
    parameter_gap[1]["length"] = 0.69
    blocked.append(build(geodesic_extension_segments=parameter_gap))

    position_gap = segments()
    position_gap[1]["start_point"] = {"x": 0.61, "y": 0.1}
    blocked.append(build(geodesic_extension_segments=position_gap))

    tangent_jump = segments()
    tangent_jump[1]["start_tangent"] = {"x": 0.0, "y": 1.0}
    blocked.append(build(geodesic_extension_segments=tangent_jump))

    wrong_end = segments()
    wrong_end[-1]["end_parameter"] = 1.3
    wrong_end[-1]["length"] = 0.6
    blocked.append(build(geodesic_extension_segments=wrong_end))

    duplicate_segment = segments()
    duplicate_segment[1]["segment_id"] = duplicate_segment[0]["segment_id"]
    blocked.append(build(geodesic_extension_segments=duplicate_segment))

    nonfinite = balls()
    nonfinite[0]["center"]["x"] = float("nan")
    blocked.append(build(normal_ball_records=nonfinite))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered = deepcopy(samples())
    stale_digest = compute_finite_cover_input_digest(
        coordinate_schema=coordinate_schema(),
        normal_ball_records=balls(),
        cover_sample_points=tampered,
        overlap_records=overlaps(),
        geodesic_extension_segments=segments(),
    )
    tampered[0]["point"]["x"] += 0.01
    item = build(
        cover_sample_points=tampered,
        finite_cover_input_digest=stale_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS Finite Normal-Ball Cover and Bounded Hopf-Rinow "
        "Witness Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
