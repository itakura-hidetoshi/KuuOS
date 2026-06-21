from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_qi_window_trajectory_kernel_v0_29"
PACKET_VERSION = "kuuos_qi_window_trajectory_packet_v0_29"
REPORT_VERSION = "kuuos_qi_window_trajectory_report_v0_29"

TRAJECTORY_CLASSES = frozenset({
    "INSUFFICIENT_HISTORY",
    "WINDOW_OPENING",
    "WINDOW_STABLE_VISIBLE",
    "WINDOW_OSCILLATING",
    "WINDOW_CONSTRICTING",
    "WINDOW_DORMANT_REOPENABLE",
    "REVIEW_HANDOFF",
})

TRAJECTORY_ROUTES = frozenset({
    "REOBSERVE",
    "CONTINUE_TRAJECTORY_OBSERVATION",
    "PRESERVE_OSCILLATION",
    "PRESERVE_REOPENING_MEMORY",
    "REVIEW_HANDOFF",
    "HOLD",
})

NON_AUTHORITY = {
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

BOUNDARY = {
    "source_v028_reports_required": True,
    "process_history_is_primary": True,
    "current_report_does_not_replace_history": True,
    "single_decline_does_not_close_future_window": True,
    "prior_visible_window_is_remembered": True,
    "oscillation_is_preserved_not_flattened": True,
    "relapse_does_not_imply_irreversibility": True,
    "dormant_window_may_remain_reopenable": True,
    "trajectory_class_is_candidate_only": True,
    "trajectory_is_not_prognosis": True,
    "trajectory_is_not_treatment_instruction": True,
    "red_flags_open_review_not_auto_triage": True,
    "source_trace_is_required": True,
    "append_only_lineage_required": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "trajectory_packet_digest")


def report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "trajectory_report_digest")


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


def require_bounded(value: Any, name: str, lower: float = 0.0, upper: float = 1.0) -> float:
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


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def average(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


__all__ = [
    "BOUNDARY",
    "NON_AUTHORITY",
    "PACKET_VERSION",
    "REPORT_VERSION",
    "TRAJECTORY_CLASSES",
    "TRAJECTORY_ROUTES",
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
]
