from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_scoped_capability_lease_v0_10"
STATE_VERSION = "kuuos_plan_os_capability_lease_state_v0_10"
CONSUMPTION_VERSION = "kuuos_plan_os_capability_lease_consumption_v0_10"
RENEWAL_VERSION = "kuuos_plan_os_capability_lease_renewal_v0_10"
STORE_COMMIT_VERSION = "kuuos_plan_os_capability_lease_store_commit_v0_10"

ACTIVE = "ACTIVE"
EXHAUSTED = "EXHAUSTED"
EXPIRED = "EXPIRED"

NON_AUTHORITY = {
    "execution_authority_granted": False,
    "host_license_granted": False,
    "approval_granted": False,
    "memory_overwrite_authority_granted": False,
    "automatic_renewal_granted": False,
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
}

BOUNDARY = {
    "v09_bound_state_required": True,
    "current_owner_required": True,
    "current_epoch_required": True,
    "stage_scope_required": True,
    "operation_scope_required": True,
    "exact_scope_digest_required": True,
    "usage_budget_monotone": True,
    "cost_budget_monotone": True,
    "time_window_enforced": True,
    "single_use_consumption_receipt": True,
    "automatic_renewal_forbidden": True,
    "external_renewal_receipt_required": True,
    "renewal_revalidates_owner_epoch_scope": True,
    "lease_not_execution": True,
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


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_lease_state_digest")


def consumption_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "lease_consumption_receipt_digest")


def renewal_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "lease_renewal_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_lease_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
