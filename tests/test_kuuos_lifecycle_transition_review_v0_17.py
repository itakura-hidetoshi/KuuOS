from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    DENIED as SOURCE_DENIED,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    BLOCKED,
    CLEAR,
    REJECTED,
)
from runtime.kuuos_lifecycle_governance_transition_review_v0_17 import (
    artifact_issues,
    make_policy,
)
from tests.kuuos_lifecycle_transition_review_fixture_v0_17 import (
    LifecycleTransitionReviewFixtureV017,
)


class LifecycleTransitionReviewV017Tests(
    LifecycleTransitionReviewFixtureV017
):
    def test_valid_input_is_clear_for_separate_transition_decision(self) -> None:
        artifact = self.evaluate_transition_review()
        self.assertEqual(artifact.status, CLEAR)
        self.assertTrue(artifact.source_post_operation_review_completed)
        self.assertTrue(artifact.transition_review_record_issued)
        self.assertTrue(artifact.transition_review_completed)
        self.assertTrue(artifact.clear_for_transition_decision)
        self.assertTrue(artifact.transition_decision_required_next)
        self.assertFalse(artifact.transition_decision_made)
        self.assertFalse(artifact.lifecycle_transition_performed)
        self.assertFalse(artifact.repository_changed)

    def test_non_reviewed_or_fresh_digest_tampered_source_is_rejected(self) -> None:
        source = self.make_source()
        denied = self.refresh_source_record(
            source[3],
            status=SOURCE_DENIED,
            post_operation_review_completed=False,
            post_operation_review_denied=True,
            lifecycle_transition_review_required_next=False,
            lifecycle_transition_review_route_required_next=False,
            operation_recovery_assessment_required_next=True,
            operation_recovery_assessment_route_required_next=True,
        )
        tampered = self.refresh_source_record(source[3], reason="fresh-digest-tamper")
        for record in (denied, tampered):
            changed = (*source[:3], record, source[4])
            evidence = self.make_transition_evidence(changed)
            review = self.make_transition_review(changed, evidence)
            self.assertEqual(
                self.evaluate_transition_review(changed, evidence, review).status,
                REJECTED,
            )

    def test_source_evidence_and_route_bindings_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(source)
        bad_evidence = self.refresh_evidence(
            evidence,
            source_post_operation_review_record_digest="b" * 64,
        )
        bad_review = self.make_transition_review(source, bad_evidence)
        self.assertEqual(
            self.evaluate_transition_review(
                source, bad_evidence, bad_review
            ).status,
            REJECTED,
        )
        review = self.make_transition_review(source, evidence)
        for changed in (
            self.refresh_review(
                review,
                transition_review_evidence_digest="e" * 64,
            ),
            self.refresh_review(
                review,
                transition_review_route_digest="r" * 64,
            ),
        ):
            self.assertEqual(
                self.evaluate_transition_review(
                    source, evidence, changed
                ).status,
                REJECTED,
            )

    def test_reviewer_policy_and_role_separation_are_enforced(self) -> None:
        source = self.make_source()
        for reviewer_id in (
            "other-reviewer",
            source[0].post_operation_reviewer_id,
            source[0].source_completion_reviewer_id,
            source[0].source_operator_id,
            self.transition_decision_maker_id,
        ):
            evidence = self.make_transition_evidence(
                source, transition_reviewer_id=reviewer_id
            )
            review = self.make_transition_review(
                source, evidence, transition_reviewer_id=reviewer_id
            )
            self.assertEqual(
                self.evaluate_transition_review(
                    source, evidence, review
                ).status,
                REJECTED,
            )
        evidence = self.make_transition_evidence(
            source,
            transition_reviewer_organization_id=(
                source[1].post_operation_reviewer_organization_id
            ),
        )
        review = self.make_transition_review(
            source,
            evidence,
            transition_reviewer_organization_id=(
                source[1].post_operation_reviewer_organization_id
            ),
        )
        self.assertEqual(
            self.evaluate_transition_review(source, evidence, review).status,
            REJECTED,
        )

    def test_objective_transition_kind_and_decision_maker_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(source)
        invalid_objective = self.make_transition_review(
            source, evidence, objective="INVALID"
        )
        self.assertEqual(
            self.evaluate_transition_review(
                source, evidence, invalid_objective
            ).status,
            REJECTED,
        )
        invalid_kind_evidence = self.make_transition_evidence(
            source, proposed_transition_kind="INVALID"
        )
        invalid_kind_review = self.make_transition_review(
            source,
            invalid_kind_evidence,
            proposed_transition_kind="INVALID",
        )
        self.assertEqual(
            self.evaluate_transition_review(
                source, invalid_kind_evidence, invalid_kind_review
            ).status,
            REJECTED,
        )
        other_maker_evidence = self.make_transition_evidence(
            source, transition_decision_maker_id="other-maker"
        )
        other_maker_review = self.make_transition_review(
            source,
            other_maker_evidence,
            transition_decision_maker_id="other-maker",
        )
        self.assertEqual(
            self.evaluate_transition_review(
                source, other_maker_evidence, other_maker_review
            ).status,
            REJECTED,
        )

    def test_governance_and_substantive_failures_block(self) -> None:
        source = self.make_source()
        changes_list = (
            {"transition_reviewer_mandate_verified": False},
            {"transition_reviewer_qualification_verified": False},
            {"transition_reviewer_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"review_ready": False},
            {"transition_basis_sufficient": False},
            {"necessity_verified": False},
            {"proportionality_verified": False},
            {"reversibility_or_exception_justified": False},
            {"dependencies_cleared": False},
            {"authority_continuity_verified": False},
            {"transition_state_compatible": False},
            {"stakeholder_impact_acceptable": False},
            {"legal_policy_compliant": False},
            {"appeal_route_available": False},
            {"dissent_route_available": False},
            {"minority_opinion_recorded": False},
            {"unresolved_anomaly_present": True},
            {"recovery_required": True},
            {"institutional_hold_active": True},
            {"emergency_state_active": True},
        )
        for changes in changes_list:
            evidence = self.make_transition_evidence(source, **changes)
            review = self.make_transition_review(source, evidence)
            artifact = self.evaluate_transition_review(source, evidence, review)
            self.assertEqual(artifact.status, BLOCKED)
            self.assertTrue(artifact.transition_reassessment_required_next)
            self.assertFalse(artifact.transition_decision_required_next)
            self.assertFalse(artifact.lifecycle_transition_performed)

    def test_scope_and_effect_changes_are_rejected(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(source)
        for changes in (
            {"operation_scope_items": ()},
            {"protected_resource_ids": ("subject-runtime-state",)},
            {"step_result_digests": {"unknown-step": "u" * 64}},
            {"external_operation_performed": True},
            {"repository_changed": True},
        ):
            changed = self.refresh_evidence(evidence, **changes)
            review = self.make_transition_review(source, changed)
            self.assertEqual(
                self.evaluate_transition_review(
                    source, changed, review
                ).status,
                REJECTED,
            )

    def test_target_resource_policy_is_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(source)
        review = self.make_transition_review(source, evidence)
        restrictive = make_policy(
            "restrictive-transition-review-policy-v0-17",
            allowed_transition_reviewer_ids=(self.transition_reviewer_id,),
            allowed_transition_reviewer_organization_ids=(
                self.transition_reviewer_organization_id,
            ),
            allowed_transition_decision_maker_ids=(
                self.transition_decision_maker_id,
            ),
            allowed_target_resource_ids=("other-resource",),
            allowed_transition_kinds=(self.proposed_transition_kind,),
            max_review_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_review_expiry_seconds=120,
            max_decision_delay_seconds=180,
            max_scope_items=8,
        )
        self.assertEqual(
            self.evaluate_transition_review(
                source, evidence, review, restrictive
            ).status,
            REJECTED,
        )

    def test_review_freshness_expiry_and_decision_deadline_are_enforced(self) -> None:
        source = self.make_source()
        late = source[0].reviewed_at_epoch_seconds + 121
        late_evidence = self.make_transition_evidence(
            source,
            review_requested_at_epoch_seconds=late,
            captured_at_epoch_seconds=late,
            reviewed_at_epoch_seconds=late,
            review_expiry_at_epoch_seconds=late + 60,
            transition_decision_deadline_at_epoch_seconds=late + 120,
        )
        late_review = self.make_transition_review(
            source,
            late_evidence,
            review_requested_at_epoch_seconds=late,
            reviewed_at_epoch_seconds=late,
            review_expiry_at_epoch_seconds=late + 60,
            transition_decision_deadline_at_epoch_seconds=late + 120,
        )
        self.assertEqual(
            self.evaluate_transition_review(
                source, late_evidence, late_review
            ).status,
            REJECTED,
        )
        evidence = self.make_transition_evidence(source)
        for changes in (
            {"captured_at_epoch_seconds": self.reviewed_at - 121},
            {"review_expiry_at_epoch_seconds": self.reviewed_at + 121},
            {
                "transition_decision_deadline_at_epoch_seconds": (
                    self.reviewed_at + 181
                )
            },
        ):
            changed = self.refresh_evidence(evidence, **changes)
            review = self.make_transition_review(
                source,
                changed,
                review_expiry_at_epoch_seconds=(
                    changed.review_expiry_at_epoch_seconds
                ),
                transition_decision_deadline_at_epoch_seconds=(
                    changed.transition_decision_deadline_at_epoch_seconds
                ),
            )
            self.assertEqual(
                self.evaluate_transition_review(
                    source, changed, review
                ).status,
                REJECTED,
            )

    def test_blocked_and_rejected_record_semantics(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(
            source, necessity_verified=False
        )
        review = self.make_transition_review(source, evidence)
        blocked = self.evaluate_transition_review(source, evidence, review)
        self.assertEqual(blocked.status, BLOCKED)
        self.assertTrue(blocked.transition_review_record_issued)
        self.assertTrue(blocked.transition_review_completed)
        self.assertTrue(blocked.transition_review_blocked)
        evidence = self.make_transition_evidence(source)
        review = self.make_transition_review(source, evidence, objective="INVALID")
        rejected = self.evaluate_transition_review(source, evidence, review)
        self.assertEqual(rejected.status, REJECTED)
        self.assertFalse(rejected.transition_review_record_issued)
        self.assertFalse(rejected.transition_review_completed)

    def test_determinism_record_integrity_and_effect_boundary(self) -> None:
        source = self.make_source()
        evidence = self.make_transition_evidence(source)
        review = self.make_transition_review(source, evidence)
        left = self.evaluate_transition_review(source, evidence, review)
        right = self.evaluate_transition_review(source, evidence, review)
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "transition_review_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(source, evidence, review),
            ),
        )
        for value in (
            left.transition_decision_made,
            left.lifecycle_transition_performed,
            left.authority_changed,
            left.quiescence_state_changed,
            left.terminal_state_changed,
            left.terminal_marker_written,
            left.resource_removed,
            left.external_operation_performed,
            left.repository_changed,
        ):
            self.assertFalse(value)
