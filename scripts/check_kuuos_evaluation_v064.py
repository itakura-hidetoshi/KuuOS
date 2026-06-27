#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT, REJECT
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from runtime.kuuos_connection_case_evaluation_v0_64 import evaluate_connection_candidate_cases
from runtime.kuuos_connection_evaluation_types_v0_64 import BLOCKED_STATUS, READY_STATUS
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def evaluate(decision: str):
    proposal, request, packet = review_fixture(decision)
    receipt = evaluate_connection_admission(proposal, request, packet, current_epoch=15)
    return proposal, receipt


def main() -> int:
    bundle, _, _ = fixture()
    checks = []

    proposal, receipt = evaluate(ADMIT)
    result = evaluate_connection_candidate_cases(
        bundle,
        proposal,
        receipt,
        {"baseline": bundle},
    )
    assert result.status == READY_STATUS
    assert result.all_cases_admissible
    assert result.strict_improvement_observed
    checks.append("ready")

    proposal, receipt = evaluate(REJECT)
    result = evaluate_connection_candidate_cases(
        bundle,
        proposal,
        receipt,
        {"baseline": bundle},
    )
    assert result.status == BLOCKED_STATUS
    checks.append("rejected")

    proposal, receipt = evaluate(ADMIT)
    result = evaluate_connection_candidate_cases(bundle, proposal, receipt, {})
    assert result.status == BLOCKED_STATUS
    checks.append("empty")

    print(json.dumps({"status": "KUUOS_V0_64_VALIDATED", "checks": checks}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
