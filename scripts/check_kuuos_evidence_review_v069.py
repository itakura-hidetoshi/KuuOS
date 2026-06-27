#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_evidence_review_attestation_v0_69 import (
    attestation_digest,
)
from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    MORE_EVIDENCE_REQUIRED,
    READY,
    REJECT_EVIDENCE,
    REJECTED,
    REQUEST_MORE_EVIDENCE,
    REVIEW_SCOPE,
)
from runtime.kuuos_connection_evidence_review_v0_69 import (
    evaluate_external_evidence_review,
)
from runtime.kuuos_connection_evidence_review_validation_v0_69 import (
    validate_external_evidence_review_record,
)
from runtime.kuuos_connection_evidence_v0_68 import build_connection_evidence_capsule
from runtime.kuuos_connection_external_review_v0_69 import (
    build_external_review_request,
    seal_external_review_attestation,
)
from scripts.check_kuuos_evidence_v068 import evidence_chain


def review_inputs():
    source, shadow, shadow_record, gauge_validation = evidence_chain()
    capsule = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_record,
        gauge_validation,
        capsule_id="external-review-evidence-v069",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    request = build_external_review_request(
        capsule,
        request_id="external-review-request-v069",
        requested_by="kuuos-governance",
        assigned_reviewer_id="reviewer-v069",
    )
    return source, shadow, shadow_record, gauge_validation, capsule, request


def decide(request, decision):
    return seal_external_review_attestation(
        request,
        attestation_id=f"attestation-{decision.lower()}-v069",
        reviewer_id="reviewer-v069",
        decision=decision,
        valid_from_epoch=12,
        valid_through_epoch=18,
    )


def reseal(attestation, **changes):
    changed = replace(attestation, attestation_digest="", **changes)
    return replace(changed, attestation_digest=attestation_digest(changed))


def run_review(inputs, attestation, current_epoch=15):
    source, shadow, shadow_record, gauge_validation, capsule, request = inputs
    return evaluate_external_evidence_review(
        capsule,
        source,
        shadow,
        shadow_record,
        gauge_validation,
        request,
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
    assert approved.review_only
    assert approved.live_effect_allowed is False
    assert approved.state_write_performed is False
    assert approved.authority_widened is False
    assert approved.rollback_target_replaced is False
    assert validate_external_evidence_review_record(
        approved,
        capsule,
        request,
        approval,
        current_epoch=15,
    ) == ()
    checks.append("approve-is-candidate-only")

    rejection = decide(request, REJECT_EVIDENCE)
    assert rejection.production_apply_allowed is False
    assert rejection.live_effect_allowed is False
    rejected = run_review(inputs, rejection)
    assert rejected.status == REJECTED
    assert rejected.governed_admission_candidate is False

    more_attestation = decide(request, REQUEST_MORE_EVIDENCE)
    assert more_attestation.production_apply_allowed is False
    assert more_attestation.live_effect_allowed is False
    more = run_review(inputs, more_attestation)
    assert more.status == MORE_EVIDENCE_REQUIRED
    assert more.governed_admission_candidate is False
    checks.append("explicit-decisions")

    expired = run_review(inputs, approval, current_epoch=21)
    assert expired.status == BLOCKED
    assert "evidence_capsule_outside_validity_window" in expired.blockers
    checks.append("expired-evidence")

    tampered_capsule = replace(capsule, sample_count=capsule.sample_count + 1)
    tampered_inputs = inputs[:4] + (tampered_capsule, request)
    tampered = run_review(tampered_inputs, approval)
    assert tampered.status == BLOCKED
    assert "evidence_capsule_digest_invalid" in tampered.blockers
    checks.append("tampered-evidence")

    wrong_reviewer = run_review(
        inputs,
        reseal(approval, reviewer_id="other-reviewer"),
    )
    assert "evidence_review_reviewer_identity_mismatch" in wrong_reviewer.blockers

    wider_scope = run_review(
        inputs,
        reseal(approval, allowed_scopes=(REVIEW_SCOPE, "widened-scope")),
    )
    assert "evidence_review_attestation_scope_invalid" in wider_scope.blockers

    changed_rollback = run_review(
        inputs,
        reseal(approval, bound_rollback_bundle_digest="changed-rollback"),
    )
    assert "evidence_review_attestation_digest_chain_mismatch" in changed_rollback.blockers
    checks.append("identity-scope-rollback-bindings")

    permission_tamper = run_review(
        inputs,
        reseal(approval, production_apply_allowed=True),
    )
    assert "evidence_review_production_apply_forbidden" in permission_tamper.blockers

    effect_tamper = run_review(
        inputs,
        reseal(approval, live_effect_allowed=True),
    )
    assert "evidence_review_live_effect_forbidden" in effect_tamper.blockers
    checks.append("no-live-authority")

    invalid_window = seal_external_review_attestation(
        request,
        attestation_id="invalid-window-v069",
        reviewer_id="reviewer-v069",
        decision=APPROVE_EVIDENCE,
        valid_from_epoch=20,
        valid_through_epoch=10,
    )
    invalid = run_review(inputs, invalid_window)
    assert "evidence_review_validity_window_invalid" in invalid.blockers
    checks.append("finite-window")

    altered_record = replace(
        approved,
        rollback_bundle_digest="tampered-record-rollback",
    )
    record_issues = validate_external_evidence_review_record(
        altered_record,
        capsule,
        request,
        approval,
        current_epoch=15,
    )
    assert "evidence_review_record_digest_invalid" in record_issues
    assert "evidence_review_record_digest_chain_mismatch" in record_issues
    checks.append("immutable-record")

    print(json.dumps({
        "status": "KUUOS_V0_69_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
