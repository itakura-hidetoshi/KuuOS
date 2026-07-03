from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_governance_transition_decision_v0_18 import (
    make_evidence,
    make_policy,
    make_state,
    make_submission,
    make_transition_rule,
    verify_artifact,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_transition_review_types_v0_17 import (
    record_digest as source_record_digest,
)
from tests.kuuos_lifecycle_transition_review_fixture_v0_17 import (
    LifecycleTransitionReviewFixtureV017,
)


class LifecycleTransitionDecisionFixtureV018(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleTransitionReviewFixtureV017(methodName="runTest")
        self.upstream.setUp()
        self.current_state = make_state(
            authority_state="AUTHORIZED",
            quiescence_state="ACTIVE",
            terminal_state="NON_TERMINAL",
            resource_state="INTACT",
            state_revision=7,
        )
        self.target_state = make_state(
            authority_state="AUTHORIZED",
            quiescence_state="QUIESCENT",
            terminal_state="NON_TERMINAL",
            resource_state="INTACT",
            state_revision=8,
        )
        self.transition_rule = make_transition_rule(
            rule_id="enter-quiescence-v0-18",
            current_state=self.current_state,
            transition_kind=self.upstream.proposed_transition_kind,
            target_state=self.target_state,
            policy_basis_digest="p" * 64,
        )
        source = self.make_source()
        self.transition_decision_maker_id = self.upstream.transition_decision_maker_id
        self.transition_decision_maker_organization_id = (
            "lifecycle-transition-decision-organization"
        )
        self.transition_preparer_id = "lifecycle-transition-preparer"
        self.decision_requested_at = source[0].reviewed_at_epoch_seconds + 1
        self.captured_at = self.decision_requested_at + 1
        self.decided_at = self.captured_at + 1
        self.decision_expiry_at = self.decided_at + 60
        self.preparation_deadline_at = self.decided_at + 120
        self.policy = make_policy(
            "lifecycle-bounded-transition-decision-policy-v0-18",
            allowed_transition_decision_maker_ids=(
                self.transition_decision_maker_id,
            ),
            allowed_transition_decision_maker_organization_ids=(
                self.transition_decision_maker_organization_id,
            ),
            allowed_transition_preparer_ids=(self.transition_preparer_id,),
            allowed_transition_kinds=(self.upstream.proposed_transition_kind,),
            max_decision_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_decision_expiry_seconds=120,
            max_preparation_delay_seconds=180,
        )

    def make_source(self):
        source = self.upstream.make_source()
        evidence = self.upstream.make_transition_evidence(
            source,
            current_lifecycle_state_digest=self.current_state.state_digest,
            proposed_target_state_digest=self.target_state.state_digest,
        )
        review = self.upstream.make_transition_review(
            source,
            evidence,
            proposed_target_state_digest=self.target_state.state_digest,
        )
        record = self.upstream.evaluate_transition_review(source, evidence, review)
        source_args = tuple(self.upstream.artifact_args(source, evidence, review)[3:])
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
    def refresh_decision(decision, **changes):
        value = replace(decision, **changes, decision_digest="")
        return replace(value, decision_digest=submission_digest(value))

    def make_decision_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-transition-decision-evidence-001",
            "transition_decision_id": "lifecycle-transition-decision-001",
            "transition_decision_maker_id": self.transition_decision_maker_id,
            "transition_decision_maker_organization_id": (
                self.transition_decision_maker_organization_id
            ),
            "decision_maker_mandate_receipt_digest": "m" * 64,
            "decision_maker_mandate_verified": True,
            "decision_maker_qualification_receipt_digest": "q" * 64,
            "decision_maker_qualification_verified": True,
            "decision_maker_identity_confirmation_digest": "i" * 64,
            "decision_maker_identity_confirmed": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "decision_readiness_receipt_digest": "r" * 64,
            "decision_ready": True,
            "transition_preparer_id": self.transition_preparer_id,
            "decision_rationale_digest": "d" * 64,
            "decision_approved": True,
            "denial_route_digest": "n" * 64,
            "denial_route_available": True,
            "appeal_route_digest": "a" * 64,
            "appeal_route_available": True,
            "dissent_route_digest": "s" * 64,
            "dissent_route_available": True,
            "minority_opinion_digest": "o" * 64,
            "minority_opinion_recorded": True,
            "unresolved_anomaly_present": False,
            "recovery_required": False,
            "institutional_hold_active": False,
            "emergency_state_active": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "decision_requested_at_epoch_seconds": self.decision_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "decided_at_epoch_seconds": self.decided_at,
            "decision_expiry_at_epoch_seconds": self.decision_expiry_at,
            "transition_preparation_deadline_at_epoch_seconds": (
                self.preparation_deadline_at
            ),
        }
        values.update(overrides)
        return make_evidence(
            source[0],
            source[1],
            source[2],
            source[3],
            source[4],
            current_state=self.current_state,
            target_state=self.target_state,
            transition_rule=self.transition_rule,
            **values,
        )

    def make_decision(self, source, evidence, **overrides):
        values = {
            "transition_decision_id": "lifecycle-transition-decision-001",
            "transition_decision_maker_id": self.transition_decision_maker_id,
            "transition_decision_maker_organization_id": (
                self.transition_decision_maker_organization_id
            ),
            "decision_requested_at_epoch_seconds": self.decision_requested_at,
            "decided_at_epoch_seconds": self.decided_at,
            "decision_expiry_at_epoch_seconds": self.decision_expiry_at,
            "source_review": source[0],
            "source_record": source[3],
            "decision_evidence": evidence,
            "transition_preparer_id": self.transition_preparer_id,
            "transition_preparation_route_digest": (
                evidence.transition_preparation_route_digest
            ),
            "transition_preparation_deadline_at_epoch_seconds": (
                self.preparation_deadline_at
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

    def evaluate_decision(self, source=None, evidence=None, decision=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = self.make_decision_evidence(source) if evidence is None else evidence
        decision = self.make_decision(source, evidence) if decision is None else decision
        return verify_artifact(*self.artifact_args(source, evidence, decision, policy))
