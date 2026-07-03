from __future__ import annotations

import unittest
from dataclasses import replace

from runtime.kuuos_lifecycle_governance_transition_preparation_v0_19 import (
    make_evidence,
    make_package,
    make_policy,
    make_step,
    make_submission,
    verify_artifact,
)
from runtime.kuuos_lifecycle_transition_decision_types_v0_18 import (
    record_digest as source_record_digest,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    evidence_digest,
    package_digest,
    submission_digest,
)
from tests.kuuos_lifecycle_transition_decision_fixture_v0_18 import (
    LifecycleTransitionDecisionFixtureV018,
)


class LifecycleTransitionPreparationFixtureV019(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = LifecycleTransitionDecisionFixtureV018(
            methodName="runTest"
        )
        self.upstream.setUp()
        source = self.make_source()
        self.transition_preparer_id = self.upstream.transition_preparer_id
        self.transition_preparer_organization_id = (
            "lifecycle-transition-preparation-organization"
        )
        self.transition_approver_id = "lifecycle-transition-approver"
        self.future_transition_operator_id = "lifecycle-transition-operator"
        self.preparation_requested_at = source[0].decided_at_epoch_seconds + 1
        self.captured_at = self.preparation_requested_at + 1
        self.prepared_at = self.captured_at + 1
        self.approval_deadline_at = self.prepared_at + 60
        self.execution_window_start_at = self.approval_deadline_at + 10
        self.execution_window_end_at = self.execution_window_start_at + 30
        self.package_expiry_at = self.execution_window_end_at + 10
        self.policy = make_policy(
            "lifecycle-bounded-transition-preparation-policy-v0-19",
            allowed_transition_preparer_ids=(self.transition_preparer_id,),
            allowed_transition_preparer_organization_ids=(
                self.transition_preparer_organization_id,
            ),
            allowed_transition_approver_ids=(self.transition_approver_id,),
            allowed_future_transition_operator_ids=(
                self.future_transition_operator_id,
            ),
            allowed_transition_kinds=(source[0].proposed_transition_kind,),
            allowed_action_kinds=("QUIESCE_INTAKE", "FREEZE_MUTATION"),
            allowed_target_resource_ids=(
                "subject-intake-gate",
                "subject-runtime-state",
            ),
            max_preparation_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_package_expiry_seconds=180,
            max_approval_delay_seconds=120,
            max_execution_window_seconds=60,
            max_steps=8,
        )

    def make_source(self):
        source = self.upstream.make_source()
        evidence = self.upstream.make_decision_evidence(source)
        decision = self.upstream.make_decision(source, evidence)
        record = self.upstream.evaluate_decision(source, evidence, decision)
        source_args = tuple(
            self.upstream.artifact_args(source, evidence, decision)[3:]
        )
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
    def refresh_preparation(preparation, **changes):
        value = replace(preparation, **changes, preparation_digest="")
        return replace(value, preparation_digest=submission_digest(value))

    @staticmethod
    def refresh_package(package, **changes):
        value = replace(package, **changes, package_digest="")
        return replace(value, package_digest=package_digest(value))

    def make_transition_package(self, source, **overrides):
        intermediate = "i" * 64
        steps = (
            make_step(
                step_id="transition-step-001",
                sequence_number=1,
                action_kind="QUIESCE_INTAKE",
                target_resource_id="subject-intake-gate",
                expected_pre_state_digest=(
                    source[3].expected_current_lifecycle_state_digest
                ),
                proposed_post_state_digest=intermediate,
                reversible=True,
                rollback_step_id="rollback-transition-step-001",
                evidence_capture_digest="e" * 64,
                stop_condition_digest="s" * 64,
            ),
            make_step(
                step_id="transition-step-002",
                sequence_number=2,
                action_kind="FREEZE_MUTATION",
                target_resource_id="subject-runtime-state",
                expected_pre_state_digest=intermediate,
                proposed_post_state_digest=(
                    source[3].proposed_target_lifecycle_state_digest
                ),
                reversible=False,
                rollback_step_id="",
                evidence_capture_digest="f" * 64,
                stop_condition_digest="t" * 64,
            ),
        )
        values = {
            "package_id": "lifecycle-transition-package-001",
            "source_transition_decision_id": source[0].transition_decision_id,
            "transition_kind": source[0].proposed_transition_kind,
            "expected_current_lifecycle_state_digest": (
                source[3].expected_current_lifecycle_state_digest
            ),
            "proposed_target_lifecycle_state_digest": (
                source[3].proposed_target_lifecycle_state_digest
            ),
            "transition_rule_digest": source[3].transition_rule_digest,
            "steps": steps,
            "rollback_plan_digest": "r" * 64,
            "recovery_plan_digest": "c" * 64,
            "monitoring_plan_digest": "m" * 64,
            "evidence_capture_plan_digest": "v" * 64,
            "resource_reservation_digest": "z" * 64,
            "authority_continuity_plan_digest": "a" * 64,
            "irreversible_exception_digest": "x" * 64,
            "aggregate_stop_conditions_digest": "o" * 64,
            "execution_window_start_epoch_seconds": (
                self.execution_window_start_at
            ),
            "execution_window_end_epoch_seconds": self.execution_window_end_at,
        }
        values.update(overrides)
        return make_package(**values)

    def make_preparation_evidence(self, source, package=None, **overrides):
        package = (
            self.make_transition_package(source) if package is None else package
        )
        values = {
            "evidence_id": "lifecycle-transition-preparation-evidence-001",
            "transition_preparation_id": "lifecycle-transition-preparation-001",
            "transition_preparer_id": self.transition_preparer_id,
            "transition_preparer_organization_id": (
                self.transition_preparer_organization_id
            ),
            "preparer_mandate_receipt_digest": "m" * 64,
            "preparer_mandate_verified": True,
            "preparer_qualification_receipt_digest": "q" * 64,
            "preparer_qualification_verified": True,
            "preparer_identity_confirmation_digest": "i" * 64,
            "preparer_identity_confirmed": True,
            "conflict_disclosure_digest": "d" * 64,
            "conflict_disclosure_complete": True,
            "material_conflict_present": False,
            "jurisdiction_receipt_digest": "j" * 64,
            "jurisdiction_verified": True,
            "preparation_readiness_receipt_digest": "p" * 64,
            "preparation_ready": True,
            "transition_approver_id": self.transition_approver_id,
            "future_transition_operator_id": self.future_transition_operator_id,
            "rollback_plan_complete": True,
            "recovery_plan_complete": True,
            "monitoring_plan_complete": True,
            "evidence_capture_plan_complete": True,
            "resource_reservations_valid": True,
            "authority_continuity_planned": True,
            "irreversible_steps_justified": True,
            "all_steps_bounded": True,
            "stop_conditions_complete": True,
            "unresolved_anomaly_present": False,
            "recovery_in_progress": False,
            "institutional_hold_active": False,
            "emergency_state_active": False,
            "external_operation_performed": False,
            "repository_changed": False,
            "preparation_requested_at_epoch_seconds": (
                self.preparation_requested_at
            ),
            "captured_at_epoch_seconds": self.captured_at,
            "prepared_at_epoch_seconds": self.prepared_at,
            "package_expiry_at_epoch_seconds": self.package_expiry_at,
            "transition_approval_deadline_at_epoch_seconds": (
                self.approval_deadline_at
            ),
        }
        values.update(overrides)
        return make_evidence(
            source[0],
            source[1],
            source[2],
            source[3],
            source[4],
            transition_package=package,
            **values,
        )

    def make_preparation(self, source, evidence, **overrides):
        values = {
            "transition_preparation_id": "lifecycle-transition-preparation-001",
            "transition_preparer_id": self.transition_preparer_id,
            "transition_preparer_organization_id": (
                self.transition_preparer_organization_id
            ),
            "preparation_requested_at_epoch_seconds": (
                self.preparation_requested_at
            ),
            "prepared_at_epoch_seconds": self.prepared_at,
            "package_expiry_at_epoch_seconds": self.package_expiry_at,
            "source_decision": source[0],
            "source_record": source[3],
            "preparation_evidence": evidence,
            "transition_approver_id": self.transition_approver_id,
            "future_transition_operator_id": self.future_transition_operator_id,
            "transition_approval_route_digest": (
                evidence.transition_approval_route_digest
            ),
            "transition_approval_deadline_at_epoch_seconds": (
                self.approval_deadline_at
            ),
        }
        values.update(overrides)
        return make_submission(**values)

    def artifact_args(self, source, evidence, preparation, policy=None):
        return (
            preparation,
            evidence,
            self.policy if policy is None else policy,
            source[0],
            source[1],
            source[2],
            source[3],
            *source[4],
        )

    def evaluate_preparation(
        self,
        source=None,
        package=None,
        evidence=None,
        preparation=None,
        policy=None,
    ):
        source = self.make_source() if source is None else source
        package = (
            self.make_transition_package(source) if package is None else package
        )
        evidence = (
            self.make_preparation_evidence(source, package)
            if evidence is None
            else evidence
        )
        preparation = (
            self.make_preparation(source, evidence)
            if preparation is None
            else preparation
        )
        return verify_artifact(
            *self.artifact_args(source, evidence, preparation, policy)
        )
