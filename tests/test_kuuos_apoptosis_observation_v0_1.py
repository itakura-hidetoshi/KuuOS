from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    OBSERVATION_NO_ACTION,
    OBSERVATION_PROTECTED,
    OBSERVATION_REJECTED,
    OBSERVATION_REVIEW_RECOMMENDED,
    SUBJECT_AGENT,
    SUBJECT_MODULE,
    apoptosis_observation_policy_digest,
    apoptosis_observation_record_digest,
)
from runtime.kuuos_apoptosis_observation_v0_1 import (
    apoptosis_observation_record_issues,
    build_apoptosis_observation_input,
    build_apoptosis_observation_policy,
    observe_apoptosis_signal,
)


class ApoptosisObservationV01Tests(unittest.TestCase):
    observed_at = 1_900_000_000

    def setUp(self) -> None:
        self.policy = build_apoptosis_observation_policy(
            "apoptosis-observation-policy-v0-1",
            protected_subject_ids=("constitutional-core",),
            max_evidence_age_seconds=300,
            repeated_failure_threshold=3,
            inactivity_threshold_seconds=1_000,
        )

    def observation(self, **overrides):
        arguments = {
            "observation_id": "apoptosis-observation-v0-1-001",
            "subject_id": "candidate-module",
            "subject_kind": SUBJECT_MODULE,
            "subject_version": "v0.42",
            "provenance_digest": "p" * 64,
            "dependency_snapshot_digest": "d" * 64,
            "authority_snapshot_digest": "a" * 64,
            "usage_evidence_digest": "u" * 64,
            "risk_evidence_digest": "r" * 64,
            "replacement_evidence_digest": "x" * 64,
            "observed_at_epoch_seconds": self.observed_at,
            "evidence_captured_at_epoch_seconds": self.observed_at - 10,
            "active_dependency_count": 0,
            "active_authority_count": 0,
            "active_execution_count": 0,
            "unresolved_incident_count": 0,
            "repeated_failure_count": 0,
            "inactive_for_seconds": 0,
            "replacement_verified": False,
            "evidence_complete": True,
            "constitutional_protected": False,
            "institutional_hold": False,
        }
        arguments.update(overrides)
        return build_apoptosis_observation_input(**arguments)

    def observe(self, observation=None, policy=None):
        return observe_apoptosis_signal(
            self.observation() if observation is None else observation,
            self.policy if policy is None else policy,
        )

    def test_healthy_subject_requires_no_action(self) -> None:
        record = self.observe()
        self.assertEqual(record.status, OBSERVATION_NO_ACTION)
        self.assertFalse(record.degradation_signal_present)
        self.assertFalse(record.external_review_required)
        self.assertFalse(record.apoptosis_candidate_issued)

    def test_verified_replacement_recommends_independent_review(self) -> None:
        record = self.observe(self.observation(replacement_verified=True))
        self.assertEqual(record.status, OBSERVATION_REVIEW_RECOMMENDED)
        self.assertTrue(record.replacement_signal)
        self.assertTrue(record.dependency_review_required)
        self.assertTrue(record.authority_review_required)
        self.assertTrue(record.quiescence_review_required)
        self.assertTrue(record.external_review_required)
        self.assertTrue(record.independent_candidate_stage_required)
        self.assertTrue(record.independent_authorization_required)

    def test_repeated_failures_recommend_review(self) -> None:
        record = self.observe(self.observation(repeated_failure_count=3))
        self.assertEqual(record.status, OBSERVATION_REVIEW_RECOMMENDED)
        self.assertTrue(record.repeated_failure_signal)

    def test_long_inactivity_recommends_review(self) -> None:
        record = self.observe(self.observation(inactive_for_seconds=1_000))
        self.assertEqual(record.status, OBSERVATION_REVIEW_RECOMMENDED)
        self.assertTrue(record.inactivity_signal)

    def test_unresolved_incident_recommends_review(self) -> None:
        record = self.observe(self.observation(unresolved_incident_count=1))
        self.assertEqual(record.status, OBSERVATION_REVIEW_RECOMMENDED)
        self.assertTrue(record.unresolved_incident_signal)

    def test_active_surfaces_are_reported_without_transition(self) -> None:
        record = self.observe(
            self.observation(
                replacement_verified=True,
                active_dependency_count=2,
                active_authority_count=1,
                active_execution_count=3,
            )
        )
        self.assertTrue(record.active_dependencies_present)
        self.assertTrue(record.active_authorities_present)
        self.assertTrue(record.active_executions_present)
        self.assertFalse(record.authority_revocation_performed)
        self.assertFalse(record.quiescence_transition_performed)
        self.assertFalse(record.terminal_transition_performed)

    def test_constitutional_core_is_protected(self) -> None:
        record = self.observe(
            self.observation(
                replacement_verified=True,
                constitutional_protected=True,
            )
        )
        self.assertEqual(record.status, OBSERVATION_PROTECTED)
        self.assertTrue(record.protected_subject)
        self.assertFalse(record.apoptosis_candidate_issued)

    def test_policy_protected_subject_is_protected(self) -> None:
        record = self.observe(
            self.observation(
                subject_id="constitutional-core",
                replacement_verified=True,
            )
        )
        self.assertEqual(record.status, OBSERVATION_PROTECTED)
        self.assertTrue(record.protected_subject)

    def test_institutional_hold_is_protected(self) -> None:
        record = self.observe(
            self.observation(
                replacement_verified=True,
                institutional_hold=True,
            )
        )
        self.assertEqual(record.status, OBSERVATION_PROTECTED)
        self.assertTrue(record.institutional_hold_present)

    def test_incomplete_evidence_is_rejected(self) -> None:
        record = self.observe(self.observation(evidence_complete=False))
        self.assertEqual(record.status, OBSERVATION_REJECTED)
        self.assertFalse(record.evidence_complete)

    def test_stale_evidence_is_rejected(self) -> None:
        record = self.observe(
            self.observation(
                evidence_captured_at_epoch_seconds=self.observed_at - 301,
            )
        )
        self.assertEqual(record.status, OBSERVATION_REJECTED)
        self.assertFalse(record.evidence_fresh)

    def test_unknown_subject_kind_is_rejected(self) -> None:
        record = self.observe(self.observation(subject_kind="UNKNOWN"))
        self.assertEqual(record.status, OBSERVATION_REJECTED)
        self.assertFalse(record.subject_kind_allowed)

    def test_effect_enabling_policy_is_rejected(self) -> None:
        unsafe = replace(
            self.policy,
            allow_physical_deletion=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_observation_policy_digest(unsafe),
        )
        record = self.observe(policy=unsafe)
        self.assertEqual(record.status, OBSERVATION_REJECTED)
        self.assertFalse(record.checks["policy_valid"])
        self.assertFalse(record.physical_deletion_performed)

    def test_all_observations_are_read_only(self) -> None:
        records = [
            self.observe(),
            self.observe(self.observation(replacement_verified=True)),
            self.observe(self.observation(evidence_complete=False)),
            self.observe(
                self.observation(
                    replacement_verified=True,
                    constitutional_protected=True,
                )
            ),
        ]
        for record in records:
            self.assertFalse(record.apoptosis_candidate_issued)
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

    def test_same_input_is_deterministic(self) -> None:
        observation = self.observation(
            subject_kind=SUBJECT_AGENT,
            repeated_failure_count=3,
        )
        self.assertEqual(self.observe(observation), self.observe(observation))

    def test_record_tamper_is_detected(self) -> None:
        observation = self.observation(replacement_verified=True)
        record = self.observe(observation)
        tampered = replace(
            record,
            terminal_transition_performed=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_observation_record_digest(tampered),
        )
        issues = apoptosis_observation_record_issues(
            tampered,
            observation,
            self.policy,
        )
        self.assertIn("apoptosis_observation_recomputation_mismatch", issues)
        self.assertIn("apoptosis_observation_effect_performed", issues)


if __name__ == "__main__":
    unittest.main()
