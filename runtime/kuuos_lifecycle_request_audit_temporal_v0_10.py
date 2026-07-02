from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def temporal_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    review_completed = source[1].completed_at_epoch_seconds
    source_limit = source[4][1].package_expiry_at_epoch_seconds

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
        request_expiry_at_epoch_seconds=source_limit + 20,
        decision_deadline_at_epoch_seconds=source_limit + 1,
    )
    request = fixture.make_request_submission(
        source,
        evidence,
        decision_deadline_at_epoch_seconds=source_limit + 1,
    )
    source_late = fixture.evaluate_request(source, evidence, request)

    evidence = fixture.make_request_evidence(
        source,
        captured_at_epoch_seconds=fixture.completed_at - 301,
    )
    request = fixture.make_request_submission(source, evidence)
    stale = fixture.evaluate_request(source, evidence, request)

    evidence = fixture.make_request_evidence(
        source,
        request_expiry_at_epoch_seconds=fixture.completed_at - 1,
        decision_deadline_at_epoch_seconds=fixture.completed_at - 2,
    )
    request = fixture.make_request_submission(
        source,
        evidence,
        decision_deadline_at_epoch_seconds=fixture.completed_at - 2,
    )
    expired = fixture.evaluate_request(source, evidence, request)

    evidence = fixture.make_request_evidence(
        source,
        decision_deadline_at_epoch_seconds=fixture.completed_at,
    )
    request = fixture.make_request_submission(
        source,
        evidence,
        decision_deadline_at_epoch_seconds=fixture.completed_at,
    )
    deadline = fixture.evaluate_request(source, evidence, request)

    return {
        "request_delay_and_source_limit_boundaries": (
            delayed.status == REJECTED and source_late.status == REJECTED
        ),
        "freshness_expiry_and_deadline_boundaries": (
            stale.status == REJECTED
            and expired.status == REJECTED
            and deadline.status == REJECTED
        ),
    }
