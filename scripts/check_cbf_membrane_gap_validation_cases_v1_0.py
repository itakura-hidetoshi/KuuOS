#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES = ROOT / "manifests" / "cbf_membrane_gap_kernel_validation_cases_v1_0.json"

REQUIRED_CASE_IDS = {
    "cbf_pass_does_not_grant_execution",
    "cbf_pass_does_not_grant_truth",
    "grave_membrane_negative_margin_not_offset_by_average",
    "soft_slack_requires_residue",
    "belief_uncertainty_blocks_strong_pass",
    "local_pass_does_not_grant_global_pass",
    "cptp_pass_does_not_grant_membrane_pass",
    "positive_expectation_cannot_mask_negative_spectral_mass",
    "domain_unclear_blocks_strong_pass",
    "projected_pass_with_large_distortion_is_hold",
}

VALID_DECISIONS = {
    "PASS_NOMINAL",
    "PASS_PROJECTED",
    "PASS_WITH_RESIDUE",
    "PASS_BUT_THIN",
    "PASS_WITH_UNCERTAINTY",
    "LOCAL_PASS_GLOBAL_HOLD",
    "REOBSERVE_REQUIRED",
    "REDECOMPOSE_REQUIRED",
    "RECOVERY_MODE_REQUIRED",
    "HOLD_MEMBRANE_THIN",
    "HOLD_DOMAIN_UNCLEAR",
    "BLOCK_MEMBRANE_BREACH",
    "BLOCK_NEGATIVE_SPECTRAL_MASS",
    "BLOCK_AUTHORITY_BOUNDARY",
    "HANDOVER_REQUIRED",
}

MUST_BLOCK_CASES = {
    "cbf_pass_does_not_grant_execution",
    "cbf_pass_does_not_grant_truth",
    "grave_membrane_negative_margin_not_offset_by_average",
    "local_pass_does_not_grant_global_pass",
    "cptp_pass_does_not_grant_membrane_pass",
    "positive_expectation_cannot_mask_negative_spectral_mass",
    "domain_unclear_blocks_strong_pass",
    "projected_pass_with_large_distortion_is_hold",
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def main() -> int:
    errors: list[str] = []
    if not CASES.exists():
        print("ERROR: missing CBF validation cases")
        return 1

    data = json.loads(CASES.read_text(encoding="utf-8"))
    if data.get("validation_cases_version") != "cbf_membrane_gap_kernel_validation_cases_v1_0":
        errors.append("bad validation_cases_version")

    cases = _as_list(data.get("cases"))
    case_by_id = {case.get("case_id"): case for case in cases if isinstance(case, dict)}
    for case_id in sorted(REQUIRED_CASE_IDS - set(case_by_id)):
        errors.append(f"missing validation case: {case_id}")

    for case_id, case in case_by_id.items():
        if not isinstance(case.get("input"), dict):
            errors.append(f"case missing input: {case_id}")
        expected = case.get("expected")
        if not isinstance(expected, dict):
            errors.append(f"case missing expected: {case_id}")
            continue
        decision = expected.get("decision")
        if decision not in VALID_DECISIONS:
            errors.append(f"case has invalid decision: {case_id}: {decision}")
        if not isinstance(expected.get("reason_code"), str) or not expected.get("reason_code"):
            errors.append(f"case missing reason_code: {case_id}")
        if case_id in MUST_BLOCK_CASES and expected.get("allowed") is not False:
            errors.append(f"case must not allow unsafe collapse: {case_id}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: CBF membrane gap validation cases v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
