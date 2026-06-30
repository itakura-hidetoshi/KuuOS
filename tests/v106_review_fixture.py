from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    ZERO_OID,
    repository_checkpoint_review_observation_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_v1_06 import (
    build_repository_checkpoint_review_observation,
    build_repository_checkpoint_review_policy,
)
from runtime.v106_review_strict import review_repository_checkpoint_discrepancy
from tests.test_kuuos_repository_checkpoint_stability_v1_05 import (
    RepositoryCheckpointStabilityV105Tests,
)


class ReviewV106Fixture:
    def setup_review_fixture(self) -> None:
        fixture = RepositoryCheckpointStabilityV105Tests(
            methodName="test_stability_is_deterministic_and_confirmed"
        )
        fixture.setUp()
        self.fixture = fixture
        self.stability = fixture._certify()
        self.v105_context = fixture._values()
        self.observer_id = "kuuos-checkpoint-review-observer-v106"
        self.policy = build_repository_checkpoint_review_policy(
            "checkpoint-review-policy-v106",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
            authorized_observer_ids=(self.observer_id,),
            max_observation_age_seconds=20,
        )
        self.evaluated_at = 10_285
        self.observation = self.make_observation(
            self.stability,
            reference_present=True,
            observed_oid=self.stability.expected_oid,
            rechecked_oid=self.stability.expected_oid,
        )

    def make_observation(
        self,
        stability,
        *,
        reference_present: bool,
        observed_oid: str,
        rechecked_oid: str,
        target_object_present: bool = True,
        target_object_type: str = "commit",
        observer_id: str | None = None,
        observed_at_epoch_seconds: int = 10_283,
        rechecked_at_epoch_seconds: int = 10_284,
        **overrides,
    ):
        return build_repository_checkpoint_review_observation(
            "checkpoint-review-observation-v106",
            observer_id or self.observer_id,
            stability,
            reference_present=reference_present,
            observed_oid=observed_oid,
            rechecked_oid=rechecked_oid,
            target_object_present=target_object_present,
            target_object_type=target_object_type,
            observed_at_epoch_seconds=observed_at_epoch_seconds,
            rechecked_at_epoch_seconds=rechecked_at_epoch_seconds,
            **overrides,
        )

    @staticmethod
    def resign_observation(value, **changes):
        value = replace(value, **changes, observation_digest="")
        return replace(
            value,
            observation_digest=repository_checkpoint_review_observation_digest(
                value
            ),
        )

    def review(self, *, stability=None, context=None, observation=None):
        return review_repository_checkpoint_discrepancy(
            "checkpoint-review-record-v106-001",
            stability or self.stability,
            context or self.v105_context,
            self.policy,
            observation or self.observation,
            evaluated_at_epoch_seconds=self.evaluated_at,
        )

    def lost_case(self):
        delayed = self.fixture._resign_delayed(
            self.fixture.delayed,
            reference_present=False,
            observed_oid=ZERO_OID,
        )
        stability = self.fixture._certify(delayed_observation=delayed)
        context = self.fixture._values(delayed_observation=delayed)
        observation = self.make_observation(
            stability,
            reference_present=False,
            observed_oid=ZERO_OID,
            rechecked_oid=ZERO_OID,
        )
        return stability, context, observation

    def substituted_case(self):
        substitute_oid = "b" * 40
        delayed = self.fixture._resign_delayed(
            self.fixture.delayed,
            observed_oid=substitute_oid,
        )
        stability = self.fixture._certify(delayed_observation=delayed)
        context = self.fixture._values(delayed_observation=delayed)
        observation = self.make_observation(
            stability,
            reference_present=True,
            observed_oid=substitute_oid,
            rechecked_oid=substitute_oid,
        )
        return stability, context, observation
