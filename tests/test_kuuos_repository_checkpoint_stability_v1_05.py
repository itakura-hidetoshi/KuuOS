from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_checkpoint_stability_strict_v1_05 import (
    certify_repository_checkpoint_stability,
    repository_checkpoint_stability_certificate_issues,
)
from runtime.kuuos_repository_checkpoint_stability_types_v1_05 import (
    FAILURE_CHECKPOINT_LOST,
    FAILURE_CHECKPOINT_SUBSTITUTED,
    FAILURE_EVIDENCE_INVALID,
    FAILURE_NAME_CONFLICT,
    FAILURE_NONE,
    FAILURE_UNREACHABLE,
    FAILURE_UNSTABLE_WINDOW,
    STABILITY_CONFIRMED,
    STABILITY_REJECTED,
    ZERO_OID,
    repository_checkpoint_namespace_observation_digest,
    repository_checkpoint_reachability_observation_digest,
    repository_checkpoint_stability_certificate_digest,
    repository_delayed_checkpoint_observation_digest,
)
from runtime.kuuos_repository_checkpoint_stability_v1_05 import (
    build_repository_checkpoint_namespace_observation,
    build_repository_checkpoint_reachability_observation,
    build_repository_checkpoint_stability_policy,
    build_repository_delayed_checkpoint_observation,
)
from tests.test_kuuos_repository_checkpoint_creation_receipt_v1_03 import (
    RepositoryCheckpointCreationReceiptV103Tests,
)


