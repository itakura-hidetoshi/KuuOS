from runtime.kuuos_lifecycle_request_core_v0_10 import artifact_issues
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def verification_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()

    valid_evidence = fixture.make_request_evidence(source)
    valid_request = fixture.make_request_submission(source, valid_evidence)
    valid = fixture.evaluate_request(source, valid_evidence, valid_request)

    blocked_evidence = fixture.make_request_evidence(
        source,
        requester_qualification_verified=False,
    )
    blocked_request = fixture.make_request_submission(source, blocked_evidence)
    blocked = fixture.evaluate_request(source, blocked_evidence, blocked_request)

    alternate_request = fixture.make_request_submission(
        source,
        valid_evidence,
        objective="ALTERNATE_REQUEST_OBJECTIVE",
    )
    alternate = fixture.evaluate_request(source, valid_evidence, alternate_request)

    cases = (
        (valid, valid_evidence, valid_request),
        (blocked, blocked_evidence, blocked_request),
        (alternate, valid_evidence, alternate_request),
    )
    return {
        "all_statuses_verify_without_later_stage_output": all(
            not artifact_issues(
                artifact,
                *fixture.artifact_args(source, evidence, request),
            )
            for artifact, evidence, request in cases
        )
    }
