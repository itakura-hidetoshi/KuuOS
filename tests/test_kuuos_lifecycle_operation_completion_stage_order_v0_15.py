from __future__ import annotations

from runtime.kuuos_lifecycle_operation_completion_core_v0_15 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    REJECTED,
)
from tests.kuuos_lifecycle_operation_completion_fixture_v0_15 import (
    LifecycleOperationCompletionFixtureV015,
)


class LifecycleOperationCompletionStageOrderV015Tests(
    LifecycleOperationCompletionFixtureV015
):
    def test_completion_request_cannot_precede_operation_start(
        self,
    ) -> None:
        source = self.make_source()
        early = source[0].started_at_epoch_seconds - 1
        evidence = self.make_completion_evidence(
            source,
            completion_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        completion = self.make_completion_submission(
            source,
            evidence,
            completion_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_completion(
            source, evidence, completion
        )
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(
            artifact.checks[SOURCE_ORDER_CHECK]
        )
        self.assertFalse(
            artifact.operation_completion_record_issued
        )
        self.assertFalse(artifact.operation_completed)
