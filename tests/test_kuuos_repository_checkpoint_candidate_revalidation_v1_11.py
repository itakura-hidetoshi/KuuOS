from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_NONE,
    CANDIDATE_READY,
    REASON_CHECKPOINT_INTERFACE_REQUIRED,
    repository_checkpoint_candidate_digest,
)
from runtime.kuuos_repository_checkpoint_candidate_revalidation_types_v1_11 import (
    REASON_CANDIDATE_STALE,
    REASON_FULL_REVALIDATION_PASSED,
    REASON_INVALID_EVIDENCE,
    REVALIDATION_REJECTED,
    REVALIDATION_VALID,
)
from tests.v111_candidate_revalidation_fixture import (
    CandidateRevalidationV111Fixture,
)


class RepositoryCheckpointCandidateRevalidationV111Tests(
    unittest.TestCase,
    CandidateRevalidationV111Fixture,
):
    def setUp(self) -> None:
        self.setup_candidate_revalidation_fixture()

    def test_substituted_candidate_passes_complete_revalidation(self) -> None:
        stability, context, observation = self.substituted_case()
        _, _, _, candidate, receipt = self.receipt_case(
            stability,
            context,
            observation,
        )
        self.assertEqual(candidate.status, CANDIDATE_READY)
        self.assertEqual(receipt.status, REVALIDATION_VALID)
        self.assertEqual(receipt.reason, REASON_FULL_REVALIDATION_PASSED)
        self.assertTrue(receipt.full_v109_revalidation_passed)
        self.assertTrue(receipt.repository_binding_exact)
        self.assertTrue(receipt.candidate_fresh)
        self.assertFalse(receipt.repository_change_authority_granted)
        self.assertFalse(receipt.execution_performed)

    def test_clean_noop_candidate_can_receive_valid_derivation_receipt(self) -> None:
        _, _, _, candidate, receipt = self.receipt_case(
            self.stability,
            self.v105_context,
            self.observation,
        )
        self.assertEqual(candidate.status, CANDIDATE_NONE)
        self.assertEqual(receipt.status, REVALIDATION_VALID)
        self.assertTrue(receipt.full_v109_revalidation_passed)

    def test_stale_candidate_is_rejected_after_successful_replay(self) -> None:
        stability, context, observation = self.substituted_case()
        _, _, _, _, receipt = self.receipt_case(
            stability,
            context,
            observation,
            revalidated_at=self.candidate_at + 31,
        )
        self.assertEqual(receipt.status, REVALIDATION_REJECTED)
        self.assertEqual(receipt.reason, REASON_CANDIDATE_STALE)
        self.assertTrue(receipt.full_v109_revalidation_passed)
        self.assertFalse(receipt.candidate_fresh)

    def test_self_consistent_forged_candidate_is_rejected_by_replay(self) -> None:
        record, route, decision, candidate = self.candidate_case(
            self.stability,
            self.v105_context,
            self.observation,
        )
        forged = replace(
            candidate,
            status=CANDIDATE_READY,
            reason=REASON_CHECKPOINT_INTERFACE_REQUIRED,
            dedicated_checkpoint_interface_required=True,
            candidate_digest="",
        )
        forged = replace(
            forged,
            candidate_digest=repository_checkpoint_candidate_digest(forged),
        )
        receipt = self.derive_receipt(
            forged,
            decision,
            route,
            record,
            self.stability,
            self.v105_context,
            self.observation,
        )
        self.assertEqual(receipt.status, REVALIDATION_REJECTED)
        self.assertEqual(receipt.reason, REASON_INVALID_EVIDENCE)
        self.assertFalse(receipt.full_v109_revalidation_passed)

    def test_same_input_has_same_receipt(self) -> None:
        stability, context, observation = self.substituted_case()
        first = self.receipt_case(stability, context, observation)[4]
        second = self.receipt_case(stability, context, observation)[4]
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
