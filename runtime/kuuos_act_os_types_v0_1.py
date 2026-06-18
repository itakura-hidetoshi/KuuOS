from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import canonical_json, sha

VERSION = "kuuos_act_os_authority_bound_invocation_v0_1"
STATE_VERSION = "kuuos_act_os_state_v0_1"
EVENT_VERSION = "kuuos_act_os_event_v0_1"
AUTHORIZATION_VERSION = "kuuos_act_os_step_authorization_v0_1"
STORE_COMMIT_VERSION = "kuuos_act_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_act_os_apply_result_v0_1"

PHASES = ("bind", "select", "authorize", "project", "invoke", "verify", "commit")
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}
ROUTES = frozenset({"PENDING", "EFFECT_RECORDED", "BLOCKED", "REPLAYED"})

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "final_commitment_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "theorem_authority_granted": False,
    "unrestricted_tool_authority_granted": False,
    "unrestricted_shell_authority_granted": False,
    "unrestricted_network_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "plan_activation_is_not_execution_authority": True,
    "explicit_act_phase_receipt_required": True,
    "exact_act_candidate_step_required": True,
    "explicit_step_authorization_required": True,
    "valid_v017_host_license_required": True,
    "exact_v017_projection_required": True,
    "one_host_invocation_at_most": True,
    "one_job_per_invocation": True,
    "one_bounded_slice_per_invocation": True,
    "lower_host_receipt_is_canonical": True,
    "duplicate_invocation_idempotent": True,
    "observation_debt_preserved": True,
    "verification_debt_preserved": True,
    "lower_authority_preserved": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = dict(value)
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "act_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "act_event_digest")


def authorization_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "step_authorization_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "act_store_commit_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "act_apply_result_digest")


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
