from __future__ import annotations

from runtime.kuuos_lifecycle_operation_approval_core_v0_13 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import REJECTED
from tests.kuuos_lifecycle_operation_approval_fixture_v0_13 import (
    LifecycleOperationApprovalFixtureV013,
)


class LifecycleOperationApprovalStageOrderV013Tests(
    LifecycleOperationApprovalFixtureV013
):
    def test_approval_request_cannot_precede_authorization_completion(self) -> None:
        source = self.make_source()
        early = source[0].completed_at_epoch_seconds - 1
        evidence = self.make_approval_evidence(
            source,
            approval_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        approval = self.make_approval_submission(
            source,
            evidence,
            approval_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.operation_approval_record_issued)
        self.assertFalse(artifact.operation_approval_made)
