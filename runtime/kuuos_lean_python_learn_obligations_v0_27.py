"""LearnOS: selected Lean theorem data obligations, v0.27.

The source Lean structure contains proof fields not constructible by a
Python boolean packet. A LOCAL result checks supplied data conditions only,
not Lean-to-Python refinement, original-state authenticity or authority.
Original OS kernel is unmodified. Copyright Hidetoshi Itakura / 板倉英俊.
"""
from __future__ import annotations

from typing import Any
from runtime.kuuos_lean_python_per_os_contracts_v0_27 import (
    Verifier, original_state_audit,
)

OS_NAME = "LearnOS"
LEAN_FILE = "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean"
THEOREMS = ["learning_delta_is_future_only","learning_delta_is_inactive_until_replan","learning_delta_does_not_overwrite_memory","learning_delta_preserves_current_and_past","learning_delta_preserves_scope_and_invariants"]
FIELDS = ["futureOnly","memoryOverwrite","activeNow","activationRequiresReplan","scopeWidening","invariantRemoval","currentCycleMutation","pastRecordMutation","reversalConditionVisible","expirationConditionVisible"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("futureOnly", "activationRequiresReplan",
                "reversalConditionVisible", "expirationConditionVisible"):
        v.flag(key, True)
    for key in ("memoryOverwrite", "activeNow", "scopeWidening",
                "invariantRemoval", "currentCycleMutation", "pastRecordMutation"):
        v.flag(key, False)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

