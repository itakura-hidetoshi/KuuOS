from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_next_cycle_session_bootstrap_v0_15"
SESSION_VERSION = "kuuos_plan_os_control_session_v0_15"
STORE_COMMIT_VERSION = "kuuos_plan_os_control_session_store_commit_v0_15"

SESSION_ACTIVE = "SESSION_ACTIVE"
PLAN_BIND = "bind"

NON_AUTHORITY = {
    "execution_authority_granted": False,
    "host_license_granted": False,
    "automatic_renewal_granted": False,
    "memory_overwrite_authority_granted": False,
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
}

BOUNDARY = {
    "v14_activation_receipt_required": True,
    "exact_v13_materialization_required": True,
    "active_from_cycle_exact": True,
    "plan_phase_exact": True,
    "owner_epoch_scope_preserved": True,
    "lease_monitor_started": True,
    "initial_plan_phase_bind": True,
    "initial_plan_state_empty": True,
    "single_activation_consumption": True,
    "session_not_execution": True,
    "host_invocation_not_granted": True,
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


def session_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "plan_control_session_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "plan_control_session_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
