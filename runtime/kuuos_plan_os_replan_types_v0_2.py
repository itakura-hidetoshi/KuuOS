from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import canonical_json, sha

VERSION = "kuuos_plan_os_qi_conditioned_nonmarkov_replan_v0_2"
STATE_VERSION = "kuuos_plan_os_replan_state_v0_2"
EVENT_VERSION = "kuuos_plan_os_replan_event_v0_2"
HISTORY_PACKET_VERSION = "kuuos_plan_os_nonmarkov_history_packet_v0_2"
QI_CONDITION_PACKET_VERSION = "kuuos_plan_os_qi_condition_packet_v0_2"
CANDIDATE_PACKET_VERSION = "kuuos_plan_os_replan_candidate_v0_2"
CONSTRAINT_REPORT_VERSION = "kuuos_plan_os_candidate_constraint_report_v0_2"
DECISION_RECEIPT_VERSION = "kuuos_plan_os_decision_bound_receipt_v0_2"
SYNTHESIS_PACKET_VERSION = "kuuos_plan_os_next_basis_synthesis_v0_2"
REPLAN_PHASE_RECEIPT_VERSION = "kuuos_plan_os_replan_phase_receipt_v0_2"
STORE_COMMIT_VERSION = "kuuos_plan_os_replan_store_commit_v0_2"
APPLY_RESULT_VERSION = "kuuos_plan_os_replan_apply_result_v0_2"

PHASES = (
    "bind",
    "history",
    "qi_condition",
    "generate",
    "constrain",
    "deliberate",
    "synthesize",
    "commit_next",
)
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}

ROUTES = frozenset(
    {
        "PENDING",
        "NEXT_PLAN_CANDIDATE",
        "REPAIR_PLAN_CANDIDATE",
        "REOBSERVATION_PLAN_CANDIDATE",
        "REROUTE_PLAN_CANDIDATE",
        "TERMINATION_PLAN_CANDIDATE",
        "HOLD",
    }
)

CANDIDATE_TYPES = frozenset(
    {
        "continue",
        "strengthen",
        "repair",
        "slow_down",
        "reobserve",
        "reroute",
        "hold",
        "terminate_candidate",
    }
)

ROUTE_BY_CANDIDATE_TYPE = {
    "continue": "NEXT_PLAN_CANDIDATE",
    "strengthen": "NEXT_PLAN_CANDIDATE",
    "slow_down": "NEXT_PLAN_CANDIDATE",
    "repair": "REPAIR_PLAN_CANDIDATE",
    "reobserve": "REOBSERVATION_PLAN_CANDIDATE",
    "reroute": "REROUTE_PLAN_CANDIDATE",
    "terminate_candidate": "TERMINATION_PLAN_CANDIDATE",
    "hold": "HOLD",
}

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "execution_authority_granted": False,
    "final_commitment_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "theorem_authority_granted": False,
    "host_license_granted": False,
}

REQUIRED_BOUNDARY = {
    "replan_owned_by_plan_os": True,
    "decision_selection_owned_by_decision_os": True,
    "plan_synthesis_owned_by_plan_os": True,
    "execution_owned_by_act_os": True,
    "current_plan_is_read_only": True,
    "learn_delta_is_read_only": True,
    "non_markov_history_required": True,
    "qi_is_context_only": True,
    "hysteresis_required": True,
    "decision_receipt_required": True,
    "future_only_next_basis": True,
    "current_cycle_mutation_forbidden": True,
    "past_plan_mutation_forbidden": True,
    "activation_requires_next_plan_phase": True,
    "append_only_history_required": True,
    "duplicate_event_idempotent": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def replan_state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "replan_state_digest")


def replan_event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "replan_event_digest")


def history_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "history_packet_digest")


def qi_condition_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "qi_condition_packet_digest")


def candidate_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "candidate_digest")


def constraint_report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "constraint_report_digest")


def decision_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "decision_receipt_digest")


def synthesis_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "synthesis_packet_digest")


def replan_phase_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "replan_phase_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "replan_store_commit_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "replan_apply_result_digest")


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_bool_required")
    return value


def finite_number(
    value: Any,
    name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    number = float(value)
    if number != number or number in (float("inf"), float("-inf")):
        raise ValueError(f"{name}_finite_required")
    if minimum is not None and number < minimum:
        raise ValueError(f"{name}_below_minimum")
    if maximum is not None and number > maximum:
        raise ValueError(f"{name}_above_maximum")
    return number


def unit_number(value: Any, name: str) -> float:
    return finite_number(value, name, minimum=0.0, maximum=1.0)


def nonnegative_number(value: Any, name: str) -> float:
    return finite_number(value, name, minimum=0.0)


def unique_strings(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name}_list_required")
    items = [require_string(item, name) for item in value]
    if not allow_empty and not items:
        raise ValueError(f"{name}_nonempty_required")
    if len(items) != len(set(items)):
        raise ValueError(f"{name}_duplicate")
    return items
