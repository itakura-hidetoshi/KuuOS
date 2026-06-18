from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_verify_os_replan_lineage_verification_envelope_v0_2"
HANDOFF_RECEIPT_VERSION = "kuuos_verify_os_lineage_handoff_receipt_v0_2"
COMPLETION_RECEIPT_VERSION = "kuuos_verify_os_lineage_completion_receipt_v0_2"
STORE_STATE_VERSION = "kuuos_verify_os_lineage_store_state_v0_2"
STORE_COMMIT_VERSION = "kuuos_verify_os_lineage_store_commit_v0_2"

STAGE_HANDOFF = "HANDOFF_ISSUED"
STAGE_COMPLETION = "VERIFICATION_COMMITTED"
STAGES = frozenset({STAGE_HANDOFF, STAGE_COMPLETION})

NON_AUTHORITY_FLAGS = {
    "absolute_truth": False,
    "causal": False,
    "execution": False,
    "final_commitment": False,
    "clinical": False,
    "legal": False,
    "institutional": False,
    "theorem": False,
    "memory_overwrite": False,
    "automatic_learning": False,
}

REQUIRED_BOUNDARY = {
    "committed_observation_required": True,
    "observe_lineage_preserved": True,
    "exact_verify_phase": True,
    "exact_cycle_preserved": True,
    "criterion_identity_preserved": True,
    "evidence_identity_preserved": True,
    "falsification_required": True,
    "counterevidence_preserved": True,
    "independent_assessment_required": True,
    "verification_not_truth": True,
    "causal_attribution_not_granted": True,
    "qi_context_non_authority": True,
    "learning_future_only": True,
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
    return _digest_without(value, "verify_lineage_handoff_receipt_digest")


def completion_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "verify_lineage_completion_receipt_digest")


def store_state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "verify_lineage_store_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "verify_lineage_store_commit_digest")


def handoff_single_use_key(value: Mapping[str, Any]) -> str:
    return sha(
        {
            "observe_completion": value.get(
                "observe_lineage_completion_receipt_digest"
            ),
            "criterion": value.get("verification_criterion_digest"),
        }
    )


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value
