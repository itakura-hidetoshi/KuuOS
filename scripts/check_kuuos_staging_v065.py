#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT, REJECT
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from runtime.kuuos_connection_case_evaluation_v0_64 import evaluate_connection_candidate_cases
from runtime.kuuos_connection_staging_types_v0_65 import BLOCKED, READY
from runtime.kuuos_connection_staging_v0_65 import (
    build_connection_staging_package,
    validate_connection_staging_package,
)
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def evaluated(decision: str):
    bundle, _, _ = fixture()
    proposal, request, packet = review_fixture(decision)
    admission = evaluate_connection_admission(
        proposal,
        request,
        packet,
        current_epoch=15,
    )
    evaluation = evaluate_connection_candidate_cases(
        bundle,
        proposal,
        admission,
        {"baseline": bundle},
    )
    return bundle, proposal, admission, evaluation


def main() -> int:
    checks: list[str] = []

    bundle, proposal, admission, evaluation = evaluated(ADMIT)
    package = build_connection_staging_package(
        bundle,
        proposal,
        admission,
        evaluation,
        package_id="connection-stage-v065",
        staging_namespace="shadow/gauge-connection-v065",
    )
    assert package.status == READY
    assert validate_connection_staging_package(package) == ()
    assert package.production_apply_allowed is False
    assert package.state_write_allowed is False
    assert package.authority_widening_allowed is False
    checks.append("sealed")

    invalid_namespace = build_connection_staging_package(
        bundle,
        proposal,
        admission,
        evaluation,
        package_id="connection-stage-v065-invalid",
        staging_namespace="production/gauge-connection-v065",
    )
    assert invalid_namespace.status == BLOCKED
    checks.append("namespace")

    changed_payload = dict(package.candidate_connection_payload)
    changed_payload["unexpected"] = True
    tampered = replace(package, candidate_connection_payload=changed_payload)
    assert "staging_package_digest_invalid" in validate_connection_staging_package(tampered)
    checks.append("tamper")

    bundle, proposal, admission, evaluation = evaluated(REJECT)
    rejected = build_connection_staging_package(
        bundle,
        proposal,
        admission,
        evaluation,
        package_id="connection-stage-v065-rejected",
        staging_namespace="shadow/rejected",
    )
    assert rejected.status == BLOCKED
    checks.append("review")

    print(json.dumps({
        "status": "KUUOS_V0_65_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
