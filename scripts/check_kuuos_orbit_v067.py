#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from runtime.kuuos_connection_case_evaluation_v0_64 import evaluate_connection_candidate_cases
from runtime.kuuos_connection_orbit_types_v0_67 import BLOCKED, READY
from runtime.kuuos_connection_orbit_validation_v0_67 import validate_connection_orbit
from runtime.kuuos_connection_shadow_v0_66 import materialize_connection_shadow
from runtime.kuuos_connection_staging_v0_65 import build_connection_staging_package
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def shadow_chain():
    bundle, _, swap = fixture()
    proposal, request, packet = review_fixture(ADMIT)
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
        package_id="orbit-stage-v067",
        staging_namespace="shadow/orbit-v067",
    )
    shadow, receipt = materialize_connection_shadow(bundle, proposal, package)
    assert shadow is not None
    return bundle, shadow, receipt, swap


def main() -> int:
    checks: list[str] = []
    source, shadow, receipt, swap = shadow_chain()
    identity = source.group.identity()
    source_before = canonical_digest(source.to_dict())

    result = validate_connection_orbit(
        source,
        shadow,
        receipt,
        {
            "identity": {},
            "channel-gauge": {
                "observe": swap,
                "verify": identity,
                "memory": swap,
            },
        },
    )
    assert result.status == READY
    assert result.sample_count == 2
    assert result.all_samples_admissible
    assert result.rollback_reconstruction_exact
    assert result.source_unchanged
    assert result.production_apply_ready is False
    assert result.state_write_performed is False
    assert result.authority_widened is False
    assert canonical_digest(source.to_dict()) == source_before
    checks.append("orbit")

    empty = validate_connection_orbit(source, shadow, receipt, {})
    assert empty.status == BLOCKED
    checks.append("empty")

    changed_receipt = replace(receipt, receipt_digest="other")
    changed = validate_connection_orbit(
        source,
        shadow,
        changed_receipt,
        {"identity": {}},
    )
    assert changed.status == BLOCKED
    checks.append("receipt")

    print(json.dumps({
        "status": "KUUOS_V0_67_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
