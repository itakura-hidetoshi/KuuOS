from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    AUTHORITY_REVIEW_BLOCKED,
    AUTHORITY_REVIEW_CLEAR,
    AUTHORITY_REVIEW_REJECTED,
    apoptosis_authority_review_policy_digest,
    apoptosis_authority_review_record_digest,
    apoptosis_authority_review_request_digest,
)
from runtime.kuuos_apoptosis_authority_review_v0_4 import (
    apoptosis_authority_review_record_issues,
    build_apoptosis_authority_evidence,
    build_apoptosis_authority_review_policy,
    build_apoptosis_authority_review_request,
    review_apoptosis_authority,
)
from runtime.kuuos_apoptosis_candidate_v0_2 import (
    build_apoptosis_candidate_policy,
    build_apoptosis_candidate_request,
    issue_apoptosis_candidate,
)
from runtime.kuuos_apoptosis_dependency_review_v0_3 import (
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


class ApoptosisAuthorityReviewV04Tests(unittest.TestCase):
    observed_at = 1_900_000_000
    candidate_at = observed_at + 30
    dependency_evidence_at = candidate_at + 10
    dependency_reviewed_at = candidate_at + 30
    authority_evidence_at = dependency_reviewed_at + 10
    authority_reviewed_at = dependency_reviewed_at + 30

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
        self.dependency_policy = build_apoptosis_dependency_review_policy(
            "dependency-review-policy-v0-3",
            allowed_reviewer_ids=("dependency-reviewer",),
            max_review_delay_seconds=600,
            max_evidence_age_seconds=300,
        )
        self.authority_policy = build_apoptosis_authority_review_policy(
            "authority-review-policy-v0-4",
            allowed_reviewer_ids=(
                "authority-reviewer",
                "dependency-reviewer",
                "lifecycle-reviewer",
                "responsible-authority",
            ),
            max_review_delay_seconds=600,
            max_evidence_age_seconds=300,
        )

    def source(self, *, dependency_blocked: bool = False):
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
            replacement_verified=True,
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
        dependent_ids = ("dependent-agent",) if dependency_blocked else ()
        dependency_evidence = build_apoptosis_dependency_evidence(
            "dependency-evidence-001",
            candidate_record.subject_id,
            candidate_record.subject_kind,
            candidate_record.subject_version,
            captured_at_epoch_seconds=self.dependency_evidence_at,
            dependency_snapshot_digest=candidate_request.dependency_snapshot_digest,
            graph_snapshot_digest="g" * 64,
            direct_dependency_ids=(),
            direct_dependent_ids=dependent_ids,
            critical_dependent_ids=(),
            replacement_covered_dependent_ids=(),
            unresolved_dependency_ids=(),
            cycle_member_ids=(),
            active_execution_dependent_ids=(),
            closure_complete=True,
        )
        dependency_request = build_apoptosis_dependency_review_request(
            "dependency-review-001",
            "dependency-reviewer",
            self.dependency_reviewed_at,
            candidate_request,
            self.candidate_policy,
            candidate_record,
            dependency_evidence,
        )
        dependency_record = review_apoptosis_dependencies(
            dependency_request,
            dependency_evidence,
            self.dependency_policy,
            observation_input,
            self.observation_policy,
            observation_record,
            candidate_request,
            self.candidate_policy,
            candidate_record,
        )
        return (
            observation_input,
            observation_record,
            candidate_request,
            candidate_record,
            dependency_evidence,
            dependency_request,
            dependency_record,
        )

    def evidence(self, source, **overrides):
        values = dict(
            evidence_id="authority-evidence-001",
            subject_id=source[6].subject_id,
            subject_kind=source[6].subject_kind,
            subject_version=source[6].subject_version,
            captured_at_epoch_seconds=self.authority_evidence_at,
            authority_snapshot_digest=source[2].authority_snapshot_digest,
            authority_graph_snapshot_digest="h" * 64,
            responsible_authority_id="responsible-authority",
            active_authority_ids=("responsible-authority", "root-authority"),
            delegation_chain_ids=("root-authority", "responsible-authority"),
            protected_authority_ids=(),
            unresolved_authority_ids=(),
            cycle_member_ids=(),
            authority_closure_complete=True,
            delegation_chain_complete=True,
            responsibility_acknowledged=True,
            subject_controls_responsible_authority=False,
            institutional_hold=False,
            constitutional_protected=False,
            emergency_override_active=False,
        )
        values.update(overrides)
        return build_apoptosis_authority_evidence(**values)

    def request(self, source, evidence, **overrides):
        values = dict(
            review_id="authority-review-001",
            reviewer_id="authority-reviewer",
            reviewed_at_epoch_seconds=self.authority_reviewed_at,
            dependency_request=source[5],
            dependency_policy=self.dependency_policy,
            dependency_evidence=source[4],
            dependency_record=source[6],
            candidate_request=source[2],
            authority_evidence=evidence,
        )
        values.update(overrides)
        return build_apoptosis_authority_review_request(**values)

    def execute(self, source=None, evidence=None, request=None, policy=None):
        source = self.source() if source is None else source
        evidence = self.evidence(source) if evidence is None else evidence
        request = self.request(source, evidence) if request is None else request
        return review_apoptosis_authority(
            request,
            evidence,
            self.authority_policy if policy is None else policy,
            source[5],
            source[4],
            self.dependency_policy,
            source[6],
            source[0],
            self.observation_policy,
            source[1],
            source[2],
            self.candidate_policy,
            source[3],
        )

    def test_valid_authority_surface_is_clear_for_quiescence_review(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, AUTHORITY_REVIEW_CLEAR)
        self.assertTrue(record.authority_clear_for_quiescence_review)
        self.assertTrue(record.authority_review_record_issued)

    def test_institutional_and_constitutional_guards_block(self) -> None:
        for overrides, reason in (
            ({"institutional_hold": True}, "institutional_hold_present"),
            ({"constitutional_protected": True}, "constitutional_protection_present"),
        ):
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, AUTHORITY_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_closure_and_responsibility_guards_block(self) -> None:
        cases = (
            ({"authority_closure_complete": False}, "authority_closure_incomplete"),
            (
                {
                    "responsible_authority_id": "",
                    "active_authority_ids": ("root-authority",),
                    "delegation_chain_ids": ("root-authority",),
                },
                "responsible_authority_absent",
            ),
            ({"responsibility_acknowledged": False}, "responsibility_not_acknowledged"),
            (
                {"subject_controls_responsible_authority": True},
                "subject_controls_responsible_authority",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, AUTHORITY_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_delegation_protection_and_unresolved_guards_block(self) -> None:
        cases = (
            ({"delegation_chain_complete": False}, "delegation_chain_incomplete"),
            (
                {"protected_authority_ids": ("root-authority",)},
                "protected_authority_present",
            ),
            (
                {"unresolved_authority_ids": ("responsible-authority",)},
                "unresolved_authority_present",
            ),
            (
                {"cycle_member_ids": ("root-authority", "responsible-authority")},
                "authority_cycle_present",
            ),
            ({"emergency_override_active": True}, "emergency_override_active"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, AUTHORITY_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_non_clear_dependency_source_is_rejected(self) -> None:
        source = self.source(dependency_blocked=True)
        record = self.execute(source)
        self.assertEqual(record.status, AUTHORITY_REVIEW_REJECTED)
        self.assertFalse(record.source_dependency_clear)

    def test_reviewer_must_be_allowed_and_independent(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        for reviewer in (
            "unknown-reviewer",
            "dependency-reviewer",
            "lifecycle-reviewer",
            "responsible-authority",
            source[6].subject_id,
        ):
            with self.subTest(reviewer=reviewer):
                request = self.request(source, evidence, reviewer_id=reviewer)
                record = self.execute(source, evidence, request)
                self.assertEqual(record.status, AUTHORITY_REVIEW_REJECTED)

    def test_objective_and_time_guards_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        cases = (
            {"objective": "REVOKE_AUTHORITY_NOW"},
            {"reviewed_at_epoch_seconds": self.dependency_reviewed_at + 601},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                request = self.request(source, evidence, **overrides)
                self.assertEqual(
                    self.execute(source, evidence, request).status,
                    AUTHORITY_REVIEW_REJECTED,
                )

    def test_stale_evidence_is_rejected(self) -> None:
        source = self.source()
        evidence = self.evidence(
            source,
            captured_at_epoch_seconds=self.authority_reviewed_at - 301,
        )
        record = self.execute(source, evidence)
        self.assertEqual(record.status, AUTHORITY_REVIEW_REJECTED)
        self.assertFalse(record.evidence_fresh)

    def test_subject_and_snapshot_binding_tamper_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        request = self.request(source, evidence)
        subject_request = replace(request, subject_id="different-subject", request_digest="")
        subject_request = replace(
            subject_request,
            request_digest=apoptosis_authority_review_request_digest(subject_request),
        )
        snapshot_request = replace(
            request, authority_snapshot_digest="z" * 64, request_digest=""
        )
        snapshot_request = replace(
            snapshot_request,
            request_digest=apoptosis_authority_review_request_digest(snapshot_request),
        )
        self.assertEqual(
            self.execute(source, evidence, subject_request).status,
            AUTHORITY_REVIEW_REJECTED,
        )
        self.assertEqual(
            self.execute(source, evidence, snapshot_request).status,
            AUTHORITY_REVIEW_REJECTED,
        )

    def test_invalid_authority_subsets_are_rejected_by_builder(self) -> None:
        source = self.source()
        with self.assertRaises(ValueError):
            self.evidence(
                source,
                protected_authority_ids=("not-active",),
            )
        with self.assertRaises(ValueError):
            self.evidence(
                source,
                delegation_chain_ids=("root-authority", "root-authority"),
            )

    def test_effect_enabling_policy_is_rejected(self) -> None:
        unsafe = replace(
            self.authority_policy,
            allow_authority_revocation=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_authority_review_policy_digest(unsafe),
        )
        record = self.execute(policy=unsafe)
        self.assertEqual(record.status, AUTHORITY_REVIEW_REJECTED)
        self.assertFalse(record.authority_revocation_performed)

    def test_clear_requires_later_gates_but_blocked_does_not_advance(self) -> None:
        clear = self.execute()
        self.assertTrue(clear.quiescence_review_required_next)
        self.assertTrue(clear.external_review_required_next)
        self.assertTrue(clear.independent_authorization_required_next)
        source = self.source()
        blocked = self.execute(source, self.evidence(source, institutional_hold=True))
        self.assertFalse(blocked.quiescence_review_required_next)
        self.assertFalse(blocked.external_review_required_next)
        self.assertFalse(blocked.independent_authorization_required_next)

    def test_all_outcomes_are_read_only_and_deterministic(self) -> None:
        clear_left = self.execute()
        clear_right = self.execute()
        self.assertEqual(clear_left, clear_right)
        source = self.source()
        blocked = self.execute(source, self.evidence(source, institutional_hold=True))
        rejected = self.execute(self.source(dependency_blocked=True))
        for record in (clear_left, blocked, rejected):
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

    def test_record_tamper_is_detected(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        request = self.request(source, evidence)
        record = self.execute(source, evidence, request)
        tampered = replace(
            record,
            authority_revocation_performed=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_authority_review_record_digest(tampered),
        )
        issues = apoptosis_authority_review_record_issues(
            tampered,
            request,
            evidence,
            self.authority_policy,
            source[5],
            source[4],
            self.dependency_policy,
            source[6],
            source[0],
            self.observation_policy,
            source[1],
            source[2],
            self.candidate_policy,
            source[3],
        )
        self.assertIn("apoptosis_authority_review_recomputation_mismatch", issues)
        self.assertIn("apoptosis_authority_execution_effect_performed", issues)


if __name__ == "__main__":
    unittest.main()
