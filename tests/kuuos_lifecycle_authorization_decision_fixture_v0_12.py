from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    evidence_digest,
    record_digest as authorization_record_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_authorization_decision_v0_12 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    record_digest as decision_review_record_digest,
)
from tests.kuuos_lifecycle_decision_review_fixture_v0_11 import (
    LifecycleDecisionReviewFixtureV011,
)


class LifecycleAuthorizationDecisionFixtureV012(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleDecisionReviewFixtureV011(methodName="runTest")
        self.upstream.setUp()
        source = self.make_source()
        source_review = source[0]
        self.authorization_decision_maker_id = (
            source_review.authorization_decision_maker_id
        )
        self.authorization_decision_maker_organization_id = (
            "lifecycle-authorization-decision-organization"
        )
        self.decision_requested_at = source_review.completed_at_epoch_seconds + 20
        self.captured_at = self.decision_requested_at + 10
        self.completed_at = self.decision_requested_at + 20
        self.approval_expiry_at = self.completed_at + 100
        self.policy = make_policy(
            "lifecycle-bounded-authorization-decision-policy-v0-12",
            allowed_authorization_decision_maker_ids=(
                self.authorization_decision_maker_id,
            ),
            allowed_authorization_decision_maker_organization_ids=(
                self.authorization_decision_maker_organization_id,
            ),
            allowed_future_operator_ids=(source_review.future_operator_id,),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_decision_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_approval_expiry_seconds=300,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        review_source = self.upstream.make_source()
        review_evidence = self.upstream.make_review_evidence(review_source)
        review = self.upstream.make_review_submission(review_source, review_evidence)
        record = self.upstream.evaluate_review(
            review_source, review_evidence, review
        )
        source_args = (
            review_source[0],
            review_source[1],
            review_source[2],
            review_source[3],
            *review_source[4],
        )
        return review, review_evidence, self.upstream.policy, record, source_args

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(
            value, record_digest=decision_review_record_digest(value)
        )

    @staticmethod
    def refresh_evidence(evidence, **changes):
        value = replace(evidence, **changes, evidence_digest="")
        return replace(value, evidence_digest=evidence_digest(value))

    @staticmethod
    def refresh_decision(decision, **changes):
        value = replace(decision, **changes, decision_digest="")
        return replace(value, decision_digest=submission_digest(value))

    @staticmethod
    def refresh_artifact(artifact, **changes):
        value = replace(artifact, **changes, record_digest="")
        return replace(
            value, record_digest=authorization_record_digest(value)
        )

    def make_authorization_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-authorization-decision-evidence-001",
            "authorization_decision_id": "lifecycle-authorization-decision-001",
            "authorization_decision_maker_id": (
                self.authorization_decision_maker_id
            ),
            "authorization_decision_maker_organization_id": (
                self.authorization_decision_maker_organization_id
            ),
            "authority_mandate_receipt_digest": "m" * 64,
            "authority_mandate_verified": True,
            "authority_qualification_receipt_digest": "q" * 64,
            "authority_qualification_verified": True,
            "authority_independence_declaration_digest": "i" * 64,
            "authority_independence_declared": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "quorum_receipt_digest": "u" * 64,
            "quorum_verified": True,
            "decision_rationale_digest": "r" * 64,
            "decision_rationale_complete": True,
            "proportionality_review_digest": "p" * 64,
            "proportionality_satisfied": True,
            "less_restrictive_alternatives_digest": "l" * 64,
            "less_restrictive_alternatives_exhausted": True,
            "irreversibility_review_digest": "v" * 64,
            "irreversibility_review_complete": True,
            "human_impact_review_digest": "h" * 64,
            "human_impact_review_complete": True,
            "decision_requested_at_epoch_seconds": self.decision_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
            "approval_expiry_at_epoch_seconds": self.approval_expiry_at,
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

    def make_authorization_submission(self, source, evidence, **overrides):
        values = {
            "authorization_decision_id": "lifecycle-authorization-decision-001",
            "authorization_decision_maker_id": (
                self.authorization_decision_maker_id
            ),
            "authorization_decision_maker_organization_id": (
                self.authorization_decision_maker_organization_id
            ),
            "decision_requested_at_epoch_seconds": self.decision_requested_at,
            "completed_at_epoch_seconds": self.completed_at,
            "source_review": source[0],
            "source_record": source[3],
            "authorization_evidence": evidence,
            "approval_expiry_at_epoch_seconds": (
                evidence.approval_expiry_at_epoch_seconds
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, decision, policy=None):
        return (
            decision,
            evidence,
            self.policy if policy is None else policy,
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )

    def evaluate_decision(
        self, source=None, evidence=None, decision=None, policy=None
    ):
        source = self.make_source() if source is None else source
        evidence = (
            self.make_authorization_evidence(source)
            if evidence is None
            else evidence
        )
        decision = (
            self.make_authorization_submission(source, evidence)
            if decision is None
            else decision
        )
        return verify_artifact(
            *self.artifact_args(source, evidence, decision, policy)
        )
