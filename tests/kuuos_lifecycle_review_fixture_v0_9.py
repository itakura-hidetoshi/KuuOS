from __future__ import annotations

import unittest

from runtime.kuuos_lifecycle_review_chain_v0_9 import named_source
from runtime.kuuos_lifecycle_review_v0_9 import (
    build_apoptosis_execution_review_evidence,
    build_apoptosis_execution_review_policy,
    build_apoptosis_execution_review_request,
    review_apoptosis_execution,
)
from tests.test_kuuos_apoptosis_bounded_execution_preparation_v0_8 import (
    ApoptosisBoundedExecutionPreparationV08Tests,
)


class LifecycleReviewFixtureV09(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = ApoptosisBoundedExecutionPreparationV08Tests(
            methodName="runTest"
        )
        self.upstream.setUp()
        self.reviewer_id = "lifecycle-reviewer"
        self.operator_id = "lifecycle-operator"
        self.requested_at = self.upstream.preparation_completed_at + 20
        self.captured_at = self.requested_at + 20
        self.completed_at = self.requested_at + 40
        self.expires_at = self.completed_at + 600
        base = self.make_bundle()
        named = named_source(base[4])
        allowed = {
            self.reviewer_id,
            self.operator_id,
            base[3].future_execution_authority_id,
            base[3].preparer_id,
            base[3].subject_id,
            named["candidate_record"].issuer_id,
            named["dependency_record"].reviewer_id,
            named["authority_record"].reviewer_id,
            named["authority_evidence"].responsible_authority_id,
            named["quiescence_record"].reviewer_id,
            named["external_record"].reviewer_id,
            named["external_evidence"].quiescence_evidence_producer_id,
            named["authorization_record"].authority_id,
        }
        self.policy = build_apoptosis_execution_review_policy(
            "lifecycle-review-policy-v0-9",
            allowed_reviewer_ids=tuple(allowed),
            allowed_reviewer_organization_ids=("lifecycle-review-organization",),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_review_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_review_expiry_seconds=900,
            max_execution_window_seconds=120,
            max_scope_items=8,
        )

    def make_bundle(
        self,
        *,
        authorization_overrides: dict | None = None,
        preparation_overrides: dict | None = None,
    ):
        authorization = self.upstream.authorization_bundle(
            authorization_overrides=authorization_overrides
        )
        evidence = self.upstream.evidence(
            authorization,
            **(preparation_overrides or {}),
        )
        request = self.upstream.request(authorization, evidence)
        record = self.upstream.execute(authorization, evidence, request)
        source = self.upstream.execution_args(
            authorization,
            evidence,
            request,
        )[3:]
        return request, evidence, self.upstream.policy, record, source

    def make_evidence(self, bundle, **overrides):
        values = {
            "evidence_id": "lifecycle-review-evidence-001",
            "review_id": "lifecycle-review-001",
            "reviewer_id": self.reviewer_id,
            "reviewer_organization_id": "lifecycle-review-organization",
            "future_execution_operator_id": self.operator_id,
            "reviewer_qualification_receipt_digest": "q" * 64,
            "reviewer_qualification_verified": True,
            "reviewer_independence_declaration_digest": "i" * 64,
            "reviewer_independence_declared": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "review_requested_at_epoch_seconds": self.requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
            "review_expiry_at_epoch_seconds": self.expires_at,
            "appeal_route_digest": "a" * 64,
            "appeal_route_available": True,
            "dissent_route_digest": "d" * 64,
            "dissent_route_available": True,
        }
        values.update(overrides)
        return build_apoptosis_execution_review_evidence(
            bundle[0], bundle[1], bundle[2], bundle[3], bundle[4], **values
        )

    def make_request(self, bundle, evidence, **overrides):
        values = {
            "review_id": "lifecycle-review-001",
            "reviewer_id": self.reviewer_id,
            "reviewer_organization_id": "lifecycle-review-organization",
            "review_requested_at_epoch_seconds": (
                evidence.review_requested_at_epoch_seconds
            ),
            "completed_at_epoch_seconds": evidence.completed_at_epoch_seconds,
            "preparation_record": bundle[3],
            "review_evidence": evidence,
            "future_execution_operator_id": evidence.future_execution_operator_id,
        }
        values.update(overrides)
        return build_apoptosis_execution_review_request(**values)

    def review(self, bundle=None, evidence=None, request=None, policy=None):
        bundle = self.make_bundle() if bundle is None else bundle
        evidence = self.make_evidence(bundle) if evidence is None else evidence
        request = self.make_request(bundle, evidence) if request is None else request
        args = (
            request,
            evidence,
            self.policy if policy is None else policy,
            bundle[0], bundle[1], bundle[2], bundle[3], *bundle[4],
        )
        return review_apoptosis_execution(*args)
