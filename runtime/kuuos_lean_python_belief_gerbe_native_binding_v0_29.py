"""BeliefOS: ORIGINAL v0.3 gerbe-to-Decision receipt with honest v0.1 gap.

The native full-cycle source uses BeliefOS gerbe v0.3, whereas the
v0.27 Lean condition adapter points at a different v0.1 structure
(FutureOnlyBeliefCommit). Exact source identity/digest and append-only
receipt history can be locally checked, but that DOES NOT give a v0.1
proof-field witness. Retain NO_DATA rather than fake an equivalent type.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    BLOCKED, NO_DATA, UnavailableSource, copied_state, field, natural,
    plain_list, string, require_match, fail,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    NativeOSBindingAudit,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_belief_os_gerbe_store_v0_3 import validate_gerbe_state
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION, receipt_digest,
)

OS_NAME = "BeliefOS"


def audit_native_belief_gerbe_source(
    belief_state: Any, belief_receipt: Any, decision_state: Any,
):
    """Check actual v0.3 source, not pretend to instantiate v0.1 Lean terms."""
    try:
        if any(item is None for item in (belief_state, belief_receipt, decision_state)):
            raise UnavailableSource("BeliefOS:source_state_or_receipt_missing")
        if any(type(item) is not dict for item in
               (belief_state, belief_receipt, decision_state)):
            raise UnavailableSource("BeliefOS:exact_plain_object_required", BLOCKED)
        belief = _finite_json(belief_state)
        receipt = _finite_json(belief_receipt)
        decision = copied_state("DecisionOS", decision_state)
        original = validate_gerbe_state(belief)
        if original:
            raise UnavailableSource("BeliefOS:original_gerbe_state_invalid", BLOCKED)
        version = string(receipt, "version", "BeliefReceipt")
        require_match(version, RECEIPT_VERSION, "BeliefOS:gerbe_receipt_version")
        receipt_id = string(receipt, "belief_gerbe_receipt_digest", "BeliefReceipt")
        require_match(receipt_id, receipt_digest(receipt),
                      "BeliefOS:gerbe_receipt_digest")
        require_match(string(belief, "latest_receipt_digest", "BeliefState"),
                      receipt_id, "BeliefOS:gerbe_latest_receipt")
        require_match(string(decision, "source_belief_receipt_digest", "DecisionOS"),
                      receipt_id, "BeliefOS:decision_belief_receipt_binding")
        require_match(string(belief, "lineage_id", "BeliefState"),
                      string(decision, "lineage_id", "DecisionOS"),
                      "BeliefOS:decision_lineage")
        require_match(string(receipt, "lineage_id", "BeliefReceipt"),
                      string(belief, "lineage_id", "BeliefState"),
                      "BeliefOS:receipt_lineage")
        history = plain_list(belief, "receipt_history", "BeliefState")
        if not history:
            raise UnavailableSource("BeliefOS:original_gerbe_history_not_observed")
        last = history[-1]
        require_match(string(last, "belief_gerbe_receipt_digest", "BeliefHistory"),
                      receipt_id, "BeliefOS:original_receipt_history")
        if natural(belief, "event_count", "BeliefState") != len(history):
            raise UnavailableSource("BeliefOS:gerbe_event_history_count_mismatch",
                                    BLOCKED)
        return NativeOSBindingAudit(
            os_name=OS_NAME, status=NO_DATA,
            source_digest=_fingerprint(belief),
            source_field_paths=(
                "BeliefOSState.receipt_history[-1].belief_gerbe_receipt_digest",
                "BeliefOSState.latest_receipt_digest",
                "BeliefOSReceipt.belief_gerbe_receipt_digest",
                "DecisionOS.source_belief_receipt_digest",
                "BeliefOSState.lineage_id",
                "DecisionOS.lineage_id",
            ),
            checked_witnesses=0,
            issues=(
                "BeliefGerbeV03_is_not_BeliefFutureOnlyCommitV01",
                "v01_FutureOnlyBeliefCommit_proof_fields_not_observed",
            ),
            original_state_validated=True,
            original_edge_validated=False,
            source_bound_python_conditions_checked=False,
        )
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (ValueError, TypeError, UnicodeError, OverflowError,
            KeyError, AttributeError, RecursionError) as exc:
        return fail(OS_NAME, "BeliefOS:gerbe_source_exception:" +
                    type(exc).__name__, status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_belief_gerbe_source")
