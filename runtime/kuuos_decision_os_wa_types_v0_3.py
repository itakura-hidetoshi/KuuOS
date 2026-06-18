from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import (
    canonical_json,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    require_unique_strings,
    sha,
)
from runtime.kuuos_decision_os_types_v0_1 import clamp01, validate_interval

VERSION = "kuuos_decision_os_wa_relational_harmony_v0_3"
EVENT_VERSION = "kuuos_decision_os_wa_event_v0_3"
STATE_VERSION = "kuuos_decision_os_wa_state_v0_3"
STORE_COMMIT_VERSION = "kuuos_decision_os_wa_store_commit_v0_3"
APPLY_RESULT_VERSION = "kuuos_decision_os_wa_apply_result_v0_3"
ACTIVATION_RECEIPT_VERSION = "kuuos_decision_os_wa_activation_receipt_v0_3"

PHASES = (
    "bind",
    "profile",
    "evaluate",
    "false_harmony_check",
    "plurality_check",
    "gate",
    "commit",
)
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}

POSITIVE_DIMENSIONS = (
    "inclusion",
    "dialogue",
    "mutual_reflection",
    "emergence",
    "dynamic_adaptation",
    "non_hierarchy",
    "recursive_feedback",
)

ALERT_DIMENSIONS = (
    "coercive_conformity",
    "exclusion",
    "oppression",
    "hierarchy_concentration",
    "minority_erasure",
    "false_stability",
    "complacency_in_safe_conditions",
)

ROUTES = frozenset(
    {
        "ENDORSE",
        "REOBSERVE",
        "REPAIR",
        "ESCALATE",
        "HOLD",
        "REJECT",
        "QUARANTINE",
    }
)

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "moral_veto_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "legal_authority_granted": False,
    "host_license_granted": False,
    "memory_overwrite_authority_granted": False,
    "global_value_authority_granted": False,
    "universal_priority_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "wa_is_dynamic_relational_harmony": True,
    "indra_network_internal_model": True,
    "v02_plural_source_is_read_only": True,
    "stakeholder_local_sections_preserved": True,
    "veto_and_appeal_history_preserved": True,
    "wa_is_not_unanimity": True,
    "wa_is_not_obedience": True,
    "wa_is_not_majority_rule": True,
    "wa_is_not_truth": True,
    "wa_is_not_execution": True,
    "wa_is_not_moral_veto": True,
    "false_harmony_detection_required": True,
    "minority_preservation_required": True,
    "dissent_consideration_required": True,
    "retained_alternatives_preserved": True,
    "silent_option_substitution_forbidden": True,
    "smooth_surface_is_not_proof": True,
    "safe_place_vigilance_required": True,
    "activation_requires_replan": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def wa_event_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wa_event_digest"))


def wa_state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wa_state_digest"))


def wa_store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wa_store_commit_digest"))


def wa_apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wa_apply_result_digest"))


def wa_activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "wa_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def normalize_string_list(
    value: Sequence[Any], name: str, *, allow_empty: bool = True
) -> list[str]:
    return require_unique_strings(value, name, allow_empty=allow_empty)


def validate_wa_weights(value: Mapping[str, Any]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for dimension in POSITIVE_DIMENSIONS:
        weights[dimension] = clamp01(value.get(dimension), f"wa_weight.{dimension}")
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError("wa_weights_must_sum_to_one")
    return weights


def validate_wa_thresholds(value: Mapping[str, Any]) -> dict[str, float]:
    result = {
        "bottleneck_weight": clamp01(
            value.get("bottleneck_weight"), "bottleneck_weight"
        ),
        "minimum_wa_floor": clamp01(
            value.get("minimum_wa_floor"), "minimum_wa_floor"
        ),
        "minimum_dimension_floor": clamp01(
            value.get("minimum_dimension_floor"), "minimum_dimension_floor"
        ),
        "suspected_false_harmony_threshold": clamp01(
            value.get("suspected_false_harmony_threshold"),
            "suspected_false_harmony_threshold",
        ),
        "confirmed_false_harmony_threshold": clamp01(
            value.get("confirmed_false_harmony_threshold"),
            "confirmed_false_harmony_threshold",
        ),
    }
    if (
        result["suspected_false_harmony_threshold"]
        > result["confirmed_false_harmony_threshold"]
    ):
        raise ValueError("wa_false_harmony_threshold_order_invalid")
    return result


def validate_axis_intervals(
    value: Mapping[str, Any], dimensions: Sequence[str], name: str
) -> dict[str, dict[str, float]]:
    normalized: dict[str, dict[str, float]] = {}
    for dimension in dimensions:
        normalized[dimension] = validate_interval(
            require_mapping(value.get(dimension), f"{name}.{dimension}"),
            f"{name}.{dimension}",
        )
    return normalized


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]
