from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def identity_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    evidence = fixture.make_request_evidence(source, requester_id="alternate-submitter")
    request = fixture.make_request_submission(
        source,
        evidence,
        requester_id="alternate-submitter",
    )
    result = fixture.evaluate_request(source, evidence, request)
    return {"requester_identity_policy": result.status == REJECTED}
