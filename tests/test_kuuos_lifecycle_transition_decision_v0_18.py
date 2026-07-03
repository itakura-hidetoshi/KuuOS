from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_governance_transition_decision_v0_18 import (
    artifact_issues,
    make_state,
    make_transition_rule,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    APPROVED,
    DENIED,
    REJECTED,
    lifecycle_state_digest,
    transition_rule_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import BLOCKED as SOURCE_BLOCKED
from tests.kuuos_lifecycle_transition_decision_fixture_v0_18 import (
    LifecycleTransitionDecisionFixtureV018,
)


class LifecycleTransitionDecisionV018Tests(
    LifecycleTransitionDecisionFixtureV018
):
    def test_valid_decision_is_approved_for_separate_preparation(self) -> None:
        artifact = self.evaluate_decision()
        self.assertEqual(artifact.status, APPROVED)
        self.assertTrue(artifact.source_transition_review_completed)
        self.assertTrue(artifact.transition_decision_record_issued)
        self.assertTrue(artifact.transition_decision_made)
        self.assertTrue(artifact.transition_approved_for_preparation)
        self.assertTrue(artifact.transition_preparation_required_next)
        self.assertFalse(artifact.lifecycle_transition_prepared)
        self.assertFalse(artifact.lifecycle_transition_performed)

    def test_policy_denial_issues_valid_record_without_preparation(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source, decision_approved=False)
        decision = self.make_decision(source, evidence)
        artifact = self.evaluate_decision(source, evidence, decision)
        self.assertEqual(artifact.status, DENIED)
        self.assertTrue(artifact.transition_decision_record_issued)
        self.assertTrue(artifact.transition_decision_made)
        self.assertTrue(artifact.transition_denied)
        self.assertTrue(artifact.transition_appeal_or_reconsideration_available)
        self.assertFalse(artifact.transition_preparation_required_next)

    def test_non_clear_or_fresh_digest_tampered_source_is_rejected(self) -> None:
        source = self.make_source()
        blocked = self.refresh_source_record(
            source[3],
            status=SOURCE_BLOCKED,
            clear_for_transition_decision=False,
            transition_review_blocked=True,
            transition_decision_required_next=False,
            transition_decision_route_required_next=False,
            transition_reassessment_required_next=True,
            transition_reassessment_route_required_next=True,
        )
        tampered = self.refresh_source_record(source[3], reason="fresh-digest-tamper")
        for record in (blocked, tampered):
            changed = (*source[:3], record, source[4])
            evidence = self.make_decision_evidence(changed)
            decision = self.make_decision(changed, evidence)
            self.assertEqual(
                self.evaluate_decision(changed, evidence, decision).status,
                REJECTED,
            )

    def test_stale_current_state_is_rejected(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source)
        stale = make_state(
            authority_state="AUTHORIZED",
            quiescence_state="ACTIVE",
            terminal_state="NON_TERMINAL",
            resource_state="INTACT",
            state_revision=6,
        )
        changed = self.refresh_evidence(evidence, current_state=stale)
        decision = self.make_decision(source, changed)
        artifact = self.evaluate_decision(source, changed, decision)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks["current_state_matches_reviewed_state"])

    def test_target_state_and_allowed_relation_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source)
        other_target = make_state(
            authority_state="AUTHORIZED",
            quiescence_state="QUIESCENT",
            terminal_state="NON_TERMINAL",
            resource_state="LIMITED",
            state_revision=8,
        )
        changed = self.refresh_evidence(evidence, target_state=other_target)
        decision = self.make_decision(source, changed)
        self.assertEqual(
            self.evaluate_decision(source, changed, decision).status,
            REJECTED,
        )
        inactive_rule = replace(self.transition_rule, active=False, rule_digest="")
        inactive_rule = replace(
            inactive_rule, rule_digest=transition_rule_digest(inactive_rule)
        )
        changed = self.refresh_evidence(evidence, transition_rule=inactive_rule)
        decision = self.make_decision(source, changed)
        artifact = self.evaluate_decision(source, changed, decision)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks["allowed_transition_relation_valid"])

    def test_non_advancing_revision_is_rejected(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source)
        target = replace(self.target_state, state_revision=7, state_digest="")
        target = replace(target, state_digest=lifecycle_state_digest(target))
        rule = make_transition_rule(
            rule_id="non-advancing-rule",
            current_state=self.current_state,
            transition_kind=self.upstream.proposed_transition_kind,
            target_state=target,
            policy_basis_digest="p" * 64,
        )
        changed = self.refresh_evidence(
            evidence, target_state=target, transition_rule=rule
        )
        decision = self.make_decision(source, changed)
        artifact = self.evaluate_decision(source, changed, decision)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks["allowed_transition_relation_valid"])

    def test_decision_maker_and_preparer_separation_are_enforced(self) -> None:
        source = self.make_source()
        prior_ids = (
            source[0].transition_reviewer_id,
            source[0].source_post_operation_reviewer_id,
            source[0].source_completion_reviewer_id,
            source[0].source_operator_id,
            source[0].requester_id,
            source[0].subject_id,
        )
        for decision_maker_id in prior_ids:
            evidence = self.make_decision_evidence(
                source, transition_decision_maker_id=decision_maker_id
            )
            decision = self.make_decision(
                source,
                evidence,
                transition_decision_maker_id=decision_maker_id,
            )
            self.assertEqual(
                self.evaluate_decision(source, evidence, decision).status,
                REJECTED,
            )
        evidence = self.make_decision_evidence(
            source, transition_preparer_id=self.transition_decision_maker_id
        )
        decision = self.make_decision(
            source,
            evidence,
            transition_preparer_id=self.transition_decision_maker_id,
        )
        self.assertEqual(
            self.evaluate_decision(source, evidence, decision).status,
            REJECTED,
        )

    def test_organization_and_route_binding_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(
            source,
            transition_decision_maker_organization_id=(
                source[1].transition_reviewer_organization_id
            ),
        )
        decision = self.make_decision(
            source,
            evidence,
            transition_decision_maker_organization_id=(
                source[1].transition_reviewer_organization_id
            ),
        )
        self.assertEqual(
            self.evaluate_decision(source, evidence, decision).status,
            REJECTED,
        )
        evidence = self.make_decision_evidence(source)
        bad = self.refresh_decision(
            self.make_decision(source, evidence),
            transition_preparation_route_digest="z" * 64,
        )
        self.assertEqual(
            self.evaluate_decision(source, evidence, bad).status,
            REJECTED,
        )

    def test_invalid_decision_authority_is_rejected(self) -> None:
        source = self.make_source()
        for changes in (
            {"decision_maker_mandate_verified": False},
            {"decision_maker_qualification_verified": False},
            {"decision_maker_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"decision_ready": False},
            {"appeal_route_available": False},
            {"dissent_route_available": False},
            {"minority_opinion_recorded": False},
        ):
            evidence = self.make_decision_evidence(source, **changes)
            decision = self.make_decision(source, evidence)
            self.assertEqual(
                self.evaluate_decision(source, evidence, decision).status,
                REJECTED,
            )

    def test_hold_recovery_or_anomaly_denies_without_effect(self) -> None:
        source = self.make_source()
        for changes in (
            {"unresolved_anomaly_present": True},
            {"recovery_required": True},
            {"institutional_hold_active": True},
            {"emergency_state_active": True},
        ):
            evidence = self.make_decision_evidence(source, **changes)
            decision = self.make_decision(source, evidence)
            artifact = self.evaluate_decision(source, evidence, decision)
            self.assertEqual(artifact.status, DENIED)
            self.assertFalse(artifact.transition_preparation_required_next)
            self.assertFalse(artifact.lifecycle_transition_performed)

    def test_time_bounds_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source)
        for changes in (
            {"captured_at_epoch_seconds": self.decided_at - 121},
            {"decision_expiry_at_epoch_seconds": self.decided_at + 121},
            {
                "transition_preparation_deadline_at_epoch_seconds": (
                    self.decided_at + 181
                )
            },
        ):
            changed = self.refresh_evidence(evidence, **changes)
            decision = self.make_decision(
                source,
                changed,
                decision_expiry_at_epoch_seconds=(
                    changed.decision_expiry_at_epoch_seconds
                ),
                transition_preparation_deadline_at_epoch_seconds=(
                    changed.transition_preparation_deadline_at_epoch_seconds
                ),
            )
            self.assertEqual(
                self.evaluate_decision(source, changed, decision).status,
                REJECTED,
            )

    def test_determinism_record_integrity_and_effect_boundary(self) -> None:
        source = self.make_source()
        evidence = self.make_decision_evidence(source)
        decision = self.make_decision(source, evidence)
        left = self.evaluate_decision(source, evidence, decision)
        right = self.evaluate_decision(source, evidence, decision)
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "transition_decision_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(source, evidence, decision),
            ),
        )
        for value in (
            left.lifecycle_transition_prepared,
            left.lifecycle_transition_approved,
            left.lifecycle_transition_started,
            left.lifecycle_transition_completed,
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
