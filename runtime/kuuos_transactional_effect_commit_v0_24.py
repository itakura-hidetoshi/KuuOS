from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    validate_transaction_final_receipt,
    validate_transaction_state,
)
from runtime.kuuos_transactional_effect_types_v0_24 import (
    FINAL_RECEIPT_VERSION,
    copy_boundary,
    copy_non_authority,
    final_receipt_digest,
    require_int,
)


def build_transaction_final_receipt_v0_24(
    *, state: Mapping[str, Any], committed_at_ms: int
) -> dict[str, Any]:
    """Seal a decided transaction without rebinding its prior decision to a later state.

    The decision is immutable evidence from the verified predecessor state.  The
    final receipt binds that decision digest to the current decided state, but
    deliberately does not reinterpret or regenerate the earlier decision.
    """
    errors = validate_transaction_state(state)
    if errors:
        raise ValueError("invalid_decided_transaction_state:" + ";".join(errors))
    if state.get("current_phase") != "decided":
        raise ValueError("final_receipt_requires_decided_state")
    decision = state.get("transaction_decision")
    if not isinstance(decision, Mapping):
        raise ValueError("transaction_decision_missing")
    if decision.get("transaction_decision_digest") != state.get(
        "transaction_decision_digest"
    ):
        raise ValueError("transaction_decision_digest_binding_mismatch")
    if decision.get("route") != state.get("route"):
        raise ValueError("transaction_decision_route_binding_mismatch")

    packet = {
        "version": FINAL_RECEIPT_VERSION,
        "transaction_id": state["transaction_id"],
        "transaction_intent_digest": state["transaction_intent_digest"],
        "source_transaction_state_digest": state["transaction_state_digest"],
        "connector_contract_digest": state["connector_contract_digest"],
        "final_act_state_digest": state["final_act_state_digest"],
        "host_receipt_digest": state["host_receipt_digest"],
        "host_invocation_digest": state["host_invocation_digest"],
        "observe_state_digest": state["observe_state_digest"],
        "reconciliation_receipt_digest": state[
            "reconciliation_receipt_digest"
        ],
        "verify_state_digest": state["verify_state_digest"],
        "transaction_decision_digest": state["transaction_decision_digest"],
        "route": state["route"],
        "effect_recorded": state["effect_recorded"],
        "reconciliation_verdict": state["reconciliation_verdict"],
        "verification_route": state["verification_route"],
        "compensation_request_digest": state["compensation_request_digest"],
        "append_only_commit": True,
        "lower_receipts_remain_canonical": True,
        "tool_response_success_not_world_confirmation": True,
        "world_reconciliation_not_truth": True,
        "decision_predecessor_digest_preserved": decision[
            "source_transaction_state_digest"
        ],
        "decision_reinterpreted_at_commit": False,
        "commit_grants_execution_authority": False,
        "commit_grants_final_authority": False,
        "memory_overwrite": False,
        "automatic_compensation": False,
        "automatic_rollback": False,
        "committed_at_ms": require_int(committed_at_ms, "committed_at_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "transaction_final_receipt_digest": "",
    }
    packet["transaction_final_receipt_digest"] = final_receipt_digest(packet)
    errors = validate_transaction_final_receipt(packet, state)
    if errors:
        raise ValueError(";".join(errors))
    return deepcopy(packet)


__all__ = ["build_transaction_final_receipt_v0_24"]
