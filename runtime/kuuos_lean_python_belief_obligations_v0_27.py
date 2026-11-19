"""BeliefOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "BeliefOS"
LEAN_FILE = "formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean"
THEOREMS = ["counterevidence_is_not_silently_erased","beliefLearning_does_not_overwrite_history","beliefActivation_requires_replan"]
FIELDS = ["priorCount","nextCount","futureOnly","memoryOverwrite","activationBoundaryIsReplan"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    prior = v.nat("priorCount")
    next_count = v.nat("nextCount")
    if prior is not None and next_count is not None:
        v.require(prior <= next_count, "counterevidence:append_only_required")
    for key, expected in (("futureOnly", True), ("memoryOverwrite", False),
                          ("activationBoundaryIsReplan", True)):
        v.flag(key, expected)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

