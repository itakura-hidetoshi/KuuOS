from runtime.kuuos_lifecycle_request_core_v0_10 import artifact_issues
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def determinism_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    evidence = fixture.make_request_evidence(source)
    request = fixture.make_request_submission(source, evidence)
    first = fixture.evaluate_request(source, evidence, request)
    second = fixture.evaluate_request(source, evidence, request)
    return {
        "determinism_and_record_integrity": (
            first.to_dict() == second.to_dict()
            and not artifact_issues(
                first,
                *fixture.artifact_args(source, evidence, request),
            )
        )
    }
