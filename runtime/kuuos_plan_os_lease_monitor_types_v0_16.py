from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

TICK_VERSION = "kuuos_plan_os_lease_monitor_tick_v0_16"
STORE_COMMIT_VERSION = "kuuos_plan_os_lease_monitor_store_commit_v0_16"

SESSION_HEALTHY = "SESSION_HEALTHY"
SESSION_SUSPENDED = "SESSION_SUSPENDED"

CONTINUE = "CONTINUE"
REVALIDATE = "REVALIDATE"
RENEW_OR_ESCALATE = "RENEW_OR_ESCALATE"
REROTATE_REQUIRED = "REROTATE_REQUIRED"

EXPIRED = "EXPIRED"
USE_BUDGET_EMPTY = "USE_BUDGET_EMPTY"
COST_BUDGET_EMPTY = "COST_BUDGET_EMPTY"
OWNER_MISMATCH = "OWNER_MISMATCH"
EPOCH_MISMATCH = "EPOCH_MISMATCH"
SCOPE_MISMATCH = "SCOPE_MISMATCH"
LEASE_WINDOW_MISMATCH = "LEASE_WINDOW_MISMATCH"
USE_BUDGET_INCREASE = "USE_BUDGET_INCREASE"
COST_BUDGET_INCREASE = "COST_BUDGET_INCREASE"
OBSERVATION_TIME_MISMATCH = "OBSERVATION_TIME_MISMATCH"

SUSPENSION_REASONS = {
    EXPIRED,
    USE_BUDGET_EMPTY,
    COST_BUDGET_EMPTY,
    OWNER_MISMATCH,
    EPOCH_MISMATCH,
    SCOPE_MISMATCH,
    LEASE_WINDOW_MISMATCH,
    USE_BUDGET_INCREASE,
    COST_BUDGET_INCREASE,
    OBSERVATION_TIME_MISMATCH,
}

NON_AUTHORITY = {
    "execution_granted": False,
    "host_access_granted": False,
    "automatic_renewal_granted": False,
    "memory_overwrite_granted": False,
}

BOUNDARY = {
    "active_v15_session_required": True,
    "all_lease_observations_required": True,
    "owner_epoch_scope_revalidated": True,
    "expiry_and_budget_revalidated": True,
    "budget_increase_forbidden": True,
    "any_anomaly_suspends_session": True,
    "suspension_terminal_for_session": True,
    "monitor_not_execution": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def tick_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "lease_monitor_tick_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "lease_monitor_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
