from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import LifecycleBoundedRequestFixtureV010


def role_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    result = fixture.evaluate_request()
    return {
        "prior_chain_separation": result.checks["independent_from_prior_chain"],
        "decision_role_separation": (
            result.checks["independent_from_decision_authority"]
            and result.checks["independent_from_future_operator"]
            and result.checks["authority_operator_separated"]
        ),
    }
