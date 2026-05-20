#!/usr/bin/env python3
"""Physical Quantum Qi Phase Transition Response Governor runtime v0.2Q.

This module advances Qi implementation from phase-transition detection to a
boundary-preserving response governor:

    QiTrajectoryPhaseTransitionCandidate -> governed response route receipt

Canonical interpretation:
- A response route is a candidate governance surface, not clinical execution.
- Physician-to-AI consultation remains open by default.
- Phase-transition HOLD/WATCH signals deepen observation/consultation before any boundary handover.
- Handover is not forced by metric or alert alone.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2Q"
PACKET_TYPE = "physical_quantum_qi_phase_transition_response_governor_packet"

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

REQUIRED_GOVERNOR_TRUE = [
    "phase_transition_candidate_input_required",
    "route_mapping_required",
    "consultation_default_preserved",
    "doctor_ai_consultation_accepted",
    "handover_not_default",
    "handover_not_forced_by_metric_alone",
    "hold_watch_visibility_preserved",
    "candidate_only_response",
    "non_markov_history_primary",
    "append_only_receipt_required",
]

REQUIRED_PHASE_CANDIDATE_KEYS = [
    "surface_type",
    "version",
    "record_count",
    "phase_pressure_score",
    "critical_slowing_down_score",
    "hysteresis_score",
    "increasing_pressure_channels",
    "hold_visible",
    "watch_visible",
    "transition_alert_level",
    "recommended_route",
    "consultation_deepening_allowed",
    "physician_ai_consultation_preserved",
    "handover_forced",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "diagnosis_authority_granted",
    "prescription_authority_granted",
    "formula_selection_authority_granted",
    "execution_authority_granted",
]

VALID_ALERT_LEVELS = {
    "phase_transition_not_indicated",
    "phase_transition_possible",
    "phase_transition_watch_visible",
    "phase_transition_hold_visible",
}

VALID_RECOMMENDED_ROUTES = {
    "continue_candidate_monitoring",
    "reobserve_before_commit",
    "continue_consultation_with_monitoring",
    "deepen_consultation_and_reobserve",
}

VALID_RESPONSE_ROUTES = {
    "continue_candidate_monitoring",
    "reobserve_and_record",
    "consultation_monitoring_route",
    "consultation_deepening_route",
    "hold_with_physician_ai_consultation_open",
}

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_response_route_candidate",
    "MemoryOS.qi_response_route_receipt_candidate",
    "ReflectionOS.qi_response_risk_review_candidate",
    "PlanOS.qi_response_monitoring_plan_candidate",
    "DecisionOS.qi_response_safety_evaluable_candidate",
    "ClinicalConsultationOS.physician_ai_consultation_open_route_candidate",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "response_route_claimed_as_clinical_action",
    "response_route_claimed_as_diagnosis",
    "response_route_claimed_as_prescription",
    "response_route_claimed_as_formula_selection",
    "response_route_claimed_as_triage",
    "response_route_grants_execution_authority",
    "response_route_grants_truth_authority",
    "response_route_grants_proof_authority",
    "phase_alert_forces_handover",
    "metric_forces_handover",
    "consultation_closed_by_governor",
    "doctor_ai_consultation_blocked",
    "hold_visibility_erased",
    "watch_visibility_erased",
    "non_markov_history_erased",
    "authority_created_by_response",
]


@dataclass(frozen=True)
class QiPhaseTransitionResponseGovernorResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    governance_status: str
    response_route: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    governed_response_candidate: Dict[str, Any]
    response_receipt: Dict[str, Any]

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


def _validate_phase_transition_candidate(candidate: Mapping[str, Any], errors: List[str]) -> None:
    for key in REQUIRED_PHASE_CANDIDATE_KEYS:
        if key not in candidate:
            errors.append(f"phase_transition_candidate.{key} is required")

    if candidate.get("surface_type") != "QiTrajectoryPhaseTransitionCandidate":
        errors.append("phase_transition_candidate.surface_type must be QiTrajectoryPhaseTransitionCandidate")
    if candidate.get("version") not in {"v0.2P", VERSION}:
        errors.append("phase_transition_candidate.version must be v0.2P or v0.2Q")
    if not isinstance(candidate.get("record_count"), int) or isinstance(candidate.get("record_count"), bool) or candidate.get("record_count", 0) < 2:
        errors.append("phase_transition_candidate.record_count must be an integer >= 2")
    for key in ["phase_pressure_score", "critical_slowing_down_score", "hysteresis_score"]:
        if not _bounded(candidate.get(key), 0.0, 1.0):
            errors.append(f"phase_transition_candidate.{key} must be a number in [0, 1]")
    if not isinstance(candidate.get("increasing_pressure_channels"), int) or isinstance(candidate.get("increasing_pressure_channels"), bool):
        errors.append("phase_transition_candidate.increasing_pressure_channels must be an integer")
    if str(candidate.get("transition_alert_level", "")) not in VALID_ALERT_LEVELS:
        errors.append("phase_transition_candidate.transition_alert_level must be valid")
    if str(candidate.get("recommended_route", "")) not in VALID_RECOMMENDED_ROUTES:
        errors.append("phase_transition_candidate.recommended_route must be valid")
    for key in ["consultation_deepening_allowed", "physician_ai_consultation_preserved", "candidate_only"]:
        if candidate.get(key) is not True:
            errors.append(f"phase_transition_candidate.{key} must be true")
    for key in [
        "handover_forced",
        "authority_granted",
        "clinical_authority_granted",
        "diagnosis_authority_granted",
        "prescription_authority_granted",
        "formula_selection_authority_granted",
        "execution_authority_granted",
    ]:
        if candidate.get(key) is not False:
            errors.append(f"phase_transition_candidate.{key} must be false")


def validate_qi_phase_transition_response_governor_packet(packet: Mapping[str, Any]) -> List[str]:
    """Return validation errors for a v0.2Q response governor packet."""

    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    governor = _section(packet, "response_governor", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)
    candidate = _section(packet, "phase_transition_candidate", errors)

    _require_true(governor, "response_governor", REQUIRED_GOVERNOR_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)
    _validate_phase_transition_candidate(candidate, errors)

    route_policy = packet.get("route_policy")
    if not isinstance(route_policy, Mapping):
        errors.append("route_policy must be an object")
    else:
        for level in VALID_ALERT_LEVELS:
            if str(route_policy.get(level, "")) not in VALID_RESPONSE_ROUTES:
                errors.append(f"route_policy.{level} must be a valid response route")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def build_governed_response_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = packet.get("phase_transition_candidate", {})
    if not isinstance(candidate, Mapping):
        candidate = {}
    route_policy = packet.get("route_policy", {})
    if not isinstance(route_policy, Mapping):
        route_policy = {}

    alert = str(candidate.get("transition_alert_level", "phase_transition_not_indicated"))
    recommended = str(candidate.get("recommended_route", "continue_candidate_monitoring"))
    response_route = str(route_policy.get(alert, "continue_candidate_monitoring"))

    hold_visible = bool(candidate.get("hold_visible")) or alert == "phase_transition_hold_visible"
    watch_visible = bool(candidate.get("watch_visible")) or alert in {
        "phase_transition_watch_visible",
        "phase_transition_hold_visible",
    }
    phase_pressure_score = float(candidate.get("phase_pressure_score", 0.0)) if _bounded(candidate.get("phase_pressure_score"), 0.0, 1.0) else 0.0
    slowing_score = float(candidate.get("critical_slowing_down_score", 0.0)) if _bounded(candidate.get("critical_slowing_down_score"), 0.0, 1.0) else 0.0
    hysteresis_score = float(candidate.get("hysteresis_score", 0.0)) if _bounded(candidate.get("hysteresis_score"), 0.0, 1.0) else 0.0

    if hold_visible:
        monitoring_intensity = "high"
        response_status = "hold_visible_consultation_open"
    elif watch_visible:
        monitoring_intensity = "moderate"
        response_status = "watch_visible_consultation_open"
    elif alert == "phase_transition_possible":
        monitoring_intensity = "moderate"
        response_status = "reobserve_before_commit"
    else:
        monitoring_intensity = "baseline"
        response_status = "continue_candidate_monitoring"

    return {
        "surface_type": "QiPhaseTransitionGovernedResponseCandidate",
        "version": VERSION,
        "source_phase_transition_version": str(candidate.get("version", "<missing>")),
        "transition_alert_level": alert,
        "source_recommended_route": recommended,
        "response_route": response_route,
        "response_status": response_status,
        "monitoring_intensity": monitoring_intensity,
        "phase_pressure_score": round(phase_pressure_score, 6),
        "critical_slowing_down_score": round(slowing_score, 6),
        "hysteresis_score": round(hysteresis_score, 6),
        "hold_visible": hold_visible,
        "watch_visible": watch_visible,
        "consultation_open": True,
        "doctor_ai_consultation_accepted": True,
        "consultation_deepening_allowed": True,
        "reobserve_required_before_commit": alert != "phase_transition_not_indicated",
        "handover_forced": False,
        "handover_default": False,
        "boundary_handover_candidate_only": hold_visible and phase_pressure_score >= 0.85,
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "triage_authority_granted": False,
        "execution_authority_granted": False,
    }


def build_response_receipt(packet: Mapping[str, Any], response: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "receipt_type": "QiPhaseTransitionResponseGovernorReceipt",
        "version": VERSION,
        "response_route": str(response.get("response_route", "<missing>")),
        "response_status": str(response.get("response_status", "<missing>")),
        "monitoring_intensity": str(response.get("monitoring_intensity", "<missing>")),
        "hold_visible": bool(response.get("hold_visible")),
        "watch_visible": bool(response.get("watch_visible")),
        "consultation_open": True,
        "doctor_ai_consultation_accepted": True,
        "consultation_deepening_allowed": True,
        "handover_forced": False,
        "handover_default": False,
        "candidate_only": True,
        "authority_created_by_response": False,
        "clinical_authority_granted": False,
        "diagnosis_authority_granted": False,
        "prescription_authority_granted": False,
        "formula_selection_authority_granted": False,
        "triage_authority_granted": False,
        "execution_authority_granted": False,
        "append_only_receipt": True,
        "non_authority_boundary_preserved": True,
    }


def build_qi_phase_transition_response_governor_result(packet: Mapping[str, Any]) -> QiPhaseTransitionResponseGovernorResult:
    errors = validate_qi_phase_transition_response_governor_packet(packet)
    valid = not errors
    response = build_governed_response_candidate(packet)
    receipt = build_response_receipt(packet, response)

    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []

    return QiPhaseTransitionResponseGovernorResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        surface_type="QiPhaseTransitionResponseGovernorResult",
        version=VERSION,
        governance_status="valid_response_route_candidate" if valid else "invalid_response_governor_packet",
        response_route=str(response.get("response_route", "<missing>")),
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        governed_response_candidate=response,
        response_receipt=receipt,
    )


def build_qi_phase_transition_response_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_phase_transition_response_governor_result(packet).to_dict()
