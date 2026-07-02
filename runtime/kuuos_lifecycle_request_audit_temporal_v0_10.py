from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def temporal_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    review_completed = source[1].completed_at_epoch_seconds
    requested = review_completed + 301
    captured = requested + 20
    completed = captured + 20
    evidence = fixture.make_request_evidence(
        source,
        requested_at_epoch_seconds=requested,
        captured_at_epoch_seconds=captured,
        completed_at_epoch_seconds=completed,
    )
    request = fixture.make_request_submission(
        source,
        evidence,
        requested_at_epoch_seconds=requested,
        completed_at_epoch_seconds=completed,
    )
    delayed = fixture.evaluate_request(source, evidence, request)

    evidence = fixture.make_request_evidence(
        source,
        captured_at_epoch_seconds=fixture.completed_at - 301,
    )
    request = fixture.make_request_submission(source, evidence)
    stale = fixture.evaluate_request(source, evidence, request)
    return {
        "request_delay_boundary": delayed.status == REJECTED,
        "evidence_freshness_boundary": stale.status == REJECTED,
    }
