from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_reference_stability_strict_v099 import (
    certify_repository_reference_stability_and_reachability,
    repository_reference_stability_reachability_certificate_issues,
)
from runtime.kuuos_repository_reference_stability_types_v0_99 import (
    CERTIFICATE_COMMITTED,
    CERTIFICATE_REJECTED,
    repository_commit_reachability_certificate_digest,
    repository_delayed_reference_observation_digest,
    repository_reference_stability_reachability_certificate_digest,
)
from runtime.kuuos_repository_reference_stability_v0_99 import (
    build_repository_commit_reachability_certificate,
    build_repository_delayed_reference_observation,
    build_repository_reference_stability_policy,
)
from runtime.kuuos_repository_reference_update_receipt_types_v0_98 import (
    repository_reference_update_receipt_digest,
)
from tests.test_kuuos_repository_reference_update_receipt_v0_98 import (
    RepositoryReferenceUpdateReceiptV098Tests,
)


class RepositoryReferenceStabilityV099Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryReferenceUpdateReceiptV098Tests(
            methodName="test_valid_receipt_is_deterministic_and_committed"
        )
        fixture.setUp()
        self.v098 = fixture
        self.receipt = fixture._certify()
        self.receipt_inputs = fixture._values()
        self.receipt_inputs.pop("receipt_id")
        self.observer_id = "kuuos-reference-stability-observer-v099"
        self.tip_oid = "f" * 40
        self.middle_oid = "e" * 40
        self.observed_at = 10_100
        self.evaluated_at = 10_102
        self.policy = self._policy()
        self.delayed_observation = self._observation()
        self.reachability = self._reachability()

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-reference-stability-policy-v099",
            "authorized_observer_ids": (self.observer_id,),
            "min_stability_interval_seconds": 30,
            "max_stability_interval_seconds": 300,
            "max_delayed_observation_age_seconds": 30,
            "max_reachability_certificate_age_seconds": 30,
            "max_reachability_depth": 4,
            "max_reachability_nodes": 5,
            "allow_tip_advance": True,
        }
        values.update(overrides)
        return build_repository_reference_stability_policy(**values)

    def _observation(self, receipt=None, **overrides):
        current_receipt = receipt or self.receipt
        values = {
            "observation_id": "repository-delayed-reference-observation-v099-001",
            "observer_id": self.observer_id,
            "receipt": current_receipt,
            "observed_tip_oid": self.tip_oid,
            "sequence_number": self.v098.post_observation.sequence_number + 2,
            "observed_at_epoch_seconds": self.observed_at,
        }
        values.update(overrides)
        return build_repository_delayed_reference_observation(**values)

    def _reachability(
        self,
        receipt=None,
        delayed_observation=None,
        **overrides,
    ):
        current_receipt = receipt or self.receipt
        current_observation = delayed_observation or self.delayed_observation
        values = {
            "certificate_id": "repository-commit-reachability-v099-001",
            "observer_id": self.observer_id,
            "receipt": current_receipt,
            "delayed_observation": current_observation,
            "path_oids": (
                current_observation.observed_tip_oid,
                self.middle_oid,
                current_receipt.proposed_new_oid,
            ),
            "observed_at_epoch_seconds": current_observation.observed_at_epoch_seconds,
        }
        values.update(overrides)
        return build_repository_commit_reachability_certificate(**values)

    def _values(self, **overrides):
        values = {
            "certificate_id": "repository-reference-stability-v099-001",
            "receipt": self.receipt,
            "receipt_inputs": self.receipt_inputs,
            "policy": self.policy,
            "delayed_observation": self.delayed_observation,
            "reachability": self.reachability,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return values

    def _certify(self, **overrides):
        return certify_repository_reference_stability_and_reachability(
            **self._values(**overrides)
        )

    def _issues(self, certificate, **overrides):
        values = self._values(**overrides)
        values.pop("certificate_id")
        return repository_reference_stability_reachability_certificate_issues(
            certificate,
            **values,
        )

    @staticmethod
    def _resign_observation(observation):
        observation = replace(observation, observation_digest="")
        return replace(
            observation,
            observation_digest=repository_delayed_reference_observation_digest(
                observation
            ),
        )

    @staticmethod
    def _resign_reachability(reachability):
        reachability = replace(reachability, certificate_digest="")
        return replace(
            reachability,
            certificate_digest=repository_commit_reachability_certificate_digest(
                reachability
            ),
        )

    @staticmethod
    def _resign_certificate(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=(
                repository_reference_stability_reachability_certificate_digest(
                    certificate
                )
            ),
        )

    @staticmethod
    def _resign_receipt(receipt):
        receipt = replace(receipt, receipt_digest="")
        return replace(
            receipt,
            receipt_digest=repository_reference_update_receipt_digest(receipt),
        )

    def test_valid_advanced_tip_certificate_is_deterministic(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, CERTIFICATE_COMMITTED)
        self.assertTrue(first.certificate_committed)
        self.assertTrue(first.delayed_tip_advanced)
        self.assertFalse(first.candidate_is_delayed_tip)
        self.assertTrue(first.candidate_reachable_from_delayed_tip)
        self.assertTrue(first.candidate_reachability_preserved)
        self.assertEqual(self._issues(first), ())

    def test_exact_candidate_tip_is_stable_with_zero_depth_path(self) -> None:
        observation = self._observation(
            observed_tip_oid=self.receipt.proposed_new_oid
        )
        reachability = self._reachability(
            delayed_observation=observation,
            path_oids=(self.receipt.proposed_new_oid,),
        )
        certificate = self._certify(
            delayed_observation=observation,
            reachability=reachability,
        )
        self.assertEqual(certificate.status, CERTIFICATE_COMMITTED)
        self.assertTrue(certificate.candidate_is_delayed_tip)
        self.assertFalse(certificate.delayed_tip_advanced)

    def test_certificate_binds_repository_reference_candidate_and_transaction(self) -> None:
        certificate = self._certify()
        self.assertEqual(certificate.repository_id, self.receipt.repository_id)
        self.assertEqual(
            certificate.git_dir_fingerprint,
            self.receipt.git_dir_fingerprint,
        )
        self.assertEqual(certificate.target_reference, self.receipt.target_reference)
        self.assertEqual(
            certificate.candidate_commit_oid,
            self.receipt.proposed_new_oid,
        )
        self.assertEqual(certificate.transaction_id, self.receipt.transaction_id)
        self.assertTrue(certificate.reference_update_receipt_binding_exact)
        self.assertTrue(certificate.delayed_observation_binding_exact)
        self.assertTrue(certificate.reachability_certificate_binding_exact)

    def test_tip_advance_policy_rejects_advanced_tip_but_allows_exact_tip(self) -> None:
        policy = self._policy(allow_tip_advance=False)
        rejected = self._certify(policy=policy)
        self.assertEqual(rejected.status, CERTIFICATE_REJECTED)
        self.assertFalse(rejected.tip_advance_allowed)
        observation = self._observation(
            observed_tip_oid=self.receipt.proposed_new_oid
        )
        reachability = self._reachability(
            delayed_observation=observation,
            path_oids=(self.receipt.proposed_new_oid,),
        )
        committed = self._certify(
            policy=policy,
            delayed_observation=observation,
            reachability=reachability,
        )
        self.assertEqual(committed.status, CERTIFICATE_COMMITTED)

    def test_rejected_upstream_receipt_cannot_commit_stability_certificate(self) -> None:
        report = self.v098._resign_report(
            replace(
                self.v098.execution_report,
                reference_update_performed=False,
            )
        )
        receipt = self.v098._certify(execution_report=report)
        receipt_inputs = self.v098._values(execution_report=report)
        receipt_inputs.pop("receipt_id")
        observation = self._observation(receipt=receipt)
        reachability = self._reachability(
            receipt=receipt,
            delayed_observation=observation,
        )
        certificate = self._certify(
            receipt=receipt,
            receipt_inputs=receipt_inputs,
            delayed_observation=observation,
            reachability=reachability,
        )
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reference_update_receipt_committed)

    def test_receipt_tamper_is_rejected_after_outer_digest_recompute(self) -> None:
        receipt = self._resign_receipt(
            replace(self.receipt, reference_update_confirmed=False)
        )
        with self.assertRaisesRegex(ValueError, "reference_update_receipt_invalid"):
            self._certify(receipt=receipt)

    def test_delayed_observation_binding_mismatches_are_rejected(self) -> None:
        cases = (
            ("transaction_id", "different-transaction-v099"),
            ("repository_id", "different-repository-v099"),
            ("target_reference", "refs/heads/other"),
            ("candidate_commit_oid", "1" * 40),
        )
        for field, value in cases:
            observation = self._resign_observation(
                replace(self.delayed_observation, **{field: value})
            )
            certificate = self._certify(delayed_observation=observation)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.delayed_observation_binding_exact)

    def test_stale_delayed_observation_is_rejected(self) -> None:
        certificate = self._certify(evaluated_at_epoch_seconds=10_140)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.delayed_observation_fresh)

    def test_stability_interval_too_short_or_too_long_is_rejected(self) -> None:
        for observed_at, evaluated_at in ((10_070, 10_071), (10_400, 10_401)):
            observation = self._observation(
                observed_at_epoch_seconds=observed_at
            )
            reachability = self._reachability(
                delayed_observation=observation,
                observed_at_epoch_seconds=observed_at,
            )
            certificate = self._certify(
                delayed_observation=observation,
                reachability=reachability,
                evaluated_at_epoch_seconds=evaluated_at,
            )
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.stability_interval_within_policy)

    def test_indirect_symbolic_or_wrong_source_observation_is_rejected(self) -> None:
        cases = (
            {"direct": False},
            {"symbolic": True},
            {"reference_store_read": False},
            {"object_database_read": False},
            {"working_tree_read": True},
            {"reflog_read": True},
            {"remote_read": True},
        )
        for changes in cases:
            observation = self._resign_observation(
                replace(self.delayed_observation, **changes)
            )
            certificate = self._certify(delayed_observation=observation)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_deleted_reference_or_force_update_evidence_is_rejected(self) -> None:
        for field in ("reference_deleted", "force_update_observed"):
            observation = self._resign_observation(
                replace(self.delayed_observation, **{field: True})
            )
            certificate = self._certify(delayed_observation=observation)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_delayed_sequence_regression_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(
                self.delayed_observation,
                sequence_number=self.v098.post_observation.sequence_number - 1,
            )
        )
        certificate = self._certify(delayed_observation=observation)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.delayed_sequence_monotone)

    def test_unauthorized_or_mismatched_observer_is_rejected(self) -> None:
        observation = self._resign_observation(
            replace(self.delayed_observation, observer_id="other-observer-v099")
        )
        certificate = self._certify(delayed_observation=observation)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.observer_authorized)
        reachability = self._resign_reachability(
            replace(self.reachability, observer_id="other-observer-v099")
        )
        certificate = self._certify(reachability=reachability)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.observer_authorized)

    def test_reachability_binding_mismatches_are_rejected(self) -> None:
        cases = (
            ("transaction_id", "different-transaction-v099"),
            ("repository_id", "different-repository-v099"),
            ("target_reference", "refs/heads/other"),
            ("tip_oid", "2" * 40),
            ("candidate_commit_oid", "3" * 40),
        )
        for field, value in cases:
            reachability = self._resign_reachability(
                replace(self.reachability, **{field: value})
            )
            certificate = self._certify(reachability=reachability)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.reachability_certificate_binding_exact)

    def test_reachability_time_mismatch_or_staleness_is_rejected(self) -> None:
        reachability = self._resign_reachability(
            replace(self.reachability, observed_at_epoch_seconds=10_099)
        )
        certificate = self._certify(reachability=reachability)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reachability_evidence_time_exact)
        certificate = self._certify(evaluated_at_epoch_seconds=10_140)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reachability_certificate_fresh)

    def test_incomplete_path_is_rejected(self) -> None:
        for path in (
            (self.middle_oid, self.receipt.proposed_new_oid),
            (self.tip_oid, self.middle_oid),
        ):
            reachability = self._reachability(path_oids=path)
            certificate = self._certify(reachability=reachability)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.reachability_path_complete)

    def test_parent_edge_tamper_is_rejected(self) -> None:
        reachability = self._resign_reachability(
            replace(
                self.reachability,
                parent_edges=((self.tip_oid, self.receipt.proposed_new_oid),),
            )
        )
        certificate = self._certify(reachability=reachability)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reachability_parent_edges_exact)

    def test_queried_oid_set_or_object_inventory_mismatch_is_rejected(self) -> None:
        cases = (
            {"queried_oid_set_complete": False},
            {"queried_oids": tuple(sorted((self.tip_oid, self.middle_oid)))},
            {
                "object_database_commit_oids": tuple(
                    sorted((self.tip_oid, self.middle_oid))
                )
            },
            {"all_objects_are_commits": False},
        )
        for changes in cases:
            reachability = self._resign_reachability(
                replace(self.reachability, **changes)
            )
            certificate = self._certify(reachability=reachability)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_reachability_evidence_cannot_use_worktree_reflog_or_remote(self) -> None:
        for field in ("working_tree_read", "reflog_read", "remote_read"):
            reachability = self._resign_reachability(
                replace(self.reachability, **{field: True})
            )
            certificate = self._certify(reachability=reachability)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.candidate_reachable_from_delayed_tip)

    def test_reachability_depth_bound_is_enforced(self) -> None:
        policy = self._policy(max_reachability_depth=1)
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reachability_depth_within_policy)

    def test_future_evidence_is_rejected(self) -> None:
        certificate = self._certify(evaluated_at_epoch_seconds=10_099)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.no_future_evidence)

    def test_cyclic_reachability_path_is_structurally_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "commit_reachability_certificate_invalid"):
            self._reachability(
                path_oids=(
                    self.tip_oid,
                    self.middle_oid,
                    self.tip_oid,
                    self.receipt.proposed_new_oid,
                )
            )

    def test_certificate_performs_no_repository_effect(self) -> None:
        certificate = self._certify()
        for field in (
            "force_update_authorized",
            "reference_delete_authorized",
            "push_authorized",
            "reference_mutation_performed",
            "object_database_write_performed",
            "working_tree_write_performed",
            "index_write_performed",
            "reflog_write_performed",
            "remote_reference_updated",
            "push_performed",
            "signing_performed",
        ):
            self.assertFalse(getattr(certificate, field))

    def test_certificate_effect_tamper_is_detected_after_digest_recompute(self) -> None:
        certificate = self._certify()
        tampered = self._resign_certificate(
            replace(certificate, push_performed=True)
        )
        issues = self._issues(tampered)
        self.assertIn(
            "reference_stability_certificate_recomputation_mismatch",
            issues,
        )
        self.assertIn("reference_stability_certificate_forbidden_effect", issues)


if __name__ == "__main__":
    unittest.main()
