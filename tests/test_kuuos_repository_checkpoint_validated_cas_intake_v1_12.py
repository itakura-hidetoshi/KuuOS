from dataclasses import replace
import unittest

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    derive_checkpoint_candidate_validation,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    repository_checkpoint_cas_contract_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_v1_10 import (
    build_repository_checkpoint_cas_policy,
    derive_repository_checkpoint_cas_contract,
)
from runtime.kuuos_repository_checkpoint_validated_cas_intake_types_v1_12 import (
    INTAKE_CONFLICT,
    INTAKE_READY,
    INTAKE_REJECTED,
)
from runtime.v112_checkpoint_validated_cas_intake_core import (
    build_repository_checkpoint_validated_cas_intake_policy,
    derive_repository_checkpoint_validated_cas_intake,
)
from tests.v109_checkpoint_candidate_fixture import CheckpointCandidateV109Fixture


class RepositoryCheckpointValidatedCasIntakeV112Tests(
    CheckpointCandidateV109Fixture,
    unittest.TestCase,
):
    def setUp(self) -> None:
        self.setup_checkpoint_candidate_fixture()
        self.cas_policy = build_repository_checkpoint_cas_policy(
            "checkpoint-cas-policy-v112-tests",
            allowed_repository_ids=(self.stability.repository_id,),
            allowed_checkpoint_references=(self.stability.checkpoint_reference,),
        )
        self.intake_policy = build_repository_checkpoint_validated_cas_intake_policy(
            "validated-cas-intake-policy-v112-tests",
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
            "candidate-validation-v111-for-v112",
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
            "checkpoint-cas-contract-v110-for-v112",
            candidate,
            self.cas_policy,
            observed_current_oid=(
                candidate.expected_current_oid
                if observed_current_oid is None
                else observed_current_oid
            ),
        )
        return validation, contract

    def test_validated_ready_contract_produces_ready_intake(self) -> None:
        validation, contract = self.artifacts()
        intake = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-ready",
            validation,
            contract,
            self.intake_policy,
        )
        self.assertEqual(intake.status, INTAKE_READY)
        self.assertTrue(intake.upstream_chain_revalidated)
        self.assertTrue(intake.compare_and_swap_required)
        self.assertFalse(intake.repository_change_authority_granted)
        self.assertFalse(intake.execution_performed)

    def test_validated_changed_observation_produces_conflict(self) -> None:
        validation, contract = self.artifacts(observed_current_oid="3" * 40)
        intake = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-conflict",
            validation,
            contract,
            self.intake_policy,
        )
        self.assertEqual(intake.status, INTAKE_CONFLICT)
        self.assertFalse(intake.compare_and_swap_required)
        self.assertFalse(intake.live_git_command_invoked)

    def test_self_consistent_candidate_binding_tamper_is_rejected(self) -> None:
        validation, contract = self.artifacts()
        changed = replace(
            contract,
            candidate_digest="different-candidate-digest",
            contract_digest="",
        )
        changed = replace(
            changed,
            contract_digest=repository_checkpoint_cas_contract_digest(changed),
        )
        intake = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-candidate-mismatch",
            validation,
            changed,
            self.intake_policy,
        )
        self.assertEqual(intake.status, INTAKE_REJECTED)
        self.assertFalse(intake.candidate_binding_exact)

    def test_self_consistent_oid_binding_tamper_is_rejected(self) -> None:
        validation, contract = self.artifacts()
        changed = replace(
            contract,
            proposed_checkpoint_oid="4" * 40,
            contract_digest="",
        )
        changed = replace(
            changed,
            contract_digest=repository_checkpoint_cas_contract_digest(changed),
        )
        intake = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-oid-mismatch",
            validation,
            changed,
            self.intake_policy,
        )
        self.assertEqual(intake.status, INTAKE_REJECTED)
        self.assertFalse(intake.oid_binding_exact)

    def test_same_input_is_deterministic(self) -> None:
        validation, contract = self.artifacts()
        first = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-deterministic",
            validation,
            contract,
            self.intake_policy,
        )
        second = derive_repository_checkpoint_validated_cas_intake(
            "validated-cas-intake-deterministic",
            validation,
            contract,
            self.intake_policy,
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
