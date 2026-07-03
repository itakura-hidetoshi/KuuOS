from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_post_operation_review_types_v0_16 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_governance_post_operation_review_v0_16 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from tests.kuuos_lifecycle_operation_completion_fixture_v0_15 import (
    LifecycleOperationCompletionFixtureV015,
)


class LifecyclePostOperationReviewFixtureV016(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleOperationCompletionFixtureV015(
            methodName="runTest"
        )
        self.upstream.setUp()
        source = self.make_source()
        source_completion = source[0]
        self.post_operation_reviewer_id = (
            "lifecycle-post-operation-reviewer"
        )
        self.post_operation_reviewer_organization_id = (
            "lifecycle-post-operation-review-organization"
        )
        self.review_requested_at = (
            source_completion.completed_at_epoch_seconds + 1
        )
        self.captured_at = self.review_requested_at + 1
        self.reviewed_at = self.captured_at + 1
        self.policy = make_policy(
            "lifecycle-bounded-post-operation-review-policy-v0-16",
            allowed_post_operation_reviewer_ids=(
                self.post_operation_reviewer_id,
            ),
            allowed_post_operation_reviewer_organization_ids=(
                self.post_operation_reviewer_organization_id,
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_review_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        completion_evidence = self.upstream.make_completion_evidence(source)
        completion = self.upstream.make_completion_submission(
            source, completion_evidence
        )
        record = self.upstream.evaluate_completion(
            source, completion_evidence, completion
        )
        source_args = tuple(
            self.upstream.artifact_args(
                source, completion_evidence, completion
            )[3:]
        )
        return (
            completion,
            completion_evidence,
            self.upstream.policy,
            record,
            source_args,
        )

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(
            value, record_digest=source_record_digest(value)
        )

    @staticmethod
    def refresh_evidence(evidence, **changes):
        value = replace(evidence, **changes, evidence_digest="")
        return replace(
            value, evidence_digest=evidence_digest(value)
        )

    @staticmethod
    def refresh_review(review, **changes):
        value = replace(review, **changes, review_digest="")
        return replace(
            value, review_digest=submission_digest(value)
        )

    def make_review_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-post-operation-review-evidence-001",
            "post_operation_review_id": (
                "lifecycle-post-operation-review-001"
            ),
            "post_operation_reviewer_id": (
                self.post_operation_reviewer_id
            ),
            "post_operation_reviewer_organization_id": (
                self.post_operation_reviewer_organization_id
            ),
            "post_operation_reviewer_mandate_receipt_digest": "m" * 64,
            "post_operation_reviewer_mandate_verified": True,
            "post_operation_reviewer_qualification_receipt_digest": "q" * 64,
            "post_operation_reviewer_qualification_verified": True,
            "post_operation_reviewer_identity_confirmation_digest": "i" * 64,
            "post_operation_reviewer_identity_confirmed": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "review_readiness_receipt_digest": "r" * 64,
            "review_ready": True,
            "intended_result_digest": "d" * 64,
            "observed_result_digest": "d" * 64,
            "intended_result_matches_observed": True,
            "target_post_state_review_digest": "t" * 64,
            "target_post_state_verified": True,
            "collateral_effects_assessment_digest": "a" * 64,
            "collateral_effects_absent": True,
            "protected_resource_continuity_digest": "p" * 64,
            "protected_resources_intact": True,
            "protected_core_continuity_digest": "k" * 64,
            "protected_core_intact": True,
            "monitoring_evidence_review_digest": "n" * 64,
            "monitoring_evidence_sufficient": True,
            "completion_evidence_review_digest": "e" * 64,
            "completion_evidence_sufficient": True,
            "unresolved_anomaly_present": False,
            "rollback_required": False,
            "recovery_required": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "review_requested_at_epoch_seconds": self.review_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "reviewed_at_epoch_seconds": self.reviewed_at,
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

    def make_review_submission(
        self, source, evidence, **overrides
    ):
        values = {
            "post_operation_review_id": (
                "lifecycle-post-operation-review-001"
            ),
            "post_operation_reviewer_id": (
                self.post_operation_reviewer_id
            ),
            "post_operation_reviewer_organization_id": (
                self.post_operation_reviewer_organization_id
            ),
            "review_requested_at_epoch_seconds": (
                self.review_requested_at
            ),
            "reviewed_at_epoch_seconds": self.reviewed_at,
            "source_completion": source[0],
            "source_record": source[3],
            "review_evidence": evidence,
            "post_operation_review_route_digest": (
                evidence.post_operation_review_route_digest
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(
        self, source, evidence, review, policy=None
    ):
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

    def evaluate_review(
        self,
        source=None,
        evidence=None,
        review=None,
        policy=None,
    ):
        source = self.make_source() if source is None else source
        evidence = (
            self.make_review_evidence(source)
            if evidence is None
            else evidence
        )
        review = (
            self.make_review_submission(source, evidence)
            if review is None
            else review
        )
        return verify_artifact(
            *self.artifact_args(source, evidence, review, policy)
        )
