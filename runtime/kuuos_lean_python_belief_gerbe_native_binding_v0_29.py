"""BeliefOS: original v0.3 gerbe Lean data, with v0.1 type gap retained.

The canonical formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean
already proves source-bound GerbeBeliefBoundary consequences.
Original v0.3 Python coherent receipt stores corresponding booleans.
Validate those original fields *directly*, then retain the independent
unproved semantic bridge to v0.1 FutureOnlyBeliefCommit as NO_DATA.

A PASS from audit_native_gerbe_v03_theorem_conditions is ONLY a scoped
native Python check of v0.3 data, NOT a proof term, global refinement,
an external issuer attestation, or authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_decision_mediator_source_v0_29 import (
    BLOCKED, NO_DATA, UnavailableSource, copied_state, field, natural,
    plain_list, string, truth, require_match, fail,
)
from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    NativeOSBindingAudit, PASS,
)
from runtime.kuuos_lean_python_os_path_composition_v0_6 import (
    _finite_json, _fingerprint,
)
from runtime.kuuos_belief_os_gerbe_store_v0_3 import validate_gerbe_state
from runtime.kuuos_belief_os_gerbe_types_v0_3 import (
    RECEIPT_VERSION, receipt_digest,
)

OS_NAME = "BeliefOS"
FORMAL_V03 = "formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean"
FORMAL_V01 = "formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean"
V03_THEOREMS = (
    "gerbeBelief_preserves_locality",
    "gerbeBelief_preserves_plurality",
    "gerbeBelief_preserves_two_truths",
    "gerbeBelief_is_non_reified",
    "gerbeBelief_does_not_search_paths",
    "gerbeBelief_does_not_select_global_winner",
    "gerbeBelief_does_not_globally_trivialize",
)


def _validated_original_v03(
    belief_state: Any, belief_receipt: Any, decision_state: Any,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if any(x is None for x in (belief_state, belief_receipt, decision_state)):
        raise UnavailableSource("BeliefOS:original_state_or_receipt_missing")
    if any(type(x) is not dict for x in
           (belief_state, belief_receipt, decision_state)):
        raise UnavailableSource("BeliefOS:exact_plain_object_required", BLOCKED)
    belief = _finite_json(belief_state)
    receipt = _finite_json(belief_receipt)
    decision = copied_state("DecisionOS", decision_state)
    original = validate_gerbe_state(belief)
    if original:
        raise UnavailableSource("BeliefOS:original_v03_state_invalid", BLOCKED)
    require_match(string(receipt, "version", "BeliefReceipt"),
                  RECEIPT_VERSION, "BeliefOS:receipt_version")
    rid = string(receipt, "belief_gerbe_receipt_digest", "BeliefReceipt")
    require_match(rid, receipt_digest(receipt), "BeliefOS:receipt_digest")
    require_match(string(belief, "latest_receipt_digest", "BeliefState"),
                  rid, "BeliefOS:latest_receipt_binding")
    require_match(string(decision, "source_belief_receipt_digest", "DecisionOS"),
                  rid, "BeliefOS:decision_source_receipt")
    require_match(string(belief, "lineage_id", "BeliefState"),
                  string(decision, "lineage_id", "DecisionOS"),
                  "BeliefOS:source_decision_lineage")
    require_match(string(receipt, "lineage_id", "BeliefReceipt"),
                  string(belief, "lineage_id", "BeliefState"),
                  "BeliefOS:source_receipt_lineage")
    history = plain_list(belief, "receipt_history", "BeliefState")
    if not history:
        raise UnavailableSource("BeliefOS:receipt_history_unobserved")
    require_match(string(history[-1], "belief_gerbe_receipt_digest",
                         "BeliefState.receipt_history"),
                  rid, "BeliefOS:last_observed_receipt")
    if natural(belief, "event_count", "BeliefState") != len(history):
        raise UnavailableSource("BeliefOS:history_commit_count_inconsistent",
                                BLOCKED)
    require_match(
        string(history[-1], "surface_holonomy_chain_digest",
               "BeliefState.receipt_history"),
        string(belief, "surface_holonomy_chain_digest", "BeliefState"),
        "BeliefOS:surface_holonomy_history_binding",
    )
    return belief, receipt, decision


def audit_native_gerbe_v03_theorem_conditions(
    belief_state: Any, belief_receipt: Any, decision_state: Any,
) -> NativeOSBindingAudit:
    """Check exact v0.3 Lean GerbeBeliefBoundary DATA from original source."""
    try:
        belief, receipt, _decision = _validated_original_v03(
            belief_state, belief_receipt, decision_state)
        flags = (
            ("locality_preserved", True),
            ("plurality_preserved", True),
            ("two_truths_separated", True),
            ("paramartha_non_reified", True),
            ("path_search_used", False),
            ("universal_winner_selected", False),
            ("global_trivialization_used", False),
        )
        for flag, expected in flags:
            require_match(truth(receipt, flag, "BeliefReceipt"), expected,
                          "BeliefOS:v03:" + flag)
        if truth(receipt, "surface_holonomy_append_only",
                 "BeliefReceipt") is not True:
            raise UnavailableSource("BeliefOS:v03:surface_history_not_append_only",
                                    BLOCKED)
        return NativeOSBindingAudit(
            os_name=OS_NAME, status=PASS,
            source_digest=_fingerprint(belief),
            source_field_paths=tuple(
                ("BeliefOSReceipt." + flag for flag, _ in flags)
            ) + (
                "BeliefOSReceipt.surface_holonomy_append_only",
                "BeliefOSState.receipt_history[-1].belief_gerbe_receipt_digest",
                "BeliefOSState.surface_holonomy_chain_digest",
                "BeliefOSState.event_count",
                "DecisionOS.source_belief_receipt_digest",
            ),
            checked_witnesses=len(flags),
            issues=("v03_Lean_GerbeBeliefBoundary_proof_fields_not_constructed",),
            original_state_validated=True,
            original_edge_validated=False,
            source_bound_python_conditions_checked=True,
        )
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (ValueError, TypeError, UnicodeError, OverflowError,
            KeyError, AttributeError, RecursionError) as exc:
        return fail(OS_NAME, "BeliefOS:original_gerbe_exception:" +
                    type(exc).__name__, status=BLOCKED)


def audit_native_belief_gerbe_source(
    belief_state: Any, belief_receipt: Any, decision_state: Any,
) -> NativeOSBindingAudit:
    """Keep v0.1 equivalence UNKNOWN although original v0.3 data checked."""
    local = audit_native_gerbe_v03_theorem_conditions(
        belief_state, belief_receipt, decision_state)
    if local.status != PASS:
        return local
    return NativeOSBindingAudit(
        os_name=OS_NAME, status=NO_DATA,
        source_digest=local.source_digest,
        source_field_paths=local.source_field_paths,
        checked_witnesses=local.checked_witnesses,
        issues=(
            "BeliefGerbeV03_to_BeliefFutureOnlyCommitV01_unproved",
            "v01_FutureOnlyBeliefCommit_proof_fields_not_observed",
        ),
        original_state_validated=True,
        original_edge_validated=False,
        source_bound_python_conditions_checked=True,
    )


__all__ = (
    "OS_NAME", "FORMAL_V03", "FORMAL_V01", "V03_THEOREMS",
    "audit_native_gerbe_v03_theorem_conditions",
    "audit_native_belief_gerbe_source",
)
