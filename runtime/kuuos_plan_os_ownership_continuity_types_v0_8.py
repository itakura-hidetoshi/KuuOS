from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_reentry_ownership_continuity_v0_8"
STAGE_RECEIPT_VERSION = "kuuos_plan_os_ownership_stage_receipt_v0_8"
STATE_VERSION = "kuuos_plan_os_ownership_continuity_state_v0_8"
STORE_COMMIT_VERSION = "kuuos_plan_os_ownership_continuity_store_commit_v0_8"

PLAN = "PLAN"
ACT = "ACT"
OBSERVE = "OBSERVE"
VERIFY = "VERIFY"
LEARN = "LEARN"
STAGES = (PLAN, ACT, OBSERVE, VERIFY, LEARN)
ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"

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
    "v07_reentry_required": True,
    "exact_reentry_receipt_binding": True,
    "exact_reentry_decision_binding": True,
    "exact_reentry_event_binding": True,
    "current_owner_required_for_every_stage": True,
    "previous_owner_reuse_forbidden_after_handover": True,
    "stage_order_fixed": True,
    "underlying_receipt_digest_required": True,
    "single_use_stage_receipt": True,
    "ownership_wrapper_not_execution": True,
    "existing_os_authority_unchanged": True,
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


def stage_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "ownership_stage_receipt_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "ownership_continuity_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "ownership_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
