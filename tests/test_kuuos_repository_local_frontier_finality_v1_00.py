from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_local_frontier_finality_strict_v100 import (
    certify_repository_local_frontier_finality,
    repository_local_frontier_finality_certificate_issues,
)
from runtime.kuuos_repository_local_frontier_finality_types_v1_00 import (
    CERTIFICATE_COMMITTED,
    CERTIFICATE_REJECTED,
    repository_local_frontier_finality_certificate_digest,
    repository_local_frontier_history_digest,
    repository_local_frontier_sample_digest,
)
from runtime.kuuos_repository_local_frontier_finality_v1_00 import (
    build_repository_local_frontier_finality_policy,
    build_repository_local_frontier_history,
    build_repository_local_frontier_sample,
)
from runtime.kuuos_repository_reference_stability_types_v0_99 import (
    repository_reference_stability_reachability_certificate_digest,
)
from tests.test_kuuos_repository_reference_stability_v0_99 import (
    RepositoryReferenceStabilityV099Tests,
)


class RepositoryLocalFrontierFinalityV100Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryReferenceStabilityV099Tests(
            methodName="test_valid_advanced_tip_certificate_is_deterministic"
        )
        fixture.setUp()
        self.v099 = fixture
        self.stability_certificate = fixture._certify()
        self.stability_inputs = fixture._values()
        self.stability_inputs.pop("certificate_id")
        self.observer_id = fixture.observer_id
        self.anchor_tip = fixture.delayed_observation.observed_tip_oid
        self.tip2 = "d" * 40
        self.tip3 = "c" * 40
        self.policy = self._policy()
        self.anchor_sample = self._anchor_sample()
        self.sample2 = self._sample2()
        self.sample3 = self._sample3()
        self.history = self._history()
        self.evaluated_at = 10_162

    def _policy(self, **overrides):
        values = {
            "policy_id": "repository-local-frontier-finality-policy-v100",
            "authorized_observer_ids": (self.observer_id,),
            "min_sample_count": 3,
            "max_sample_count": 5,
            "min_total_interval_seconds": 50,
            "max_total_interval_seconds": 180,
            "min_inter_sample_interval_seconds": 20,
            "max_inter_sample_interval_seconds": 60,
            "max_history_age_seconds": 30,
            "max_candidate_reachability_depth": 5,
            "max_transition_depth": 2,
            "max_total_queried_nodes": 15,
            "allow_equal_tip": True,
            "allow_tip_advance": True,
        }
        values.update(overrides)
        return build_repository_local_frontier_finality_policy(**values)

    def _anchor_sample(self, **overrides):
        observation = self.v099.delayed_observation
        reachability = self.v099.reachability
        values = {
            "sample_id": "repository-local-frontier-sample-v100-001",
            "observer_id": self.observer_id,
            "transaction_id": self.stability_certificate.transaction_id,
            "repository_id": self.stability_certificate.repository_id,
            "git_dir_fingerprint": self.stability_certificate.git_dir_fingerprint,
            "target_reference": self.stability_certificate.target_reference,
            "candidate_commit_oid": self.stability_certificate.candidate_commit_oid,
            "observed_tip_oid": observation.observed_tip_oid,
            "previous_tip_oid": observation.observed_tip_oid,
            "sequence_number": observation.sequence_number,
            "observed_at_epoch_seconds": observation.observed_at_epoch_seconds,
            "candidate_path_oids": reachability.path_oids,
            "transition_path_oids": (observation.observed_tip_oid,),
        }
        values.update(overrides)
        return build_repository_local_frontier_sample(**values)

    def _sample2(self, **overrides):
        values = {
            "sample_id": "repository-local-frontier-sample-v100-002",
            "observer_id": self.observer_id,
            "transaction_id": self.stability_certificate.transaction_id,
            "repository_id": self.stability_certificate.repository_id,
            "git_dir_fingerprint": self.stability_certificate.git_dir_fingerprint,
            "target_reference": self.stability_certificate.target_reference,
            "candidate_commit_oid": self.stability_certificate.candidate_commit_oid,
            "observed_tip_oid": self.tip2,
            "previous_tip_oid": self.anchor_tip,
            "sequence_number": self.v099.delayed_observation.sequence_number + 1,
            "observed_at_epoch_seconds": 10_130,
            "candidate_path_oids": (
                self.tip2,
                self.anchor_tip,
                self.v099.middle_oid,
                self.stability_certificate.candidate_commit_oid,
            ),
            "transition_path_oids": (self.tip2, self.anchor_tip),
        }
        values.update(overrides)
        return build_repository_local_frontier_sample(**values)

    def _sample3(self, **overrides):
        values = {
            "sample_id": "repository-local-frontier-sample-v100-003",
            "observer_id": self.observer_id,
            "transaction_id": self.stability_certificate.transaction_id,
            "repository_id": self.stability_certificate.repository_id,
            "git_dir_fingerprint": self.stability_certificate.git_dir_fingerprint,
            "target_reference": self.stability_certificate.target_reference,
            "candidate_commit_oid": self.stability_certificate.candidate_commit_oid,
            "observed_tip_oid": self.tip3,
            "previous_tip_oid": self.tip2,
            "sequence_number": self.v099.delayed_observation.sequence_number + 2,
            "observed_at_epoch_seconds": 10_160,
            "candidate_path_oids": (
                self.tip3,
                self.tip2,
                self.anchor_tip,
                self.v099.middle_oid,
                self.stability_certificate.candidate_commit_oid,
            ),
            "transition_path_oids": (self.tip3, self.tip2),
        }
        values.update(overrides)
        return build_repository_local_frontier_sample(**values)

    def _history(self, samples=None, stability_certificate=None):
        return build_repository_local_frontier_history(
            "repository-local-frontier-history-v100-001",
            stability_certificate or self.stability_certificate,
            samples=tuple(samples or (
                self.anchor_sample,
                self.sample2,
                self.sample3,
            )),
        )

    def _values(self, **overrides):
        values = {
            "certificate_id": "repository-local-frontier-finality-v100-001",
            "reference_stability_certificate": self.stability_certificate,
            "reference_stability_inputs": self.stability_inputs,
            "policy": self.policy,
            "history": self.history,
            "evaluated_at_epoch_seconds": self.evaluated_at,
        }
        values.update(overrides)
        return values

    def _certify(self, **overrides):
        return certify_repository_local_frontier_finality(
            **self._values(**overrides)
        )

    def _issues(self, certificate, **overrides):
        values = self._values(**overrides)
        values.pop("certificate_id")
        return repository_local_frontier_finality_certificate_issues(
            certificate,
            **values,
        )

    @staticmethod
    def _resign_sample(sample):
        sample = replace(sample, sample_digest="")
        return replace(
            sample,
            sample_digest=repository_local_frontier_sample_digest(sample),
        )

    @staticmethod
    def _resign_history(history):
        history = replace(history, history_digest="")
        return replace(
            history,
            history_digest=repository_local_frontier_history_digest(history),
        )

    @staticmethod
    def _resign_certificate(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=(
                repository_local_frontier_finality_certificate_digest(
                    certificate
                )
            ),
        )

    @staticmethod
    def _resign_stability(certificate):
        certificate = replace(certificate, certificate_digest="")
        return replace(
            certificate,
            certificate_digest=(
                repository_reference_stability_reachability_certificate_digest(
                    certificate
                )
            ),
        )

    def test_valid_finality_certificate_is_deterministic(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, CERTIFICATE_COMMITTED)
        self.assertTrue(first.certificate_committed)
        self.assertTrue(first.local_frontier_history_monotone)
        self.assertTrue(first.candidate_reachability_continuous)
        self.assertTrue(first.bounded_local_finality_verified)
        self.assertEqual(self._issues(first), ())

    def test_certificate_binds_exact_frontier_identity(self) -> None:
        certificate = self._certify()
        self.assertEqual(
            certificate.repository_id,
            self.stability_certificate.repository_id,
        )
        self.assertEqual(
            certificate.target_reference,
            self.stability_certificate.target_reference,
        )
        self.assertEqual(
            certificate.candidate_commit_oid,
            self.stability_certificate.candidate_commit_oid,
        )
        self.assertEqual(
            certificate.transaction_id,
            self.stability_certificate.transaction_id,
        )
        self.assertEqual(certificate.first_tip_oid, self.anchor_tip)
        self.assertEqual(certificate.final_tip_oid, self.tip3)

    def test_anchor_sample_is_exact_v099_evidence(self) -> None:
        certificate = self._certify()
        self.assertTrue(certificate.reference_stability_binding_exact)
        self.assertTrue(certificate.history_binding_exact)
        self.assertTrue(certificate.anchor_sample_exact)

    def test_repeated_equal_tip_is_allowed_when_policy_allows_it(self) -> None:
        equal2 = self._sample2(
            observed_tip_oid=self.anchor_tip,
            previous_tip_oid=self.anchor_tip,
            candidate_path_oids=self.v099.reachability.path_oids,
            transition_path_oids=(self.anchor_tip,),
        )
        equal3 = self._sample3(
            observed_tip_oid=self.anchor_tip,
            previous_tip_oid=self.anchor_tip,
            candidate_path_oids=self.v099.reachability.path_oids,
            transition_path_oids=(self.anchor_tip,),
        )
        history = self._history(samples=(self.anchor_sample, equal2, equal3))
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_COMMITTED)
        self.assertTrue(certificate.equal_tip_policy_satisfied)

    def test_equal_tip_policy_rejects_repeated_tip(self) -> None:
        policy = self._policy(allow_equal_tip=False)
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.equal_tip_policy_satisfied)

    def test_tip_advance_policy_rejects_advanced_history(self) -> None:
        policy = self._policy(allow_tip_advance=False)
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.tip_advance_policy_satisfied)

    def test_sample_count_bounds_are_enforced(self) -> None:
        history = self._history(samples=(self.anchor_sample, self.sample2))
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.sample_count_within_policy)

    def test_sample_binding_mismatches_are_rejected(self) -> None:
        cases = (
            ("transaction_id", "different-transaction-v100"),
            ("repository_id", "different-repository-v100"),
            ("target_reference", "refs/heads/other"),
            ("candidate_commit_oid", "1" * 40),
        )
        for field, value in cases:
            sample = self._resign_sample(replace(self.sample2, **{field: value}))
            history = self._history(
                samples=(self.anchor_sample, sample, self.sample3)
            )
            certificate = self._certify(history=history)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
            self.assertFalse(certificate.sample_bindings_exact)

    def test_anchor_sample_tamper_is_rejected(self) -> None:
        sample = self._resign_sample(
            replace(
                self.anchor_sample,
                sequence_number=self.anchor_sample.sequence_number + 1,
            )
        )
        history = self._history(samples=(sample, self.sample2, self.sample3))
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.anchor_sample_exact)

    def test_unauthorized_or_noncommon_observer_is_rejected(self) -> None:
        sample = self._resign_sample(
            replace(self.sample2, observer_id="other-observer-v100")
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.common_observer_exact)
        self.assertFalse(certificate.observers_authorized)

    def test_wrong_observation_sources_are_rejected(self) -> None:
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
            sample = self._resign_sample(replace(self.sample2, **changes))
            history = self._history(
                samples=(self.anchor_sample, sample, self.sample3)
            )
            certificate = self._certify(history=history)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_delete_or_force_evidence_is_rejected(self) -> None:
        for field in ("reference_deleted", "force_update_observed"):
            sample = self._resign_sample(
                replace(self.sample2, **{field: True})
            )
            history = self._history(
                samples=(self.anchor_sample, sample, self.sample3)
            )
            certificate = self._certify(history=history)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_sequence_must_strictly_increase(self) -> None:
        sample = self._resign_sample(
            replace(
                self.sample2,
                sequence_number=self.anchor_sample.sequence_number,
            )
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.sequences_strictly_increasing)

    def test_observation_time_must_strictly_increase(self) -> None:
        sample = self._resign_sample(
            replace(
                self.sample2,
                observed_at_epoch_seconds=self.anchor_sample.observed_at_epoch_seconds,
            )
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.observation_times_strictly_increasing)

    def test_inter_sample_interval_bounds_are_enforced(self) -> None:
        sample = self._resign_sample(
            replace(self.sample2, observed_at_epoch_seconds=10_110)
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.inter_sample_intervals_within_policy)

    def test_total_interval_bounds_are_enforced(self) -> None:
        policy = self._policy(min_total_interval_seconds=90)
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.total_interval_within_policy)

    def test_stale_or_future_history_is_rejected(self) -> None:
        stale = self._certify(evaluated_at_epoch_seconds=10_200)
        self.assertEqual(stale.status, CERTIFICATE_REJECTED)
        self.assertFalse(stale.history_fresh)
        future = self._certify(evaluated_at_epoch_seconds=10_150)
        self.assertEqual(future.status, CERTIFICATE_REJECTED)
        self.assertFalse(future.no_future_evidence)

    def test_candidate_path_must_be_complete(self) -> None:
        sample = self._sample2(
            candidate_path_oids=(self.tip2, self.anchor_tip)
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.candidate_paths_complete)

    def test_candidate_parent_edge_tamper_is_rejected(self) -> None:
        sample = self._resign_sample(
            replace(
                self.sample2,
                candidate_parent_edges=((self.tip2, self.anchor_tip),),
            )
        )
        history = self._history(
            samples=(self.anchor_sample, sample, self.sample3)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.candidate_parent_edges_exact)

    def test_transition_path_must_reach_immediate_previous_tip(self) -> None:
        sample = self._sample3(
            previous_tip_oid=self.anchor_tip,
            transition_path_oids=(self.tip3, self.anchor_tip),
        )
        history = self._history(
            samples=(self.anchor_sample, self.sample2, sample)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.transition_paths_complete)
        self.assertFalse(certificate.frontier_transitions_monotone)

    def test_transition_parent_edge_tamper_is_rejected(self) -> None:
        sample = self._resign_sample(
            replace(
                self.sample3,
                transition_parent_edges=((self.tip3, self.anchor_tip),),
            )
        )
        history = self._history(
            samples=(self.anchor_sample, self.sample2, sample)
        )
        certificate = self._certify(history=history)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.transition_parent_edges_exact)

    def test_queried_set_inventory_and_commit_kind_are_enforced(self) -> None:
        cases = (
            {"queried_oid_set_complete": False},
            {"queried_oids": tuple(sorted((self.tip2, self.anchor_tip)))},
            {
                "object_database_commit_oids": tuple(
                    sorted((self.tip2, self.anchor_tip))
                )
            },
            {"all_objects_are_commits": False},
        )
        for changes in cases:
            sample = self._resign_sample(replace(self.sample2, **changes))
            history = self._history(
                samples=(self.anchor_sample, sample, self.sample3)
            )
            certificate = self._certify(history=history)
            self.assertEqual(certificate.status, CERTIFICATE_REJECTED)

    def test_candidate_and_transition_depth_bounds_are_enforced(self) -> None:
        policy = self._policy(
            max_candidate_reachability_depth=3,
            max_transition_depth=0,
        )
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.candidate_depths_within_policy)
        self.assertFalse(certificate.transition_depths_within_policy)

    def test_total_queried_node_bound_is_enforced(self) -> None:
        policy = self._policy(max_total_queried_nodes=11)
        certificate = self._certify(policy=policy)
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.total_queried_nodes_within_policy)

    def test_rejected_v099_certificate_cannot_commit_finality(self) -> None:
        v099_policy = self.v099._policy(allow_tip_advance=False)
        stability = self.v099._certify(policy=v099_policy)
        stability_inputs = self.v099._values(policy=v099_policy)
        stability_inputs.pop("certificate_id")
        history = self._history(stability_certificate=stability)
        certificate = self._certify(
            reference_stability_certificate=stability,
            reference_stability_inputs=stability_inputs,
            history=history,
        )
        self.assertEqual(certificate.status, CERTIFICATE_REJECTED)
        self.assertFalse(certificate.reference_stability_certificate_committed)

    def test_v099_tamper_is_rejected_after_outer_digest_recompute(self) -> None:
        stability = self._resign_stability(
            replace(
                self.stability_certificate,
                candidate_reachability_preserved=False,
            )
        )
        with self.assertRaisesRegex(
            ValueError,
            "reference_stability_certificate_invalid",
        ):
            self._certify(reference_stability_certificate=stability)

    def test_duplicate_sample_id_is_structurally_rejected(self) -> None:
        duplicate = self._resign_sample(
            replace(self.sample2, sample_id=self.anchor_sample.sample_id)
        )
        with self.assertRaisesRegex(ValueError, "local_frontier_history_invalid"):
            self._history(
                samples=(self.anchor_sample, duplicate, self.sample3)
            )

    def test_certificate_makes_no_absolute_or_external_claim(self) -> None:
        certificate = self._certify()
        for field in (
            "absolute_finality_claimed",
            "remote_finality_claimed",
            "branch_protection_verified",
            "garbage_collection_retention_guaranteed",
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
            replace(
                certificate,
                remote_finality_claimed=True,
                push_performed=True,
            )
        )
        issues = self._issues(tampered)
        self.assertIn("local_frontier_certificate_recomputation_mismatch", issues)
        self.assertIn("local_frontier_certificate_forbidden_claim", issues)
        self.assertIn("local_frontier_certificate_forbidden_effect", issues)


if __name__ == "__main__":
    unittest.main()
