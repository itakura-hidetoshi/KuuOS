from __future__ import annotations

from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    APPROVED,
    DENIED,
    REJECTED,
)
from runtime.kuuos_lifecycle_authorization_decision_v0_12 import artifact_issues
from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    BLOCKED as SOURCE_BLOCKED,
)
from tests.kuuos_lifecycle_authorization_decision_fixture_v0_12 import (
    LifecycleAuthorizationDecisionFixtureV012,
)


class LifecycleAuthorizationDecisionV012Tests(
    LifecycleAuthorizationDecisionFixtureV012
):
    def audit_matrix(self) -> dict[str, bool]:
        checks: dict[str, bool] = {}
        source = self.make_source()
        evidence = self.make_authorization_evidence(source)
        decision = self.make_authorization_submission(source, evidence)
        approved = self.evaluate_decision(source, evidence, decision)

        checks["valid_input_produces_real_approval"] = (
            approved.status == APPROVED
            and approved.decision_record_issued
            and approved.authorization_decision_made
            and approved.operation_approved
            and approved.operation_start_required_next
        )

        blocked_record = self.refresh_source_record(
            source[3],
            status=SOURCE_BLOCKED,
            clear_for_authorization_decision=False,
            authorization_decision_required_next=False,
        )
        blocked_source = (*source[:3], blocked_record, source[4])
        blocked_evidence = self.make_authorization_evidence(blocked_source)
        blocked_decision = self.make_authorization_submission(
            blocked_source, blocked_evidence
        )
        checks["non_clear_source_rejected"] = (
            self.evaluate_decision(
                blocked_source, blocked_evidence, blocked_decision
            ).status
            == REJECTED
        )

        tampered_record = self.refresh_source_record(
            source[3], reason="fresh-digest-source-tamper"
        )
        tampered_source = (*source[:3], tampered_record, source[4])
        tampered_evidence = self.make_authorization_evidence(tampered_source)
        tampered_decision = self.make_authorization_submission(
            tampered_source, tampered_evidence
        )
        checks["full_source_recomputation_detects_tamper"] = (
            self.evaluate_decision(
                tampered_source, tampered_evidence, tampered_decision
            ).status
            == REJECTED
        )

        source_binding_evidence = self.refresh_evidence(
            evidence, source_decision_review_record_digest="x" * 64
        )
        source_binding_decision = self.make_authorization_submission(
            source, source_binding_evidence
        )
        checks["source_binding_enforced"] = (
            self.evaluate_decision(
                source, source_binding_evidence, source_binding_decision
            ).status
            == REJECTED
        )

        evidence_binding_decision = self.refresh_decision(
            decision, authorization_evidence_digest="y" * 64
        )
        checks["evidence_binding_enforced"] = (
            self.evaluate_decision(
                source, evidence, evidence_binding_decision
            ).status
            == REJECTED
        )

        unknown_evidence = self.make_authorization_evidence(
            source, authorization_decision_maker_id="unknown-authority"
        )
        unknown_decision = self.make_authorization_submission(
            source,
            unknown_evidence,
            authorization_decision_maker_id="unknown-authority",
        )
        checks["authorization_maker_policy_enforced"] = (
            self.evaluate_decision(
                source, unknown_evidence, unknown_decision
            ).status
            == REJECTED
        )

        unknown_org_evidence = self.make_authorization_evidence(
            source,
            authorization_decision_maker_organization_id="unknown-organization",
        )
        unknown_org_decision = self.make_authorization_submission(
            source,
            unknown_org_evidence,
            authorization_decision_maker_organization_id="unknown-organization",
        )
        checks["authorization_organization_policy_enforced"] = (
            self.evaluate_decision(
                source, unknown_org_evidence, unknown_org_decision
            ).status
            == REJECTED
        )

        objective_decision = self.make_authorization_submission(
            source, evidence, objective="START_OPERATION_NOW"
        )
        checks["objective_policy_enforced"] = (
            self.evaluate_decision(source, evidence, objective_decision).status
            == REJECTED
        )

        checks["prior_chain_independence_verified"] = approved.checks[
            "independent_from_prior_chain"
        ]

        reviewer_evidence = self.make_authorization_evidence(
            source,
            authorization_decision_maker_id=source[0].decision_reviewer_id,
        )
        reviewer_decision = self.make_authorization_submission(
            source,
            reviewer_evidence,
            authorization_decision_maker_id=source[0].decision_reviewer_id,
        )
        checks["reviewer_authority_separation_enforced"] = (
            self.evaluate_decision(
                source, reviewer_evidence, reviewer_decision
            ).status
            == REJECTED
        )

        requester_evidence = self.make_authorization_evidence(
            source,
            authorization_decision_maker_id=source[0].requester_id,
        )
        requester_decision = self.make_authorization_submission(
            source,
            requester_evidence,
            authorization_decision_maker_id=source[0].requester_id,
        )
        checks["requester_authority_separation_enforced"] = (
            self.evaluate_decision(
                source, requester_evidence, requester_decision
            ).status
            == REJECTED
        )

        operator_evidence = self.make_authorization_evidence(
            source,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        operator_decision = self.make_authorization_submission(
            source,
            operator_evidence,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        checks["operator_authority_separation_enforced"] = (
            self.evaluate_decision(
                source, operator_evidence, operator_decision
            ).status
            == REJECTED
        )

        mandate_evidence = self.make_authorization_evidence(
            source, authority_mandate_verified=False
        )
        mandate_decision = self.make_authorization_submission(
            source, mandate_evidence
        )
        checks["mandate_failure_denies"] = (
            self.evaluate_decision(
                source, mandate_evidence, mandate_decision
            ).status
            == DENIED
        )

        qualification_evidence = self.make_authorization_evidence(
            source, authority_qualification_verified=False
        )
        qualification_decision = self.make_authorization_submission(
            source, qualification_evidence
        )
        checks["qualification_failure_denies"] = (
            self.evaluate_decision(
                source, qualification_evidence, qualification_decision
            ).status
            == DENIED
        )

        conflict_evidence = self.make_authorization_evidence(
            source, material_conflict_present=True
        )
        conflict_decision = self.make_authorization_submission(
            source, conflict_evidence
        )
        checks["material_conflict_denies"] = (
            self.evaluate_decision(
                source, conflict_evidence, conflict_decision
            ).status
            == DENIED
        )

        jurisdiction_evidence = self.make_authorization_evidence(
            source, jurisdiction_verified=False, quorum_verified=False
        )
        jurisdiction_decision = self.make_authorization_submission(
            source, jurisdiction_evidence
        )
        checks["jurisdiction_or_quorum_failure_denies"] = (
            self.evaluate_decision(
                source, jurisdiction_evidence, jurisdiction_decision
            ).status
            == DENIED
        )

        safety_evidence = self.make_authorization_evidence(
            source, rollback_plan_verified=False
        )
        safety_decision = self.make_authorization_submission(
            source, safety_evidence
        )
        checks["package_safety_failure_denies"] = (
            self.evaluate_decision(
                source, safety_evidence, safety_decision
            ).status
            == DENIED
        )

        expired_completed = (
            source[1].authorization_decision_deadline_at_epoch_seconds + 1
        )
        expired_evidence = self.make_authorization_evidence(
            source,
            decision_requested_at_epoch_seconds=expired_completed - 2,
            captured_at_epoch_seconds=expired_completed - 1,
            completed_at_epoch_seconds=expired_completed,
            approval_expiry_at_epoch_seconds=expired_completed + 1,
        )
        expired_decision = self.make_authorization_submission(
            source,
            expired_evidence,
            decision_requested_at_epoch_seconds=expired_completed - 2,
            completed_at_epoch_seconds=expired_completed,
            approval_expiry_at_epoch_seconds=expired_completed + 1,
        )
        checks["temporal_boundaries_enforced"] = (
            self.evaluate_decision(
                source, expired_evidence, expired_decision
            ).status
            == REJECTED
        )

        denied = self.evaluate_decision(
            source, mandate_evidence, mandate_decision
        )
        rejected = self.evaluate_decision(
            blocked_source, blocked_evidence, blocked_decision
        )
        later_effect_names = (
            "operation_started",
            "operation_completed",
            "authority_changed",
            "quiescence_state_changed",
            "terminal_state_changed",
            "terminal_marker_written",
            "resource_removed",
            "external_operation_performed",
            "repository_changed",
        )
        checks["decision_stage_does_not_forge_execution"] = (
            all(not getattr(approved, name) for name in later_effect_names)
            and all(not getattr(denied, name) for name in later_effect_names)
            and all(not getattr(rejected, name) for name in later_effect_names)
            and denied.authorization_decision_made
            and not denied.operation_approved
            and not rejected.authorization_decision_made
        )

        same = self.evaluate_decision(source, evidence, decision)
        checks["determinism_and_record_integrity"] = (
            approved.to_dict() == same.to_dict()
            and not artifact_issues(
                approved, *self.artifact_args(source, evidence, decision)
            )
        )
        return checks

    def test_complete_audit_matrix(self) -> None:
        checks = self.audit_matrix()
        failures = sorted(name for name, passed in checks.items() if not passed)
        self.assertFalse(
            failures,
            f"failed lifecycle authorization decision checks: {failures}",
        )
        self.assertEqual(len(checks), 20)


if __name__ == "__main__":
    import unittest

    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
