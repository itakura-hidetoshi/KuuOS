from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

HANDOFF_VERSION = "kuuos_plan_os_suspension_recovery_handoff_v0_17"
STORE_COMMIT_VERSION = "kuuos_plan_os_suspension_recovery_store_commit_v0_17"

RECOVERY_ROUTED = "RECOVERY_ROUTED"
REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
V11_RENEWAL_REVIEW = "V11_RENEWAL_REVIEW"
V12_ESCALATION_REQUIRED = "V12_ESCALATION_REQUIRED"
V12_REROTATION_REQUIRED = "V12_REROTATION_REQUIRED"

TARGET_STAGES = {
    REVALIDATION_REQUIRED,
    V11_RENEWAL_REVIEW,
    V12_ESCALATION_REQUIRED,
    V12_REROTATION_REQUIRED,
}

NON_AUTHORITY = {
    "execution_granted": False,
    "host_access_granted": False,
    "automatic_renewal_granted": False,
    "rerotation_granted": False,
    "memory_overwrite_granted": False,
}

BOUNDARY = {
    "terminal_v16_suspension_required": True,
    "exact_v15_session_required": True,
    "exact_v13_materialization_required": True,
    "route_preserved": True,
    "old_session_closed": True,
    "old_session_resume_forbidden": True,
    "new_lineage_required": True,
    "new_session_required": True,
    "renewal_policy_rechecked": True,
    "router_not_revalidation": True,
    "router_not_renewal": True,
    "router_not_rerotation": True,
    "router_not_execution": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def handoff_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "suspension_recovery_handoff_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "suspension_recovery_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
