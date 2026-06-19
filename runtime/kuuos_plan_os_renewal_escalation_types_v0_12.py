from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_renewal_ceiling_escalation_v0_12"
STATE_VERSION = "kuuos_plan_os_renewal_escalation_state_v0_12"
DECISION_VERSION = "kuuos_plan_os_renewal_escalation_decision_v0_12"
STORE_COMMIT_VERSION = "kuuos_plan_os_renewal_escalation_store_commit_v0_12"

OPEN = "OPEN"
RESOLVED_DENIED = "RESOLVED_DENIED"
HANDOVER_PENDING = "HANDOVER_PENDING"
REROTATION_AUTHORIZED = "REROTATION_AUTHORIZED"

DENY = "DENY"
HUMAN_HANDOVER = "HUMAN_HANDOVER"
RE_ROTATE = "RE_ROTATE"
ROUTES = (DENY, HUMAN_HANDOVER, RE_ROTATE)

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
    "v11_escalation_required": True,
    "single_resolution_required": True,
    "old_lease_lineage_closed": True,
    "deny_grants_no_continuation": True,
    "handover_requires_distinct_owner": True,
    "handover_requires_human_acceptance": True,
    "rerotation_requires_governance_authority": True,
    "rerotation_epoch_strictly_increases": True,
    "rerotation_requires_new_v09_chain": True,
    "decision_not_execution": True,
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
    return _digest_without(value, "renewal_escalation_state_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "renewal_escalation_decision_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "renewal_escalation_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
