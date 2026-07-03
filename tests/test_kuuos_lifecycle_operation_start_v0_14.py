from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_operation_approval_types_v0_13 import DENIED as SOURCE_DENIED
from runtime.kuuos_lifecycle_operation_start_types_v0_14 import DENIED, REJECTED, STARTED
from runtime.kuuos_lifecycle_governance_operation_start_v0_14 import artifact_issues, make_policy
from tests.kuuos_lifecycle_operation_start_fixture_v0_14 import LifecycleOperationStartFixtureV014


class LifecycleOperationStartV014Tests(LifecycleOperationStartFixtureV014):
    def test_valid_input_performs_real_operation_start(self) -> None:
        artifact = self.evaluate_start()
        self.assertEqual(artifact.status, STARTED)
        self.assertTrue(artifact.operation_start_record_issued)
        self.assertTrue(artifact.operation_start_decision_made)
        self.assertTrue(artifact.operation_started)
        self.assertTrue(artifact.operation_completion_required_next)
        self.assertFalse(artifact.operation_completed)
        self.assertFalse(artifact.repository_changed)

    def test_non_approved_or_fresh_digest_tampered_source_is_rejected(self) -> None:
        source = self.make_source()
        denied = self.refresh_source_record(
            source[3], status=SOURCE_DENIED, operation_approved=False,
            operation_denied=True, operation_start_required_next=False,
            operation_start_route_required_next=False,
        )
        tampered = self.refresh_source_record(source[3], reason="fresh-digest-tamper")
        for record in (denied, tampered):
            changed = (*source[:3], record, source[4])
            evidence = self.make_start_evidence(changed)
            start = self.make_start_submission(changed, evidence)
            self.assertEqual(self.evaluate_start(changed, evidence, start).status, REJECTED)

    def test_source_evidence_and_route_bindings_are_enforced(self) -> None:
        source = self.make_source()
        bad_source = self.make_start_evidence(
            source, source_operation_approval_record_digest="b" * 64
        )
        bad_source_start = self.make_start_submission(source, bad_source)
        self.assertEqual(
            self.evaluate_start(source, bad_source, bad_source_start).status, REJECTED
        )
        evidence = self.make_start_evidence(source)
        start = self.make_start_submission(source, evidence)
        for changed in (
            self.refresh_start(start, start_evidence_digest="e" * 64),
            self.refresh_start(start, operation_start_route_digest="r" * 64),
        ):
            self.assertEqual(self.evaluate_start(source, evidence, changed).status, REJECTED)

    def test_operator_identity_policy_and_role_separation_are_enforced(self) -> None:
        source = self.make_source()
        for operator_id in ("other-operator", source[0].operation_approver_id):
            evidence = self.make_start_evidence(source, operator_id=operator_id)
            start = self.make_start_submission(source, evidence, operator_id=operator_id)
            self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)
        evidence = self.make_start_evidence(
            source, operator_organization_id="unknown-organization"
        )
        start = self.make_start_submission(
            source, evidence, operator_organization_id="unknown-organization"
        )
        self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)

    def test_objective_is_structurally_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_start_evidence(source)
        start = self.make_start_submission(source, evidence, objective="INVALID")
        self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)

    def test_operator_authority_and_readiness_failures_deny(self) -> None:
        source = self.make_source()
        for changes in (
            {"operator_mandate_verified": False},
            {"operator_qualification_verified": False},
            {"operator_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"operator_ready": False},
            {"start_authorization_acknowledged": False},
        ):
            evidence = self.make_start_evidence(source, **changes)
            start = self.make_start_submission(source, evidence)
            self.assertEqual(self.evaluate_start(source, evidence, start).status, DENIED)

    def test_package_reservation_and_safety_rechecks_deny(self) -> None:
        source = self.make_source()
        names = (
            "execution_package_integrity_reconfirmed", "resources_reserved_reconfirmed",
            "rollback_readiness_reconfirmed", "recovery_readiness_reconfirmed",
            "stop_conditions_reconfirmed", "abort_channel_reconfirmed",
            "human_oversight_reconfirmed", "monitoring_reconfirmed",
            "evidence_capture_reconfirmed", "protected_core_exclusion_reconfirmed",
            "institutional_hold_absence_reconfirmed", "emergency_state_absence_reconfirmed",
        )
        for name in names:
            evidence = self.make_start_evidence(source, **{name: False})
            start = self.make_start_submission(source, evidence)
            self.assertEqual(self.evaluate_start(source, evidence, start).status, DENIED)

    def test_scope_and_irreversibility_changes_are_rejected(self) -> None:
        source = self.make_source()
        for changes in (
            {"operation_scope_items": ()},
            {"protected_resource_ids": ("subject-runtime-state",)},
            {"irreversible_step_ids": ("irreversible-step",)},
            {"institutional_hold_active": True},
            {"emergency_state_active": True},
            {"protected_core_excluded": False},
        ):
            evidence = self.make_start_evidence(source, **changes)
            start = self.make_start_submission(source, evidence)
            self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)

    def test_target_resource_policy_is_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_start_evidence(source)
        start = self.make_start_submission(source, evidence)
        restrictive = make_policy(
            "restrictive-operation-start-policy-v0-14",
            allowed_operator_ids=(self.operator_id,),
            allowed_operator_organization_ids=(self.operator_organization_id,),
            allowed_target_resource_ids=("other-resource",),
            max_start_delay_seconds=120, max_evidence_age_seconds=120,
            max_operation_window_seconds=120, max_scope_items=8,
        )
        self.assertEqual(
            self.evaluate_start(source, evidence, start, restrictive).status, REJECTED
        )

    def test_start_and_completion_time_boundaries_are_enforced(self) -> None:
        source = self.make_source()
        late = source[1].operation_start_deadline_at_epoch_seconds + 1
        evidence = self.make_start_evidence(
            source, start_requested_at_epoch_seconds=late,
            captured_at_epoch_seconds=late, started_at_epoch_seconds=late,
            operation_completion_deadline_at_epoch_seconds=late + 10,
        )
        start = self.make_start_submission(
            source, evidence, start_requested_at_epoch_seconds=late,
            started_at_epoch_seconds=late,
            operation_completion_deadline_at_epoch_seconds=late + 10,
        )
        self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)
        evidence = self.make_start_evidence(
            source, operation_completion_deadline_at_epoch_seconds=self.started_at
        )
        start = self.make_start_submission(
            source, evidence, operation_completion_deadline_at_epoch_seconds=self.started_at
        )
        self.assertEqual(self.evaluate_start(source, evidence, start).status, REJECTED)

    def test_denied_and_rejected_record_semantics(self) -> None:
        source = self.make_source()
        evidence = self.make_start_evidence(source, operator_ready=False)
        start = self.make_start_submission(source, evidence)
        denied = self.evaluate_start(source, evidence, start)
        self.assertEqual(denied.status, DENIED)
        self.assertTrue(denied.operation_start_record_issued)
        self.assertFalse(denied.operation_started)
        evidence = self.make_start_evidence(source)
        start = self.make_start_submission(source, evidence, objective="INVALID")
        rejected = self.evaluate_start(source, evidence, start)
        self.assertEqual(rejected.status, REJECTED)
        self.assertFalse(rejected.operation_start_record_issued)
        self.assertFalse(rejected.operation_started)

    def test_determinism_record_integrity_and_later_effect_boundary(self) -> None:
        source = self.make_source()
        evidence = self.make_start_evidence(source)
        start = self.make_start_submission(source, evidence)
        left = self.evaluate_start(source, evidence, start)
        right = self.evaluate_start(source, evidence, start)
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "operation_start_recomputation_mismatch",
            artifact_issues(tampered, *self.artifact_args(source, evidence, start)),
        )
        self.assertTrue(left.operation_started)
        for value in (
            left.operation_completed, left.authority_changed,
            left.quiescence_state_changed, left.terminal_state_changed,
            left.terminal_marker_written, left.resource_removed,
            left.external_operation_performed, left.repository_changed,
        ):
            self.assertFalse(value)
