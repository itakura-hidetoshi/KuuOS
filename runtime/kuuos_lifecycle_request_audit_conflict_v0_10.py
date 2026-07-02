from runtime.kuuos_lifecycle_bounded_request_types_v0_10 import BLOCKED
from tests.kuuos_lifecycle_bounded_request_fixture_v0_10 import (
    LifecycleBoundedRequestFixtureV010,
)


def conflict_audit_matrix() -> dict[str, bool]:
    fixture = LifecycleBoundedRequestFixtureV010(methodName="runTest")
    fixture.setUp()
    source = fixture.make_source()
    results: dict[str, bool] = {}

    evidence = fixture.make_request_evidence(
        source,
        conflict_disclosure_complete=False,
    )
    request = fixture.make_request_submission(source, evidence)
    disclosure = fixture.evaluate_request(source, evidence, request)
    results["conflict_disclosure_blocker"] = (
        disclosure.status == BLOCKED
        and disclosure.reason == "conflict_disclosure_complete"
    )

    evidence = fixture.make_request_evidence(
        source,
        material_conflict_present=True,
    )
    request = fixture.make_request_submission(source, evidence)
    material = fixture.evaluate_request(source, evidence, request)
    results["material_conflict_blocker"] = (
        material.status == BLOCKED
        and material.reason == "material_conflict_absent"
    )
    return results
