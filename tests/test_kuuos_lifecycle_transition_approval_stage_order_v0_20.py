from __future__ import annotations

from runtime.kuuos_lifecycle_governance_transition_approval_v0_20 import (
    REJECTED,
    SOURCE_ORDER_CHECK,
)
from tests.kuuos_lifecycle_transition_approval_fixture_v0_20 import (
    LifecycleTransitionApprovalFixtureV020,
)


class LifecycleTransitionApprovalStageOrderV020Tests(LifecycleTransitionApprovalFixtureV020):
    def test_approval_request_cannot_precede_transition_preparation(self) -> None:
        source = self.make_source()
        early = source[0].prepared_at_epoch_seconds - 1
        evidence = self.make_approval_evidence(
            source,
            approval_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        approval = self.make_approval(
            source,
            evidence,
            approval_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.transition_approval_record_issued)

    def test_approval_must_complete_within_source_deadline(self) -> None:
        source = self.make_source()
        late = source[0].transition_approval_deadline_at_epoch_seconds + 1
        evidence = self.make_approval_evidence(source, approved_at_epoch_seconds=late)
        approval = self.make_approval(source, evidence, approved_at_epoch_seconds=late)
        artifact = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
