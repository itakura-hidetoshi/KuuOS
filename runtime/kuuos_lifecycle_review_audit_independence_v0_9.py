from __future__ import annotations

from runtime.kuuos_lifecycle_review_chain_v0_9 import named_source
from runtime.kuuos_lifecycle_review_types_v0_9 import CLEAR, REJECTED
from tests.kuuos_lifecycle_review_fixture_v0_9 import LifecycleReviewFixtureV09


def independence_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleReviewFixtureV09(methodName="runTest")
    fixture.setUp()
    results: dict[str, bool] = {}
    bundle = fixture.make_bundle()
    evidence = fixture.make_evidence(bundle)

    reviewer_request = fixture.make_request(
        bundle,
        evidence,
        reviewer_id="unknown-reviewer",
    )
    reviewer_result = fixture.review(bundle, evidence, reviewer_request)
    results["reviewer_allowlist"] = reviewer_result.status == REJECTED

    organization_request = fixture.make_request(
        bundle,
        evidence,
        reviewer_organization_id="unknown-organization",
    )
    organization_result = fixture.review(
        bundle,
        evidence,
        organization_request,
    )
    results["organization_allowlist"] = organization_result.status == REJECTED

    objective_request = fixture.make_request(
        bundle,
        evidence,
        objective="UNAUTHORIZED_OBJECTIVE",
    )
    objective_result = fixture.review(bundle, evidence, objective_request)
    results["objective_allowlist"] = objective_result.status == REJECTED

    named = named_source(bundle[4])
    identities = {
        bundle[3].subject_id,
        bundle[3].preparer_id,
        fixture.operator_id,
        named["candidate_record"].issuer_id,
        named["dependency_record"].reviewer_id,
        named["authority_record"].reviewer_id,
        named["authority_evidence"].responsible_authority_id,
        named["quiescence_record"].reviewer_id,
        named["external_record"].reviewer_id,
        named["external_evidence"].quiescence_evidence_producer_id,
        named["authorization_record"].authority_id,
    }
    independent = True
    for identity in identities:
        changed_evidence = fixture.make_evidence(bundle, reviewer_id=identity)
        changed_request = fixture.make_request(
            bundle,
            changed_evidence,
            reviewer_id=identity,
        )
        changed_result = fixture.review(
            bundle,
            changed_evidence,
            changed_request,
        )
        independent = independent and changed_result.status == REJECTED
    results["reviewer_independence"] = independent

    authority = bundle[3].future_execution_authority_id
    authority_evidence = fixture.make_evidence(bundle, reviewer_id=authority)
    authority_request = fixture.make_request(
        bundle,
        authority_evidence,
        reviewer_id=authority,
    )
    authority_result = fixture.review(
        bundle,
        authority_evidence,
        authority_request,
    )
    results["designated_authority_may_review"] = (
        authority_result.status == CLEAR
        and authority_result.checks["authority_operator_separated"]
        and authority_result.checks["independent_from_execution_operator"]
    )

    same_evidence = fixture.make_evidence(
        bundle,
        future_execution_operator_id=authority,
    )
    same_request = fixture.make_request(
        bundle,
        same_evidence,
        future_execution_operator_id=authority,
    )
    same_result = fixture.review(bundle, same_evidence, same_request)
    results["authority_operator_separation"] = (
        same_result.status == REJECTED
        and not same_result.checks["authority_operator_separated"]
    )

    return results
