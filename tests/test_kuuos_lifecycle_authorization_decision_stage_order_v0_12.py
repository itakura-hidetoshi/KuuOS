from __future__ import annotations

from runtime.kuuos_lifecycle_authorization_decision_core_v0_12 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import REJECTED
from tests.kuuos_lifecycle_authorization_decision_fixture_v0_12 import (
    LifecycleAuthorizationDecisionFixtureV012,
)


class LifecycleAuthorizationDecisionStageOrderV012Tests(
    LifecycleAuthorizationDecisionFixtureV012
):
    def test_decision_request_cannot_precede_source_review_completion(self) -> None:
        source = self.make_source()
        early_request = source[0].completed_at_epoch_seconds - 1
        evidence = self.make_decision_evidence(
            source,
            decision_requested_at_epoch_seconds=early_request,
        )
        decision = self.make_decision_submission(
            source,
            evidence,
            decision_requested_at_epoch_seconds=early_request,
        )

        artifact = self.evaluate_decision(source, evidence, decision)

        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.authorization_decision_record_issued)
        self.assertFalse(artifact.authorization_decision_made)
