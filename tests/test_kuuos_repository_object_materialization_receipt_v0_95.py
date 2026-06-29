from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    GIT_OBJECT_FORMAT_SHA1,
    RepositoryObjectDatabaseEntry,
)
from runtime.kuuos_repository_object_materialization_authorization_v0_94 import (
    build_repository_object_database_observation,
)
from runtime.kuuos_repository_object_materialization_receipt_strict_v0_95 import (
    certify_repository_object_materialization_receipt,
    repository_object_materialization_receipt_issues,
)
from runtime.kuuos_repository_object_materialization_receipt_types_v0_95 import (
    ITEM_REUSED,
    MATERIALIZATION_ABORTED,
    MATERIALIZATION_COMMITTED,
    repository_object_materialization_execution_report_digest,
    repository_object_materialization_nonce_consumption_receipt_digest,
    repository_object_materialization_receipt_digest,
)
from runtime.kuuos_repository_object_materialization_receipt_v0_95 import (
    build_repository_object_materialization_execution_report,
    build_repository_object_materialization_nonce_consumption_receipt,
    build_repository_object_materialization_policy,
)
from tests.test_kuuos_repository_object_materialization_authorization_v0_94 import (
    RepositoryObjectMaterializationAuthorizationV094Tests,
)


class RepositoryObjectMaterializationReceiptV095Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryObjectMaterializationAuthorizationV094Tests(
            methodName="test_authorization_is_deterministic_and_granted"
        )
        fixture.setUp()
        self.fixture = fixture
        self.authorization = fixture._authorize()
        self.executor_id = "kuuos-object-materializer-v095"
        self.policy = self._policy()
        self.execution = self._execution()
        self.post_observation = self._post_observation()
        self.nonce_consumption = self._nonce_consumption()

    def _policy(self, **overrides):
        values = {
            "policy_id": "object-materialization-receipt-policy-v095",
            "authorized_executor_ids": (self.executor_id,),
            "max_materialization_duration_seconds": 60,
            "max_post_observation_age_seconds": 60,
        }
        values.update(overrides)
        return build_repository_object_materialization_policy(**values)

    def _candidate_entries(self, authorization=None):
        authorization = authorization or self.authorization
        return tuple(
            RepositoryObjectDatabaseEntry(
                kind=item.kind,
                oid=item.oid,
                payload_size=item.payload_size,
                payload_digest=item.payload_digest,
            )
            for item in authorization.plan_items
        )

    def _post_observation(self, authorization=None, pre_observation=None, **overrides):
        authorization = authorization or self.authorization
        pre_observation = pre_observation or self.fixture.observation
        parent = next(
            entry
            for entry in pre_observation.existing_objects
            if entry.oid == authorization.parent_commit_sha
        )
        values = {
            "observation_id": "object-materialization-post-observation-v095",
            "repository_id": authorization.repository_id,
            "git_dir_fingerprint": authorization.git_dir_fingerprint,
            "object_format": GIT_OBJECT_FORMAT_SHA1,
            "source_commit_sha": authorization.parent_commit_sha,
            "queried_oids": tuple(item.oid for item in authorization.plan_items)
            + (authorization.parent_commit_sha,),
            "existing_objects": (parent,) + self._candidate_entries(authorization),
            "object_database_read": True,
            "working_tree_read": False,
            "observed_at_epoch_seconds": 10_040,
        }
        values.update(overrides)
        return build_repository_object_database_observation(**values)

    def _execution(self, authorization=None, **overrides):
        authorization = authorization or self.authorization
        values = {
            "execution_id": "object-materialization-transaction-v095-001",
            "authorization": authorization,
            "executor_id": self.executor_id,
            "started_at_epoch_seconds": 10_021,
            "completed_at_epoch_seconds": 10_030,
        }
        values.update(overrides)
        return build_repository_object_materialization_execution_report(**values)

    def _nonce_consumption(self, authorization=None, scope=None, **overrides):
        authorization = authorization or self.authorization
        scope = scope or self.fixture.scope
        values = {
            "transaction_id": "object-materialization-transaction-v095-001",
            "authorization": authorization,
            "scope": scope,
            "registry_before_digest": "c" * 64,
            "registry_after_digest": "d" * 64,
            "consumed_before": False,
            "consumed_after": True,
            "revoked": False,
            "materialization_committed": True,
            "atomic_with_materialization": True,
        }
        values.update(overrides)
        return build_repository_object_materialization_nonce_consumption_receipt(
            **values
        )

    def _certify(self, **overrides):
        values = {
            "authorization": self.authorization,
            "candidate_certificate": self.fixture.candidate,
            "application_receipt": self.fixture.application_receipt,
            "snapshot": self.fixture.snapshot,
            "parent_tree_inventory": self.fixture.parent_inventory,
            "candidate_policy": self.fixture.candidate_policy,
            "authorization_policy": self.fixture.policy,
            "scope": self.fixture.scope,
            "pre_observation": self.fixture.observation,
            "pre_nonce_status": self.fixture.nonce_status,
            "policy": self.policy,
            "execution_report": self.execution,
            "post_observation": self.post_observation,
            "nonce_consumption": self.nonce_consumption,
        }
        values.update(overrides)
        return certify_repository_object_materialization_receipt(**values)

    def _issues(self, receipt, **overrides):
        values = {
            "authorization": self.authorization,
            "candidate_certificate": self.fixture.candidate,
            "application_receipt": self.fixture.application_receipt,
            "snapshot": self.fixture.snapshot,
            "parent_tree_inventory": self.fixture.parent_inventory,
            "candidate_policy": self.fixture.candidate_policy,
            "authorization_policy": self.fixture.policy,
            "scope": self.fixture.scope,
            "pre_observation": self.fixture.observation,
            "pre_nonce_status": self.fixture.nonce_status,
            "policy": self.policy,
            "execution_report": self.execution,
            "post_observation": self.post_observation,
            "nonce_consumption": self.nonce_consumption,
        }
        values.update(overrides)
        return repository_object_materialization_receipt_issues(receipt, **values)

    @staticmethod
    def _resign_execution(report):
        report = replace(report, report_digest="")
        return replace(
            report,
            report_digest=repository_object_materialization_execution_report_digest(
                report
            ),
        )

    @staticmethod
    def _resign_nonce(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=(
                repository_object_materialization_nonce_consumption_receipt_digest(
                    receipt
                )
            ),
        )

    def test_receipt_is_deterministic_and_committed(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, MATERIALIZATION_COMMITTED)
        self.assertTrue(first.object_database_materialization_committed)
        self.assertTrue(first.atomic_state_transition)
        self.assertTrue(first.candidate_commit_present)
        self.assertTrue(first.commit_object_written)
        self.assertEqual(self._issues(first), ())

    def test_written_counts_and_payload_bytes_match_authorization(self) -> None:
        receipt = self._certify()
        self.assertEqual(
            receipt.actual_written_object_count,
            self.authorization.new_object_count,
        )
        self.assertEqual(
            receipt.actual_reused_object_count,
            self.authorization.reused_existing_object_count,
        )
        self.assertEqual(
            receipt.actual_written_payload_bytes,
            self.authorization.new_payload_bytes,
        )

    def test_parent_and_all_candidate_objects_are_verified(self) -> None:
        receipt = self._certify()
        self.assertTrue(receipt.parent_commit_preserved)
        self.assertTrue(receipt.all_candidate_objects_present)
        self.assertTrue(receipt.all_candidate_payloads_exact)
        self.assertTrue(receipt.post_query_set_exact)

    def test_nonce_is_consumed_atomically(self) -> None:
        receipt = self._certify()
        self.assertTrue(receipt.nonce_scope_bound)
        self.assertTrue(receipt.nonce_authorization_bound)
        self.assertTrue(receipt.nonce_unused_before)
        self.assertTrue(receipt.nonce_consumed_after)
        self.assertTrue(receipt.nonce_consumption_committed)
        self.assertTrue(receipt.nonce_atomic_with_materialization)

    def test_forbidden_repository_effects_remain_false(self) -> None:
        receipt = self._certify()
        self.assertFalse(receipt.index_write_performed)
        self.assertFalse(receipt.working_tree_write_performed)
        self.assertFalse(receipt.reference_mutated)
        self.assertFalse(receipt.signing_performed)

    def test_all_existing_objects_can_be_reused_without_new_write(self) -> None:
        pre = self.fixture._observation(
            existing_objects=(self.fixture._parent_entry(),)
            + self._candidate_entries()
        )
        scope = self.fixture._scope(observation=pre)
        nonce_status = self.fixture._nonce(scope=scope)
        authorization = self.fixture._authorize(
            observation=pre,
            scope=scope,
            nonce_status=nonce_status,
        )
        self.assertEqual(authorization.new_object_count, 0)
        execution = self._execution(authorization=authorization)
        post = self._post_observation(
            authorization=authorization,
            pre_observation=pre,
        )
        nonce = self._nonce_consumption(
            authorization=authorization,
            scope=scope,
        )
        receipt = self._certify(
            authorization=authorization,
            scope=scope,
            pre_observation=pre,
            pre_nonce_status=nonce_status,
            execution_report=execution,
            post_observation=post,
            nonce_consumption=nonce,
        )
        self.assertEqual(receipt.status, MATERIALIZATION_COMMITTED)
        self.assertEqual(receipt.actual_written_object_count, 0)
        self.assertEqual(
            receipt.actual_reused_object_count,
            authorization.unique_candidate_object_count,
        )
        self.assertTrue(receipt.reused_objects_preserved)
        self.assertTrue(receipt.candidate_commit_present)
        self.assertFalse(receipt.commit_object_written)

    def test_missing_candidate_object_aborts(self) -> None:
        entries = self.post_observation.existing_objects[:-1]
        post = self._post_observation(existing_objects=entries)
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.all_candidate_objects_present)
        self.assertFalse(receipt.object_database_materialization_committed)

    def test_payload_mismatch_aborts(self) -> None:
        entries = list(self.post_observation.existing_objects)
        target_index = next(
            index
            for index, entry in enumerate(entries)
            if entry.oid != self.authorization.parent_commit_sha
        )
        entries[target_index] = replace(entries[target_index], payload_digest="f" * 64)
        post = self._post_observation(existing_objects=tuple(entries))
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.all_candidate_payloads_exact)

    def test_parent_commit_change_aborts(self) -> None:
        entries = list(self.post_observation.existing_objects)
        parent_index = next(
            index
            for index, entry in enumerate(entries)
            if entry.oid == self.authorization.parent_commit_sha
        )
        entries[parent_index] = replace(entries[parent_index], payload_digest="e" * 64)
        post = self._post_observation(existing_objects=tuple(entries))
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.parent_commit_preserved)

    def test_candidate_commit_missing_aborts(self) -> None:
        entries = tuple(
            entry
            for entry in self.post_observation.existing_objects
            if entry.oid != self.authorization.candidate_commit_oid
        )
        post = self._post_observation(existing_objects=entries)
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.candidate_commit_present)

    def test_incomplete_post_query_and_inventory_abort(self) -> None:
        omitted = self.authorization.plan_items[0].oid
        entries = tuple(
            entry for entry in self.post_observation.existing_objects if entry.oid != omitted
        )
        queries = tuple(
            oid for oid in self.post_observation.queried_oids if oid != omitted
        )
        post = self._post_observation(
            existing_objects=entries,
            queried_oids=queries,
        )
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.post_query_set_exact)

    def test_stale_post_observation_aborts(self) -> None:
        post = self._post_observation(observed_at_epoch_seconds=10_091)
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.post_observation_fresh)

    def test_non_object_database_post_observation_aborts(self) -> None:
        post = self._post_observation(object_database_read=False)
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.post_observation_object_database_source)

    def test_working_tree_post_observation_aborts(self) -> None:
        post = self._post_observation(working_tree_read=True)
        receipt = self._certify(post_observation=post)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.post_observation_working_tree_ignored)

    def test_unauthorized_executor_aborts(self) -> None:
        execution = self._execution(executor_id="unknown-executor")
        receipt = self._certify(execution_report=execution)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.executor_authorized)

    def test_duration_exceeding_policy_aborts(self) -> None:
        execution = self._execution(completed_at_epoch_seconds=10_090)
        post = self._post_observation(observed_at_epoch_seconds=10_095)
        receipt = self._certify(
            execution_report=execution,
            post_observation=post,
        )
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.duration_within_policy)

    def test_completion_after_authorization_expiry_aborts(self) -> None:
        execution = self._execution(completed_at_epoch_seconds=10_101)
        post = self._post_observation(observed_at_epoch_seconds=10_102)
        receipt = self._certify(
            execution_report=execution,
            post_observation=post,
        )
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.authorization_not_expired_at_completion)

    def test_reordered_plan_aborts(self) -> None:
        execution = self._execution(items=tuple(reversed(self.execution.items)))
        receipt = self._certify(execution_report=execution)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.plan_order_exact)

    def test_write_reuse_substitution_aborts(self) -> None:
        items = list(self.execution.items)
        items[0] = replace(items[0], outcome=ITEM_REUSED, write_order=-1)
        execution = self._execution(items=tuple(items))
        receipt = self._certify(execution_report=execution)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.write_set_exact)
        self.assertFalse(receipt.reuse_set_exact)

    def test_missing_execution_item_aborts(self) -> None:
        execution = self._execution(items=self.execution.items[:-1])
        receipt = self._certify(execution_report=execution)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.plan_item_set_exact)

    def test_repository_identity_mismatch_aborts(self) -> None:
        execution = self._resign_execution(
            replace(self.execution, repository_id="github:other/repository")
        )
        receipt = self._certify(execution_report=execution)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.repository_identity_exact)

    def test_nonce_consumed_before_aborts(self) -> None:
        nonce = self._nonce_consumption(consumed_before=True)
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_unused_before)

    def test_nonce_not_consumed_after_aborts(self) -> None:
        nonce = self._nonce_consumption(consumed_after=False)
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_consumed_after)

    def test_revoked_nonce_aborts(self) -> None:
        nonce = self._nonce_consumption(revoked=True)
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_not_revoked)

    def test_non_atomic_nonce_consumption_aborts(self) -> None:
        nonce = self._nonce_consumption(atomic_with_materialization=False)
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_atomic_with_materialization)

    def test_uncommitted_nonce_receipt_aborts(self) -> None:
        nonce = self._nonce_consumption(materialization_committed=False)
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_consumption_committed)

    def test_nonce_scope_mismatch_aborts(self) -> None:
        nonce = self._resign_nonce(
            replace(
                self.nonce_consumption,
                authorization_scope_digest="e" * 64,
            )
        )
        receipt = self._certify(nonce_consumption=nonce)
        self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
        self.assertFalse(receipt.nonce_scope_bound)

    def test_forbidden_side_effects_abort(self) -> None:
        for field in (
            "index_write_performed",
            "working_tree_write_performed",
            "reference_mutated",
            "signing_performed",
        ):
            execution = self._execution(**{field: True})
            receipt = self._certify(execution_report=execution)
            self.assertEqual(receipt.status, MATERIALIZATION_ABORTED)
            self.assertTrue(getattr(receipt, field))

    def test_authorization_tamper_fails_closed(self) -> None:
        authorization = replace(
            self.authorization,
            candidate_commit_oid="f" * 40,
            certificate_digest="",
        )
        with self.assertRaisesRegex(
            ValueError,
            "object_materialization_authorization_invalid",
        ):
            self._certify(authorization=authorization)

    def test_receipt_tamper_is_detected_after_digest_recomputation(self) -> None:
        receipt = self._certify()
        tampered = replace(
            receipt,
            candidate_commit_present=False,
            receipt_digest="",
        )
        tampered = replace(
            tampered,
            receipt_digest=repository_object_materialization_receipt_digest(tampered),
        )
        self.assertIn(
            "object_materialization_receipt_recomputation_mismatch",
            self._issues(tampered),
        )


if __name__ == "__main__":
    unittest.main()
