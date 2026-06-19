from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_adaptive_agent_reference_architecture_v1_0"
STATE_VERSION = "kuuos_adaptive_control_state_v1_0"
EVENT_VERSION = "kuuos_adaptive_event_v1_0"

PLANES = (
    "DELIBERATION",
    "EXECUTION",
    "LEARNING",
    "AUTHORITY",
    "ASSURANCE",
    "RECOVERY",
)

TASK_STAGES = (
    "BELIEF",
    "DECISION",
    "PLAN",
    "ACT",
    "OBSERVE",
    "VERIFY",
    "LEARN",
    "TERMINAL",
)

CONTROL_MODES = (
    "IDLE",
    "ACTIVE",
    "SUSPENDED",
    "RECOVERING",
    "TERMINATED",
)

AUTHORITY_MODES = (
    "UNBOUND",
    "BOUND",
    "LEASED",
    "RENEWAL_REVIEW",
    "ESCALATION",
    "REROTATION",
)

MODULE_STATUSES = (
    "IDLE",
    "RUNNING",
    "SUCCEEDED",
    "FAILED",
    "BLOCKED",
    "SUSPENDED",
)

RECOVERY_DECISIONS = (
    "CONTINUE",
    "RETRY",
    "REVALIDATE",
    "REPLAN",
    "RENEW",
    "ESCALATE",
    "REROTATE",
    "REQUEST_HUMAN",
    "ABORT",
)

EVENT_KINDS = (
    "DECISION_COMMITTED",
    "PLAN_BOUND",
    "AUTHORITY_BOUND",
    "LEASE_ACTIVATED",
    "SESSION_BOOTSTRAPPED",
    "ACT_AUTHORIZED",
    "EFFECT_RECORDED",
    "OBSERVATION_COMMITTED",
    "VERIFICATION_PASSED",
    "VERIFICATION_FAILED",
    "LEARNING_COMMITTED",
    "LEASE_ANOMALY",
    "RECOVERY_ROUTED",
    "RECOVERY_COMPLETED",
    "ABORTED",
)

NON_AUTHORITY = {
    "planner_grants_execution": False,
    "monitor_grants_renewal": False,
    "router_performs_recovery": False,
    "evidence_grants_truth": False,
    "memory_overwrite_granted": False,
}

GLOBAL_BOUNDARY = {
    "behavior_and_configuration_adaptation_separated": True,
    "runtime_models_related_by_megamodel": True,
    "feedback_loop_behavior_explicit": True,
    "advanced_and_assurance_planes_separated": True,
    "recovery_algebra_finite": True,
    "terminal_session_never_reactivated": True,
    "observation_precedes_verification": True,
    "execution_requires_active_leased_session": True,
    "recovery_creates_fresh_lineage": True,
}

IMPLEMENTATION_REFINEMENT_MAP = {
    **{f"PlanOS_v0_{index}": "DELIBERATION" for index in range(1, 9)},
    **{f"PlanOS_v0_{index}": "AUTHORITY" for index in range(9, 15)},
    "PlanOS_v0_15": "EXECUTION",
    "PlanOS_v0_16": "ASSURANCE",
    "PlanOS_v0_17": "RECOVERY",
    "BeliefOS": "DELIBERATION",
    "DecisionOS": "DELIBERATION",
    "ActOS": "EXECUTION",
    "ObserveOS": "EXECUTION",
    "VerifyOS": "EXECUTION",
    "LearnOS": "LEARNING",
}

RECOVERY_CONTRACTS = {
    "CONTINUE": {
        "requires_suspension": False,
        "requires_authority_receipt": False,
        "creates_new_lineage": False,
        "requires_new_session": False,
        "terminal": False,
    },
    "RETRY": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "REVALIDATE": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "REPLAN": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "RENEW": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "ESCALATE": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "REROTATE": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "REQUEST_HUMAN": {
        "requires_suspension": True,
        "requires_authority_receipt": True,
        "creates_new_lineage": True,
        "requires_new_session": True,
        "terminal": False,
    },
    "ABORT": {
        "requires_suspension": False,
        "requires_authority_receipt": True,
        "creates_new_lineage": False,
        "requires_new_session": False,
        "terminal": True,
    },
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_global_boundary() -> dict[str, bool]:
    return deepcopy(GLOBAL_BOUNDARY)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "adaptive_control_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "adaptive_event_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
