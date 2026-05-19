#!/usr/bin/env python3
"""Physical Quantum Qi Observation Kernel runtime v0.2M.

This module implements the minimal runtime projection:

    observation event sequence -> non-authoritative QiStateCandidate

Canonical interpretation:
- Process Tensor remains the multi-time non-Markov temporal structure.
- Qi is a history-bearing relational/action/recoverability flow projected from
  observation events and process-memory residues.
- Observation is not free: every event must preserve backaction visibility,
  source trace, and authority boundaries.

This runtime does not simulate quantum mechanics. It computes bounded runtime
candidate metrics and validates that no proof, truth, ontology, clinical,
execution, commit, memory-overwrite, world-rewrite, or safety-override authority
is granted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence

VERSION = "v0.2M"
PACKET_TYPE = "physical_quantum_qi_observation_kernel_packet"

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
    "observation_sequence_declared",
    "process_tensor_context_required",
    "non_markov_memory_primary",
    "history_state_not_replaced_by_snapshot",
    "observation_backaction_visible",
    "source_trace_required",
    "qi_state_projection_is_candidate_only",
    "qi_is_operator_valued_flow_not_substantial_essence",
    "clinical_consultation_boundary_preserved",
]

REQUIRED_METRICS = [
    "qi_memory_gain",
    "qi_backflow",
    "qi_env_correlation_credit",
    "qi_temporal_complexity",
    "qi_coherence_margin",
    "qi_recoverability_margin",
    "qi_transport_distortion",
    "qi_tail_residue",
]

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.qi_observation_candidate",
    "MemoryOS.qi_process_history_record_candidate",
    "ReflectionOS.qi_residue_analysis_candidate",
    "PlanOS.qi_transport_candidate",
    "DecisionOS.qi_safety_evaluable_candidate",
    "QiProcessTensor.observation_update_surface",
}

FORBIDDEN_REDUCTIONS_FALSE = [
    "observation_collapsed_to_free_readout",
    "qi_state_claimed_as_truth",
    "qi_state_claimed_as_clinical_action",
    "qi_projection_replaces_source_history",
    "current_snapshot_replaces_process_history",
    "backaction_erased",
    "environment_memory_erased",
    "tail_residue_hidden",
    "handover_forced_by_red_flag_alone",
    "doctor_ai_consultation_blocked_by_default",
]

EVENT_REQUIRED_KEYS = [
    "time_index",
    "event_id",
    "operation_id",
    "observation_kind",
    "signal_strength",
    "coherence_delta",
    "recoverability_delta",
    "transport_distortion_delta",
    "memory_residue",
    "backflow_weight",
    "env_correlation_weight",
    "backaction_visible",
    "source_trace",
]


@dataclass(frozen=True)
class QiObservationKernelResult:
    packet_id: str
    valid: bool
    errors: List[str]
    surface_type: str
    version: str
    qi_state_status: str
    non_markov_status: str
    observation_status: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    qi_state_candidate: Dict[str, Any]

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


def validate_qi_observation_kernel_packet(packet: Mapping[str, Any]) -> List[str]:
    """Return validation errors for a v0.2M observation-kernel packet."""

    errors: List[str] = []
    if packet.get("packet_type") != PACKET_TYPE:
        errors.append(f"packet_type must be {PACKET_TYPE}")
    if packet.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")

    kernel = _section(packet, "observation_kernel", errors)
    metric_schema = _section(packet, "metric_schema", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)

    _require_true(kernel, "observation_kernel", REQUIRED_KERNEL_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_REDUCTIONS_FALSE, errors)
    _require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)

    metrics = metric_schema.get("metrics")
    if not isinstance(metrics, list):
        errors.append("metric_schema.metrics must be a list")
    else:
        missing_metrics = sorted(set(REQUIRED_METRICS) - {str(metric) for metric in metrics})
        for metric in missing_metrics:
            errors.append(f"metric_schema.metrics missing {metric}")

    events = packet.get("observation_events")
    if not isinstance(events, list) or len(events) < 2:
        errors.append("observation_events must contain at least two events")
    else:
        previous_time: int | None = None
        seen_event_ids: set[str] = set()
        for index, event in enumerate(events):
            if not isinstance(event, Mapping):
                errors.append(f"observation_events[{index}] must be an object")
                continue
            for key in EVENT_REQUIRED_KEYS:
                if key not in event:
                    errors.append(f"observation_events[{index}].{key} is required")
            event_id = str(event.get("event_id", ""))
            if not event_id:
                errors.append(f"observation_events[{index}].event_id must be nonempty")
            if event_id in seen_event_ids:
                errors.append(f"observation_events[{index}].event_id must be unique")
            seen_event_ids.add(event_id)

            time_index = event.get("time_index")
            if not isinstance(time_index, int) or isinstance(time_index, bool):
                errors.append(f"observation_events[{index}].time_index must be an integer")
            elif previous_time is not None and time_index <= previous_time:
                errors.append(f"observation_events[{index}].time_index must strictly increase")
            else:
                previous_time = time_index

            if not str(event.get("operation_id", "")):
                errors.append(f"observation_events[{index}].operation_id must be nonempty")
            if not str(event.get("observation_kind", "")):
                errors.append(f"observation_events[{index}].observation_kind must be nonempty")
            if not str(event.get("source_trace", "")):
                errors.append(f"observation_events[{index}].source_trace must be nonempty")
            if event.get("backaction_visible") is not True:
                errors.append(f"observation_events[{index}].backaction_visible must be true")

            for key in [
                "signal_strength",
                "transport_distortion_delta",
                "memory_residue",
                "backflow_weight",
                "env_correlation_weight",
            ]:
                if not _bounded(event.get(key), 0.0, 1.0):
                    errors.append(f"observation_events[{index}].{key} must be a number in [0, 1]")
            for key in ["coherence_delta", "recoverability_delta"]:
                if not _bounded(event.get(key), -1.0, 1.0):
                    errors.append(f"observation_events[{index}].{key} must be a number in [-1, 1]")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def project_qi_state_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Project a validated-looking packet into bounded Qi state candidate metrics.

    The projection is deliberately conservative: invalid packets may still produce
    a diagnostic candidate, but authority is always false and source history is
    never replaced.
    """

    events_raw = packet.get("observation_events", [])
    events = [event for event in events_raw if isinstance(event, Mapping)] if isinstance(events_raw, list) else []

    signal_strengths = [float(event.get("signal_strength", 0.0)) for event in events if _bounded(event.get("signal_strength"), 0.0, 1.0)]
    coherence_deltas = [float(event.get("coherence_delta", 0.0)) for event in events if _bounded(event.get("coherence_delta"), -1.0, 1.0)]
    recoverability_deltas = [float(event.get("recoverability_delta", 0.0)) for event in events if _bounded(event.get("recoverability_delta"), -1.0, 1.0)]
    transport_deltas = [float(event.get("transport_distortion_delta", 0.0)) for event in events if _bounded(event.get("transport_distortion_delta"), 0.0, 1.0)]
    memory_residues = [float(event.get("memory_residue", 0.0)) for event in events if _bounded(event.get("memory_residue"), 0.0, 1.0)]
    backflows = [float(event.get("backflow_weight", 0.0)) for event in events if _bounded(event.get("backflow_weight"), 0.0, 1.0)]
    env_corrs = [float(event.get("env_correlation_weight", 0.0)) for event in events if _bounded(event.get("env_correlation_weight"), 0.0, 1.0)]

    operations = {str(event.get("operation_id")) for event in events if str(event.get("operation_id", ""))}
    kinds = {str(event.get("observation_kind")) for event in events if str(event.get("observation_kind", ""))}
    event_count = len(events)

    qi_memory_gain = _clamp01(_average(memory_residues) * (0.5 + 0.5 * _average(env_corrs)))
    qi_backflow = _clamp01(_average(backflows))
    qi_env_correlation_credit = _clamp01(_average(env_corrs))
    qi_temporal_complexity = _clamp01((event_count + len(operations) + len(kinds)) / 12.0)
    qi_coherence_margin = _clamp01(0.5 + 0.5 * _average(coherence_deltas))
    qi_recoverability_margin = _clamp01(0.5 + 0.5 * _average(recoverability_deltas))
    qi_transport_distortion = _clamp01(_average(transport_deltas))
    qi_tail_residue = _clamp01(_average(memory_residues))

    if qi_backflow >= 0.55:
        mode = "counterflow_watch"
    elif qi_tail_residue >= 0.55:
        mode = "stagnation_watch"
    elif qi_recoverability_margin <= 0.35 or qi_coherence_margin <= 0.35:
        mode = "deficiency_watch"
    else:
        mode = "monitor_continue"

    return {
        "surface_type": "QiStateCandidate",
        "version": VERSION,
        "event_count": event_count,
        "operation_count": len(operations),
        "observation_kind_count": len(kinds),
        "qi_memory_gain": round(qi_memory_gain, 6),
        "qi_backflow": round(qi_backflow, 6),
        "qi_env_correlation_credit": round(qi_env_correlation_credit, 6),
        "qi_temporal_complexity": round(qi_temporal_complexity, 6),
        "qi_coherence_margin": round(qi_coherence_margin, 6),
        "qi_recoverability_margin": round(qi_recoverability_margin, 6),
        "qi_transport_distortion": round(qi_transport_distortion, 6),
        "qi_tail_residue": round(qi_tail_residue, 6),
        "qi_runtime_mode": mode,
        "source_history_replaced": False,
        "backaction_visible": all(event.get("backaction_visible") is True for event in events) if events else False,
        "candidate_only": True,
        "authority_granted": False,
        "clinical_authority_granted": False,
        "execution_authority_granted": False,
    }


def build_qi_observation_kernel_result(packet: Mapping[str, Any]) -> QiObservationKernelResult:
    errors = validate_qi_observation_kernel_packet(packet)
    valid = not errors

    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []

    return QiObservationKernelResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        surface_type="QiObservationKernelResult",
        version=VERSION,
        qi_state_status="valid_qi_state_candidate" if valid else "invalid_qi_state_candidate",
        non_markov_status="history_bearing_non_markov_projection" if valid else "non_markov_projection_failed",
        observation_status="backaction_visible_observation_sequence" if valid else "observation_validation_failed",
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in AUTHORITY_FALSE_FIELDS},
        qi_state_candidate=project_qi_state_candidate(packet),
    )


def build_qi_observation_kernel_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return build_qi_observation_kernel_result(packet).to_dict()
