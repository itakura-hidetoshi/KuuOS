#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-9


@dataclass
class ConjugateEventSequenceInjectivityRadiusCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: float, right: float, tolerance: float = TOL) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def _vector_ok(name: str, value: Any, coordinates: Sequence[str]) -> tuple[list[str], dict]:
    if not isinstance(value, dict) or set(value) != set(coordinates):
        return [f"{name}_schema_invalid"], {}
    if any(not finite(value[c]) for c in coordinates):
        return [f"{name}_nonfinite"], {}
    return [], {c: float(value[c]) for c in coordinates}


def _max_vector_residual(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    return max((abs(float(left[c]) - float(right[c])) for c in left), default=0.0)


def _normalize_segments(
    segments: Any,
    coordinates: Sequence[str],
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(segments, list) or not segments:
        return ["piecewise_segments_empty"], []
    fields = {
        "segment_id",
        "start_parameter",
        "end_parameter",
        "length",
        "start_point",
        "end_point",
        "start_tangent",
        "end_tangent",
        "source_segment_digest",
    }
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    out: list[dict] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or set(segment) != fields:
            blockers.append(f"piecewise_segment_schema_invalid_{index}")
            continue
        sid = segment["segment_id"]
        digest = segment["source_segment_digest"]
        if not isinstance(sid, str) or not sid:
            blockers.append(f"segment_id_invalid_{index}")
            continue
        if sid in seen_ids:
            blockers.append("duplicate_segment_id")
        seen_ids.add(sid)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"source_segment_digest_missing_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_source_segment_digest")
        else:
            seen_digests.add(digest)
        numeric_names = ("start_parameter", "end_parameter", "length")
        if any(not finite(segment[name]) for name in numeric_names):
            blockers.append(f"segment_nonfinite_scalar_{index}")
            continue
        start = float(segment["start_parameter"])
        end = float(segment["end_parameter"])
        length = float(segment["length"])
        if end <= start:
            blockers.append(f"segment_parameter_order_invalid_{sid}")
        if length <= 0.0:
            blockers.append(f"segment_length_nonpositive_{sid}")
        if not close(length, end - start):
            blockers.append(f"segment_length_parameter_mismatch_{sid}")
        normalized = {
            "segment_id": sid,
            "start_parameter": start,
            "end_parameter": end,
            "length": length,
            "source_segment_digest": digest,
        }
        bad = False
        for name in ("start_point", "end_point", "start_tangent", "end_tangent"):
            errors, vector = _vector_ok(f"segment_{name}_{sid}", segment[name], coordinates)
            blockers.extend(errors)
            bad = bad or bool(errors)
            normalized[name] = vector
        if not bad:
            out.append(normalized)
    out.sort(key=lambda item: (item["start_parameter"], item["segment_id"]))
    return blockers, out


def _normalize_events(events: Any) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(events, list):
        return ["conjugate_events_not_list"], []
    fields = {
        "event_id",
        "parameter",
        "multiplicity",
        "morse_index_before",
        "morse_index_after",
        "nullity_at_event",
        "source_event_digest",
    }
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    out: list[dict] = []
    for index, event in enumerate(events):
        if not isinstance(event, dict) or set(event) != fields:
            blockers.append(f"conjugate_event_schema_invalid_{index}")
            continue
        eid = event["event_id"]
        digest = event["source_event_digest"]
        if not isinstance(eid, str) or not eid:
            blockers.append(f"event_id_invalid_{index}")
            continue
        if eid in seen_ids:
            blockers.append("duplicate_event_id")
        seen_ids.add(eid)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"source_event_digest_missing_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_source_event_digest")
        else:
            seen_digests.add(digest)
        if not finite(event["parameter"]):
            blockers.append(f"event_parameter_nonfinite_{eid}")
            continue
        integer_names = (
            "multiplicity",
            "morse_index_before",
            "morse_index_after",
            "nullity_at_event",
        )
        if any(
            not isinstance(event[name], int) or isinstance(event[name], bool)
            for name in integer_names
        ):
            blockers.append(f"event_integer_field_invalid_{eid}")
            continue
        normalized = {
            "event_id": eid,
            "parameter": float(event["parameter"]),
            "multiplicity": int(event["multiplicity"]),
            "morse_index_before": int(event["morse_index_before"]),
            "morse_index_after": int(event["morse_index_after"]),
            "nullity_at_event": int(event["nullity_at_event"]),
            "source_event_digest": digest,
        }
        if normalized["multiplicity"] <= 0:
            blockers.append(f"event_multiplicity_nonpositive_{eid}")
        if min(
            normalized["morse_index_before"],
            normalized["morse_index_after"],
            normalized["nullity_at_event"],
        ) < 0:
            blockers.append(f"event_negative_index_or_nullity_{eid}")
        out.append(normalized)
    out.sort(key=lambda item: (item["parameter"], item["event_id"]))
    return blockers, out


