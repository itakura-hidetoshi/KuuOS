from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import BLOCKED as SOURCE_BLOCKED
from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED as SOURCE_REJECTED
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import BLOCKED, CLEAR, REJECTED
from runtime.kuuos_lifecycle_governance_decision_review_v0_11 import (
    artifact_issues,
    make_policy,
)
from tests.kuuos_lifecycle_decision_review_fixture_v0_11 import (
    LifecycleDecisionReviewFixtureV011,
)


class LifecycleDecisionReviewV011Tests(LifecycleDecisionReviewFixtureV011):
    def audit_matrix(self) -> dict[str, bool]:
        checks: dict[str, bool] = {}
        source = self.make_source()
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(source, evidence)
        clear = self.evaluate_review(source, evidence, review)
        checks["valid_input_produces_clear"] = clear.status == CLEAR

        blocked_source_record = self.refresh_source_record(
            source[3],
            status=SOURCE_BLOCKED,
            bounded_request_issued=False,
            ready_for_decision_review=False,
            decision_review_required_next=False,
        )
        blocked_source = (*source[:3], blocked_source_record, source[4])
        blocked_evidence = self.make_review_evidence(blocked_source)
        blocked_review = self.make_review_submission(blocked_source, blocked_evidence)
        blocked_source_rejected = (
            self.evaluate_review(blocked_source, blocked_evidence, blocked_review).status
            == REJECTED
        )

        rejected_source_record = self.refresh_source_record(
            source[3],
            status=SOURCE_REJECTED,
            request_record_issued=False,
            bounded_request_issued=False,
            ready_for_decision_review=False,
            decision_review_required_next=False,
        )
        rejected_source = (*source[:3], rejected_source_record, source[4])
        rejected_evidence = self.make_review_evidence(rejected_source)
        rejected_review = self.make_review_submission(rejected_source, rejected_evidence)
        rejected_source_rejected = (
            self.evaluate_review(rejected_source, rejected_evidence, rejected_review).status
            == REJECTED
        )
        checks["non_issued_source_rejected"] = (
            blocked_source_rejected and rejected_source_rejected
        )

        tampered_record = self.refresh_source_record(source[3], reason="fresh-digest-tamper")
        tampered_source = (*source[:3], tampered_record, source[4])
        tampered_evidence = self.make_review_evidence(tampered_source)
        tampered_review = self.make_review_submission(tampered_source, tampered_evidence)
        checks["fresh_digest_source_tamper_detected"] = (
            self.evaluate_review(tampered_source, tampered_evidence, tampered_review).status
            == REJECTED
        )

        source_binding_evidence = self.refresh_evidence(
            evidence, source_bounded_request_record_digest="x" * 64
        )
        source_binding_review = self.make_review_submission(source, source_binding_evidence)
        checks["source_binding_enforced"] = (
            self.evaluate_review(source, source_binding_evidence, source_binding_review).status
            == REJECTED
        )

        evidence_binding_review = self.refresh_review(review, review_evidence_digest="y" * 64)
        checks["evidence_digest_binding_enforced"] = (
            self.evaluate_review(source, evidence, evidence_binding_review).status == REJECTED
        )

        unknown_evidence = self.make_review_evidence(
            source, decision_reviewer_id="unknown-reviewer"
        )
        unknown_review = self.make_review_submission(
            source, unknown_evidence, decision_reviewer_id="unknown-reviewer"
        )
        checks["reviewer_id_policy_enforced"] = (
            self.evaluate_review(source, unknown_evidence, unknown_review).status == REJECTED
        )

        org_evidence = self.make_review_evidence(
            source, decision_reviewer_organization_id="unknown-organization"
        )
        org_review = self.make_review_submission(
            source,
            org_evidence,
            decision_reviewer_organization_id="unknown-organization",
        )
        checks["reviewer_organization_policy_enforced"] = (
            self.evaluate_review(source, org_evidence, org_review).status == REJECTED
        )

        objective_review = self.make_review_submission(
            source, evidence, objective="AUTHORIZE_OPERATION"
        )
        checks["objective_policy_enforced"] = (
            self.evaluate_review(source, evidence, objective_review).status == REJECTED
        )

        prior_id = sorted(
            item
            for item in self.policy.allowed_decision_reviewer_ids
            if item not in {
                self.reviewer_id,
                source[0].requester_id,
                source[0].decision_authority_id,
                source[0].future_operator_id,
            }
        )[0]
        prior_evidence = self.make_review_evidence(source, decision_reviewer_id=prior_id)
        prior_review = self.make_review_submission(
            source, prior_evidence, decision_reviewer_id=prior_id
        )
        checks["prior_chain_independence_enforced"] = (
            self.evaluate_review(source, prior_evidence, prior_review).status == REJECTED
        )

        requester_evidence = self.make_review_evidence(
            source, decision_reviewer_id=source[0].requester_id
        )
        requester_review = self.make_review_submission(
            source, requester_evidence, decision_reviewer_id=source[0].requester_id
        )
        checks["requester_reviewer_separation_enforced"] = (
            self.evaluate_review(source, requester_evidence, requester_review).status
            == REJECTED
        )

        authority_evidence = self.make_review_evidence(
            source, decision_reviewer_id=source[0].decision_authority_id
        )
        authority_review = self.make_review_submission(
            source,
            authority_evidence,
            decision_reviewer_id=source[0].decision_authority_id,
        )
        checks["reviewer_authorization_maker_separation_enforced"] = (
            self.evaluate_review(source, authority_evidence, authority_review).status
            == REJECTED
        )

        operator_evidence = self.make_review_evidence(
            source, decision_reviewer_id=source[0].future_operator_id
        )
        operator_review = self.make_review_submission(
            source, operator_evidence, decision_reviewer_id=source[0].future_operator_id
        )
        checks["reviewer_operator_separation_enforced"] = (
            self.evaluate_review(source, operator_evidence, operator_review).status
            == REJECTED
        )

        separation_evidence = self.refresh_evidence(
            evidence, authorization_decision_maker_id=source[0].future_operator_id
        )
        separation_review = self.refresh_review(
            review, authorization_decision_maker_id=source[0].future_operator_id,
            review_evidence_digest=separation_evidence.evidence_digest,
        )
        checks["authorization_maker_operator_separation_enforced"] = (
            self.evaluate_review(source, separation_evidence, separation_review).status
            == REJECTED
        )

        qualification_evidence = self.make_review_evidence(
            source, reviewer_qualification_verified=False
        )
        qualification_review = self.make_review_submission(source, qualification_evidence)
        checks["qualification_failure_blocks"] = (
            self.evaluate_review(source, qualification_evidence, qualification_review).status
            == BLOCKED
        )

        disclosure_evidence = self.make_review_evidence(
            source, conflict_disclosure_complete=False
        )
        disclosure_review = self.make_review_submission(source, disclosure_evidence)
        checks["conflict_disclosure_failure_blocks"] = (
            self.evaluate_review(source, disclosure_evidence, disclosure_review).status
            == BLOCKED
        )

        conflict_evidence = self.make_review_evidence(source, material_conflict_present=True)
        conflict_review = self.make_review_submission(source, conflict_evidence)
        checks["material_conflict_blocks"] = (
            self.evaluate_review(source, conflict_evidence, conflict_review).status == BLOCKED
        )

        restrictive_policy = make_policy(
            "restrictive-lifecycle-decision-review-policy-v0-11",
            allowed_decision_reviewer_ids=self.policy.allowed_decision_reviewer_ids,
            allowed_decision_reviewer_organization_ids=(self.reviewer_organization_id,),
            allowed_authorization_decision_maker_ids=(
                source[0].decision_authority_id,
                source[0].future_operator_id,
            ),
            allowed_target_resource_ids=self.policy.allowed_target_resource_ids,
            max_review_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_review_expiry_seconds=300,
            max_operation_window_seconds=1,
            max_scope_items=8,
        )
        checks["package_safety_failure_blocks"] = (
            self.evaluate_review(source, evidence, review, restrictive_policy).status == BLOCKED
        )

        expired_evidence = self.make_review_evidence(
            source,
            review_requested_at_epoch_seconds=source[1].request_expiry_at_epoch_seconds + 1,
            captured_at_epoch_seconds=source[1].request_expiry_at_epoch_seconds + 2,
            completed_at_epoch_seconds=source[1].request_expiry_at_epoch_seconds + 3,
            review_expiry_at_epoch_seconds=source[1].request_expiry_at_epoch_seconds + 4,
            authorization_decision_deadline_at_epoch_seconds=(
                source[1].request_expiry_at_epoch_seconds + 4
            ),
        )
        expired_review = self.make_review_submission(
            source,
            expired_evidence,
            review_requested_at_epoch_seconds=expired_evidence.review_requested_at_epoch_seconds,
            completed_at_epoch_seconds=expired_evidence.completed_at_epoch_seconds,
            authorization_decision_deadline_at_epoch_seconds=(
                expired_evidence.authorization_decision_deadline_at_epoch_seconds
            ),
        )
        checks["temporal_boundaries_enforced"] = (
            self.evaluate_review(source, expired_evidence, expired_review).status == REJECTED
        )

        blocked = self.evaluate_review(source, qualification_evidence, qualification_review)
        rejected = self.evaluate_review(blocked_source, blocked_evidence, blocked_review)
        effect_names = (
            "authorization_decision_made",
            "operation_approved",
            "operation_started",
            "operation_completed",
            "authority_changed",
            "quiescence_state_changed",
            "terminal_state_changed",
            "terminal_marker_written",
            "resource_removed",
            "external_operation_performed",
            "repository_changed",
        )
        checks["all_statuses_preserve_read_only_boundary"] = all(
            item.lifecycle_read_only
            and not any(getattr(item, name) for name in effect_names)
            for item in (clear, blocked, rejected)
        )

        same = self.evaluate_review(source, evidence, review)
        checks["determinism_and_record_integrity"] = (
            clear.to_dict() == same.to_dict()
            and not artifact_issues(clear, *self.artifact_args(source, evidence, review))
        )
        return checks

    def test_complete_audit_matrix(self) -> None:
        checks = self.audit_matrix()
        failures = sorted(name for name, passed in checks.items() if not passed)
        self.assertFalse(failures, f"failed lifecycle decision review checks: {failures}")
        self.assertEqual(len(checks), 20)


if __name__ == "__main__":
    import unittest

    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
