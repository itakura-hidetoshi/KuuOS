"""VerifyOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "VerifyOS"
LEAN_FILE = "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean"
THEOREMS = ["passed_requires_satisfied_unfalsified_criterion","passed_requires_matched_admissible_observation","failed_requires_conclusive_failure_basis","indeterminate_is_not_conclusive","every_verdict_requires_learning","indeterminate_preserves_verification_debt"]
FIELDS = ["verdict","sourceMatched","sourceDivergent","corroborationAdmissible","criterionSatisfied","falsifierTriggered","verificationIsTruth","causalAttributionGranted","verificationDebtDischarged","verificationRequired","reobservationRequired","correctiveActionRequired","learningRequired"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    verdict = v.enum("verdict", ("passed", "failed", "indeterminate"))
    for key in ("verificationIsTruth", "causalAttributionGranted"):
        v.flag(key, False)
    v.flag("learningRequired", True)
    matched = v.bool_value("sourceMatched")
    divergent = v.bool_value("sourceDivergent")
    corroborated = v.bool_value("corroborationAdmissible")
    criterion = v.bool_value("criterionSatisfied")
    falsifier = v.bool_value("falsifierTriggered")
    debt = v.bool_value("verificationDebtDischarged")
    required = v.bool_value("verificationRequired")
    reobserve = v.bool_value("reobservationRequired")
    corrective = v.bool_value("correctiveActionRequired")
    if verdict == "passed":
        for value, reason in ((matched, "passed:source_matched"),
                              (corroborated, "passed:corroboration_admissible"),
                              (criterion, "passed:criterion_satisfied"),
                              (debt, "passed:debt_discharged")):
            if value is not None:
                v.require(value, reason)
        for value, reason in ((falsifier, "passed:no_falsifier"),
                              (required, "passed:no_verification_debt"),
                              (reobserve, "passed:no_reobservation"),
                              (corrective, "passed:no_corrective_action")):
            if value is not None:
                v.require(not value, reason)
    elif verdict == "failed":
        if corroborated is not None:
            v.require(corroborated, "failed:corroboration_admissible")
        if None not in (divergent, criterion, falsifier):
            v.require(divergent or not criterion or falsifier,
                      "failed:failure_basis_required")
        for value, reason in ((debt, "failed:debt_discharged"),
                              (corrective, "failed:corrective_action")):
            if value is not None:
                v.require(value, reason)
        for value, reason in ((required, "failed:no_verification_debt"),
                              (reobserve, "failed:no_reobservation")):
            if value is not None:
                v.require(not value, reason)
    elif verdict == "indeterminate":
        if corroborated is not None:
            v.require(not corroborated, "indeterminate:no_admissible_corroboration")
        for value, reason in ((required, "indeterminate:verification_remains"),
                              (reobserve, "indeterminate:reobservation_required")):
            if value is not None:
                v.require(value, reason)
        for value, reason in ((debt, "indeterminate:debt_not_discharged"),
                              (corrective, "indeterminate:no_corrective_action")):
            if value is not None:
                v.require(not value, reason)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

