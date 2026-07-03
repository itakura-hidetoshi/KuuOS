from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_governance_transition_review_v0_17 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from tests.kuuos_lifecycle_post_operation_review_fixture_v0_16 import (
    LifecyclePostOperationReviewFixtureV016,
)


class LifecycleTransitionReviewFixtureV017(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecyclePostOperationReviewFixtureV016(
            methodName="runTest"
        )
        self.upstream.setUp()
        source = self.make_source()
        self.transition_reviewer_id = "lifecycle-transition-reviewer"
        self.transition_reviewer_organization_id = (
            "lifecycle-transition-review-organization"
        )
        self.transition_decision_maker_id = "lifecycle-transition-decision-maker"
        self.proposed_transition_kind = "ENTER_QUIESCENCE"
        self.proposed_target_state_digest = "t" * 64
        self.review_requested_at = source[0].reviewed_at_epoch_seconds + 1
        self.captured_at = self.review_requested_at + 1
        self.reviewed_at = self.captured_at + 1
        self.review_expiry_at = self.reviewed_at + 60
        self.transition_decision_deadline_at = self.reviewed_at + 120
        self.policy = make_policy(
            "lifecycle-bounded-transition-review-policy-v0-17",
            allowed_transition_reviewer_ids=(self.transition_reviewer_id,),
            allowed_transition_reviewer_organization_ids=(
                self.transition_reviewer_organization_id,
            ),
            allowed_transition_decision_maker_ids=(
                self.transition_decision_maker_id,
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            allowed_transition_kinds=(self.proposed_transition_kind,),
            max_review_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_review_expiry_seconds=120,
            max_decision_delay_seconds=180,
            max_scope_items=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        evidence = self.upstream.make_review_evidence(source)
        review = self.upstream.make_review_submission(source, evidence)
        record = self.upstream.evaluate_review(source, evidence, review)
        source_args = tuple(
            self.upstream.artifact_args(source, evidence, review)[3:]
        )
        return review, evidence, self.upstream.policy, record, source_args

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(value, record_digest=source_record_digest(value))

    @staticmethod
    def refresh_evidence(evidence, **changes):
        value = replace(evidence, **changes, evidence_digest="")
        return replace(value, evidence_digest=evidence_digest(value))

    @staticmethod
    def refresh_review(review, **changes):
        value = replace(review, **changes, review_digest="")
        return replace(value, review_digest=submission_digest(value))

    def make_transition_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-transition-review-evidence-001",
            "transition_review_id": "lifecycle-transition-review-001",
            "transition_reviewer_id": self.transition_reviewer_id,
            "transition_reviewer_organization_id": (
                self.transition_reviewer_organization_id
            ),
            "transition_reviewer_mandate_receipt_digest": "m" * 64,
            "transition_reviewer_mandate_verified": True,
            "transition_reviewer_qualification_receipt_digest": "q" * 64,
            "transition_reviewer_qualification_verified": True,
            "transition_reviewer_identity_confirmation_digest": "i" * 64,
            "transition_reviewer_identity_confirmed": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "review_readiness_receipt_digest": "r" * 64,
            "review_ready": True,
            "transition_decision_maker_id": self.transition_decision_maker_id,
            "proposed_transition_kind": self.proposed_transition_kind,
            "current_lifecycle_state_digest": "s" * 64,
            "proposed_target_state_digest": self.proposed_target_state_digest,
            "transition_basis_digest": "b" * 64,
            "transition_basis_sufficient": True,
            "necessity_assessment_digest": "n" * 64,
            "necessity_verified": True,
            "proportionality_assessment_digest": "p" * 64,
            "proportionality_verified": True,
            "reversibility_assessment_digest": "v" * 64,
            "reversibility_or_exception_justified": True,
            "dependency_clearance_digest": "d" * 64,
            "dependencies_cleared": True,
            "authority_continuity_digest": "a" * 64,
            "authority_continuity_verified": True,
            "transition_state_compatibility_digest": "x" * 64,
            "transition_state_compatible": True,
            "stakeholder_impact_assessment_digest": "h" * 64,
            "stakeholder_impact_acceptable": True,
            "legal_policy_compliance_digest": "l" * 64,
            "legal_policy_compliant": True,
            "appeal_route_digest": "e" * 64,
            "appeal_route_available": True,
            "dissent_route_digest": "f" * 64,
            "dissent_route_available": True,
            "minority_opinion_digest": "o" * 64,
            "minority_opinion_recorded": True,
            "unresolved_anomaly_present": False,
            "recovery_required": False,
            "institutional_hold_active": False,
            "emergency_state_active": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "review_requested_at_epoch_seconds": self.review_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "reviewed_at_epoch_seconds": self.reviewed_at,
            "review_expiry_at_epoch_seconds": self.review_expiry_at,
            "transition_decision_deadline_at_epoch_seconds": (
                self.transition_decision_deadline_at
            ),
        }
        values.update(overrides)
        return make_evidence(
            source[0], source[1], source[2], source[3], source[4], **values
        )

    def make_transition_review(self, source, evidence, **overrides):
        values = {
            "transition_review_id": "lifecycle-transition-review-001",
            "transition_reviewer_id": self.transition_reviewer_id,
            "transition_reviewer_organization_id": (
                self.transition_reviewer_organization_id
            ),
            "review_requested_at_epoch_seconds": self.review_requested_at,
            "reviewed_at_epoch_seconds": self.reviewed_at,
            "review_expiry_at_epoch_seconds": self.review_expiry_at,
            "source_review": source[0],
            "source_record": source[3],
            "review_evidence": evidence,
            "transition_decision_maker_id": self.transition_decision_maker_id,
            "proposed_transition_kind": self.proposed_transition_kind,
            "proposed_target_state_digest": self.proposed_target_state_digest,
            "transition_review_route_digest": evidence.transition_review_route_digest,
            "transition_decision_deadline_at_epoch_seconds": (
                self.transition_decision_deadline_at
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, review, policy=None):
        return (
            review,
            evidence,
            self.policy if policy is None else policy,
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )

    def evaluate_transition_review(
        self,
        source=None,
        evidence=None,
        review=None,
        policy=None,
    ):
        source = self.make_source() if source is None else source
        evidence = (
            self.make_transition_evidence(source)
            if evidence is None
            else evidence
        )
        review = (
            self.make_transition_review(source, evidence)
            if review is None
            else review
        )
        return verify_artifact(
            *self.artifact_args(source, evidence, review, policy)
        )
