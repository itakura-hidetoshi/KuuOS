"""DecisionOSPlural: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "DecisionOSPlural"
LEAN_FILE = "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean"
THEOREMS = ["rawVeto_does_not_grant_authority","validatedVeto_excludes_consensus","validatedVeto_is_mission_bound","validatedVeto_is_stakeholder_protected"]
FIELDS = ["optionInSourceField","missionBoundConstraint","stakeholderProtectedConstraint","evidencePresent","grantsAuthority","excludesConsensusOption"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("optionInSourceField", "missionBoundConstraint",
                "stakeholderProtectedConstraint", "evidencePresent",
                "excludesConsensusOption"):
        v.flag(key, True)
    v.flag("grantsAuthority", False)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)


def audit_native_edge(source_state: Any, target_state: Any):
    """Check original typed mediator handoff; cannot skip the source OS."""
    from runtime.kuuos_lean_python_os_registry_v0_5 import audit_edge
    return audit_edge("DecisionOS", "DecisionOSPlural",
                      source_state, target_state)

