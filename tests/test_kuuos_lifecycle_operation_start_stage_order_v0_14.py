from __future__ import annotations

from runtime.kuuos_lifecycle_operation_start_core_v0_14 import SOURCE_ORDER_CHECK
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import REJECTED
from tests.kuuos_lifecycle_operation_start_fixture_v0_14 import (
    LifecycleOperationStartFixtureV014,
)


class LifecycleOperationStartStageOrderV014Tests(
    LifecycleOperationStartFixtureV014
):
    def test_start_request_cannot_precede_operation_approval_completion(self) -> None:
        source = self.make_source()
        early = source[0].completed_at_epoch_seconds - 1
        evidence = self.make_start_evidence(
            source,
            start_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        start = self.make_start_submission(
            source,
            evidence,
            start_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_start(source, evidence, start)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.operation_start_record_issued)
        self.assertFalse(artifact.operation_started)
