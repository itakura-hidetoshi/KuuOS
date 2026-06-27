#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    EXTERNAL_HUMAN_REVIEWER,
    MORE_EVIDENCE_REQUIRED,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    REVIEW_SCOPE,
    attestation_digest,
    receipt_digest,
    request_digest,
)
from runtime.kuuos_connection_evidence_review_v0_69 import (
    build_connection_evidence_review_request,
    evaluate_external_evidence_review,
    seal_connection_evidence_review_attestation,
    validate_external_evidence_review_receipt,
)
from runtime.kuuos_connection_evidence_v0_68 import build_connection_evidence_capsule
from scripts.check_kuuos_evidence_v068 import evidence_chain


def review_inputs():
    source, shadow, shadow_receipt, gauge_validation = evidence_chain()
    capsule = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        capsule_id="external-review-evidence-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    request = build_connection_evidence_review_request(
        capsule,
        request_id="external-review-request-v069",
        requested_by="kuuos-governance",
        assigned_reviewer_id="reviewer-v069",
        assigned_reviewer_class=EXTERNAL_HUMAN_REVIEWER,
    )
    return source, shadow, shadow_receipt, gauge_validation, capsule, request


def decide(request, decision):
    return seal_connection_evidence_review_attestation(
        request,
        attestation_id=f"attestation-{decision.lower()}-v069",
        reviewer_id="reviewer-v069",
        reviewer_class=EXTERNAL_HUMAN_REVIEWER,
        decision=decision,
        valid_from_epoch=12,
        valid_through_epoch=18,
    )


def reseal_attestation(attestation, **changes):
    changed = replace(attestation, **changes, attestation_digest="")
    return replace(changed, attestation_digest=attestation_digest(changed))


def reseal_request(request, **changes):
    changed = replace(request, **changes, request_digest="")
    return replace(changed, request_digest=request_digest(changed))


def run_review(
    inputs,
    attestation,
    *,
    current_epoch=15,
    capsule_override=None,
    request_override=None,
):
    source, shadow, shadow_receipt, gauge_validation, capsule, request = inputs
    return evaluate_external_evidence_review(
        capsule if capsule_override is None else capsule_override,
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        request if request_override is None else request_override,
        attestation,
        current_epoch=current_epoch,
    )


