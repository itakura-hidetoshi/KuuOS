"""v0.49: preserve missing original PlanOS resulting sets as NO_DATA.

Input is the independently emitted original VerifyOS/PlanOS Python certificate
pair, not a reconstructed Lean structure. This read-only check uses v0.48
first and disallows forged newly advertised result-set fields.
An original PlanOS digest is not independent authentication or a causal clock.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import (
    kuuos_lean_python_original_verify_plan_certificate_seam_v0_48 as prior,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    NO_DATA, BLOCKED,
)

VERSION = "kuuos_lean_python_plan_result_observation_obstruction_v0_49"
MISSING_ORIGINAL_OUTPUTS = (
    "resulting_lineage_digests",
    "resulting_dissent_evidence_digests",
    "resulting_minority_evidence_digests",
)
MISSING_PROOF_OBLIGATIONS = (
    "PLANOS_RESULTING_LINEAGE_FINSET_NOT_OBSERVED",
    "PLANOS_RESULTING_DISSENT_FINSET_NOT_OBSERVED",
    "PLANOS_RESULTING_MINORITY_FINSET_NOT_OBSERVED",
    "DIGEST_CANNOT_AUTHENTICATE_ORIGINAL_CAUSAL_EXECUTION",
    "LEAN_TO_CPYTHON_UNIVERSAL_REFINEMENT_NOT_PROVED",
    "GLOBAL_DESCENT_AND_HOST_AUTHORITY_NOT_GRANTED",
)


@dataclass(frozen=True)
class OriginalPlanResultObstruction:
    status: str
    issues: tuple[str, ...] = ()
    source_projection_checked: bool = False
    retained_source_transition: str | None = None
    unobserved: tuple[str, ...] = MISSING_PROOF_OBLIGATIONS
    plan_resulting_lineage_observed: bool = False
    plan_resulting_dissent_observed: bool = False
    plan_resulting_minority_observed: bool = False
    universal_lean_cpython_refinement: bool = False
    externally_authenticated: bool = False
    global_descent_certified: bool = False
    host_execution_permission: bool = False
    native_kernels_invoked: int = 0
    read_only: bool = True


def audit_original_plan_result_obstruction(
    original_verify_certificate: Any,
    original_plan_certificate: Any,
) -> OriginalPlanResultObstruction:
    """Reject invented result sets; otherwise keep genuine absence NO_DATA.

    The source of positive bounded projection evidence is v0.48. This function
    does not conflate that proof with an unavailable full Lean certificate.
    """
    baseline = prior.audit_original_certificates(
        original_verify_certificate, original_plan_certificate,
    )
    if baseline.status != prior.SCOPED:
        return OriginalPlanResultObstruction(
            status=baseline.status,
            issues=tuple(baseline.issues),
        )
    # baseline SCOPED establishes plain original finite JSON dictionaries.
    extra = tuple(
        field for field in MISSING_ORIGINAL_OUTPUTS
        if field in original_plan_certificate
    )
    if extra:
        return OriginalPlanResultObstruction(
            status=BLOCKED,
            issues=tuple("unsupported_original_plan_result:" + field for field in extra),
            source_projection_checked=True,
            retained_source_transition=baseline.transition_kind,
        )
    return OriginalPlanResultObstruction(
        status=NO_DATA,
        issues=MISSING_PROOF_OBLIGATIONS,
        source_projection_checked=True,
        retained_source_transition=baseline.transition_kind,
    )


__all__ = (
    "VERSION", "MISSING_ORIGINAL_OUTPUTS", "MISSING_PROOF_OBLIGATIONS",
    "OriginalPlanResultObstruction", "audit_original_plan_result_obstruction",
)
