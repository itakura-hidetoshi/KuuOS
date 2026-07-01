from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_candidate_types_v0_2 import (
    CANDIDATE_PROPOSED,
    CANDIDATE_REJECTED,
    apoptosis_candidate_policy_digest,
    apoptosis_candidate_record_digest,
    apoptosis_candidate_request_digest,
)
from runtime.kuuos_apoptosis_candidate_v0_2 import (
    apoptosis_candidate_record_issues,
    build_apoptosis_candidate_policy,
    build_apoptosis_candidate_request,
    issue_apoptosis_candidate,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import (
    SUBJECT_AGENT,
    SUBJECT_MODULE,
    apoptosis_observation_record_digest,
)
from runtime.kuuos_apoptosis_observation_v0_1 import (
    build_apoptosis_observation_input,
    build_apoptosis_observation_policy,
    observe_apoptosis_signal,
)


class ApoptosisCandidateV02Tests(unittest.TestCase):
    observed_at = 1_900_000_000

    def setUp(self) -> None:
        self.observation_policy = build_apoptosis_observation_policy(
            "apoptosis-observation-policy-v0-1",
            protected_subject_ids=("constitutional-core",),
            max_evidence_age_seconds=300,
            repeated_failure_threshold=3,
            inactivity_threshold_seconds=1_000,
        )
        self.candidate_policy = build_apoptosis_candidate_policy(
            "apoptosis-candidate-policy-v0-2",
            allowed_issuer_ids=("lifecycle-reviewer",),
            max_candidate_delay_seconds=600,
        )

    def observation_input(self, **overrides):
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
            "replacement_verified": True,
            "evidence_complete": True,
            "constitutional_protected": False,
            "institutional_hold": False,
        }
        arguments.update(overrides)
        return build_apoptosis_observation_input(**arguments)

    def source(self, **overrides):
        source_input = self.observation_input(**overrides)
        source_record = observe_apoptosis_signal(
            source_input,
            self.observation_policy,
        )
        return source_input, source_record

    def request(self, source_input, source_record, **overrides):
        arguments = {
            "candidate_id": "apoptosis-candidate-v0-2-001",
            "issuer_id": "lifecycle-reviewer",
            "issued_at_epoch_seconds": self.observed_at + 30,
            "source_input": source_input,
            "source_policy": self.observation_policy,
            "source_record": source_record,
        }
        arguments.update(overrides)
        return build_apoptosis_candidate_request(**arguments)

    def issue(self, source_input=None, source_record=None, request=None, policy=None):
        if source_input is None or source_record is None:
            source_input, source_record = self.source()
        if request is None:
            request = self.request(source_input, source_record)
        return issue_apoptosis_candidate(
            request,
            source_input,
            self.observation_policy,
            source_record,
            self.candidate_policy if policy is None else policy,
        )

    def test_review_recommended_source_proposes_candidate(self) -> None:
        record = self.issue()
        self.assertEqual(record.status, CANDIDATE_PROPOSED)
        self.assertTrue(record.source_recomputed_valid)
        self.assertTrue(record.source_review_recommended)
        self.assertTrue(record.candidate_artifact_issued)

    def test_candidate_requires_all_independent_reviews(self) -> None:
        record = self.issue()
        self.assertTrue(record.dependency_review_required)
        self.assertTrue(record.authority_review_required)
        self.assertTrue(record.quiescence_review_required)
        self.assertTrue(record.external_review_required)
        self.assertTrue(record.independent_authorization_required)

    def test_no_action_source_is_rejected(self) -> None:
        source_input, source_record = self.source(replacement_verified=False)
        request = self.request(source_input, source_record)
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_review_recommended)
        self.assertFalse(record.candidate_artifact_issued)

    def test_protected_source_is_rejected(self) -> None:
        source_input, source_record = self.source(
            subject_id="constitutional-core",
            replacement_verified=True,
        )
        request = self.request(source_input, source_record)
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_non_protected)

    def test_institutional_hold_source_is_rejected(self) -> None:
        source_input, source_record = self.source(institutional_hold=True)
        request = self.request(source_input, source_record)
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_no_hold)

    def test_unauthorized_issuer_is_rejected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(
            source_input,
            source_record,
            issuer_id="unauthorized-issuer",
        )
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.issuer_allowed)

    def test_non_governance_objective_is_rejected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(
            source_input,
            source_record,
            objective="TERMINATE_NOW",
        )
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.objective_allowed)

    def test_stale_candidate_request_is_rejected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(
            source_input,
            source_record,
            issued_at_epoch_seconds=self.observed_at + 601,
        )
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.candidate_delay_valid)

    def test_tampered_source_record_is_rejected_after_fresh_digest(self) -> None:
        source_input, source_record = self.source()
        tampered = replace(
            source_record,
            active_executions_present=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_observation_record_digest(tampered),
        )
        request = self.request(source_input, tampered)
        record = self.issue(source_input, tampered, request)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_subject_binding_tamper_is_rejected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(source_input, source_record)
        tampered = replace(request, subject_id="different-subject", request_digest="")
        tampered = replace(
            tampered,
            request_digest=apoptosis_candidate_request_digest(tampered),
        )
        record = self.issue(source_input, source_record, tampered)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_subject_binding_valid)

    def test_dependency_binding_tamper_is_rejected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(source_input, source_record)
        tampered = replace(
            request,
            dependency_snapshot_digest="z" * 64,
            request_digest="",
        )
        tampered = replace(
            tampered,
            request_digest=apoptosis_candidate_request_digest(tampered),
        )
        record = self.issue(source_input, source_record, tampered)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.source_dependency_binding_valid)

    def test_active_surfaces_remain_review_only(self) -> None:
        source_input, source_record = self.source(
            subject_kind=SUBJECT_AGENT,
            active_dependency_count=2,
            active_authority_count=1,
            active_execution_count=3,
        )
        request = self.request(source_input, source_record)
        record = self.issue(source_input, source_record, request)
        self.assertEqual(record.status, CANDIDATE_PROPOSED)
        self.assertTrue(record.source_rationale_binding_valid)
        self.assertTrue(record.quiescence_review_required)
        self.assertFalse(record.quiescence_transition_performed)
        self.assertFalse(record.authority_revocation_performed)

    def test_effect_enabling_policy_is_rejected(self) -> None:
        unsafe = replace(
            self.candidate_policy,
            allow_physical_deletion=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_candidate_policy_digest(unsafe),
        )
        record = self.issue(policy=unsafe)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.checks["policy_valid"])
        self.assertFalse(record.physical_deletion_performed)

    def test_candidate_issuance_disabled_policy_is_rejected(self) -> None:
        disabled = replace(
            self.candidate_policy,
            allow_candidate_artifact_issuance=False,
            policy_digest="",
        )
        disabled = replace(
            disabled,
            policy_digest=apoptosis_candidate_policy_digest(disabled),
        )
        record = self.issue(policy=disabled)
        self.assertEqual(record.status, CANDIDATE_REJECTED)
        self.assertFalse(record.candidate_artifact_issued)

    def test_all_candidate_records_perform_no_execution_effect(self) -> None:
        proposed = self.issue()
        source_input, source_record = self.source(replacement_verified=False)
        rejected = self.issue(
            source_input,
            source_record,
            self.request(source_input, source_record),
        )
        for record in (proposed, rejected):
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

    def test_same_input_is_deterministic(self) -> None:
        source_input, source_record = self.source()
        request = self.request(source_input, source_record)
        left = self.issue(source_input, source_record, request)
        right = self.issue(source_input, source_record, request)
        self.assertEqual(left, right)

    def test_candidate_record_tamper_is_detected(self) -> None:
        source_input, source_record = self.source()
        request = self.request(source_input, source_record)
        record = self.issue(source_input, source_record, request)
        tampered = replace(
            record,
            terminal_transition_performed=True,
            candidate_digest="",
        )
        tampered = replace(
            tampered,
            candidate_digest=apoptosis_candidate_record_digest(tampered),
        )
        issues = apoptosis_candidate_record_issues(
            tampered,
            request,
            source_input,
            self.observation_policy,
            source_record,
            self.candidate_policy,
        )
        self.assertIn("apoptosis_candidate_recomputation_mismatch", issues)
        self.assertIn("apoptosis_candidate_execution_effect_performed", issues)


if __name__ == "__main__":
    unittest.main()
