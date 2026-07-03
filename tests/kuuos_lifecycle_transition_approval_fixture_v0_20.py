from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_governance_transition_approval_v0_20 import (
    Rec,
    evidence_digest,
    make_evidence,
    make_policy,
    make_submission,
    submission_digest,
    verify_artifact,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    record_digest as source_record_digest,
)
from tests.kuuos_lifecycle_transition_preparation_fixture_v0_19 import (
    LifecycleTransitionPreparationFixtureV019,
)


class LifecycleTransitionApprovalFixtureV020(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleTransitionPreparationFixtureV019(methodName="runTest")
        self.upstream.setUp()
        source = self.make_source()
        self.transition_approver_id = source[0].transition_approver_id
        self.transition_approver_organization_id = "lifecycle-transition-approval-organization"
        self.future_transition_operator_id = source[0].future_transition_operator_id
        self.approval_requested_at = source[0].prepared_at_epoch_seconds + 1
        self.captured_at = self.approval_requested_at + 1
        self.approved_at = self.captured_at + 1
        self.start_authorization_deadline_at = self.approved_at + 60
        self.policy = make_policy(
            "lifecycle-bounded-transition-approval-policy-v0-20",
            allowed_transition_approver_ids=(self.transition_approver_id,),
            allowed_transition_approver_organization_ids=(self.transition_approver_organization_id,),
            allowed_future_transition_operator_ids=(self.future_transition_operator_id,),
            max_approval_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_start_authorization_delay_seconds=120,
        )

    def make_source(self):
        source = self.upstream.make_source()
        package = self.upstream.make_transition_package(source)
        evidence = self.upstream.make_preparation_evidence(source, package)
        preparation = self.upstream.make_preparation(source, evidence)
        record = self.upstream.evaluate_preparation(source, package, evidence, preparation)
        source_args = tuple(self.upstream.artifact_args(source, evidence, preparation)[3:])
        return preparation, evidence, self.upstream.policy, record, source_args

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(value, record_digest=source_record_digest(value))

    @staticmethod
    def refresh_evidence(evidence, **changes):
        payload = evidence.to_dict()
        payload.update(changes)
        payload["evidence_digest"] = ""
        value = Rec(**payload)
        value.evidence_digest = evidence_digest(value)
        return value

    @staticmethod
    def refresh_approval(approval, **changes):
        payload = approval.to_dict()
        payload.update(changes)
        payload["approval_digest"] = ""
        value = Rec(**payload)
        value.approval_digest = submission_digest(value)
        return value

    def make_approval_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-transition-approval-evidence-001",
            "transition_approval_id": "lifecycle-transition-approval-001",
            "transition_approver_id": self.transition_approver_id,
            "transition_approver_organization_id": self.transition_approver_organization_id,
            "approver_mandate_receipt_digest": "m" * 64,
            "approver_mandate_verified": True,
            "approver_authority_receipt_digest": "a" * 64,
            "approver_authority_verified": True,
            "approver_identity_confirmation_digest": "i" * 64,
            "approver_identity_confirmed": True,
            "conflict_disclosure_digest": "d" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "package_freshness_receipt_digest": "p" * 64,
            "package_fresh": True,
            "current_state_freshness_receipt_digest": "c" * 64,
            "current_state_not_stale": True,
            "target_state_validity_receipt_digest": "t" * 64,
            "target_state_still_valid": True,
            "transition_approval_granted": True,
            "denial_reason_digest": "",
            "unresolved_anomaly_present": False,
            "recovery_in_progress": False,
            "institutional_hold_active": False,
            "emergency_state_active": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "approval_requested_at_epoch_seconds": self.approval_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "approved_at_epoch_seconds": self.approved_at,
            "transition_start_authorization_deadline_at_epoch_seconds": self.start_authorization_deadline_at,
        }
        values.update(overrides)
        return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)

    def make_approval(self, source, evidence, **overrides):
        values = {
            "transition_approval_id": "lifecycle-transition-approval-001",
            "transition_approver_id": self.transition_approver_id,
            "transition_approver_organization_id": self.transition_approver_organization_id,
            "approval_requested_at_epoch_seconds": self.approval_requested_at,
            "approved_at_epoch_seconds": self.approved_at,
            "source_preparation": source[0],
            "source_record": source[3],
            "approval_evidence": evidence,
            "transition_start_authorization_route_digest": evidence.transition_start_authorization_route_digest,
            "transition_start_authorization_deadline_at_epoch_seconds": self.start_authorization_deadline_at,
            "transition_approval_granted": evidence.transition_approval_granted,
            "denial_reason_digest": evidence.denial_reason_digest,
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, approval, policy=None):
        return (approval, evidence, self.policy if policy is None else policy, source[0], source[1], source[2], source[3], *source[4])

    def evaluate_approval(self, source=None, evidence=None, approval=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = self.make_approval_evidence(source) if evidence is None else evidence
        approval = self.make_approval(source, evidence) if approval is None else approval
        return verify_artifact(*self.artifact_args(source, evidence, approval, policy))
