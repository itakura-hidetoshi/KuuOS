from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_generational_replan_cycle_driver_v0_5"
RECEIPT_VERSION = "kuuos_plan_os_generational_cycle_receipt_v0_5"
STORE_STATE_VERSION = "kuuos_plan_os_generational_cycle_store_state_v0_5"
STORE_COMMIT_VERSION = "kuuos_plan_os_generational_cycle_store_commit_v0_5"

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
    "source_bind_receipt_required": True,
    "strict_replan_phase_order_required": True,
    "decision_selection_identity_preserved": True,
    "next_cycle_compiler_required": True,
    "exact_successor_cycle_required": True,
    "single_generation_consumption": True,
    "current_cycle_unchanged_during_replan": True,
    "past_plan_unchanged": True,
    "memory_overwrite_forbidden": True,
    "execution_owned_by_act_os": True,
    "replan_owned_by_plan_os": True,
    "selection_owned_by_decision_os": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def generational_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "generational_cycle_receipt_digest")


def store_state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "generational_cycle_store_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "generational_cycle_store_commit_digest")


def generation_key(value: Mapping[str, Any]) -> str:
    return sha({
        "source_plan": value.get("source_plan_state_digest"),
        "learn_input": value.get("planos_replan_input_digest"),
        "source_cycle": value.get("source_cycle_index"),
    })


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value
