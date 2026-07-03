from __future__ import annotations

from runtime.kuuos_lifecycle_governance_transition_approval_v0_20 import APPROVED, DENIED, REJECTED
from tests.kuuos_lifecycle_transition_approval_fixture_v0_20 import LifecycleTransitionApprovalFixtureV020


class LifecycleTransitionApprovalV020Tests(LifecycleTransitionApprovalFixtureV020):
    def test_valid_approval_routes_only_to_start_authorization(self) -> None:
        artifact = self.evaluate_approval()
        self.assertEqual(artifact.status, APPROVED)
        self.assertTrue(artifact.transition_approval_record_issued)
        self.assertTrue(artifact.transition_package_approved)
        self.assertTrue(artifact.transition_start_authorization_required_next)
        self.assertFalse(artifact.lifecycle_transition_start_authorized)
        self.assertFalse(artifact.lifecycle_transition_started)
        self.assertFalse(artifact.lifecycle_transition_performed)
        self.assertFalse(artifact.repository_changed)

    def test_authority_or_freshness_failure_is_denied_not_started(self) -> None:
        source = self.make_source()
        for changes in ({"approver_authority_verified": False}, {"package_fresh": False}):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval(source, evidence)
            artifact = self.evaluate_approval(source, evidence, approval)
            self.assertEqual(artifact.status, DENIED)
            self.assertTrue(artifact.transition_approval_record_issued)
            self.assertTrue(artifact.transition_approval_denied)
            self.assertFalse(artifact.transition_package_approved)
            self.assertFalse(artifact.transition_start_authorization_required_next)
            self.assertFalse(artifact.lifecycle_transition_started)

    def test_non_ready_source_preparation_is_rejected(self) -> None:
        source = self.make_source()
        record = self.refresh_source_record(source[3], ready_for_separate_transition_approval=False, transition_approval_required_next=False, transition_approval_route_required_next=False)
        changed = (*source[:3], record, source[4])
        evidence = self.make_approval_evidence(changed)
        approval = self.make_approval(changed, evidence)
        artifact = self.evaluate_approval(changed, evidence, approval)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.transition_approval_record_issued)

    def test_route_and_actor_swaps_are_rejected(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval(source, evidence)
        for changed in (
            self.refresh_approval(approval, transition_start_authorization_route_digest="z" * 64),
            self.refresh_approval(approval, transition_approver_id="other-approver"),
        ):
            artifact = self.evaluate_approval(source, evidence, changed)
            self.assertEqual(artifact.status, REJECTED)
            self.assertFalse(artifact.transition_approval_record_issued)
