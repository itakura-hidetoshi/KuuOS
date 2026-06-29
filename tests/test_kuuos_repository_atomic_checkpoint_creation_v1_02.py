from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_atomic_checkpoint_creation_strict_v1_02 import (
    execute_atomic_repository_checkpoint_creation,
    repository_atomic_checkpoint_creation_result_issues,
)
from runtime.kuuos_repository_atomic_checkpoint_creation_types_v1_02 import (
    CHECKPOINT_CREATION_ABORTED,
    CHECKPOINT_CREATION_COMMITTED,
    ZERO_OID,
    repository_atomic_checkpoint_creation_policy_digest,
    repository_atomic_checkpoint_creation_request_digest,
    repository_atomic_checkpoint_creation_result_digest,
    repository_checkpoint_nonce_registry_digest,
    repository_checkpoint_state_digest,
)
from runtime.kuuos_repository_atomic_checkpoint_creation_v1_02 import (
    build_repository_atomic_checkpoint_creation_policy,
    build_repository_atomic_checkpoint_creation_request,
    build_repository_checkpoint_nonce_registry,
    build_repository_checkpoint_state,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_types_v1_01 import (
    repository_local_frontier_checkpoint_authorization_certificate_digest,
)
from tests.test_kuuos_repository_local_frontier_checkpoint_authorization_v1_01 import (
    RepositoryLocalFrontierCheckpointAuthorizationV101Tests,
)


class RepositoryAtomicCheckpointCreationV102Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryLocalFrontierCheckpointAuthorizationV101Tests(
            methodName="test_valid_authorization_is_deterministic_and_granted"
        )
        fixture.setUp()
        self.v101 = fixture
        self.authorization = fixture._authorize()
        self.authorization_inputs = fixture._values()
        self.authorization_inputs.pop("authorization_id")
        self.transaction_id = self.authorization.transaction_id
        self.executor_id = "kuuos-checkpoint-executor-v102"
        self.policy = self._policy()
        self.source_state = self._state()
        self.source_registry = self._registry()
        self.request = self._request()
        self.started_at = 10_176
        self.completed_at = 10_177

    def _policy(self, **overrides):
        values = {
            "policy_id": "atomic-checkpoint-policy-v102",
            "authorized_executor_ids": (self.executor_id,),
            "max_execution_duration_seconds": 10,
            "max_checkpoint_state_age_seconds": 30,
            "max_nonce_registry_age_seconds": 30,
        }
        values.update(overrides)
        return build_repository_atomic_checkpoint_creation_policy(**values)

    def _state(self, **overrides):
        values = {
            "state_id": "checkpoint-state-v102-001",
            "repository_id": self.authorization.repository_id,
            "git_dir_fingerprint": self.authorization.git_dir_fingerprint,
            "checkpoint_reference": self.authorization.checkpoint_reference,
            "current_oid": ZERO_OID,
            "direct": True,
            "symbolic": False,
            "reference_store_source": True,
            "working_tree_source": False,
            "reflog_source": False,
            "remote_source": False,
            "sequence_number": 7,
            "observed_at_epoch_seconds": 10_175,
        }
        values.update(overrides)
        return build_repository_checkpoint_state(**values)

    def _registry(self, **overrides):
        nonce_status = self.authorization_inputs["nonce_status"]
        values = {
            "registry_id": "checkpoint-nonce-registry-v102-001",
            "authority_id": nonce_status.authority_id,
            "upstream_snapshot_digest": nonce_status.registry_snapshot_digest,
            "consumed_nonces": (),
            "revoked_nonces": (),
            "sequence_number": 11,
            "observed_at_epoch_seconds": 10_175,
        }
        values.update(overrides)
        return build_repository_checkpoint_nonce_registry(**values)

    def _request(self, authorization=None, **overrides):
        authorization = authorization or self.authorization
        scope = self.authorization_inputs["scope"]
        values = {
            "request_id": "atomic-checkpoint-request-v102-001",
            "transaction_id": self.transaction_id,
            "authorization": authorization,
            "authorization_scope_digest": scope.scope_digest,
            "authorization_nonce": scope.authorization_nonce,
            "executor_id": self.executor_id,
            "requested_at_epoch_seconds": 10_175,
        }
        values.update(overrides)
        return build_repository_atomic_checkpoint_creation_request(**values)

    def _values(self, **overrides):
        values = {
            "transaction_id": self.transaction_id,
            "authorization": self.authorization,
            "authorization_inputs": self.authorization_inputs,
            "policy": self.policy,
            "request": self.request,
            "source_checkpoint_state": self.source_state,
            "source_nonce_registry": self.source_registry,
            "execution_started_at_epoch_seconds": self.started_at,
            "execution_completed_at_epoch_seconds": self.completed_at,
        }
        values.update(overrides)
        return values

    def _execute(self, **overrides):
        return execute_atomic_repository_checkpoint_creation(
            **self._values(**overrides)
        )

    def _issues(self, result, final_state, final_registry, **overrides):
        values = self._values(**overrides)
        values.pop("transaction_id")
        return repository_atomic_checkpoint_creation_result_issues(
            result,
            final_state,
            final_registry,
            **values,
        )

    @staticmethod
    def _resign_policy(policy):
        policy = replace(policy, policy_digest="")
        return replace(
            policy,
            policy_digest=repository_atomic_checkpoint_creation_policy_digest(
                policy
            ),
        )

    @staticmethod
    def _resign_request(request):
        request = replace(request, request_digest="")
        return replace(
            request,
            request_digest=repository_atomic_checkpoint_creation_request_digest(
                request
            ),
        )

    @staticmethod
    def _resign_state(state):
        state = replace(state, state_digest="")
        return replace(
            state,
            state_digest=repository_checkpoint_state_digest(state),
        )

    @staticmethod
    def _resign_registry(registry):
        registry = replace(registry, registry_digest="")
        return replace(
            registry,
            registry_digest=repository_checkpoint_nonce_registry_digest(registry),
        )

    @staticmethod
    def _resign_result(result):
        result = replace(result, result_digest="")
        return replace(
            result,
            result_digest=repository_atomic_checkpoint_creation_result_digest(
                result
            ),
        )

    @staticmethod
    def _resign_authorization(authorization):
        authorization = replace(authorization, certificate_digest="")
        return replace(
            authorization,
            certificate_digest=(
                repository_local_frontier_checkpoint_authorization_certificate_digest(
                    authorization
                )
            ),
        )

    def test_valid_creation_is_deterministic_and_committed(self) -> None:
        first = self._execute()
        second = self._execute()
        self.assertEqual(first, second)
        result, final_state, final_registry = first
        self.assertEqual(result.status, CHECKPOINT_CREATION_COMMITTED)
        self.assertEqual(final_state.current_oid, self.authorization.proposed_new_oid)
        self.assertIn(
            self.request.authorization_nonce,
            final_registry.consumed_nonces,
        )
        self.assertEqual(self._issues(result, final_state, final_registry), ())

    def test_commit_updates_state_and_nonce_registry_atomically(self) -> None:
        result, final_state, final_registry = self._execute()
        self.assertTrue(result.atomic_checkpoint_nonce_transition)
        self.assertTrue(result.checkpoint_creation_transition_committed)
        self.assertTrue(result.checkpoint_state_mutated)
        self.assertTrue(result.checkpoint_created)
        self.assertTrue(result.nonce_consumed)
        self.assertEqual(
            final_state.sequence_number,
            self.source_state.sequence_number + 1,
        )
        self.assertEqual(
            final_registry.sequence_number,
            self.source_registry.sequence_number + 1,
        )
        self.assertEqual(
            final_registry.upstream_snapshot_digest,
            self.source_registry.registry_digest,
        )

    def test_commit_binds_exact_repository_reference_tip_and_nonce(self) -> None:
        result, final_state, final_registry = self._execute()
        self.assertEqual(result.repository_id, self.authorization.repository_id)
        self.assertEqual(
            result.git_dir_fingerprint,
            self.authorization.git_dir_fingerprint,
        )
        self.assertEqual(
            result.checkpoint_reference,
            self.authorization.checkpoint_reference,
        )
        self.assertEqual(result.expected_old_oid, ZERO_OID)
        self.assertEqual(result.proposed_new_oid, self.authorization.proposed_new_oid)
        self.assertEqual(
            final_state.checkpoint_reference,
            self.authorization.checkpoint_reference,
        )
        self.assertIn(result.authorization_nonce, final_registry.consumed_nonces)

    def test_existing_checkpoint_causes_cas_abort_without_nonce_consumption(self) -> None:
        state = self._state(current_oid="b" * 40)
        result, final_state, final_registry = self._execute(
            source_checkpoint_state=state
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertTrue(result.compare_and_swap_attempted)
        self.assertFalse(result.compare_and_swap_succeeded)
        self.assertFalse(result.checkpoint_absent_before_creation)
        self.assertIs(final_state, state)
        self.assertIs(final_registry, self.source_registry)
        self.assertNotIn(
            self.request.authorization_nonce,
            final_registry.consumed_nonces,
        )

    def test_every_abort_preserves_both_source_states_exactly(self) -> None:
        cases = (
            {"request": self._request(executor_id="unauthorized-v102")},
            {"source_checkpoint_state": self._state(direct=False)},
            {"source_checkpoint_state": self._state(symbolic=True)},
            {
                "source_checkpoint_state": self._state(
                    reference_store_source=False
                )
            },
            {
                "source_checkpoint_state": self._state(
                    working_tree_source=True
                )
            },
            {"source_checkpoint_state": self._state(reflog_source=True)},
            {"source_checkpoint_state": self._state(remote_source=True)},
        )
        for changes in cases:
            source_state = changes.get(
                "source_checkpoint_state",
                self.source_state,
            )
            result, final_state, final_registry = self._execute(**changes)
            self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
            self.assertIs(final_state, source_state)
            self.assertIs(final_registry, self.source_registry)
            self.assertTrue(result.failure_preserved_checkpoint_state)
            self.assertTrue(result.failure_preserved_nonce_registry)
            self.assertFalse(result.nonce_consumed)

    def test_repository_or_checkpoint_binding_mismatch_aborts(self) -> None:
        cases = (
            self._state(repository_id="different-repository-v102"),
            self._state(
                checkpoint_reference="refs/kuuos/checkpoints/different-v102"
            ),
            self._state(git_dir_fingerprint="b" * 64),
        )
        for state in cases:
            result, final_state, final_registry = self._execute(
                source_checkpoint_state=state
            )
            self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
            self.assertFalse(result.checkpoint_state_binding_exact)
            self.assertIs(final_state, state)
            self.assertIs(final_registry, self.source_registry)

    def test_stale_checkpoint_state_aborts(self) -> None:
        state = self._state(observed_at_epoch_seconds=10_100)
        result, final_state, final_registry = self._execute(
            source_checkpoint_state=state
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.checkpoint_state_fresh)
        self.assertIs(final_state, state)
        self.assertIs(final_registry, self.source_registry)

    def test_nonce_registry_authority_or_snapshot_mismatch_aborts(self) -> None:
        cases = (
            self._registry(authority_id="different-authority-v102"),
            self._registry(upstream_snapshot_digest="b" * 64),
        )
        for registry in cases:
            result, final_state, final_registry = self._execute(
                source_nonce_registry=registry
            )
            self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
            self.assertIs(final_state, self.source_state)
            self.assertIs(final_registry, registry)
            self.assertFalse(result.nonce_consumed)

    def test_consumed_or_revoked_nonce_aborts(self) -> None:
        nonce = self.request.authorization_nonce
        cases = (
            self._registry(consumed_nonces=(nonce,)),
            self._registry(revoked_nonces=(nonce,)),
        )
        for registry in cases:
            result, final_state, final_registry = self._execute(
                source_nonce_registry=registry
            )
            self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
            self.assertFalse(result.nonce_unused and result.nonce_not_revoked)
            self.assertIs(final_state, self.source_state)
            self.assertIs(final_registry, registry)

    def test_stale_nonce_registry_aborts(self) -> None:
        registry = self._registry(observed_at_epoch_seconds=10_100)
        result, final_state, final_registry = self._execute(
            source_nonce_registry=registry
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.nonce_registry_fresh)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, registry)

    def test_expired_authorization_aborts(self) -> None:
        result, final_state, final_registry = self._execute(
            execution_started_at_epoch_seconds=10_201,
            execution_completed_at_epoch_seconds=10_202,
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.authorization_not_expired_at_execution)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_execution_duration_bound_aborts(self) -> None:
        result, final_state, final_registry = self._execute(
            execution_completed_at_epoch_seconds=10_190,
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.execution_duration_within_policy)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_future_request_evidence_aborts(self) -> None:
        request = self._resign_request(
            replace(self.request, requested_at_epoch_seconds=10_180)
        )
        result, final_state, final_registry = self._execute(request=request)
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.no_future_evidence)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_transaction_mismatch_aborts(self) -> None:
        request = self._request(transaction_id="different-transaction-v102")
        result, final_state, final_registry = self._execute(
            transaction_id="different-transaction-v102",
            request=request,
        )
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.authorization_binding_exact)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_authorization_scope_digest_mismatch_aborts(self) -> None:
        request = self._resign_request(
            replace(self.request, authorization_scope_digest="b" * 64)
        )
        result, final_state, final_registry = self._execute(request=request)
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.authorization_binding_exact)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_proposed_tip_mismatch_aborts(self) -> None:
        request = self._resign_request(
            replace(self.request, proposed_new_oid="b" * 40)
        )
        result, final_state, final_registry = self._execute(request=request)
        self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
        self.assertFalse(result.authorization_binding_exact)
        self.assertIs(final_state, self.source_state)
        self.assertIs(final_registry, self.source_registry)

    def test_create_flag_and_forbidden_requests_abort(self) -> None:
        cases = (
            {"create_requested": False},
            {"overwrite_requested": True},
            {"delete_requested": True},
            {"force_update_requested": True},
            {"tag_creation_requested": True},
            {"push_requested": True},
        )
        for changes in cases:
            request = self._resign_request(replace(self.request, **changes))
            result, final_state, final_registry = self._execute(request=request)
            self.assertEqual(result.status, CHECKPOINT_CREATION_ABORTED)
            self.assertIs(final_state, self.source_state)
            self.assertIs(final_registry, self.source_registry)
            self.assertFalse(result.checkpoint_created)
            self.assertFalse(result.nonce_consumed)

    def test_policy_cannot_enable_overwrite_force_delete_tag_or_push(self) -> None:
        for field in (
            "allow_checkpoint_overwrite",
            "allow_force_update",
            "allow_reference_delete",
            "allow_tag_creation",
            "allow_push",
        ):
            policy = self._resign_policy(replace(self.policy, **{field: True}))
            with self.assertRaisesRegex(
                ValueError,
                "atomic_checkpoint_policy_invalid",
            ):
                self._execute(policy=policy)

    def test_authorization_tamper_is_rejected_after_digest_recompute(self) -> None:
        authorization = self._resign_authorization(
            replace(self.authorization, checkpoint_creation_authorized=False)
        )
        with self.assertRaisesRegex(ValueError, "checkpoint_authorization_invalid"):
            self._execute(authorization=authorization)

    def test_committed_result_has_no_live_or_unrelated_effect(self) -> None:
        result, _, _ = self._execute()
        for field in (
            "checkpoint_overwrite_performed",
            "force_update_performed",
            "reference_delete_performed",
            "branch_updated",
            "tag_updated",
            "remote_reference_updated",
            "push_performed",
            "index_write_performed",
            "working_tree_write_performed",
            "object_database_write_performed",
            "reflog_write_performed",
            "signing_performed",
            "live_git_command_invoked",
            "live_repository_mutated",
        ):
            self.assertFalse(getattr(result, field))

    def test_result_tamper_is_detected_after_digest_recompute(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered = self._resign_result(
            replace(result, push_performed=True, live_repository_mutated=True)
        )
        issues = self._issues(tampered, final_state, final_registry)
        self.assertIn("atomic_checkpoint_recomputation_mismatch", issues)
        self.assertIn("atomic_checkpoint_forbidden_effect", issues)

    def test_final_state_tamper_is_detected(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered_state = self._resign_state(
            replace(final_state, current_oid="b" * 40)
        )
        issues = self._issues(result, tampered_state, final_registry)
        self.assertIn("atomic_checkpoint_final_state_mismatch", issues)
        self.assertIn("atomic_checkpoint_final_oid_mismatch", issues)

    def test_final_registry_tamper_is_detected(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered_registry = self._resign_registry(
            replace(final_registry, consumed_nonces=())
        )
        issues = self._issues(result, final_state, tampered_registry)
        self.assertIn("atomic_checkpoint_final_registry_mismatch", issues)
        self.assertIn("atomic_checkpoint_nonce_not_consumed", issues)


if __name__ == "__main__":
    unittest.main()
