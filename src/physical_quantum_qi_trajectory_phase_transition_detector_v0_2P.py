#!/usr/bin/env python3
"""Physical Quantum Qi Trajectory Phase Transition Detector runtime v0.2P.

This module advances Qi implementation from trajectory ledger to a candidate
phase-transition detector:

    QiTransitionTrajectoryCandidate -> phase-transition candidate receipt

Canonical interpretation:
- Phase transition detection is a non-authoritative runtime candidate.
- It detects regime-change signs without claiming ontology, diagnosis, or action.
- A phase-transition alert deepens observation / consultation; it does not force handover.
- HOLD / WATCH visibility from the trajectory ledger remains preserved.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2P"
PACKET_TYPE = "physical_quantum_qi_trajectory_phase_transition_detector_packet"

AUTHORITY_FALSE_FIELDS = [
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "clinical_authority",
    "diagnosis_authority",
    "prescription_authority",
    "formula_selection_authority",
    "triage_authority",
    "safety_override_authority",
]

REQUIRED_DETECTOR_TRUE = [
    "trajectory_input_required",
    "trend_based_detection_required",
    "critical_slowing_down_visible",
    "hysteresis_visible",
    "early_warning_visible",
    "hold_watch_visibility_preserved",
    "candidate_only_detection",
    "non_markov_memory_primary",
    "consultation_default_preserved",
    "handover_not_forced_by_detection_alone",
]

REQUIRED_TRAJECTORY_KEYS = [
    "surface_type",
    "version",
    "record_count",
    "average_risk_score",
    "latest_risk_score",
    "stability_index",
    "risk_trend",
    "backflow_trend",
    "tail_residue_trend",
    "recoverability_trend",
    "transport_distortion_trend",
    "trajectory_decision",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "execution_authority_granted",
    "handover_forced",
    "doctor_ai_consultation_blocked",
]

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_phase_transition_candidate",
    "MemoryOS.qi_phase_transition_lineage_note_candidate",
    "ReflectionOS.qi_phase_transition_residue_analysis_candidate",
    "PlanOS.qi_phase_transition_monitoring_route_candidate",
    "DecisionOS.qi_phase_transition_safety_evaluable_candidate",
    "ClinicalConsultationOS.qi_phase_transition_consultation_deepening_candidate",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "phase_transition_claimed_as_truth",
    "phase_transition_claimed_as_diagnosis",
    "phase_transition_claimed_as_prescription",
    "phase_transition_claimed_as_formula_selection",
    "phase_transition_claimed_as_execution_permission",
    "phase_transition_forces_handover_by_metric_alone",
    "phase_transition_closes_physician_ai_consultation",
    "hold_visibility_erased",
    "watch_visibility_erased",
    "non_markov_history_reduced_to_snapshot",
    "tail_residue_hidden",
    "backflow_hidden",
    "transport_distortion_hidden",
    "recoverability_loss_hidden",
    "authority_created_by_alert",
]

VALID_TREND_VALUES = {
    "increasing",
    "decreasing",
    "stable",
    "insufficient_history",
}

VALID_TRAJECTORY_DECISIONS = {
    "trajectory_continue_candidate",
    "trajectory_watch_visible",
    "trajectory_hold_visible",
}


@dataclass(frozen=True)
class QiTrajectoryPhaseTransitionDetectorResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    detection_status: str
    transition_alert_level: str
    recommended_route: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    phase_transition_candidate: Dict[str, Any]
    phase_transition_receipt: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _bounded(value: Any, lower: float, upper: float) -> bool:
    return _is_number(value) and lower <= float(value) <= upper


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _section(packet: Mapping[str, Any], name: str, errors: List[str]) -> Mapping[str, Any]:
    value = packet.get(name)
    if not isinstance(value, Mapping):
        errors.append(f"{name} must be an object")
        return {}
    return value


def _require_true(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not True:
            errors.append(f"{section_name}.{key} must be true")


def _require_false(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not False:
            errors.append(f"{section_name}.{key} must be false")


def _trend_is(candidate: Mapping[str, Any], key: str, value: str) -> bool:
    return str(candidate.get(key, "")) == value


def _bool(candidate: Mapping[str, Any], key: str) -> bool:
    return candidate.get(key) is True


def _validate_trajectory_candidate(candidate: Mapping[str, Any], errors: List[str]) -> None:
    for key in REQUIRED_TRAJECTORY_KEYS:
        if key not in candidate:
            errors.append(f"trajectory_candidate.{key} is required")

    if candidate.get("surface_type") != "QiTransitionTrajectoryCandidate":
        errors.append("trajectory_candidate.surface_type must be QiTransitionTrajectoryCandidate")
    if candidate.get("version") not in {"v0.2O", VERSION}:
        errors.append("trajectory_candidate.version must be v0.2O or v0.2P")
    if not isinstance(candidate.get("record_count"), int) or isinstance(candidate.get("record_count"), bool) or candidate.get("record_count", 0) < 2:
        errors.append("trajectory_candidate.record_count must be an integer >= 2")
    for key in ["average_risk_score", "latest_risk_score", "stability_index"]:
        if not _bounded(candidate.get(key), 0.0, 1.0):
            errors.append(f"trajectory_candidate.{key} must be a number in [0, 1]")
    for key in ["risk_trend", "backflow_trend", "tail_residue_trend", "recoverability_trend", "transport_distortion_trend"]:
        if str(candidate.get(key, "")) not in VALID_TREND_VALUES:
            errors.append(f"trajectory_candidate.{key} must be a valid trend")
    if str(candidate.get("trajectory_decision", "")) not in VALID_TRAJECTORY_DECISIONS:
        errors.append("trajectory_candidate.trajectory_decision must be a valid trajectory decision")
    if candidate.get("candidate_only") is not True:
        errors.append("trajectory_candidate.candidate_only must be true")
    for key in ["authority_granted", "clinical_authority_granted", "execution_authority_granted", "handover_forced", "doctor_ai_consultation_blocked"]:
        if candidate.get(key) is not False:
            errors.append(f"trajectory_candidate.{key} must be false")


def validate_qi_trajectory_phase_transition_detector_packet(packet: Mapping[str, Any]) -> List[str]:
    """Return validation errors for a v0.2P phase-transition detector packet."""

    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    detector = _section(packet, "phase_transition_detector", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)
    trajectory = _section(packet, "trajectory_candidate", errors)

    _require_true(detector, "phase_transition_detector", REQUIRED_DETECTOR_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)
    _validate_trajectory_candidate(trajectory, errors)

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    thresholds = _section(packet, "thresholds", errors)
    for key in ["watch_threshold", "hold_threshold", "transition_threshold"]:
        if key not in thresholds or not _bounded(thresholds.get(key), 0.0, 1.0):
            errors.append(f"thresholds.{key} must be a number in [0, 1]")
    if _bounded(thresholds.get("watch_threshold"), 0.0, 1.0) and _bounded(thresholds.get("hold_threshold"), 0.0, 1.0):
        if float(thresholds["watch_threshold"]) > float(thresholds["hold_threshold"]):
            errors.append("thresholds.watch_threshold must be <= thresholds.hold_threshold")

    return errors


def build_phase_transition_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    trajectory = packet.get("trajectory_candidate", {})
    if not isinstance(trajectory, Mapping):
        trajectory = {}
    thresholds = packet.get("thresholds", {})
    if not isinstance(thresholds, Mapping):
        thresholds = {}

    latest_risk = float(trajectory.get("latest_risk_score", 0.0)) if _bounded(trajectory.get("latest_risk_score"), 0.0, 1.0) else 0.0
    average_risk = float(trajectory.get("average_risk_score", 0.0)) if _bounded(trajectory.get("average_risk_score"), 0.0, 1.0) else 0.0
    stability_index = float(trajectory.get("stability_index", 1.0)) if _bounded(trajectory.get("stability_index"), 0.0, 1.0) else 1.0
    watch_threshold = float(thresholds.get("watch_threshold", 0.45)) if _bounded(thresholds.get("watch_threshold"), 0.0, 1.0) else 0.45
    hold_threshold = float(thresholds.get("hold_threshold", 0.65)) if _bounded(thresholds.get("hold_threshold"), 0.0, 1.0) else 0.65
    transition_threshold = float(thresholds.get("transition_threshold", 0.60)) if _bounded(thresholds.get("transition_threshold"), 0.0, 1.0) else 0.60

    increasing_pressure = 0
    if _trend_is(trajectory, "risk_trend", "increasing"):
        increasing_pressure += 1
    if _trend_is(trajectory, "backflow_trend", "increasing"):
        increasing_pressure += 1
    if _trend_is(trajectory, "tail_residue_trend", "increasing"):
        increasing_pressure += 1
    if _trend_is(trajectory, "transport_distortion_trend", "increasing"):
        increasing_pressure += 1
    if _trend_is(trajectory, "recoverability_trend", "decreasing"):
        increasing_pressure += 1

    trajectory_decision = str(trajectory.get("trajectory_decision", ""))
    hold_visible = trajectory_decision == "trajectory_hold_visible" or int(trajectory.get("hold_count", 0) or 0) > 0
    watch_visible = trajectory_decision in {"trajectory_hold_visible", "trajectory_watch_visible"} or int(trajectory.get("watch_count", 0) or 0) > 0

    phase_pressure_score = _clamp01(
        0.30 * latest_risk
        + 0.20 * average_risk
        + 0.20 * (1.0 - stability_index)
        + 0.06 * increasing_pressure
    )
    critical_slowing_down_score = _clamp01(
        0.35 * (1.0 - stability_index)
        + 0.20 * (1.0 if _trend_is(trajectory, "recoverability_trend", "decreasing") else 0.0)
        + 0.20 * (1.0 if _trend_is(trajectory, "tail_residue_trend", "increasing") else 0.0)
        + 0.15 * (1.0 if _trend_is(trajectory, "backflow_trend", "increasing") else 0.0)
    )
    hysteresis_score = _clamp01(
        0.25 * (1.0 if hold_visible else 0.0)
        + 0.20 * (1.0 if watch_visible else 0.0)
        + 0.20 * (1.0 if _trend_is(trajectory, "transport_distortion_trend", "increasing") else 0.0)
        + 0.20 * latest_risk
    )

    if phase_pressure_score >= hold_threshold or latest_risk >= hold_threshold or hold_visible:
        alert_level = "phase_transition_hold_visible"
        recommended_route = "deepen_consultation_and_reobserve"
    elif phase_pressure_score >= watch_threshold or latest_risk >= watch_threshold or watch_visible:
        alert_level = "phase_transition_watch_visible"
        recommended_route = "continue_consultation_with_monitoring"
    elif phase_pressure_score >= transition_threshold:
        alert_level = "phase_transition_possible"
        recommended_route = "reobserve_before_commit"
    else:
        alert_level = "phase_transition_not_indicated"
        recommended_route = "continue_candidate_monitoring"

    return {
        "surface_type": "QiTrajectoryPhaseTransitionCandidate",
        "version": VERSION,
        "source_trajectory_version": str(trajectory.get("version", "<missing>")),
        "record_count": int(trajectory.get("record_count", 0) or 0),
        "phase_pressure_score": round(phase_pressure_score, 6),
        "critical_slowing_down_score": round(critical_slowing_down_score, 6),
        "hysteresis_score": round(hysteresis_score, 6),
        "increasing_pressure_channels": increasing_pressure,
        "hold_visible": bool(hold_visible),
        "watch_visible": bool(watch_visible),
        "transition_alert_level": alert_level,
        "recommended_route": recommended_route,
        "consultation_deepening_allowed": True,
        "physician_ai_consultation_preserved": True,
        "handover_forced": False,
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "execution_authority_granted": False,
    }


def build_phase_transition_receipt(packet: Mapping[str, Any], candidate: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "receipt_type": "QiTrajectoryPhaseTransitionReceipt",
        "version": VERSION,
        "transition_alert_level": str(candidate.get("transition_alert_level", "<missing>")),
        "recommended_route": str(candidate.get("recommended_route", "<missing>")),
        "hold_visible": bool(candidate.get("hold_visible")),
        "watch_visible": bool(candidate.get("watch_visible")),
        "consultation_deepening_allowed": bool(candidate.get("consultation_deepening_allowed")),
        "physician_ai_consultation_preserved": bool(candidate.get("physician_ai_consultation_preserved")),
        "handover_forced": False,
        "candidate_only": True,
        "authority_created_by_alert": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "execution_authority_granted": False,
        "non_authority_boundary_preserved": True,
    }


def build_qi_trajectory_phase_transition_detector_result(packet: Mapping[str, Any]) -> QiTrajectoryPhaseTransitionDetectorResult:
    errors = validate_qi_trajectory_phase_transition_detector_packet(packet)
    valid = not errors
    candidate = build_phase_transition_candidate(packet)
    receipt = build_phase_transition_receipt(packet, candidate)

    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []

    return QiTrajectoryPhaseTransitionDetectorResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        surface_type="QiTrajectoryPhaseTransitionDetectorResult",
        version=VERSION,
        detection_status="valid_phase_transition_candidate_detection" if valid else "invalid_phase_transition_detector_packet",
        transition_alert_level=str(candidate.get("transition_alert_level", "<missing>")),
        recommended_route=str(candidate.get("recommended_route", "<missing>")),
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        phase_transition_candidate=candidate,
        phase_transition_receipt=receipt,
    )


def build_qi_trajectory_phase_transition_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_trajectory_phase_transition_detector_result(packet).to_dict()
