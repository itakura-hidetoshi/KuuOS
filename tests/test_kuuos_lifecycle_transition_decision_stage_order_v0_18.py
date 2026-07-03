from __future__ import annotations

from runtime.kuuos_lifecycle_transition_decision_core_v0_18 import SOURCE_ORDER_CHECK
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import REJECTED
from tests.kuuos_lifecycle_transition_decision_fixture_v0_18 import (
    LifecycleTransitionDecisionFixtureV018,
)


class LifecycleTransitionDecisionStageOrderV018Tests(
    LifecycleTransitionDecisionFixtureV018
):
    def test_decision_request_cannot_precede_transition_review(self) -> None:
        source = self.make_source()
        early = source[0].reviewed_at_epoch_seconds - 1
        evidence = self.make_decision_evidence(
            source,
            decision_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        decision = self.make_decision(
            source,
            evidence,
            decision_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_decision(source, evidence, decision)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.transition_decision_record_issued)
        self.assertFalse(artifact.transition_decision_made)
