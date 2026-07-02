from dataclasses import replace

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    BLOCKED,
    REJECTED,
    policy_digest,
)
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def safety_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()

    immutable_changes = (
        {"operation_scope_items": ()},
        {"target_resource_ids": ("unlisted-resource",)},
        {
            "target_resource_ids": ("subject-runtime-state",),
            "protected_resource_ids": ("subject-runtime-state",),
        },
        {"irreversible_step_ids": ("unrecoverable-step",)},
        {"operation_window_seconds": 0},
    )
    immutable_outcomes = []
    for overrides in immutable_changes:
        evidence = fixture.make_request_evidence(source, **overrides)
        request = fixture.make_request_submission(source, evidence)
        artifact = fixture.evaluate_request(source, evidence, request)
        immutable_outcomes.append(
            artifact.status == REJECTED
            and not artifact.request_record_issued
            and not artifact.bounded_request_issued
        )

    blockers = (
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
        {"decision_route_available": False},
        {"appeal_route_available": False},
        {"dissent_route_available": False},
    )
    blocker_outcomes = []
    for overrides in blockers:
        evidence = fixture.make_request_evidence(source, **overrides)
        request = fixture.make_request_submission(source, evidence)
        artifact = fixture.evaluate_request(source, evidence, request)
        blocker_outcomes.append(
            artifact.status == BLOCKED
            and artifact.request_record_issued
            and not artifact.bounded_request_issued
            and not artifact.ready_for_decision_review
        )

    evidence = fixture.make_request_evidence(source)
    request = fixture.make_request_submission(source, evidence)
    policy_cases = (
        {"max_scope_items": 1},
        {"max_operation_window_seconds": 30},
        {"allowed_target_resource_ids": ("subject-runtime-state",)},
    )
    policy_outcomes = []
    for changes in policy_cases:
        policy = replace(fixture.policy, **changes, policy_digest="")
        policy = replace(policy, policy_digest=policy_digest(policy))
        artifact = fixture.evaluate_request(source, evidence, request, policy)
        policy_outcomes.append(
            artifact.status == BLOCKED and not artifact.bounded_request_issued
        )

    return {
        "scope_and_package_safety_classification": (
            all(immutable_outcomes)
            and all(blocker_outcomes)
            and all(policy_outcomes)
        )
    }
