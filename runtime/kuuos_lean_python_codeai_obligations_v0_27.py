"""CodeAI: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "CodeAI"
LEAN_FILE = "formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean"
THEOREMS = ["highScoreCannotOverrideInadmissible","incompleteEvidenceCannotBecomeEligible","Receipt.WellFormed.selectedCandidateEligible","Receipt.WellFormed.scoreBoundary","Receipt.WellFormed.abstentionIsNotRejection"]
FIELDS = ["candidateId","sourceClassification","evidenceStatus","evidenceScore","maximumEvidenceScore","decision","scoreTreatedAsProbability","scoreTreatedAsCorrectnessProof","selectionTreatedAsCorrectnessProof","abstentionTreatedAsRejection"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    v.string("candidateId")
    classification = v.enum("sourceClassification",
                            ("admissible", "repairable", "hold", "rejected"))
    evidence = v.enum("evidenceStatus", ("allPassed", "hasFailure", "incomplete"))
    v.nat("evidenceScore")
    v.nat("maximumEvidenceScore")
    decision = v.enum("decision", ("selected", "abstained"))
    for key in ("scoreTreatedAsProbability", "scoreTreatedAsCorrectnessProof",
                "selectionTreatedAsCorrectnessProof", "abstentionTreatedAsRejection"):
        v.flag(key, False)
    if decision == "selected" and classification is not None and evidence is not None:
        v.require(classification == "admissible" and evidence == "allPassed",
                  "selection:requires_strict_eligible_candidate")
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

