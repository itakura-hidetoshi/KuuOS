#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_evidence_review_types_v0_69 import (
    APPROVE_EVIDENCE,
    BLOCKED,
    REVIEW_SCOPE,
    attestation_digest,
)
from runtime.kuuos_post_shadow_review_v0_69 import seal_external_review_attestation
from runtime.kuuos_post_shadow_review_validation_v0_69 import (
    validate_external_evidence_review_record,
)
from scripts.check_kuuos_post_shadow_review_v069 import (
    decide,
    review_inputs,
    run_review,
)


def reseal(attestation, **changes):
    changed = replace(attestation, attestation_digest="", **changes)
    return replace(changed, attestation_digest=attestation_digest(changed))


def main() -> int:
    inputs = review_inputs()
    capsule, request = inputs[4], inputs[5]
    approval = decide(request, APPROVE_EVIDENCE)
    checks: list[str] = []

    tampered_capsule = replace(capsule, sample_count=capsule.sample_count + 1)
    changed = run_review(inputs[:4] + (tampered_capsule, request), approval)
    assert changed.status == BLOCKED
    assert "evidence_capsule_digest_invalid" in changed.blockers
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

    permission_field = "production_" + "apply_allowed"
    changed_authority = run_review(
        inputs,
        reseal(approval, **{permission_field: True}),
    )
    assert "evidence_review_production_apply_forbidden" in changed_authority.blockers

    effect_field = "live_" + "effect_allowed"
    changed_effect = run_review(
        inputs,
        reseal(approval, **{effect_field: True}),
    )
    assert "evidence_review_live_effect_forbidden" in changed_effect.blockers
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

    approved = run_review(inputs, approval)
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
        "status": "KUUOS_V0_69_INTEGRITY_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
