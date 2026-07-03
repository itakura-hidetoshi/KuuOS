from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_governance_transition_preparation_v0_19 import (
    artifact_issues,
    make_package,
    make_step,
)
from runtime.kuuos_lifecycle_transition_preparation_types_v0_19 import (
    BLOCKED,
    PREPARED,
    REJECTED,
    package_digest,
    step_digest,
)
from tests.kuuos_lifecycle_transition_preparation_fixture_v0_19 import (
    LifecycleTransitionPreparationFixtureV019,
)


class LifecycleTransitionPreparationV019Tests(
    LifecycleTransitionPreparationFixtureV019
):
    def test_valid_package_is_ready_for_separate_approval(self) -> None:
        artifact = self.evaluate_preparation()
        self.assertEqual(artifact.status, PREPARED)
        self.assertTrue(artifact.source_transition_decision_approved)
        self.assertTrue(artifact.transition_preparation_record_issued)
        self.assertTrue(artifact.transition_preparation_completed)
        self.assertTrue(artifact.transition_package_prepared)
        self.assertTrue(artifact.ready_for_separate_transition_approval)
        self.assertTrue(artifact.transition_approval_required_next)
        self.assertFalse(artifact.lifecycle_transition_approved)
        self.assertFalse(artifact.lifecycle_transition_performed)

    def test_incomplete_substantive_plan_is_blocked_for_repreparation(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        for changes in (
            {"rollback_plan_complete": False},
            {"recovery_plan_complete": False},
            {"monitoring_plan_complete": False},
            {"evidence_capture_plan_complete": False},
            {"resource_reservations_valid": False},
            {"authority_continuity_planned": False},
            {"irreversible_steps_justified": False},
            {"all_steps_bounded": False},
            {"stop_conditions_complete": False},
            {"unresolved_anomaly_present": True},
            {"recovery_in_progress": True},
            {"institutional_hold_active": True},
            {"emergency_state_active": True},
        ):
            evidence = self.make_preparation_evidence(
                source, package, **changes
            )
            preparation = self.make_preparation(source, evidence)
            artifact = self.evaluate_preparation(
                source, package, evidence, preparation
            )
            self.assertEqual(artifact.status, BLOCKED)
            self.assertTrue(artifact.transition_preparation_record_issued)
            self.assertTrue(artifact.transition_preparation_completed)
            self.assertTrue(artifact.transition_preparation_blocked)
            self.assertTrue(artifact.transition_repreparation_required_next)
            self.assertFalse(artifact.transition_approval_required_next)
            self.assertFalse(artifact.lifecycle_transition_performed)

    def test_denied_source_decision_is_rejected(self) -> None:
        upstream_source = self.upstream.make_source()
        source_evidence = self.upstream.make_decision_evidence(
            upstream_source, decision_approved=False
        )
        source_decision = self.upstream.make_decision(
            upstream_source, source_evidence
        )
        source_record = self.upstream.evaluate_decision(
            upstream_source, source_evidence, source_decision
        )
        source_args = tuple(
            self.upstream.artifact_args(
                upstream_source, source_evidence, source_decision
            )[3:]
        )
        source = (
            source_decision,
            source_evidence,
            self.upstream.policy,
            source_record,
            source_args,
        )
        package = self.make_transition_package(source)
        evidence = self.make_preparation_evidence(source, package)
        preparation = self.make_preparation(source, evidence)
        artifact = self.evaluate_preparation(
            source, package, evidence, preparation
        )
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.transition_preparation_record_issued)

    def test_fresh_digest_tampered_source_is_rejected(self) -> None:
        source = self.make_source()
        record = self.refresh_source_record(source[3], reason="tampered")
        changed = (*source[:3], record, source[4])
        package = self.make_transition_package(changed)
        evidence = self.make_preparation_evidence(changed, package)
        preparation = self.make_preparation(changed, evidence)
        self.assertEqual(
            self.evaluate_preparation(
                changed, package, evidence, preparation
            ).status,
            REJECTED,
        )

    def test_package_state_rule_and_source_bindings_are_enforced(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        for changes in (
            {"transition_rule_digest": "u" * 64},
            {"source_transition_decision_id": "other-decision"},
        ):
            changed = self.refresh_package(package, **changes)
            evidence = self.make_preparation_evidence(source, changed)
            preparation = self.make_preparation(source, evidence)
            self.assertEqual(
                self.evaluate_preparation(
                    source, changed, evidence, preparation
                ).status,
                REJECTED,
            )

    def test_discontinuous_or_unordered_step_chain_is_rejected(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        second = replace(
            package.steps[1],
            expected_pre_state_digest="w" * 64,
            step_digest="",
        )
        second = replace(second, step_digest=step_digest(second))
        broken = self.refresh_package(package, steps=(package.steps[0], second))
        evidence = self.make_preparation_evidence(source, broken)
        preparation = self.make_preparation(source, evidence)
        self.assertEqual(
            self.evaluate_preparation(
                source, broken, evidence, preparation
            ).status,
            REJECTED,
        )
        reordered = self.refresh_package(
            package, steps=(package.steps[1], package.steps[0])
        )
        evidence = self.make_preparation_evidence(source, reordered)
        preparation = self.make_preparation(source, evidence)
        self.assertEqual(
            self.evaluate_preparation(
                source, reordered, evidence, preparation
            ).status,
            REJECTED,
        )

    def test_action_resource_and_step_bounds_are_enforced(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        first = replace(
            package.steps[0], action_kind="UNLISTED_ACTION", step_digest=""
        )
        first = replace(first, step_digest=step_digest(first))
        changed = self.refresh_package(package, steps=(first, package.steps[1]))
        evidence = self.make_preparation_evidence(source, changed)
        preparation = self.make_preparation(source, evidence)
        artifact = self.evaluate_preparation(
            source, changed, evidence, preparation
        )
        self.assertEqual(artifact.status, REJECTED)
        self.assertFalse(artifact.checks["action_kinds_allowed"])

    def test_preparer_approver_and_operator_separation_are_enforced(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        prior_actor = source[1].source_transition_reviewer_id
        cases = (
            {
                "transition_preparer_id": prior_actor,
            },
            {
                "transition_approver_id": self.transition_preparer_id,
            },
            {
                "future_transition_operator_id": self.transition_approver_id,
            },
            {
                "future_transition_operator_id": source[1].source_operator_id,
            },
        )
        for changes in cases:
            evidence = self.make_preparation_evidence(
                source, package, **changes
            )
            preparation = self.make_preparation(
                source,
                evidence,
                transition_preparer_id=changes.get(
                    "transition_preparer_id", self.transition_preparer_id
                ),
                transition_approver_id=changes.get(
                    "transition_approver_id", self.transition_approver_id
                ),
                future_transition_operator_id=changes.get(
                    "future_transition_operator_id",
                    self.future_transition_operator_id,
                ),
            )
            self.assertEqual(
                self.evaluate_preparation(
                    source, package, evidence, preparation
                ).status,
                REJECTED,
            )

    def test_preparer_organization_and_authority_are_enforced(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        for changes in (
            {
                "transition_preparer_organization_id": (
                    source[0].transition_decision_maker_organization_id
                )
            },
            {"preparer_mandate_verified": False},
            {"preparer_qualification_verified": False},
            {"preparer_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"preparation_ready": False},
        ):
            evidence = self.make_preparation_evidence(
                source, package, **changes
            )
            preparation = self.make_preparation(
                source,
                evidence,
                transition_preparer_organization_id=changes.get(
                    "transition_preparer_organization_id",
                    self.transition_preparer_organization_id,
                ),
            )
            self.assertEqual(
                self.evaluate_preparation(
                    source, package, evidence, preparation
                ).status,
                REJECTED,
            )

    def test_approval_route_and_time_bounds_are_enforced(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        evidence = self.make_preparation_evidence(source, package)
        bad_route = self.refresh_preparation(
            self.make_preparation(source, evidence),
            transition_approval_route_digest="z" * 64,
        )
        self.assertEqual(
            self.evaluate_preparation(
                source, package, evidence, bad_route
            ).status,
            REJECTED,
        )
        changed = self.refresh_evidence(
            evidence,
            transition_approval_deadline_at_epoch_seconds=(
                self.prepared_at + 121
            ),
        )
        preparation = self.make_preparation(
            source,
            changed,
            transition_approval_deadline_at_epoch_seconds=(
                changed.transition_approval_deadline_at_epoch_seconds
            ),
        )
        self.assertEqual(
            self.evaluate_preparation(
                source, package, changed, preparation
            ).status,
            REJECTED,
        )

    def test_determinism_record_integrity_and_effect_boundary(self) -> None:
        source = self.make_source()
        package = self.make_transition_package(source)
        evidence = self.make_preparation_evidence(source, package)
        preparation = self.make_preparation(source, evidence)
        left = self.evaluate_preparation(
            source, package, evidence, preparation
        )
        right = self.evaluate_preparation(
            source, package, evidence, preparation
        )
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "transition_preparation_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(source, evidence, preparation),
            ),
        )
        for value in (
            left.lifecycle_transition_approved,
            left.lifecycle_transition_started,
            left.lifecycle_transition_completed,
            left.lifecycle_transition_performed,
            left.authority_changed,
            left.quiescence_state_changed,
            left.terminal_state_changed,
            left.terminal_marker_written,
            left.resource_removed,
            left.external_operation_performed,
            left.repository_changed,
        ):
            self.assertFalse(value)
