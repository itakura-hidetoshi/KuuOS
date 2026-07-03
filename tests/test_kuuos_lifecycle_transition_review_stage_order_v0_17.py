from __future__ import annotations

from runtime.kuuos_lifecycle_transition_review_core_v0_17 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import REJECTED
from tests.kuuos_lifecycle_transition_review_fixture_v0_17 import (
    LifecycleTransitionReviewFixtureV017,
)


class LifecycleTransitionReviewStageOrderV017Tests(
    LifecycleTransitionReviewFixtureV017
):
    def test_transition_review_request_cannot_precede_post_operation_review(
        self,
    ) -> None:
        source = self.make_source()
        early = source[0].reviewed_at_epoch_seconds - 1
        evidence = self.make_transition_evidence(
            source,
            review_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        review = self.make_transition_review(
            source,
            evidence,
            review_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_transition_review(source, evidence, review)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.transition_review_record_issued)
        self.assertFalse(artifact.transition_review_completed)
