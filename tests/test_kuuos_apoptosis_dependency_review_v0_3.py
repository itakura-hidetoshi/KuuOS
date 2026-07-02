from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_candidate_types_v0_2 import apoptosis_candidate_record_digest
from runtime.kuuos_apoptosis_candidate_v0_2 import (
    build_apoptosis_candidate_policy,
    build_apoptosis_candidate_request,
    issue_apoptosis_candidate,
)
from runtime.kuuos_apoptosis_dependency_review_types_v0_3 import (
    DEPENDENCY_REVIEW_BLOCKED,
    DEPENDENCY_REVIEW_CLEAR,
    DEPENDENCY_REVIEW_REJECTED,
    apoptosis_dependency_evidence_digest,
    apoptosis_dependency_review_policy_digest,
    apoptosis_dependency_review_record_digest,
    apoptosis_dependency_review_request_digest,
)
from runtime.kuuos_apoptosis_dependency_review_v0_3 import (
    apoptosis_dependency_review_record_issues,
    build_apoptosis_dependency_evidence,
    build_apoptosis_dependency_review_policy,
    build_apoptosis_dependency_review_request,
    review_apoptosis_dependencies,
)
from runtime.kuuos_apoptosis_observation_types_v0_1 import SUBJECT_MODULE
from runtime.kuuos_apoptosis_observation_v0_1 import (
    build_apoptosis_observation_input,
    build_apoptosis_observation_policy,
    observe_apoptosis_signal,
)


