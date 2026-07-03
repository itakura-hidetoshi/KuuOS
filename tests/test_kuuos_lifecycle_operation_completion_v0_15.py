from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_operation_start_types_v0_14 import (
    DENIED as SOURCE_DENIED,
)
from runtime.kuuos_lifecycle_operation_completion_types_v0_15 import (
    COMPLETED,
    DENIED,
    REJECTED,
)
from runtime.kuuos_lifecycle_governance_operation_completion_v0_15 import (
    artifact_issues,
    make_policy,
)
from tests.kuuos_lifecycle_operation_completion_fixture_v0_15 import (
    LifecycleOperationCompletionFixtureV015,
)


class LifecycleOperationCompletionV015Tests(
    LifecycleOperationCompletionFixtureV015
):
    def test_valid_input_completes_started_operation(self) -> None:
        artifact = self.evaluate_completion()
        self.assertEqual(artifact.status, COMPLETED)
        self.assertTrue(artifact.operation_started)
        self.assertTrue(artifact.operation_completion_record_issued)
        self.assertTrue(artifact.operation_completion_decision_made)
        self.assertTrue(artifact.operation_completed)
        self.assertTrue(artifact.post_operation_review_required_next)
        self.assertFalse(artifact.operation_recovery_required_next)
        self.assertFalse(artifact.authority_changed)
        self.assertFalse(artifact.repository_changed)

    def test_non_started_or_fresh_digest_tampered_source_is_rejected(
        self,
    ) -> None:
        source = self.make_source()
        denied = self.refresh_source_record(
            source[3],
            status=SOURCE_DENIED,
            operation_started=False,
            operation_start_denied=True,
            operation_completion_required_next=False,
            operation_completion_route_required_next=False,
        )
        tampered = self.refresh_source_record(
            source[3], reason="fresh-digest-tamper"
        )
        for record in (denied, tampered):
            changed = (*source[:3], record, source[4])
            evidence = self.make_completion_evidence(changed)
            completion = self.make_completion_submission(
                changed, evidence
            )
            self.assertEqual(
                self.evaluate_completion(
                    changed, evidence, completion
                ).status,
                REJECTED,
            )

    def test_source_evidence_and_route_bindings_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        bad_source = self.make_completion_evidence(
            source,
            source_operation_start_record_digest="b" * 64,
        )
        bad_source_completion = self.make_completion_submission(
            source, bad_source
        )
        self.assertEqual(
            self.evaluate_completion(
                source, bad_source, bad_source_completion
            ).status,
            REJECTED,
        )
        evidence = self.make_completion_evidence(source)
        completion = self.make_completion_submission(
            source, evidence
        )
        for changed in (
            self.refresh_completion(
                completion,
                completion_evidence_digest="e" * 64,
            ),
            self.refresh_completion(
                completion,
                operation_completion_route_digest="r" * 64,
            ),
        ):
            self.assertEqual(
                self.evaluate_completion(
                    source, evidence, changed
                ).status,
                REJECTED,
            )

    def test_completion_reviewer_policy_and_role_separation_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        for reviewer_id in (
            "other-reviewer",
            source[0].operator_id,
            source[0].source_operation_approver_id,
        ):
            evidence = self.make_completion_evidence(
                source, completion_reviewer_id=reviewer_id
            )
            completion = self.make_completion_submission(
                source,
                evidence,
                completion_reviewer_id=reviewer_id,
            )
            self.assertEqual(
                self.evaluate_completion(
                    source, evidence, completion
                ).status,
                REJECTED,
            )
        evidence = self.make_completion_evidence(
            source,
            completion_reviewer_organization_id=(
                "unknown-organization"
            ),
        )
        completion = self.make_completion_submission(
            source,
            evidence,
            completion_reviewer_organization_id=(
                "unknown-organization"
            ),
        )
        self.assertEqual(
            self.evaluate_completion(
                source, evidence, completion
            ).status,
            REJECTED,
        )

    def test_objective_is_structurally_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_completion_evidence(source)
        completion = self.make_completion_submission(
            source, evidence, objective="INVALID"
        )
        self.assertEqual(
            self.evaluate_completion(
                source, evidence, completion
            ).status,
            REJECTED,
        )

    def test_reviewer_authority_and_readiness_failures_deny(
        self,
    ) -> None:
        source = self.make_source()
        for changes in (
            {"completion_reviewer_mandate_verified": False},
            {"completion_reviewer_qualification_verified": False},
            {"completion_reviewer_identity_confirmed": False},
            {"material_conflict_present": True},
            {"jurisdiction_verified": False},
            {"completion_ready": False},
        ):
            evidence = self.make_completion_evidence(
                source, **changes
            )
            completion = self.make_completion_submission(
                source, evidence
            )
            self.assertEqual(
                self.evaluate_completion(
                    source, evidence, completion
                ).status,
                DENIED,
            )

    def test_completion_and_safety_failures_deny_and_route_recovery(
        self,
    ) -> None:
        source = self.make_source()
        changes_list = (
            {"operation_execution_finished": False},
            {"execution_result_integrity_verified": False},
            {"all_scope_items_accounted": False},
            {"all_reversible_steps_accounted": False},
            {"target_post_state_verified": False},
            {"protected_resources_intact": False},
            {"protected_core_intact": False},
            {"resource_reservations_released": False},
            {"monitoring_completed": False},
            {"evidence_capture_completed": False},
            {"unresolved_stop_condition_present": True},
            {"abort_triggered": True},
            {"rollback_pending": True},
            {"recovery_pending": True},
        )
        for changes in changes_list:
            evidence = self.make_completion_evidence(
                source, **changes
            )
            completion = self.make_completion_submission(
                source, evidence
            )
            artifact = self.evaluate_completion(
                source, evidence, completion
            )
            self.assertEqual(artifact.status, DENIED)
            self.assertTrue(
                artifact.operation_recovery_required_next
            )
            self.assertFalse(artifact.operation_completed)

    def test_scope_result_and_effect_changes_are_rejected(self) -> None:
        source = self.make_source()
        for changes in (
            {"operation_scope_items": ()},
            {
                "protected_resource_ids": (
                    "subject-runtime-state",
                )
            },
            {"irreversible_step_ids": ("irreversible-step",)},
            {"step_result_digests": {"unknown-step": "u" * 64}},
            {"external_operation_performed": True},
            {"repository_changed": True},
        ):
            evidence = self.make_completion_evidence(
                source, **changes
            )
            completion = self.make_completion_submission(
                source, evidence
            )
            self.assertEqual(
                self.evaluate_completion(
                    source, evidence, completion
                ).status,
                REJECTED,
            )

    def test_target_resource_policy_is_enforced(self) -> None:
        source = self.make_source()
        evidence = self.make_completion_evidence(source)
        completion = self.make_completion_submission(
            source, evidence
        )
        restrictive = make_policy(
            "restrictive-operation-completion-policy-v0-15",
            allowed_completion_reviewer_ids=(
                self.completion_reviewer_id,
            ),
            allowed_completion_reviewer_organization_ids=(
                self.completion_reviewer_organization_id,
            ),
            allowed_target_resource_ids=("other-resource",),
            max_completion_delay_seconds=120,
            max_evidence_age_seconds=120,
            max_scope_items=8,
        )
        self.assertEqual(
            self.evaluate_completion(
                source, evidence, completion, restrictive
            ).status,
            REJECTED,
        )

    def test_completion_deadline_and_evidence_freshness_are_enforced(
        self,
    ) -> None:
        source = self.make_source()
        late = (
            source[0].operation_completion_deadline_at_epoch_seconds
            + 1
        )
        evidence = self.make_completion_evidence(
            source,
            completion_requested_at_epoch_seconds=late,
            captured_at_epoch_seconds=late,
            completed_at_epoch_seconds=late,
        )
        completion = self.make_completion_submission(
            source,
            evidence,
            completion_requested_at_epoch_seconds=late,
            completed_at_epoch_seconds=late,
        )
        self.assertEqual(
            self.evaluate_completion(
                source, evidence, completion
            ).status,
            REJECTED,
        )
        stale_captured = (
            self.completed_at
            - self.policy.max_evidence_age_seconds
            - 1
        )
        evidence = self.make_completion_evidence(
            source,
            completion_requested_at_epoch_seconds=(
                stale_captured
            ),
            captured_at_epoch_seconds=stale_captured,
        )
        completion = self.make_completion_submission(
            source,
            evidence,
            completion_requested_at_epoch_seconds=(
                stale_captured
            ),
        )
        self.assertEqual(
            self.evaluate_completion(
                source, evidence, completion
            ).status,
            REJECTED,
        )

    def test_denied_and_rejected_record_semantics(self) -> None:
        source = self.make_source()
        evidence = self.make_completion_evidence(
            source, completion_ready=False
        )
        completion = self.make_completion_submission(
            source, evidence
        )
        denied = self.evaluate_completion(
            source, evidence, completion
        )
        self.assertEqual(denied.status, DENIED)
        self.assertTrue(
            denied.operation_completion_record_issued
        )
        self.assertFalse(denied.operation_completed)
        self.assertTrue(
            denied.operation_recovery_required_next
        )
        evidence = self.make_completion_evidence(source)
        completion = self.make_completion_submission(
            source, evidence, objective="INVALID"
        )
        rejected = self.evaluate_completion(
            source, evidence, completion
        )
        self.assertEqual(rejected.status, REJECTED)
        self.assertFalse(
            rejected.operation_completion_record_issued
        )
        self.assertFalse(rejected.operation_completed)

    def test_determinism_record_integrity_and_later_effect_boundary(
        self,
    ) -> None:
        source = self.make_source()
        evidence = self.make_completion_evidence(source)
        completion = self.make_completion_submission(
            source, evidence
        )
        left = self.evaluate_completion(
            source, evidence, completion
        )
        right = self.evaluate_completion(
            source, evidence, completion
        )
        self.assertEqual(left.to_dict(), right.to_dict())
        tampered = replace(left, reason="tampered")
        self.assertIn(
            "operation_completion_recomputation_mismatch",
            artifact_issues(
                tampered,
                *self.artifact_args(
                    source, evidence, completion
                ),
            ),
        )
        self.assertTrue(left.operation_completed)
        for value in (
            left.authority_changed,
            left.quiescence_state_changed,
            left.terminal_state_changed,
            left.terminal_marker_written,
            left.resource_removed,
            left.external_operation_performed,
            left.repository_changed,
        ):
            self.assertFalse(value)
