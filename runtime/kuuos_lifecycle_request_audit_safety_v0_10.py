from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import BLOCKED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def safety_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    cases = (
        {"operation_scope_items": ()},
        {"target_resource_ids": ("unlisted-resource",)},
        {
            "target_resource_ids": ("subject-runtime-state",),
            "protected_resource_ids": ("subject-runtime-state",),
        },
        {"irreversible_step_ids": ("unrecoverable-step",)},
        {"rollback_plan_verified": False},
        {"recovery_route_verified": False},
        {"stop_conditions_complete": False},
        {"abort_channel_available": False},
        {"human_oversight_available": False},
        {"monitoring_plan_complete": False},
        {"evidence_capture_plan_complete": False},
        {"simulation_verified": False},
        {"operation_window_seconds": 0},
        {"protected_core_excluded": False},
        {"institutional_hold_active": True},
        {"emergency_state_active": True},
        {"decision_route_available": False},
        {"appeal_route_available": False},
        {"dissent_route_available": False},
    )
    outcomes = []
    for overrides in cases:
        evidence = fixture.make_request_evidence(source, **overrides)
        request = fixture.make_request_submission(source, evidence)
        artifact = fixture.evaluate_request(source, evidence, request)
        outcomes.append(
            artifact.status == BLOCKED
            and artifact.request_record_issued
            and not artifact.bounded_request_issued
            and not artifact.ready_for_decision_review
        )
    return {"package_safety_blockers": all(outcomes)}
