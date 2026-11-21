"""v0.50: check caller-supplied PlanOS result sets without manufacturing truth.

The original PlanOS v1.03 output lacks three *resulting* Finsets.
v0.48 source-projection checks and v0.49 NO_DATA are prerequisites.
An optional separate evidence object can be checked for bounded consistency,
but not authenticated as a native PlanOS output or as a Lean proof term.

No native kernel is run, no memory or world state is written.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import kuuos_lean_python_plan_result_observation_obstruction_v0_49 as prior
from runtime import kuuos_lean_python_original_verify_plan_certificate_seam_v0_48 as original
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, _plain_copy, _fingerprint,
)

VERSION = "kuuos_lean_python_explicit_plan_result_evidence_v0_50"
PROPOSAL_ONLY = "PROPOSAL_ONLY_BOUNDED_SUPPLIED_PLAN_RESULT_EVIDENCE"
SCHEMA = "kuuos.plan-result-supplied-evidence.v0.50"
REQUIRED_FIELDS = frozenset((
    "schema_version",
    "source_verifyos_certificate_digest",
    "source_planos_certificate_digest",
    "resulting_lineage_digests",
    "resulting_dissent_evidence_digests",
    "resulting_minority_evidence_digests",
))
RESULT_FIELDS = (
    "resulting_lineage_digests",
    "resulting_dissent_evidence_digests",
    "resulting_minority_evidence_digests",
)
UNPROVED = (
    "CALLER_SUPPLIED_RESULT_SETS_NOT_ORIGINALLY_EMITTED_BY_PLANOS",
    "PLANOS_RESULT_FINSETS_NOT_VERIFIED_AS_LEAN_PROOF_TERMS",
    "EXTERNAL_ISSUER_NOT_AUTHENTICATED",
    "HISTORICAL_CALL_IDENTITY_AND_CAUSAL_CLOCK_UNPROVED",
    "UNIVERSAL_LEAN_CPYTHON_REFINEMENT_UNPROVED",
    "GLOBAL_DESCENT_AND_HOST_EXECUTION_AUTHORITY_NOT_GRANTED",
)


@dataclass(frozen=True)
class SuppliedPlanResultEvidenceAudit:
    status: str
    issues: tuple[str, ...] = ()
    source_projection_checked: bool = False
    submitted_sets_consistent_with_source: bool = False
    original_plan_result_state: str = NO_DATA
    input_source_unchanged: bool = False
    native_result_sets_observed: bool = False
    original_lean_evidence_proof_constructed: bool = False
    external_issuer_authenticated: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    read_only: bool = True
    unresolved: tuple[str, ...] = UNPROVED


def _hold(status: str, *issues: str, source_checked: bool = False):
    return SuppliedPlanResultEvidenceAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        source_projection_checked=source_checked,
    )


def _canonical_set_list(value: Any) -> bool:
    return (type(value) is list
            and all(type(x) is str and bool(x) for x in value)
            and value == sorted(set(value)))


def audit_supplied_plan_result_evidence(
    verify_certificate: Any,
    plan_certificate: Any,
    supplied_evidence: Any = None,
) -> SuppliedPlanResultEvidenceAudit:
    """Return PROPOSAL_ONLY for bounded-consistent evidence, never CERTIFIED."""
    base = prior.audit_original_plan_result_obstruction(
        verify_certificate, plan_certificate,
    )
    if base.status != NO_DATA or not base.source_projection_checked:
        return _hold(base.status, *base.issues)
    if supplied_evidence is None:
        return _hold(NO_DATA, "separate_original_result_evidence_missing",
                     source_checked=True)
    if type(supplied_evidence) is not dict:
        return _hold(BLOCKED, "plain_supplied_evidence_dictionary_required",
                     source_checked=True)
    try:
        supplied = _plain_copy(supplied_evidence, "evidence", dict)
        before = _fingerprint(supplied)
    except (TypeError, ValueError, RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "invalid_supplied_json:" + type(exc).__name__,
                     source_checked=True)
    if set(supplied) != REQUIRED_FIELDS:
        return _hold(BLOCKED, "supplied_evidence_schema_incomplete_or_extra",
                     source_checked=True)
    if type(supplied["schema_version"]) is not str or supplied["schema_version"] != SCHEMA:
        return _hold(BLOCKED, "supplied_schema_version_mismatch", source_checked=True)

    expected_verify = verify_certificate.get(
        "verifyos_middle_way_conditional_continuity_certificate_digest"
    )
    expected_plan = plan_certificate.get(
        "planos_middle_way_bounded_synthesis_intake_certificate_digest"
    )
    if (type(supplied["source_verifyos_certificate_digest"]) is not str
            or type(supplied["source_planos_certificate_digest"]) is not str
            or supplied["source_verifyos_certificate_digest"] != expected_verify
            or supplied["source_planos_certificate_digest"] != expected_plan):
        return _hold(BLOCKED, "source_certificate_reference_mismatch",
                     source_checked=True)
    if not all(_canonical_set_list(supplied[x]) for x in RESULT_FIELDS):
        return _hold(BLOCKED, "result_set_not_canonical_plain_list",
                     source_checked=True)
    spec = plan_certificate["source_transition_spec"]
    obligations = (
        ("resulting_lineage_digests", "resulting_lineage_digests"),
        ("resulting_dissent_evidence_digests", "preserved_dissent_evidence_digests"),
        ("resulting_minority_evidence_digests", "preserved_minority_evidence_digests"),
    )
    for destination, required in obligations:
        if not set(spec[required]).issubset(supplied[destination]):
            return _hold(BLOCKED, "source_provenance_erased:" + destination,
                         source_checked=True)
    if spec["predecessor_reference_digest"] not in supplied["resulting_lineage_digests"]:
        return _hold(BLOCKED, "original_predecessor_erased", source_checked=True)

    try:
        unchanged = before == _fingerprint(supplied_evidence)
    except (TypeError, ValueError, RecursionError, OverflowError):
        unchanged = False
    if not unchanged:
        return _hold(BLOCKED, "caller_supplied_evidence_mutated", source_checked=True)
    return SuppliedPlanResultEvidenceAudit(
        status=PROPOSAL_ONLY,
        issues=UNPROVED,
        source_projection_checked=True,
        submitted_sets_consistent_with_source=True,
        original_plan_result_state=NO_DATA,
        input_source_unchanged=unchanged,
        native_result_sets_observed=False,
    )


__all__ = (
    "VERSION", "SCHEMA", "PROPOSAL_ONLY", "REQUIRED_FIELDS", "RESULT_FIELDS",
    "UNPROVED", "SuppliedPlanResultEvidenceAudit",
    "audit_supplied_plan_result_evidence",
)