def _normalize_cut_candidates(candidates: Any) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(candidates, list):
        return ["cut_locus_candidates_not_list"], []
    fields = {
        "candidate_id",
        "parameter",
        "cause",
        "competing_geodesic_count",
        "endpoint_distance",
        "matched_event_id",
        "source_candidate_digest",
    }
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    out: list[dict] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict) or set(candidate) != fields:
            blockers.append(f"cut_candidate_schema_invalid_{index}")
            continue
        cid = candidate["candidate_id"]
        digest = candidate["source_candidate_digest"]
        cause = candidate["cause"]
        if not isinstance(cid, str) or not cid:
            blockers.append(f"cut_candidate_id_invalid_{index}")
            continue
        if cid in seen_ids:
            blockers.append("duplicate_cut_candidate_id")
        seen_ids.add(cid)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"source_cut_candidate_digest_missing_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_source_cut_candidate_digest")
        else:
            seen_digests.add(digest)
        if cause not in {"conjugate", "multiple_geodesic"}:
            blockers.append(f"cut_candidate_cause_invalid_{cid}")
        if not finite(candidate["parameter"]) or not finite(candidate["endpoint_distance"]):
            blockers.append(f"cut_candidate_nonfinite_{cid}")
            continue
        count = candidate["competing_geodesic_count"]
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            blockers.append(f"competing_geodesic_count_invalid_{cid}")
            continue
        matched_event_id = candidate["matched_event_id"]
        if not isinstance(matched_event_id, str):
            blockers.append(f"matched_event_id_invalid_{cid}")
            continue
        out.append(
            {
                "candidate_id": cid,
                "parameter": float(candidate["parameter"]),
                "cause": cause,
                "competing_geodesic_count": count,
                "endpoint_distance": float(candidate["endpoint_distance"]),
                "matched_event_id": matched_event_id,
                "source_candidate_digest": digest,
            }
        )
    out.sort(key=lambda item: (item["parameter"], item["candidate_id"]))
    return blockers, out


def compute_event_sequence_input_digest(
    *,
    coordinates: Sequence[str],
    segments: Sequence[Mapping[str, Any]],
    conjugate_events: Sequence[Mapping[str, Any]],
    cut_locus_candidates: Sequence[Mapping[str, Any]],
) -> str:
    return canonical_digest(
        {
            "coordinates": list(coordinates),
            "segments": list(segments),
            "conjugate_events": list(conjugate_events),
            "cut_locus_candidates": list(cut_locus_candidates),
        }
    )


