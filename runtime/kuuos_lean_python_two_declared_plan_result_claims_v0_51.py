"""v0.51: compare two untrusted caller-declared PlanOS result supplements.

The two claims are NOT verified independent issuers or original kernel output.
Uses the original v0.48/v0.49/v0.50 audits, preserves source NO_DATA and any
explicit pairwise discrepancy. No native kernel, issuer lookup or host effect.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import kuuos_lean_python_explicit_plan_result_evidence_v0_50 as prior
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    BLOCKED, NO_DATA, _plain_copy, _fingerprint,
)

VERSION = "kuuos_lean_python_two_declared_plan_result_claims_v0_51"
SCHEMA = "kuuos.plan-result-two-declarations.v0.51"
PROPOSAL_ONLY = "PROPOSAL_ONLY_TWO_DECLARED_PLAN_RESULT_CLAIMS_AGREE"
OBSTRUCTION = "OBSTRUCTION_TWO_DECLARED_PLAN_RESULT_SETS_DISAGREE"
EXPECTED_CLAIMS = frozenset(("first", "second"))
CLAIM_FIELDS = frozenset(("schema_version", "claim_id", "claimed_issuer_label",
                          "supplied_result_evidence"))
UNPROVED = (
    "CLAIM_LABELS_NOT_AUTHENTICATED_ISSUERS",
    "DISTINCT_CLAIM_IDENTIFIERS_NOT_INDEPENDENT_SOURCES",
    "CALLER_DECLARATIONS_NOT_NATIVE_PLANOS_RESULT_OUTPUT",
    "NO_ORIGINAL_TYPED_EVIDENCEMATCHESORIGINAL_PROOF_FROM_JSON",
    "NO_HISTORICAL_CAUSAL_IDENTITY_OR_COMMON_CLOCK",
    "NO_GLOBAL_DESCENT_OR_HOST_EXECUTION_AUTHORITY",
)


@dataclass(frozen=True)
class TwoDeclaredResultClaimsAudit:
    status: str
    issues: tuple[str, ...] = ()
    conflicting_fields: tuple[str, ...] = ()
    declared_claims: tuple[tuple[str, str], ...] = ()
    result_sets_by_claim: tuple[tuple[str, str, tuple[str, ...]], ...] = ()
    original_plan_result_state: str = NO_DATA
    original_source_projection_checked: bool = False
    first_supplement_locally_checked: bool = False
    second_supplement_locally_checked: bool = False
    pairwise_agreement_checked: bool = False
    claimed_issuers_independent: bool = False
    external_issuer_authenticated: bool = False
    original_lean_match_proved: bool = False
    global_descent_certified: bool = False
    host_execution_authorized: bool = False
    native_kernel_invocations: int = 0
    read_only: bool = True
    unresolved: tuple[str, ...] = UNPROVED


def _hold(status: str, *issues: str, source_checked: bool = False,
          first_checked: bool = False, second_checked: bool = False):
    return TwoDeclaredResultClaimsAudit(
        status=status,
        issues=tuple(dict.fromkeys(issues)),
        original_source_projection_checked=source_checked,
        first_supplement_locally_checked=first_checked,
        second_supplement_locally_checked=second_checked,
    )


def _claim_label(value: Any) -> bool:
    return (type(value) is str and 0 < len(value) <= 128
            and value == value.strip()
            and all(32 <= ord(ch) < 127 for ch in value))


def audit_two_declared_plan_result_claims(
    original_verify_certificate: Any,
    original_plan_certificate: Any,
    supplied_claims: Any = None,
) -> TwoDeclaredResultClaimsAudit:
    """Bounded comparison, without upgrading either caller declaration."""
    source = prior.audit_supplied_plan_result_evidence(
        original_verify_certificate, original_plan_certificate,
    )
    if source.status != NO_DATA or not source.source_projection_checked:
        return _hold(source.status, *source.issues)
    if supplied_claims is None:
        return _hold(NO_DATA, "two_claim_envelopes_missing", source_checked=True)
    if type(supplied_claims) is not dict:
        return _hold(BLOCKED, "two_named_plain_claims_required", source_checked=True)
    if not set(supplied_claims).issubset(EXPECTED_CLAIMS):
        return _hold(BLOCKED, "unknown_claim_slot", source_checked=True)
    if set(supplied_claims) != EXPECTED_CLAIMS:
        return _hold(NO_DATA, "required_claim_slot_missing", source_checked=True)

    try:
        copied = _plain_copy(supplied_claims, "two_claims", dict)
        before = _fingerprint(copied)
    except (TypeError, ValueError, RecursionError, OverflowError) as exc:
        return _hold(BLOCKED, "invalid_finite_claim_json:" + type(exc).__name__,
                     source_checked=True)

    claims: list[dict] = []
    checked: list[bool] = []
    for slot in ("first", "second"):
        claim = copied[slot]
        if type(claim) is not dict or set(claim) != CLAIM_FIELDS:
            return _hold(BLOCKED, slot + ":claim_schema_mismatch", source_checked=True,
                         first_checked=bool(checked), second_checked=False)
        if claim.get("schema_version") != SCHEMA or type(claim.get("schema_version")) is not str:
            return _hold(BLOCKED, slot + ":claim_version_mismatch", source_checked=True,
                         first_checked=bool(checked), second_checked=False)
        if not _claim_label(claim.get("claim_id")) or not _claim_label(claim.get("claimed_issuer_label")):
            return _hold(BLOCKED, slot + ":invalid_declared_identifiers",
                         source_checked=True, first_checked=bool(checked))
        one = prior.audit_supplied_plan_result_evidence(
            original_verify_certificate, original_plan_certificate,
            claim.get("supplied_result_evidence"),
        )
        if one.status != prior.PROPOSAL_ONLY:
            return _hold(one.status, *(slot + ":" + issue for issue in one.issues),
                         source_checked=True, first_checked=bool(checked))
        checked.append(True)
        claims.append(claim)

    first, second = claims
    if first["claim_id"] == second["claim_id"]:
        return _hold(BLOCKED, "duplicate_declared_claim_id", source_checked=True,
                     first_checked=True, second_checked=True)
    fields = prior.RESULT_FIELDS
    result_sets = tuple(
        (claim["claim_id"], field, tuple(claim["supplied_result_evidence"][field]))
        for claim in (first, second) for field in fields
    )
    conflicts = tuple(
        field for field in fields
        if first["supplied_result_evidence"][field] !=
            second["supplied_result_evidence"][field]
    )
    try:
        if _fingerprint(supplied_claims) != before:
            return _hold(BLOCKED, "caller_claims_mutated_during_audit",
                         source_checked=True, first_checked=True,
                         second_checked=True)
    except (TypeError, ValueError, RecursionError, OverflowError):
        return _hold(BLOCKED, "caller_claims_reobservation_unavailable",
                     source_checked=True, first_checked=True,
                     second_checked=True)

    return TwoDeclaredResultClaimsAudit(
        status=OBSTRUCTION if conflicts else PROPOSAL_ONLY,
        issues=(
            tuple("declared_result_conflict:" + x for x in conflicts)
            if conflicts else UNPROVED
        ),
        conflicting_fields=conflicts,
        declared_claims=tuple(
            (c["claim_id"], c["claimed_issuer_label"]) for c in claims
        ),
        result_sets_by_claim=result_sets,
        original_source_projection_checked=True,
        first_supplement_locally_checked=True,
        second_supplement_locally_checked=True,
        pairwise_agreement_checked=not bool(conflicts),
        original_plan_result_state=NO_DATA,
        claimed_issuers_independent=False,
        external_issuer_authenticated=False,
        original_lean_match_proved=False,
        host_execution_authorized=False,
    )


__all__ = (
    "VERSION", "SCHEMA", "PROPOSAL_ONLY", "OBSTRUCTION",
    "CLAIM_FIELDS", "EXPECTED_CLAIMS", "UNPROVED",
    "TwoDeclaredResultClaimsAudit", "audit_two_declared_plan_result_claims",
)
