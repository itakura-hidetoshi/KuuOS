from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    repository_checkpoint_reflog_result_digest,
)
from runtime.kuuos_checkpoint_recovery_proposal_types_v0_1 import (
    RECOVERY_OBJECTIVE_COMPARE_ONLY,
    RECOVERY_PROPOSAL_PROPOSED,
    RECOVERY_PROPOSAL_REJECTED,
    checkpoint_recovery_proposal_digest,
)
from runtime.kuuos_checkpoint_recovery_proposal_v0_1 import (
    build_checkpoint_recovery_proposal_policy,
    checkpoint_recovery_proposal_issues,
    propose_checkpoint_recovery,
)
from tests.test_kuuos_repository_checkpoint_reflog_v1_24 import (
    RepositoryCheckpointReflogV124Tests,
)


class CheckpointRecoveryProposalV01Tests(unittest.TestCase):
    requestor_id = "checkpoint-recovery-requestor-v0-1"
    target_reference = "refs/heads/recovery-candidate"
    proposed_at = 1_800_000_100
    rationale = "compare the accepted checkpoint with the bounded recovery target"

    @classmethod
    def setUpClass(cls) -> None:
        cls.helper = RepositoryCheckpointReflogV124Tests(
            methodName="test_exact_checkpoint_transition_is_recorded_without_ref_change"
        )
        cls.helper.setUp()
        cls.source_result = cls.helper.execute()
        cls.policy = build_checkpoint_recovery_proposal_policy(
            "checkpoint-recovery-proposal-policy-v0-1",
            authorized_requestor_ids=(cls.requestor_id,),
            allowed_repository_ids=(cls.source_result.repository_id,),
            allowed_checkpoint_references=(
                cls.source_result.checkpoint_reference,
            ),
            allowed_target_references=(cls.target_reference,),
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.helper.tearDown()

    def proposal(self, *, source_result=None, **overrides):
        arguments = {
            "target_reference": self.target_reference,
            "requestor_id": self.requestor_id,
            "rationale": self.rationale,
            "proposed_at_epoch_seconds": self.proposed_at,
            "objective": RECOVERY_OBJECTIVE_COMPARE_ONLY,
        }
        arguments.update(overrides)
        return propose_checkpoint_recovery(
            "checkpoint-recovery-proposal-v0-1-001",
            self.source_result if source_result is None else source_result,
            self.policy,
            **arguments,
        )

    def test_accepted_v124_result_yields_comparison_only_proposal(self) -> None:
        proposal = self.proposal()
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_PROPOSED)
        self.assertTrue(proposal.source_result_accepted)
        self.assertTrue(proposal.source_binding_exact)
        self.assertTrue(proposal.comparison_required)
        self.assertTrue(proposal.external_review_required)
        self.assertTrue(proposal.explicit_authorization_decision_required)
        self.assertFalse(proposal.source_target_comparison_performed)
        self.assertFalse(proposal.recovery_authority_granted)
        self.assertFalse(proposal.live_git_execution_performed)
        self.assertFalse(proposal.repository_mutation_performed)
        self.assertFalse(proposal.continues_v124_mutation_series)

    def test_same_input_is_deterministic(self) -> None:
        self.assertEqual(self.proposal(), self.proposal())

    def test_proposal_is_repository_read_only(self) -> None:
        before = self.helper.protected_snapshot()
        proposal = self.proposal()
        after = self.helper.protected_snapshot()
        self.assertEqual(before, after)
        self.assertFalse(proposal.checks["live_git_execution_performed"])
        self.assertFalse(proposal.checks["repository_mutation_performed"])

    def test_unapproved_target_is_rejected(self) -> None:
        proposal = self.proposal(target_reference="refs/heads/not-allowed")
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_REJECTED)
        self.assertFalse(proposal.target_reference_allowed)
        self.assertFalse(proposal.comparison_required)

    def test_checkpoint_namespace_cannot_be_reused_as_target(self) -> None:
        proposal = self.proposal(
            target_reference=self.source_result.checkpoint_reference
        )
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_REJECTED)
        self.assertFalse(proposal.target_reference_allowed)
        self.assertFalse(proposal.source_target_distinct)

    def test_unauthorized_requestor_is_rejected(self) -> None:
        proposal = self.proposal(requestor_id="unauthorized-requestor")
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_REJECTED)
        self.assertFalse(proposal.requestor_authorized)

    def test_tampered_v124_result_is_rejected_even_with_fresh_digest(self) -> None:
        tampered = replace(
            self.source_result,
            current_ref_exact_after=False,
            result_digest="",
        )
        tampered = replace(
            tampered,
            result_digest=repository_checkpoint_reflog_result_digest(tampered),
        )
        proposal = self.proposal(source_result=tampered)
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_REJECTED)
        self.assertTrue(proposal.source_result_valid)
        self.assertFalse(proposal.source_result_accepted)

    def test_non_comparison_objective_is_rejected(self) -> None:
        proposal = self.proposal(objective="EXECUTE_RECOVERY")
        self.assertEqual(proposal.status, RECOVERY_PROPOSAL_REJECTED)
        self.assertFalse(proposal.objective_allowed)
        self.assertFalse(proposal.recovery_authority_granted)

    def test_proposal_tamper_is_detected(self) -> None:
        proposal = self.proposal()
        tampered = replace(
            proposal,
            recovery_authority_granted=True,
            proposal_digest="",
        )
        tampered = replace(
            tampered,
            proposal_digest=checkpoint_recovery_proposal_digest(tampered),
        )
        issues = checkpoint_recovery_proposal_issues(
            tampered,
            self.source_result,
            self.policy,
            target_reference=self.target_reference,
            requestor_id=self.requestor_id,
            rationale=self.rationale,
            proposed_at_epoch_seconds=self.proposed_at,
        )
        self.assertIn("recovery_proposal_recomputation_mismatch", issues)
        self.assertIn("recovery_authority_granted_too_early", issues)


if __name__ == "__main__":
    unittest.main()
