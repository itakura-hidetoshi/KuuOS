"""PlanOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "PlanOS"
LEAN_FILE = "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean"
THEOREMS = ["effectfulStep_has_rollback_or_escalation","effectfulStep_has_stop_condition","effectfulStep_has_checkpoint","plan_does_not_execute"]
FIELDS = ["effectful","rollbackPresent","humanReviewRequired","externalLicenseRequired","stopConditionPresent","checkpointPresent","planIsExecution"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    effectful = v.bool_value("effectful")
    rollback = v.bool_value("rollbackPresent")
    human = v.bool_value("humanReviewRequired")
    license_bound = v.bool_value("externalLicenseRequired")
    stop = v.bool_value("stopConditionPresent")
    checkpoint = v.bool_value("checkpointPresent")
    v.flag("planIsExecution", False)
    if effectful is True:
        if rollback is not None and human is not None and license_bound is not None:
            v.require(rollback or (human and license_bound),
                      "effectful:rollback_or_authorized_escalation_required")
        if stop is not None:
            v.require(stop, "effectful:stop_condition_required")
        if checkpoint is not None:
            v.require(checkpoint, "effectful:checkpoint_required")
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

