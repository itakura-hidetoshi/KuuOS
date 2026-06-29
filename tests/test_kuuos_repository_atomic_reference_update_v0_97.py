from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_atomic_reference_update_strict_v0_97 import (
    execute_atomic_repository_reference_update,
    repository_atomic_reference_update_result_issues,
)
from runtime.kuuos_repository_atomic_reference_update_types_v0_97 import (
    REFERENCE_UPDATE_ABORTED,
    REFERENCE_UPDATE_COMMITTED,
    repository_atomic_reference_update_request_digest,
    repository_atomic_reference_update_result_digest,
    repository_reference_nonce_registry_digest,
    repository_reference_state_digest,
)
from runtime.kuuos_repository_atomic_reference_update_v0_97 import (
    build_repository_atomic_reference_update_policy,
    build_repository_atomic_reference_update_request,
    build_repository_reference_nonce_registry,
    build_repository_reference_state,
)
from runtime.kuuos_repository_reference_update_authorization_types_v0_96 import (
    repository_reference_update_authorization_certificate_digest,
)
from tests.test_kuuos_repository_reference_update_authorization_v0_96 import (
    RepositoryReferenceUpdateAuthorizationV096Tests,
)


class RepositoryAtomicReferenceUpdateV097Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryReferenceUpdateAuthorizationV096Tests(
            methodName="test_valid_fast_forward_authorization_is_deterministic"
        )
        fixture.setUp()
        self.v096 = fixture
        self.authorization = fixture._authorize()
        self.authorization_inputs = fixture._authorization_values()
        self.authorization_inputs.pop("authorization_id")
        self.transaction_id = "reference-update-transaction-v097-001"
        self.executor_id = "kuuos-reference-executor-v097"
        self.policy = self._policy()
        self.source_state = self._state()
        self.source_registry = self._registry()
        self.request = self._request()

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-atomic-reference-update-policy-v097",
            "authorized_executor_ids": (self.executor_id,),
            "max_execution_duration_seconds": 10,
            "max_reference_state_age_seconds": 30,
            "max_nonce_registry_age_seconds": 30,
        }
        values.update(overrides)
        return build_repository_atomic_reference_update_policy(**values)

    def _state(self, **overrides):
        values = {
            "state_id": "repository-reference-state-v097-source",
            "repository_id": self.authorization.repository_id,
            "git_dir_fingerprint": self.authorization.git_dir_fingerprint,
            "target_reference": self.authorization.target_reference,
            "current_oid": self.authorization.expected_old_oid,
            "direct": True,
            "symbolic": False,
            "reference_store_source": True,
            "working_tree_source": False,
            "sequence_number": 7,
            "observed_at_epoch_seconds": 10_051,
        }
        values.update(overrides)
        return build_repository_reference_state(**values)

    def _registry(self, **overrides):
        values = {
            "registry_id": "repository-reference-nonce-registry-v097-source",
            "authority_id": self.v096.nonce_status.authority_id,
            "upstream_snapshot_digest": self.v096.nonce_status.registry_snapshot_digest,
            "consumed_nonces": (),
            "revoked_nonces": (),
            "sequence_number": 11,
            "observed_at_epoch_seconds": 10_051,
        }
        values.update(overrides)
        return build_repository_reference_nonce_registry(**values)

    def _request(self, authorization=None, **overrides):
        values = {
            "request_id": "repository-atomic-reference-update-request-v097-001",
            "transaction_id": self.transaction_id,
            "authorization": authorization or self.authorization,
            "authorization_scope_digest": self.v096.scope.scope_digest,
            "authorization_nonce": self.v096.scope.authorization_nonce,
            "executor_id": self.executor_id,
            "requested_at_epoch_seconds": 10_051,
            "force_update_requested": False,
            "delete_requested": False,
            "push_requested": False,
        }
        values.update(overrides)
        return build_repository_atomic_reference_update_request(**values)

    def _values(self, **overrides):
        values = {
            "transaction_id": self.transaction_id,
            "authorization": self.authorization,
            "authorization_inputs": self.authorization_inputs,
            "policy": self.policy,
            "request": self.request,
            "source_reference_state": self.source_state,
            "source_nonce_registry": self.source_registry,
            "execution_started_at_epoch_seconds": 10_052,
            "execution_completed_at_epoch_seconds": 10_054,
        }
        values.update(overrides)
        return values

    def _execute(self, **overrides):
        return execute_atomic_repository_reference_update(**self._values(**overrides))

    def _issues(self, result, final_state, final_registry, **overrides):
        values = self._values(**overrides)
        values.pop("transaction_id")
        return repository_atomic_reference_update_result_issues(
            result,
            final_state,
            final_registry,
            **values,
        )

    @staticmethod
    def _resign_request(request):
        request = replace(request, request_digest="")
        return replace(
            request,
            request_digest=repository_atomic_reference_update_request_digest(request),
        )

    @staticmethod
    def _resign_result(result):
        result = replace(result, result_digest="")
        return replace(
            result,
            result_digest=repository_atomic_reference_update_result_digest(result),
        )

    @staticmethod
    def _resign_state(state):
        state = replace(state, state_digest="")
        return replace(state, state_digest=repository_reference_state_digest(state))

    @staticmethod
    def _resign_registry(registry):
        registry = replace(registry, registry_digest="")
        return replace(
            registry,
            registry_digest=repository_reference_nonce_registry_digest(registry),
        )

    def test_valid_atomic_reference_update_is_deterministic(self) -> None:
        first = self._execute()
        second = self._execute()
        self.assertEqual(first, second)
        result, final_state, final_registry = first
        self.assertEqual(result.status, REFERENCE_UPDATE_COMMITTED)
        self.assertEqual(self._issues(result, final_state, final_registry), ())

    def test_commit_updates_exact_reference_and_consumes_exact_nonce(self) -> None:
        result, final_state, final_registry = self._execute()
        self.assertEqual(final_state.current_oid, self.authorization.proposed_new_oid)
        self.assertEqual(final_state.target_reference, self.authorization.target_reference)
        self.assertIn(self.v096.scope.authorization_nonce, final_registry.consumed_nonces)
        self.assertTrue(result.atomic_reference_nonce_transition)
        self.assertTrue(result.reference_state_mutated)
        self.assertTrue(result.branch_state_updated)
        self.assertTrue(result.nonce_consumed)

    def test_commit_binds_exact_repository_reference_and_oids(self) -> None:
        result, _, _ = self._execute()
        self.assertEqual(result.repository_id, self.authorization.repository_id)
        self.assertEqual(result.git_dir_fingerprint, self.authorization.git_dir_fingerprint)
        self.assertEqual(result.target_reference, self.authorization.target_reference)
        self.assertEqual(result.expected_old_oid, self.authorization.expected_old_oid)
        self.assertEqual(result.proposed_new_oid, self.authorization.proposed_new_oid)
        self.assertTrue(result.authorization_binding_exact)
        self.assertTrue(result.reference_state_binding_exact)

    def test_compare_and_swap_mismatch_aborts_without_nonce_consumption(self) -> None:
        source_state = self._state(current_oid="1" * 40)
        result, final_state, final_registry = self._execute(
            source_reference_state=source_state
        )
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertTrue(result.compare_and_swap_attempted)
        self.assertFalse(result.compare_and_swap_succeeded)
        self.assertFalse(result.current_oid_matches_expected_old)
        self.assertEqual(final_state, source_state)
        self.assertEqual(final_registry, self.source_registry)
        self.assertFalse(result.nonce_consumed)

    def test_consumed_nonce_aborts_before_compare_and_swap(self) -> None:
        registry = self._registry(
            consumed_nonces=(self.v096.scope.authorization_nonce,)
        )
        result, final_state, final_registry = self._execute(
            source_nonce_registry=registry
        )
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.nonce_unused)
        self.assertFalse(result.compare_and_swap_attempted)
        self.assertEqual(final_state, self.source_state)
        self.assertEqual(final_registry, registry)

    def test_revoked_nonce_aborts_before_compare_and_swap(self) -> None:
        registry = self._registry(
            revoked_nonces=(self.v096.scope.authorization_nonce,)
        )
        result, _, final_registry = self._execute(source_nonce_registry=registry)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.nonce_not_revoked)
        self.assertFalse(result.compare_and_swap_attempted)
        self.assertEqual(final_registry, registry)

    def test_nonce_registry_snapshot_mismatch_aborts(self) -> None:
        registry = self._registry(upstream_snapshot_digest="b" * 64)
        result, _, _ = self._execute(source_nonce_registry=registry)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.nonce_registry_snapshot_bound)

    def test_unauthorized_executor_aborts(self) -> None:
        request = self._request(executor_id="unauthorized-executor-v097")
        result, _, _ = self._execute(request=request)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.executor_authorized)

    def test_transaction_id_mismatch_aborts(self) -> None:
        request = self._request(transaction_id="different-transaction-v097")
        result, _, _ = self._execute(request=request)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.request_binding_exact)

    def test_request_old_or_new_oid_mismatch_aborts(self) -> None:
        for field, value in (
            ("expected_old_oid", "2" * 40),
            ("proposed_new_oid", "3" * 40),
        ):
            request = self._resign_request(replace(self.request, **{field: value}))
            result, _, _ = self._execute(request=request)
            self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
            self.assertFalse(result.authorization_binding_exact)

    def test_repository_or_reference_state_mismatch_aborts(self) -> None:
        for field, value in (
            ("repository_id", "different-repository-v097"),
            ("target_reference", "refs/heads/other"),
        ):
            state = self._state(**{field: value})
            result, _, _ = self._execute(source_reference_state=state)
            self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
            self.assertFalse(result.reference_state_binding_exact)

    def test_stale_reference_state_aborts(self) -> None:
        state = self._state(observed_at_epoch_seconds=9_900)
        result, _, _ = self._execute(source_reference_state=state)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.reference_state_fresh)

    def test_stale_nonce_registry_aborts(self) -> None:
        registry = self._registry(observed_at_epoch_seconds=9_900)
        result, _, _ = self._execute(source_nonce_registry=registry)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.nonce_registry_fresh)

    def test_symbolic_or_indirect_reference_aborts(self) -> None:
        for changes in (
            {"direct": False},
            {"symbolic": True},
        ):
            state = self._state(**changes)
            result, _, _ = self._execute(source_reference_state=state)
            self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)

    def test_non_reference_store_or_working_tree_source_aborts(self) -> None:
        for changes in (
            {"reference_store_source": False},
            {"working_tree_source": True},
        ):
            state = self._state(**changes)
            result, _, _ = self._execute(source_reference_state=state)
            self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)

    def test_expired_authorization_aborts(self) -> None:
        result, _, _ = self._execute(
            execution_started_at_epoch_seconds=10_101,
            execution_completed_at_epoch_seconds=10_102,
        )
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.authorization_not_expired_at_execution)

    def test_execution_duration_bound_is_enforced(self) -> None:
        result, _, _ = self._execute(execution_completed_at_epoch_seconds=10_063)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.execution_duration_within_policy)

    def test_future_request_or_state_evidence_aborts(self) -> None:
        request = self._request(requested_at_epoch_seconds=10_060)
        result, _, _ = self._execute(request=request)
        self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)
        self.assertFalse(result.no_future_evidence)

    def test_force_delete_and_push_requests_abort(self) -> None:
        for field in (
            "force_update_requested",
            "delete_requested",
            "push_requested",
        ):
            request = self._request(**{field: True})
            result, _, _ = self._execute(request=request)
            self.assertEqual(result.status, REFERENCE_UPDATE_ABORTED)

    def test_abort_preserves_both_state_components(self) -> None:
        request = self._request(executor_id="unauthorized-executor-v097")
        result, final_state, final_registry = self._execute(request=request)
        self.assertTrue(result.failure_preserved_reference_state)
        self.assertTrue(result.failure_preserved_nonce_registry)
        self.assertEqual(final_state, self.source_state)
        self.assertEqual(final_registry, self.source_registry)

    def test_no_live_git_or_unrelated_repository_effect_is_recorded(self) -> None:
        result, _, _ = self._execute()
        for field in (
            "force_update_performed",
            "reference_delete_performed",
            "head_updated",
            "tag_updated",
            "remote_reference_updated",
            "push_performed",
            "index_write_performed",
            "working_tree_write_performed",
            "object_database_write_performed",
            "signing_performed",
            "live_git_command_invoked",
            "live_repository_mutated",
        ):
            self.assertFalse(getattr(result, field))

    def test_result_effect_tamper_is_detected_after_outer_digest_recomputation(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered = self._resign_result(replace(result, push_performed=True))
        issues = self._issues(tampered, final_state, final_registry)
        self.assertIn("atomic_reference_update_recomputation_mismatch", issues)
        self.assertIn("atomic_reference_update_forbidden_effect", issues)

    def test_final_state_tamper_is_detected(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered_state = self._resign_state(
            replace(final_state, current_oid=self.authorization.expected_old_oid)
        )
        issues = self._issues(result, tampered_state, final_registry)
        self.assertIn("atomic_reference_update_final_state_mismatch", issues)
        self.assertIn("atomic_reference_update_final_oid_mismatch", issues)

    def test_final_nonce_registry_tamper_is_detected(self) -> None:
        result, final_state, final_registry = self._execute()
        tampered_registry = self._resign_registry(
            replace(final_registry, consumed_nonces=())
        )
        issues = self._issues(result, final_state, tampered_registry)
        self.assertIn("atomic_reference_update_final_registry_mismatch", issues)
        self.assertIn("atomic_reference_update_nonce_not_consumed", issues)

    def test_outer_authorization_digest_recomputation_cannot_hide_tamper(self) -> None:
        authorization = replace(
            self.authorization,
            reference_update_authority_granted=False,
            certificate_digest="",
        )
        authorization = replace(
            authorization,
            certificate_digest=repository_reference_update_authorization_certificate_digest(
                authorization
            ),
        )
        request = self._request(authorization=authorization)
        with self.assertRaisesRegex(ValueError, "reference_update_authorization_invalid"):
            self._execute(authorization=authorization, request=request)


if __name__ == "__main__":
    unittest.main()
