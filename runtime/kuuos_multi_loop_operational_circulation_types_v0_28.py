from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_multi_loop_operational_circulation_kernel_v0_28"
CONTRACT_VERSION = "kuuos_multi_loop_network_contract_v0_28"
LOOP_VERSION = "kuuos_multi_loop_binding_v0_28"
EDGE_VERSION = "kuuos_multi_loop_edge_v0_28"
ASSESSMENT_VERSION = "kuuos_multi_loop_interference_assessment_v0_28"
REPAIR_VERSION = "kuuos_multi_loop_repair_proposal_v0_28"
CONTROL_VERSION = "kuuos_multi_loop_control_event_v0_28"
STATE_VERSION = "kuuos_multi_loop_network_state_v0_28"
EVENT_VERSION = "kuuos_multi_loop_network_event_v0_28"
APPLY_RESULT_VERSION = "kuuos_multi_loop_apply_result_v0_28"

LOOP_MODES = frozenset(
    {
        "ACTIVE",
        "PAUSED",
        "RENEWAL_REQUIRED",
        "TERMINATED",
        "HANDED_OVER",
    }
)

NETWORK_MODES = frozenset(
    {
        "ACTIVE",
        "DEGRADED",
        "PAUSED",
        "ARBITRATION_REQUIRED",
        "TERMINATED",
    }
)

EDGE_KINDS = frozenset(
    {
        "SHARED_RESOURCE",
        "EFFECT_CONFLICT",
        "EVIDENCE_DEPENDENCY",
        "CHECKPOINT_DEPENDENCY",
        "CONTROL_COLLISION",
    }
)

INTERFERENCE_CLASSES = frozenset(
    {
        "NONE",
        "RESOURCE_CONTENTION",
        "EFFECT_COLLISION",
        "DEPENDENCY_BLOCK",
        "WAIT_CYCLE",
        "CONTROL_COLLISION",
        "MIXED",
    }
)

SEVERITIES = frozenset({"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"})

REPAIR_ROUTES = frozenset(
    {
        "NO_ACTION",
        "HOLD",
        "SERIALIZE",
        "SPLIT_RESOURCE",
        "REQUEST_ARBITRATION",
        "HANDOVER",
        "TERMINATE_ONE",
    }
)

CONTROL_COMMANDS = frozenset(
    {
        "pause_network",
        "resume_network",
        "request_arbitration",
        "release_arbitration",
        "terminate_network",
    }
)

EVENT_KINDS = frozenset(
    {
        "loop_binding",
        "edge_binding",
        "assessment",
        "repair_proposal",
        "control",
    }
)

NON_AUTHORITY_FLAGS = {
    "pools_loop_authority": False,
    "transfers_license_between_loops": False,
    "creates_execution_permission": False,
    "creates_dispatch_permission": False,
    "creates_truth_status": False,
    "directly_pauses_loop": False,
    "directly_resumes_loop": False,
    "directly_terminates_loop": False,
    "rewrites_v027_state": False,
    "overwrites_memory_root": False,
}

REQUIRED_BOUNDARY = {
    "every_loop_retains_v027_boundary": True,
    "loop_authority_is_not_pooled": True,
    "licenses_are_not_transferable": True,
    "edge_set_is_finite": True,
    "resource_capacity_is_finite": True,
    "circulation_round_is_finite": True,
    "interference_assessment_is_advisory": True,
    "repair_proposal_is_nonexecuting": True,
    "network_control_does_not_mutate_loop": True,
    "verification_does_not_transfer_between_loops": True,
    "dependency_does_not_grant_authority": True,
    "checkpoint_precedes_handover": True,
    "duplicate_event_is_idempotent": True,
    "stale_state_is_rejected": True,
    "history_is_append_only": True,
    "audit_and_provenance_are_preserved": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def contract_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_contract_digest")


def loop_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_binding_digest")


def edge_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_edge_digest")


def assessment_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_assessment_digest")


def repair_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_repair_digest")


def control_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_control_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_event_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "multi_loop_apply_result_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_bool_required")
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


def string_map(value: Any, name: str, *, allow_empty: bool = False) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    result = {
        require_string(key, f"{name}_key"): require_string(item, f"{name}_{key}")
        for key, item in value.items()
    }
    if not allow_empty and not result:
        raise ValueError(f"{name}_nonempty_required")
    return dict(sorted(result.items()))


def nonnegative_int_map(
    value: Any, name: str, *, allow_empty: bool = False
) -> dict[str, int]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    result = {
        require_string(key, f"{name}_key"): require_nonnegative_int(
            item, f"{name}_{key}"
        )
        for key, item in value.items()
    }
    if not allow_empty and not result:
        raise ValueError(f"{name}_nonempty_required")
    return dict(sorted(result.items()))


def positive_int_map(value: Any, name: str) -> dict[str, int]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name}_mapping_required")
    result = {
        require_string(key, f"{name}_key"): require_positive_int(
            item, f"{name}_{key}"
        )
        for key, item in value.items()
    }
    if not result:
        raise ValueError(f"{name}_nonempty_required")
    return dict(sorted(result.items()))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


__all__ = [
    "APPLY_RESULT_VERSION",
    "ASSESSMENT_VERSION",
    "CONTRACT_VERSION",
    "CONTROL_COMMANDS",
    "CONTROL_VERSION",
    "EDGE_KINDS",
    "EDGE_VERSION",
    "EVENT_KINDS",
    "EVENT_VERSION",
    "INTERFERENCE_CLASSES",
    "LOOP_MODES",
    "LOOP_VERSION",
    "NETWORK_MODES",
    "NON_AUTHORITY_FLAGS",
    "REPAIR_ROUTES",
    "REPAIR_VERSION",
    "REQUIRED_BOUNDARY",
    "SEVERITIES",
    "STATE_VERSION",
    "VERSION",
    "apply_result_digest",
    "assessment_digest",
    "contract_digest",
    "control_digest",
    "copy_boundary",
    "copy_non_authority",
    "edge_digest",
    "event_digest",
    "loop_digest",
    "nonnegative_int_map",
    "positive_int_map",
    "repair_digest",
    "require_bool",
    "require_nonnegative_int",
    "require_positive_int",
    "require_string",
    "state_digest",
    "string_map",
    "unique_strings",
    "without",
]
