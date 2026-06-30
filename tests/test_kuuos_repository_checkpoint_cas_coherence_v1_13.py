from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    derive_checkpoint_candidate_validation,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    COHERENCE_CONFLICT,
    COHERENCE_READY,
    COHERENCE_REJECTED,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    REASON_CURRENT_OID_CHANGED,
    repository_checkpoint_cas_contract_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_v1_10 import (
    build_repository_checkpoint_cas_policy,
    derive_repository_checkpoint_cas_contract,
)
from runtime.kuuos_repository_checkpoint_validated_cas_intake_types_v1_12 import (
    INTAKE_CONFLICT,
    REASON_VALIDATED_CONFLICT,
    repository_checkpoint_validated_cas_intake_digest,
)
from runtime.v112_checkpoint_validated_cas_intake_core import (
    build_repository_checkpoint_validated_cas_intake_policy,
    derive_repository_checkpoint_validated_cas_intake,
)
from runtime.v113_checkpoint_cas_coherence_core import (
    derive_repository_checkpoint_cas_coherence_receipt,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture

OTHER_OID = "3" * 40


class RepositoryCheckpointCasCoherenceV113Tests(
    CheckpointCandidateV109Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_checkpoint_candidate_fixture()
        self.cas_policy = build_repository_checkpoint_cas_policy(
            "checkpoint-cas-policy-v113-tests",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
        )
        self.intake_policy = build_repository_checkpoint_validated_cas_intake_policy(
            "validated-cas-intake-policy-v113-tests",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
        )

    def artifacts(self, *, observed_current_oid=None):
        stability, context, observation = self.substituted_case()
        record, route, decision, candidate = self.candidate_case(
            stability,
            context,
            observation,
        )
        validation = derive_checkpoint_candidate_validation(
            "candidate-validation-v111-for-v113",
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
        contract = derive_repository_checkpoint_cas_contract(
            "checkpoint-cas-contract-v110-for-v113",
            candidate,
            self.cas_policy,
            observed_current_oid=(
                candidate.expected_current_oid
                if observed_current_oid is None
                else observed_current_oid
            ),
        )
        intake = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-v112-for-v113",
            validation,
            contract,
            self.intake_policy,
        )
        return contract, intake

    def test_coherent_ready_evidence_produces_ready_receipt(self) -> None:
        contract, intake = self.artifacts()
        receipt = derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-ready",
            contract,
            intake,
        )
        self.assertEqual(receipt.status, COHERENCE_READY)
        self.assertTrue(receipt.contract_local_coherence)
        self.assertTrue(receipt.intake_local_coherence)
        self.assertTrue(receipt.exact_contract_intake_binding)
        self.assertTrue(receipt.compare_and_swap_required)
        self.assertFalse(receipt.repository_change_authority_granted)
        self.assertFalse(receipt.execution_performed)
        self.assertFalse(receipt.live_git_command_invoked)

    def test_coherent_conflict_evidence_produces_conflict_receipt(self) -> None:
        contract, intake = self.artifacts(observed_current_oid=OTHER_OID)
        receipt = derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-conflict",
            contract,
            intake,
        )
        self.assertEqual(receipt.status, COHERENCE_CONFLICT)
        self.assertTrue(receipt.contract_local_coherence)
        self.assertTrue(receipt.intake_local_coherence)
        self.assertFalse(receipt.compare_and_swap_required)

    def test_invalid_input_digests_are_rejected(self) -> None:
        contract, intake = self.artifacts()
        cases = (
            (
                "contract",
                replace(contract, contract_digest="invalid-contract-digest"),
                intake,
                "contract_digest_valid",
            ),
            (
                "intake",
                contract,
                replace(intake, intake_digest="invalid-intake-digest"),
                "intake_digest_valid",
            ),
        )
        for label, changed_contract, changed_intake, validity_field in cases:
            with self.subTest(input_digest=label):
                receipt = derive_repository_checkpoint_cas_coherence_receipt(
                    f"checkpoint-cas-coherence-invalid-{label}",
                    changed_contract,
                    changed_intake,
                )
                self.assertEqual(receipt.status, COHERENCE_REJECTED)
                self.assertFalse(getattr(receipt, validity_field))

    def test_self_consistent_state_and_binding_tamper_is_rejected(self) -> None:
        contract, intake = self.artifacts()

        contract_checks = dict(contract.checks)
        contract_checks["compare_and_swap_required"] = False
        contract_checks["observed_oid_matches_expected"] = False
        changed_contract = replace(
            contract,
            status=CONTRACT_CONFLICT,
            reason=REASON_CURRENT_OID_CHANGED,
            compare_and_swap_required=False,
            checks=contract_checks,
            contract_digest="",
        )
        changed_contract = replace(
            changed_contract,
            contract_digest=repository_checkpoint_cas_contract_digest(
                changed_contract
            ),
        )

        intake_checks = dict(intake.checks)
        intake_checks["compare_and_swap_required"] = False
        intake_evidence = dict(intake.evidence_digests)
        intake_evidence["checkpoint_cas_contract"] = changed_contract.contract_digest
        changed_intake = replace(
            intake,
            status=INTAKE_CONFLICT,
            reason=REASON_VALIDATED_CONFLICT,
            contract_digest=changed_contract.contract_digest,
            compare_and_swap_required=False,
            checks=intake_checks,
            evidence_digests=intake_evidence,
            intake_digest="",
        )
        changed_intake = replace(
            changed_intake,
            intake_digest=repository_checkpoint_validated_cas_intake_digest(
                changed_intake
            ),
        )
        receipt = derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-state-tamper",
            changed_contract,
            changed_intake,
        )
        self.assertEqual(receipt.status, COHERENCE_REJECTED)
        self.assertFalse(receipt.contract_local_coherence)
        self.assertTrue(receipt.intake_local_coherence)
        self.assertTrue(receipt.exact_contract_intake_binding)

        binding_cases = (
            ("candidate_digest", "different-candidate"),
            ("repository_id", "repository-other"),
            ("git_dir_fingerprint", "git-dir-other"),
            ("checkpoint_reference", "refs/kuuos/checkpoints/other"),
            ("expected_current_oid", "4" * 40),
            ("observed_current_oid", "5" * 40),
            ("proposed_checkpoint_oid", "6" * 40),
        )
        for field, changed_value in binding_cases:
            with self.subTest(binding=field):
                changed = replace(
                    intake,
                    **{field: changed_value},
                    intake_digest="",
                )
                changed = replace(
                    changed,
                    intake_digest=repository_checkpoint_validated_cas_intake_digest(
                        changed
                    ),
                )
                binding_receipt = derive_repository_checkpoint_cas_coherence_receipt(
                    f"checkpoint-cas-coherence-binding-{field}",
                    contract,
                    changed,
                )
                self.assertEqual(binding_receipt.status, COHERENCE_REJECTED)
                self.assertFalse(
                    binding_receipt.exact_contract_intake_binding
                )

    def test_same_input_is_deterministic(self) -> None:
        contract, intake = self.artifacts()
        first = derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-deterministic",
            contract,
            intake,
        )
        second = derive_repository_checkpoint_cas_coherence_receipt(
            "checkpoint-cas-coherence-deterministic",
            contract,
            intake,
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
