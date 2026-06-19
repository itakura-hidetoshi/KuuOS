from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_rerotation_materialization_v0_13"
RECEIPT_VERSION = "kuuos_plan_os_rerotation_materialization_receipt_v0_13"
STORE_COMMIT_VERSION = "kuuos_plan_os_rerotation_materialization_store_commit_v0_13"

MATERIALIZED = "MATERIALIZED"

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
    "v12_rerotation_authorization_required": True,
    "exact_v12_seed_binding": True,
    "old_epoch_capabilities_revoked": True,
    "old_capability_digest_reuse_forbidden": True,
    "fresh_lower_authority_receipts_required": True,
    "fresh_v09_capability_state_required": True,
    "fresh_v10_lease_state_required": True,
    "fresh_v11_renewal_state_required": True,
    "old_lease_history_not_carried_forward": True,
    "old_renewal_history_not_carried_forward": True,
    "single_materialization": True,
    "materialization_not_execution": True,
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


def receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "rerotation_materialization_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "rerotation_materialization_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
