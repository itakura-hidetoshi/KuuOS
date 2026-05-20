#!/usr/bin/env python3
"""Physical Quantum Qi Transition Trajectory Ledger runtime v0.2O.

This module advances Qi implementation from a single bounded state transition to
an append-only trajectory ledger:

    ordered Qi transition records -> trajectory-level candidate receipt

Canonical interpretation:
- Qi trajectory is a non-authoritative runtime candidate surface.
- Multiple transition records do not accumulate authority.
- HOLD / WATCH / CONTINUE remain visible canonical outcomes.
- Worsening is not silently promoted; improvement is not execution permission.
- Source lineage, non-Markov memory, and backaction visibility remain first-class.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2O"
PACKET_TYPE = "physical_quantum_qi_transition_trajectory_ledger_packet"

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

REQUIRED_LEDGER_TRUE = [
    "ordered_transition_records_required",
    "append_only_trajectory_required",
    "lineage_preservation_required",
    "source_history_preservation_required",
    "non_markov_memory_primary",
    "backaction_visibility_required",
    "candidate_only_trajectory",
    "no_authority_accumulation",
    "hold_visible_as_canonical_outcome",
    "watch_visible_as_canonical_outcome",
    "clinical_consultation_boundary_preserved",
]

REQUIRED_RECORD_KEYS = [
    "sequence_index",
    "transition_id",
    "source_trace",
    "transition_decision",
    "risk_score",
    "lineage_preserved",
    "source_history_replaced",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "execution_authority_granted",
    "next_state_candidate",
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

STATE_REQUIRED_KEYS = [
    "surface_type",
    "version",
    "qi_runtime_mode",
    "candidate_only",
    "authority_granted",
    "clinical_authority_granted",
    "execution_authority_granted",
]

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_transition_trajectory_candidate",
    "MemoryOS.qi_trajectory_lineage_ledger_candidate",
    "ReflectionOS.qi_trajectory_residue_analysis_candidate",
    "PlanOS.qi_trajectory_transport_candidate",
    "DecisionOS.qi_trajectory_safety_evaluable_candidate",
    "QiProcessTensor.trajectory_update_surface",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "trajectory_claimed_as_truth",
    "trajectory_claimed_as_clinical_action",
    "trajectory_grants_execution_authority",
    "trajectory_grants_diagnosis_authority",
    "trajectory_grants_prescription_authority",
    "trajectory_grants_formula_selection_authority",
    "trajectory_forces_handover_by_metric_alone",
    "authority_accumulates_across_records",
    "lineage_replaced",
    "source_history_erased",
    "current_snapshot_replaces_process_history",
    "backaction_erased",
    "tail_residue_hidden",
    "worsening_state_silently_promoted",
    "hold_result_silently_closed",
    "watch_result_silently_closed",
]

VALID_TRANSITION_DECISIONS = {
    "candidate_continue",
    "candidate_watch",
    "candidate_hold",
}


@dataclass(frozen=True)
class QiTransitionTrajectoryLedgerResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    trajectory_status: str
    lineage_status: str
    authority_status: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    trajectory_candidate: Dict[str, Any]
    trajectory_receipt: Dict[str, Any]

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


def _trend(values: Sequence[float], tolerance: float = 0.03) -> str:
    if len(values) < 2:
        return "insufficient_history"
    delta = values[-1] - values[0]
    if delta > tolerance:
        return "increasing"
    if delta < -tolerance:
        return "decreasing"
    return "stable"


def _validate_next_state(record: Mapping[str, Any], index: int, errors: List[str]) -> None:
    state = record.get("next_state_candidate")
    if not isinstance(state, Mapping):
        errors.append(f"transition_records[{index}].next_state_candidate must be an object")
        return
    for key in STATE_REQUIRED_KEYS:
        if key not in state:
            errors.append(f"transition_records[{index}].next_state_candidate.{key} is required")
    if state.get("surface_type") != "QiStateCandidate":
        errors.append(f"transition_records[{index}].next_state_candidate.surface_type must be QiStateCandidate")
    if state.get("candidate_only") is not True:
        errors.append(f"transition_records[{index}].next_state_candidate.candidate_only must be true")
    for key in ["authority_granted", "clinical_authority_granted", "execution_authority_granted"]:
        if state.get(key) is not False:
            errors.append(f"transition_records[{index}].next_state_candidate.{key} must be false")
    for metric in METRIC_KEYS:
        if not _bounded(state.get(metric), 0.0, 1.0):
            errors.append(f"transition_records[{index}].next_state_candidate.{metric} must be a number in [0, 1]")


def validate_qi_transition_trajectory_ledger_packet(packet: Mapping[str, Any]) -> List[str]:
    """Return validation errors for a v0.2O trajectory ledger packet."""

    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    ledger = _section(packet, "trajectory_ledger", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)

    _require_true(ledger, "trajectory_ledger", REQUIRED_LEDGER_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)

    records = packet.get("transition_records")
    if not isinstance(records, list) or len(records) < 2:
        errors.append("transition_records must contain at least two records")
    else:
        previous_index: int | None = None
        seen_ids: set[str] = set()
        decisions_seen: set[str] = set()
        for index, record in enumerate(records):
            if not isinstance(record, Mapping):
                errors.append(f"transition_records[{index}] must be an object")
                continue
            for key in REQUIRED_RECORD_KEYS:
                if key not in record:
                    errors.append(f"transition_records[{index}].{key} is required")
            sequence_index = record.get("sequence_index")
            if not isinstance(sequence_index, int) or isinstance(sequence_index, bool):
                errors.append(f"transition_records[{index}].sequence_index must be an integer")
            elif previous_index is not None and sequence_index <= previous_index:
                errors.append(f"transition_records[{index}].sequence_index must strictly increase")
            else:
                previous_index = sequence_index

            transition_id = str(record.get("transition_id", ""))
            if not transition_id:
                errors.append(f"transition_records[{index}].transition_id must be nonempty")
            if transition_id in seen_ids:
                errors.append(f"transition_records[{index}].transition_id must be unique")
            seen_ids.add(transition_id)

            if not str(record.get("source_trace", "")):
                errors.append(f"transition_records[{index}].source_trace must be nonempty")
            decision = str(record.get("transition_decision", ""))
            decisions_seen.add(decision)
            if decision not in VALID_TRANSITION_DECISIONS:
                errors.append(f"transition_records[{index}].transition_decision must be a valid candidate decision")
            if not _bounded(record.get("risk_score"), 0.0, 1.0):
                errors.append(f"transition_records[{index}].risk_score must be a number in [0, 1]")
            if record.get("lineage_preserved") is not True:
                errors.append(f"transition_records[{index}].lineage_preserved must be true")
            if record.get("source_history_replaced") is not False:
                errors.append(f"transition_records[{index}].source_history_replaced must be false")
            if record.get("candidate_only") is not True:
                errors.append(f"transition_records[{index}].candidate_only must be true")
            for key in ["authority_granted", "clinical_authority_granted", "execution_authority_granted"]:
                if record.get(key) is not False:
                    errors.append(f"transition_records[{index}].{key} must be false")
            _validate_next_state(record, index, errors)

        if "candidate_hold" not in decisions_seen and ledger.get("hold_visible_as_canonical_outcome") is True:
            errors.append("transition_records must include at least one candidate_hold record for hold visibility")
        if "candidate_watch" not in decisions_seen and ledger.get("watch_visible_as_canonical_outcome") is True:
            errors.append("transition_records must include at least one candidate_watch record for watch visibility")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def build_trajectory_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    records_raw = packet.get("transition_records", [])
    records = [record for record in records_raw if isinstance(record, Mapping)] if isinstance(records_raw, list) else []

    risk_scores = [float(record.get("risk_score", 0.0)) for record in records if _bounded(record.get("risk_score"), 0.0, 1.0)]
    decisions = [str(record.get("transition_decision", "")) for record in records]
    states = [record.get("next_state_candidate") for record in records if isinstance(record.get("next_state_candidate"), Mapping)]

    latest_state = states[-1] if states else {}
    metric_paths: Dict[str, List[float]] = {}
    for metric in METRIC_KEYS:
        metric_paths[metric] = [
            float(state.get(metric, 0.0))
            for state in states
            if isinstance(state, Mapping) and _bounded(state.get(metric), 0.0, 1.0)
        ]

    hold_count = sum(1 for decision in decisions if decision == "candidate_hold")
    watch_count = sum(1 for decision in decisions if decision == "candidate_watch")
    continue_count = sum(1 for decision in decisions if decision == "candidate_continue")
    risk_trend = _trend(risk_scores)
    distortion_trend = _trend(metric_paths["qi_transport_distortion"])
    recoverability_trend = _trend(metric_paths["qi_recoverability_margin"])
    backflow_trend = _trend(metric_paths["qi_backflow"])
    tail_residue_trend = _trend(metric_paths["qi_tail_residue"])

    average_risk = _clamp01(_average(risk_scores))
    latest_risk = risk_scores[-1] if risk_scores else 0.0
    stability_index = _clamp01(1.0 - average_risk)

    if hold_count > 0 or latest_risk >= 0.65:
        trajectory_decision = "trajectory_hold_visible"
    elif watch_count > 0 or latest_risk >= 0.45:
        trajectory_decision = "trajectory_watch_visible"
    else:
        trajectory_decision = "trajectory_continue_candidate"

    return {
        "surface_type": "QiTransitionTrajectoryCandidate",
        "version": VERSION,
        "record_count": len(records),
        "continue_count": continue_count,
        "watch_count": watch_count,
        "hold_count": hold_count,
        "average_risk_score": round(average_risk, 6),
        "latest_risk_score": round(latest_risk, 6),
        "stability_index": round(stability_index, 6),
        "risk_trend": risk_trend,
        "backflow_trend": backflow_trend,
        "tail_residue_trend": tail_residue_trend,
        "recoverability_trend": recoverability_trend,
        "transport_distortion_trend": distortion_trend,
        "latest_qi_runtime_mode": str(latest_state.get("qi_runtime_mode", "<missing>")) if isinstance(latest_state, Mapping) else "<missing>",
        "trajectory_decision": trajectory_decision,
        "lineage_preserved": all(record.get("lineage_preserved") is True for record in records) if records else False,
        "source_history_replaced": any(record.get("source_history_replaced") is True for record in records),
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "execution_authority_granted": False,
        "handover_forced": False,
        "doctor_ai_consultation_blocked": False,
    }


def build_trajectory_receipt(packet: Mapping[str, Any], candidate: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "receipt_type": "QiTransitionTrajectoryLedgerReceipt",
        "version": VERSION,
        "trajectory_decision": str(candidate.get("trajectory_decision", "<missing>")),
        "record_count": int(candidate.get("record_count", 0)) if isinstance(candidate.get("record_count"), int) else 0,
        "lineage_preserved": bool(candidate.get("lineage_preserved")),
        "source_history_replaced": bool(candidate.get("source_history_replaced")),
        "candidate_only": True,
        "authority_accumulated": False,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "execution_authority_granted": False,
        "hold_visible": int(candidate.get("hold_count", 0)) > 0 if isinstance(candidate.get("hold_count"), int) else False,
        "watch_visible": int(candidate.get("watch_count", 0)) > 0 if isinstance(candidate.get("watch_count"), int) else False,
        "handover_forced": False,
        "doctor_ai_consultation_blocked": False,
        "non_authority_boundary_preserved": True,
    }


def build_qi_transition_trajectory_ledger_result(packet: Mapping[str, Any]) -> QiTransitionTrajectoryLedgerResult:
    errors = validate_qi_transition_trajectory_ledger_packet(packet)
    valid = not errors
    candidate = build_trajectory_candidate(packet)
    receipt = build_trajectory_receipt(packet, candidate)

    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []

    return QiTransitionTrajectoryLedgerResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        surface_type="QiTransitionTrajectoryLedgerResult",
        version=VERSION,
        trajectory_status="valid_append_only_qi_transition_trajectory" if valid else "invalid_qi_transition_trajectory",
        lineage_status="lineage_preserved" if valid else "lineage_validation_failed",
        authority_status="no_authority_accumulation" if valid else "authority_boundary_unvalidated",
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        trajectory_candidate=candidate,
        trajectory_receipt=receipt,
    )


def build_qi_transition_trajectory_ledger_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_transition_trajectory_ledger_result(packet).to_dict()
