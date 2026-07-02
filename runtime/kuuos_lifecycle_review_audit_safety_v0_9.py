from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_lifecycle_review_types_v0_9 import (
    BLOCKED,
    REJECTED,
    lifecycle_review_policy_digest,
    lifecycle_review_record_digest,
)
from runtime.kuuos_lifecycle_review_v0_9 import (
    apoptosis_execution_review_record_issues,
)
from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


def safety_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleReviewFixtureV09(methodName="runTest")
    fixture.setUp()
    results: dict[str, bool] = {}
    bundle = fixture.make_bundle()

    governance_cases = (
        {"reviewer_qualification_verified": False},
        {"reviewer_independence_declared": False},
        {"conflict_disclosure_complete": False},
        {"material_conflict_present": True},
        {"appeal_route_available": False},
        {"dissent_route_available": False},
    )
    governance_ok = True
    for overrides in governance_cases:
        evidence = fixture.make_evidence(bundle, **overrides)
        record = fixture.review(
            bundle,
            evidence,
            fixture.make_request(bundle, evidence),
        )
        governance_ok = governance_ok and (
            record.status == BLOCKED
            and record.review_record_issued
            and not record.clear_for_next_request_layer
            and not record.next_request_layer_required
        )
    results["governance_blockers"] = governance_ok

    safety_cases = (
        {"rollback_plan_verified": False},
        {"recovery_route_verified": False},
        {"stop_conditions_complete": False},
        {"abort_channel_available": False},
        {"human_oversight_available": False},
        {"monitoring_plan_complete": False},
        {"evidence_capture_plan_complete": False},
        {"simulation_verified": False},
        {"protected_core_excluded": False},
        {"institutional_hold_active": True},
        {"emergency_state_active": True},
    )
    safety_ok = True
    for overrides in safety_cases:
        evidence = fixture.make_evidence(bundle, **overrides)
        record = fixture.review(
            bundle,
            evidence,
            fixture.make_request(bundle, evidence),
        )
        safety_ok = safety_ok and record.status == BLOCKED
    results["package_safety_blockers"] = safety_ok

    scope_cases = (
        {"execution_scope_items": ("different-step",)},
        {"target_resource_ids": ("unlisted-resource",)},
        {"irreversible_step_ids": ("irreversible-step",)},
    )
    scope_ok = True
    for overrides in scope_cases:
        evidence = fixture.make_evidence(bundle, **overrides)
        record = fixture.review(
            bundle,
            evidence,
            fixture.make_request(bundle, evidence),
        )
        scope_ok = scope_ok and (
            record.status == REJECTED
            and not record.checks["scope_binding_valid"]
        )
    results["scope_binding"] = scope_ok

    timing_cases = (
        {
            "completed_at_epoch_seconds": (
                fixture.upstream.preparation_completed_at + 400
            ),
            "review_expiry_at_epoch_seconds": (
                fixture.upstream.preparation_completed_at + 500
            ),
        },
        {"captured_at_epoch_seconds": fixture.requested_at - 1},
        {"review_expiry_at_epoch_seconds": fixture.completed_at - 1},
        {
            "review_requested_at_epoch_seconds": (
                fixture.upstream.package_expiry_at + 1
            ),
            "captured_at_epoch_seconds": fixture.upstream.package_expiry_at + 2,
            "completed_at_epoch_seconds": fixture.upstream.package_expiry_at + 3,
            "review_expiry_at_epoch_seconds": (
                fixture.upstream.package_expiry_at + 10
            ),
        },
    )
    timing_ok = True
    for overrides in timing_cases:
        evidence = fixture.make_evidence(bundle, **overrides)
        record = fixture.review(
            bundle,
            evidence,
            fixture.make_request(bundle, evidence),
        )
        timing_ok = timing_ok and record.status == REJECTED
    results["time_and_expiry_bounds"] = timing_ok

    evidence = fixture.make_evidence(bundle)
    request = fixture.make_request(bundle, evidence)
    unsafe = replace(fixture.policy, read_only=False, policy_digest="")
    unsafe = replace(
        unsafe,
        policy_digest=lifecycle_review_policy_digest(unsafe),
    )
    unsafe_result = fixture.review(bundle, evidence, request, unsafe)
    results["unsafe_policy_rejected"] = (
        unsafe_result.status == REJECTED
        and not unsafe_result.checks["policy_valid"]
    )

    clear = fixture.review(bundle, evidence, request)
    blocked_evidence = fixture.make_evidence(
        bundle,
        appeal_route_available=False,
    )
    blocked = fixture.review(
        bundle,
        blocked_evidence,
        fixture.make_request(bundle, blocked_evidence),
    )
    rejected_bundle = fixture.make_bundle(
        authorization_overrides={"quorum_satisfied": False}
    )
    rejected = fixture.review(rejected_bundle)
    results["all_statuses_read_only"] = all(
        record.effect_free and record.read_only
        for record in (clear, blocked, rejected)
    )

    left = fixture.review(bundle, evidence, request)
    right = fixture.review(bundle, evidence, request)
    altered = replace(left, effect_free=False, record_digest="")
    altered = replace(
        altered,
        record_digest=lifecycle_review_record_digest(altered),
    )
    args = (
        request,
        evidence,
        fixture.policy,
        bundle[0],
        bundle[1],
        bundle[2],
        bundle[3],
        *bundle[4],
    )
    issues = apoptosis_execution_review_record_issues(altered, *args)
    results["determinism_and_record_integrity"] = (
        left.to_dict() == right.to_dict()
        and "review_recomputation_mismatch" in issues
        and "non_read_only_artifact" in issues
    )

    return results
