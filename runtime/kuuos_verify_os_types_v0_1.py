from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import canonical_json, sha

VERSION = "kuuos_verify_os_evidence_bound_verification_v0_1"
STATE_VERSION = "kuuos_verify_os_state_v0_1"
EVENT_VERSION = "kuuos_verify_os_event_v0_1"
CRITERION_PACKET_VERSION = "kuuos_verify_os_criterion_packet_v0_1"
CHALLENGE_PACKET_VERSION = "kuuos_verify_os_challenge_packet_v0_1"
CORROBORATION_REPORT_VERSION = "kuuos_verify_os_corroboration_report_v0_1"
ADJUDICATION_RECEIPT_VERSION = "kuuos_verify_os_adjudication_receipt_v0_1"
VERIFY_PHASE_RECEIPT_VERSION = "kuuos_verify_os_phase_receipt_v0_1"
STORE_COMMIT_VERSION = "kuuos_verify_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_verify_os_apply_result_v0_1"

PHASES = ("bind", "criterion", "challenge", "corroborate", "adjudicate", "commit")
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}
ROUTES = frozenset(
    {
        "PENDING",
        "VERIFICATION_PASSED",
        "VERIFICATION_FAILED",
        "VERIFICATION_INDETERMINATE",
    }
)
ADJUDICATION_VERDICTS = frozenset({"PASSED", "FAILED", "INDETERMINATE"})
CRITERION_TYPES = frozenset({"invariant", "threshold", "exact", "consistency", "safety", "contract"})

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "execution_authority_granted": False,
    "final_commitment_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "theorem_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "committed_observe_state_required": True,
    "exact_source_binding_required": True,
    "exact_criterion_binding_required": True,
    "falsification_attempt_required": True,
    "counterevidence_preserved": True,
    "independent_assessment_required": True,
    "corroboration_required": True,
    "verification_is_not_truth": True,
    "causal_attribution_not_granted": True,
    "learning_required_after_verification": True,
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
    return digest_without(value, "verify_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "verify_event_digest")


def criterion_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "criterion_packet_digest")


def challenge_packet_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "challenge_packet_digest")


def corroboration_report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "corroboration_report_digest")


def adjudication_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "adjudication_receipt_digest")


def verify_phase_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "verify_phase_receipt_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "verify_store_commit_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "verify_apply_result_digest")


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
