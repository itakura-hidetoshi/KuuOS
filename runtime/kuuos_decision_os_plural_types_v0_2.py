from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import (
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
)
from runtime.kuuos_decision_os_types_v0_1 import ALL_DIMENSIONS

VERSION = "kuuos_decision_os_plural_harmony_appeal_kernel_v0_2"
STATE_VERSION = "kuuos_decision_os_plural_state_v0_2"
EVENT_VERSION = "kuuos_decision_os_plural_event_v0_2"
APPLY_RESULT_VERSION = "kuuos_decision_os_plural_apply_result_v0_2"
STORE_COMMIT_VERSION = "kuuos_decision_os_plural_store_commit_v0_2"
ACTIVATION_RECEIPT_VERSION = "kuuos_decision_os_plural_activation_receipt_v0_2"

PHASES = (
    "bind_v01",
    "register_stakeholders",
    "evaluate_plurality",
    "validate_vetoes",
    "aggregate",
    "explain",
    "appeal_window",
    "adjudicate",
    "commit",
)
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}

ROUTES = frozenset(
    {
        "CONSENSUS_CANDIDATE",
        "NEGOTIATE",
        "APPEAL",
        "HANDOVER",
        "HOLD",
        "REJECT",
        "QUARANTINE",
    }
)

NON_AUTHORITY = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "legal_authority_granted": False,
    "host_license_granted": False,
    "stakeholder_sovereignty_granted": False,
    "raw_veto_authority_granted": False,
    "consensus_truth_authority_granted": False,
    "memory_overwrite_authority_granted": False,
}

BOUNDARY = {
    "v01_source_is_read_only": True,
    "source_option_expansion_forbidden": True,
    "stakeholder_values_are_local_sections": True,
    "raw_veto_is_boundary_signal_only": True,
    "validated_veto_requires_mission_binding": True,
    "weighted_median_is_not_truth": True,
    "nash_product_is_not_truth": True,
    "worst_case_floor_is_preserved": True,
    "appeal_is_append_only": True,
    "consensus_is_not_execution": True,
    "activation_requires_replan": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def event_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_event_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_state_digest"))


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_apply_result_digest"))


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_store_commit_digest"))


def activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]


def clamp01(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0, maximum=1.0)


def bounded(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=-1.0, maximum=1.0)


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name}_must_be_bool")
    return value


def require_string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list):
        raise TypeError(f"{name}_must_be_list")
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        text = require_nonempty_string(item, f"{name}[{index}]")
        if text in seen:
            raise ValueError(f"{name}_duplicate")
        seen.add(text)
        result.append(text)
    return result


def validate_profile_weights(value: Mapping[str, Any]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for dimension in ALL_DIMENSIONS:
        weights[dimension] = clamp01(
            value.get(dimension), f"profile_weight.{dimension}"
        )
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("stakeholder_profile_weights_must_sum_to_one")
    return weights


def validate_thresholds(value: Mapping[str, Any]) -> dict[str, float]:
    result = {
        "minimum_support_weight": clamp01(
            value.get("minimum_support_weight"), "minimum_support_weight"
        ),
        "maximum_opposition_weight": clamp01(
            value.get("maximum_opposition_weight"), "maximum_opposition_weight"
        ),
        "minimum_worst_case_value": bounded(
            value.get("minimum_worst_case_value"), "minimum_worst_case_value"
        ),
        "consensus_separation_margin": clamp01(
            value.get("consensus_separation_margin"),
            "consensus_separation_margin",
        ),
        "material_appeal_threshold": clamp01(
            value.get("material_appeal_threshold"),
            "material_appeal_threshold",
        ),
    }
    if result["minimum_support_weight"] <= result["maximum_opposition_weight"]:
        raise ValueError("plural_support_must_exceed_opposition_ceiling")
    return result


def require_mapping_field(value: Any, name: str) -> Mapping[str, Any]:
    return require_mapping(value, name)


__all__ = [
    "ACTIVATION_RECEIPT_VERSION",
    "ALL_DIMENSIONS",
    "APPLY_RESULT_VERSION",
    "BOUNDARY",
    "EVENT_VERSION",
    "NON_AUTHORITY",
    "PHASES",
    "ROUTES",
    "STATE_VERSION",
    "STORE_COMMIT_VERSION",
    "VERSION",
    "activation_receipt_digest",
    "apply_result_digest",
    "bounded",
    "clamp01",
    "copy_boundary",
    "copy_non_authority",
    "event_digest",
    "next_phase",
    "require_bool",
    "require_mapping_field",
    "require_nonempty_string",
    "require_nonnegative_int",
    "require_string_list",
    "sha",
    "state_digest",
    "store_commit_digest",
    "validate_profile_weights",
    "validate_thresholds",
]
