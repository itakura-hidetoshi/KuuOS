from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import ISSUED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def valid_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    result = fixture.evaluate_request()
    return {
        "valid_issued": (
            result.status == ISSUED
            and result.request_record_issued
            and result.bounded_request_issued
            and result.ready_for_decision_review
            and result.decision_review_required_next
        )
    }
