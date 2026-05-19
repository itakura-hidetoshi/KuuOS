#!/usr/bin/env python3
"""Physical Quantum Qi State Transition Kernel runtime v0.2N.

This module advances the Qi implementation from:

    observation event sequence -> QiStateCandidate

to:

    QiStateCandidate + bounded transition events -> next QiStateCandidate

Canonical interpretation:
- Qi state is a non-authoritative runtime candidate.
- Transition is bounded, lineage-preserving, and non-Markov-history aware.
- Improvement, worsening, and hold are all valid candidate outcomes.
- No transition grants proof, truth, clinical, diagnosis, prescription,
  formula-selection, triage, execution, commit, memory-overwrite, world-rewrite,
  ontology, or safety-override authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2N"
PACKET_TYPE = "physical_quantum_qi_state_transition_kernel_packet"

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

REQUIRED_KERNEL_TRUE = [
    "qi_state_candidate_input_required",
    "transition_events_declared",
    "bounded_transition_required",
    "lineage_preservation_required",
    "source_history_preservation_required",
    "non_markov_memory_primary",
    "backaction_visibility_required",
    "candidate_only_transition",
    "hold_is_valid_transition_result",
    "clinical_consultation_boundary_preserved",
]

REQUIRED_STATE_FIELDS = [
    "surface_type",
    "version",
    "qi_memory_gain",
    "qi_backflow",
    "qi_env_correlation_credit",
    "qi_temporal_complexity",
    "qi_coherence_margin",
    "qi_recoverability_margin",
    "qi_transport_distortion",
    "qi_tail_residue",
    "qi_runtime_mode",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "execution_authority_granted",
]

REQUIRED_EVENT_KEYS = [
    "transition_id",
    "transition_kind",
    "memory_gain_delta",
    "backflow_delta",
    "env_correlation_delta",
    "temporal_complexity_delta",
    "coherence_delta",
    "recoverability_delta",
    "transport_distortion_delta",
    "tail_residue_delta",
    "backaction_visible",
    "source_trace",
]

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_state_transition_candidate",
    "MemoryOS.qi_transition_lineage_record_candidate",
    "ReflectionOS.qi_transition_residue_analysis_candidate",
    "PlanOS.qi_transition_transport_candidate",
    "DecisionOS.qi_transition_safety_evaluable_candidate",
    "QiProcessTensor.transition_update_surface",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "transition_claimed_as_truth",
    "transition_claimed_as_clinical_action",
    "transition_grants_execution_authority",
    "transition_grants_diagnosis_authority",
    "transition_grants_prescription_authority",
    "transition_grants_formula_selection_authority",
    "transition_forces_handover_by_metric_alone",
    "lineage_replaced",
    "source_history_erased",
    "current_snapshot_replaces_process_history",
    "backaction_erased",
    "tail_residue_hidden",
    "worsening_state_silently_promoted",
    "hold_result_silently_closed",
]

METRIC_KEYS = [
    "qi_memory_gain",
    "qi_backflow",
    "qi_env_correlation_credit",
    "qi_temporal_complexity",
    "qi_coherence_margin",
    "qi_recoverability_margin",
    "qi_transport_distortion",
    "qi_tail_residue",
]

DELTA_TO_METRIC = {
    "memory_gain_delta": "qi_memory_gain",
    "backflow_delta": "qi_backflow",
    "env_correlation_delta": "qi_env_correlation_credit",
    "temporal_complexity_delta": "qi_temporal_complexity",
    "coherence_delta": "qi_coherence_margin",
    "recoverability_delta": "qi_recoverability_margin",
    "transport_distortion_delta": "qi_transport_distortion",
    "tail_residue_delta": "qi_tail_residue",
}


@dataclass(frozen=True)
class QiStateTransitionResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    transition_status: str
    lineage_status: str
    non_markov_status: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    previous_state_candidate: Dict[str, Any]
    next_state_candidate: Dict[str, Any]
    transition_receipt: Dict[str, Any]

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


def _average(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _runtime_mode(state: Mapping[str, Any]) -> str:
    backflow = float(state.get("qi_backflow", 0.0)) if _bounded(state.get("qi_backflow"), 0.0, 1.0) else 0.0
    tail = float(state.get("qi_tail_residue", 0.0)) if _bounded(state.get("qi_tail_residue"), 0.0, 1.0) else 0.0
    recoverability = float(state.get("qi_recoverability_margin", 0.0)) if _bounded(state.get("qi_recoverability_margin"), 0.0, 1.0) else 0.0
    coherence = float(state.get("qi_coherence_margin", 0.0)) if _bounded(state.get("qi_coherence_margin"), 0.0, 1.0) else 0.0
    distortion = float(state.get("qi_transport_distortion", 0.0)) if _bounded(state.get("qi_transport_distortion"), 0.0, 1.0) else 0.0

    if backflow >= 0.55:
        return "counterflow_watch"
    if tail >= 0.55:
        return "stagnation_watch"
    if recoverability <= 0.35 or coherence <= 0.35:
        return "deficiency_watch"
    if distortion >= 0.6:
        return "transport_distortion_watch"
    return "monitor_continue"


def validate_qi_state_transition_packet(packet: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    kernel = _section(packet, "state_transition_kernel", errors)
    previous_state = _section(packet, "previous_state_candidate", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)

    _require_true(kernel, "state_transition_kernel", REQUIRED_KERNEL_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)

    for key in REQUIRED_STATE_FIELDS:
        if key not in previous_state:
            errors.append(f"previous_state_candidate.{key} is required")
    if previous_state.get("surface_type") != "QiStateCandidate":
        errors.append("previous_state_candidate.surface_type must be QiStateCandidate")
    if previous_state.get("candidate_only") is not True:
        errors.append("previous_state_candidate.candidate_only must be true")
    for key in ["authority_granted", "clinical_authority_granted", "execution_authority_granted"]:
        if previous_state.get(key) is not False:
            errors.append(f"previous_state_candidate.{key} must be false")
    for key in METRIC_KEYS:
        if not _bounded(previous_state.get(key), 0.0, 1.0):
            errors.append(f"previous_state_candidate.{key} must be a number in [0, 1]")

    events = packet.get("transition_events")
    if not isinstance(events, list) or not events:
        errors.append("transition_events must be a nonempty list")
    else:
        seen_ids: set[str] = set()
        for index, event in enumerate(events):
            if not isinstance(event, Mapping):
                errors.append(f"transition_events[{index}] must be an object")
                continue
            for key in REQUIRED_EVENT_KEYS:
                if key not in event:
                    errors.append(f"transition_events[{index}].{key} is required")
            transition_id = str(event.get("transition_id", ""))
            if not transition_id:
                errors.append(f"transition_events[{index}].transition_id must be nonempty")
            if transition_id in seen_ids:
                errors.append(f"transition_events[{index}].transition_id must be unique")
            seen_ids.add(transition_id)
            if not str(event.get("transition_kind", "")):
                errors.append(f"transition_events[{index}].transition_kind must be nonempty")
            if not str(event.get("source_trace", "")):
                errors.append(f"transition_events[{index}].source_trace must be nonempty")
            if event.get("backaction_visible") is not True:
                errors.append(f"transition_events[{index}].backaction_visible must be true")
            for key in DELTA_TO_METRIC:
                if not _bounded(event.get(key), -0.25, 0.25):
                    errors.append(f"transition_events[{index}].{key} must be a number in [-0.25, 0.25]")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def project_next_qi_state_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    previous = packet.get("previous_state_candidate", {})
    if not isinstance(previous, Mapping):
        previous = {}
    events_raw = packet.get("transition_events", [])
    events = [event for event in events_raw if isinstance(event, Mapping)] if isinstance(events_raw, list) else []

    next_state: Dict[str, Any] = {
        "surface_type": "QiStateCandidate",
        "version": VERSION,
    }
    for metric in METRIC_KEYS:
        base = float(previous.get(metric, 0.0)) if _bounded(previous.get(metric), 0.0, 1.0) else 0.0
        delta_key = next(key for key, value in DELTA_TO_METRIC.items() if value == metric)
        deltas = [float(event.get(delta_key, 0.0)) for event in events if _bounded(event.get(delta_key), -0.25, 0.25)]
        next_state[metric] = round(_clamp01(base + _average(deltas)), 6)

    next_state["qi_runtime_mode"] = _runtime_mode(next_state)
    next_state["candidate_only"] = True
    next_state["authority_granted"] = False
    next_state["clinical_authority_granted"] = False
    next_state["execution_authority_granted"] = False
    next_state["source_history_replaced"] = False
    next_state["lineage_preserved"] = True
    next_state["backaction_visible"] = all(event.get("backaction_visible") is True for event in events) if events else False
    next_state["transition_count"] = len(events)
    return next_state


def build_transition_receipt(packet: Mapping[str, Any], next_state: Mapping[str, Any]) -> Dict[str, Any]:
    previous = packet.get("previous_state_candidate", {})
    if not isinstance(previous, Mapping):
        previous = {}

    risk_terms = [
        float(next_state.get("qi_backflow", 0.0)),
        float(next_state.get("qi_tail_residue", 0.0)),
        float(next_state.get("qi_transport_distortion", 0.0)),
        1.0 - float(next_state.get("qi_recoverability_margin", 0.0)),
        1.0 - float(next_state.get("qi_coherence_margin", 0.0)),
    ]
    risk_score = _clamp01(_average(risk_terms))
    if next_state.get("qi_runtime_mode") == "monitor_continue" and risk_score < 0.45:
        transition_decision = "candidate_continue"
    elif risk_score < 0.65:
        transition_decision = "candidate_watch"
    else:
        transition_decision = "candidate_hold"

    return {
        "receipt_type": "QiStateTransitionReceipt",
        "version": VERSION,
        "previous_version": str(previous.get("version", "<missing>")),
        "next_version": VERSION,
        "transition_decision": transition_decision,
        "risk_score": round(risk_score, 6),
        "lineage_preserved": True,
        "source_history_replaced": False,
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "execution_authority_granted": False,
        "handover_forced": False,
        "doctor_ai_consultation_blocked": False,
    }


def build_qi_state_transition_result(packet: Mapping[str, Any]) -> QiStateTransitionResult:
    errors = validate_qi_state_transition_packet(packet)
    valid = not errors
    previous = packet.get("previous_state_candidate", {})
    if not isinstance(previous, Mapping):
        previous = {}
    next_state = project_next_qi_state_candidate(packet)
    receipt = build_transition_receipt(packet, next_state)

    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []

    return QiStateTransitionResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        surface_type="QiStateTransitionKernelResult",
        version=VERSION,
        transition_status="valid_bounded_qi_state_transition" if valid else "invalid_qi_state_transition",
        lineage_status="lineage_preserved" if valid else "lineage_validation_failed",
        non_markov_status="history_bearing_transition" if valid else "non_markov_transition_failed",
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        previous_state_candidate=dict(previous),
        next_state_candidate=next_state,
        transition_receipt=receipt,
    )


def build_qi_state_transition_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_state_transition_result(packet).to_dict()
