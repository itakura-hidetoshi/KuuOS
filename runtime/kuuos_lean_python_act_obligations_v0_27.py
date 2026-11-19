"""ActOS: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "ActOS"
LEAN_FILE = "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean"
THEOREMS = ["invocation_requires_committed_plan","invocation_requires_exact_step","invocation_requires_act_phase","invocation_requires_host_license","invocation_requires_projection_receipt_binding","authorization_is_single_use","invocation_claims_at_most_one_job","invocation_runs_at_most_one_slice"]
FIELDS = ["committedPlanBound","exactStepBound","actPhaseBound","hostLicenseBound","projectionReceiptBound","singleUse","doesNotWidenLicense","jobsClaimed","slicesRun"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("committedPlanBound", "exactStepBound", "actPhaseBound",
                "hostLicenseBound", "projectionReceiptBound", "singleUse",
                "doesNotWidenLicense"):
        v.flag(key, True)
    jobs = v.nat("jobsClaimed")
    slices = v.nat("slicesRun")
    if jobs is not None:
        v.require(jobs <= 1, "invocation:jobs_at_most_one")
    if slices is not None:
        v.require(slices <= 1, "invocation:slices_at_most_one")
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

