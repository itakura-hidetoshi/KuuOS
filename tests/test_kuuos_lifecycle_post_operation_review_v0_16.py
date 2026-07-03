from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    DENIED as SOURCE_DENIED,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    DENIED,
    REJECTED,
    REVIEWED,
)
from runtime.kuuos_lifecycle_governance_post_operation_review_v0_16 import (
    artifact_issues,
    make_policy,
)
from tests.kuuos_lifecycle_post_operation_review_fixture_v0_16 import (
    LifecyclePostOperationReviewFixtureV016,
)


class LifecyclePostOperationReviewV016Tests(
    LifecyclePostOperationReviewFixtureV016
):
    def test_valid_input_reviews_completed_operation(self) -> None:
        artifact = self.evaluate_review()
        self.assertEqual(artifact.status, REVIEWED)
        self.assertTrue(artifact.operation_completed)
        self.assertTrue(artifact.post_operation_review_record_issued)
        self.assertTrue(artifact.post_operation_review_decision_made)
        self.assertTrue(artifact.post_operation_review_completed)
        self.assertTrue(
            artifact.lifecycle_transition_review_required_next
        )
        self.assertFalse(
            artifact.operation_recovery_assessment_required_next
        )
        self.assertFalse(artifact.authority_changed)
        self.assertFalse(artifact.repository_changed)

    def test_non_completed_or_fresh_digest_tampered_source_is_rejected(
        self,
    ) -> None:
        source = self.make_source()
        denied = self.refresh_source_record(
            source[3],
            status=SOURCE_DENIED,
            operation_completed=False,
            operation_completion_denied=True,
            post_operation_review_required_next=False,
            post_operation_review_route_required_next=False,
            operation_recovery_required_next=True,
            operation_recovery_route_required_next=True,
        )
        tampered = self.refresh_source_record(
            source[3], reason="fresh-digest-tamper"
        )
        for record in (denied, tampered):
            changed = (*source[:3], record, source[4])
            evidence = self.make_review_evidence(changed)
            review = self.make_review_submission(changed, evidence)
            self.assertEqual(
                self.evaluate_review(
                    changed, evidence, review
                ).status,
                REJECTED,
            )

    def test_source_evidence_and_route_bindings_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        bad_source = self.make_review_evidence(
            source,
            source_operation_completion_record_digest="b" * 64,
        )
        bad_review = self.make_review_submission(
            source, bad_source
        )
        self.assertEqual(
            self.evaluate_review(
                source, bad_source, bad_review
            ).status,
            REJECTED,
        )
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(source, evidence)
        for changed in (
            self.refresh_review(
                review,
                post_operation_review_evidence_digest="e" * 64,
            ),
            self.refresh_review(
                review,
                post_operation_review_route_digest="r" * 64,
            ),
        ):
            self.assertEqual(
                self.evaluate_review(
                    source, evidence, changed
                ).status,
                REJECTED,
            )

    def test_reviewer_policy_and_role_separation_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        for reviewer_id in (
            "other-reviewer",
            source[0].completion_reviewer_id,
            source[0].source_operator_id,
            source[0].source_operation_approver_id,
        ):
            evidence = self.make_review_evidence(
                source, post_operation_reviewer_id=reviewer_id
            )
            review = self.make_review_submission(
                source,
                evidence,
                post_operation_reviewer_id=reviewer_id,
            )
            self.assertEqual(
                self.evaluate_review(
                    source, evidence, review
                ).status,
                REJECTED,
            )
        evidence = self.make_review_evidence(
            source,
            post_operation_reviewer_organization_id=(
                source[0].completion_reviewer_organization_id
            ),
        )
        review = self.make_review_submission(
            source,
            evidence,
            post_operation_reviewer_organization_id=(
                source[0].completion_reviewer_organization_id
            ),
        )
        self.assertEqual(
            self.evaluate_review(
                source, evidence, review
            ).status,
            REJECTED,
        )

    def test_objective_is_structurally_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(
            source, evidence, objective="INVALID"
        )
        self.assertEqual(
            self.evaluate_review(source, evidence, review).status,
            REJECTED,
        )

    def test_reviewer_authority_and_readiness_failures_deny(
        self,
    ) -> None:
        source = self.make_source()
        for changes in (
            {"post_operation_reviewer_mandate_verified": False},
            {"post_operation_reviewer_qualification_verified": False},
            {"post_operation_reviewer_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"review_ready": False},
        ):
            evidence = self.make_review_evidence(
                source, **changes
            )
            review = self.make_review_submission(
                source, evidence
            )
            self.assertEqual(
                self.evaluate_review(
                    source, evidence, review
                ).status,
                DENIED,
            )

    def test_outcome_anomaly_and_recovery_findings_deny(
        self,
    ) -> None:
        source = self.make_source()
        changes_list = (
            {"intended_result_matches_observed": False},
            {"target_post_state_verified": False},
            {"collateral_effects_absent": False},
            {"protected_resources_intact": False},
            {"protected_core_intact": False},
            {"monitoring_evidence_sufficient": False},
            {"completion_evidence_sufficient": False},
            {"unresolved_anomaly_present": True},
            {"rollback_required": True},
            {"recovery_required": True},
        )
        for changes in changes_list:
            evidence = self.make_review_evidence(
                source, **changes
            )
            review = self.make_review_submission(
                source, evidence
            )
            artifact = self.evaluate_review(
                source, evidence, review
            )
            self.assertEqual(artifact.status, DENIED)
            self.assertTrue(
                artifact.operation_recovery_assessment_required_next
            )
            self.assertFalse(
                artifact.post_operation_review_completed
            )

    def test_scope_and_effect_changes_are_rejected(self) -> None:
        source = self.make_source()
        for changes in (
            {"operation_scope_items": ()},
            {
                "protected_resource_ids": (
                    "subject-runtime-state",
                )
            },
            {"step_result_digests": {"unknown-step": "u" * 64}},
            {"external_operation_performed": True},
            {"repository_changed": True},
        ):
            evidence = self.make_review_evidence(
                source, **changes
            )
            review = self.make_review_submission(
                source, evidence
            )
            self.assertEqual(
                self.evaluate_review(
                    source, evidence, review
                ).status,
                REJECTED,
            )

    def test_target_resource_policy_is_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(source, evidence)
        restrictive = make_policy(
            "restrictive-post-operation-review-policy-v0-16",
            allowed_post_operation_reviewer_ids=(
                self.post_operation_reviewer_id,
            ),
            allowed_post_operation_reviewer_organization_ids=(
                self.post_operation_reviewer_organization_id,
            ),
            allowed_target_resource_ids=("other-resource",),
            max_review_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_scope_items=8,
        )
        self.assertEqual(
            self.evaluate_review(
                source, evidence, review, restrictive
            ).status,
            REJECTED,
        )

    def test_review_delay_and_evidence_freshness_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        late = (
            source[0].completed_at_epoch_seconds
            + self.policy.max_review_delay_seconds
            + 1
        )
        evidence = self.make_review_evidence(
            source,
            review_requested_at_epoch_seconds=late,
            captured_at_epoch_seconds=late,
            reviewed_at_epoch_seconds=late,
        )
        review = self.make_review_submission(
            source,
            evidence,
            review_requested_at_epoch_seconds=late,
            reviewed_at_epoch_seconds=late,
        )
        self.assertEqual(
            self.evaluate_review(source, evidence, review).status,
            REJECTED,
        )
        stale_captured = (
            self.reviewed_at
            - self.policy.max_evidence_age_seconds
            - 1
        )
        evidence = self.make_review_evidence(
            source,
            review_requested_at_epoch_seconds=stale_captured,
            captured_at_epoch_seconds=stale_captured,
        )
        review = self.make_review_submission(
            source,
            evidence,
            review_requested_at_epoch_seconds=stale_captured,
        )
        self.assertEqual(
            self.evaluate_review(source, evidence, review).status,
            REJECTED,
        )

    def test_denied_and_rejected_record_semantics(self) -> None:
        source = self.make_source()
        evidence = self.make_review_evidence(
            source, review_ready=False
        )
        review = self.make_review_submission(source, evidence)
        denied = self.evaluate_review(source, evidence, review)
        self.assertEqual(denied.status, DENIED)
        self.assertTrue(
            denied.post_operation_review_record_issued
        )
        self.assertFalse(
            denied.post_operation_review_completed
        )
        self.assertTrue(
            denied.operation_recovery_assessment_required_next
        )
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(
            source, evidence, objective="INVALID"
        )
        rejected = self.evaluate_review(
            source, evidence, review
        )
        self.assertEqual(rejected.status, REJECTED)
        self.assertFalse(
            rejected.post_operation_review_record_issued
        )
        self.assertFalse(
            rejected.post_operation_review_completed
        )

    def test_determinism_record_integrity_and_later_effect_boundary(
        self,
    ) -> None:
        source = self.make_source()
        evidence = self.make_review_evidence(source)
        review = self.make_review_submission(source, evidence)
        left = self.evaluate_review(source, evidence, review)
        right = self.evaluate_review(source, evidence, review)
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "post_operation_review_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(source, evidence, review),
            ),
        )
        self.assertTrue(left.operation_completed)
        for value in (
            left.authority_changed,
            left.quiescence_state_changed,
            left.terminal_state_changed,
            left.terminal_marker_written,
            left.resource_removed,
            left.external_operation_performed,
            left.repository_changed,
        ):
            self.assertFalse(value)
