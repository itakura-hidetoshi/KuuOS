from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def policy_scope_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()

    organization_evidence = fixture.make_request_evidence(
        source,
        requester_organization_id="alternate-organization",
    )
    organization_request = fixture.make_request_submission(
        source,
        organization_evidence,
        requester_organization_id="alternate-organization",
    )
    organization_result = fixture.evaluate_request(
        source,
        organization_evidence,
        organization_request,
    )

    valid_evidence = fixture.make_request_evidence(source)
    objective_request = fixture.make_request_submission(
        source,
        valid_evidence,
        objective="ALTERNATE_REQUEST_OBJECTIVE",
    )
    objective_result = fixture.evaluate_request(
        source,
        valid_evidence,
        objective_request,
    )
    return {
        "requester_organization_policy": organization_result.status == REJECTED,
        "request_objective_policy": objective_result.status == REJECTED,
    }
