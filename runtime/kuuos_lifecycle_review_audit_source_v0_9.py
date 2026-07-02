from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    apoptosis_bounded_execution_preparation_record_digest,
)
from runtime.kuuos_lifecycle_review_types_v0_9 import (
    CLEAR,
    REJECTED,
    lifecycle_review_evidence_digest,
    lifecycle_review_request_digest,
)
from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


def source_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleReviewFixtureV09(methodName="runTest")
    fixture.setUp()
    results: dict[str, bool] = {}

    valid = fixture.review()
    results["valid_clear"] = (
        valid.status == CLEAR
        and valid.review_record_issued
        and valid.review_completed
        and valid.clear_for_next_request_layer
        and valid.next_request_layer_required
        and valid.effect_free
        and valid.read_only
    )

    blocked = fixture.make_bundle(
        preparation_overrides={"simulation_verified": False}
    )
    blocked_result = fixture.review(blocked)
    results["blocked_source_rejected"] = (
        blocked_result.status == REJECTED
        and not blocked_result.checks["source_preparation_ready"]
        and not blocked_result.review_record_issued
    )

    denied = fixture.make_bundle(
        authorization_overrides={"quorum_satisfied": False}
    )
    denied_result = fixture.review(denied)
    results["denied_source_rejected"] = (
        denied_result.status == REJECTED
        and not denied_result.checks["source_preparation_ready"]
    )

    bundle = fixture.make_bundle()
    altered_record = replace(
        bundle[3],
        bounded_execution_package_prepared=False,
        record_digest="",
    )
    altered_record = replace(
        altered_record,
        record_digest=apoptosis_bounded_execution_preparation_record_digest(
            altered_record
        ),
    )
    changed = bundle[:3] + (altered_record, bundle[4])
    changed_result = fixture.review(changed)
    results["fresh_digest_source_change_rejected"] = (
        changed_result.status == REJECTED
        and not changed_result.checks["source_recomputed_valid"]
    )

    evidence = fixture.make_evidence(bundle)
    digests = dict(evidence.source_artifact_digests)
    digests["observation_record"] = "x" * 64
    altered_evidence = replace(
        evidence,
        source_artifact_digests=digests,
        evidence_digest="",
    )
    altered_evidence = replace(
        altered_evidence,
        evidence_digest=lifecycle_review_evidence_digest(altered_evidence),
    )
    binding_result = fixture.review(
        bundle,
        altered_evidence,
        fixture.make_request(bundle, altered_evidence),
    )
    results["source_binding_rejected"] = (
        binding_result.status == REJECTED
        and not binding_result.checks["source_binding_valid"]
    )

    request = fixture.make_request(bundle, evidence)
    altered_request = replace(
        request,
        review_evidence_digest="y" * 64,
        request_digest="",
    )
    altered_request = replace(
        altered_request,
        request_digest=lifecycle_review_request_digest(altered_request),
    )
    request_result = fixture.review(bundle, evidence, altered_request)
    results["request_binding_rejected"] = (
        request_result.status == REJECTED
        and not request_result.checks["identity_binding_valid"]
    )

    return results
