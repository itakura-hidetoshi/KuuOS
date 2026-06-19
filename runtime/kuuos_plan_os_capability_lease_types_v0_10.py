from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_scoped_capability_lease_supervisor_v0_10"
STATE_VERSION = "kuuos_plan_os_capability_lease_state_v0_10"
CONSUMPTION_VERSION = "kuuos_plan_os_capability_lease_consumption_v0_10"
RENEWAL_VERSION = "kuuos_plan_os_capability_lease_renewal_v0_10"
STORE_COMMIT_VERSION = "kuuos_plan_os_capability_lease_store_commit_v0_10"

ACTIVE = "ACTIVE"
PARTIALLY_EXHAUSTED = "PARTIALLY_EXHAUSTED"
EXHAUSTED = "EXHAUSTED"
EXPIRED = "EXPIRED"
RENEWED = "RENEWED"

NON_AUTHORITY = {
    "execution_authority_granted": False,
    "host_license_granted": False,
    "approval_granted": False,
    "operation_authority_granted": False,
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
}

BOUNDARY = {
    "v09_bound_capability_state_required": True,
    "owner_epoch_binding_required": True,
    "stage_operation_scope_binding_required": True,
    "use_budget_monotone": True,
    "cost_budget_monotone": True,
    "expiry_enforced": True,
    "exact_replay_idempotent": True,
    "renewal_requires_external_receipt": True,
    "renewal_preserves_owner_epoch_scope": True,
    "consumption_not_execution": True,
    "renewal_not_authority": True,
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
    return _digest_without(value, "capability_lease_consumption_digest")


def renewal_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_lease_renewal_digest")


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
