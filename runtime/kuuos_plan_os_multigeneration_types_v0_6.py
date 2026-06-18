from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_bounded_multi_generation_supervisor_v0_6"
POLICY_VERSION = "kuuos_plan_os_multi_generation_policy_v0_6"
REPORT_VERSION = "kuuos_plan_os_supervised_generation_report_v0_6"
DECISION_VERSION = "kuuos_plan_os_generation_supervision_decision_v0_6"
STATE_VERSION = "kuuos_plan_os_multi_generation_supervisor_state_v0_6"
EVENT_VERSION = "kuuos_plan_os_multi_generation_supervisor_event_v0_6"
STORE_COMMIT_VERSION = "kuuos_plan_os_multi_generation_store_commit_v0_6"

ACTIVE = "ACTIVE"
HOLD = "HOLD"
STOPPED = "STOPPED"
HANDOVER = "HANDOVER"
TERMINAL_STATUSES = {HOLD, STOPPED, HANDOVER}

CONTINUE = "CONTINUE"
STOP_CONVERGED = "STOP_CONVERGED"
STOP_MAX_GENERATIONS = "STOP_MAX_GENERATIONS"
STOP_STAGNATION = "STOP_STAGNATION"
STOP_OSCILLATION = "STOP_OSCILLATION"
HOLD_OBSERVATION_DEBT = "HOLD_OBSERVATION_DEBT"
HOLD_RECOVERY = "HOLD_RECOVERY"
STOP_MISSION_COMPLETE = "STOP_MISSION_COMPLETE"
HANDOVER_HUMAN = "HANDOVER_HUMAN"
HANDOVER_AUTHORITY = "HANDOVER_AUTHORITY"

DECISIONS = {
    CONTINUE,
    STOP_CONVERGED,
    STOP_MAX_GENERATIONS,
    STOP_STAGNATION,
    STOP_OSCILLATION,
    HOLD_OBSERVATION_DEBT,
    HOLD_RECOVERY,
    STOP_MISSION_COMPLETE,
    HANDOVER_HUMAN,
    HANDOVER_AUTHORITY,
}

NON_AUTHORITY = {
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

BOUNDARY = {
    "bounded_generation_count_required": True,
    "exact_successor_cycle_required": True,
    "generation_receipt_chain_required": True,
    "terminal_state_blocks_automatic_continuation": True,
    "hold_requires_external_resume": True,
    "handover_requires_external_owner": True,
    "mission_completion_is_terminal": True,
    "authority_boundary_is_handover": True,
    "execution_owned_by_act_os": True,
    "replan_owned_by_plan_os": True,
    "selection_owned_by_decision_os": True,
    "memory_overwrite_forbidden": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def policy_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "multi_generation_policy_digest")


def report_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "supervised_generation_report_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "generation_supervision_decision_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "multi_generation_supervisor_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "multi_generation_supervisor_event_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "multi_generation_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value


def unit_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ValueError(f"{name}_unit_interval_required")
    return number
