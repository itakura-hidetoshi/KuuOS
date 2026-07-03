from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_governance_operation_approval_v0_13 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from tests.kuuos_lifecycle_authorization_decision_fixture_v0_12 import (
    LifecycleAuthorizationDecisionFixtureV012,
)


class LifecycleOperationApprovalFixtureV013(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleAuthorizationDecisionFixtureV012(methodName="runTest")
        self.upstream.setUp()
        source = self.make_source()
        source_decision = source[0]
        self.operation_approver_id = "lifecycle-operation-approver-001"
        self.operation_approver_organization_id = "lifecycle-operation-approval-organization"
        self.approval_requested_at = source_decision.completed_at_epoch_seconds + 20
        self.captured_at = self.approval_requested_at + 10
        self.completed_at = self.approval_requested_at + 20
        self.approval_expiry_at = self.completed_at + 40
        self.start_window_open_at = self.completed_at + 5
        self.operation_start_deadline_at = self.completed_at + 20
        self.policy = make_policy(
            "lifecycle-bounded-operation-approval-policy-v0-13",
            allowed_operation_approver_ids=(self.operation_approver_id,),
            allowed_operation_approver_organization_ids=(
                self.operation_approver_organization_id,
            ),
            allowed_future_operator_ids=(source_decision.future_operator_id,),
            allowed_target_resource_ids=("subject-runtime-state", "subject-intake-gate"),
            max_approval_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_approval_expiry_seconds=90,
            max_operation_start_delay_seconds=60,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        evidence = self.upstream.make_decision_evidence(source)
        decision = self.upstream.make_decision_submission(source, evidence)
        record = self.upstream.evaluate_decision(source, evidence, decision)
        source_args = (source[0], source[1], source[2], source[3], *source[4])
        return decision, evidence, self.upstream.policy, record, source_args

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(value, record_digest=source_record_digest(value))

    @staticmethod
    def refresh_evidence(evidence, **changes):
        value = replace(evidence, **changes, evidence_digest="")
        return replace(value, evidence_digest=evidence_digest(value))

    @staticmethod
    def refresh_approval(approval, **changes):
        value = replace(approval, **changes, approval_digest="")
        return replace(value, approval_digest=submission_digest(value))

    def make_approval_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-operation-approval-evidence-001",
            "operation_approval_id": "lifecycle-operation-approval-001",
            "operation_approver_id": self.operation_approver_id,
            "operation_approver_organization_id": self.operation_approver_organization_id,
            "approver_mandate_receipt_digest": "m" * 64,
            "approver_mandate_verified": True,
            "approver_qualification_receipt_digest": "q" * 64,
            "approver_qualification_verified": True,
            "approver_independence_declaration_digest": "i" * 64,
            "approver_independence_declared": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "quorum_receipt_digest": "u" * 64,
            "quorum_satisfied": True,
            "approval_rationale_digest": "r" * 64,
            "reasoned_approval_complete": True,
            "proportionality_review_digest": "p" * 64,
            "proportionality_satisfied": True,
            "execution_package_digest": "x" * 64,
            "execution_package_integrity_verified": True,
            "operator_acknowledgement_digest": "k" * 64,
            "operator_acknowledged": True,
            "resource_reservation_digest": "z" * 64,
            "resources_reserved": True,
            "approval_requested_at_epoch_seconds": self.approval_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
            "operation_approval_expiry_at_epoch_seconds": self.approval_expiry_at,
            "operation_start_window_open_at_epoch_seconds": self.start_window_open_at,
            "operation_start_deadline_at_epoch_seconds": self.operation_start_deadline_at,
        }
        values.update(overrides)
        return make_evidence(source[0], source[1], source[2], source[3], source[4], **values)

    def make_approval_submission(self, source, evidence, **overrides):
        values = {
            "operation_approval_id": "lifecycle-operation-approval-001",
            "operation_approver_id": self.operation_approver_id,
            "operation_approver_organization_id": self.operation_approver_organization_id,
            "approval_requested_at_epoch_seconds": self.approval_requested_at,
            "completed_at_epoch_seconds": self.completed_at,
            "source_decision": source[0],
            "source_record": source[3],
            "approval_evidence": evidence,
            "operation_approval_route_digest": evidence.operation_approval_route_digest,
            "operation_start_deadline_at_epoch_seconds": evidence.operation_start_deadline_at_epoch_seconds,
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, approval, policy=None):
        return (
            approval,
            evidence,
            self.policy if policy is None else policy,
            source[0], source[1], source[2], source[3], *source[4],
        )

    def evaluate_approval(self, source=None, evidence=None, approval=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = self.make_approval_evidence(source) if evidence is None else evidence
        approval = self.make_approval_submission(source, evidence) if approval is None else approval
        return verify_artifact(*self.artifact_args(source, evidence, approval, policy))
