from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_integrated_long_duration_operation_kernel_v0_27"
CONTRACT_VERSION = "kuuos_integrated_operation_contract_v0_27"
CYCLE_VERSION = "kuuos_integrated_operation_cycle_receipt_v0_27"
CONTROL_VERSION = "kuuos_integrated_operation_control_event_v0_27"
RECOVERY_VERSION = "kuuos_integrated_operation_recovery_receipt_v0_27"
STATE_VERSION = "kuuos_integrated_operation_state_v0_27"
EVENT_VERSION = "kuuos_integrated_operation_event_v0_27"
APPLY_RESULT_VERSION = "kuuos_integrated_operation_apply_result_v0_27"

CONTROL_COMMANDS = frozenset(
    {"pause", "resume", "terminate", "handover", "request_renewal", "renew"}
)

OPERATION_MODES = frozenset(
    {"ACTIVE", "PAUSED", "RENEWAL_REQUIRED", "TERMINATED", "HANDED_OVER"}
)

CYCLE_ROUTES = frozenset(
    {"CONTINUE", "PAUSE", "RENEWAL_REQUIRED", "TERMINATE", "HANDOVER"}
)

LOWER_COMPONENTS = (
    "mission_contract_v0_20",
    "observation_belief_v0_21",
    "semantic_planner_verifier_v0_22",
    "cognitive_memory_credit_v0_23",
    "transactional_effect_reconciliation_v0_24",
    "event_wakeup_control_resource_v0_25",
    "governed_change_management_v0_26",
)

NON_AUTHORITY_FLAGS = {
    "extends_existing_authority": False,
    "creates_effect_permission": False,
    "creates_truth_status": False,
    "creates_plan_activation": False,
    "overwrites_memory_root": False,
    "changes_world_without_receipt": False,
    "removes_user_control": False,
    "removes_resource_limits": False,
    "removes_cycle_limits": False,
    "removes_audit_history": False,
}

REQUIRED_BOUNDARY = {
    "all_lower_contracts_bound": True,
    "every_cycle_separately_bounded": True,
    "fresh_cycle_authorization_required": True,
    "repeatability_preserves_cycle_bounds": True,
    "repeatability_preserves_resource_bounds": True,
    "foreground_user_control_preserved": True,
    "termination_preserved": True,
    "handover_preserved": True,
    "renewal_explicit": True,
    "queued_work_not_running": True,
    "running_work_not_verified": True,
    "verification_not_truth": True,
    "learning_not_permission": True,
    "wake_event_not_permission": True,
    "change_review_not_deployment": True,
    "process_recovery_uses_replay": True,
    "host_recovery_requires_fresh_license": True,
    "duplicate_event_idempotent": True,
    "stale_state_rejected": True,
    "history_append_only": True,
    "checkpoint_before_handoff": True,
    "audit_and_provenance_preserved": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def contract_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_operation_contract_digest")


def cycle_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_cycle_receipt_digest")


def control_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_control_event_digest")


def recovery_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_recovery_receipt_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_operation_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_operation_event_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "integrated_operation_apply_result_digest")


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


def exact_string_map(value: Any, keys: Sequence[str], name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    expected = set(keys)
    if set(value) != expected:
        raise ValueError(f"{name}_keys_invalid")
    return {key: require_string(value.get(key), f"{name}_{key}") for key in keys}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


__all__ = [
    "APPLY_RESULT_VERSION",
    "CONTRACT_VERSION",
    "CONTROL_COMMANDS",
    "CONTROL_VERSION",
    "CYCLE_ROUTES",
    "CYCLE_VERSION",
    "EVENT_VERSION",
    "LOWER_COMPONENTS",
    "NON_AUTHORITY_FLAGS",
    "OPERATION_MODES",
    "RECOVERY_VERSION",
    "REQUIRED_BOUNDARY",
    "STATE_VERSION",
    "VERSION",
    "apply_result_digest",
    "contract_digest",
    "control_digest",
    "copy_boundary",
    "copy_non_authority",
    "cycle_digest",
    "event_digest",
    "exact_string_map",
    "recovery_digest",
    "require_bool",
    "require_nonnegative_int",
    "require_positive_int",
    "require_string",
    "state_digest",
    "unique_strings",
    "without",
]
