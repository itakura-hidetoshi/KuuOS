from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import canonical_json, sha

VERSION = "kuuos_plan_os_next_cycle_basis_compiler_adapter_v0_3"
ACTIVATION_RECEIPT_VERSION = "kuuos_plan_os_next_cycle_activation_receipt_v0_3"
MATERIALIZATION_PACKET_VERSION = "kuuos_plan_os_step_materialization_packet_v0_3"
COMPILER_RECEIPT_VERSION = "kuuos_plan_os_next_cycle_compiler_receipt_v0_3"
STORE_STATE_VERSION = "kuuos_plan_os_next_cycle_adapter_store_state_v0_3"
STORE_COMMIT_VERSION = "kuuos_plan_os_next_cycle_adapter_store_commit_v0_3"

ROUTE_PROJECTION = {
    "NEXT_PLAN_CANDIDATE": "PLAN_CANDIDATE",
    "REPAIR_PLAN_CANDIDATE": "REPAIR_PLAN",
    "REOBSERVATION_PLAN_CANDIDATE": "OBSERVATION_PLAN",
    "REROUTE_PLAN_CANDIDATE": "HANDOVER_PLAN",
    "TERMINATION_PLAN_CANDIDATE": "HANDOVER_PLAN",
    "HOLD": "HOLD",
}

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "execution_authority_granted": False,
    "final_commitment_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
    "theorem_authority_granted": False,
    "host_license_granted": False,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def next_plan_activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "next_plan_activation_receipt_digest")


def materialization_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "materialization_packet_digest")


def next_cycle_compiler_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "next_cycle_compiler_receipt_digest")


def adapter_store_state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "adapter_store_state_digest")


def adapter_store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "adapter_store_commit_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name}_bool_required")
    return value


def unique_strings(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name}_list_required")
    items = [require_string(item, name) for item in value]
    if not allow_empty and not items:
        raise ValueError(f"{name}_nonempty_required")
    if len(items) != len(set(items)):
        raise ValueError(f"{name}_duplicate")
    return items


def ordered_digest(value: Any) -> str:
    return sha(value)
