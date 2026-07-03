from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    DENIED as SOURCE_DENIED,
)
from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import (
    APPROVED,
    DENIED,
    REJECTED,
)
from runtime.kuuos_lifecycle_governance_operation_approval_v0_13 import (
    artifact_issues,
    make_policy,
)
from tests.kuuos_lifecycle_operation_approval_fixture_v0_13 import (
    LifecycleOperationApprovalFixtureV013,
)


class LifecycleOperationApprovalV013Tests(
    LifecycleOperationApprovalFixtureV013
):
    def test_valid_input_produces_real_operation_approval(self) -> None:
        artifact = self.evaluate_approval()
        self.assertEqual(artifact.status, APPROVED)
        self.assertTrue(artifact.operation_approval_record_issued)
        self.assertTrue(artifact.operation_approval_made)
        self.assertTrue(artifact.operation_approved)
        self.assertTrue(artifact.operation_start_required_next)
        self.assertFalse(artifact.operation_started)
        self.assertFalse(artifact.repository_changed)

    def test_non_approved_source_is_rejected(self) -> None:
        source = self.make_source()
        record = self.refresh_source_record(
            source[3],
            status=SOURCE_DENIED,
            authorization_approved=False,
            authorization_denied=True,
            operation_approval_required_next=False,
            operation_approval_route_required_next=False,
        )
        changed = (*source[:3], record, source[4])
        evidence = self.make_approval_evidence(changed)
        approval = self.make_approval_submission(changed, evidence)
        self.assertEqual(
            self.evaluate_approval(changed, evidence, approval).status,
            REJECTED,
        )

    def test_fresh_digest_source_tamper_is_rejected(self) -> None:
        source = self.make_source()
        record = self.refresh_source_record(
            source[3],
            reason="fresh-digest-source-tamper",
        )
        changed = (*source[:3], record, source[4])
        evidence = self.make_approval_evidence(changed)
        approval = self.make_approval_submission(changed, evidence)
        self.assertEqual(
            self.evaluate_approval(changed, evidence, approval).status,
            REJECTED,
        )

    def test_source_record_binding_is_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(
            source,
            source_authorization_record_digest="b" * 64,
        )
        approval = self.make_approval_submission(source, evidence)
        self.assertEqual(
            self.evaluate_approval(source, evidence, approval).status,
            REJECTED,
        )

    def test_evidence_and_route_bindings_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval_submission(source, evidence)
        bad_evidence_digest = self.refresh_approval(
            approval,
            approval_evidence_digest="e" * 64,
        )
        bad_route = self.refresh_approval(
            approval,
            operation_approval_route_digest="o" * 63 + "x",
        )
        self.assertEqual(
            self.evaluate_approval(
                source, evidence, bad_evidence_digest
            ).status,
            REJECTED,
        )
        self.assertEqual(
            self.evaluate_approval(source, evidence, bad_route).status,
            REJECTED,
        )

    def test_approver_identity_policy_and_role_separation_are_enforced(self) -> None:
        source = self.make_source()
        for actor_id in (
            "unknown-operation-approver",
            source[0].requester_id,
            source[0].source_decision_reviewer_id,
            source[0].authorization_decision_maker_id,
            source[0].future_operator_id,
        ):
            evidence = self.make_approval_evidence(
                source,
                operation_approver_id=actor_id,
            )
            approval = self.make_approval_submission(
                source,
                evidence,
                operation_approver_id=actor_id,
            )
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                REJECTED,
            )

    def test_approver_organization_and_future_operator_policy_are_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(
            source,
            operation_approver_organization_id="unknown-organization",
        )
        approval = self.make_approval_submission(
            source,
            evidence,
            operation_approver_organization_id="unknown-organization",
        )
        self.assertEqual(
            self.evaluate_approval(source, evidence, approval).status,
            REJECTED,
        )
        operator_evidence = self.make_approval_evidence(
            source,
            future_operator_id="unknown-future-operator",
        )
        operator_approval = self.make_approval_submission(
            source,
            operator_evidence,
        )
        self.assertEqual(
            self.evaluate_approval(
                source,
                operator_evidence,
                operator_approval,
            ).status,
            REJECTED,
        )

    def test_objective_is_structurally_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval_submission(
            source,
            evidence,
            objective="START_OPERATION_NOW",
        )
        self.assertEqual(
            self.evaluate_approval(source, evidence, approval).status,
            REJECTED,
        )

    def test_mandate_qualification_independence_and_conflict_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"approver_mandate_verified": False},
            {"approver_qualification_verified": False},
            {"approver_independence_declared": False},
            {"material_conflict_present": True},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                DENIED,
            )

    def test_jurisdiction_quorum_reasoning_and_proportionality_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"jurisdiction_verified": False},
            {"quorum_satisfied": False},
            {"reasoned_approval_complete": False},
            {"proportionality_satisfied": False},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                DENIED,
            )

    def test_operator_package_and_reservation_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"operator_acknowledged": False},
            {"execution_package_integrity_verified": False},
            {"resources_reserved": False},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                DENIED,
            )

    def test_scope_and_irreversibility_tamper_is_rejected(self) -> None:
        source = self.make_source()
        for changes in (
            {"operation_scope_items": ()},
            {"protected_resource_ids": ("subject-runtime-state",)},
            {"irreversible_step_ids": ("irreversible-delete",)},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                REJECTED,
            )

    def test_target_resource_policy_failure_denies(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval_submission(source, evidence)
        restrictive = make_policy(
            "restrictive-operation-approval-policy-v0-13",
            allowed_operation_approver_ids=(self.operation_approver_id,),
            allowed_operation_approver_organization_ids=(
                self.operation_approver_organization_id,
            ),
            allowed_future_operator_ids=(source[0].future_operator_id,),
            allowed_target_resource_ids=("other-resource",),
            max_approval_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_approval_expiry_seconds=90,
            max_operation_start_delay_seconds=60,
            max_operation_window_seconds=120,
            max_scope_items=8,
        )
        self.assertEqual(
            self.evaluate_approval(
                source,
                evidence,
                approval,
                policy=restrictive,
            ).status,
            DENIED,
        )

    def test_readiness_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"rollback_plan_verified": False},
            {"recovery_route_verified": False},
            {"stop_conditions_complete": False},
            {"abort_channel_available": False},
            {"human_oversight_available": False},
            {"monitoring_plan_complete": False},
            {"evidence_capture_plan_complete": False},
            {"simulation_verified": False},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                DENIED,
            )

    def test_hold_emergency_protected_core_and_routes_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"protected_core_excluded": False},
            {"institutional_hold_active": True},
            {"emergency_state_active": True},
            {"appeal_route_available": False},
            {"dissent_route_available": False},
            {"minority_opinion_recorded": False},
        ):
            evidence = self.make_approval_evidence(source, **changes)
            approval = self.make_approval_submission(source, evidence)
            self.assertEqual(
                self.evaluate_approval(source, evidence, approval).status,
                DENIED,
            )

    def test_expired_source_authorization_is_rejected(self) -> None:
        source = self.make_source()
        late = source[1].authorization_decision_expiry_at_epoch_seconds + 1
        evidence = self.make_approval_evidence(
            source,
            approval_requested_at_epoch_seconds=late,
            captured_at_epoch_seconds=late + 1,
            completed_at_epoch_seconds=late + 2,
            operation_approval_expiry_at_epoch_seconds=late + 3,
            operation_start_window_open_at_epoch_seconds=late + 2,
            operation_start_deadline_at_epoch_seconds=late + 3,
        )
        approval = self.make_approval_submission(
            source,
            evidence,
            approval_requested_at_epoch_seconds=late,
            completed_at_epoch_seconds=late + 2,
            operation_start_deadline_at_epoch_seconds=late + 3,
        )
        self.assertEqual(
            self.evaluate_approval(source, evidence, approval).status,
            REJECTED,
        )

    def test_invalid_start_deadline_is_rejected(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(
            source,
            operation_start_deadline_at_epoch_seconds=self.completed_at,
        )
        approval = self.make_approval_submission(
            source,
            evidence,
            operation_start_deadline_at_epoch_seconds=self.completed_at,
        )
        self.assertEqual(
            self.evaluate_approval(source, evidence, approval).status,
            REJECTED,
        )

    def test_denied_does_not_advance(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(
            source,
            approver_mandate_verified=False,
        )
        approval = self.make_approval_submission(source, evidence)
        artifact = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(artifact.status, DENIED)
        self.assertTrue(artifact.operation_approval_record_issued)
        self.assertTrue(artifact.operation_approval_made)
        self.assertFalse(artifact.operation_approved)
        self.assertTrue(artifact.operation_denied)
        self.assertFalse(artifact.operation_start_required_next)

    def test_rejected_issues_no_approval_record(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval_submission(
            source,
            evidence,
            objective="INVALID",
        )
        artifact = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.operation_approval_record_issued)
        self.assertFalse(artifact.operation_approval_made)
        self.assertFalse(artifact.operation_approved)

    def test_determinism_and_record_integrity(self) -> None:
        source = self.make_source()
        evidence = self.make_approval_evidence(source)
        approval = self.make_approval_submission(source, evidence)
        left = self.evaluate_approval(source, evidence, approval)
        right = self.evaluate_approval(source, evidence, approval)
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "operation_approval_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(source, evidence, approval),
            ),
        )

    def test_approved_performs_no_execution_or_lifecycle_effect(self) -> None:
        artifact = self.evaluate_approval()
        self.assertTrue(artifact.operation_approved)
        self.assertFalse(artifact.operation_started)
        self.assertFalse(artifact.operation_completed)
        self.assertFalse(artifact.authority_changed)
        self.assertFalse(artifact.quiescence_state_changed)
        self.assertFalse(artifact.terminal_state_changed)
        self.assertFalse(artifact.terminal_marker_written)
        self.assertFalse(artifact.resource_removed)
        self.assertFalse(artifact.external_operation_performed)
        self.assertFalse(artifact.repository_changed)
