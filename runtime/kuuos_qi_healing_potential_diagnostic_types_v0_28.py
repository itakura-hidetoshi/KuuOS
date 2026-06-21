from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_qi_healing_potential_diagnostic_kernel_v0_28"
PACKET_VERSION = "kuuos_qi_healing_potential_diagnostic_packet_v0_28"
REPORT_VERSION = "kuuos_qi_healing_potential_diagnostic_report_v0_28"
LEDGER_VERSION = "kuuos_qi_healing_potential_diagnostic_ledger_v0_28"

HEALING_POTENTIAL_CLASSES = frozenset(
    {
        "INSUFFICIENT_EVIDENCE",
        "HEALING_POTENTIAL_VISIBLE",
        "HEALING_POTENTIAL_UNCERTAIN",
        "HEALING_POTENTIAL_CONSTRAINED",
        "CLINICIAN_REVIEW_REQUIRED",
    }
)

DIAGNOSTIC_ROUTES = frozenset(
    {
        "REOBSERVE",
        "PRESERVE_PLURAL_HYPOTHESES",
        "EVALUATE_RECOVERY_WINDOW",
        "CLINICIAN_REVIEW_HANDOFF",
        "HOLD",
    }
)

PROCESS_HISTORY_FIELDS = (
    "time_index",
    "observation_id",
    "qi_recoverability_margin",
    "qi_coherence_margin",
    "qi_transport_distortion",
    "qi_tail_residue",
    "qi_memory_gain",
    "response_delta",
    "adaptive_stability",
    "intervention_burden",
    "bounded_intervention",
    "backaction_visible",
    "source_trace",
)

HYPOTHESIS_FIELDS = (
    "hypothesis_id",
    "label",
    "support",
    "counterevidence",
    "uncertainty",
    "severity",
    "candidate_only",
    "source_traces",
)

NON_AUTHORITY_FLAGS = {
    "grants_clinical_authority": False,
    "grants_diagnosis_authority": False,
    "grants_prognosis_authority": False,
    "grants_treatment_authority": False,
    "grants_prescription_authority": False,
    "grants_formula_selection_authority": False,
    "grants_triage_authority": False,
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_safety_override_authority": False,
    "grants_irreversibility_authority": False,
}

REQUIRED_BOUNDARY = {
    "process_history_is_primary": True,
    "current_snapshot_does_not_replace_history": True,
    "diagnosis_remains_plural_candidate_set": True,
    "healing_potential_is_separate_from_diagnostic_support": True,
    "severity_does_not_imply_irreversibility": True,
    "recoverability_does_not_imply_guaranteed_healing": True,
    "positive_response_does_not_imply_cure": True,
    "negative_response_does_not_erase_future_recovery_window": True,
    "counterevidence_is_preserved": True,
    "uncertainty_is_preserved": True,
    "red_flags_open_clinician_handoff_not_auto_triage": True,
    "clinician_review_required_for_clinical_use": True,
    "treatment_route_remains_separate": True,
    "memory_history_is_append_only": True,
    "source_trace_is_required": True,
    "backaction_is_visible": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "diagnostic_packet_digest")


def report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "diagnostic_report_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_bool_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name}_int_required")
    return value


def require_nonnegative_int(value: Any, name: str) -> int:
    result = require_int(value, name)
    if result < 0:
        raise ValueError(f"{name}_nonnegative_required")
    return result


def require_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    return float(value)


def require_bounded(value: Any, name: str, lower: float, upper: float) -> float:
    result = require_number(value, name)
    if result < lower or result > upper:
        raise ValueError(f"{name}_out_of_range")
    return result


def require_sequence(value: Any, name: str, *, allow_empty: bool = False) -> list[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError(f"{name}_list_required")
    result = list(value)
    if not allow_empty and not result:
        raise ValueError(f"{name}_nonempty_required")
    return result


def require_string_list(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    items = require_sequence(value, name, allow_empty=allow_empty)
    result = [require_string(item, name) for item in items]
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def average(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


__all__ = [
    "DIAGNOSTIC_ROUTES",
    "HEALING_POTENTIAL_CLASSES",
    "HYPOTHESIS_FIELDS",
    "LEDGER_VERSION",
    "NON_AUTHORITY_FLAGS",
    "PACKET_VERSION",
    "PROCESS_HISTORY_FIELDS",
    "REPORT_VERSION",
    "REQUIRED_BOUNDARY",
    "VERSION",
    "average",
    "clamp01",
    "copy_boundary",
    "copy_non_authority",
    "packet_digest",
    "report_digest",
    "require_bool",
    "require_bounded",
    "require_nonnegative_int",
    "require_sequence",
    "require_string",
    "require_string_list",
    "without",
]
