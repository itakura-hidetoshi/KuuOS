from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_creation_receipt_strict_v1_03 import (
    certify_repository_checkpoint_creation_receipt,
    repository_checkpoint_creation_receipt_issues,
)
from runtime.kuuos_repository_checkpoint_creation_receipt_v1_03 import (
    build_repository_checkpoint_creation_execution_report,
    build_repository_checkpoint_creation_receipt_policy,
    build_repository_checkpoint_identity_snapshot,
    build_repository_checkpoint_nonce_registry_snapshot,
    build_repository_checkpoint_reference_snapshot,
)
from runtime.v103_evidence_a import (
    repository_checkpoint_creation_execution_report_digest,
)
from runtime.v103_receipt_helpers import snapshot_digest
from runtime.v103_receipt_policy import RECEIPT_CONFIRMED, RECEIPT_REJECTED
from runtime.v103_result import checkpoint_receipt_result_digest
from tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02 import (
    RepositoryAtomicCheckpointCreationV102Tests,
)


class RepositoryCheckpointCreationReceiptV103Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryAtomicCheckpointCreationV102Tests(
            methodName="test_valid_creation_is_deterministic_and_committed"
        )
        fixture.setUp()
        self.fixture = fixture
        self.observer_id = "kuuos-checkpoint-observer-v103"
        self.evaluated_at = 10_182
        self.policy = build_repository_checkpoint_creation_receipt_policy(
            "checkpoint-receipt-policy-v103",
            authorized_observer_ids=(self.observer_id,),
            max_report_age_seconds=20,
            max_observation_age_seconds=20,
            max_external_duration_seconds=10,
        )
        self.result, self.final_state, self.final_registry = fixture._execute()
        self.inputs = fixture._values()
        self._build_evidence()

    def _build_evidence(self) -> None:
        self.report = build_repository_checkpoint_creation_execution_report(
            self.result,
            report_id="checkpoint-report-v103",
            executor_sequence_number=1,
            execution_started_at_epoch_seconds=10_177,
            execution_completed_at_epoch_seconds=10_178,
        )
        self.reference_snapshot = build_repository_checkpoint_reference_snapshot(
            "checkpoint-reference-snapshot-v103",
            self.observer_id,
            self.result.transaction_id,
            self.final_state,
            sequence_number=2,
            recorded_at_epoch_seconds=10_179,
        )
        self.nonce_snapshot = build_repository_checkpoint_nonce_registry_snapshot(
            "checkpoint-nonce-snapshot-v103",
            self.observer_id,
            self.result.transaction_id,
            self.final_registry,
            sequence_number=3,
            recorded_at_epoch_seconds=10_180,
        )
        self.identity_snapshot = build_repository_checkpoint_identity_snapshot(
            "checkpoint-identity-snapshot-v103",
            self.observer_id,
            self.result.transaction_id,
            pre_repository_id=self.result.repository_id,
            post_repository_id=self.result.repository_id,
            pre_git_dir_fingerprint=self.result.git_dir_fingerprint,
            post_git_dir_fingerprint=self.result.git_dir_fingerprint,
            sequence_number=4,
            recorded_at_epoch_seconds=10_181,
        )

    @staticmethod
    def _resign_report(report):
        report = replace(report, report_digest="")
        return replace(
            report,
            report_digest=repository_checkpoint_creation_execution_report_digest(report),
        )

    @staticmethod
    def _resign_snapshot(snapshot, **changes):
        value = dict(snapshot)
        value.update(changes)
        value["snapshot_digest"] = ""
        value["snapshot_digest"] = snapshot_digest(value)
        return value

    def _values(self, **overrides):
        values = {
            "receipt_id": "checkpoint-creation-receipt-v103-001",
            "result": self.result,
            "final_checkpoint_state": self.final_state,
            "final_nonce_registry": self.final_registry,
            "v102_inputs": self.inputs,
            "policy": self.policy,
            "execution_report": self.report,
            "reference_snapshot": self.reference_snapshot,
            "nonce_registry_snapshot": self.nonce_snapshot,
            "identity_snapshot": self.identity_snapshot,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return values

    def _certify(self, **overrides):
        return certify_repository_checkpoint_creation_receipt(
            **self._values(**overrides)
        )

    def test_committed_receipt_is_deterministic_and_confirmed(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, RECEIPT_CONFIRMED)
        self.assertTrue(first.checks["committed_receipt_confirmed"])
        self.assertTrue(first.checks["supplied_external_report_consistent"])

    def test_aborted_v102_result_is_confirmed_without_mutation(self) -> None:
        source_state = self.fixture._state(current_oid="b" * 40)
        inputs = self.fixture._values(source_checkpoint_state=source_state)
        result, final_state, final_registry = self.fixture._execute(
            source_checkpoint_state=source_state
        )
        self.result, self.final_state, self.final_registry, self.inputs = (
            result,
            final_state,
            final_registry,
            inputs,
        )
        self._build_evidence()
        receipt = self._certify()
        self.assertEqual(receipt.status, RECEIPT_CONFIRMED)
        self.assertTrue(receipt.checks["aborted_receipt_confirmed"])
        self.assertIs(final_state, source_state)
        self.assertIs(final_registry, self.fixture.source_registry)

    def test_report_binds_all_v102_digests(self) -> None:
        report = self._resign_report(replace(self.report, request_digest="b" * 64))
        receipt = self._certify(execution_report=report)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["execution_report_binding_exact"])

    def test_wrong_post_oid_is_rejected(self) -> None:
        snapshot = self._resign_snapshot(self.reference_snapshot, observed_oid="b" * 40)
        receipt = self._certify(reference_snapshot=snapshot)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["reference_snapshot_exact"])

    def test_symbolic_or_non_reference_store_evidence_is_rejected(self) -> None:
        for changes in (
            {"symbolic": True},
            {"direct": False},
            {"reference_store_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        ):
            snapshot = self._resign_snapshot(self.reference_snapshot, **changes)
            self.assertEqual(
                self._certify(reference_snapshot=snapshot).status,
                RECEIPT_REJECTED,
            )

    def test_nonce_must_be_consumed_exactly_once(self) -> None:
        nonce = self.result.authorization_nonce
        for consumed in ([], [nonce, nonce]):
            snapshot = self._resign_snapshot(
                self.nonce_snapshot,
                consumed_nonces=consumed,
            )
            receipt = self._certify(nonce_registry_snapshot=snapshot)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.checks["nonce_snapshot_exact"])

    def test_checkpoint_and_nonce_sequences_are_exact(self) -> None:
        reference = self._resign_snapshot(
            self.reference_snapshot,
            checkpoint_state_sequence_number=self.final_state.sequence_number + 1,
        )
        nonce = self._resign_snapshot(
            self.nonce_snapshot,
            nonce_registry_sequence_number=self.final_registry.sequence_number + 1,
        )
        self.assertEqual(self._certify(reference_snapshot=reference).status, RECEIPT_REJECTED)
        self.assertEqual(self._certify(nonce_registry_snapshot=nonce).status, RECEIPT_REJECTED)

    def test_repository_identity_and_git_dir_must_remain_stable(self) -> None:
        snapshot = self._resign_snapshot(
            self.identity_snapshot,
            post_git_dir_fingerprint="b" * 64,
        )
        receipt = self._certify(identity_snapshot=snapshot)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["repository_identity_and_git_dir_stable"])

    def test_observer_must_be_authorized_and_shared(self) -> None:
        snapshot = self._resign_snapshot(
            self.identity_snapshot,
            observer_id="unauthorized-observer-v103",
        )
        receipt = self._certify(identity_snapshot=snapshot)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["observer_authorized"])

    def test_observation_sequence_is_strictly_ordered(self) -> None:
        snapshot = self._resign_snapshot(self.nonce_snapshot, sequence_number=2)
        receipt = self._certify(nonce_registry_snapshot=snapshot)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["observation_sequence_ordered"])

    def test_future_or_stale_evidence_is_rejected(self) -> None:
        future = self._resign_snapshot(
            self.identity_snapshot,
            recorded_at_epoch_seconds=self.evaluated_at + 1,
        )
        stale = self._resign_snapshot(
            self.reference_snapshot,
            recorded_at_epoch_seconds=10_100,
        )
        self.assertEqual(self._certify(identity_snapshot=future).status, RECEIPT_REJECTED)
        self.assertEqual(self._certify(reference_snapshot=stale).status, RECEIPT_REJECTED)

    def test_forbidden_external_effect_is_rejected(self) -> None:
        report = self._resign_report(
            replace(self.report, reported_effects=("push",))
        )
        receipt = self._certify(execution_report=report)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["no_forbidden_execution_effect"])

    def test_committed_report_requires_cas_creation_and_nonce_consumption(self) -> None:
        for changes in (
            {"compare_and_swap_succeeded": False},
            {"checkpoint_created": False},
            {"nonce_consumed": False},
            {"aborted_without_mutation": True},
        ):
            report = self._resign_report(replace(self.report, **changes))
            receipt = self._certify(execution_report=report)
            self.assertEqual(receipt.status, RECEIPT_REJECTED)
            self.assertFalse(receipt.checks["committed_receipt_confirmed"])

    def test_v102_original_input_mismatch_is_rejected(self) -> None:
        inputs = dict(self.inputs)
        inputs["source_checkpoint_state"] = self.fixture._state(
            checkpoint_reference="refs/kuuos/checkpoints/different-v103"
        )
        receipt = self._certify(v102_inputs=inputs)
        self.assertEqual(receipt.status, RECEIPT_REJECTED)
        self.assertFalse(receipt.checks["v102_result_valid"])

    def test_receipt_never_claims_independent_truth_or_live_execution(self) -> None:
        receipt = self._certify()
        for key in (
            "external_report_independently_trusted",
            "live_execution_proven",
            "receipt_performed_checkpoint_mutation",
            "receipt_performed_nonce_consumption",
            "receipt_invoked_live_git_command",
            "receipt_mutated_live_repository",
        ):
            self.assertFalse(receipt.checks[key])

    def test_receipt_tamper_is_detected_after_digest_recompute(self) -> None:
        receipt = self._certify()
        checks = dict(receipt.checks)
        checks["live_execution_proven"] = True
        tampered = replace(receipt, checks=checks, receipt_digest="")
        tampered = replace(
            tampered,
            receipt_digest=checkpoint_receipt_result_digest(tampered),
        )
        values = self._values()
        values.pop("receipt_id")
        issues = repository_checkpoint_creation_receipt_issues(tampered, **values)
        self.assertIn("checkpoint_receipt_recomputation_mismatch", issues)
        self.assertIn("checkpoint_receipt_forbidden_claim", issues)


if __name__ == "__main__":
    unittest.main()
