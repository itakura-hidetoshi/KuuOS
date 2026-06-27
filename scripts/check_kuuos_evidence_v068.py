#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from runtime.kuuos_connection_case_evaluation_v0_64 import evaluate_connection_candidate_cases
from runtime.kuuos_connection_evidence_types_v0_68 import BLOCKED, READY
from runtime.kuuos_connection_evidence_v0_68 import (
    build_connection_evidence_capsule,
    validate_connection_evidence_capsule,
)
from runtime.kuuos_connection_orbit_validation_v0_67 import validate_connection_orbit
from runtime.kuuos_connection_shadow_v0_66 import materialize_connection_shadow
from runtime.kuuos_connection_staging_v0_65 import build_connection_staging_package
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def evidence_chain():
    source, _, swap = fixture()
    proposal, request, packet = review_fixture(ADMIT)
    admission = evaluate_connection_admission(
        proposal,
        request,
        packet,
        current_epoch=15,
    )
    evaluation = evaluate_connection_candidate_cases(
        source,
        proposal,
        admission,
        {"baseline": source},
    )
    package = build_connection_staging_package(
        source,
        proposal,
        admission,
        evaluation,
        package_id="evidence-stage-v068",
        staging_namespace="shadow/evidence-v068",
    )
    shadow, shadow_receipt = materialize_connection_shadow(source, proposal, package)
    assert shadow is not None
    gauge_validation = validate_connection_orbit(
        source,
        shadow,
        shadow_receipt,
        {
            "identity": {},
            "channel-gauge": {
                "observe": swap,
                "memory": swap,
            },
        },
    )
    return source, shadow, shadow_receipt, gauge_validation


def main() -> int:
    source, shadow, shadow_receipt, gauge_validation = evidence_chain()
    checks: list[str] = []

    capsule = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        capsule_id="connection-evidence-v068",
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    assert capsule.status == READY
    assert validate_connection_evidence_capsule(
        capsule,
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        current_epoch=15,
    ) == ()
    assert capsule.evidence_only
    assert capsule.live_effect_allowed is False
    assert capsule.state_write_allowed is False
    assert capsule.authority_widening_allowed is False
    checks.append("ready")

    expired = validate_connection_evidence_capsule(
        capsule,
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        current_epoch=21,
    )
    assert "evidence_capsule_outside_validity_window" in expired
    checks.append("expiry")

    tampered = replace(capsule, sample_count=capsule.sample_count + 1)
    changed = validate_connection_evidence_capsule(
        tampered,
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        current_epoch=15,
    )
    assert "evidence_capsule_digest_invalid" in changed
    checks.append("tamper")

    invalid_window = build_connection_evidence_capsule(
        source,
        shadow,
        shadow_receipt,
        gauge_validation,
        capsule_id="invalid-window-v068",
        valid_from_epoch=20,
        valid_through_epoch=10,
    )
    assert invalid_window.status == BLOCKED
    checks.append("window")

    print(json.dumps({
        "status": "KUUOS_V0_68_VALIDATED",
        "checks": checks,
        "check_count": len(checks),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
