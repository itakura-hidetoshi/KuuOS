"""v0.48 read-only projections of ORIGINAL VerifyOS and PlanOS certificates.

Checks exactly the data actually serialized by the original Python kernels.
Does not manufacture an unobserved PlanOS resulting-lineage field; does not
re-run kernels, authenticate issuers, or prove a Lean/CPython refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime import (
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as native_verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as native_plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    ROUTES, VERIFY_TRUE, VERIFY_FALSE, PLAN_TRUE, PLAN_FALSE,
    _plain_copy, _fingerprint, BLOCKED, NO_DATA,
)

VERSION = "kuuos_lean_python_original_verify_plan_certificate_seam_v0_48"
SCOPED = "SCOPED_ORIGINAL_VERIFY_PLAN_CERTIFICATE_PROJECTION_V0_48"
MATCHED_FIELDS = (
    ("source_handoff_receipt_digest", "source_decisionos_handoff_receipt_digest"),
    ("source_selection_receipt_digest", "source_selection_receipt_digest"),
    ("source_world_binding_digest", "source_world_binding_digest"),
    ("source_world_model_state_digest", "source_world_model_state_digest"),
    ("source_world_model_revision", "source_world_model_revision"),
    ("source_world_lineage_digest", "source_world_lineage_digest"),
    ("source_synthesis_constraint_digest", "source_synthesis_constraint_digest"),
    ("source_synthesis_handoff_bundle_digest", "source_synthesis_handoff_bundle_digest"),
    ("selected_candidate_id", "selected_candidate_id"),
    ("selected_candidate_plan_intent_digest", "selected_candidate_plan_intent_digest"),
    ("transition_kind", "transition_kind"),
    ("conditional_validity_status", "conditional_validity_status"),
    ("transition_reason_digest", "transition_reason_digest"),
)
SPEC_LISTS = (
    "source_lineage_digests",
    "resulting_lineage_digests",
    "source_responsibility_lineage_digests",
    "resulting_responsibility_lineage_digests",
    "preserved_dissent_evidence_digests",
    "preserved_minority_evidence_digests",
)
UNOBSERVED = (
    "PLANOS_RESULTING_LINEAGE_FINSET_NOT_EXPLICITLY_SERIALIZED",
    "PLANOS_RESULTING_DISSENT_FINSET_NOT_EXPLICITLY_SERIALIZED",
    "PLANOS_RESULTING_MINORITY_FINSET_NOT_EXPLICITLY_SERIALIZED",
    "CERTIFICATE_DIGEST_BINDING_IS_NOT_HISTORICAL_CALL_IDENTITY",
    "GENERAL_LEAN_CPYTHON_REFINEMENT_NOT_PROVED",
    "EXTERNAL_ISSUER_AND_GLOBAL_DESCENT_NOT_PROVED",
    "HOST_EXECUTION_AUTHORITY_NOT_GRANTED",
)


@dataclass(frozen=True)
class OriginalCertificateProjectionAudit:
    status: str
    issues: tuple[str, ...] = ()
    transition_kind: str | None = None
    bounded_intake_admitted: bool = False
    exact_original_source_projection_checked: bool = False
    original_provenance_monotonicity_checked: bool = False
    resulting_plan_responsibility_checked: bool = False
    unobserved: tuple[str, ...] = UNOBSERVED
    plan_resulting_lineage_finset_certified: bool = False
    historical_native_call_identity_certified: bool = False
    global_descent_certified: bool = False
    lean_cpython_refinement_certified: bool = False
    execution_authority_granted: bool = False
    native_kernel_invocations: int = 0
    read_only: bool = True


def _halt(status: str, *issues: str) -> OriginalCertificateProjectionAudit:
    return OriginalCertificateProjectionAudit(status, tuple(dict.fromkeys(issues)))


def _list_of_unique_sorted_strings(value: Any) -> bool:
    return (type(value) is list
            and all(type(x) is str and bool(x) for x in value)
            and value == sorted(set(value)))


def audit_original_certificates(
    original_verify_certificate: Any,
    original_plan_certificate: Any,
) -> OriginalCertificateProjectionAudit:
    """Projection-level seam for supplied actual native certificate dictionaries.

    All seven original Lean seam fields are retained as formal obligations.
    Only fields actually emitted by Python are examined; missing result sets
    remain unobserved, never inferred from a boolean preservation flag.
    """
    if original_verify_certificate is None or original_plan_certificate is None:
        return _halt(NO_DATA, "original_verify_or_plan_certificate_missing")
    if type(original_verify_certificate) is not dict or type(original_plan_certificate) is not dict:
        return _halt(BLOCKED, "original_certificates_must_be_plain_dicts")
    try:
        v = _plain_copy(original_verify_certificate, "verify", dict)
        p = _plain_copy(original_plan_certificate, "plan", dict)
        original_v_digest = _fingerprint(v)
        original_p_digest = _fingerprint(p)
    except (TypeError, ValueError, RecursionError, OverflowError) as e:
        return _halt(BLOCKED, "invalid_finite_source:" + type(e).__name__)

    issues: list[str] = []
    vk = "verifyos_middle_way_conditional_continuity_certificate_digest"
    pk = "planos_middle_way_bounded_synthesis_intake_certificate_digest"
    if v.get("status") != "VERIFYOS_MIDDLE_WAY_CONDITIONAL_CONTINUITY_VERIFIED":
        issues.append("original_verify_status_invalid")
    if p.get("status") != "PLANOS_MIDDLE_WAY_BOUNDED_SYNTHESIS_INTAKE_ROUTED":
        issues.append("original_plan_status_invalid")
    for cert, key, digest_fn, scope in (
        (v, vk, native_verify.canonical_digest, "verify"),
        (p, pk, native_plan.canonical_digest, "plan"),
    ):
        claim = cert.get(key)
        if (type(claim) is not str or len(claim) != 64
                or claim != digest_fn({k: val for k, val in cert.items() if k != key})):
            issues.append(scope + ":certificate_digest_invalid")

    kind = v.get("transition_kind")
    routes = {k: (s, d, ok) for k, s, d, ok in ROUTES}
    if type(kind) is not str or kind not in routes:
        issues.append("verify_transition_kind_unknown")
    else:
        status, disposition, admitted = routes[kind]
        if (v.get("conditional_validity_status") != status
                or p.get("conditional_validity_status") != status
                or p.get("transition_kind") != kind
                or p.get("intake_disposition") != disposition
                or p.get("bounded_synthesis_request_admitted") is not admitted
                or p.get("bounded_synthesis_intake_ready") is not admitted):
            issues.append("conditional_route_or_admission_mismatch")

    if p.get("source_verifyos_certificate_digest") != v.get(vk):
        issues.append("source_verify_digest_mismatch")
    if p.get("expected_source_verifyos_certificate_digest") != v.get(vk):
        issues.append("expected_verify_digest_mismatch")
    for source, target in MATCHED_FIELDS:
        if source not in v or target not in p or type(v[source]) is not type(p[target]) or v[source] != p[target]:
            issues.append("original_source_field_mismatch:" + source)

    v_spec, p_spec = v.get("transition_spec"), p.get("source_transition_spec")
    if type(v_spec) is not dict or type(p_spec) is not dict:
        issues.append("original_transition_spec_missing")
        v_spec, p_spec = {}, {}
    elif _fingerprint(v_spec) != _fingerprint(p_spec):
        issues.append("original_transition_spec_seam_mismatch")
    if (p.get("source_transition_spec_digest") != v.get("transition_spec_digest")
            or v.get("transition_spec_digest") != native_verify.canonical_digest(v_spec)):
        issues.append("original_transition_spec_digest_mismatch")

    if not all(_list_of_unique_sorted_strings(v_spec.get(k)) for k in SPEC_LISTS):
        issues.append("source_spec_noncanonical_provenance")
    else:
        if not set(v_spec["source_lineage_digests"]).issubset(v_spec["resulting_lineage_digests"]):
            issues.append("verify_lineage_not_monotone")
        if not set(v_spec["source_responsibility_lineage_digests"]).issubset(
                v_spec["resulting_responsibility_lineage_digests"]):
            issues.append("verify_responsibility_not_monotone")
        if v_spec.get("predecessor_reference_digest") not in v_spec["resulting_lineage_digests"]:
            issues.append("verify_predecessor_erased")
        owner = p.get("planos_intake_responsibility_digest")
        final_responsibility = p.get("resulting_responsibility_lineage_digests")
        if (type(owner) is not str or not owner or
                not _list_of_unique_sorted_strings(final_responsibility) or
                final_responsibility != sorted(
                    set(v_spec["resulting_responsibility_lineage_digests"]) | {owner}
                )):
            issues.append("plan_responsibility_extension_mismatch")

    for cert, must_be_true, must_be_false, label in (
        (v, VERIFY_TRUE, VERIFY_FALSE, "verify"),
        (p, PLAN_TRUE, PLAN_FALSE, "plan"),
    ):
        for key in must_be_true:
            if cert.get(key) is not True:
                issues.append(label + ":required_true:" + key)
        for key in must_be_false:
            if cert.get(key) is not False:
                issues.append(label + ":required_false:" + key)
    for key in ("world_mutation_not_granted", "history_read_only", "qi_grants_no_authority"):
        if p.get(key) is not True:
            issues.append("plan:authority_boundary:" + key)
    try:
        if original_v_digest != _fingerprint(original_verify_certificate) or original_p_digest != _fingerprint(original_plan_certificate):
            issues.append("source_mutated_during_read_only_projection")
    except (TypeError, ValueError, RecursionError, OverflowError):
        issues.append("source_reobservation_unavailable")

    if issues:
        return _halt(BLOCKED, *issues)
    return OriginalCertificateProjectionAudit(
        status=SCOPED, transition_kind=kind,
        bounded_intake_admitted=routes[kind][2],
        exact_original_source_projection_checked=True,
        original_provenance_monotonicity_checked=True,
        resulting_plan_responsibility_checked=True,
    )


__all__ = ("VERSION", "SCOPED", "MATCHED_FIELDS", "SPEC_LISTS", "UNOBSERVED",
           "OriginalCertificateProjectionAudit", "audit_original_certificates")
