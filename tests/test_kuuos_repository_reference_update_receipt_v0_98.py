from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_atomic_reference_update_types_v0_97 import (
    repository_atomic_reference_update_result_digest,
)
from runtime.kuuos_repository_reference_update_receipt_strict_v0_98 import (
    certify_repository_reference_update_receipt,
    repository_reference_update_receipt_issues,
)
from runtime.kuuos_repository_reference_update_receipt_types_v0_98 import (
    RECEIPT_COMMITTED,
    RECEIPT_REJECTED,
    repository_post_reference_observation_digest,
    repository_reference_nonce_consumption_receipt_digest,
    repository_reference_update_execution_report_digest,
    repository_reference_update_receipt_digest,
)
from runtime.kuuos_repository_reference_update_receipt_v0_98 import (
    build_repository_post_reference_observation,
    build_repository_reference_nonce_consumption_receipt,
    build_repository_reference_update_execution_report,
    build_repository_reference_update_receipt_policy,
)
from tests.test_kuuos_repository_atomic_reference_update_v0_97 import (
    RepositoryAtomicReferenceUpdateV097Tests,
)


class RepositoryReferenceUpdateReceiptV098Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryAtomicReferenceUpdateV097Tests(
            methodName="test_valid_atomic_reference_update_is_deterministic"
        )
        fixture.setUp()
        self.v097 = fixture
        (
            self.atomic_result,
            self.final_reference_state,
            self.final_nonce_registry,
        ) = fixture._execute()
        self.atomic_update_inputs = fixture._values()
        self.atomic_update_inputs.pop("transaction_id")
        self.observer_id = "kuuos-reference-observer-v098"
        self.policy = self._policy()
        self.execution_report = self._execution_report()
        self.post_observation = self._post_observation()
        self.nonce_receipt = self._nonce_receipt()

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-reference-update-receipt-policy-v098",
            "authorized_observer_ids": (self.observer_id,),
            "max_execution_report_age_seconds": 30,
            "max_post_reference_observation_age_seconds": 30,
            "max_nonce_consumption_receipt_age_seconds": 30,
        }
        values.update(overrides)
        return build_repository_reference_update_receipt_policy(**values)

    def _execution_report(self, atomic_result=None, **overrides):
        values = {
            "report_id": "repository-reference-update-execution-v098-001",
            "atomic_update_result": atomic_result or self.atomic_result,
            "executor_id": self.atomic_result.executor_id,
            "reference_update_attempted": True,
            "reference_update_performed": True,
            "compare_and_swap_succeeded": True,
            "branch_updated": True,
            "nonce_consumed": True,
            "execution_started_at_epoch_seconds": 10_052,
            "execution_completed_at_epoch_seconds": 10_054,
        }
        values.update(overrides)
        return build_repository_reference_update_execution_report(**values)

    def _post_observation(self, atomic_result=None, final_state=None, **overrides):
        values = {
            "observation_id": "repository-post-reference-observation-v098-001",
            "observer_id": self.observer_id,
            "atomic_update_result": atomic_result or self.atomic_result,
            "final_reference_state": final_state or self.final_reference_state,
            "observed_at_epoch_seconds": 10_055,
        }
        values.update(overrides)
        return build_repository_post_reference_observation(**values)

    def _nonce_receipt(
        self,
        atomic_result=None,
        source_registry=None,
        final_registry=None,
        **overrides,
    ):
        values = {
            "receipt_id": "repository-reference-nonce-consumption-v098-001",
            "observer_id": self.observer_id,
            "atomic_update_result": atomic_result or self.atomic_result,
            "source_nonce_registry": (
                source_registry or self.v097.source_registry
            ),
            "final_nonce_registry": final_registry or self.final_nonce_registry,
            "consumed_at_epoch_seconds": 10_055,
        }
        values.update(overrides)
        return build_repository_reference_nonce_consumption_receipt(**values)

    def _values(self, **overrides):
        values = {
            "receipt_id": "repository-reference-update-receipt-v098-001",
            "atomic_update_result": self.atomic_result,
            "final_reference_state": self.final_reference_state,
            "final_nonce_registry": self.final_nonce_registry,
            "atomic_update_inputs": self.atomic_update_inputs,
            "policy": self.policy,
            "execution_report": self.execution_report,
            "post_reference_observation": self.post_observation,
            "nonce_consumption_receipt": self.nonce_receipt,
            "evaluated_at_epoch_seconds": 10_056,
        }
        values.update(overrides)
        return values

    def _certify(self, **overrides):
        return certify_repository_reference_update_receipt(
            **self._values(**overrides)
        )

    def _issues(self, receipt, **overrides):
        values = self._values(**overrides)
        values.pop("receipt_id")
        return repository_reference_update_receipt_issues(receipt, **values)

    @staticmethod
    def _resign_report(report):
        report = replace(report, report_digest="")
        return replace(
            report,
            report_digest=repository_reference_update_execution_report_digest(
                report
            ),
        )

    @staticmethod
    def _resign_observation(observation):
        observation = replace(observation, receipt_digest="")
        return replace(
            observation,
            receipt_digest=repository_post_reference_observation_digest(
                observation
            ),
        )

    @staticmethod
    def _resign_nonce_receipt(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=repository_reference_nonce_consumption_receipt_digest(
                receipt
            ),
        )

    @staticmethod
    def _resign_receipt(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=repository_reference_update_receipt_digest(receipt),
        )

    def test_valid_receipt_is_deterministic_and_committed(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, RECEIPT_COMMITTED)
        self.assertTrue(first.receipt_committed)
        self.assertTrue(first.reference_update_confirmed)
        self.assertTrue(first.atomic_reference_nonce_transition_confirmed)
        self.assertEqual(self._issues(first), ())

    def test_receipt_binds_exact_repository_reference_and_oids(self) -> None:
        receipt = self._certify()
        self.assertEqual(receipt.repository_id, self.atomic_result.repository_id)
        self.assertEqual(
            receipt.git_dir_fingerprint,
            self.atomic_result.git_dir_fingerprint,
        )
        self.assertEqual(receipt.target_reference, self.atomic_result.target_reference)
        self.assertEqual(receipt.expected_old_oid, self.atomic_result.expected_old_oid)
        self.assertEqual(receipt.proposed_new_oid, self.atomic_result.proposed_new_oid)
        self.assertTrue(receipt.atomic_update_binding_exact)

    def test_receipt_binds_exact_transaction_and_nonce(self) -> None:
        receipt = self._certify()
        self.assertEqual(receipt.transaction_id, self.atomic_result.transaction_id)
        self.assertEqual(
            receipt.authorization_nonce,
            self.atomic_result.authorization_nonce,
        )
        self.assertTrue(receipt.transaction_binding_exact)
        self.assertTrue(receipt.nonce_consumption_confirmed)

    def test_execution_report_transaction_mismatch_is_rejected(self) -> None:
        report = self._resign_report(
            replace(self.execution_report, transaction_id="different-v098")
        )
        receipt = self._certify(execution_report=report)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.execution_report_binding_exact)
        self.assertFalse(receipt.transaction_binding_exact)

    def test_execution_report_result_digest_mismatch_is_rejected(self) -> None:
        report = self._resign_report(
            replace(
                self.execution_report,
                atomic_update_result_digest="a" * 64,
            )
        )
        receipt = self._certify(execution_report=report)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.execution_report_binding_exact)

    def test_execution_report_timing_mismatch_is_rejected(self) -> None:
        report = self._resign_report(
            replace(
                self.execution_report,
                execution_started_at_epoch_seconds=10_051,
            )
        )
        receipt = self._certify(execution_report=report)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.execution_timing_exact)

    def test_unperformed_reference_update_is_rejected(self) -> None:
        for field in (
            "reference_update_attempted",
            "reference_update_performed",
            "compare_and_swap_succeeded",
            "branch_updated",
            "nonce_consumed",
        ):
            report = self._resign_report(
                replace(self.execution_report, **{field: False})
            )
            receipt = self._certify(execution_report=report)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)

    def test_force_delete_push_and_unrelated_effects_are_rejected(self) -> None:
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
        ):
            report = self._resign_report(
                replace(self.execution_report, **{field: True})
            )
            receipt = self._certify(execution_report=report)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.no_forbidden_execution_effect)

    def test_post_reference_oid_mismatch_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(self.post_observation, observed_oid="1" * 40)
        )
        receipt = self._certify(post_reference_observation=observation)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.post_reference_oid_exact)

    def test_post_reference_transaction_or_repository_mismatch_is_rejected(self) -> None:
        for field, value in (
            ("transaction_id", "different-v098"),
            ("repository_id", "different-repository-v098"),
            ("target_reference", "refs/heads/other"),
        ):
            observation = self._resign_observation(
                replace(self.post_observation, **{field: value})
            )
            receipt = self._certify(post_reference_observation=observation)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.post_reference_observation_binding_exact)

    def test_symbolic_indirect_or_working_tree_observation_is_rejected(self) -> None:
        for changes in (
            {"direct": False},
            {"symbolic": True},
            {"reference_store_read": False},
            {"working_tree_read": True},
        ):
            observation = self._resign_observation(
                replace(self.post_observation, **changes)
            )
            receipt = self._certify(post_reference_observation=observation)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)

    def test_post_reference_sequence_mismatch_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(
                self.post_observation,
                sequence_number=self.post_observation.sequence_number + 1,
            )
        )
        receipt = self._certify(post_reference_observation=observation)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.post_reference_sequence_exact)

    def test_stale_execution_report_is_rejected(self) -> None:
        receipt = self._certify(evaluated_at_epoch_seconds=10_100)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.execution_report_fresh)

    def test_stale_post_observation_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(self.post_observation, observed_at_epoch_seconds=10_000)
        )
        receipt = self._certify(post_reference_observation=observation)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.post_reference_observation_fresh)

    def test_nonce_receipt_transaction_or_nonce_mismatch_is_rejected(self) -> None:
        for field, value in (
            ("transaction_id", "different-v098"),
            ("authorization_nonce", "different-nonce-v098"),
        ):
            nonce_receipt = self._resign_nonce_receipt(
                replace(self.nonce_receipt, **{field: value})
            )
            receipt = self._certify(
                nonce_consumption_receipt=nonce_receipt
            )
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.nonce_consumption_receipt_binding_exact)

    def test_nonce_not_consumed_or_revoked_is_rejected(self) -> None:
        for changes in (
            {"consumed": False},
            {"revoked": True},
        ):
            nonce_receipt = self._resign_nonce_receipt(
                replace(self.nonce_receipt, **changes)
            )
            receipt = self._certify(
                nonce_consumption_receipt=nonce_receipt
            )
            self.assertEqual(receipt.status, RECEIPT_REJECTED)

    def test_nonce_registry_digest_or_sequence_mismatch_is_rejected(self) -> None:
        for field, value in (
            ("final_registry_digest", "b" * 64),
            (
                "final_sequence_number",
                self.nonce_receipt.final_sequence_number + 1,
            ),
        ):
            nonce_receipt = self._resign_nonce_receipt(
                replace(self.nonce_receipt, **{field: value})
            )
            receipt = self._certify(
                nonce_consumption_receipt=nonce_receipt
            )
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.nonce_consumption_receipt_binding_exact)

    def test_stale_nonce_consumption_receipt_is_rejected(self) -> None:
        nonce_receipt = self._resign_nonce_receipt(
            replace(self.nonce_receipt, consumed_at_epoch_seconds=10_000)
        )
        receipt = self._certify(nonce_consumption_receipt=nonce_receipt)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.nonce_consumption_receipt_fresh)

    def test_unauthorized_or_mismatched_observer_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(self.post_observation, observer_id="other-observer-v098")
        )
        receipt = self._certify(post_reference_observation=observation)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.observer_authorized)

    def test_future_or_pre_execution_evidence_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(self.post_observation, observed_at_epoch_seconds=10_053)
        )
        receipt = self._certify(post_reference_observation=observation)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.no_future_evidence)
        future = self._certify(evaluated_at_epoch_seconds=10_053)
        self.assertEqual(future.status, RECEIPT_REJECTED)
        self.assertFalse(future.no_future_evidence)

    def test_valid_aborted_atomic_update_cannot_produce_committed_receipt(self) -> None:
        source_state = self.v097._state(current_oid="2" * 40)
        atomic_result, final_state, final_registry = self.v097._execute(
            source_reference_state=source_state
        )
        atomic_inputs = self.v097._values(
            source_reference_state=source_state
        )
        atomic_inputs.pop("transaction_id")
        report = self._execution_report(atomic_result=atomic_result)
        observation = self._post_observation(
            atomic_result=atomic_result,
            final_state=final_state,
        )
        nonce_receipt = self._nonce_receipt(
            atomic_result=atomic_result,
            source_registry=self.v097.source_registry,
            final_registry=final_registry,
        )
        receipt = self._certify(
            atomic_update_result=atomic_result,
            final_reference_state=final_state,
            final_nonce_registry=final_registry,
            atomic_update_inputs=atomic_inputs,
            execution_report=report,
            post_reference_observation=observation,
            nonce_consumption_receipt=nonce_receipt,
        )
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.atomic_update_committed)

    def test_receipt_itself_performs_no_mutation(self) -> None:
        receipt = self._certify()
        for field in (
            "receipt_performed_reference_mutation",
            "receipt_performed_nonce_consumption",
            "receipt_performed_push",
            "force_update_confirmed",
            "reference_delete_confirmed",
            "head_update_confirmed",
            "tag_update_confirmed",
            "remote_reference_update_confirmed",
            "push_confirmed",
            "index_write_confirmed",
            "working_tree_write_confirmed",
            "object_database_write_confirmed",
            "signing_confirmed",
        ):
            self.assertFalse(getattr(receipt, field))

    def test_receipt_effect_tamper_is_detected_after_outer_digest_recompute(self) -> None:
        receipt = self._certify()
        tampered = self._resign_receipt(
            replace(receipt, receipt_performed_push=True)
        )
        issues = self._issues(tampered)
        self.assertIn("reference_update_receipt_recomputation_mismatch", issues)
        self.assertIn("reference_update_receipt_forbidden_effect", issues)

    def test_outer_atomic_result_digest_recompute_cannot_hide_tamper(self) -> None:
        atomic_result = replace(
            self.atomic_result,
            branch_state_updated=False,
            result_digest="",
        )
        atomic_result = replace(
            atomic_result,
            result_digest=repository_atomic_reference_update_result_digest(
                atomic_result
            ),
        )
        with self.assertRaisesRegex(ValueError, "atomic_reference_update_invalid"):
            self._certify(atomic_update_result=atomic_result)


if __name__ == "__main__":
    unittest.main()
