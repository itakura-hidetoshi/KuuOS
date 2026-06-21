from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_governed_self_modification_gate_v0_26"
PROPOSAL_VERSION = "kuuos_self_modification_proposal_v0_26"
EVIDENCE_VERSION = "kuuos_self_modification_stage_evidence_v0_26"
APPROVAL_VERSION = "kuuos_self_modification_external_approval_v0_26"
DECISION_VERSION = "kuuos_self_modification_decision_v0_26"
DEPLOYMENT_VERSION = "kuuos_limited_deployment_authorization_v0_26"
ROLLBACK_VERSION = "kuuos_self_modification_rollback_receipt_v0_26"
STATE_VERSION = "kuuos_self_modification_state_v0_26"
EVENT_VERSION = "kuuos_self_modification_event_v0_26"
APPLY_RESULT_VERSION = "kuuos_self_modification_apply_result_v0_26"

STAGES = (
    "proposal",
    "static_analysis",
    "sandbox",
    "regression",
    "formal_property",
    "canary",
    "approval",
    "decision",
    "limited_deployment",
    "rollback_or_close",
)

EVIDENCE_STAGES = frozenset(
    {"static_analysis", "sandbox", "regression", "formal_property", "canary"}
)

DECISION_ROUTES = frozenset(
    {
        "PENDING",
        "REJECTED_PERMANENT_FORBIDDEN_ACTION",
        "REJECTED_VALIDATION_FAILURE",
        "EXTERNAL_APPROVAL_REQUIRED",
        "LIMITED_DEPLOYMENT_AUTHORIZED",
        "ROLLBACK_REQUIRED",
        "ROLLED_BACK",
        "DEPLOYMENT_CLOSED_SUCCESS",
    }
)

PERMANENT_FORBIDDEN_ACTIONS = frozenset(
    {
        "widen_own_authority",
        "delete_hard_gate",
        "disable_audit",
        "erase_provenance",
        "remove_rollback",
        "grant_unrestricted_shell",
        "grant_unrestricted_network",
        "redefine_success_to_hide_failure",
    }
)

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_plan_activation_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_rewrite_authority": False,
    "grants_unbounded_wakeup_authority": False,
    "grants_budget_self_increase_authority": False,
    "grants_model_tier_self_escalation_authority": False,
    "grants_self_modification_authority": False,
    "grants_production_deployment_authority": False,
    "grants_rollback_suppression_authority": False,
    "grants_clinical_authority": False,
    "grants_legal_authority": False,
    "grants_institutional_authority": False,
    "grants_theorem_authority": False,
}

REQUIRED_BOUNDARY = {
    "proposal_does_not_modify_running_system": True,
    "static_analysis_precedes_sandbox": True,
    "sandbox_precedes_regression": True,
    "regression_precedes_formal_property_checks": True,
    "formal_checks_precede_canary": True,
    "canary_precedes_limited_deployment": True,
    "external_approval_required_when_policy_demands": True,
    "authority_widening_is_permanently_forbidden": True,
    "hard_gate_deletion_is_permanently_forbidden": True,
    "audit_disabling_is_permanently_forbidden": True,
    "provenance_erasure_is_permanently_forbidden": True,
    "rollback_removal_is_permanently_forbidden": True,
    "unrestricted_shell_and_network_are_permanently_forbidden": True,
    "success_redefinition_to_hide_failure_is_permanently_forbidden": True,
    "limited_deployment_requires_separate_actos_authorization": True,
    "rollback_artifact_is_immutable": True,
    "rollback_window_is_finite_and_nonzero": True,
    "deployment_scope_is_finite": True,
    "canary_success_is_not_permanent_truth": True,
    "self_modification_learning_is_not_self_license": True,
    "user_control_remains_available": True,
    "duplicate_event_is_idempotent": True,
    "stale_state_is_rejected": True,
    "history_is_append_only": True,
    "source_v025_state_remains_canonical": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def proposal_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "self_modification_proposal_digest")


def evidence_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "stage_evidence_digest")


def approval_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "external_approval_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "self_modification_decision_digest")


def deployment_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "limited_deployment_authorization_digest")


def rollback_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "rollback_receipt_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "self_modification_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "self_modification_event_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "self_modification_apply_result_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def require_positive_int(value: Any, name: str) -> int:
    result = require_nonnegative_int(value, name)
    if result < 1:
        raise ValueError(f"{name}_positive_int_required")
    return result


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_bool_required")
    return value


def unique_strings(
    values: Any, name: str, *, allow_empty: bool = False
) -> list[str]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{name}_list_required")
    result = [require_string(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_nonempty_required")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


__all__ = [
    "APPLY_RESULT_VERSION",
    "APPROVAL_VERSION",
    "DECISION_ROUTES",
    "DECISION_VERSION",
    "DEPLOYMENT_VERSION",
    "EVIDENCE_STAGES",
    "EVIDENCE_VERSION",
    "EVENT_VERSION",
    "NON_AUTHORITY_FLAGS",
    "PERMANENT_FORBIDDEN_ACTIONS",
    "PROPOSAL_VERSION",
    "REQUIRED_BOUNDARY",
    "ROLLBACK_VERSION",
    "STAGES",
    "STATE_VERSION",
    "VERSION",
    "apply_result_digest",
    "approval_digest",
    "copy_boundary",
    "copy_non_authority",
    "decision_digest",
    "deployment_digest",
    "event_digest",
    "evidence_digest",
    "proposal_digest",
    "require_bool",
    "require_nonnegative_int",
    "require_positive_int",
    "require_string",
    "rollback_digest",
    "state_digest",
    "unique_strings",
    "without",
]
