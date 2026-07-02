from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import REJECTED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def source_status_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    blocked_source = fixture.make_source(
        review_evidence_overrides={"reviewer_qualification_verified": False}
    )
    blocked_result = fixture.evaluate_request(source=blocked_source)
    rejected_source = fixture.make_source(
        review_request_overrides={"objective": "INVALID_REVIEW_OBJECTIVE"}
    )
    rejected_result = fixture.evaluate_request(source=rejected_source)
    return {
        "blocked_source_rejected": (
            blocked_result.status == REJECTED
            and not blocked_result.checks["source_review_clear"]
        ),
        "rejected_source_rejected": (
            rejected_result.status == REJECTED
            and not rejected_result.checks["source_review_clear"]
        ),
    }
