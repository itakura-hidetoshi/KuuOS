from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import canonical_json, sha

VERSION = "kuuos_observe_os_effect_grounded_observation_v0_1"
STATE_VERSION = "kuuos_observe_os_state_v0_1"
EVENT_VERSION = "kuuos_observe_os_event_v0_1"
COMPARISON_RECEIPT_VERSION = "kuuos_observe_os_comparison_receipt_v0_1"
OBSERVE_PHASE_RECEIPT_VERSION = "kuuos_observe_os_phase_receipt_v0_1"
STORE_COMMIT_VERSION = "kuuos_observe_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_observe_os_apply_result_v0_1"

PHASES = ("bind", "scope", "collect", "trace", "assess", "compare", "commit")
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}
ROUTES = frozenset(
    {
        "PENDING",
        "OBSERVATION_MATCHED",
        "OBSERVATION_DIVERGENT",
        "OBSERVATION_INCONCLUSIVE",
        "OBSERVATION_CONFLICTED",
    }
)
COMPARISON_VERDICTS = frozenset({"MATCHED", "DIVERGENT", "INCONCLUSIVE", "CONFLICTED"})
SOURCE_KINDS = frozenset({"sensor", "human", "system", "document", "external"})

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "verification_authority_granted": False,
    "execution_authority_granted": False,
    "final_commitment_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "theorem_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "source_effect_receipt_required": True,
    "source_act_state_committed": True,
    "exact_effect_binding_required": True,
    "observation_scope_required": True,
    "raw_evidence_digest_required": True,
    "provenance_chain_required": True,
    "collector_identity_required": True,
    "time_window_required": True,
    "quality_assessment_non_authoritative": True,
    "comparison_is_not_verification": True,
    "verification_debt_preserved": True,
    "append_only_history_required": True,
    "duplicate_event_idempotent": True,
    "lower_authority_preserved": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = dict(value)
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "observe_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "observe_event_digest")


def comparison_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "comparison_receipt_digest")


def observe_phase_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "observe_phase_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "observe_store_commit_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "observe_apply_result_digest")


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
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ValueError(f"{name}_unit_interval_required")
    return number


def unique_strings(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name}_list_required")
    items = [require_string(item, name) for item in value]
    if not allow_empty and not items:
        raise ValueError(f"{name}_nonempty_required")
    if len(items) != len(set(items)):
        raise ValueError(f"{name}_duplicate")
    return items
