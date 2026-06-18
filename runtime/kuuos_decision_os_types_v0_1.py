from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import (
    canonical_json,
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    require_unique_strings,
    sha,
)

VERSION = "kuuos_decision_os_relational_deliberation_kernel_v0_1"
EVENT_VERSION = "kuuos_decision_os_event_v0_1"
STATE_VERSION = "kuuos_decision_os_state_v0_1"
STORE_COMMIT_VERSION = "kuuos_decision_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_decision_os_apply_result_v0_1"
ACTIVATION_RECEIPT_VERSION = "kuuos_decision_os_activation_receipt_v0_1"

PHASES = (
    "frame",
    "generate",
    "constrain",
    "evaluate",
    "challenge",
    "qi_condition",
    "two_truths_check",
    "middle_way_gate",
    "decide",
    "commit",
)
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}

ROUTES = frozenset(
    {
        "SELECT_CANDIDATE",
        "OBSERVE",
        "EXPERIMENT_RECOMMENDED",
        "HOLD",
        "REPAIR",
        "ESCALATE",
        "REJECT",
        "QUARANTINE",
    }
)

ACTION_CLASSES = frozenset(
    {"observe", "experiment", "exploit", "repair", "hold", "escalate", "local_action"}
)

POSITIVE_DIMENSIONS = (
    "mission_alignment",
    "expected_benefit",
    "information_gain",
    "recoverability",
    "reversibility",
    "stakeholder_fit",
    "qi_process_compatibility",
)
NEGATIVE_DIMENSIONS = (
    "expected_harm",
    "cost_burden",
    "delay_risk",
    "uncertainty_burden",
)
ALL_DIMENSIONS = POSITIVE_DIMENSIONS + NEGATIVE_DIMENSIONS

QI_ALLOWED_ROLES = frozenset(
    {
        "temporal_transition_context",
        "recovery_trajectory_signal",
        "reversibility_context",
        "timing_context",
        "stakeholder_resonance_context",
        "uncertainty_context",
    }
)
QI_FORBIDDEN_ROLES = frozenset(
    {
        "truth_authority",
        "execution_license",
        "moral_veto",
        "clinical_order",
        "universal_priority",
    }
)

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
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
    "mission_contract_is_source_authority": True,
    "belief_os_is_conditional_epistemic_source": True,
    "advisory_policy_receipts_are_non_authoritative": True,
    "decision_is_not_truth": True,
    "decision_is_not_execution": True,
    "decision_is_not_host_license": True,
    "interval_evaluation_required": True,
    "universal_total_order_forbidden": True,
    "alternatives_retained": True,
    "counterfactuals_are_not_outcomes": True,
    "qi_is_context_only": True,
    "two_truths_separated": True,
    "middle_way_required": True,
    "activation_requires_replan": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def event_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "decision_event_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "decision_state_digest"))


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "decision_store_commit_digest"))


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "decision_apply_result_digest"))


def activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "decision_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def clamp01(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0, maximum=1.0)


def bounded_value(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=-1.0, maximum=1.0)


def validate_interval(value: Mapping[str, Any], name: str) -> dict[str, float]:
    lower = clamp01(value.get("lower"), f"{name}.lower")
    upper = clamp01(value.get("upper"), f"{name}.upper")
    if lower > upper:
        raise ValueError(f"{name}_interval_inverted")
    return {"lower": lower, "upper": upper}


def validate_value_interval(value: Mapping[str, Any], name: str) -> dict[str, float]:
    lower = bounded_value(value.get("lower"), f"{name}.lower")
    upper = bounded_value(value.get("upper"), f"{name}.upper")
    if lower > upper:
        raise ValueError(f"{name}_interval_inverted")
    return {"lower": lower, "upper": upper}


def validate_weights(value: Mapping[str, Any]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for dimension in ALL_DIMENSIONS:
        weights[dimension] = clamp01(value.get(dimension), f"weight.{dimension}")
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError("decision_weights_must_sum_to_one")
    return weights


def validate_thresholds(value: Mapping[str, Any]) -> dict[str, float]:
    maximum_risk = clamp01(value.get("maximum_risk"), "maximum_risk")
    minimum_recoverability = clamp01(
        value.get("minimum_recoverability"), "minimum_recoverability"
    )
    minimum_reversibility = clamp01(
        value.get("minimum_reversibility"), "minimum_reversibility"
    )
    dominance_margin = clamp01(value.get("dominance_margin"), "dominance_margin")
    observe_width = clamp01(value.get("observe_width"), "observe_width")
    experiment_information_gain = clamp01(
        value.get("experiment_information_gain"), "experiment_information_gain"
    )
    experiment_maximum_risk = clamp01(
        value.get("experiment_maximum_risk"), "experiment_maximum_risk"
    )
    experiment_minimum_recoverability = clamp01(
        value.get("experiment_minimum_recoverability"),
        "experiment_minimum_recoverability",
    )
    middle_way_maximum_risk = clamp01(
        value.get("middle_way_maximum_risk"), "middle_way_maximum_risk"
    )
    return {
        "maximum_risk": maximum_risk,
        "minimum_recoverability": minimum_recoverability,
        "minimum_reversibility": minimum_reversibility,
        "dominance_margin": dominance_margin,
        "observe_width": observe_width,
        "experiment_information_gain": experiment_information_gain,
        "experiment_maximum_risk": experiment_maximum_risk,
        "experiment_minimum_recoverability": experiment_minimum_recoverability,
        "middle_way_maximum_risk": middle_way_maximum_risk,
    }


def normalize_string_list(
    value: Sequence[Any], name: str, *, allow_empty: bool = True
) -> list[str]:
    return require_unique_strings(value, name, allow_empty=allow_empty)


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]
