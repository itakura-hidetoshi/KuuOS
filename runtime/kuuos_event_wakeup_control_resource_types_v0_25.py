from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_event_wakeup_control_resource_kernel_v0_25"
TRIGGER_VERSION = "kuuos_external_trigger_event_v0_25"
WAKEUP_VERSION = "kuuos_bounded_wakeup_proposal_v0_25"
CONTROL_COMMAND_VERSION = "kuuos_user_control_command_v0_25"
RESOURCE_ENVELOPE_VERSION = "kuuos_resource_model_envelope_v0_25"
RESOURCE_DECISION_VERSION = "kuuos_resource_admission_decision_v0_25"
STATE_VERSION = "kuuos_event_wakeup_control_resource_state_v0_25"
EVENT_VERSION = "kuuos_event_wakeup_control_resource_event_v0_25"
STATUS_VERSION = "kuuos_user_visible_status_snapshot_v0_25"
APPLY_RESULT_VERSION = "kuuos_event_wakeup_apply_result_v0_25"

TRIGGER_CLASSES = frozenset(
    {
        "clock_schedule",
        "queue_available",
        "lease_expiry",
        "dependency_completed",
        "resource_replenished",
        "webhook_connector_event",
        "user_command",
        "monitoring_condition",
    }
)

CONTROL_COMMANDS = frozenset(
    {
        "inspect",
        "explain",
        "pause",
        "resume",
        "cancel",
        "reprioritize",
        "revise_mission",
        "revise_constraint",
        "approve_permission",
        "increase_budget",
        "force_replan",
        "release_dead_letter",
        "handover",
    }
)

MUTATING_CONTROL_COMMANDS = CONTROL_COMMANDS - {"inspect", "explain"}

CONTROL_MODES = frozenset(
    {
        "ACTIVE",
        "PAUSED",
        "CANCELLED",
        "HANDOVER",
        "AWAITING_RENEWAL",
    }
)

RESOURCE_ROUTES = frozenset(
    {
        "ADMIT",
        "DEGRADE_MODEL",
        "RENEWAL_REQUIRED",
        "PAUSE_RESOURCE_EXHAUSTED",
        "REJECT_CONTROL_PAUSED",
        "REJECT_CONTROL_CANCELLED",
        "REJECT_HANDOVER",
    }
)

WAKEUP_ROUTES = frozenset(
    {
        "WAKEUP_PROPOSED",
        "WAKEUP_DEGRADED",
        "WAKEUP_BLOCKED_RENEWAL",
        "WAKEUP_BLOCKED_PAUSED",
        "WAKEUP_BLOCKED_CANCELLED",
        "WAKEUP_BLOCKED_HANDOVER",
    }
)

MODEL_TIERS = ("small", "standard", "advanced")

RESOURCE_FIELDS = (
    "tokens",
    "api_calls",
    "cost_microunits",
    "storage_bytes",
    "worker_millis",
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
    "grants_clinical_authority": False,
    "grants_legal_authority": False,
    "grants_institutional_authority": False,
    "grants_theorem_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "external_trigger_surface_required": True,
    "conversation_model_is_not_hidden_daemon": True,
    "every_wakeup_starts_new_bounded_cycle": True,
    "fresh_cycle_license_required": True,
    "wakeup_does_not_inherit_execution_authority": True,
    "queue_is_not_running": True,
    "running_is_not_verified": True,
    "foreground_user_control_remains_available": True,
    "user_control_path_is_independent": True,
    "inspect_and_explain_are_read_only": True,
    "pause_cancel_and_handover_preempt_wakeup": True,
    "permission_approval_does_not_execute": True,
    "budget_increase_requires_external_control_authority": True,
    "resource_envelopes_remain_finite": True,
    "resource_exhaustion_causes_pause_replan_or_renewal": True,
    "model_degradation_precedes_unlicensed_escalation": True,
    "resource_replenishment_does_not_auto_resume": True,
    "duplicate_trigger_is_idempotent": True,
    "stale_state_is_rejected": True,
    "event_history_is_append_only": True,
    "source_transaction_receipt_remains_canonical": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def trigger_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "trigger_event_digest")


def wakeup_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "wakeup_proposal_digest")


def control_command_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "control_command_digest")


def resource_envelope_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "resource_envelope_digest")


def resource_decision_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "resource_decision_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "event_wakeup_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "event_wakeup_event_digest")


def status_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "status_snapshot_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "event_wakeup_apply_result_digest")


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


def require_finite_nonnegative(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name}_finite_nonnegative_required")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_finite_nonnegative_required") from exc
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name}_finite_nonnegative_required")
    return result


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
    "CONTROL_COMMANDS",
    "CONTROL_COMMAND_VERSION",
    "CONTROL_MODES",
    "EVENT_VERSION",
    "MODEL_TIERS",
    "MUTATING_CONTROL_COMMANDS",
    "NON_AUTHORITY_FLAGS",
    "REQUIRED_BOUNDARY",
    "RESOURCE_DECISION_VERSION",
    "RESOURCE_ENVELOPE_VERSION",
    "RESOURCE_FIELDS",
    "RESOURCE_ROUTES",
    "STATE_VERSION",
    "STATUS_VERSION",
    "TRIGGER_CLASSES",
    "TRIGGER_VERSION",
    "VERSION",
    "WAKEUP_ROUTES",
    "WAKEUP_VERSION",
    "apply_result_digest",
    "control_command_digest",
    "copy_boundary",
    "copy_non_authority",
    "event_digest",
    "require_bool",
    "require_finite_nonnegative",
    "require_nonnegative_int",
    "require_positive_int",
    "require_string",
    "resource_decision_digest",
    "resource_envelope_digest",
    "state_digest",
    "status_digest",
    "trigger_digest",
    "unique_strings",
    "wakeup_digest",
    "without",
]
