from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_qi_healing_potential_diagnostic_types_v0_28 import (
    DIAGNOSTIC_ROUTES,
    HEALING_POTENTIAL_CLASSES,
    HYPOTHESIS_FIELDS,
    NON_AUTHORITY_FLAGS,
    PACKET_VERSION,
    PROCESS_HISTORY_FIELDS,
    REPORT_VERSION,
    REQUIRED_BOUNDARY,
    average,
    clamp01,
    copy_boundary,
    copy_non_authority,
    packet_digest,
    report_digest,
    require_bool,
    require_bounded,
    require_nonnegative_int,
    require_sequence,
    require_string,
    require_string_list,
)


def build_diagnostic_packet(
    *,
    packet_id: str,
    context_digest: str,
    source_v027_state_digest: str,
    qi_process_tensor_receipt_digest: str,
    qi_observation_candidate_digest: str,
    process_tensor_visible: bool,
    process_history: list[Mapping[str, Any]],
    diagnostic_hypotheses: list[Mapping[str, Any]],
    red_flags: list[str],
    source_coverage: float,
    temporal_coverage: float,
    contradiction_visibility: float,
    created_at_ms: int,
) -> dict[str, Any]:
    packet = {
        "version": PACKET_VERSION,
        "packet_id": require_string(packet_id, "packet_id"),
        "context_digest": require_string(context_digest, "context_digest"),
        "source_v027_state_digest": require_string(
            source_v027_state_digest, "source_v027_state_digest"
        ),
        "qi_process_tensor_receipt_digest": require_string(
            qi_process_tensor_receipt_digest, "qi_process_tensor_receipt_digest"
        ),
        "qi_observation_candidate_digest": require_string(
            qi_observation_candidate_digest, "qi_observation_candidate_digest"
        ),
        "process_tensor_visible": require_bool(
            process_tensor_visible, "process_tensor_visible"
        ),
        "process_history": [deepcopy(dict(item)) for item in process_history],
        "diagnostic_hypotheses": [
            deepcopy(dict(item)) for item in diagnostic_hypotheses
        ],
        "red_flags": list(red_flags),
        "data_quality": {
            "source_coverage": require_bounded(
                source_coverage, "source_coverage", 0.0, 1.0
            ),
            "temporal_coverage": require_bounded(
                temporal_coverage, "temporal_coverage", 0.0, 1.0
            ),
            "contradiction_visibility": require_bounded(
                contradiction_visibility,
                "contradiction_visibility",
                0.0,
                1.0,
            ),
        },
        "candidate_only": True,
        "clinical_review_required": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "diagnostic_packet_digest": "",
    }
    packet["diagnostic_packet_digest"] = packet_digest(packet)
    errors = validate_diagnostic_packet(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def _validate_history_item(
    item: Mapping[str, Any], index: int, previous_time: int | None
) -> tuple[list[str], int | None]:
    errors: list[str] = []
    for field in PROCESS_HISTORY_FIELDS:
        if field not in item:
            errors.append(f"process_history[{index}].{field}_required")
    try:
        time_index = require_nonnegative_int(
            item.get("time_index"), f"process_history_{index}_time_index"
        )
        if previous_time is not None and time_index <= previous_time:
            errors.append(f"process_history[{index}].time_index_not_increasing")
        require_string(
            item.get("observation_id"), f"process_history_{index}_observation_id"
        )
        for field in (
            "qi_recoverability_margin",
            "qi_coherence_margin",
            "qi_transport_distortion",
            "qi_tail_residue",
            "qi_memory_gain",
            "adaptive_stability",
            "intervention_burden",
        ):
            require_bounded(
                item.get(field), f"process_history_{index}_{field}", 0.0, 1.0
            )
        require_bounded(
            item.get("response_delta"),
            f"process_history_{index}_response_delta",
            -1.0,
            1.0,
        )
        if item.get("bounded_intervention") is not True:
            errors.append(f"process_history[{index}].bounded_intervention_required")
        if item.get("backaction_visible") is not True:
            errors.append(f"process_history[{index}].backaction_visible_required")
        require_string(
            item.get("source_trace"), f"process_history_{index}_source_trace"
        )
        return errors, time_index
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
        return errors, previous_time


def _validate_hypothesis(item: Mapping[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    for field in HYPOTHESIS_FIELDS:
        if field not in item:
            errors.append(f"diagnostic_hypotheses[{index}].{field}_required")
    try:
        require_string(
            item.get("hypothesis_id"), f"hypothesis_{index}_hypothesis_id"
        )
        require_string(item.get("label"), f"hypothesis_{index}_label")
        for field in ("support", "counterevidence", "uncertainty", "severity"):
            require_bounded(item.get(field), f"hypothesis_{index}_{field}", 0.0, 1.0)
        if item.get("candidate_only") is not True:
            errors.append(f"diagnostic_hypotheses[{index}].candidate_only_required")
        require_string_list(
            item.get("source_traces"),
            f"hypothesis_{index}_source_traces",
            allow_empty=False,
        )
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_diagnostic_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if packet.get("version") != PACKET_VERSION:
            errors.append("diagnostic_packet_version_invalid")
        for field in (
            "packet_id",
            "context_digest",
            "source_v027_state_digest",
            "qi_process_tensor_receipt_digest",
            "qi_observation_candidate_digest",
        ):
            require_string(packet.get(field), field)
        require_bool(packet.get("process_tensor_visible"), "process_tensor_visible")
        history = require_sequence(packet.get("process_history"), "process_history")
        seen_observations: set[str] = set()
        previous_time: int | None = None
        for index, raw in enumerate(history):
            if not isinstance(raw, Mapping):
                errors.append(f"process_history[{index}]_mapping_required")
                continue
            item_errors, new_time = _validate_history_item(raw, index, previous_time)
            errors.extend(item_errors)
            previous_time = new_time
            observation_id = str(raw.get("observation_id", ""))
            if observation_id in seen_observations:
                errors.append(f"process_history[{index}].observation_id_duplicate")
            seen_observations.add(observation_id)
        hypotheses = require_sequence(
            packet.get("diagnostic_hypotheses"), "diagnostic_hypotheses"
        )
        seen_hypotheses: set[str] = set()
        for index, raw in enumerate(hypotheses):
            if not isinstance(raw, Mapping):
                errors.append(f"diagnostic_hypotheses[{index}]_mapping_required")
                continue
            errors.extend(_validate_hypothesis(raw, index))
            hypothesis_id = str(raw.get("hypothesis_id", ""))
            if hypothesis_id in seen_hypotheses:
                errors.append(
                    f"diagnostic_hypotheses[{index}].hypothesis_id_duplicate"
                )
            seen_hypotheses.add(hypothesis_id)
        require_string_list(packet.get("red_flags"), "red_flags", allow_empty=True)
        quality = packet.get("data_quality")
        if not isinstance(quality, Mapping):
            errors.append("data_quality_mapping_required")
        else:
            for field in (
                "source_coverage",
                "temporal_coverage",
                "contradiction_visibility",
            ):
                require_bounded(quality.get(field), field, 0.0, 1.0)
        if packet.get("candidate_only") is not True:
            errors.append("diagnostic_candidate_only_required")
        if packet.get("clinical_review_required") is not True:
            errors.append("diagnostic_clinical_review_required")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("diagnostic_authority_expansion")
        if dict(packet.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("diagnostic_boundary_invalid")
        require_nonnegative_int(packet.get("created_at_ms"), "created_at_ms")
        if packet.get("diagnostic_packet_digest") != packet_digest(packet):
            errors.append("diagnostic_packet_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _process_metrics(history: list[Mapping[str, Any]]) -> dict[str, Any]:
    recoverability = [float(item["qi_recoverability_margin"]) for item in history]
    coherence = [float(item["qi_coherence_margin"]) for item in history]
    distortion = [float(item["qi_transport_distortion"]) for item in history]
    residue = [float(item["qi_tail_residue"]) for item in history]
    memory_gain = [float(item["qi_memory_gain"]) for item in history]
    response = [float(item["response_delta"]) for item in history]
    stability = [float(item["adaptive_stability"]) for item in history]
    intervention_burden = [float(item["intervention_burden"]) for item in history]

    positive_responses = [max(0.0, value) for value in response]
    negative_responses = [max(0.0, -value) for value in response]
    recovery_slope = recoverability[-1] - recoverability[0]
    coherence_slope = coherence[-1] - coherence[0]
    reopening_credit = clamp01(0.5 + 0.5 * average([recovery_slope, coherence_slope]))

    support_score = clamp01(
        0.24 * average(recoverability)
        + 0.18 * average(coherence)
        + 0.14 * average(positive_responses)
        + 0.12 * average(stability)
        + 0.10 * average(memory_gain)
        + 0.10 * (1.0 - average(distortion))
        + 0.07 * (1.0 - average(residue))
        + 0.05 * reopening_credit
    )
    burden_score = clamp01(
        0.30 * average(intervention_burden)
        + 0.25 * average(distortion)
        + 0.20 * average(residue)
        + 0.15 * average(negative_responses)
        + 0.10 * (1.0 - average(stability))
    )
    center = clamp01(support_score - 0.35 * burden_score)
    return {
        "support_score": support_score,
        "burden_score": burden_score,
        "center": center,
        "average_recoverability": average(recoverability),
        "average_coherence": average(coherence),
        "average_transport_distortion": average(distortion),
        "average_tail_residue": average(residue),
        "average_memory_gain": average(memory_gain),
        "positive_response_count": sum(1 for value in response if value > 0.0),
        "negative_response_count": sum(1 for value in response if value < 0.0),
        "recovery_slope": recovery_slope,
        "coherence_slope": coherence_slope,
        "reopening_credit": reopening_credit,
    }


def _hypothesis_summary(hypotheses: list[Mapping[str, Any]]) -> dict[str, Any]:
    ranked = sorted(
        (
            {
                "hypothesis_id": str(item["hypothesis_id"]),
                "label": str(item["label"]),
                "support": float(item["support"]),
                "counterevidence": float(item["counterevidence"]),
                "uncertainty": float(item["uncertainty"]),
                "severity": float(item["severity"]),
                "candidate_only": True,
                "source_traces": list(item["source_traces"]),
                "net_support": clamp01(
                    float(item["support"])
                    * (1.0 - 0.5 * float(item["counterevidence"]))
                    * (1.0 - 0.5 * float(item["uncertainty"]))
                ),
            }
            for item in hypotheses
        ),
        key=lambda item: (-item["net_support"], item["hypothesis_id"]),
    )
    leading = ranked[0] if ranked else None
    return {
        "plural_hypotheses": ranked,
        "leading_hypothesis_id": leading["hypothesis_id"] if leading else "",
        "leading_hypothesis_is_truth": False,
        "single_winner_forced": False,
        "severity_used_as_irreversibility": False,
        "counterevidence_preserved": True,
    }


def evaluate_diagnostic_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_diagnostic_packet(packet)
    history_raw = packet.get("process_history", [])
    history = [item for item in history_raw if isinstance(item, Mapping)]
    hypotheses_raw = packet.get("diagnostic_hypotheses", [])
    hypotheses = [item for item in hypotheses_raw if isinstance(item, Mapping)]
    red_flags = list(packet.get("red_flags", []))
    quality = packet.get("data_quality", {})
    if not isinstance(quality, Mapping):
        quality = {}

    process = _process_metrics(history) if history else {
        "support_score": 0.0,
        "burden_score": 1.0,
        "center": 0.0,
        "average_recoverability": 0.0,
        "average_coherence": 0.0,
        "average_transport_distortion": 1.0,
        "average_tail_residue": 1.0,
        "average_memory_gain": 0.0,
        "positive_response_count": 0,
        "negative_response_count": 0,
        "recovery_slope": 0.0,
        "coherence_slope": 0.0,
        "reopening_credit": 0.0,
    }
    hypothesis_summary = _hypothesis_summary(hypotheses)

    history_credit = min(1.0, len(history) / 5.0)
    evidence_quality = clamp01(
        0.30 * history_credit
        + 0.25 * float(quality.get("source_coverage", 0.0))
        + 0.25 * float(quality.get("temporal_coverage", 0.0))
        + 0.20 * float(quality.get("contradiction_visibility", 0.0))
    )
    interval_half_width = 0.10 + 0.35 * (1.0 - evidence_quality)
    center = float(process["center"])
    lower = clamp01(center - interval_half_width)
    upper = clamp01(center + interval_half_width)

    if red_flags:
        classification = "CLINICIAN_REVIEW_REQUIRED"
        route = "CLINICIAN_REVIEW_HANDOFF"
    elif errors or not packet.get("process_tensor_visible") or len(history) < 3:
        classification = "INSUFFICIENT_EVIDENCE"
        route = "REOBSERVE"
    elif evidence_quality < 0.45:
        classification = "HEALING_POTENTIAL_UNCERTAIN"
        route = "PRESERVE_PLURAL_HYPOTHESES"
    elif lower >= 0.40 and int(process["positive_response_count"]) >= 1:
        classification = "HEALING_POTENTIAL_VISIBLE"
        route = "EVALUATE_RECOVERY_WINDOW"
    elif upper < 0.35:
        classification = "HEALING_POTENTIAL_CONSTRAINED"
        route = "HOLD"
    else:
        classification = "HEALING_POTENTIAL_UNCERTAIN"
        route = "PRESERVE_PLURAL_HYPOTHESES"

    if classification not in HEALING_POTENTIAL_CLASSES:
        raise ValueError("healing_potential_class_invalid")
    if route not in DIAGNOSTIC_ROUTES:
        raise ValueError("diagnostic_route_invalid")

    supporting_factors: list[str] = []
    constraining_factors: list[str] = []
    if float(process["average_recoverability"]) >= 0.55:
        supporting_factors.append("recoverability_margin_visible")
    if float(process["average_coherence"]) >= 0.55:
        supporting_factors.append("coherence_margin_visible")
    if int(process["positive_response_count"]) > 0:
        supporting_factors.append("positive_response_history_visible")
    if float(process["recovery_slope"]) > 0.0:
        supporting_factors.append("recoverability_trajectory_improving")
    if float(process["average_transport_distortion"]) >= 0.55:
        constraining_factors.append("transport_distortion_visible")
    if float(process["average_tail_residue"]) >= 0.55:
        constraining_factors.append("tail_residue_visible")
    if int(process["negative_response_count"]) > 0:
        constraining_factors.append("negative_response_history_visible")
    if evidence_quality < 0.60:
        constraining_factors.append("evidence_quality_limited")

    report = {
        "version": REPORT_VERSION,
        "packet_id": packet.get("packet_id", ""),
        "source_packet_digest": packet.get("diagnostic_packet_digest", ""),
        "valid": not errors,
        "errors": errors,
        "diagnostic_hypothesis_summary": hypothesis_summary,
        "healing_potential": {
            "classification": classification,
            "interval_lower": round(lower, 6),
            "interval_center": round(center, 6),
            "interval_upper": round(upper, 6),
            "support_score": round(float(process["support_score"]), 6),
            "burden_score": round(float(process["burden_score"]), 6),
            "evidence_quality": round(evidence_quality, 6),
            "supporting_factors": supporting_factors,
            "constraining_factors": constraining_factors,
            "healing_guaranteed": False,
            "cure_claimed": False,
            "prognosis_claimed": False,
            "irreversibility_claimed": False,
            "severity_used_in_score": False,
        },
        "process_tensor_summary": {
            key: round(value, 6) if isinstance(value, float) else value
            for key, value in process.items()
        },
        "red_flags": red_flags,
        "route": route,
        "route_is_clinical_instruction": False,
        "clinician_review_required": True,
        "treatment_route_generated": False,
        "candidate_only": True,
        "source_history_preserved": True,
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "diagnostic_report_digest": "",
    }
    report["diagnostic_report_digest"] = report_digest(report)
    return report


__all__ = [
    "build_diagnostic_packet",
    "evaluate_diagnostic_packet",
    "validate_diagnostic_packet",
]
