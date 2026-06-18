from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_external_resume_handover_reentry_v0_7"
RECEIPT_VERSION = "kuuos_plan_os_external_reentry_receipt_v0_7"
DECISION_VERSION = "kuuos_plan_os_reentry_decision_v0_7"
EVENT_VERSION = "kuuos_plan_os_reentry_event_v0_7"
STATE_VERSION = "kuuos_plan_os_reentry_controller_state_v0_7"
STORE_COMMIT_VERSION = "kuuos_plan_os_reentry_store_commit_v0_7"

RESUME_HOLD = "RESUME_HOLD"
ACCEPT_HANDOVER = "ACCEPT_HANDOVER"
REENTRY_KINDS = {RESUME_HOLD, ACCEPT_HANDOVER}

REENTRY_AUTHORIZED = "REENTRY_AUTHORIZED"
REENTRY_REJECTED = "REENTRY_REJECTED"

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
    "explicit_external_receipt_required": True,
    "stopped_state_not_resumable": True,
    "hold_resume_requires_same_owner": True,
    "handover_requires_distinct_new_owner": True,
    "handover_requires_outgoing_delegation": True,
    "handover_requires_incoming_acceptance": True,
    "lineage_mission_policy_revalidation_required": True,
    "source_terminal_state_digest_binding_required": True,
    "single_use_receipt_required": True,
    "reentry_is_not_execution": True,
    "execution_owned_by_act_os": True,
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
    return _digest_without(value, "external_reentry_receipt_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "reentry_decision_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "reentry_event_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "reentry_controller_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "reentry_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
