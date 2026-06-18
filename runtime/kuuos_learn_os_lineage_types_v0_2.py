from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_learn_os_replan_lineage_future_only_learning_envelope_v0_2"
HANDOFF_RECEIPT_VERSION = "kuuos_learn_os_lineage_handoff_receipt_v0_2"
COMPLETION_RECEIPT_VERSION = "kuuos_learn_os_lineage_completion_receipt_v0_2"
STORE_STATE_VERSION = "kuuos_learn_os_lineage_store_state_v0_2"
STORE_COMMIT_VERSION = "kuuos_learn_os_lineage_store_commit_v0_2"

STAGE_HANDOFF = "HANDOFF_ISSUED"
STAGE_COMPLETION = "LEARNING_COMMITTED"
STAGES = frozenset({STAGE_HANDOFF, STAGE_COMPLETION})

PLANOS_CANDIDATE_TYPES_BY_LEARNING_ROUTE = {
    "LEARNING_REINFORCEMENT_CANDIDATE": ("continue", "strengthen", "slow_down", "hold"),
    "LEARNING_REPAIR_CANDIDATE": ("repair", "slow_down", "reroute", "hold"),
    "LEARNING_REOBSERVATION_CANDIDATE": ("reobserve", "hold"),
    "LEARNING_HOLD": ("hold", "reobserve"),
}

NON_AUTHORITY_FLAGS = {
    "truth": False,
    "causal": False,
    "execution": False,
    "final_commitment": False,
    "memory_overwrite": False,
    "self_modification": False,
    "replan_activation": False,
    "plan_activation": False,
    "host_license": False,
}

REQUIRED_BOUNDARY = {
    "committed_verification_required": True,
    "verify_lineage_preserved": True,
    "exact_learn_phase": True,
    "exact_cycle_preserved": True,
    "verification_evidence_preserved": True,
    "criterion_identity_preserved": True,
    "counterevidence_preserved": True,
    "anti_overgeneralization_required": True,
    "middle_way_gate_required": True,
    "qi_context_non_authority": True,
    "future_only_delta": True,
    "current_cycle_unchanged": True,
    "past_records_unchanged": True,
    "active_now_forbidden": True,
    "activation_requires_planos_replan": True,
    "replan_owned_by_planos": True,
    "selection_owned_by_decisionos": True,
    "execution_owned_by_actos": True,
    "single_use_handoff": True,
    "append_only_history": True,
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
    return _digest_without(value, "learn_lineage_handoff_receipt_digest")


def completion_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "learn_lineage_completion_receipt_digest")


def store_state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "learn_lineage_store_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "learn_lineage_store_commit_digest")


def handoff_single_use_key(value: Mapping[str, Any]) -> str:
    return sha({
        "verify_completion": value.get("verify_lineage_completion_receipt_digest"),
        "verify_state": value.get("committed_verify_state_digest"),
    })


def planos_replan_input_digest(value: Mapping[str, Any]) -> str:
    return sha({
        "learn_state": value.get("committed_learn_state_digest"),
        "learning_delta": value.get("learning_delta_digest"),
        "middle_way": value.get("middle_way_report_digest"),
        "learning_route": value.get("learning_route"),
        "verify_completion": value.get("verify_lineage_completion_receipt_digest"),
        "qi_condition": value.get("qi_condition_packet_digest"),
    })


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value
