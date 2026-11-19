"""DecisionOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "DecisionOS"
LEAN_FILE = "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean"
THEOREMS = ["admissibleOption_is_not_prohibited","admissibleOption_does_not_claim_authority","decisionCommit_does_not_overwrite_memory","decisionCommit_is_not_execution"]
FIELDS = ["missionAllowed","prohibited","authorityClaimed","withinBudget","withinRisk","recoverable","reversible","evidencePresent","futureOnly","memoryOverwrite","decisionNotExecution"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("missionAllowed", "withinBudget", "withinRisk",
                "recoverable", "reversible", "evidencePresent", "futureOnly",
                "decisionNotExecution"):
        v.flag(key, True)
    for key in ("prohibited", "authorityClaimed", "memoryOverwrite"):
        v.flag(key, False)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

