from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_bounded_renewal_governance_v0_11"
STATE_VERSION = "kuuos_plan_os_bounded_renewal_state_v0_11"
RECEIPT_VERSION = "kuuos_plan_os_governed_renewal_receipt_v0_11"
STORE_COMMIT_VERSION = "kuuos_plan_os_bounded_renewal_store_commit_v0_11"

ACTIVE = "ACTIVE"
ESCALATION_REQUIRED = "ESCALATION_REQUIRED"

NON_AUTHORITY = {
    "execution_authority_granted": False,
    "host_license_granted": False,
    "approval_granted": False,
    "automatic_renewal_granted": False,
    "memory_overwrite_authority_granted": False,
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
}

BOUNDARY = {
    "v10_lease_state_required": True,
    "external_authority_receipt_required": True,
    "renewal_authority_identity_fixed": True,
    "renewal_count_bounded": True,
    "cumulative_use_extension_bounded": True,
    "cumulative_cost_extension_bounded": True,
    "absolute_expiry_horizon_bounded": True,
    "renewal_cooldown_enforced": True,
    "owner_epoch_scope_revalidated": True,
    "automatic_renewal_forbidden": True,
    "ceiling_requires_escalation_or_rotation": True,
    "renewal_wrapper_not_execution": True,
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
    return _digest_without(value, "bounded_renewal_state_digest")


def receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "governed_renewal_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "bounded_renewal_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
