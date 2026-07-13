#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_conjugate_event_sequence_injectivity_radius_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_conjugate_event_sequence_injectivity_radius_certificate,
    compute_event_sequence_input_digest,
)


def coordinates() -> list[str]:
    return ["x", "y"]


def segments() -> list[dict]:
    return [
        {
            "segment_id": "segment-0",
            "start_parameter": 0.0,
            "end_parameter": 1.5,
            "length": 1.5,
            "start_point": {"x": 0.0, "y": 0.0},
            "end_point": {"x": 1.5, "y": 0.0},
            "start_tangent": {"x": 1.0, "y": 0.0},
            "end_tangent": {"x": 1.0, "y": 0.0},
            "source_segment_digest": "source-segment-0",
        },
        {
            "segment_id": "segment-1",
            "start_parameter": 1.5,
            "end_parameter": 3.0,
            "length": 1.5,
            "start_point": {"x": 1.5, "y": 0.0},
            "end_point": {"x": 3.0, "y": 0.0},
            "start_tangent": {"x": 1.0, "y": 0.0},
            "end_tangent": {"x": 1.0, "y": 0.0},
            "source_segment_digest": "source-segment-1",
        },
    ]


def events() -> list[dict]:
    return [
        {
            "event_id": "conjugate-2",
            "parameter": 2.0,
            "multiplicity": 1,
            "morse_index_before": 0,
            "morse_index_after": 1,
            "nullity_at_event": 1,
            "source_event_digest": "source-event-2",
        }
    ]


def cuts() -> list[dict]:
    return [
        {
            "candidate_id": "cut-conjugate-2",
            "parameter": 2.0,
            "cause": "conjugate",
            "competing_geodesic_count": 1,
            "endpoint_distance": 2.0,
            "matched_event_id": "conjugate-2",
            "source_candidate_digest": "source-cut-conjugate-2",
        },
        {
            "candidate_id": "cut-multiple-25",
            "parameter": 2.5,
            "cause": "multiple_geodesic",
            "competing_geodesic_count": 2,
            "endpoint_distance": 2.5,
            "matched_event_id": "",
            "source_candidate_digest": "source-cut-multiple-25",
        },
    ]


def build(**overrides):
    coords = overrides.pop("coordinate_schema", coordinates())
    segs = overrides.pop("piecewise_geodesic_segments", segments())
    evs = overrides.pop("conjugate_events", events())
    cut_candidates = overrides.pop("cut_locus_candidates", cuts())
    digest = overrides.pop(
        "event_sequence_input_digest",
        compute_event_sequence_input_digest(
            coordinates=coords,
            segments=segs,
            conjugate_events=evs,
            cut_locus_candidates=cut_candidates,
        ),
    )
    args = {
        "source_morse_index_certificate_digest": "planos-v1-10-morse-index-certificate",
        "event_sequence_input_digest": digest,
        "coordinate_schema": coords,
        "piecewise_geodesic_segments": segs,
        "conjugate_events": evs,
        "cut_locus_candidates": cut_candidates,
        "window_start_parameter": 0.0,
        "window_end_parameter": 3.0,
        "initial_morse_index": 0,
        "expected_final_morse_index": 1,
        "local_injectivity_radius_lower_bound": 1.5,
        "maximum_junction_position_residual": 1e-8,
        "maximum_junction_tangent_jump": 1e-8,
    }
    args.update(overrides)
    return build_conjugate_event_sequence_injectivity_radius_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["final_morse_index"] == 1
    assert cert["total_conjugate_multiplicity"] == 1
    assert cert["earliest_conjugate_event_parameter"] == 2.0
    assert cert["earliest_cut_locus_candidate_parameter"] == 2.0
    assert cert["first_obstruction_parameter"] == 2.0
    assert cert["local_injectivity_radius_lower_bound"] == 1.5
    assert cert["event_free_through_parameter"] == 1.5
    for name in (
        "piecewise_geodesic_segments_contiguous",
        "junction_position_compatible",
        "junction_tangent_jump_bounded",
        "conjugate_event_sequence_strictly_ordered",
        "morse_index_jump_matches_multiplicity",
        "event_nullity_matches_multiplicity",
        "finite_window_morse_index_consistent",
        "cut_locus_candidates_retained",
        "injectivity_radius_lower_bound_certified",
        "conjugate_events_local_only",
        "cut_locus_candidates_local_only",
        "injectivity_radius_bound_local_only",
        "candidate_identity_retained",
        "source_morse_index_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "morse_index_grants_no_authority",
        "conjugate_event_grants_no_authority",
        "cut_locus_grants_no_authority",
        "injectivity_radius_grants_no_authority",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["decision_selection_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    blocked = []
    blocked.append(build(source_morse_index_certificate_digest=""))
    blocked.append(build(event_sequence_input_digest="stale"))
    blocked.append(build(coordinate_schema=["x", "x"]))

    bad_segments = segments()
    bad_segments[1]["start_parameter"] = 1.6
    blocked.append(build(piecewise_geodesic_segments=bad_segments))

    bad_position = segments()
    bad_position[1]["start_point"]["x"] = 1.6
    blocked.append(build(piecewise_geodesic_segments=bad_position))

    bad_tangent = segments()
    bad_tangent[1]["start_tangent"]["y"] = 0.2
    blocked.append(build(piecewise_geodesic_segments=bad_tangent))

    duplicate_segment = segments()
    duplicate_segment[1]["segment_id"] = duplicate_segment[0]["segment_id"]
    blocked.append(build(piecewise_geodesic_segments=duplicate_segment))

    bad_jump = events()
    bad_jump[0]["morse_index_after"] = 2
    blocked.append(build(conjugate_events=bad_jump))

    bad_nullity = events()
    bad_nullity[0]["nullity_at_event"] = 2
    blocked.append(build(conjugate_events=bad_nullity))

    duplicate_event = events() + [deepcopy(events()[0])]
    duplicate_event[1]["event_id"] = "conjugate-2b"
    duplicate_event[1]["source_event_digest"] = "source-event-2b"
    blocked.append(build(conjugate_events=duplicate_event))

    early_event = events()
    early_event[0]["parameter"] = 1.0
    blocked.append(build(conjugate_events=early_event))

    unmatched_cut = cuts()
    unmatched_cut[0]["matched_event_id"] = "missing"
    blocked.append(build(cut_locus_candidates=unmatched_cut))

    weak_multiple = cuts()
    weak_multiple[1]["competing_geodesic_count"] = 1
    blocked.append(build(cut_locus_candidates=weak_multiple))

    invalid_cause = cuts()
    invalid_cause[0]["cause"] = "unknown"
    blocked.append(build(cut_locus_candidates=invalid_cause))

    early_cut = cuts()
    early_cut[0]["parameter"] = 1.0
    early_cut[0]["matched_event_id"] = ""
    early_cut[0]["cause"] = "multiple_geodesic"
    early_cut[0]["competing_geodesic_count"] = 2
    blocked.append(build(cut_locus_candidates=early_cut))

    blocked.append(build(expected_final_morse_index=2))
    blocked.append(build(local_injectivity_radius_lower_bound=2.1))
    blocked.append(build(window_end_parameter=2.5))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print(
        "PASS: PlanOS Conjugate Event Sequence and Injectivity Radius Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
