from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_atomic_cas_transition_types_v1_16 import (
    TRANSITION_ABORTED,
    TRANSITION_COMMITTED,
)
from runtime.kuuos_repository_checkpoint_atomic_cas_transition_v1_16 import (
    build_repository_checkpoint_atomic_cas_transition_policy,
    build_repository_checkpoint_atomic_cas_transition_request,
    build_repository_checkpoint_nonce_registry,
    build_repository_checkpoint_reference_state,
    derive_repository_checkpoint_atomic_cas_transition,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_decision_types_v1_15 import (
    EXTERNAL_DENY,
    repository_checkpoint_cas_authorization_decision_certificate_digest,
)
from tests import test_kuuos_repository_checkpoint_cas_authorization_decision_v1_15 as v115_tests


class RepositoryCheckpointAtomicCasTransitionV116Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = v115_tests.RepositoryCheckpointCasAuthorizationDecisionV115Tests(
            methodName="test_same_input_is_deterministic"
        )
        self.helper.setUp()
        self.external_decision = self.helper.external_decision()
        self.nonce_status = self.helper.nonce_status()
        self.authorization = self.helper.certificate(
            external_decision=self.external_decision,
            nonce_status=self.nonce_status,
        )
        self.policy = build_repository_checkpoint_atomic_cas_transition_policy(
            "checkpoint-atomic-cas-transition-policy-v116-tests",
            authorized_executor_ids=("executor-v116",),
            max_execution_duration_seconds=30,
            max_reference_state_age_seconds=60,
            max_nonce_registry_age_seconds=60,
        )
        self.started_at = self.helper.evaluated_at + 10
        self.completed_at = self.started_at + 2

    def transition_request(self, authorization=None):
        current = self.authorization if authorization is None else authorization
        return build_repository_checkpoint_atomic_cas_transition_request(
            "checkpoint-atomic-cas-transition-v116",
            current,
            executor_id="executor-v116",
            requested_at_epoch_seconds=self.helper.evaluated_at + 5,
        )

    def reference_state(self, *, current_oid=None):
        return build_repository_checkpoint_reference_state(
            "checkpoint-reference-state-v116",
            repository_id=self.authorization.repository_id,
            git_dir_fingerprint=self.authorization.git_dir_fingerprint,
            checkpoint_reference=self.authorization.checkpoint_reference,
            current_oid=(
                self.authorization.expected_current_oid
                if current_oid is None
                else current_oid
            ),
            sequence_number=7,
            observed_at_epoch_seconds=self.started_at - 10,
        )

    def nonce_registry(self, *, consumed=(), revoked=()):
        return build_repository_checkpoint_nonce_registry(
            "checkpoint-nonce-registry-v116",
            authority_id=self.authorization.nonce_authority_id,
            upstream_snapshot_digest=self.nonce_status.registry_snapshot_digest,
            consumed_nonces=consumed,
            revoked_nonces=revoked,
            sequence_number=11,
            observed_at_epoch_seconds=self.started_at - 10,
        )

    def apply(
        self,
        *,
        authorization=None,
        transition_request=None,
        reference_state=None,
        nonce_registry=None,
        external_decision=None,
        started_at=None,
        completed_at=None,
    ):
        current_authorization = (
            self.authorization if authorization is None else authorization
        )
        current_request = (
            self.transition_request(current_authorization)
            if transition_request is None
            else transition_request
        )
        return derive_repository_checkpoint_atomic_cas_transition(
            current_request,
            current_authorization,
            self.helper.request,
            self.helper.coherence,
            self.helper.helper.policy,
            self.helper.policy,
            self.external_decision
            if external_decision is None
            else external_decision,
            self.nonce_status,
            self.policy,
            self.reference_state() if reference_state is None else reference_state,
            self.nonce_registry() if nonce_registry is None else nonce_registry,
            execution_started_at_epoch_seconds=(
                self.started_at if started_at is None else started_at
            ),
            execution_completed_at_epoch_seconds=(
                self.completed_at if completed_at is None else completed_at
            ),
        )

    def test_granted_matching_cas_commits_reference_and_nonce_atomically(self) -> None:
        source_state = self.reference_state()
        source_registry = self.nonce_registry()
        result, final_state, final_registry = self.apply(
            reference_state=source_state,
            nonce_registry=source_registry,
        )
        self.assertEqual(result.status, TRANSITION_COMMITTED)
        self.assertTrue(result.compare_and_swap_attempted)
        self.assertTrue(result.compare_and_swap_succeeded)
        self.assertTrue(result.atomic_reference_nonce_transition)
        self.assertEqual(final_state.current_oid, self.authorization.proposed_checkpoint_oid)
        self.assertEqual(final_state.sequence_number, source_state.sequence_number + 1)
        self.assertIn(self.authorization.authorization_nonce, final_registry.consumed_nonces)
        self.assertEqual(final_registry.sequence_number, source_registry.sequence_number + 1)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.live_repository_mutated)

    def test_oid_conflict_aborts_and_preserves_both_source_states(self) -> None:
        source_state = self.reference_state(
            current_oid=v115_tests.v114_tests.v113_tests.OTHER_OID
        )
        source_registry = self.nonce_registry()
        result, final_state, final_registry = self.apply(
            reference_state=source_state,
            nonce_registry=source_registry,
        )
        self.assertEqual(result.status, TRANSITION_ABORTED)
        self.assertTrue(result.compare_and_swap_attempted)
        self.assertFalse(result.compare_and_swap_succeeded)
        self.assertTrue(result.failure_preserved_reference_state)
        self.assertTrue(result.failure_preserved_nonce_registry)
        self.assertEqual(final_state.to_dict(), source_state.to_dict())
        self.assertEqual(final_registry.to_dict(), source_registry.to_dict())

    def test_consumed_or_revoked_nonce_aborts_without_partial_transition(self) -> None:
        cases = (
            self.nonce_registry(consumed=(self.authorization.authorization_nonce,)),
            self.nonce_registry(revoked=(self.authorization.authorization_nonce,)),
        )
        for registry in cases:
            with self.subTest(registry=registry.registry_id, consumed=registry.consumed_nonces):
                source_state = self.reference_state()
                result, final_state, final_registry = self.apply(
                    reference_state=source_state,
                    nonce_registry=registry,
                )
                self.assertEqual(result.status, TRANSITION_ABORTED)
                self.assertFalse(result.compare_and_swap_attempted)
                self.assertFalse(result.nonce_consumed)
                self.assertEqual(final_state.to_dict(), source_state.to_dict())
                self.assertEqual(final_registry.to_dict(), registry.to_dict())

    def test_denied_or_self_consistently_tampered_authorization_cannot_commit(self) -> None:
        denial = self.helper.external_decision(decision=EXTERNAL_DENY)
        denied_authorization = self.helper.certificate(
            external_decision=denial,
            nonce_status=self.nonce_status,
        )
        denied_result, _, _ = self.apply(
            authorization=denied_authorization,
            transition_request=self.transition_request(denied_authorization),
            external_decision=denial,
        )
        self.assertEqual(denied_result.status, TRANSITION_ABORTED)
        self.assertFalse(denied_result.authorization_granted)

        tampered = replace(
            self.authorization,
            proposed_checkpoint_oid=v115_tests.v114_tests.v113_tests.OTHER_OID,
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=(
                repository_checkpoint_cas_authorization_decision_certificate_digest(
                    tampered
                )
            ),
        )
        tampered_result, _, _ = self.apply(
            authorization=tampered,
            transition_request=self.transition_request(tampered),
        )
        self.assertEqual(tampered_result.status, TRANSITION_ABORTED)
        self.assertFalse(tampered_result.authorization_valid)
        self.assertFalse(tampered_result.transition_committed)

    def test_same_input_is_deterministic(self) -> None:
        source_state = self.reference_state()
        source_registry = self.nonce_registry()
        first = self.apply(
            reference_state=source_state,
            nonce_registry=source_registry,
        )
        second = self.apply(
            reference_state=source_state,
            nonce_registry=source_registry,
        )
        self.assertEqual(
            tuple(item.to_dict() for item in first),
            tuple(item.to_dict() for item in second),
        )


if __name__ == "__main__":
    unittest.main()