def build_conjugate_event_sequence_injectivity_radius_certificate(
    *,
    source_morse_index_certificate_digest: str,
    event_sequence_input_digest: str,
    coordinate_schema: list[str],
    piecewise_geodesic_segments: list[dict],
    conjugate_events: list[dict],
    cut_locus_candidates: list[dict],
    window_start_parameter: float,
    window_end_parameter: float,
    initial_morse_index: int,
    expected_final_morse_index: int,
    local_injectivity_radius_lower_bound: float,
    maximum_junction_position_residual: float,
    maximum_junction_tangent_jump: float,
) -> ConjugateEventSequenceInjectivityRadiusCertificateResult:
    blockers: list[str] = []
    if not isinstance(source_morse_index_certificate_digest, str) or not source_morse_index_certificate_digest:
        blockers.append("source_morse_index_certificate_digest_missing")
    if not isinstance(event_sequence_input_digest, str) or not event_sequence_input_digest:
        blockers.append("event_sequence_input_digest_missing")
    if (
        not isinstance(coordinate_schema, list)
        or not coordinate_schema
        or any(not isinstance(c, str) or not c for c in coordinate_schema)
        or len(set(coordinate_schema)) != len(coordinate_schema)
    ):
        blockers.append("coordinate_schema_invalid")
        coordinates: list[str] = []
    else:
        coordinates = list(coordinate_schema)
    for name, value in {
        "window_start_parameter": window_start_parameter,
        "window_end_parameter": window_end_parameter,
        "local_injectivity_radius_lower_bound": local_injectivity_radius_lower_bound,
        "maximum_junction_position_residual": maximum_junction_position_residual,
        "maximum_junction_tangent_jump": maximum_junction_tangent_jump,
    }.items():
        if not finite(value):
            blockers.append(f"{name}_invalid")
    if finite(window_start_parameter) and finite(window_end_parameter):
        if float(window_end_parameter) <= float(window_start_parameter):
            blockers.append("window_parameter_order_invalid")
    if finite(local_injectivity_radius_lower_bound) and float(local_injectivity_radius_lower_bound) <= 0.0:
        blockers.append("local_injectivity_radius_lower_bound_nonpositive")
    if finite(maximum_junction_position_residual) and float(maximum_junction_position_residual) < 0.0:
        blockers.append("maximum_junction_position_residual_negative")
    if finite(maximum_junction_tangent_jump) and float(maximum_junction_tangent_jump) < 0.0:
        blockers.append("maximum_junction_tangent_jump_negative")
    for name, value in {
        "initial_morse_index": initial_morse_index,
        "expected_final_morse_index": expected_final_morse_index,
    }.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"{name}_invalid")

    segment_errors, segments = _normalize_segments(piecewise_geodesic_segments, coordinates)
    event_errors, events = _normalize_events(conjugate_events)
    cut_errors, cuts = _normalize_cut_candidates(cut_locus_candidates)
    blockers.extend(segment_errors)
    blockers.extend(event_errors)
    blockers.extend(cut_errors)
    if blockers:
        return ConjugateEventSequenceInjectivityRadiusCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    expected_digest = compute_event_sequence_input_digest(
        coordinates=coordinates,
        segments=segments,
        conjugate_events=events,
        cut_locus_candidates=cuts,
    )
    if event_sequence_input_digest != expected_digest:
        blockers.append("event_sequence_input_digest_mismatch")

    window_start = float(window_start_parameter)
    window_end = float(window_end_parameter)
    if not close(segments[0]["start_parameter"], window_start):
        blockers.append("first_segment_does_not_start_at_window_start")
    if not close(segments[-1]["end_parameter"], window_end):
        blockers.append("last_segment_does_not_end_at_window_end")

    max_position_residual = 0.0
    max_tangent_jump = 0.0
    for left, right in zip(segments, segments[1:]):
        if not close(left["end_parameter"], right["start_parameter"]):
            blockers.append(f"segment_parameter_gap_or_overlap_{left['segment_id']}_{right['segment_id']}")
        position_residual = _max_vector_residual(left["end_point"], right["start_point"])
        tangent_jump = _max_vector_residual(left["end_tangent"], right["start_tangent"])
        max_position_residual = max(max_position_residual, position_residual)
        max_tangent_jump = max(max_tangent_jump, tangent_jump)
        if position_residual > float(maximum_junction_position_residual) + TOL:
            blockers.append(f"junction_position_residual_exceeded_{left['segment_id']}_{right['segment_id']}")
        if tangent_jump > float(maximum_junction_tangent_jump) + TOL:
            blockers.append(f"junction_tangent_jump_exceeded_{left['segment_id']}_{right['segment_id']}")

    total_segment_length = sum(segment["length"] for segment in segments)
    if not close(total_segment_length, window_end - window_start):
        blockers.append("piecewise_segment_total_length_mismatch")

    current_index = int(initial_morse_index)
    previous_parameter: float | None = None
    event_ids = {event["event_id"] for event in events}
    for event in events:
        parameter = event["parameter"]
        eid = event["event_id"]
        if not (window_start < parameter <= window_end):
            blockers.append(f"event_outside_window_{eid}")
        if previous_parameter is not None and parameter <= previous_parameter + TOL:
            blockers.append("conjugate_event_parameters_not_strictly_increasing")
        previous_parameter = parameter
        if event["morse_index_before"] != current_index:
            blockers.append(f"morse_index_chain_before_mismatch_{eid}")
        if event["morse_index_after"] - event["morse_index_before"] != event["multiplicity"]:
            blockers.append(f"morse_index_jump_multiplicity_mismatch_{eid}")
        if event["nullity_at_event"] != event["multiplicity"]:
            blockers.append(f"event_nullity_multiplicity_mismatch_{eid}")
        current_index = event["morse_index_after"]
    if current_index != int(expected_final_morse_index):
        blockers.append("final_morse_index_mismatch")

    earliest_event_parameter = min((event["parameter"] for event in events), default=math.inf)
    earliest_cut_parameter = min((cut["parameter"] for cut in cuts), default=math.inf)
    for cut in cuts:
        cid = cut["candidate_id"]
        parameter = cut["parameter"]
        if not (window_start < parameter <= window_end):
            blockers.append(f"cut_candidate_outside_window_{cid}")
        if cut["endpoint_distance"] < 0.0:
            blockers.append(f"cut_candidate_endpoint_distance_negative_{cid}")
        if cut["cause"] == "conjugate":
            if cut["matched_event_id"] not in event_ids:
                blockers.append(f"conjugate_cut_candidate_unmatched_{cid}")
            else:
                matched = next(event for event in events if event["event_id"] == cut["matched_event_id"])
                if not close(parameter, matched["parameter"]):
                    blockers.append(f"conjugate_cut_candidate_parameter_mismatch_{cid}")
            if cut["competing_geodesic_count"] != 1:
                blockers.append(f"conjugate_cut_candidate_count_invalid_{cid}")
        elif cut["cause"] == "multiple_geodesic":
            if cut["competing_geodesic_count"] < 2:
                blockers.append(f"multiple_geodesic_cut_candidate_count_invalid_{cid}")
            if cut["matched_event_id"]:
                blockers.append(f"multiple_geodesic_cut_candidate_should_not_match_event_{cid}")

    first_obstruction_parameter = min(earliest_event_parameter, earliest_cut_parameter)
    lower_bound = float(local_injectivity_radius_lower_bound)
    absolute_lower_bound_parameter = window_start + lower_bound
    if absolute_lower_bound_parameter > window_end + TOL:
        blockers.append("injectivity_radius_lower_bound_exceeds_window")
    if first_obstruction_parameter < absolute_lower_bound_parameter - TOL:
        blockers.append("obstruction_before_injectivity_radius_lower_bound")

    if blockers:
        return ConjugateEventSequenceInjectivityRadiusCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": "PlanOS Conjugate Event Sequence and Injectivity Radius Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.11",
        "source_morse_index_certificate_digest": source_morse_index_certificate_digest,
        "event_sequence_input_digest": event_sequence_input_digest,
        "coordinate_schema": coordinates,
        "piecewise_geodesic_segments": segments,
        "conjugate_events": events,
        "cut_locus_candidates": cuts,
        "window_start_parameter": window_start,
        "window_end_parameter": window_end,
        "initial_morse_index": int(initial_morse_index),
        "final_morse_index": current_index,
        "expected_final_morse_index": int(expected_final_morse_index),
        "total_conjugate_multiplicity": sum(event["multiplicity"] for event in events),
        "earliest_conjugate_event_parameter": (
            None if math.isinf(earliest_event_parameter) else earliest_event_parameter
        ),
        "earliest_cut_locus_candidate_parameter": (
            None if math.isinf(earliest_cut_parameter) else earliest_cut_parameter
        ),
        "first_obstruction_parameter": (
            None if math.isinf(first_obstruction_parameter) else first_obstruction_parameter
        ),
        "local_injectivity_radius_lower_bound": lower_bound,
        "event_free_through_parameter": absolute_lower_bound_parameter,
        "computed_total_segment_length": total_segment_length,
        "computed_maximum_junction_position_residual": max_position_residual,
        "computed_maximum_junction_tangent_jump": max_tangent_jump,
        "piecewise_geodesic_segments_contiguous": True,
        "junction_position_compatible": True,
        "junction_tangent_jump_bounded": True,
        "conjugate_event_sequence_strictly_ordered": True,
        "morse_index_jump_matches_multiplicity": True,
        "event_nullity_matches_multiplicity": True,
        "finite_window_morse_index_consistent": True,
        "cut_locus_candidates_retained": True,
        "injectivity_radius_lower_bound_certified": True,
        "conjugate_events_local_only": True,
        "cut_locus_candidates_local_only": True,
        "injectivity_radius_bound_local_only": True,
        "candidate_identity_retained": True,
        "source_morse_index_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "morse_index_grants_no_authority": True,
        "conjugate_event_grants_no_authority": True,
        "cut_locus_grants_no_authority": True,
        "injectivity_radius_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["event_sequence_certificate_digest"] = canonical_digest(certificate)
    return ConjugateEventSequenceInjectivityRadiusCertificateResult(
        STATUS_READY, [], certificate
    )
