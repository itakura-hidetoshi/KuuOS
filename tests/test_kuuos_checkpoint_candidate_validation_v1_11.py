from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    REJECTED,
    VALID,
    derive_checkpoint_candidate_validation,
)
from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_READY,
    REASON_CHECKPOINT_INTERFACE_REQUIRED,
    RepositoryCheckpointCandidate,
    repository_checkpoint_candidate_digest,
)

REPOSITORY_ID = "repo:kuuos"
CHECKPOINT_REFERENCE = "refs/kuuos/checkpoints/stable"
CURRENT_OID = "1" * 40
PROPOSED_OID = "2" * 40


def candidate() -> RepositoryCheckpointCandidate:
    value = RepositoryCheckpointCandidate(
        candidate_id="candidate-v109",
        status=CANDIDATE_READY,
        reason=REASON_CHECKPOINT_INTERFACE_REQUIRED,
        namespace_gate_decision_digest="gate-digest",
        candidate_policy_digest="candidate-policy-digest",
        repository_id=REPOSITORY_ID,
        git_dir_fingerprint="git-dir-fingerprint",
        checkpoint_reference=CHECKPOINT_REFERENCE,
        expected_current_oid=CURRENT_OID,
        proposed_checkpoint_oid=PROPOSED_OID,
        dedicated_checkpoint_interface_required=True,
        human_review_required=False,
        repository_change_authority_granted=False,
        execution_performed=False,
        evaluated_at_epoch_seconds=100,
        checks={},
        evidence_digests={},
        candidate_digest="",
    )
    return replace(value, candidate_digest=repository_checkpoint_candidate_digest(value))


class CheckpointCandidateValidationV111Tests(unittest.TestCase):
    def test_valid_candidate_is_accepted(self) -> None:
        result = derive_checkpoint_candidate_validation(
            "validation-ok",
            candidate(),
            expected_repository_id=REPOSITORY_ID,
            expected_checkpoint_reference=CHECKPOINT_REFERENCE,
        )
        self.assertEqual(result.status, VALID)
        self.assertFalse(result.operation_performed)

    def test_repository_mismatch_is_rejected(self) -> None:
        result = derive_checkpoint_candidate_validation(
            "validation-repo-mismatch",
            candidate(),
            expected_repository_id="repo:other",
            expected_checkpoint_reference=CHECKPOINT_REFERENCE,
        )
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.repository_matches)

    def test_checkpoint_mismatch_is_rejected(self) -> None:
        result = derive_checkpoint_candidate_validation(
            "validation-ref-mismatch",
            candidate(),
            expected_repository_id=REPOSITORY_ID,
            expected_checkpoint_reference="refs/kuuos/checkpoints/other",
        )
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.checkpoint_matches)

    def test_digest_mismatch_is_rejected(self) -> None:
        tampered = replace(candidate(), candidate_digest="tampered")
        result = derive_checkpoint_candidate_validation(
            "validation-digest-mismatch",
            tampered,
            expected_repository_id=REPOSITORY_ID,
            expected_checkpoint_reference=CHECKPOINT_REFERENCE,
        )
        self.assertEqual(result.status, REJECTED)
        self.assertFalse(result.digest_matches)

    def test_same_input_is_deterministic(self) -> None:
        first = derive_checkpoint_candidate_validation(
            "validation-deterministic",
            candidate(),
            expected_repository_id=REPOSITORY_ID,
            expected_checkpoint_reference=CHECKPOINT_REFERENCE,
        )
        second = derive_checkpoint_candidate_validation(
            "validation-deterministic",
            candidate(),
            expected_repository_id=REPOSITORY_ID,
            expected_checkpoint_reference=CHECKPOINT_REFERENCE,
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
