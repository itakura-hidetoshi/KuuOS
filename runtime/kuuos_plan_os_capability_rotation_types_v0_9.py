from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_post_reentry_capability_rotation_v0_9"
STATE_VERSION = "kuuos_plan_os_capability_epoch_state_v0_9"
ROTATION_RECEIPT_VERSION = "kuuos_plan_os_capability_rotation_receipt_v0_9"
BINDING_VERSION = "kuuos_plan_os_capability_reissue_binding_v0_9"
STORE_COMMIT_VERSION = "kuuos_plan_os_capability_rotation_store_commit_v0_9"

HOST_LICENSE = "HOST_LICENSE"
HUMAN_APPROVAL = "HUMAN_APPROVAL"
STEP_AUTHORIZATION = "STEP_AUTHORIZATION"
OPERATION_AUTHORIZATION = "OPERATION_AUTHORIZATION"
CAPABILITY_KINDS = (
    HOST_LICENSE,
    HUMAN_APPROVAL,
    STEP_AUTHORIZATION,
    OPERATION_AUTHORIZATION,
)

ROTATED = "ROTATED"
BOUND = "BOUND"

NON_AUTHORITY = {
    "execution_authority_granted": False,
    "host_license_granted": False,
    "human_approval_granted": False,
    "step_authorization_granted": False,
    "operation_authorization_granted": False,
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
}

BOUNDARY = {
    "v08_ownership_continuity_required": True,
    "rotation_before_plan_stage_required": True,
    "capability_epoch_monotone": True,
    "all_previous_capabilities_revoked": True,
    "previous_owner_capabilities_forbidden_after_handover": True,
    "current_owner_required_for_reissue": True,
    "reissue_requires_lower_authority_receipt": True,
    "reissue_binding_not_capability": True,
    "old_epoch_reuse_forbidden": True,
    "single_use_capability_binding": True,
    "existing_actos_authority_unchanged": True,
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


def rotation_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_rotation_receipt_digest")


def binding_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_reissue_binding_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_epoch_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "capability_rotation_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
