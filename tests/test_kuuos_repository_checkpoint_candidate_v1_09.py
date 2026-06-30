from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_NONE,
    CANDIDATE_READY,
    CANDIDATE_REJECTED,
    REASON_CHECKPOINT_INTERFACE_REQUIRED,
    REASON_CLEAN_NOOP,
    REASON_CREATION_ROUTE_AVAILABLE,
    REASON_INVALID_EVIDENCE,
    repository_checkpoint_candidate_digest,
)
from runtime.kuuos_repository_checkpoint_candidate_v1_09 import (
    repository_checkpoint_candidate_issues,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture


class RepositoryCheckpointCandidateV109Tests(
    CheckpointCandidateV109Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_checkpoint_candidate_fixture()

    def test_clean_checkpoint_produces_no_candidate(self) -> None:
        first = self.candidate_case(
            self.stability,
            self.v105_context,
            self.observation,
        )[3]
        second = self.candidate_case(
            self.stability,
            self.v105_context,
            self.observation,
        )[3]
        self.assertEqual(first, second)
        self.assertEqual(first.status, CANDIDATE_NONE)
        self.assertEqual(first.reason, REASON_CLEAN_NOOP)
        self.assertFalse(first.dedicated_checkpoint_interface_required)

    def test_lost_checkpoint_uses_existing_creation_route(self) -> None:
        stability, context, observation = self.lost_case()
        candidate = self.candidate_case(stability, context, observation)[3]
        self.assertEqual(candidate.status, CANDIDATE_NONE)
        self.assertEqual(candidate.reason, REASON_CREATION_ROUTE_AVAILABLE)
        self.assertFalse(candidate.dedicated_checkpoint_interface_required)

    def test_substitution_produces_checkpoint_candidate(self) -> None:
        stability, context, observation = self.substituted_case()
        candidate = self.candidate_case(stability, context, observation)[3]
        self.assertEqual(candidate.status, CANDIDATE_READY)
        self.assertEqual(
            candidate.reason,
            REASON_CHECKPOINT_INTERFACE_REQUIRED,
        )
        self.assertTrue(candidate.dedicated_checkpoint_interface_required)
        self.assertNotEqual(
            candidate.expected_current_oid,
            candidate.proposed_checkpoint_oid,
        )
        self.assertFalse(candidate.human_review_required)
        self.assertFalse(candidate.repository_change_authority_granted)
        self.assertFalse(candidate.execution_performed)

    def test_stale_gate_evidence_is_rejected(self) -> None:
        candidate = self.candidate_case(
            self.stability,
            self.v105_context,
            self.observation,
            candidate_at=self.gate_at + 21,
        )[3]
        self.assertEqual(candidate.status, CANDIDATE_REJECTED)
        self.assertEqual(candidate.reason, REASON_INVALID_EVIDENCE)
        self.assertFalse(candidate.checks["namespace_gate_fresh"])

    def test_candidate_tamper_is_detected(self) -> None:
        record, route, decision, candidate = self.candidate_case(
            self.stability,
            self.v105_context,
            self.observation,
        )
        tampered = replace(
            candidate,
            dedicated_checkpoint_interface_required=True,
            candidate_digest="",
        )
        tampered = replace(
            tampered,
            candidate_digest=repository_checkpoint_candidate_digest(tampered),
        )
        issues = repository_checkpoint_candidate_issues(
            tampered,
            decision,
            route,
            record,
            self.stability,
            self.v105_context,
            self.policy,
            self.observation,
            self.routing_policy,
            self.gate_policy,
            self.candidate_policy,
            review_evaluated_at_epoch_seconds=self.evaluated_at,
            routed_at_epoch_seconds=self.routed_at,
            gate_evaluated_at_epoch_seconds=self.gate_at,
            evaluated_at_epoch_seconds=self.candidate_at,
        )
        self.assertIn("checkpoint_candidate_recomputation_mismatch", issues)
        self.assertIn("checkpoint_candidate_interface_boundary_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
