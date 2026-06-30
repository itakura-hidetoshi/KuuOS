from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    checkpoint_candidate_validation_digest,
    derive_checkpoint_candidate_validation,
)
from runtime.kuuos_checkpoint_evidence_envelope_types_v1_12 import (
    ENVELOPE_CONFLICT,
    ENVELOPE_READY,
    ENVELOPE_REJECTED,
)
from runtime.kuuos_repository_checkpoint_cas_contract_v1_10 import (
    build_repository_checkpoint_cas_policy,
    derive_repository_checkpoint_cas_contract,
)
from runtime.v112_checkpoint_evidence_envelope import (
    derive_checkpoint_evidence_envelope,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture

OTHER_OID = "3" * 40


class CheckpointEvidenceEnvelopeV112Tests(
    CheckpointCandidateV109Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_checkpoint_candidate_fixture()
        stability, context, observation = self.substituted_case()
        record, route, decision, candidate = self.candidate_case(
            stability, context, observation
        )
        self.stability = stability
        self.context = context
        self.observation = observation
        self.record = record
        self.route = route
        self.decision = decision
        self.candidate = candidate
        self.validation = derive_checkpoint_candidate_validation(
            "validation-v112",
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
            expected_repository_id=stability.repository_id,
            expected_checkpoint_reference=stability.checkpoint_reference,
        )
        self.cas_policy = build_repository_checkpoint_cas_policy(
            "cas-policy-v112",
            allowed_repository_ids=(stability.repository_id,),
            allowed_checkpoint_references=(stability.checkpoint_reference,),
        )

    def contract(self, observed_oid=None):
        return derive_repository_checkpoint_cas_contract(
            "contract-v112",
            self.candidate,
            self.cas_policy,
            observed_current_oid=(
                self.candidate.expected_current_oid
                if observed_oid is None
                else observed_oid
            ),
        )

    def test_exact_ready_evidence_is_eligible(self) -> None:
        envelope = derive_checkpoint_evidence_envelope(
            "envelope-ready", self.contract(), self.validation
        )
        self.assertEqual(envelope.status, ENVELOPE_READY)
        self.assertTrue(envelope.eligible)
        self.assertFalse(envelope.operation_performed)

    def test_observed_oid_conflict_is_not_eligible(self) -> None:
        envelope = derive_checkpoint_evidence_envelope(
            "envelope-conflict", self.contract(OTHER_OID), self.validation
        )
        self.assertEqual(envelope.status, ENVELOPE_CONFLICT)
        self.assertFalse(envelope.eligible)

    def test_invalid_input_digests_are_rejected(self) -> None:
        cases = (
            (
                "contract",
                replace(self.contract(), contract_digest="invalid-contract-digest"),
                self.validation,
                "contract_valid",
            ),
            (
                "validation",
                self.contract(),
                replace(self.validation, validation_digest="invalid-validation-digest"),
                "validation_valid",
            ),
        )
        for label, contract, validation, validity_field in cases:
            with self.subTest(input_digest=label):
                envelope = derive_checkpoint_evidence_envelope(
                    f"envelope-invalid-{label}", contract, validation
                )
                self.assertEqual(envelope.status, ENVELOPE_REJECTED)
                self.assertFalse(getattr(envelope, validity_field))

    def test_self_consistent_binding_mismatches_are_rejected(self) -> None:
        cases = (
            ("candidate_digest", "different-candidate", "candidate_match"),
            ("repository_id", "repository-other", "repository_match"),
            (
                "checkpoint_reference",
                "refs/kuuos/checkpoints/other",
                "checkpoint_match",
            ),
            ("expected_current_oid", "4" * 40, "expected_oid_match"),
            ("proposed_checkpoint_oid", "5" * 40, "proposed_oid_match"),
        )
        for field, changed_value, match_field in cases:
            with self.subTest(binding=field):
                changed = replace(
                    self.validation,
                    **{field: changed_value},
                    validation_digest="",
                )
                changed = replace(
                    changed,
                    validation_digest=checkpoint_candidate_validation_digest(changed),
                )
                envelope = derive_checkpoint_evidence_envelope(
                    f"envelope-mismatch-{field}", self.contract(), changed
                )
                self.assertEqual(envelope.status, ENVELOPE_REJECTED)
                self.assertFalse(getattr(envelope, match_field))

    def test_same_input_is_deterministic(self) -> None:
        first = derive_checkpoint_evidence_envelope(
            "envelope-deterministic", self.contract(), self.validation
        )
        second = derive_checkpoint_evidence_envelope(
            "envelope-deterministic", self.contract(), self.validation
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
