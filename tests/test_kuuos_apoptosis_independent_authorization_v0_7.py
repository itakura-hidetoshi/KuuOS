from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_external_review_types_v0_6 import (
    apoptosis_external_review_record_digest,
)
from runtime.kuuos_apoptosis_independent_authorization_types_v0_7 import (
    INDEPENDENT_AUTHORIZATION_APPROVED,
    INDEPENDENT_AUTHORIZATION_DENIED,
    INDEPENDENT_AUTHORIZATION_REJECTED,
    apoptosis_independent_authorization_evidence_digest,
    apoptosis_independent_authorization_policy_digest,
    apoptosis_independent_authorization_record_digest,
    apoptosis_independent_authorization_request_digest,
)
from runtime.kuuos_apoptosis_independent_authorization_v0_7 import (
    apoptosis_independent_authorization_record_issues,
    authorize_apoptosis_independently,
    build_apoptosis_independent_authorization_evidence,
    build_apoptosis_independent_authorization_policy,
    build_apoptosis_independent_authorization_request,
)
from tests.test_kuuos_apoptosis_external_review_v0_6 import (
    ApoptosisExternalReviewV06Tests,
)


class ApoptosisIndependentAuthorizationV07Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = ApoptosisExternalReviewV06Tests(methodName="runTest")
        self.upstream.setUp()
        self.authorization_requested_at = self.upstream.external_completed_at + 20
        self.authorization_evidence_at = self.authorization_requested_at + 20
        self.authorization_completed_at = self.authorization_requested_at + 40
        self.authorization_expiry_at = self.authorization_completed_at + 600
        self.authorization_policy = (
            build_apoptosis_independent_authorization_policy(
                "independent-authorization-policy-v0-7",
                allowed_authority_ids=(
                    "future-authorization-authority",
                    "candidate-module",
                    "dependency-reviewer",
                    "authority-reviewer",
                    "responsible-authority",
                    "quiescence-reviewer",
                    "quiescence-evidence-producer",
                    "external-reviewer",
                    "future-execution-authority",
                ),
                allowed_authority_organization_ids=(
                    "independent-authorization-organization",
                ),
                max_authorization_delay_seconds=300,
                max_evidence_age_seconds=300,
            )
        )

    def source_bundle(
        self,
        *,
        external_overrides: dict | None = None,
        authority_blocked: bool = False,
    ):
        quiescence_bundle = self.upstream.source_bundle(
            authority_blocked=authority_blocked
        )
        external_evidence = self.upstream.evidence(
            quiescence_bundle,
            **(external_overrides or {}),
        )
        external_request = self.upstream.request(
            quiescence_bundle,
            external_evidence,
        )
        external_record = self.upstream.execute(
            quiescence_bundle,
            external_evidence,
            external_request,
        )
        return (
            quiescence_bundle,
            external_evidence,
            external_request,
            external_record,
        )

    def evidence(self, bundle, **overrides):
        quiescence_bundle, external_evidence, external_request, external_record = (
            bundle
        )
        source, quiescence_evidence, quiescence_request, quiescence_record = (
            quiescence_bundle
        )
        values = dict(
            evidence_id="independent-authorization-evidence-001",
            authorization_id="independent-authorization-001",
            authorization_authority_id="future-authorization-authority",
            authorization_authority_organization_id=(
                "independent-authorization-organization"
            ),
            external_reviewer_id=external_record.reviewer_id,
            authority_mandate_receipt_digest="m" * 64,
            authority_mandate_verified=True,
            authority_qualification_receipt_digest="q" * 64,
            authority_qualification_verified=True,
            authority_independence_declaration_digest="i" * 64,
            authority_independence_declared=True,
            conflict_of_interest_disclosure_digest="c" * 64,
            conflict_disclosure_complete=True,
            material_conflict_present=False,
            jurisdiction_receipt_digest="j" * 64,
            jurisdiction_verified=True,
            quorum_receipt_digest="u" * 64,
            quorum_satisfied=True,
            decision_rationale_digest="r" * 64,
            reasoned_decision_complete=True,
            proportionality_review_digest="p" * 64,
            proportionality_satisfied=True,
            alternatives_review_digest="a" * 64,
            less_restrictive_alternatives_exhausted=True,
            irreversibility_review_digest="v" * 64,
            irreversibility_review_complete=True,
            human_impact_review_digest="h" * 64,
            human_impact_review_complete=True,
            authorization_requested_at_epoch_seconds=(
                self.authorization_requested_at
            ),
            captured_at_epoch_seconds=self.authorization_evidence_at,
            authorization_completed_at_epoch_seconds=(
                self.authorization_completed_at
            ),
            authorization_expiry_at_epoch_seconds=(
                self.authorization_expiry_at
            ),
            appeal_route_digest="e" * 64,
            appeal_route_available=True,
            dissent_route_digest="d" * 64,
            dissent_route_available=True,
            minority_opinion_receipt_digest="n" * 64,
            protected_core_excluded=True,
            institutional_hold_active=False,
            emergency_state_active=False,
            external_request=external_request,
            external_evidence=external_evidence,
            external_policy=self.upstream.external_policy,
            external_record=external_record,
            quiescence_request=quiescence_request,
            quiescence_evidence=quiescence_evidence,
            quiescence_policy=self.upstream.upstream.quiescence_policy,
            quiescence_record=quiescence_record,
            authority_request=source[8],
            authority_evidence=source[7],
            authority_policy=self.upstream.upstream.authority_policy,
            authority_record=source[9],
            dependency_request=source[5],
            dependency_evidence=source[4],
            dependency_policy=self.upstream.upstream.dependency_policy,
            dependency_record=source[6],
            observation_input=source[0],
            observation_policy=self.upstream.upstream.observation_policy,
            observation_record=source[1],
            candidate_request=source[2],
            candidate_policy=self.upstream.upstream.candidate_policy,
            candidate_record=source[3],
        )
        values.update(overrides)
        return build_apoptosis_independent_authorization_evidence(**values)

    def request(self, bundle, evidence, **overrides):
        values = dict(
            authorization_id="independent-authorization-001",
            authority_id="future-authorization-authority",
            authority_organization_id=(
                "independent-authorization-organization"
            ),
            requested_at_epoch_seconds=self.authorization_requested_at,
            completed_at_epoch_seconds=self.authorization_completed_at,
            external_record=bundle[3],
            authorization_evidence=evidence,
            future_execution_authority_id="future-execution-authority",
        )
        values.update(overrides)
        return build_apoptosis_independent_authorization_request(**values)

    def execute(self, bundle=None, evidence=None, request=None, policy=None):
        bundle = self.source_bundle() if bundle is None else bundle
        evidence = self.evidence(bundle) if evidence is None else evidence
        request = self.request(bundle, evidence) if request is None else request
        quiescence_bundle, external_evidence, external_request, external_record = (
            bundle
        )
        source, quiescence_evidence, quiescence_request, quiescence_record = (
            quiescence_bundle
        )
        return authorize_apoptosis_independently(
            request,
            evidence,
            self.authorization_policy if policy is None else policy,
            external_request,
            external_evidence,
            self.upstream.external_policy,
            external_record,
            quiescence_request,
            quiescence_evidence,
            self.upstream.upstream.quiescence_policy,
            quiescence_record,
            source[8],
            source[7],
            self.upstream.upstream.authority_policy,
            source[9],
            source[5],
            source[4],
            self.upstream.upstream.dependency_policy,
            source[6],
            source[0],
            self.upstream.upstream.observation_policy,
            source[1],
            source[2],
            self.upstream.upstream.candidate_policy,
            source[3],
        )

    def record_issues(self, bundle, evidence, request, record, policy=None):
        quiescence_bundle, external_evidence, external_request, external_record = (
            bundle
        )
        source, quiescence_evidence, quiescence_request, quiescence_record = (
            quiescence_bundle
        )
        return apoptosis_independent_authorization_record_issues(
            record,
            request,
            evidence,
            self.authorization_policy if policy is None else policy,
            external_request,
            external_evidence,
            self.upstream.external_policy,
            external_record,
            quiescence_request,
            quiescence_evidence,
            self.upstream.upstream.quiescence_policy,
            quiescence_record,
            source[8],
            source[7],
            self.upstream.upstream.authority_policy,
            source[9],
            source[5],
            source[4],
            self.upstream.upstream.dependency_policy,
            source[6],
            source[0],
            self.upstream.upstream.observation_policy,
            source[1],
            source[2],
            self.upstream.upstream.candidate_policy,
            source[3],
        )

    def test_valid_surface_is_approved_for_bounded_preparation(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_APPROVED)
        self.assertTrue(record.authorization_record_issued)
        self.assertTrue(record.authorization_decision_made)
        self.assertTrue(record.authorization_approved)
        self.assertTrue(record.bounded_execution_preparation_allowed_next)
        self.assertFalse(record.execution_request_issued)
        self.assertFalse(record.execution_decision_made)

    def test_non_clear_external_sources_are_rejected(self) -> None:
        blocked = self.source_bundle(
            external_overrides={"reviewer_qualification_verified": False}
        )
        rejected = self.source_bundle(authority_blocked=True)
        for bundle in (blocked, rejected):
            with self.subTest(status=bundle[3].status):
                record = self.execute(bundle)
                self.assertEqual(
                    record.status,
                    INDEPENDENT_AUTHORIZATION_REJECTED,
                )
                self.assertFalse(record.source_external_review_clear)

    def test_tampered_external_record_is_rejected_after_fresh_digest(self) -> None:
        bundle = self.source_bundle()
        tampered = replace(
            bundle[3],
            authorization_decision_made=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_external_review_record_digest(tampered),
        )
        tampered_bundle = bundle[:3] + (tampered,)
        evidence = self.evidence(tampered_bundle)
        request = self.request(tampered_bundle, evidence)
        record = self.execute(tampered_bundle, evidence, request)
        self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_allowlists_and_objective_are_enforced(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(bundle)
        cases = (
            {"authority_id": "unknown-authority"},
            {"authority_organization_id": "unknown-organization"},
            {"objective": "EXECUTE_TERMINATION_NOW"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                request = self.request(bundle, evidence, **overrides)
                record = self.execute(bundle, evidence, request)
                self.assertEqual(
                    record.status,
                    INDEPENDENT_AUTHORIZATION_REJECTED,
                )

    def test_external_designated_authority_binding_is_enforced(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(
            bundle,
            authorization_authority_id="authority-reviewer",
        )
        request = self.request(
            bundle,
            evidence,
            authority_id="authority-reviewer",
        )
        record = self.execute(bundle, evidence, request)
        self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_REJECTED)
        self.assertFalse(record.external_authority_designation_binding_valid)

    def test_authority_is_independent_from_prior_chain(self) -> None:
        bundle = self.source_bundle()
        prior_ids = (
            "candidate-module",
            "dependency-reviewer",
            "authority-reviewer",
            "responsible-authority",
            "quiescence-reviewer",
            "quiescence-evidence-producer",
            "external-reviewer",
        )
        for authority_id in prior_ids:
            with self.subTest(authority_id=authority_id):
                evidence = self.evidence(
                    bundle,
                    authorization_authority_id=authority_id,
                )
                request = self.request(
                    bundle,
                    evidence,
                    authority_id=authority_id,
                )
                record = self.execute(bundle, evidence, request)
                self.assertEqual(
                    record.status,
                    INDEPENDENT_AUTHORIZATION_REJECTED,
                )
                self.assertFalse(record.authority_independent)

    def test_authority_is_separate_from_execution_authority(self) -> None:
        bundle = self.source_bundle()
        evidence = self.evidence(bundle)
        request = self.request(
            bundle,
            evidence,
            future_execution_authority_id="future-authorization-authority",
        )
        record = self.execute(bundle, evidence, request)
        self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_REJECTED)
        self.assertFalse(record.independent_from_future_execution_authority)

    def test_mandate_qualification_and_independence_denials(self) -> None:
        bundle = self.source_bundle()
        cases = (
            ({"authority_mandate_verified": False}, "authority_mandate_not_verified"),
            (
                {"authority_qualification_verified": False},
                "authority_qualification_not_verified",
            ),
            (
                {"authority_independence_declared": False},
                "authority_independence_not_declared",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_DENIED)
                self.assertEqual(record.reason, reason)

    def test_conflict_jurisdiction_and_quorum_denials(self) -> None:
        bundle = self.source_bundle()
        cases = (
            (
                {"conflict_disclosure_complete": False},
                "conflict_disclosure_incomplete",
            ),
            ({"material_conflict_present": True}, "material_conflict_present"),
            ({"jurisdiction_verified": False}, "jurisdiction_not_verified"),
            ({"quorum_satisfied": False}, "quorum_not_satisfied"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_DENIED)
                self.assertEqual(record.reason, reason)

    def test_reasoning_proportionality_and_alternatives_denials(self) -> None:
        bundle = self.source_bundle()
        cases = (
            (
                {"reasoned_decision_complete": False},
                "reasoned_decision_incomplete",
            ),
            (
                {"proportionality_satisfied": False},
                "proportionality_not_satisfied",
            ),
            (
                {"less_restrictive_alternatives_exhausted": False},
                "less_restrictive_alternatives_not_exhausted",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_DENIED)
                self.assertEqual(record.reason, reason)

    def test_impact_routes_and_protected_state_denials(self) -> None:
        bundle = self.source_bundle()
        cases = (
            (
                {"irreversibility_review_complete": False},
                "irreversibility_review_incomplete",
            ),
            (
                {"human_impact_review_complete": False},
                "human_impact_review_incomplete",
            ),
            ({"appeal_route_available": False}, "appeal_route_missing"),
            ({"dissent_route_available": False}, "dissent_route_missing"),
            ({"protected_core_excluded": False}, "protected_core_not_excluded"),
            ({"institutional_hold_active": True}, "institutional_hold_active"),
            ({"emergency_state_active": True}, "emergency_state_active"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, INDEPENDENT_AUTHORIZATION_DENIED)
                self.assertEqual(record.reason, reason)

    def test_expiry_staleness_and_delay_are_rejected(self) -> None:
        bundle = self.source_bundle()
        expired = self.evidence(
            bundle,
            authorization_expiry_at_epoch_seconds=(
                self.authorization_completed_at - 1
            ),
        )
        stale = self.evidence(
            bundle,
            captured_at_epoch_seconds=self.authorization_completed_at - 301,
        )
        late_completed = bundle[3].completed_at_epoch_seconds + 301
        late_evidence = self.evidence(
            bundle,
            authorization_requested_at_epoch_seconds=late_completed - 2,
            captured_at_epoch_seconds=late_completed - 1,
            authorization_completed_at_epoch_seconds=late_completed,
            authorization_expiry_at_epoch_seconds=late_completed + 600,
        )
        late_request = self.request(
            bundle,
            late_evidence,
            requested_at_epoch_seconds=late_completed - 2,
            completed_at_epoch_seconds=late_completed,
        )
        cases = (
            (expired, self.request(bundle, expired)),
            (stale, self.request(bundle, stale)),
            (late_evidence, late_request),
        )
        for evidence, request in cases:
            with self.subTest(evidence=evidence.evidence_id):
                record = self.execute(bundle, evidence, request)
                self.assertEqual(
                    record.status,
                    INDEPENDENT_AUTHORIZATION_REJECTED,
                )

    def test_subject_and_source_artifact_tamper_reject(self) -> None:
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
            request_digest=apoptosis_independent_authorization_request_digest(
                subject_request
            ),
        )
        tampered_evidence = replace(
            evidence,
            source_external_review_record_digest="z" * 64,
            evidence_digest="",
        )
        tampered_evidence = replace(
            tampered_evidence,
            evidence_digest=apoptosis_independent_authorization_evidence_digest(
                tampered_evidence
            ),
        )
        tampered_request = self.request(bundle, tampered_evidence)
        self.assertEqual(
            self.execute(bundle, evidence, subject_request).status,
            INDEPENDENT_AUTHORIZATION_REJECTED,
        )
        self.assertEqual(
            self.execute(bundle, tampered_evidence, tampered_request).status,
            INDEPENDENT_AUTHORIZATION_REJECTED,
        )

    def test_unsafe_policy_rejects_and_denied_does_not_advance(self) -> None:
        unsafe = replace(
            self.authorization_policy,
            allow_execution_request=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_independent_authorization_policy_digest(
                unsafe
            ),
        )
        rejected = self.execute(policy=unsafe)
        self.assertEqual(rejected.status, INDEPENDENT_AUTHORIZATION_REJECTED)
        bundle = self.source_bundle()
        denied = self.execute(
            bundle,
            self.evidence(bundle, quorum_satisfied=False),
        )
        self.assertTrue(denied.authorization_decision_made)
        self.assertTrue(denied.authorization_denied)
        self.assertFalse(denied.bounded_execution_preparation_allowed_next)
        self.assertFalse(denied.execution_request_issued)

    def test_all_outcomes_are_deterministic_read_only_and_tamper_evident(self) -> None:
        approved_left = self.execute()
        approved_right = self.execute()
        self.assertEqual(approved_left, approved_right)
        bundle = self.source_bundle()
        denied = self.execute(
            bundle,
            self.evidence(bundle, quorum_satisfied=False),
        )
        rejected_bundle = self.source_bundle(authority_blocked=True)
        rejected = self.execute(rejected_bundle)
        for record in (approved_left, denied, rejected):
            self.assertFalse(record.execution_request_issued)
            self.assertFalse(record.execution_decision_made)
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
            execution_request_issued=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_independent_authorization_record_digest(
                tampered
            ),
        )
        issues = self.record_issues(bundle, evidence, request, tampered)
        self.assertIn(
            "apoptosis_independent_authorization_recomputation_mismatch",
            issues,
        )
        self.assertIn(
            "apoptosis_independent_authorization_execution_effect_performed",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
