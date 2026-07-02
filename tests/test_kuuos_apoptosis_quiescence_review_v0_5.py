from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_authority_review_types_v0_4 import (
    apoptosis_authority_review_record_digest,
)
from runtime.kuuos_apoptosis_authority_review_v0_4 import (
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
from runtime.kuuos_apoptosis_quiescence_review_types_v0_5 import (
    QUIESCENCE_REVIEW_BLOCKED,
    QUIESCENCE_REVIEW_CLEAR,
    QUIESCENCE_REVIEW_REJECTED,
    apoptosis_quiescence_review_policy_digest,
    apoptosis_quiescence_review_record_digest,
    apoptosis_quiescence_review_request_digest,
)
from runtime.kuuos_apoptosis_quiescence_review_v0_5 import (
    apoptosis_quiescence_review_record_issues,
    build_apoptosis_quiescence_evidence,
    build_apoptosis_quiescence_review_policy,
    build_apoptosis_quiescence_review_request,
    review_apoptosis_quiescence,
)


class ApoptosisQuiescenceReviewV05Tests(unittest.TestCase):
    observed_at = 1_900_000_000
    candidate_at = observed_at + 30
    dependency_evidence_at = candidate_at + 10
    dependency_reviewed_at = candidate_at + 30
    authority_evidence_at = dependency_reviewed_at + 10
    authority_reviewed_at = dependency_reviewed_at + 30
    quiescence_started_at = authority_reviewed_at + 10
    last_activity_at = authority_reviewed_at + 5
    quiescence_evidence_at = authority_reviewed_at + 310
    quiescence_reviewed_at = authority_reviewed_at + 330

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
            allowed_reviewer_ids=("authority-reviewer",),
            max_review_delay_seconds=600,
            max_evidence_age_seconds=300,
        )
        self.quiescence_policy = build_apoptosis_quiescence_review_policy(
            "quiescence-review-policy-v0-5",
            allowed_reviewer_ids=(
                "quiescence-reviewer",
                "authority-reviewer",
                "dependency-reviewer",
                "lifecycle-reviewer",
                "responsible-authority",
                "candidate-module",
            ),
            max_review_delay_seconds=600,
            max_evidence_age_seconds=300,
            minimum_grace_period_seconds=300,
        )

    def source(self, *, authority_blocked: bool = False):
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
        dependency_evidence = build_apoptosis_dependency_evidence(
            "dependency-evidence-001",
            candidate_record.subject_id,
            candidate_record.subject_kind,
            candidate_record.subject_version,
            captured_at_epoch_seconds=self.dependency_evidence_at,
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
        authority_evidence = build_apoptosis_authority_evidence(
            "authority-evidence-001",
            dependency_record.subject_id,
            dependency_record.subject_kind,
            dependency_record.subject_version,
            captured_at_epoch_seconds=self.authority_evidence_at,
            authority_snapshot_digest=candidate_request.authority_snapshot_digest,
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
            institutional_hold=authority_blocked,
            constitutional_protected=False,
            emergency_override_active=False,
        )
        authority_request = build_apoptosis_authority_review_request(
            "authority-review-001",
            "authority-reviewer",
            self.authority_reviewed_at,
            dependency_request,
            self.dependency_policy,
            dependency_evidence,
            dependency_record,
            candidate_request,
            authority_evidence,
        )
        authority_record = review_apoptosis_authority(
            authority_request,
            authority_evidence,
            self.authority_policy,
            dependency_request,
            dependency_evidence,
            self.dependency_policy,
            dependency_record,
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
            authority_evidence,
            authority_request,
            authority_record,
        )

    def evidence(self, source, **overrides):
        values = dict(
            evidence_id="quiescence-evidence-001",
            subject_id=source[9].subject_id,
            subject_kind=source[9].subject_kind,
            subject_version=source[9].subject_version,
            captured_at_epoch_seconds=self.quiescence_evidence_at,
            execution_snapshot_digest="e" * 64,
            work_snapshot_digest="w" * 64,
            intake_snapshot_digest="i" * 64,
            state_checkpoint_digest="c" * 64,
            drain_plan_digest="n" * 64,
            recovery_route_digest="y" * 64,
            active_execution_ids=(),
            pending_work_ids=(),
            critical_pending_work_ids=(),
            active_lease_ids=(),
            intake_channel_ids=("primary-intake",),
            open_intake_channel_ids=(),
            blocking_external_dependency_ids=(),
            quiescence_closure_complete=True,
            new_intake_stopped=True,
            drain_verified=True,
            checkpoint_verified=True,
            recovery_route_verified=True,
            reentry_possible=True,
            quiescence_started_at_epoch_seconds=self.quiescence_started_at,
            last_activity_at_epoch_seconds=self.last_activity_at,
            emergency_operation_active=False,
        )
        values.update(overrides)
        return build_apoptosis_quiescence_evidence(**values)

    def request(self, source, evidence, **overrides):
        values = dict(
            review_id="quiescence-review-001",
            reviewer_id="quiescence-reviewer",
            reviewed_at_epoch_seconds=self.quiescence_reviewed_at,
            authority_request=source[8],
            authority_policy=self.authority_policy,
            authority_evidence=source[7],
            authority_record=source[9],
            quiescence_evidence=evidence,
        )
        values.update(overrides)
        return build_apoptosis_quiescence_review_request(**values)

    def execute(self, source=None, evidence=None, request=None, policy=None):
        source = self.source() if source is None else source
        evidence = self.evidence(source) if evidence is None else evidence
        request = self.request(source, evidence) if request is None else request
        return review_apoptosis_quiescence(
            request,
            evidence,
            self.quiescence_policy if policy is None else policy,
            source[8],
            source[7],
            self.authority_policy,
            source[9],
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

    def test_valid_surface_is_clear_for_external_review(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, QUIESCENCE_REVIEW_CLEAR)
        self.assertTrue(record.quiescence_clear_for_external_review)
        self.assertTrue(record.quiescence_review_record_issued)

    def test_execution_and_work_surfaces_block(self) -> None:
        cases = (
            ({"active_execution_ids": ("execution-1",)}, "active_execution_present"),
            (
                {
                    "pending_work_ids": ("critical-work",),
                    "critical_pending_work_ids": ("critical-work",),
                },
                "critical_pending_work_present",
            ),
            ({"pending_work_ids": ("work-1",)}, "pending_work_present"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, QUIESCENCE_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_lease_intake_and_external_dependency_surfaces_block(self) -> None:
        cases = (
            ({"active_lease_ids": ("lease-1",)}, "active_lease_present"),
            ({"new_intake_stopped": False}, "new_intake_not_stopped"),
            (
                {"open_intake_channel_ids": ("primary-intake",)},
                "open_intake_channel_present",
            ),
            (
                {"blocking_external_dependency_ids": ("external-service",)},
                "blocking_external_dependency_present",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, QUIESCENCE_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_drain_checkpoint_recovery_and_reentry_guards_block(self) -> None:
        cases = (
            ({"drain_verified": False}, "drain_not_verified"),
            ({"checkpoint_verified": False}, "checkpoint_not_verified"),
            ({"recovery_route_verified": False}, "recovery_route_not_verified"),
            ({"reentry_possible": False}, "reentry_not_possible"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, QUIESCENCE_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_closure_emergency_and_time_guards_block(self) -> None:
        cases = (
            ({"quiescence_closure_complete": False}, "quiescence_closure_incomplete"),
            ({"emergency_operation_active": True}, "emergency_operation_active"),
            (
                {
                    "quiescence_started_at_epoch_seconds": self.authority_reviewed_at - 1,
                    "last_activity_at_epoch_seconds": self.authority_reviewed_at - 2,
                },
                "quiescence_time_order_invalid",
            ),
            (
                {
                    "quiescence_started_at_epoch_seconds": self.quiescence_reviewed_at - 299,
                    "last_activity_at_epoch_seconds": self.quiescence_reviewed_at - 300,
                },
                "grace_period_not_elapsed",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                source = self.source()
                record = self.execute(source, self.evidence(source, **overrides))
                self.assertEqual(record.status, QUIESCENCE_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_non_clear_authority_source_is_rejected(self) -> None:
        source = self.source(authority_blocked=True)
        record = self.execute(source)
        self.assertEqual(record.status, QUIESCENCE_REVIEW_REJECTED)
        self.assertFalse(record.source_authority_clear)

    def test_tampered_authority_source_is_rejected_after_fresh_digest(self) -> None:
        source = self.source()
        authority_record = replace(
            source[9],
            quiescence_transition_performed=True,
            record_digest="",
        )
        authority_record = replace(
            authority_record,
            record_digest=apoptosis_authority_review_record_digest(
                authority_record
            ),
        )
        tampered_source = source[:9] + (authority_record,)
        evidence = self.evidence(tampered_source)
        request = self.request(tampered_source, evidence)
        record = self.execute(tampered_source, evidence, request)
        self.assertEqual(record.status, QUIESCENCE_REVIEW_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_reviewer_must_be_allowed_and_independent(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        for reviewer in (
            "unknown-reviewer",
            "authority-reviewer",
            "dependency-reviewer",
            "lifecycle-reviewer",
            "responsible-authority",
            "candidate-module",
        ):
            with self.subTest(reviewer=reviewer):
                request = self.request(source, evidence, reviewer_id=reviewer)
                record = self.execute(source, evidence, request)
                self.assertEqual(record.status, QUIESCENCE_REVIEW_REJECTED)

    def test_objective_delay_and_stale_evidence_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        bad_objective = self.request(
            source,
            evidence,
            objective="ENTER_QUIESCENCE_NOW",
        )
        self.assertEqual(
            self.execute(source, evidence, bad_objective).status,
            QUIESCENCE_REVIEW_REJECTED,
        )
        late_request = self.request(
            source,
            evidence,
            reviewed_at_epoch_seconds=self.authority_reviewed_at + 601,
        )
        self.assertEqual(
            self.execute(source, evidence, late_request).status,
            QUIESCENCE_REVIEW_REJECTED,
        )
        stale_evidence = self.evidence(
            source,
            captured_at_epoch_seconds=self.quiescence_reviewed_at - 301,
        )
        stale_record = self.execute(source, stale_evidence)
        self.assertEqual(stale_record.status, QUIESCENCE_REVIEW_REJECTED)
        self.assertFalse(stale_record.evidence_fresh)

    def test_subject_and_snapshot_binding_tamper_reject(self) -> None:
        source = self.source()
        evidence = self.evidence(source)
        request = self.request(source, evidence)
        subject_request = replace(
            request,
            subject_id="different-subject",
            request_digest="",
        )
        subject_request = replace(
            subject_request,
            request_digest=apoptosis_quiescence_review_request_digest(
                subject_request
            ),
        )
        snapshot_request = replace(
            request,
            execution_snapshot_digest="z" * 64,
            request_digest="",
        )
        snapshot_request = replace(
            snapshot_request,
            request_digest=apoptosis_quiescence_review_request_digest(
                snapshot_request
            ),
        )
        self.assertEqual(
            self.execute(source, evidence, subject_request).status,
            QUIESCENCE_REVIEW_REJECTED,
        )
        self.assertEqual(
            self.execute(source, evidence, snapshot_request).status,
            QUIESCENCE_REVIEW_REJECTED,
        )

    def test_invalid_evidence_subsets_are_rejected_by_builder(self) -> None:
        source = self.source()
        with self.assertRaises(ValueError):
            self.evidence(
                source,
                critical_pending_work_ids=("not-pending",),
            )
        with self.assertRaises(ValueError):
            self.evidence(
                source,
                open_intake_channel_ids=("undeclared-intake",),
            )

    def test_effect_enabling_policy_is_rejected(self) -> None:
        unsafe = replace(
            self.quiescence_policy,
            allow_quiescence_transition=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_quiescence_review_policy_digest(unsafe),
        )
        record = self.execute(policy=unsafe)
        self.assertEqual(record.status, QUIESCENCE_REVIEW_REJECTED)
        self.assertFalse(record.quiescence_transition_performed)

    def test_clear_requires_later_gates_but_blocked_does_not_advance(self) -> None:
        clear = self.execute()
        self.assertTrue(clear.external_review_required_next)
        self.assertTrue(clear.independent_authorization_required_next)
        source = self.source()
        blocked = self.execute(
            source,
            self.evidence(source, active_execution_ids=("execution-1",)),
        )
        self.assertFalse(blocked.external_review_required_next)
        self.assertFalse(blocked.independent_authorization_required_next)

    def test_all_outcomes_are_read_only_and_deterministic(self) -> None:
        clear_left = self.execute()
        clear_right = self.execute()
        self.assertEqual(clear_left, clear_right)
        source = self.source()
        blocked = self.execute(
            source,
            self.evidence(source, active_execution_ids=("execution-1",)),
        )
        rejected = self.execute(self.source(authority_blocked=True))
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
            quiescence_transition_performed=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_quiescence_review_record_digest(tampered),
        )
        issues = apoptosis_quiescence_review_record_issues(
            tampered,
            request,
            evidence,
            self.quiescence_policy,
            source[8],
            source[7],
            self.authority_policy,
            source[9],
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
        self.assertIn("apoptosis_quiescence_review_recomputation_mismatch", issues)
        self.assertIn("apoptosis_quiescence_execution_effect_performed", issues)


if __name__ == "__main__":
    unittest.main()
