from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_governance_decision_review_v0_11 import (
    make_evidence,
    make_policy,
    make_submission,
    prior_actor_ids,
    verify_artifact,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    evidence_digest,
    submission_digest,
)
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


class LifecycleDecisionReviewFixtureV011(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleBoundedRequestFixtureV010(methodName="runTest")
        self.upstream.setUp()
        self.reviewer_id = "bounded-decision-reviewer-v0-11"
        self.reviewer_organization_id = "lifecycle-decision-review-organization"
        self.review_requested_at = self.upstream.completed_at + 20
        self.captured_at = self.review_requested_at + 20
        self.completed_at = self.review_requested_at + 40
        self.review_expiry_at = self.completed_at + 240
        self.authorization_deadline_at = self.completed_at + 180
        source = self.make_source()
        source_request, _, _, _, source_args = source
        actors = prior_actor_ids(source_request.subject_id, source_request, source_args)
        actors.update(
            {
                self.reviewer_id,
                source_request.requester_id,
                source_request.decision_authority_id,
                source_request.future_operator_id,
            }
        )
        self.policy = make_policy(
            "lifecycle-bounded-decision-review-policy-v0-11",
            allowed_decision_reviewer_ids=tuple(actors),
            allowed_decision_reviewer_organization_ids=(
                self.reviewer_organization_id,
            ),
            allowed_authorization_decision_maker_ids=(
                source_request.decision_authority_id,
                source_request.future_operator_id,
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_review_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_review_expiry_seconds=300,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        request_source = self.upstream.make_source()
        request_evidence = self.upstream.make_request_evidence(request_source)
        request = self.upstream.make_request_submission(request_source, request_evidence)
        record = self.upstream.evaluate_request(request_source, request_evidence, request)
        source_args = (
            request_source[0],
            request_source[1],
            request_source[2],
            request_source[3],
            *request_source[4],
        )
        return request, request_evidence, self.upstream.policy, record, source_args

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

    def make_review_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-bounded-decision-review-evidence-001",
            "decision_review_id": "lifecycle-bounded-decision-review-001",
            "decision_reviewer_id": self.reviewer_id,
            "decision_reviewer_organization_id": self.reviewer_organization_id,
            "reviewer_qualification_receipt_digest": "q" * 64,
            "reviewer_qualification_verified": True,
            "reviewer_independence_declaration_digest": "i" * 64,
            "reviewer_independence_declared": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "review_requested_at_epoch_seconds": self.review_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
            "review_expiry_at_epoch_seconds": self.review_expiry_at,
            "authorization_decision_deadline_at_epoch_seconds": (
                self.authorization_deadline_at
            ),
            "authorization_route_digest": "a" * 64,
            "authorization_route_available": True,
            "minority_opinion_digest": "m" * 64,
            "minority_opinion_recorded": True,
        }
        values.update(overrides)
        return make_evidence(
            source[0], source[1], source[2], source[3], source[4], **values
        )

    def make_review_submission(self, source, evidence, **overrides):
        values = {
            "decision_review_id": "lifecycle-bounded-decision-review-001",
            "decision_reviewer_id": self.reviewer_id,
            "decision_reviewer_organization_id": self.reviewer_organization_id,
            "review_requested_at_epoch_seconds": self.review_requested_at,
            "completed_at_epoch_seconds": self.completed_at,
            "source_request": source[0],
            "source_record": source[3],
            "review_evidence": evidence,
            "authorization_route_digest": evidence.authorization_route_digest,
            "authorization_decision_deadline_at_epoch_seconds": (
                evidence.authorization_decision_deadline_at_epoch_seconds
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

    def evaluate_review(self, source=None, evidence=None, review=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = self.make_review_evidence(source) if evidence is None else evidence
        review = self.make_review_submission(source, evidence) if review is None else review
        return verify_artifact(*self.artifact_args(source, evidence, review, policy))
