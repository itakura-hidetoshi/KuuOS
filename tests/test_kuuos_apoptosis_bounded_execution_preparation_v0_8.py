from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_apoptosis_independent_authorization_types_v0_7 import (
    apoptosis_independent_authorization_record_digest,
)
from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    BOUNDED_EXECUTION_PREPARATION_BLOCKED,
    BOUNDED_EXECUTION_PREPARATION_READY,
    BOUNDED_EXECUTION_PREPARATION_REJECTED,
    apoptosis_bounded_execution_preparation_evidence_digest,
    apoptosis_bounded_execution_preparation_policy_digest,
    apoptosis_bounded_execution_preparation_record_digest,
    apoptosis_bounded_execution_preparation_request_digest,
)
from runtime.kuuos_apoptosis_bounded_execution_preparation_v0_8 import (
    apoptosis_bounded_execution_preparation_record_issues,
    build_apoptosis_bounded_execution_preparation_evidence,
    build_apoptosis_bounded_execution_preparation_policy,
    build_apoptosis_bounded_execution_preparation_request,
    prepare_apoptosis_bounded_execution,
)
from tests.test_kuuos_apoptosis_independent_authorization_v0_7 import (
    ApoptosisIndependentAuthorizationV07Tests,
)


class ApoptosisBoundedExecutionPreparationV08Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = ApoptosisIndependentAuthorizationV07Tests(
            methodName="runTest"
        )
        self.upstream.setUp()
        self.preparation_requested_at = self.upstream.authorization_completed_at + 20
        self.preparation_evidence_at = self.preparation_requested_at + 20
        self.preparation_completed_at = self.preparation_requested_at + 40
        self.package_expiry_at = self.preparation_completed_at + 600
        self.policy = build_apoptosis_bounded_execution_preparation_policy(
            "bounded-execution-preparation-policy-v0-8",
            allowed_preparer_ids=(
                "bounded-preparer",
                "candidate-module",
                "dependency-reviewer",
                "authority-reviewer",
                "responsible-authority",
                "quiescence-reviewer",
                "quiescence-evidence-producer",
                "external-reviewer",
                "future-authorization-authority",
                "future-execution-authority",
            ),
            allowed_preparer_organization_ids=(
                "bounded-preparation-organization",
            ),
            allowed_target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            max_preparation_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_execution_window_seconds=120,
            max_scope_items=8,
        )

    def authorization_bundle(
        self,
        *,
        authorization_overrides: dict | None = None,
        rejected_source: bool = False,
    ):
        external_bundle = self.upstream.source_bundle(
            authority_blocked=rejected_source
        )
        authorization_evidence = self.upstream.evidence(
            external_bundle,
            **(authorization_overrides or {}),
        )
        authorization_request = self.upstream.request(
            external_bundle,
            authorization_evidence,
        )
        authorization_record = self.upstream.execute(
            external_bundle,
            authorization_evidence,
            authorization_request,
        )
        return (
            external_bundle,
            authorization_evidence,
            authorization_request,
            authorization_record,
        )

    def evidence(self, bundle, **overrides):
        (
            external_bundle,
            authorization_evidence,
            authorization_request,
            authorization_record,
        ) = bundle
        (
            quiescence_bundle,
            external_evidence,
            external_request,
            external_record,
        ) = external_bundle
        source, quiescence_evidence, quiescence_request, quiescence_record = (
            quiescence_bundle
        )
        values = dict(
            evidence_id="bounded-execution-preparation-evidence-001",
            preparation_id="bounded-execution-preparation-001",
            preparer_id="bounded-preparer",
            preparer_organization_id="bounded-preparation-organization",
            authorization_authority_id=authorization_record.authority_id,
            future_execution_authority_id="future-execution-authority",
            preparer_qualification_receipt_digest="q" * 64,
            preparer_qualification_verified=True,
            preparer_independence_declaration_digest="i" * 64,
            preparer_independence_declared=True,
            conflict_of_interest_disclosure_digest="c" * 64,
            conflict_disclosure_complete=True,
            material_conflict_present=False,
            execution_scope_digest="s" * 64,
            execution_scope_items=(
                "checkpoint-subject-state",
                "close-subject-intake",
            ),
            target_resource_ids=(
                "subject-runtime-state",
                "subject-intake-gate",
            ),
            protected_resource_ids=("protected-core",),
            reversible_step_ids=(
                "checkpoint-subject-state",
                "close-subject-intake",
            ),
            irreversible_step_ids=(),
            rollback_plan_digest="r" * 64,
            rollback_plan_verified=True,
            recovery_route_digest="v" * 64,
            recovery_route_verified=True,
            stop_condition_digest="t" * 64,
            stop_conditions_complete=True,
            abort_channel_digest="a" * 64,
            abort_channel_available=True,
            human_oversight_digest="h" * 64,
            human_oversight_available=True,
            monitoring_plan_digest="m" * 64,
            monitoring_plan_complete=True,
            evidence_capture_plan_digest="e" * 64,
            evidence_capture_plan_complete=True,
            simulation_receipt_digest="z" * 64,
            simulation_verified=True,
            requested_at_epoch_seconds=self.preparation_requested_at,
            captured_at_epoch_seconds=self.preparation_evidence_at,
            completed_at_epoch_seconds=self.preparation_completed_at,
            package_expiry_at_epoch_seconds=self.package_expiry_at,
            execution_window_seconds=60,
            protected_core_excluded=True,
            institutional_hold_active=False,
            emergency_state_active=False,
            authorization_request=authorization_request,
            authorization_evidence=authorization_evidence,
            authorization_policy=self.upstream.authorization_policy,
            authorization_record=authorization_record,
            external_request=external_request,
            external_evidence=external_evidence,
            external_policy=self.upstream.upstream.external_policy,
            external_record=external_record,
            quiescence_request=quiescence_request,
            quiescence_evidence=quiescence_evidence,
            quiescence_policy=self.upstream.upstream.upstream.quiescence_policy,
            quiescence_record=quiescence_record,
            authority_request=source[8],
            authority_evidence=source[7],
            authority_policy=self.upstream.upstream.upstream.authority_policy,
            authority_record=source[9],
            dependency_request=source[5],
            dependency_evidence=source[4],
            dependency_policy=self.upstream.upstream.upstream.dependency_policy,
            dependency_record=source[6],
            observation_input=source[0],
            observation_policy=self.upstream.upstream.upstream.observation_policy,
            observation_record=source[1],
            candidate_request=source[2],
            candidate_policy=self.upstream.upstream.upstream.candidate_policy,
            candidate_record=source[3],
        )
        values.update(overrides)
        return build_apoptosis_bounded_execution_preparation_evidence(**values)

    def request(self, bundle, evidence, **overrides):
        values = dict(
            preparation_id="bounded-execution-preparation-001",
            preparer_id="bounded-preparer",
            preparer_organization_id="bounded-preparation-organization",
            requested_at_epoch_seconds=self.preparation_requested_at,
            completed_at_epoch_seconds=self.preparation_completed_at,
            authorization_record=bundle[3],
            preparation_evidence=evidence,
            future_execution_authority_id="future-execution-authority",
        )
        values.update(overrides)
        return build_apoptosis_bounded_execution_preparation_request(**values)

    def execution_args(self, bundle, evidence, request, policy=None):
        (
            external_bundle,
            authorization_evidence,
            authorization_request,
            authorization_record,
        ) = bundle
        (
            quiescence_bundle,
            external_evidence,
            external_request,
            external_record,
        ) = external_bundle
        source, quiescence_evidence, quiescence_request, quiescence_record = (
            quiescence_bundle
        )
        return (
            request,
            evidence,
            self.policy if policy is None else policy,
            authorization_request,
            authorization_evidence,
            self.upstream.authorization_policy,
            authorization_record,
            external_request,
            external_evidence,
            self.upstream.upstream.external_policy,
            external_record,
            quiescence_request,
            quiescence_evidence,
            self.upstream.upstream.upstream.quiescence_policy,
            quiescence_record,
            source[8],
            source[7],
            self.upstream.upstream.upstream.authority_policy,
            source[9],
            source[5],
            source[4],
            self.upstream.upstream.upstream.dependency_policy,
            source[6],
            source[0],
            self.upstream.upstream.upstream.observation_policy,
            source[1],
            source[2],
            self.upstream.upstream.upstream.candidate_policy,
            source[3],
        )

    def execute(self, bundle=None, evidence=None, request=None, policy=None):
        bundle = self.authorization_bundle() if bundle is None else bundle
        evidence = self.evidence(bundle) if evidence is None else evidence
        request = self.request(bundle, evidence) if request is None else request
        return prepare_apoptosis_bounded_execution(
            *self.execution_args(bundle, evidence, request, policy)
        )

    def record_issues(self, bundle, evidence, request, record, policy=None):
        return apoptosis_bounded_execution_preparation_record_issues(
            record,
            *self.execution_args(bundle, evidence, request, policy),
        )

    def test_valid_package_is_ready_for_execution_review(self) -> None:
        record = self.execute()
        self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_READY)
        self.assertTrue(record.preparation_record_issued)
        self.assertTrue(record.bounded_execution_package_prepared)
        self.assertTrue(record.ready_for_execution_review)
        self.assertTrue(record.execution_review_required_next)
        self.assertFalse(record.execution_request_issued)
        self.assertFalse(record.execution_decision_made)

    def test_denied_and_rejected_authorizations_are_rejected(self) -> None:
        denied = self.authorization_bundle(
            authorization_overrides={"quorum_satisfied": False}
        )
        rejected = self.authorization_bundle(rejected_source=True)
        for bundle in (denied, rejected):
            with self.subTest(status=bundle[3].status):
                record = self.execute(bundle)
                self.assertEqual(
                    record.status,
                    BOUNDED_EXECUTION_PREPARATION_REJECTED,
                )
                self.assertFalse(record.source_authorization_approved)

    def test_tampered_authorization_is_rejected_after_fresh_digest(self) -> None:
        bundle = self.authorization_bundle()
        tampered = replace(
            bundle[3],
            execution_request_issued=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_independent_authorization_record_digest(
                tampered
            ),
        )
        tampered_bundle = bundle[:3] + (tampered,)
        evidence = self.evidence(tampered_bundle)
        request = self.request(tampered_bundle, evidence)
        record = self.execute(tampered_bundle, evidence, request)
        self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_REJECTED)
        self.assertFalse(record.source_recomputed_valid)

    def test_allowlists_and_objective_are_enforced(self) -> None:
        bundle = self.authorization_bundle()
        evidence = self.evidence(bundle)
        for overrides in (
            {"preparer_id": "unknown-preparer"},
            {"preparer_organization_id": "unknown-organization"},
            {"objective": "EXECUTE_NOW"},
        ):
            with self.subTest(overrides=overrides):
                request = self.request(bundle, evidence, **overrides)
                record = self.execute(bundle, evidence, request)
                self.assertEqual(
                    record.status,
                    BOUNDED_EXECUTION_PREPARATION_REJECTED,
                )

    def test_execution_authority_designation_binding_is_enforced(self) -> None:
        bundle = self.authorization_bundle()
        evidence = self.evidence(
            bundle,
            future_execution_authority_id="other-execution-authority",
        )
        request = self.request(
            bundle,
            evidence,
            future_execution_authority_id="other-execution-authority",
        )
        record = self.execute(bundle, evidence, request)
        self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_REJECTED)
        self.assertFalse(record.execution_authority_designation_binding_valid)

    def test_preparer_must_be_independent(self) -> None:
        bundle = self.authorization_bundle()
        identities = (
            "candidate-module",
            "dependency-reviewer",
            "authority-reviewer",
            "responsible-authority",
            "quiescence-reviewer",
            "quiescence-evidence-producer",
            "external-reviewer",
            "future-authorization-authority",
            "future-execution-authority",
        )
        for preparer_id in identities:
            with self.subTest(preparer_id=preparer_id):
                evidence = self.evidence(bundle, preparer_id=preparer_id)
                request = self.request(
                    bundle,
                    evidence,
                    preparer_id=preparer_id,
                )
                record = self.execute(bundle, evidence, request)
                self.assertEqual(
                    record.status,
                    BOUNDED_EXECUTION_PREPARATION_REJECTED,
                )
                self.assertFalse(record.preparer_independent)

    def test_qualification_independence_and_conflict_block(self) -> None:
        bundle = self.authorization_bundle()
        cases = (
            (
                {"preparer_qualification_verified": False},
                "preparer_qualification_not_verified",
            ),
            (
                {"preparer_independence_declared": False},
                "preparer_independence_not_declared",
            ),
            (
                {"conflict_disclosure_complete": False},
                "conflict_disclosure_incomplete",
            ),
            ({"material_conflict_present": True}, "material_conflict_present"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_scope_target_and_irreversibility_block(self) -> None:
        bundle = self.authorization_bundle()
        cases = (
            ({"execution_scope_items": ()}, "execution_scope_not_bounded"),
            (
                {"target_resource_ids": ("unapproved-resource",)},
                "target_resource_not_allowed",
            ),
            (
                {"protected_resource_ids": ("subject-runtime-state",)},
                "protected_resource_in_execution_scope",
            ),
            (
                {"irreversible_step_ids": ("delete-subject-state",)},
                "irreversible_step_present",
            ),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_rollback_recovery_stop_and_abort_block(self) -> None:
        bundle = self.authorization_bundle()
        cases = (
            ({"rollback_plan_verified": False}, "rollback_plan_not_verified"),
            ({"recovery_route_verified": False}, "recovery_route_not_verified"),
            ({"stop_conditions_complete": False}, "stop_conditions_incomplete"),
            ({"abort_channel_available": False}, "abort_channel_unavailable"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_oversight_monitoring_capture_and_simulation_block(self) -> None:
        bundle = self.authorization_bundle()
        cases = (
            ({"human_oversight_available": False}, "human_oversight_unavailable"),
            ({"monitoring_plan_complete": False}, "monitoring_plan_incomplete"),
            (
                {"evidence_capture_plan_complete": False},
                "evidence_capture_plan_incomplete",
            ),
            ({"simulation_verified": False}, "simulation_not_verified"),
            ({"execution_window_seconds": 121}, "execution_window_invalid"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_protected_hold_and_emergency_block(self) -> None:
        bundle = self.authorization_bundle()
        cases = (
            ({"protected_core_excluded": False}, "protected_core_not_excluded"),
            ({"institutional_hold_active": True}, "institutional_hold_active"),
            ({"emergency_state_active": True}, "emergency_state_active"),
        )
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                record = self.execute(bundle, self.evidence(bundle, **overrides))
                self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_BLOCKED)
                self.assertEqual(record.reason, reason)

    def test_expiry_staleness_and_delay_are_rejected(self) -> None:
        bundle = self.authorization_bundle()
        expired = self.evidence(
            bundle,
            package_expiry_at_epoch_seconds=self.preparation_completed_at - 1,
        )
        stale_requested = self.preparation_completed_at - 302
        stale = self.evidence(
            bundle,
            requested_at_epoch_seconds=stale_requested,
            captured_at_epoch_seconds=self.preparation_completed_at - 301,
        )
        stale_request = self.request(
            bundle,
            stale,
            requested_at_epoch_seconds=stale_requested,
        )
        late_completed = bundle[3].completed_at_epoch_seconds + 301
        late_evidence = self.evidence(
            bundle,
            requested_at_epoch_seconds=late_completed - 2,
            captured_at_epoch_seconds=late_completed - 1,
            completed_at_epoch_seconds=late_completed,
            package_expiry_at_epoch_seconds=late_completed + 600,
        )
        late_request = self.request(
            bundle,
            late_evidence,
            requested_at_epoch_seconds=late_completed - 2,
            completed_at_epoch_seconds=late_completed,
        )
        for evidence, request in (
            (expired, self.request(bundle, expired)),
            (stale, stale_request),
            (late_evidence, late_request),
        ):
            record = self.execute(bundle, evidence, request)
            self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_REJECTED)

    def test_subject_source_and_evidence_binding_tamper_reject(self) -> None:
        bundle = self.authorization_bundle()
        evidence = self.evidence(bundle)
        request = self.request(bundle, evidence)
        subject_request = replace(
            request,
            subject_id="different-subject",
            request_digest="",
        )
        subject_request = replace(
            subject_request,
            request_digest=apoptosis_bounded_execution_preparation_request_digest(
                subject_request
            ),
        )
        tampered_evidence = replace(
            evidence,
            source_independent_authorization_record_digest="x" * 64,
            evidence_digest="",
        )
        tampered_evidence = replace(
            tampered_evidence,
            evidence_digest=apoptosis_bounded_execution_preparation_evidence_digest(
                tampered_evidence
            ),
        )
        tampered_request = self.request(bundle, tampered_evidence)
        unbound_request = replace(
            request,
            preparation_evidence_digest="y" * 64,
            request_digest="",
        )
        unbound_request = replace(
            unbound_request,
            request_digest=apoptosis_bounded_execution_preparation_request_digest(
                unbound_request
            ),
        )
        for ev, req in (
            (evidence, subject_request),
            (tampered_evidence, tampered_request),
            (evidence, unbound_request),
        ):
            record = self.execute(bundle, ev, req)
            self.assertEqual(record.status, BOUNDED_EXECUTION_PREPARATION_REJECTED)

    def test_unsafe_policy_rejects_and_blocked_does_not_advance(self) -> None:
        unsafe = replace(
            self.policy,
            allow_execution_request=True,
            policy_digest="",
        )
        unsafe = replace(
            unsafe,
            policy_digest=apoptosis_bounded_execution_preparation_policy_digest(
                unsafe
            ),
        )
        self.assertEqual(
            self.execute(policy=unsafe).status,
            BOUNDED_EXECUTION_PREPARATION_REJECTED,
        )
        bundle = self.authorization_bundle()
        blocked = self.execute(
            bundle,
            self.evidence(bundle, rollback_plan_verified=False),
        )
        self.assertTrue(blocked.preparation_record_issued)
        self.assertFalse(blocked.bounded_execution_package_prepared)
        self.assertFalse(blocked.ready_for_execution_review)
        self.assertFalse(blocked.execution_request_issued)

    def test_determinism_read_only_and_record_tamper_detection(self) -> None:
        left = self.execute()
        right = self.execute()
        self.assertEqual(left, right)
        bundle = self.authorization_bundle()
        blocked = self.execute(
            bundle,
            self.evidence(bundle, simulation_verified=False),
        )
        rejected_bundle = self.authorization_bundle(rejected_source=True)
        rejected = self.execute(rejected_bundle)
        for record in (left, blocked, rejected):
            self.assertFalse(record.execution_request_issued)
            self.assertFalse(record.execution_decision_made)
            self.assertFalse(record.authority_revocation_performed)
            self.assertFalse(record.quiescence_transition_performed)
            self.assertFalse(record.terminal_transition_performed)
            self.assertFalse(record.tombstone_write_performed)
            self.assertFalse(record.physical_deletion_performed)
            self.assertFalse(record.live_git_execution_performed)
            self.assertFalse(record.repository_mutation_performed)

        evidence = self.evidence(bundle)
        request = self.request(bundle, evidence)
        record = self.execute(bundle, evidence, request)
        tampered = replace(
            record,
            execution_request_issued=True,
            record_digest="",
        )
        tampered = replace(
            tampered,
            record_digest=apoptosis_bounded_execution_preparation_record_digest(
                tampered
            ),
        )
        issues = self.record_issues(bundle, evidence, request, tampered)
        self.assertIn("bounded_execution_preparation_recomputation_mismatch", issues)
        self.assertIn(
            "bounded_execution_preparation_execution_effect_performed",
            issues,
        )


if __name__ == "__main__":
    unittest.main()