class RepositoryCheckpointStabilityV105Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryCheckpointCreationReceiptV103Tests(
            methodName="test_committed_receipt_is_deterministic_and_confirmed"
        )
        fixture.setUp()
        self.fixture = fixture
        self.creation_receipt = fixture._certify()
        self.v103_context = fixture._values()
        self.creation_result = fixture.result
        self.observer_id = "kuuos-checkpoint-stability-observer-v105"
        self.policy = build_repository_checkpoint_stability_policy(
            "checkpoint-stability-policy-v105",
            authorized_observer_ids=(self.observer_id,),
            min_stability_interval_seconds=60,
            max_stability_interval_seconds=600,
            max_observation_age_seconds=20,
            max_reachability_age_seconds=20,
        )
        self.evaluated_at = 10_282
        self._build_observations()

    def _build_observations(self) -> None:
        self.delayed = build_repository_delayed_checkpoint_observation(
            "delayed-checkpoint-observation-v105",
            self.observer_id,
            self.creation_receipt,
            self.creation_result,
            observed_oid=self.creation_result.proposed_new_oid,
            reference_present=True,
            sequence_number=5,
            observed_at_epoch_seconds=10_279,
        )
        self.reachability = build_repository_checkpoint_reachability_observation(
            "checkpoint-reachability-observation-v105",
            self.observer_id,
            self.creation_receipt,
            self.creation_result,
            object_present=True,
            object_type="commit",
            sequence_number=6,
            observed_at_epoch_seconds=10_280,
        )
        self.namespace = build_repository_checkpoint_namespace_observation(
            "checkpoint-namespace-observation-v105",
            self.observer_id,
            self.creation_receipt,
            self.creation_result,
            observed_checkpoint_references=(
                self.creation_result.checkpoint_reference,
            ),
            sequence_number=7,
            observed_at_epoch_seconds=10_281,
        )

    @staticmethod
    def _resign_delayed(value, **changes):
        value = replace(value, **changes, observation_digest="")
        return replace(
            value,
            observation_digest=repository_delayed_checkpoint_observation_digest(
                value
            ),
        )

    @staticmethod
    def _resign_reachability(value, **changes):
        value = replace(value, **changes, observation_digest="")
        return replace(
            value,
            observation_digest=(
                repository_checkpoint_reachability_observation_digest(value)
            ),
        )

    @staticmethod
    def _resign_namespace(value, **changes):
        value = replace(value, **changes, observation_digest="")
        return replace(
            value,
            observation_digest=repository_checkpoint_namespace_observation_digest(
                value
            ),
        )

    def _values(self, **overrides):
        values = {
            "certificate_id": "checkpoint-stability-certificate-v105-001",
            "creation_receipt": self.creation_receipt,
            "v103_context": self.v103_context,
            "policy": self.policy,
            "delayed_observation": self.delayed,
            "reachability_observation": self.reachability,
            "namespace_observation": self.namespace,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return values

    def _certify(self, **overrides):
        return certify_repository_checkpoint_stability(
            **self._values(**overrides)
        )

    def test_stability_is_deterministic_and_confirmed(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, STABILITY_CONFIRMED)
        self.assertEqual(first.failure_kind, FAILURE_NONE)
        self.assertTrue(first.checks["checkpoint_stability_confirmed"])

    def test_checkpoint_loss_has_explicit_failure_disposition(self) -> None:
        delayed = self._resign_delayed(
            self.delayed,
            reference_present=False,
            observed_oid=ZERO_OID,
        )
        certificate = self._certify(delayed_observation=delayed)
        self.assertEqual(certificate.status, STABILITY_REJECTED)
        self.assertEqual(certificate.failure_kind, FAILURE_CHECKPOINT_LOST)

    def test_checkpoint_oid_substitution_is_rejected(self) -> None:
        delayed = self._resign_delayed(self.delayed, observed_oid="b" * 40)
        certificate = self._certify(delayed_observation=delayed)
        self.assertEqual(certificate.failure_kind, FAILURE_CHECKPOINT_SUBSTITUTED)
        self.assertFalse(certificate.checks["checkpoint_not_substituted"])

    def test_overwrite_or_force_observation_is_rejected(self) -> None:
        for changes in (
            {"overwrite_observed": True},
            {"force_update_observed": True},
        ):
            delayed = self._resign_delayed(self.delayed, **changes)
            certificate = self._certify(delayed_observation=delayed)
            self.assertEqual(
                certificate.failure_kind,
                FAILURE_CHECKPOINT_SUBSTITUTED,
            )

    def test_reference_source_must_be_direct_and_local(self) -> None:
        for changes in (
            {"direct": False},
            {"symbolic": True},
            {"reference_store_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        ):
            delayed = self._resign_delayed(self.delayed, **changes)
            certificate = self._certify(delayed_observation=delayed)
            self.assertEqual(
                certificate.failure_kind,
                FAILURE_CHECKPOINT_SUBSTITUTED,
            )

    def test_unreachable_or_non_commit_object_is_rejected(self) -> None:
        for changes in (
            {"object_present": False},
            {"object_type": "blob"},
            {"object_database_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        ):
            observation = self._resign_reachability(
                self.reachability,
                **changes,
            )
            certificate = self._certify(
                reachability_observation=observation
            )
            self.assertEqual(certificate.failure_kind, FAILURE_UNREACHABLE)

    def test_checkpoint_name_must_be_unique(self) -> None:
        duplicate = build_repository_checkpoint_namespace_observation(
            "checkpoint-namespace-duplicate-v105",
            self.observer_id,
            self.creation_receipt,
            self.creation_result,
            observed_checkpoint_references=(
                self.creation_result.checkpoint_reference,
                self.creation_result.checkpoint_reference,
            ),
            sequence_number=7,
            observed_at_epoch_seconds=10_281,
        )
        certificate = self._certify(namespace_observation=duplicate)
        self.assertEqual(certificate.failure_kind, FAILURE_NAME_CONFLICT)

    def test_explicit_name_conflict_is_rejected(self) -> None:
        namespace = build_repository_checkpoint_namespace_observation(
            "checkpoint-namespace-conflict-v105",
            self.observer_id,
            self.creation_receipt,
            self.creation_result,
            observed_checkpoint_references=(
                self.creation_result.checkpoint_reference,
            ),
            conflicting_reference_names=(
                self.creation_result.checkpoint_reference + "-alias",
            ),
            sequence_number=7,
            observed_at_epoch_seconds=10_281,
        )
        certificate = self._certify(namespace_observation=namespace)
        self.assertEqual(certificate.failure_kind, FAILURE_NAME_CONFLICT)

    def test_stability_window_is_bounded(self) -> None:
        for observed_at in (10_200, 10_900):
            delayed = self._resign_delayed(
                self.delayed,
                observed_at_epoch_seconds=observed_at,
            )
            reachability = self._resign_reachability(
                self.reachability,
                observed_at_epoch_seconds=max(observed_at, 10_280),
            )
            namespace = self._resign_namespace(
                self.namespace,
                observed_at_epoch_seconds=max(observed_at, 10_281),
            )
            evaluated = max(self.evaluated_at, observed_at + 3)
            certificate = self._certify(
                delayed_observation=delayed,
                reachability_observation=reachability,
                namespace_observation=namespace,
                evaluated_at_epoch_seconds=evaluated,
            )
            self.assertEqual(certificate.failure_kind, FAILURE_UNSTABLE_WINDOW)

    def test_observer_and_transaction_binding_are_exact(self) -> None:
        delayed = self._resign_delayed(
            self.delayed,
            observer_id="unauthorized-observer-v105",
        )
        certificate = self._certify(delayed_observation=delayed)
        self.assertEqual(certificate.failure_kind, FAILURE_EVIDENCE_INVALID)
        self.assertFalse(certificate.checks["observer_authorized"])

        delayed = self._resign_delayed(
            self.delayed,
            transaction_id="different-transaction-v105",
        )
        certificate = self._certify(delayed_observation=delayed)
        self.assertEqual(certificate.failure_kind, FAILURE_EVIDENCE_INVALID)
        self.assertFalse(certificate.checks["evidence_binding_exact"])

    def test_observation_sequence_and_time_are_ordered(self) -> None:
        reachability = self._resign_reachability(
            self.reachability,
            sequence_number=5,
        )
        certificate = self._certify(reachability_observation=reachability)
        self.assertEqual(certificate.failure_kind, FAILURE_EVIDENCE_INVALID)

        namespace = self._resign_namespace(
            self.namespace,
            observed_at_epoch_seconds=self.evaluated_at + 1,
        )
        certificate = self._certify(namespace_observation=namespace)
        self.assertEqual(certificate.failure_kind, FAILURE_EVIDENCE_INVALID)

    def test_stability_requires_committed_v103_receipt(self) -> None:
        aborted_fixture = RepositoryCheckpointCreationReceiptV103Tests(
            methodName="test_aborted_v102_result_is_confirmed_without_mutation"
        )
        aborted_fixture.setUp()
        source_state = aborted_fixture.fixture._state(current_oid="b" * 40)
        aborted_fixture.inputs = aborted_fixture.fixture._values(
            source_checkpoint_state=source_state
        )
        (
            aborted_fixture.result,
            aborted_fixture.final_state,
            aborted_fixture.final_registry,
        ) = aborted_fixture.fixture._execute(
            source_checkpoint_state=source_state
        )
        aborted_fixture._build_evidence()
        aborted_receipt = aborted_fixture._certify()
        context = aborted_fixture._values()
        certificate = self._certify(
            creation_receipt=aborted_receipt,
            v103_context=context,
        )
        self.assertEqual(certificate.failure_kind, FAILURE_EVIDENCE_INVALID)
        self.assertFalse(certificate.checks["creation_receipt_committed"])

    def test_immutability_grants_no_mutation_or_recovery_authority(self) -> None:
        certificate = self._certify()
        for key in (
            "checkpoint_overwrite_authorized",
            "checkpoint_delete_authorized",
            "force_update_authorized",
            "restore_authorized",
            "recovery_authorized",
            "branch_update_authorized",
            "tag_update_authorized",
            "remote_reference_update_authorized",
            "push_authorized",
            "certificate_performed_reference_mutation",
            "certificate_performed_object_write",
            "certificate_invoked_live_git_command",
            "certificate_mutated_live_repository",
        ):
            self.assertFalse(certificate.checks[key])

    def test_certificate_tamper_is_detected(self) -> None:
        certificate = self._certify()
        checks = dict(certificate.checks)
        checks["restore_authorized"] = True
        tampered = replace(certificate, checks=checks, certificate_digest="")
        tampered = replace(
            tampered,
            certificate_digest=repository_checkpoint_stability_certificate_digest(
                tampered
            ),
        )
        values = self._values()
        values.pop("certificate_id")
        issues = repository_checkpoint_stability_certificate_issues(
            tampered,
            **values,
        )
        self.assertIn("checkpoint_stability_recomputation_mismatch", issues)
        self.assertIn("checkpoint_stability_forbidden_claim", issues)


if __name__ == "__main__":
    unittest.main()
