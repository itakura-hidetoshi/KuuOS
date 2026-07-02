from dataclasses import replace

from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import (
    REJECTED,
    submission_digest,
)
from runtime.kuuos_lifecycle_review_types_v0_9 import (
    lifecycle_review_record_digest,
)
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def integrity_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()

    changed_record = replace(source[3], reason="changed-after-review", record_digest="")
    changed_record = replace(
        changed_record,
        record_digest=lifecycle_review_record_digest(changed_record),
    )
    changed_source = source[:3] + (changed_record, source[4])
    changed_result = fixture.evaluate_request(source=changed_source)

    evidence = fixture.make_request_evidence(source)
    digests = dict(evidence.source_artifact_digests)
    digests["review_record"] = "0" * 64
    rebound_evidence = fixture.make_request_evidence(
        source,
        source_artifact_digests=digests,
    )
    rebound_request = fixture.make_request_submission(source, rebound_evidence)
    rebound_result = fixture.evaluate_request(
        source,
        rebound_evidence,
        rebound_request,
    )

    request = fixture.make_request_submission(source, evidence)
    request = replace(
        request,
        request_evidence_digest="0" * 64,
        request_digest="",
    )
    request = replace(request, request_digest=submission_digest(request))
    request_result = fixture.evaluate_request(source, evidence, request)

    return {
        "fresh_digest_source_change": (
            changed_result.status == REJECTED
            and not changed_result.checks["source_recomputed_valid"]
        ),
        "source_artifact_binding": (
            rebound_result.status == REJECTED
            and not rebound_result.checks["source_binding_valid"]
        ),
        "request_evidence_binding": (
            request_result.status == REJECTED
            and not request_result.checks["identity_binding_valid"]
        ),
    }
