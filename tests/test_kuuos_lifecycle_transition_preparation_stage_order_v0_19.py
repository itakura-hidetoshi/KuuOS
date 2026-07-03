from __future__ import annotations

from runtime.kuuos_lifecycle_transition_preparation_core_v0_19 import (
    SOURCE_ORDER_CHECK,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import REJECTED
from tests.kuuos_lifecycle_transition_preparation_fixture_v0_19 import (
    LifecycleTransitionPreparationFixtureV019,
)


class LifecycleTransitionPreparationStageOrderV019Tests(
    LifecycleTransitionPreparationFixtureV019
):
    def test_preparation_request_cannot_precede_transition_decision(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        early = source[0].decided_at_epoch_seconds - 1
        evidence = self.make_preparation_evidence(
            source,
            package,
            preparation_requested_at_epoch_seconds=early,
            captured_at_epoch_seconds=early,
        )
        preparation = self.make_preparation(
            source,
            evidence,
            preparation_requested_at_epoch_seconds=early,
        )
        artifact = self.evaluate_preparation(
            source, package, evidence, preparation
        )
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
        self.assertFalse(artifact.transition_preparation_record_issued)

    def test_preparation_must_complete_within_source_deadline(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        late = source[0].transition_preparation_deadline_at_epoch_seconds + 1
        evidence = self.make_preparation_evidence(
            source,
            package,
            prepared_at_epoch_seconds=late,
        )
        preparation = self.make_preparation(
            source,
            evidence,
            prepared_at_epoch_seconds=late,
        )
        artifact = self.evaluate_preparation(
            source, package, evidence, preparation
        )
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks[SOURCE_ORDER_CHECK])
