from __future__ import annotations

from runtime.kuuos_lifecycle_decision_review_types_v0_11 import (
    BLOCKED as SOURCE_BLOCKED,
    REJECTED as SOURCE_REJECTED,
)
from runtime.kuuos_lifecycle_authorization_decision_types_v0_12 import (
    APPROVED,
    DENIED,
    REJECTED,
)
from runtime.kuuos_lifecycle_governance_authorization_decision_v0_12 import (
    artifact_issues,
    make_policy,
    prior_actor_ids,
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
        evidence = self.make_decision_evidence(source)
        decision = self.make_decision_submission(source, evidence)
        approved = self.evaluate_decision(source, evidence, decision)
        checks["valid_input_produces_approved"] = (
            approved.status == APPROVED
            and approved.authorization_decision_made
            and approved.authorization_approved
            and approved.operation_approval_required_next
            and not approved.operation_approved
        )

        blocked_source_record = self.refresh_source_record(
            source[3],
            status=SOURCE_BLOCKED,
            clear_for_authorization_decision=False,
            authorization_decision_required_next=False,
        )
        blocked_source = (*source[:3], blocked_source_record, source[4])
        blocked_evidence = self.make_decision_evidence(blocked_source)
        blocked_decision = self.make_decision_submission(
            blocked_source,
            blocked_evidence,
        )
        blocked_source_rejected = (
            self.evaluate_decision(
                blocked_source,
                blocked_evidence,
                blocked_decision,
            ).status
            == REJECTED
        )

        rejected_source_record = self.refresh_source_record(
            source[3],
            status=SOURCE_REJECTED,
            review_record_issued=False,
            review_completed=False,
            clear_for_authorization_decision=False,
            authorization_decision_required_next=False,
        )
        rejected_source = (*source[:3], rejected_source_record, source[4])
        rejected_evidence = self.make_decision_evidence(rejected_source)
        rejected_decision = self.make_decision_submission(
            rejected_source,
            rejected_evidence,
        )
        rejected_source_rejected = (
            self.evaluate_decision(
                rejected_source,
                rejected_evidence,
                rejected_decision,
            ).status
            == REJECTED
        )
        checks["non_clear_source_rejected"] = (
            blocked_source_rejected and rejected_source_rejected
        )

        tampered_record = self.refresh_source_record(
            source[3],
            reason="fresh-digest-tamper",
        )
        tampered_source = (*source[:3], tampered_record, source[4])
        tampered_evidence = self.make_decision_evidence(tampered_source)
        tampered_decision = self.make_decision_submission(
            tampered_source,
            tampered_evidence,
        )
        checks["fresh_digest_source_tamper_detected"] = (
            self.evaluate_decision(
                tampered_source,
                tampered_evidence,
                tampered_decision,
            ).status
            == REJECTED
        )

        source_binding_evidence = self.refresh_evidence(
            evidence,
            source_decision_review_record_digest="x" * 64,
        )
        source_binding_decision = self.make_decision_submission(
            source,
            source_binding_evidence,
        )
        checks["source_binding_enforced"] = (
            self.evaluate_decision(
                source,
                source_binding_evidence,
                source_binding_decision,
            ).status
            == REJECTED
        )

        evidence_binding_decision = self.refresh_decision(
            decision,
            decision_evidence_digest="y" * 64,
        )
        checks["evidence_digest_binding_enforced"] = (
            self.evaluate_decision(
                source,
                evidence,
                evidence_binding_decision,
            ).status
            == REJECTED
        )

        unknown_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id="unknown-decision-maker",
        )
        unknown_decision = self.make_decision_submission(
            source,
            unknown_evidence,
            authorization_decision_maker_id="unknown-decision-maker",
        )
        checks["decision_maker_id_policy_enforced"] = (
            self.evaluate_decision(
                source,
                unknown_evidence,
                unknown_decision,
            ).status
            == REJECTED
        )

        org_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_organization_id="unknown-organization",
        )
        org_decision = self.make_decision_submission(
            source,
            org_evidence,
            authorization_decision_maker_organization_id="unknown-organization",
        )
        checks["decision_maker_organization_policy_enforced"] = (
            self.evaluate_decision(
                source,
                org_evidence,
                org_decision,
            ).status
            == REJECTED
        )

        designated_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        designated_decision = self.make_decision_submission(
            source,
            designated_evidence,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        checks["designated_decision_maker_binding_enforced"] = (
            self.evaluate_decision(
                source,
                designated_evidence,
                designated_decision,
            ).status
            == REJECTED
        )

        objective_decision = self.make_decision_submission(
            source,
            evidence,
            objective="APPROVE_OPERATION_NOW",
        )
        checks["objective_policy_enforced"] = (
            self.evaluate_decision(
                source,
                evidence,
                objective_decision,
            ).status
            == REJECTED
        )

        prior_ids = prior_actor_ids(
            source[0].subject_id,
            source[0],
            source[4],
        )
        prior_id = sorted(
            item
            for item in prior_ids
            if item
            not in {
                self.decision_maker_id,
                source[0].decision_reviewer_id,
                source[0].requester_id,
                source[0].future_operator_id,
            }
        )[0]
        prior_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id=prior_id,
        )
        prior_decision = self.make_decision_submission(
            source,
            prior_evidence,
            authorization_decision_maker_id=prior_id,
        )
        checks["prior_chain_independence_enforced"] = (
            self.evaluate_decision(
                source,
                prior_evidence,
                prior_decision,
            ).status
            == REJECTED
        )

        requester_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id=source[0].requester_id,
        )
        requester_decision = self.make_decision_submission(
            source,
            requester_evidence,
            authorization_decision_maker_id=source[0].requester_id,
        )
        reviewer_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id=source[0].decision_reviewer_id,
        )
        reviewer_decision = self.make_decision_submission(
            source,
            reviewer_evidence,
            authorization_decision_maker_id=source[0].decision_reviewer_id,
        )
        checks["requester_and_reviewer_separation_enforced"] = (
            self.evaluate_decision(
                source,
                requester_evidence,
                requester_decision,
            ).status
            == REJECTED
            and self.evaluate_decision(
                source,
                reviewer_evidence,
                reviewer_decision,
            ).status
            == REJECTED
        )

        operator_evidence = self.make_decision_evidence(
            source,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        operator_decision = self.make_decision_submission(
            source,
            operator_evidence,
            authorization_decision_maker_id=source[0].future_operator_id,
        )
        checks["decision_maker_operator_separation_enforced"] = (
            self.evaluate_decision(
                source,
                operator_evidence,
                operator_decision,
            ).status
            == REJECTED
        )

        mandate_evidence = self.make_decision_evidence(
            source,
            decision_maker_mandate_verified=False,
        )
        mandate_decision = self.make_decision_submission(
            source,
            mandate_evidence,
        )
        qualification_evidence = self.make_decision_evidence(
            source,
            decision_maker_qualification_verified=False,
        )
        qualification_decision = self.make_decision_submission(
            source,
            qualification_evidence,
        )
        checks["mandate_or_qualification_failure_denies"] = (
            self.evaluate_decision(
                source,
                mandate_evidence,
                mandate_decision,
            ).status
            == DENIED
            and self.evaluate_decision(
                source,
                qualification_evidence,
                qualification_decision,
            ).status
            == DENIED
        )

        independence_evidence = self.make_decision_evidence(
            source,
            decision_maker_independence_declared=False,
        )
        independence_decision = self.make_decision_submission(
            source,
            independence_evidence,
        )
        conflict_evidence = self.make_decision_evidence(
            source,
            material_conflict_present=True,
        )
        conflict_decision = self.make_decision_submission(
            source,
            conflict_evidence,
        )
        checks["independence_or_conflict_failure_denies"] = (
            self.evaluate_decision(
                source,
                independence_evidence,
                independence_decision,
            ).status
            == DENIED
            and self.evaluate_decision(
                source,
                conflict_evidence,
                conflict_decision,
            ).status
            == DENIED
        )

        jurisdiction_evidence = self.make_decision_evidence(
            source,
            jurisdiction_verified=False,
        )
        jurisdiction_decision = self.make_decision_submission(
            source,
            jurisdiction_evidence,
        )
        quorum_evidence = self.make_decision_evidence(
            source,
            quorum_satisfied=False,
        )
        quorum_decision = self.make_decision_submission(
            source,
            quorum_evidence,
        )
        checks["jurisdiction_or_quorum_failure_denies"] = (
            self.evaluate_decision(
                source,
                jurisdiction_evidence,
                jurisdiction_decision,
            ).status
            == DENIED
            and self.evaluate_decision(
                source,
                quorum_evidence,
                quorum_decision,
            ).status
            == DENIED
        )

        rationale_evidence = self.make_decision_evidence(
            source,
            reasoned_decision_complete=False,
        )
        rationale_decision = self.make_decision_submission(
            source,
            rationale_evidence,
        )
        proportionality_evidence = self.make_decision_evidence(
            source,
            proportionality_satisfied=False,
        )
        proportionality_decision = self.make_decision_submission(
            source,
            proportionality_evidence,
        )
        alternatives_evidence = self.make_decision_evidence(
            source,
            less_restrictive_alternatives_exhausted=False,
        )
        alternatives_decision = self.make_decision_submission(
            source,
            alternatives_evidence,
        )
        checks["reasoned_proportionality_alternatives_failure_denies"] = all(
            item.status == DENIED
            for item in (
                self.evaluate_decision(
                    source,
                    rationale_evidence,
                    rationale_decision,
                ),
                self.evaluate_decision(
                    source,
                    proportionality_evidence,
                    proportionality_decision,
                ),
                self.evaluate_decision(
                    source,
                    alternatives_evidence,
                    alternatives_decision,
                ),
            )
        )

        irreversibility_evidence = self.make_decision_evidence(
            source,
            irreversibility_review_complete=False,
        )
        irreversibility_decision = self.make_decision_submission(
            source,
            irreversibility_evidence,
        )
        human_impact_evidence = self.make_decision_evidence(
            source,
            human_impact_review_complete=False,
        )
        human_impact_decision = self.make_decision_submission(
            source,
            human_impact_evidence,
        )
        route_evidence = self.make_decision_evidence(
            source,
            operation_approval_route_available=False,
            appeal_route_available=False,
            dissent_route_available=False,
            minority_opinion_recorded=False,
        )
        route_decision = self.make_decision_submission(
            source,
            route_evidence,
        )
        checks[
            "irreversibility_human_impact_and_routes_failure_denies"
        ] = all(
            item.status == DENIED
            for item in (
                self.evaluate_decision(
                    source,
                    irreversibility_evidence,
                    irreversibility_decision,
                ),
                self.evaluate_decision(
                    source,
                    human_impact_evidence,
                    human_impact_decision,
                ),
                self.evaluate_decision(
                    source,
                    route_evidence,
                    route_decision,
                ),
            )
        )

        expired_evidence = self.make_decision_evidence(
            source,
            decision_requested_at_epoch_seconds=(
                source[1].authorization_decision_deadline_at_epoch_seconds + 1
            ),
            captured_at_epoch_seconds=(
                source[1].authorization_decision_deadline_at_epoch_seconds + 2
            ),
            completed_at_epoch_seconds=(
                source[1].authorization_decision_deadline_at_epoch_seconds + 3
            ),
            authorization_decision_expiry_at_epoch_seconds=(
                source[1].authorization_decision_deadline_at_epoch_seconds + 4
            ),
            operation_approval_deadline_at_epoch_seconds=(
                source[1].authorization_decision_deadline_at_epoch_seconds + 4
            ),
        )
        expired_decision = self.make_decision_submission(
            source,
            expired_evidence,
            decision_requested_at_epoch_seconds=(
                expired_evidence.decision_requested_at_epoch_seconds
            ),
            completed_at_epoch_seconds=(
                expired_evidence.completed_at_epoch_seconds
            ),
            operation_approval_deadline_at_epoch_seconds=(
                expired_evidence.operation_approval_deadline_at_epoch_seconds
            ),
        )
        restrictive_policy = make_policy(
            "restrictive-lifecycle-authorization-decision-policy-v0-12",
            allowed_authorization_decision_maker_ids=(
                self.policy.allowed_authorization_decision_maker_ids
            ),
            allowed_authorization_decision_maker_organization_ids=(
                self.policy.allowed_authorization_decision_maker_organization_ids
            ),
            allowed_target_resource_ids=self.policy.allowed_target_resource_ids,
            max_decision_delay_seconds=300,
            max_evidence_age_seconds=300,
            max_decision_expiry_seconds=180,
            max_operation_approval_delay_seconds=120,
            max_operation_window_seconds=1,
            max_scope_items=8,
        )
        checks["temporal_or_package_boundaries_enforced"] = (
            self.evaluate_decision(
                source,
                expired_evidence,
                expired_decision,
            ).status
            == REJECTED
            and self.evaluate_decision(
                source,
                evidence,
                decision,
                restrictive_policy,
            ).status
            == DENIED
        )

        denied = self.evaluate_decision(
            source,
            mandate_evidence,
            mandate_decision,
        )
        rejected = self.evaluate_decision(
            blocked_source,
            blocked_evidence,
            blocked_decision,
        )
        effect_names = (
            "operation_approved",
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
        checks["all_statuses_preserve_operation_boundary"] = (
            all(
                item.lifecycle_read_only
                and not any(getattr(item, name) for name in effect_names)
                for item in (approved, denied, rejected)
            )
            and approved.authorization_decision_made
            and denied.authorization_decision_made
            and not rejected.authorization_decision_made
        )

        same = self.evaluate_decision(source, evidence, decision)
        checks["determinism_and_record_integrity"] = (
            approved.to_dict() == same.to_dict()
            and not artifact_issues(
                approved,
                *self.artifact_args(source, evidence, decision),
            )
        )
        return checks

    def test_complete_audit_matrix(self) -> None:
        checks = self.audit_matrix()
        failures = sorted(
            name for name, passed in checks.items() if not passed
        )
        self.assertFalse(
            failures,
            f"failed lifecycle authorization decision checks: {failures}",
        )
        self.assertEqual(len(checks), 20)


if __name__ == "__main__":
    import unittest

    result = unittest.main(exit=False, verbosity=2).result
    raise SystemExit(0 if result.wasSuccessful() else 1)
