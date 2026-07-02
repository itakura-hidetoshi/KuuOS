from __future__ import annotations

import unittest

from runtime.kuuos_lifecycle_governance_request_v0_10 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from runtime.kuuos_lifecycle_source_chain_v0_10 import (
    prior_actor_ids,
    source_authority,
    source_operator,
)
from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


class LifecycleBoundedRequestFixtureV010(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleReviewFixtureV09(methodName="runTest")
        self.upstream.setUp()
        self.requester_id = "bounded-request-submitter-v0-10"
        self.requester_organization_id = "lifecycle-request-organization"
        self.requested_at = self.upstream.completed_at + 20
        self.captured_at = self.requested_at + 20
        self.completed_at = self.requested_at + 40
        self.request_expiry_at = self.completed_at + 500
        self.decision_deadline_at = self.completed_at + 300
        source = self.make_source()
        review_record = source[3]
        allowed_requesters = prior_actor_ids(
            source[0].subject_id,
            review_record,
            source[4],
        ) | {
            self.requester_id,
            source_authority(review_record),
            source_operator(review_record),
        }
        self.policy = make_policy(
            "lifecycle-bounded-request-policy-v0-10",
            allowed_requester_ids=tuple(allowed_requesters),
            allowed_requester_organization_ids=(
                self.requester_organization_id,
            ),
            allowed_decision_authority_ids=(
                source_authority(review_record),
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_request_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_request_expiry_seconds=600,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )

    def make_source(
        self,
        *,
        review_evidence_overrides: dict | None = None,
        review_request_overrides: dict | None = None,
    ):
        review_bundle = self.upstream.make_bundle()
        review_evidence = self.upstream.make_evidence(
            review_bundle,
            **(review_evidence_overrides or {}),
        )
        review_request = self.upstream.make_request(
            review_bundle,
            review_evidence,
            **(review_request_overrides or {}),
        )
        review_record = self.upstream.review(
            review_bundle,
            review_evidence,
            review_request,
        )
        source_args = (
            review_bundle[0],
            review_bundle[1],
            review_bundle[2],
            review_bundle[3],
            *review_bundle[4],
        )
        return (
            review_request,
            review_evidence,
            self.upstream.policy,
            review_record,
            source_args,
        )

    def make_request_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-bounded-request-evidence-001",
            "bounded_request_id": "lifecycle-bounded-request-001",
            "requester_id": self.requester_id,
            "requester_organization_id": self.requester_organization_id,
            "requester_qualification_receipt_digest": "q" * 64,
            "requester_qualification_verified": True,
            "requester_independence_declaration_digest": "i" * 64,
            "requester_independence_declared": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "requested_at_epoch_seconds": self.requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
            "request_expiry_at_epoch_seconds": self.request_expiry_at,
            "decision_deadline_at_epoch_seconds": self.decision_deadline_at,
            "decision_route_digest": "u" * 64,
            "decision_route_available": True,
        }
        values.update(overrides)
        return make_evidence(
            source[0],
            source[1],
            source[2],
            source[3],
            source[4],
            **values,
        )

    def make_request_submission(self, source, evidence, **overrides):
        values = {
            "bounded_request_id": "lifecycle-bounded-request-001",
            "requester_id": self.requester_id,
            "requester_organization_id": self.requester_organization_id,
            "requested_at_epoch_seconds": self.requested_at,
            "completed_at_epoch_seconds": self.completed_at,
            "review_record": source[3],
            "request_evidence": evidence,
            "decision_route_digest": evidence.decision_route_digest,
            "decision_deadline_at_epoch_seconds": (
                evidence.decision_deadline_at_epoch_seconds
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, request, policy=None):
        return (
            request,
            evidence,
            self.policy if policy is None else policy,
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )

    def evaluate_request(self, source=None, evidence=None, request=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = (
            self.make_request_evidence(source)
            if evidence is None
            else evidence
        )
        request = (
            self.make_request_submission(source, evidence)
            if request is None
            else request
        )
        return verify_artifact(*self.artifact_args(source, evidence, request, policy))
