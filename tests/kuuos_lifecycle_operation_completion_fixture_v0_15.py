from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    evidence_digest,
    submission_digest,
)
from runtime.kuuos_lifecycle_governance_operation_completion_v0_15 import (
    make_evidence,
    make_policy,
    make_submission,
    verify_artifact,
)
from tests.kuuos_lifecycle_operation_start_fixture_v0_14 import (
    LifecycleOperationStartFixtureV014,
)


class LifecycleOperationCompletionFixtureV015(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleOperationStartFixtureV014(
            methodName="runTest"
        )
        self.upstream.setUp()
        source = self.make_source()
        source_start = source[0]
        self.completion_reviewer_id = "lifecycle-operation-completion-reviewer"
        self.completion_reviewer_organization_id = (
            "lifecycle-operation-completion-review-organization"
        )
        self.completion_requested_at = (
            source_start.started_at_epoch_seconds + 1
        )
        self.captured_at = self.completion_requested_at + 1
        self.completed_at = self.captured_at + 1
        self.policy = make_policy(
            "lifecycle-bounded-operation-completion-policy-v0-15",
            allowed_completion_reviewer_ids=(
                self.completion_reviewer_id,
            ),
            allowed_completion_reviewer_organization_ids=(
                self.completion_reviewer_organization_id,
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_completion_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_scope_items=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        start_evidence = self.upstream.make_start_evidence(source)
        start = self.upstream.make_start_submission(
            source, start_evidence
        )
        record = self.upstream.evaluate_start(
            source, start_evidence, start
        )
        source_args = (
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )
        return (
            start,
            start_evidence,
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
    def refresh_completion(completion, **changes):
        value = replace(completion, **changes, completion_digest="")
        return replace(
            value, completion_digest=submission_digest(value)
        )

    def make_completion_evidence(self, source, **overrides):
        source_evidence = source[1]
        step_result_digests = {
            step_id: f"result-{index:02d}-" + "s" * 48
            for index, step_id in enumerate(
                source_evidence.reversible_step_ids
            )
        }
        values = {
            "evidence_id": "lifecycle-operation-completion-evidence-001",
            "operation_completion_id": (
                "lifecycle-operation-completion-001"
            ),
            "completion_reviewer_id": self.completion_reviewer_id,
            "completion_reviewer_organization_id": (
                self.completion_reviewer_organization_id
            ),
            "completion_reviewer_mandate_receipt_digest": "m" * 64,
            "completion_reviewer_mandate_verified": True,
            "completion_reviewer_qualification_receipt_digest": "q" * 64,
            "completion_reviewer_qualification_verified": True,
            "completion_reviewer_identity_confirmation_digest": "i" * 64,
            "completion_reviewer_identity_confirmed": True,
            "conflict_disclosure_digest": "c" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "completion_readiness_receipt_digest": "r" * 64,
            "completion_ready": True,
            "operation_execution_result_digest": "x" * 64,
            "operation_execution_finished": True,
            "step_result_digests": step_result_digests,
            "execution_result_integrity_verified": True,
            "all_scope_items_accounted": True,
            "all_reversible_steps_accounted": True,
            "target_resource_post_state_digest": "t" * 64,
            "target_post_state_verified": True,
            "protected_resource_integrity_digest": "p" * 64,
            "protected_resources_intact": True,
            "protected_core_integrity_digest": "k" * 64,
            "protected_core_intact": True,
            "resource_reservation_release_digest": "z" * 64,
            "resource_reservations_released": True,
            "monitoring_completion_digest": "n" * 64,
            "monitoring_completed": True,
            "evidence_capture_completion_digest": "e" * 64,
            "evidence_capture_completed": True,
            "unresolved_stop_condition_present": False,
            "abort_triggered": False,
            "rollback_pending": False,
            "recovery_pending": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "completion_requested_at_epoch_seconds": (
                self.completion_requested_at
            ),
            "captured_at_epoch_seconds": self.captured_at,
            "completed_at_epoch_seconds": self.completed_at,
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

    def make_completion_submission(
        self, source, evidence, **overrides
    ):
        values = {
            "operation_completion_id": (
                "lifecycle-operation-completion-001"
            ),
            "completion_reviewer_id": self.completion_reviewer_id,
            "completion_reviewer_organization_id": (
                self.completion_reviewer_organization_id
            ),
            "completion_requested_at_epoch_seconds": (
                self.completion_requested_at
            ),
            "completed_at_epoch_seconds": self.completed_at,
            "source_start": source[0],
            "source_record": source[3],
            "completion_evidence": evidence,
            "operation_completion_route_digest": (
                evidence.operation_completion_route_digest
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(
        self, source, evidence, completion, policy=None
    ):
        return (
            completion,
            evidence,
            self.policy if policy is None else policy,
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )

    def evaluate_completion(
        self,
        source=None,
        evidence=None,
        completion=None,
        policy=None,
    ):
        source = self.make_source() if source is None else source
        evidence = (
            self.make_completion_evidence(source)
            if evidence is None
            else evidence
        )
        completion = (
            self.make_completion_submission(source, evidence)
            if completion is None
            else completion
        )
        return verify_artifact(
            *self.artifact_args(
                source, evidence, completion, policy
            )
        )
