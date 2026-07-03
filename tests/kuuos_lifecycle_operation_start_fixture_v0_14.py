from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_governance_operation_start_v0_14 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from tests.kuuos_lifecycle_operation_approval_fixture_v0_13 import (
    LifecycleOperationApprovalFixtureV013,
)


class LifecycleOperationStartFixtureV014(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleOperationApprovalFixtureV013(methodName="runTest")
        self.upstream.setUp()
        source = self.make_source()
        source_approval, source_evidence = source[0], source[1]
        self.operator_id = source_approval.future_operator_id
        self.operator_organization_id = "lifecycle-operation-operator-organization"
        self.start_requested_at = max(
            source_approval.completed_at_epoch_seconds + 1,
            source_evidence.operation_start_window_open_at_epoch_seconds,
        )
        self.captured_at = self.start_requested_at + 1
        self.started_at = self.captured_at + 1
        self.completion_deadline_at = self.started_at + 30
        self.policy = make_policy(
            "lifecycle-bounded-operation-start-policy-v0-14",
            allowed_operator_ids=(self.operator_id,),
            allowed_operator_organization_ids=(self.operator_organization_id,),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_start_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        evidence = self.upstream.make_approval_evidence(source)
        approval = self.upstream.make_approval_submission(source, evidence)
        record = self.upstream.evaluate_approval(source, evidence, approval)
        source_args = (source[0], source[1], source[2], source[3], *source[4])
        return approval, evidence, self.upstream.policy, record, source_args

    @staticmethod
    def refresh_source_record(record, **changes):
        value = replace(record, **changes, record_digest="")
        return replace(value, record_digest=source_record_digest(value))

    @staticmethod
    def refresh_evidence(evidence, **changes):
        value = replace(evidence, **changes, evidence_digest="")
        return replace(value, evidence_digest=evidence_digest(value))

    @staticmethod
    def refresh_start(start, **changes):
        value = replace(start, **changes, start_digest="")
        return replace(value, start_digest=submission_digest(value))

    def make_start_evidence(self, source, **overrides):
        values = {
            "evidence_id": "lifecycle-operation-start-evidence-001",
            "operation_start_id": "lifecycle-operation-start-001",
            "operator_id": self.operator_id,
            "operator_organization_id": self.operator_organization_id,
            "operator_mandate_receipt_digest": "m" * 64,
            "operator_mandate_verified": True,
            "operator_qualification_receipt_digest": "q" * 64,
            "operator_qualification_verified": True,
            "operator_identity_confirmation_digest": "i" * 64,
            "operator_identity_confirmed": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "operator_readiness_receipt_digest": "r" * 64,
            "operator_ready": True,
            "start_authorization_acknowledgement_digest": "a" * 64,
            "start_authorization_acknowledged": True,
            "execution_package_recheck_digest": "x" * 64,
            "execution_package_integrity_reconfirmed": True,
            "resource_reservation_recheck_digest": "z" * 64,
            "resources_reserved_reconfirmed": True,
            "rollback_recheck_digest": "b" * 64,
            "rollback_readiness_reconfirmed": True,
            "recovery_recheck_digest": "v" * 64,
            "recovery_readiness_reconfirmed": True,
            "stop_condition_recheck_digest": "s" * 64,
            "stop_conditions_reconfirmed": True,
            "abort_channel_recheck_digest": "o" * 64,
            "abort_channel_reconfirmed": True,
            "human_oversight_recheck_digest": "h" * 64,
            "human_oversight_reconfirmed": True,
            "monitoring_recheck_digest": "n" * 64,
            "monitoring_reconfirmed": True,
            "evidence_capture_recheck_digest": "e" * 64,
            "evidence_capture_reconfirmed": True,
            "start_requested_at_epoch_seconds": self.start_requested_at,
            "captured_at_epoch_seconds": self.captured_at,
            "started_at_epoch_seconds": self.started_at,
            "operation_completion_deadline_at_epoch_seconds": self.completion_deadline_at,
            "protected_core_exclusion_reconfirmed": True,
            "institutional_hold_absence_reconfirmed": True,
            "emergency_state_absence_reconfirmed": True,
        }
        values.update(overrides)
        return make_evidence(
            source[0], source[1], source[2], source[3], source[4], **values
        )

    def make_start_submission(self, source, evidence, **overrides):
        values = {
            "operation_start_id": "lifecycle-operation-start-001",
            "operator_id": self.operator_id,
            "operator_organization_id": self.operator_organization_id,
            "start_requested_at_epoch_seconds": self.start_requested_at,
            "started_at_epoch_seconds": self.started_at,
            "source_approval": source[0],
            "source_record": source[3],
            "start_evidence": evidence,
            "operation_start_route_digest": evidence.operation_start_route_digest,
            "operation_completion_deadline_at_epoch_seconds": evidence.operation_completion_deadline_at_epoch_seconds,
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, start, policy=None):
        return (
            start,
            evidence,
            self.policy if policy is None else policy,
            source[0], source[1], source[2], source[3], *source[4],
        )

    def evaluate_start(self, source=None, evidence=None, start=None, policy=None):
        source = self.make_source() if source is None else source
        evidence = self.make_start_evidence(source) if evidence is None else evidence
        start = self.make_start_submission(source, evidence) if start is None else start
        return verify_artifact(*self.artifact_args(source, evidence, start, policy))
