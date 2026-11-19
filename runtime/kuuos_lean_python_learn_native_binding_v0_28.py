"""LearnOS: source-bind future-only learning proof conditions to real delta.

Requires original Verify→Learn lineage and original learning_delta digest.
This is not an activation of the candidate or a memory write.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_native_os_source_binding_v0_28 import (
    BLOCKED, UnavailableSource, copied_state, copied_edge, fail,
    field, truth, string, require_match, finalize,
)
from runtime.kuuos_learn_os_types_v0_1 import (
    learning_delta_digest as original_delta_digest,
)

OS_NAME = "LearnOS"


def audit_native_learn_from_verify(verify_state: Any, learn_state: Any):
    try:
        verify = copied_state("VerifyOS", verify_state)
        learn = copied_state(OS_NAME, learn_state)
        copied_edge("VerifyOS", OS_NAME, verify, learn)
        delta = field(learn, "learning_delta", "LearnOS")
        delta_id = string(delta, "learning_delta_digest", "LearnOS.delta")
        require_match(delta_id, original_delta_digest(delta),
                      "LearnOS.learning_delta.digest")
        require_match(string(learn, "learning_delta_digest", "LearnOS"),
                      delta_id, "LearnOS.learning_delta.source_binding")
        require_match(string(delta, "source_verify_state_digest", "LearnOS.delta"),
                      string(verify, "verify_state_digest", "VerifyOS"),
                      "LearnOS.delta.verify_lineage")
        require_match(string(learn, "source_verify_state_digest", "LearnOS"),
                      string(verify, "verify_state_digest", "VerifyOS"),
                      "LearnOS.state.verify_lineage")
        if not truth(learn, "learning_recorded", "LearnOS"):
            raise UnavailableSource("LearnOS:learning_not_recorded")
        if not truth(learn, "replan_required", "LearnOS"):
            raise UnavailableSource("LearnOS:replan_not_recorded", BLOCKED)
        reversal = string(delta, "reversal_condition_digest", "LearnOS.delta")
        expiration = string(delta, "expiration_condition_digest", "LearnOS.delta")
        projection = {
            "futureOnly": truth(delta, "future_only", "LearnOS.delta"),
            "memoryOverwrite": truth(delta, "memory_overwrite", "LearnOS.delta"),
            "activeNow": truth(delta, "active_now", "LearnOS.delta"),
            "activationRequiresReplan": truth(
                delta, "activation_requires_replan", "LearnOS.delta"),
            "scopeWidening": truth(delta, "scope_widening", "LearnOS.delta"),
            "invariantRemoval": truth(delta, "invariant_removal", "LearnOS.delta"),
            "currentCycleMutation": truth(
                delta, "current_cycle_mutation", "LearnOS.delta"),
            "pastRecordMutation": truth(
                delta, "past_record_mutation", "LearnOS.delta"),
            "reversalConditionVisible": bool(reversal.strip()),
            "expirationConditionVisible": bool(expiration.strip()),
        }
        require_match(projection["activeNow"],
                      truth(learn, "active_now", "LearnOS"), "LearnOS:active_state")
        paths = [
            "VerifyOS.verify_state_digest", "LearnOS.source_verify_state_digest",
            "LearnOS.learning_recorded", "LearnOS.replan_required", "LearnOS.active_now",
            "LearnOS.learning_delta.learning_delta_digest",
            "LearnOS.learning_delta.source_verify_state_digest",
            "LearnOS.learning_delta.future_only",
            "LearnOS.learning_delta.memory_overwrite",
            "LearnOS.learning_delta.active_now",
            "LearnOS.learning_delta.activation_requires_replan",
            "LearnOS.learning_delta.scope_widening",
            "LearnOS.learning_delta.invariant_removal",
            "LearnOS.learning_delta.current_cycle_mutation",
            "LearnOS.learning_delta.past_record_mutation",
            "LearnOS.learning_delta.reversal_condition_digest",
            "LearnOS.learning_delta.expiration_condition_digest",
        ]
        return finalize(OS_NAME, learn, [projection], paths, edge_validated=True)
    except UnavailableSource as exc:
        return fail(OS_NAME, exc.reason, status=exc.status)
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        return fail(OS_NAME, "original_learning_digest_check:" + type(exc).__name__,
                    status=BLOCKED)


__all__ = ("OS_NAME", "audit_native_learn_from_verify")
