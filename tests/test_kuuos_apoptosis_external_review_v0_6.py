from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_external_review_types_v0_6 import (
    EXTERNAL_REVIEW_BLOCKED,
    EXTERNAL_REVIEW_CLEAR,
    EXTERNAL_REVIEW_REJECTED,
    apoptosis_external_review_evidence_digest,
    apoptosis_external_review_policy_digest,
    apoptosis_external_review_record_digest,
    apoptosis_external_review_request_digest,
)
from runtime.kuuos_apoptosis_external_review_v0_6 import (
    apoptosis_external_review_record_issues,
    build_apoptosis_external_review_evidence,
    build_apoptosis_external_review_policy,
    build_apoptosis_external_review_request,
    review_apoptosis_external,
)
from runtime.kuuos_apoptosis_quiescence_review_types_v0_5 import (
    apoptosis_quiescence_review_record_digest,
)
from tests.test_kuuos_apoptosis_quiescence_review_v0_5 import (
    ApoptosisQuiescenceReviewV05Tests,
)


class ApoptosisExternalReviewV06Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = ApoptosisQuiescenceReviewV05Tests(methodName="runTest")
        self.upstream.setUp()
        self.external_requested_at = self.upstream.quiescence_reviewed_at + 20
        self.external_evidence_at = self.external_requested_at + 20
        self.external_completed_at = self.external_requested_at + 40
        self.external_expiry_at = self.external_completed_at + 600
        self.external_policy = build_apoptosis_external_review_policy(
            "external-review-policy-v0-6",
            allowed_reviewer_ids=(
                "external-reviewer",
                "authority-reviewer",
                "candidate-module",
                "dependency-reviewer",
                "future-authorization-authority",
                "future-execution-authority",
                "lifecycle-reviewer",
                "quiescence-evidence-producer",
                "quiescence-reviewer",
                "responsible-authority",
            ),
            allowed_reviewer_organization_ids=(
                "external-review-organization",
            ),
            max_review_delay_seconds=300,
            max_evidence_age_seconds=300,
        )

    def source_bundle(
        self,
        *,
        authority_blocked: bool = False,
        quiescence_overrides: dict | None = None,
    ):
        source = self.upstream.source(authority_blocked=authority_blocked)
        quiescence_evidence = self.upstream.evidence(
            source,
            **(quiescence_overrides or {}),
        )
        quiescence_request = self.upstream.request(source, quiescence_evidence)
        quiescence_record = self.upstream.execute(
            source,
            quiescence_evidence,
            quiescence_request,
        )
        return source, quiescence_evidence, quiescence_request, quiescence_record

    def evidence(self, bundle, **overrides):
        source, quiescence_evidence, quiescence_request, quiescence_record = bundle
        values = dict(
            evidence_id="external-evidence-001",
            external_review_id="external-review-001",
            external_reviewer_id="external-reviewer",
            external_reviewer_organization_id="external-review-organization",
            quiescence_evidence_producer_id="quiescence-evidence-producer",
            reviewer_qualification_receipt_digest="q" * 64,
            reviewer_qualification_verified=True,
            reviewer_independence_declaration_digest="j" * 64,
            reviewer_independence_declared=True,
            conflict_of_interest_disclosure_digest="f" * 64,
            conflict_disclosure_complete=True,
            material_conflict_present=False,
            institutional_affiliation_digest="i" * 64,
            review_scope="full lifecycle-governance external review",
            review_scope_complete=True,
            review_methodology_digest="m" * 64,
            review_evidence_receipt_digest="v" * 64,
            review_evidence_receipt_complete=True,
            review_requested_at_epoch_seconds=self.external_requested_at,
            captured_at_epoch_seconds=self.external_evidence_at,
            review_completed_at_epoch_seconds=self.external_completed_at,
            review_expiry_at_epoch_seconds=self.external_expiry_at,
            appeal_route_digest="a" * 64,
            appeal_route_available=True,
            dissent_route_digest="d" * 64,
            dissent_route_available=True,
            minority_opinion_receipt_digest="n" * 64,
            protected_core_excluded=True,
            institutional_hold_active=False,
            emergency_state_active=False,
            quiescence_request=quiescence_request,
            quiescence_evidence=quiescence_evidence,
            quiescence_policy=self.upstream.quiescence_policy,
            quiescence_record=quiescence_record,
            authority_request=source[8],
            authority_evidence=source[7],
            authority_policy=self.upstream.authority_policy,
            authority_record=source[9],
            dependency_request=source[5],
            dependency_evidence=source[4],
            dependency_policy=self.upstream.dependency_policy,
            dependency_record=source[6],
            observation_input=source[0],
            observation_policy=self.upstream.observation_policy,
            observation_record=source[1],
            candidate_request=source[2],
            candidate_policy=self.upstream.candidate_policy,
            candidate_record=source[3],
        )
        values.update(overrides)
        return build_apoptosis_external_review_evidence(**values)

    def request(self, bundle, evidence, **overrides):
        values = dict(
            review_id="external-review-001",
            reviewer_id="external-reviewer",
            reviewer_organization_id="external-review-organization",
            requested_at_epoch_seconds=self.external_requested_at,
            completed_at_epoch_seconds=self.external_completed_at,
            quiescence_record=bundle[3],
            external_evidence=evidence,
            future_authorization_authority_id=(
                "future-authorization-authority"
            ),
            future_execution_authority_id="future-execution-authority",
        )
        values.update(overrides)
        return build_apoptosis_external_review_request(**values)

    def execute(self, bundle=None, evidence=None, request=None, policy=None):
        bundle = self.source_bundle() if bundle is None else bundle
        evidence = self.evidence(bundle) if evidence is None else evidence
        request = self.request(bundle, evidence) if request is None else request
        source, quiescence_evidence, quiescence_request, quiescence_record = bundle
        return review_apoptosis_external(
            request,
            evidence,
            self.external_policy if policy is None else policy,
            quiescence_request,
            quiescence_evidence,
            self.upstream.quiescence_policy,
            quiescence_record,
            source[8],
            source[7],
            self.upstream.authority_policy,
            source[9],
            source[5],
            source[4],
            self.upstream.dependency_policy,
            source[6],
            source[0],
            self.upstream.observation_policy,
            source[1],
            source[2],
            self.upstream.candidate_policy,
            source[3],
        )

    def record_issues(self, bundle, evidence, request, record, policy=None):
        source, quiescence_evidence, quiescence_request, quiescence_record = bundle
        return apoptosis_external_review_record_issues(
            record,
            request,
            evidence,
            self.external_policy if policy is None else policy,
            quiescence_request,
            quiescence_evidence,
            self.upstream.quiescence_policy,
            quiescence_record,
            source[8],
            source[7],
            self.upstream.authority_policy,
            source[9],
            source[5],
            source[4],
            self.upstream.dependency_policy,
            source[6],
            source[0],
            self.upstream.observation_policy,
            source[1],
            source[2],
            self.upstream.candidate_policy,
            source[3],
        )

    def test_valid_surface_is_clear_for_independent_authorization(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, EXTERNAL_REVIEW_CLEAR)
        self.assertTrue(record.external_clear_for_independent_authorization)
        self.assertTrue(record.independent_authorization_required_next)
        self.assertFalse(record.authorization_request_issued)
        self.assertFalse(record.authorization_decision_made)

    def test_non_clear_quiescence_sources_are_rejected(self) -> None:
        blocked = self.source_bundle(
            quiescence_overrides={"active_execution_ids": ("execution-1",)}
        )
        rejected = self.source_bundle(authority_blocked=True)
        for bundle in (blocked, rejected):
            with self.subTest(status=bundle[3].status):
                record = self.execute(bundle)
                self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)
                self.assertFalse(record.source_quiescence_clear)

    def test_tampered_quiescence_record_is_rejected_after_fresh_digest(self) -> None:
        bundle = self.source_bundle()
        tampered = replace(
            bundle[3],
            quiescence_transition_performed=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_quiescence_review_record_digest(tampered),
        )
        tampered_bundle = bundle[:3] + (tampered,)
        evidence = self.evidence(tampered_bundle)
        request = self.request(tampered_bundle, evidence)
        record = self.execute(tampered_bundle, evidence, request)
        self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_reviewer_allowlist_organization_and_objective_are_enforced(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(bundle)
        cases = (
            {"reviewer_id": "unknown-reviewer"},
            {"reviewer_organization_id": "unknown-organization"},
            {"objective": "AUTHORIZE_TERMINATION_NOW"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                request = self.request(bundle, evidence, **overrides)
                record = self.execute(bundle, evidence, request)
                self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)

    def test_reviewer_is_independent_from_prior_chain(self) -> None:
        bundle = self.source_bundle()
        prior_ids = (
            "candidate-module",
            "lifecycle-reviewer",
            "dependency-reviewer",
            "authority-reviewer",
            "responsible-authority",
            "quiescence-reviewer",
            "quiescence-evidence-producer",
        )
        for reviewer_id in prior_ids:
            with self.subTest(reviewer_id=reviewer_id):
                evidence = self.evidence(
                    bundle,
                    external_reviewer_id=reviewer_id,
                )
                request = self.request(
                    bundle,
                    evidence,
                    reviewer_id=reviewer_id,
                )
                record = self.execute(bundle, evidence, request)
                self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)
                self.assertFalse(record.reviewer_independent)

    def test_reviewer_is_separate_from_future_authorities(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(bundle)
        cases = (
            {"future_authorization_authority_id": "external-reviewer"},
            {"future_execution_authority_id": "external-reviewer"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                request = self.request(bundle, evidence, **overrides)
                record = self.execute(bundle, evidence, request)
                self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)
                self.assertFalse(record.reviewer_independent)

    def test_qualification_and_independence_declaration_block(self) -> None:
        bundle = self.source_bundle()
        cases = (
            (
                {"reviewer_qualification_verified": False},
                "reviewer_qualification_not_verified",
            ),
            (
                {"reviewer_independence_declared": False},
                "reviewer_independence_not_declared",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, EXTERNAL_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_conflict_disclosure_and_material_conflict_block(self) -> None:
        bundle = self.source_bundle()
        cases = (
            (
                {
                    "conflict_of_interest_disclosure_digest": "",
                    "conflict_disclosure_complete": False,
                },
                "conflict_disclosure_incomplete",
            ),
            (
                {"material_conflict_present": True},
                "material_conflict_present",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, EXTERNAL_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_scope_methodology_and_evidence_receipt_block(self) -> None:
        bundle = self.source_bundle()
        cases = (
            ({"review_scope_complete": False}, "review_scope_incomplete"),
            ({"review_methodology_digest": ""}, "review_methodology_missing"),
            (
                {"review_evidence_receipt_complete": False},
                "review_evidence_receipt_incomplete",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, EXTERNAL_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_appeal_and_dissent_routes_block_when_missing(self) -> None:
        bundle = self.source_bundle()
        cases = (
            ({"appeal_route_available": False}, "appeal_route_missing"),
            ({"dissent_route_available": False}, "dissent_route_missing"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, EXTERNAL_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_protected_core_hold_and_emergency_states_block(self) -> None:
        bundle = self.source_bundle()
        cases = (
            ({"protected_core_excluded": False}, "protected_core_not_excluded"),
            ({"institutional_hold_active": True}, "institutional_hold_active"),
            ({"emergency_state_active": True}, "emergency_state_active"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, EXTERNAL_REVIEW_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_expiry_staleness_and_delay_are_rejected(self) -> None:
        bundle = self.source_bundle()
        expired = self.evidence(
            bundle,
            review_expiry_at_epoch_seconds=self.external_completed_at - 1,
        )
        stale = self.evidence(
            bundle,
            captured_at_epoch_seconds=self.external_completed_at - 301,
        )
        late_evidence = self.evidence(
            bundle,
            review_requested_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 301
            ),
            captured_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 302
            ),
            review_completed_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 303
            ),
            review_expiry_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 900
            ),
        )
        late_request = self.request(
            bundle,
            late_evidence,
            requested_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 301
            ),
            completed_at_epoch_seconds=(
                self.upstream.quiescence_reviewed_at + 303
            ),
        )
        cases = (
            (expired, self.request(bundle, expired)),
            (stale, self.request(bundle, stale)),
            (late_evidence, late_request),
        )
        for evidence, request in cases:
            with self.subTest(evidence=evidence.evidence_id):
                record = self.execute(bundle, evidence, request)
                self.assertEqual(record.status, EXTERNAL_REVIEW_REJECTED)

    def test_subject_and_source_artifact_binding_tamper_reject(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(bundle)
        request = self.request(bundle, evidence)
        subject_request = replace(
            request,
            subject_id="different-subject",
            request_digest="",
        )
        subject_request = replace(
            subject_request,
            request_digest=apoptosis_external_review_request_digest(
                subject_request
            ),
        )
        tampered_evidence = replace(
            evidence,
            source_candidate_record_digest="z" * 64,
            evidence_digest="",
        )
        tampered_evidence = replace(
            tampered_evidence,
            evidence_digest=apoptosis_external_review_evidence_digest(
                tampered_evidence
            ),
        )
        tampered_request = self.request(bundle, tampered_evidence)
        self.assertEqual(
            self.execute(bundle, evidence, subject_request).status,
            EXTERNAL_REVIEW_REJECTED,
        )
        self.assertEqual(
            self.execute(bundle, tampered_evidence, tampered_request).status,
            EXTERNAL_REVIEW_REJECTED,
        )

    def test_unsafe_policy_rejects_and_blocked_does_not_advance(self) -> None:
        unsafe = replace(
            self.external_policy,
            allow_authorization_request=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_external_review_policy_digest(unsafe),
        )
        rejected = self.execute(policy=unsafe)
        self.assertEqual(rejected.status, EXTERNAL_REVIEW_REJECTED)
        self.assertFalse(rejected.authorization_request_issued)
        bundle = self.source_bundle()
        blocked = self.execute(
            bundle,
            self.evidence(bundle, reviewer_qualification_verified=False),
        )
        self.assertFalse(blocked.independent_authorization_required_next)
        self.assertFalse(blocked.external_clear_for_independent_authorization)

    def test_all_outcomes_are_read_only_deterministic_and_tamper_evident(self) -> None:
        clear_left = self.execute()
        clear_right = self.execute()
        self.assertEqual(clear_left, clear_right)
        bundle = self.source_bundle()
        blocked = self.execute(
            bundle,
            self.evidence(bundle, reviewer_qualification_verified=False),
        )
        rejected_bundle = self.source_bundle(authority_blocked=True)
        rejected = self.execute(rejected_bundle)
        for record in (clear_left, blocked, rejected):
            self.assertFalse(record.authorization_request_issued)
            self.assertFalse(record.authorization_decision_made)
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

        evidence = self.evidence(bundle)
        request = self.request(bundle, evidence)
        record = self.execute(bundle, evidence, request)
        tampered = replace(
            record,
            authorization_decision_made=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_external_review_record_digest(tampered),
        )
        issues = self.record_issues(bundle, evidence, request, tampered)
        self.assertIn("apoptosis_external_review_recomputation_mismatch", issues)
        self.assertIn("apoptosis_external_review_execution_effect_performed", issues)


if __name__ == "__main__":
    unittest.main()
