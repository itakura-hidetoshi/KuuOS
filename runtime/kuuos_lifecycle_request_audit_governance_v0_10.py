from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import BLOCKED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def governance_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    results: dict[str, bool] = {}

    evidence = fixture.make_request_evidence(
        source,
        requester_qualification_verified=False,
    )
    request = fixture.make_request_submission(source, evidence)
    qualification = fixture.evaluate_request(source, evidence, request)
    results["qualification_blocker"] = (
        qualification.status == BLOCKED
        and qualification.reason == "requester_qualification_verified"
        and not qualification.bounded_request_issued
    )

    evidence = fixture.make_request_evidence(
        source,
        requester_independence_declared=False,
    )
    request = fixture.make_request_submission(source, evidence)
    declaration = fixture.evaluate_request(source, evidence, request)
    results["independence_declaration_blocker"] = (
        declaration.status == BLOCKED
        and declaration.reason == "requester_independence_declared"
        and not declaration.bounded_request_issued
    )
    return results
