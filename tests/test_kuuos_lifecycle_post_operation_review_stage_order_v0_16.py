from __future__ import annotations

from runtime.kuuos_lifecycle_post_operation_review_core_v0_16 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import REJECTED
from tests.kuuos_lifecycle_post_operation_review_fixture_v0_16 import (
    LifecyclePostOperationReviewFixtureV016,
)


class LifecyclePostOperationReviewStageOrderV016Tests(
    LifecyclePostOperationReviewFixtureV016
):
    def test_review_request_cannot_precede_operation_completion(self) -> None:
        source = self.make_source()
        early = source[0].completed_at_epoch_seconds - 1
        evidence = self.make_review_evidence(
            source,
            review_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        review = self.make_review_submission(
            source,
            evidence,
            review_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_review(source, evidence, review)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.post_operation_review_record_issued)
        self.assertFalse(artifact.post_operation_review_completed)