class ApoptosisDependencyReviewV03Tests(unittest.TestCase):
    observed_at = 1_900_000_000
    candidate_at = observed_at + 30
    evidence_at = candidate_at + 10
    reviewed_at = candidate_at + 30

    def setUp(self) -> None:
        self.observation_policy = build_apoptosis_observation_policy(
            "observation-policy-v0-1",
            protected_subject_ids=("constitutional-core",),
            max_evidence_age_seconds=300,
            repeated_failure_threshold=3,
            inactivity_threshold_seconds=1_000,
        )
        self.candidate_policy = build_apoptosis_candidate_policy(
            "candidate-policy-v0-2",
            allowed_issuer_ids=("lifecycle-reviewer",),
            max_candidate_delay_seconds=600,
        )
        self.review_policy = build_apoptosis_dependency_review_policy(
            "dependency-review-policy-v0-3",
            allowed_reviewer_ids=("dependency-reviewer",),
            max_review_delay_seconds=600,
            max_evidence_age_seconds=300,
        )

    def source(self, *, replacement_verified: bool = True):
        observation_input = build_apoptosis_observation_input(
            "observation-001",
            "candidate-module",
            SUBJECT_MODULE,
            "v0.42",
            provenance_digest="p" * 64,
            dependency_snapshot_digest="d" * 64,
            authority_snapshot_digest="a" * 64,
            usage_evidence_digest="u" * 64,
            risk_evidence_digest="r" * 64,
            replacement_evidence_digest="x" * 64,
            observed_at_epoch_seconds=self.observed_at,
            evidence_captured_at_epoch_seconds=self.observed_at - 10,
            active_dependency_count=0,
            active_authority_count=0,
            active_execution_count=0,
            unresolved_incident_count=0,
            repeated_failure_count=0,
            inactive_for_seconds=0,
            replacement_verified=replacement_verified,
            evidence_complete=True,
            constitutional_protected=False,
            institutional_hold=False,
        )
        observation_record = observe_apoptosis_signal(
            observation_input,
            self.observation_policy,
        )
        candidate_request = build_apoptosis_candidate_request(
            "candidate-001",
            "lifecycle-reviewer",
            self.candidate_at,
            observation_input,
            self.observation_policy,
            observation_record,
        )
        candidate_record = issue_apoptosis_candidate(
            candidate_request,
            observation_input,
            self.observation_policy,
            observation_record,
            self.candidate_policy,
        )
        return observation_input, observation_record, candidate_request, candidate_record

    def evidence(self, candidate_request, candidate_record, **overrides):
        values = dict(
            evidence_id="dependency-evidence-001",
            subject_id=candidate_record.subject_id,
            subject_kind=candidate_record.subject_kind,
            subject_version=candidate_record.subject_version,
            captured_at_epoch_seconds=self.evidence_at,
            dependency_snapshot_digest=candidate_request.dependency_snapshot_digest,
            graph_snapshot_digest="g" * 64,
            direct_dependency_ids=(),
            direct_dependent_ids=(),
            critical_dependent_ids=(),
            replacement_covered_dependent_ids=(),
            unresolved_dependency_ids=(),
            cycle_member_ids=(),
            active_execution_dependent_ids=(),
            closure_complete=True,
        )
        values.update(overrides)
        return build_apoptosis_dependency_evidence(**values)

    def request(self, candidate_request, candidate_record, evidence, **overrides):
        values = dict(
            review_id="dependency-review-001",
            reviewer_id="dependency-reviewer",
            reviewed_at_epoch_seconds=self.reviewed_at,
            candidate_request=candidate_request,
            candidate_policy=self.candidate_policy,
            candidate_record=candidate_record,
            evidence=evidence,
        )
        values.update(overrides)
        return build_apoptosis_dependency_review_request(**values)

    def execute(self, source=None, evidence=None, request=None, review_policy=None):
        source = self.source() if source is None else source
        evidence = self.evidence(source[2], source[3]) if evidence is None else evidence
        request = self.request(source[2], source[3], evidence) if request is None else request
        return review_apoptosis_dependencies(
            request,
            evidence,
            self.review_policy if review_policy is None else review_policy,
            source[0],
            self.observation_policy,
            source[1],
            source[2],
            self.candidate_policy,
            source[3],
        )

    def test_empty_surface_is_clear_for_further_review(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, DEPENDENCY_REVIEW_CLEAR)
        self.assertTrue(record.dependency_review_record_issued)
        self.assertTrue(record.dependency_clear_for_further_review)

    def test_replacement_covered_dependents_are_clear(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3],
            direct_dependent_ids=("agent-a", "agent-b"),
            critical_dependent_ids=("agent-a",),
            replacement_covered_dependent_ids=("agent-a", "agent-b"),
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_CLEAR)
        self.assertTrue(record.replacement_coverage_complete)

    def test_incomplete_closure_is_blocked(self) -> None:
        source = self.source()
        record = self.execute(source, self.evidence(source[2], source[3], closure_complete=False))
        self.assertEqual(record.status, DEPENDENCY_REVIEW_BLOCKED)
        self.assertEqual(record.reason, "dependency_closure_incomplete")

    def test_cycle_is_blocked(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3], cycle_member_ids=(source[3].subject_id, "agent-a")
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_BLOCKED)
        self.assertTrue(record.cycle_through_subject_present)

    def test_unresolved_dependency_is_blocked(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3],
            direct_dependency_ids=("service-a",),
            unresolved_dependency_ids=("service-a",),
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_BLOCKED)
        self.assertTrue(record.unresolved_dependencies_present)

    def test_orphaned_and_critical_dependents_are_blocked(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3],
            direct_dependent_ids=("critical-agent",),
            critical_dependent_ids=("critical-agent",),
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_BLOCKED)
        self.assertTrue(record.orphaned_dependents_present)
        self.assertTrue(record.uncovered_critical_dependents_present)

    def test_active_execution_dependence_is_blocked(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3],
            direct_dependent_ids=("active-agent",),
            replacement_covered_dependent_ids=("active-agent",),
            active_execution_dependent_ids=("active-agent",),
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_BLOCKED)
        self.assertTrue(record.active_execution_dependence_present)

    def test_rejected_candidate_source_is_rejected(self) -> None:
        source = self.source(replacement_verified=False)
        record = self.execute(source)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_REJECTED)
        self.assertFalse(record.source_candidate_proposed)

    def test_tampered_candidate_is_rejected_after_fresh_digest(self) -> None:
        source = self.source()
        candidate = replace(source[3], terminal_transition_performed=True, candidate_digest="")
        candidate = replace(candidate, candidate_digest=apoptosis_candidate_record_digest(candidate))
        tampered_source = source[0], source[1], source[2], candidate
        evidence = self.evidence(source[2], candidate)
        request = self.request(source[2], candidate, evidence)
        record = self.execute(tampered_source, evidence, request)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_reviewer_objective_and_time_guards_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source[2], source[3])
        cases = (
            {"reviewer_id": "unknown-reviewer"},
            {"objective": "UNAUTHORIZED_OBJECTIVE"},
            {"reviewed_at_epoch_seconds": self.candidate_at + 601},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                request = self.request(source[2], source[3], evidence, **overrides)
                self.assertEqual(
                    self.execute(source, evidence, request).status,
                    DEPENDENCY_REVIEW_REJECTED,
                )

    def test_stale_evidence_is_rejected(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source[2], source[3], captured_at_epoch_seconds=self.reviewed_at - 301
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_REJECTED)
        self.assertFalse(record.evidence_fresh)

    def test_subject_and_snapshot_binding_tamper_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source[2], source[3])
        request = self.request(source[2], source[3], evidence)
        subject_request = replace(request, subject_id="different-subject", request_digest="")
        subject_request = replace(
            subject_request,
            request_digest=apoptosis_dependency_review_request_digest(subject_request),
        )
        snapshot_request = replace(
            request, dependency_snapshot_digest="z" * 64, request_digest=""
        )
        snapshot_request = replace(
            snapshot_request,
            request_digest=apoptosis_dependency_review_request_digest(snapshot_request),
        )
        self.assertEqual(
            self.execute(source, evidence, subject_request).status,
            DEPENDENCY_REVIEW_REJECTED,
        )
        self.assertEqual(
            self.execute(source, evidence, snapshot_request).status,
            DEPENDENCY_REVIEW_REJECTED,
        )

    def test_invalid_evidence_subset_is_rejected_by_builder(self) -> None:
        source = self.source()
        with self.assertRaises(ValueError):
            self.evidence(
                source[2], source[3],
                critical_dependent_ids=("not-a-direct-dependent",),
            )

    def test_effect_enabling_policy_is_rejected(self) -> None:
        unsafe = replace(
            self.review_policy, allow_repository_mutation=True, policy_digest=""
        )
        unsafe = replace(
            unsafe, policy_digest=apoptosis_dependency_review_policy_digest(unsafe)
        )
        record = self.execute(review_policy=unsafe)
        self.assertEqual(record.status, DEPENDENCY_REVIEW_REJECTED)
        self.assertFalse(record.repository_mutation_performed)

    def test_clear_requires_next_reviews_but_blocked_does_not_advance(self) -> None:
        clear = self.execute()
        self.assertTrue(clear.authority_review_required_next)
        self.assertTrue(clear.quiescence_review_required_next)
        self.assertTrue(clear.external_review_required_next)
        self.assertTrue(clear.independent_authorization_required_next)
        source = self.source()
        blocked_evidence = self.evidence(
            source[2], source[3], direct_dependent_ids=("agent-a",)
        )
        blocked = self.execute(source, blocked_evidence)
        self.assertFalse(blocked.authority_review_required_next)
        self.assertFalse(blocked.quiescence_review_required_next)
        self.assertFalse(blocked.external_review_required_next)
        self.assertFalse(blocked.independent_authorization_required_next)

    def test_all_outcomes_are_read_only_and_deterministic(self) -> None:
        clear_left = self.execute()
        clear_right = self.execute()
        self.assertEqual(clear_left, clear_right)
        source = self.source()
        blocked = self.execute(
            source,
            self.evidence(source[2], source[3], direct_dependent_ids=("agent-a",)),
        )
        rejected = self.execute(self.source(replacement_verified=False))
        for record in (clear_left, blocked, rejected):
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

    def test_record_and_evidence_tamper_are_detected(self) -> None:
        source = self.source()
        evidence = self.evidence(source[2], source[3])
        request = self.request(source[2], source[3], evidence)
        record = self.execute(source, evidence, request)
        tampered_record = replace(
            record, physical_deletion_performed=True, record_digest=""
        )
        tampered_record = replace(
            tampered_record,
            record_digest=apoptosis_dependency_review_record_digest(tampered_record),
        )
        issues = apoptosis_dependency_review_record_issues(
            tampered_record, request, evidence, self.review_policy,
            source[0], self.observation_policy, source[1], source[2],
            self.candidate_policy, source[3],
        )
        self.assertIn("apoptosis_dependency_review_recomputation_mismatch", issues)
        self.assertIn("apoptosis_dependency_execution_effect_performed", issues)
        tampered_evidence = replace(
            evidence, dependency_snapshot_digest="q" * 64, evidence_digest=""
        )
        tampered_evidence = replace(
            tampered_evidence,
            evidence_digest=apoptosis_dependency_evidence_digest(tampered_evidence),
        )
        tampered_request = self.request(source[2], source[3], tampered_evidence)
        self.assertEqual(
            self.execute(source, tampered_evidence, tampered_request).status,
            DEPENDENCY_REVIEW_REJECTED,
        )


if __name__ == "__main__":
    unittest.main()
