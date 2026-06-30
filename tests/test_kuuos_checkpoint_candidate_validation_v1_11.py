from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    REJECTED,
    VALID,
    derive_checkpoint_candidate_validation,
)
from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    repository_checkpoint_candidate_digest,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture


class CheckpointCandidateValidationV111Tests(
    CheckpointCandidateV109Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_checkpoint_candidate_fixture()

    def substitution_inputs(self):
        stability, context, observation = self.substituted_case()
        record, route, decision, candidate = self.candidate_case(
            stability,
            context,
            observation,
        )
        return stability, context, observation, record, route, decision, candidate

    def validate(
        self,
        validation_id: str,
        *,
        candidate_override=None,
        expected_repository_id=None,
        expected_checkpoint_reference=None,
    ):
        stability, context, observation, record, route, decision, candidate = (
            self.substitution_inputs()
        )
        if candidate_override is not None:
            candidate = candidate_override(candidate)
        return derive_checkpoint_candidate_validation(
            validation_id,
            candidate,
            decision,
            route,
            record,
            stability,
            context,
            self.policy,
            observation,
            self.routing_policy,
            self.gate_policy,
            self.candidate_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            gate_evaluated_at_epoch_seconds=self.gate_at,
            candidate_evaluated_at_epoch_seconds=self.candidate_at,
            expected_repository_id=(
                stability.repository_id
                if expected_repository_id is None
                else expected_repository_id
            ),
            expected_checkpoint_reference=(
                stability.checkpoint_reference
                if expected_checkpoint_reference is None
                else expected_checkpoint_reference
            ),
        )

    def test_complete_candidate_chain_is_accepted(self) -> None:
        result = self.validate("validation-ok")
        self.assertEqual(result.status, VALID)
        self.assertTrue(result.upstream_chain_revalidated)
        self.assertFalse(result.operation_performed)

    def test_self_consistent_candidate_tamper_is_rejected_by_replay(self) -> None:
        def tamper(candidate):
            changed = replace(
                candidate,
                candidate_policy_digest="tampered-policy-digest",
                candidate_digest="",
            )
            return replace(
                changed,
                candidate_digest=repository_checkpoint_candidate_digest(changed),
            )

        result = self.validate("validation-replay-tamper", candidate_override=tamper)
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.upstream_chain_revalidated)
        self.assertTrue(result.ready_candidate)

    def test_repository_mismatch_is_rejected(self) -> None:
        result = self.validate(
            "validation-repo-mismatch",
            expected_repository_id="repo:other",
        )
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.repository_matches)

    def test_checkpoint_mismatch_is_rejected(self) -> None:
        result = self.validate(
            "validation-ref-mismatch",
            expected_checkpoint_reference="refs/kuuos/checkpoints/other",
        )
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.checkpoint_matches)

    def test_same_input_is_deterministic(self) -> None:
        first = self.validate("validation-deterministic")
        second = self.validate("validation-deterministic")
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
