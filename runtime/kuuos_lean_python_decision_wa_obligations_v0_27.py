"""DecisionOSWa: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "DecisionOSWa"
LEAN_FILE = "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean"
THEOREMS = ["endorsedWa_has_no_confirmed_false_harmony","endorsedWa_preserves_minority","endorsedWa_considers_dissent","endorsedWa_preserves_plural_selected_identity"]
FIELDS = ["confirmedFalseHarmony","minorityPreserved","dissentConsidered","minimumWaPassed","weakestDimensionPassed","sourcePluralIdentityPreserved"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    v.flag("confirmedFalseHarmony", False)
    for key in ("minorityPreserved", "dissentConsidered", "minimumWaPassed",
                "weakestDimensionPassed", "sourcePluralIdentityPreserved"):
        v.flag(key, True)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)


def audit_native_edge(source_state: Any, target_state: Any):
    """Check original typed mediator handoff; cannot skip the source OS."""
    from runtime.kuuos_lean_python_os_registry_v0_5 import audit_edge
    return audit_edge("DecisionOSPlural", "DecisionOSWa",
                      source_state, target_state)

