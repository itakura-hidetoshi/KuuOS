from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_transactional_effect_reconciliation_v0_24"
CONNECTOR_CONTRACT_VERSION = "kuuos_transactional_connector_contract_v0_24"
INTENT_VERSION = "kuuos_transaction_intent_v0_24"
STATE_VERSION = "kuuos_transaction_state_v0_24"
EVENT_VERSION = "kuuos_transaction_event_v0_24"
RECONCILIATION_VERSION = "kuuos_world_effect_reconciliation_receipt_v0_24"
COMPENSATION_REQUEST_VERSION = "kuuos_compensation_plan_request_v0_24"
DECISION_VERSION = "kuuos_transaction_decision_v0_24"
FINAL_RECEIPT_VERSION = "kuuos_transaction_final_receipt_v0_24"
APPLY_RESULT_VERSION = "kuuos_transaction_apply_result_v0_24"
STORE_VERSION = "kuuos_transaction_store_v0_24"

PHASES = (
    "prepared",
    "effect_bound",
    "observed",
    "reconciled",
    "verified",
    "decided",
    "committed",
)

RECONCILIATION_VERDICTS = frozenset(
    {
        "EFFECT_CONFIRMED",
        "EFFECT_PARTIAL",
        "EFFECT_NOT_OBSERVED",
        "EFFECT_CONFLICTED",
        "EXTERNAL_STATE_CHANGED",
        "COMPENSATION_REQUIRED",
    }
)

TRANSACTION_ROUTES = frozenset(
    {
        "PENDING",
        "EFFECT_CONFIRMED",
        "COMPENSATION_PROPOSED",
        "HANDOVER_REQUIRED",
        "REOBSERVATION_REQUIRED",
        "NO_EFFECT_RECORDED",
    }
)

COMPENSATION_MODES = frozenset(
    {"explicit_operation", "manual_handover", "noncompensable"}
)

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_rewrite_authority": False,
    "grants_plan_activation_authority": False,
    "grants_wakeup_authority": False,
    "grants_clinical_authority": False,
    "grants_legal_authority": False,
    "grants_institutional_authority": False,
    "grants_theorem_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "lower_actos_authority_is_canonical": True,
    "lower_host_receipt_is_canonical": True,
    "prepare_precedes_effect_binding": True,
    "exact_operation_and_input_binding_required": True,
    "exact_capability_lease_binding_required": True,
    "idempotency_key_required": True,
    "one_transaction_binds_one_lower_invocation": True,
    "tool_response_success_is_not_world_confirmation": True,
    "independent_world_evidence_required": True,
    "observation_is_not_verification": True,
    "verification_is_not_truth": True,
    "compensation_is_separate_authorized_transaction": True,
    "automatic_compensation_is_forbidden": True,
    "automatic_rollback_is_forbidden": True,
    "hidden_connector_call_is_forbidden": True,
    "connector_contract_is_read_only": True,
    "transaction_history_is_append_only": True,
    "duplicate_event_is_idempotent": True,
    "stale_state_is_rejected": True,
    "noncompensability_must_be_explicit": True,
    "wake_up_does_not_grant_authority": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def connector_contract_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "connector_contract_digest")


def intent_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_intent_digest")


def state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_state_digest")


def event_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_event_digest")


def reconciliation_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "reconciliation_receipt_digest")


def compensation_request_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "compensation_request_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_decision_digest")


def final_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_final_receipt_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_apply_result_digest")


def store_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "transaction_store_digest")


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


def finite_number(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name}_finite_number_required")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_finite_number_required") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_finite_number_required")
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


def seal(packet: dict[str, Any], field: str, supplied: Any = None) -> dict[str, Any]:
    packet[field] = ""
    expected = sha({key: value for key, value in packet.items() if key != field})
    packet[field] = expected
    if supplied not in (None, "", expected):
        raise ValueError(f"{field}_invalid")
    return packet


__all__ = [
    "APPLY_RESULT_VERSION",
    "COMPENSATION_MODES",
    "COMPENSATION_REQUEST_VERSION",
    "CONNECTOR_CONTRACT_VERSION",
    "DECISION_VERSION",
    "EVENT_VERSION",
    "FINAL_RECEIPT_VERSION",
    "INTENT_VERSION",
    "NON_AUTHORITY_FLAGS",
    "PHASES",
    "RECONCILIATION_VERDICTS",
    "RECONCILIATION_VERSION",
    "REQUIRED_BOUNDARY",
    "STATE_VERSION",
    "STORE_VERSION",
    "TRANSACTION_ROUTES",
    "VERSION",
    "apply_result_digest",
    "compensation_request_digest",
    "connector_contract_digest",
    "copy_boundary",
    "copy_non_authority",
    "decision_digest",
    "event_digest",
    "final_receipt_digest",
    "finite_number",
    "intent_digest",
    "reconciliation_digest",
    "require_bool",
    "require_int",
    "require_string",
    "seal",
    "state_digest",
    "store_digest",
    "unique_strings",
    "without",
]
