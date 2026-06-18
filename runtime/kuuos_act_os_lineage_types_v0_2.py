from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_act_os_replan_lineage_authority_envelope_v0_2"
HANDOFF_RECEIPT_VERSION = "kuuos_act_os_lineage_handoff_receipt_v0_2"
AUTHORIZATION_ENVELOPE_VERSION = "kuuos_act_os_lineage_bound_authorization_envelope_v0_2"
COMPLETION_RECEIPT_VERSION = "kuuos_act_os_lineage_completion_receipt_v0_2"
STORE_STATE_VERSION = "kuuos_act_os_lineage_store_state_v0_2"
STORE_COMMIT_VERSION = "kuuos_act_os_lineage_store_commit_v0_2"

STAGE_HANDOFF = "HANDOFF_ISSUED"
STAGE_COMPLETION = "COMPLETION_COMMITTED"
STAGES = frozenset({STAGE_HANDOFF, STAGE_COMPLETION})

NON_AUTHORITY_FLAGS = {
    "truth": False,
    "causal": False,
    "execution_by_handoff": False,
    "clinical": False,
    "legal": False,
    "institutional": False,
    "host_license": False,
    "memory_overwrite": False,
    "tool_widening": False,
    "shell_widening": False,
    "network_widening": False,
}

REQUIRED_BOUNDARY = {
    "plan_activation_not_execution": True,
    "exact_act_phase": True,
    "exact_effectful_step": True,
    "step_authorization_required": True,
    "human_approval_preserved": True,
    "host_license_required": True,
    "inner_authorization_unchanged": True,
    "license_not_widened": True,
    "replan_lineage_preserved": True,
    "qi_context_non_authority": True,
    "single_use_handoff": True,
    "observation_debt_preserved": True,
    "verification_debt_preserved": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def handoff_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "act_lineage_handoff_receipt_digest")


def authorization_envelope_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "authorization_envelope_digest")


def completion_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "act_lineage_completion_receipt_digest")


def store_state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "act_lineage_store_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "act_lineage_store_commit_digest")


def handoff_single_use_key(value: Mapping[str, Any]) -> str:
    return sha({
        "compiler": value.get("next_cycle_compiler_receipt_digest"),
        "step": value.get("selected_step_digest"),
    })


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
