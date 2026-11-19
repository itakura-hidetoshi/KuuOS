"""ObserveOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "ObserveOS"
LEAN_FILE = "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean"
THEOREMS = ["observation_requires_committed_effect","observation_requires_canonical_ready_receipt","comparison_is_not_verification","inconclusive_requires_reobservation","conflicted_requires_reobservation","every_observation_preserves_verification_debt"]
FIELDS = ["committedActState","effectRecorded","canonicalReadyReceipt","comparisonIsVerification","verdict","observationDebtDischarged","reobservationRequired","verificationRequired"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("committedActState", "effectRecorded",
                "canonicalReadyReceipt", "verificationRequired"):
        v.flag(key, True)
    v.flag("comparisonIsVerification", False)
    verdict = v.enum("verdict", ("matched", "divergent", "inconclusive", "conflicted"))
    debt = v.bool_value("observationDebtDischarged")
    reobserve = v.bool_value("reobservationRequired")
    if verdict in ("matched", "divergent"):
        if debt is not None:
            v.require(debt, "observation:matched_or_divergent_discharge_debt")
        if reobserve is not None:
            v.require(not reobserve, "observation:reobservation_not_required")
    elif verdict in ("inconclusive", "conflicted"):
        if debt is not None:
            v.require(not debt, "observation:debt_must_remain")
        if reobserve is not None:
            v.require(reobserve, "observation:reobservation_required")
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