def main() -> int:
    inputs = review_inputs()
    capsule, request = inputs[4], inputs[5]
    checks: list[str] = []

    approval = decide(request, APPROVE_EVIDENCE)
    assert approval.production_apply_allowed is False
    assert approval.live_effect_allowed is False
    approved = run_review(inputs, approval)
    assert approved.status == READY
    assert approved.governed_admission_candidate
    assert approved.production_apply_ready is False
    assert approved.review_only
    assert approved.live_effect_performed is False
    assert approved.state_write_performed is False
    assert approved.authority_widened is False
    assert approved.rollback_target_replaced is False
    assert validate_external_evidence_review_receipt(
        approved,
        capsule,
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[3],
        request,
        approval,
        current_epoch=15,
    ) == ()
    checks.append("approve-is-candidate-only")

    rejection = decide(request, REJECT_EVIDENCE)
    rejected = run_review(inputs, rejection)
    assert rejected.status == REJECTED
    assert rejected.governed_admission_candidate is False
    assert rejected.production_apply_ready is False

    more_attestation = decide(request, REQUEST_MORE_EVIDENCE)
    more = run_review(inputs, more_attestation)
    assert more.status == MORE_EVIDENCE_REQUIRED
    assert more.governed_admission_candidate is False
    assert more.production_apply_ready is False
    checks.append("explicit-decisions")

    expired = run_review(inputs, approval, current_epoch=21)
    assert expired.status == BLOCKED
    assert "evidence_capsule_outside_validity_window" in expired.blockers
    checks.append("expired-evidence")

    tampered_capsule = replace(capsule, sample_count=capsule.sample_count + 1)
    tampered = run_review(
        inputs,
        approval,
        capsule_override=tampered_capsule,
    )
    assert tampered.status == BLOCKED
    assert "evidence_capsule_digest_invalid" in tampered.blockers
    checks.append("tampered-evidence")

    identity_mismatch = reseal_attestation(
        approval,
        reviewer_id="reviewer-other",
    )
    identity_blocked = run_review(inputs, identity_mismatch)
    assert identity_blocked.status == BLOCKED
    assert "evidence_review_reviewer_identity_mismatch" in identity_blocked.blockers

    class_mismatch = reseal_attestation(
        approval,
        reviewer_class="unrecognized_reviewer_class",
    )
    class_blocked = run_review(inputs, class_mismatch)
    assert class_blocked.status == BLOCKED
    assert "evidence_review_reviewer_class_mismatch" in class_blocked.blockers
    assert "evidence_review_reviewer_class_invalid" in class_blocked.blockers
    checks.append("reviewer-binding")

    widened = reseal_attestation(
        approval,
        allowed_scopes=(REVIEW_SCOPE, "additional_scope"),
    )
    widened_blocked = run_review(inputs, widened)
    assert widened_blocked.status == BLOCKED
    assert "evidence_review_attestation_scope_invalid" in widened_blocked.blockers
    checks.append("scope-widening")

    rollback_changed = reseal_attestation(
        approval,
        bound_rollback_bundle_digest="replacement-rollback-digest",
    )
    rollback_blocked = run_review(inputs, rollback_changed)
    assert rollback_blocked.status == BLOCKED
    assert "evidence_review_attestation_rollback_binding_mismatch" in rollback_blocked.blockers
    checks.append("rollback-binding")

    oversized_window = reseal_attestation(approval, valid_from_epoch=9)
    window_blocked = run_review(inputs, oversized_window)
    assert window_blocked.status == BLOCKED
    assert "evidence_review_window_exceeds_capsule" in window_blocked.blockers
    checks.append("bounded-window")

    forbidden_permissions = reseal_attestation(
        approval,
        production_apply_allowed=True,
        live_effect_allowed=True,
        state_write_allowed=True,
        authority_widening_allowed=True,
        rollback_replacement_allowed=True,
    )
    permission_blocked = run_review(inputs, forbidden_permissions)
    assert permission_blocked.status == BLOCKED
    assert "evidence_review_production_apply_forbidden" in permission_blocked.blockers
    assert "evidence_review_live_effect_forbidden" in permission_blocked.blockers
    assert "evidence_review_state_write_forbidden" in permission_blocked.blockers
    assert "evidence_review_authority_widening_forbidden" in permission_blocked.blockers
    assert "evidence_review_rollback_replacement_forbidden" in permission_blocked.blockers
    checks.append("permission-boundary")

    digest_tamper = replace(approval, decision=REJECT_EVIDENCE)
    digest_blocked = run_review(inputs, digest_tamper)
    assert digest_blocked.status == BLOCKED
    assert "evidence_review_attestation_digest_invalid" in digest_blocked.blockers
    checks.append("attestation-tamper")

    widened_request = reseal_request(
        request,
        requested_scope="expanded_external_review_scope",
    )
    request_blocked = run_review(
        inputs,
        approval,
        request_override=widened_request,
    )
    assert request_blocked.status == BLOCKED
    assert "evidence_review_request_scope_invalid" in request_blocked.blockers
    assert "evidence_review_attestation_request_binding_mismatch" in request_blocked.blockers
    checks.append("request-binding")

    altered_receipt = replace(
        approved,
        governed_admission_candidate=False,
        receipt_digest="",
    )
    altered_receipt = replace(
        altered_receipt,
        receipt_digest=receipt_digest(altered_receipt),
    )
    receipt_issues = validate_external_evidence_review_receipt(
        altered_receipt,
        capsule,
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[3],
        request,
        approval,
        current_epoch=15,
    )
    assert "evidence_review_receipt_candidate_scope_invalid" in receipt_issues
    checks.append("receipt-consistency")

    print(json.dumps({
        "status": "KUUOS_V0_69_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
