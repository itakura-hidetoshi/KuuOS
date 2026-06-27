#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT, REJECT
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from runtime.kuuos_connection_case_evaluation_v0_64 import evaluate_connection_candidate_cases
from runtime.kuuos_connection_shadow_types_v0_66 import BLOCKED, READY
from runtime.kuuos_connection_shadow_v0_66 import materialize_connection_shadow
from runtime.kuuos_connection_staging_v0_65 import build_connection_staging_package
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def staged(decision: str):
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
    package = build_connection_staging_package(
        bundle,
        proposal,
        admission,
        evaluation,
        package_id=f"shadow-package-{decision.lower()}",
        staging_namespace=f"shadow/materialization-{decision.lower()}",
    )
    return bundle, proposal, package


def main() -> int:
    checks: list[str] = []

    bundle, proposal, package = staged(ADMIT)
    before = canonical_digest(bundle.to_dict())
    shadow, receipt = materialize_connection_shadow(bundle, proposal, package)
    after = canonical_digest(bundle.to_dict())
    assert receipt.status == READY
    assert shadow is not None
    assert before == after
    assert receipt.source_unchanged
    assert receipt.rollback_witness_ready
    assert receipt.curvature_nonincreasing
    assert receipt.memory_holonomy_preserved
    assert receipt.production_apply_ready is False
    assert receipt.state_write_performed is False
    assert receipt.authority_widened is False
    checks.append("shadow")

    tampered = replace(package, candidate_connection_digest="other")
    shadow, receipt = materialize_connection_shadow(bundle, proposal, tampered)
    assert shadow is None
    assert receipt.status == BLOCKED
    checks.append("tamper")

    bundle, proposal, package = staged(REJECT)
    shadow, receipt = materialize_connection_shadow(bundle, proposal, package)
    assert shadow is None
    assert receipt.status == BLOCKED
    checks.append("review")

    print(json.dumps({
        "status": "KUUOS_V0_66_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
