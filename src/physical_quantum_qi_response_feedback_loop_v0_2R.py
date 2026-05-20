#!/usr/bin/env python3
"""Physical Quantum Qi Response Feedback Loop runtime v0.2R.

Adds an append-only feedback loop after the v0.2Q response governor:
QiPhaseTransitionGovernedResponseCandidate -> QiResponseFeedbackLoopReceipt.
Feedback changes monitoring/consultation/re-observation candidates only; it does
not create diagnosis, prescription, formula-selection, triage, clinical, truth,
proof, or execution authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2R"
PACKET_TYPE = "physical_quantum_qi_response_feedback_loop_packet"

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

REQUIRED_LOOP_TRUE = [
    "response_governor_receipt_required",
    "feedback_observation_required",
    "append_only_feedback_required",
    "consultation_default_preserved",
    "doctor_ai_consultation_accepted",
    "hold_watch_visibility_preserved",
    "non_markov_history_primary",
    "candidate_only_feedback",
    "no_silent_recovery_claim",
    "no_handover_by_metric_alone",
]

REQUIRED_RESPONSE_KEYS = [
    "surface_type",
    "version",
    "response_route",
    "response_status",
    "monitoring_intensity",
    "hold_visible",
    "watch_visible",
    "consultation_open",
    "doctor_ai_consultation_accepted",
    "consultation_deepening_allowed",
    "handover_forced",
    "handover_default",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "diagnosis_authority_granted",
    "prescription_authority_granted",
    "formula_selection_authority_granted",
    "triage_authority_granted",
    "execution_authority_granted",
]

REQUIRED_FEEDBACK_KEYS = [
    "feedback_window_count",
    "phase_pressure_delta",
    "critical_slowing_down_delta",
    "hysteresis_delta",
    "consultation_continuity",
    "reobservation_completed",
    "memory_receipt_appended",
    "physician_ai_consultation_preserved",
]

VALID_RESPONSE_ROUTES = {
    "continue_candidate_monitoring",
    "reobserve_and_record",
    "consultation_monitoring_route",
    "consultation_deepening_route",
    "hold_with_physician_ai_consultation_open",
}

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_feedback_state_candidate",
    "MemoryOS.qi_feedback_receipt_candidate",
    "ReflectionOS.qi_feedback_residue_review_candidate",
    "PlanOS.qi_feedback_monitoring_loop_candidate",
    "DecisionOS.qi_feedback_safety_evaluable_candidate",
    "ClinicalConsultationOS.physician_ai_consultation_feedback_candidate",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "feedback_claimed_as_clinical_action",
    "feedback_claimed_as_recovery_truth",
    "feedback_claimed_as_diagnosis",
    "feedback_claimed_as_prescription",
    "feedback_claimed_as_formula_selection",
    "feedback_claimed_as_triage",
    "improvement_grants_execution_authority",
    "improvement_grants_truth_authority",
    "metric_forces_handover",
    "metric_closes_consultation",
    "hold_visibility_erased",
    "watch_visibility_erased",
    "non_markov_history_erased",
    "response_receipt_overwritten",
    "authority_created_by_feedback",
]


@dataclass(frozen=True)
class QiResponseFeedbackLoopResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    feedback_status: str
    next_loop_route: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    feedback_candidate: Dict[str, Any]
    feedback_receipt: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _bounded(value: Any, lower: float, upper: float) -> bool:
    return _is_number(value) and lower <= float(value) <= upper


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


def _validate_response_candidate(response: Mapping[str, Any], errors: List[str]) -> None:
    for key in REQUIRED_RESPONSE_KEYS:
        if key not in response:
            errors.append(f"response_candidate.{key} is required")
    if response.get("surface_type") != "QiPhaseTransitionGovernedResponseCandidate":
        errors.append("response_candidate.surface_type must be QiPhaseTransitionGovernedResponseCandidate")
    if response.get("version") not in {"v0.2Q", VERSION}:
        errors.append("response_candidate.version must be v0.2Q or v0.2R")
    if str(response.get("response_route", "")) not in VALID_RESPONSE_ROUTES:
        errors.append("response_candidate.response_route must be valid")
    for key in ["consultation_open", "doctor_ai_consultation_accepted", "consultation_deepening_allowed", "candidate_only"]:
        if response.get(key) is not True:
            errors.append(f"response_candidate.{key} must be true")
    for key in [
        "handover_forced",
        "handover_default",
        "authority_granted",
        "clinical_authority_granted",
        "diagnosis_authority_granted",
        "prescription_authority_granted",
        "formula_selection_authority_granted",
        "triage_authority_granted",
        "execution_authority_granted",
    ]:
        if response.get(key) is not False:
            errors.append(f"response_candidate.{key} must be false")


def _validate_feedback_observation(feedback: Mapping[str, Any], errors: List[str]) -> None:
    for key in REQUIRED_FEEDBACK_KEYS:
        if key not in feedback:
            errors.append(f"feedback_observation.{key} is required")
    if not isinstance(feedback.get("feedback_window_count"), int) or isinstance(feedback.get("feedback_window_count"), bool) or feedback.get("feedback_window_count", 0) < 1:
        errors.append("feedback_observation.feedback_window_count must be an integer >= 1")
    for key in ["phase_pressure_delta", "critical_slowing_down_delta", "hysteresis_delta"]:
        if not _bounded(feedback.get(key), -1.0, 1.0):
            errors.append(f"feedback_observation.{key} must be a number in [-1, 1]")
    for key in [
        "consultation_continuity",
        "reobservation_completed",
        "memory_receipt_appended",
        "physician_ai_consultation_preserved",
    ]:
        if feedback.get(key) is not True:
            errors.append(f"feedback_observation.{key} must be true")


def validate_qi_response_feedback_loop_packet(packet: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    loop = _section(packet, "feedback_loop", errors)
    response = _section(packet, "response_candidate", errors)
    feedback = _section(packet, "feedback_observation", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)

    _require_true(loop, "feedback_loop", REQUIRED_LOOP_TRUE, errors)
    _validate_response_candidate(response, errors)
    _validate_feedback_observation(feedback, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")
    return errors


def _safe_delta(feedback: Mapping[str, Any], key: str) -> float:
    value = feedback.get(key, 0.0)
    return float(value) if _bounded(value, -1.0, 1.0) else 0.0


def _classify_feedback(response: Mapping[str, Any], feedback: Mapping[str, Any]) -> Dict[str, Any]:
    pressure_delta = _safe_delta(feedback, "phase_pressure_delta")
    slowing_delta = _safe_delta(feedback, "critical_slowing_down_delta")
    hysteresis_delta = _safe_delta(feedback, "hysteresis_delta")
    mean_delta = (pressure_delta + slowing_delta + hysteresis_delta) / 3.0
    recovery_signal = round(max(0.0, -mean_delta), 6)
    residue_signal = round(max(0.0, mean_delta), 6)
    hold_visible = bool(response.get("hold_visible"))
    watch_visible = bool(response.get("watch_visible")) or hold_visible

    if hold_visible and residue_signal > 0.05:
        feedback_status = "hold_visible_residue_persistent"
        next_route = "hold_with_consultation_open"
    elif recovery_signal >= 0.05 and watch_visible:
        feedback_status = "partial_recovery_watch_visible"
        next_route = "continue_consultation_monitoring"
    elif residue_signal >= 0.10:
        feedback_status = "residue_increasing_reobserve"
        next_route = "continue_reobservation_loop"
    elif str(response.get("response_route")) == "consultation_deepening_route":
        feedback_status = "consultation_deepening_continues"
        next_route = "deepen_consultation_loop"
    else:
        feedback_status = "candidate_monitoring_continues"
        next_route = "continue_candidate_monitoring"

    return {
        "feedback_status": feedback_status,
        "next_loop_route": next_route,
        "recovery_signal": recovery_signal,
        "residue_signal": residue_signal,
        "pressure_delta": round(pressure_delta, 6),
        "slowing_delta": round(slowing_delta, 6),
        "hysteresis_delta": round(hysteresis_delta, 6),
        "hold_visible": hold_visible,
        "watch_visible": watch_visible,
    }


def build_feedback_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    response = packet.get("response_candidate", {})
    if not isinstance(response, Mapping):
        response = {}
    feedback = packet.get("feedback_observation", {})
    if not isinstance(feedback, Mapping):
        feedback = {}
    classified = _classify_feedback(response, feedback)
    return {
        "surface_type": "QiResponseFeedbackLoopCandidate",
        "version": VERSION,
        "source_response_version": str(response.get("version", "<missing>")),
        "source_response_route": str(response.get("response_route", "<missing>")),
        "feedback_status": classified["feedback_status"],
        "next_loop_route": classified["next_loop_route"],
        "recovery_signal": classified["recovery_signal"],
        "residue_signal": classified["residue_signal"],
        "phase_pressure_delta": classified["pressure_delta"],
        "critical_slowing_down_delta": classified["slowing_delta"],
        "hysteresis_delta": classified["hysteresis_delta"],
        "hold_visible": classified["hold_visible"],
        "watch_visible": classified["watch_visible"],
        "consultation_open": True,
        "doctor_ai_consultation_accepted": True,
        "consultation_deepening_allowed": True,
        "reobservation_completed": bool(feedback.get("reobservation_completed")),
        "memory_receipt_appended": bool(feedback.get("memory_receipt_appended")),
        "silent_recovery_claim_allowed": False,
        "handover_forced": False,
        "handover_default": False,
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "triage_authority_granted": False,
        "execution_authority_granted": False,
    }


def build_feedback_receipt(feedback_candidate: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "receipt_type": "QiResponseFeedbackLoopReceipt",
        "version": VERSION,
        "feedback_status": str(feedback_candidate.get("feedback_status", "<missing>")),
        "next_loop_route": str(feedback_candidate.get("next_loop_route", "<missing>")),
        "recovery_signal": float(feedback_candidate.get("recovery_signal", 0.0)),
        "residue_signal": float(feedback_candidate.get("residue_signal", 0.0)),
        "hold_visible": bool(feedback_candidate.get("hold_visible")),
        "watch_visible": bool(feedback_candidate.get("watch_visible")),
        "consultation_open": True,
        "doctor_ai_consultation_accepted": True,
        "consultation_deepening_allowed": True,
        "handover_forced": False,
        "handover_default": False,
        "candidate_only": True,
        "append_only_receipt": True,
        "non_markov_history_preserved": True,
        "authority_created_by_feedback": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "triage_authority_granted": False,
        "execution_authority_granted": False,
    }


def build_qi_response_feedback_loop_result(packet: Mapping[str, Any]) -> QiResponseFeedbackLoopResult:
    errors = validate_qi_response_feedback_loop_packet(packet)
    feedback_candidate = build_feedback_candidate(packet)
    feedback_receipt = build_feedback_receipt(feedback_candidate)
    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []
    return QiResponseFeedbackLoopResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=not errors,
        errors=errors,
        surface_type="QiResponseFeedbackLoopResult",
        version=VERSION,
        feedback_status=str(feedback_candidate.get("feedback_status", "<missing>")),
        next_loop_route=str(feedback_candidate.get("next_loop_route", "<missing>")),
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        feedback_candidate=feedback_candidate,
        feedback_receipt=feedback_receipt,
    )


def build_qi_response_feedback_loop_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_response_feedback_loop_result(packet).to_dict()
