from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_learn_os_future_only_evidence_learning_v0_1"
STATE_VERSION = "kuuos_learn_os_state_v0_1"
EVENT_VERSION = "kuuos_learn_os_event_v0_1"
ABSTRACTION_PACKET_VERSION = "kuuos_learn_os_abstraction_packet_v0_1"
CHALLENGE_PACKET_VERSION = "kuuos_learn_os_challenge_packet_v0_1"
LEARNING_DELTA_VERSION = "kuuos_learn_os_learning_delta_v0_1"
MIDDLE_WAY_REPORT_VERSION = "kuuos_learn_os_middle_way_report_v0_1"
LEARN_PHASE_RECEIPT_VERSION = "kuuos_learn_os_phase_receipt_v0_1"
STORE_COMMIT_VERSION = "kuuos_learn_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_learn_os_apply_result_v0_1"

PHASES = ("bind", "abstract", "challenge", "delta", "middle_way_gate", "commit")
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}
ROUTES = frozenset(
    {
        "PENDING",
        "LEARNING_REINFORCEMENT_CANDIDATE",
        "LEARNING_REPAIR_CANDIDATE",
        "LEARNING_REOBSERVATION_CANDIDATE",
        "LEARNING_HOLD",
    }
)
LEARNING_KINDS = frozenset({"reinforcement", "repair", "reobservation", "hold"})
TARGET_SCOPES = frozenset(
    {
        "belief_candidate",
        "plan_assumption",
        "verification_criterion",
        "observation_policy",
        "execution_guard",
        "no_change",
    }
)

NON_AUTHORITY_FLAGS = {
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
}

REQUIRED_BOUNDARY = {
    "committed_verify_state_required": True,
    "exact_source_binding_required": True,
    "source_evidence_preserved": True,
    "counterevidence_preserved": True,
    "anti_overgeneralization_required": True,
    "future_only_learning_required": True,
    "memory_overwrite_forbidden": True,
    "current_cycle_mutation_forbidden": True,
    "past_record_mutation_forbidden": True,
    "activation_requires_replan": True,
    "qi_is_context_only": True,
    "two_truths_separation_required": True,
    "middle_way_gate_required": True,
    "append_only_history_required": True,
    "duplicate_event_idempotent": True,
    "lower_authority_preserved": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learn_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learn_event_digest")


def abstraction_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "abstraction_packet_digest")


def challenge_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "challenge_packet_digest")


def learning_delta_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learning_delta_digest")


def middle_way_report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "middle_way_report_digest")


def learn_phase_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learn_phase_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learn_store_commit_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "learn_apply_result_digest")


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]


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


def unit_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    result = float(value)
    if result < 0.0 or result > 1.0:
        raise ValueError(f"{name}_unit_interval_required")
    return result


def unique_strings(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name}_list_required")
    items = [require_string(item, name) for item in value]
    if not allow_empty and not items:
        raise ValueError(f"{name}_nonempty_required")
    if len(items) != len(set(items)):
        raise ValueError(f"{name}_duplicate")
    return items
