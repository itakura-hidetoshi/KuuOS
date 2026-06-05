#!/usr/bin/env python3
"""Regression tests for Regge Zero Governance v0.1.

These tests intentionally use only the Python standard library so the dedicated
GitHub Actions lane can run without dependency installation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "validators" / "validate_regge_zero_governance_v0_1.py"
CONTRACT = ROOT / "contracts" / "kuos_regge_zero_governance_contract_v0_1.yaml"
CASES = ROOT / "validation_cases" / "regge_zero_governance_validation_cases_v0_1.yaml"
RUNNER = ROOT / "scripts" / "run_regge_zero_governance_checks_v0_1.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    require(result.returncode == 0, result.stdout)
    require("REGGE_ZERO_GOVERNANCE_VALIDATION: PASS" in result.stdout, result.stdout)


def test_contract_preserves_minimal_null_and_non_authority() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    for token in [
        "minimal_null_constraint_only",
        "nested_null_inheritance",
        "no_extra_blocker_without_witness",
        "no_single_scalar_authority_collapse",
        "candidate_not_authority: true",
        "validation_not_truth: true",
        "ci_pass_not_theorem_authority: true",
        "runtime_tick_not_autonomous_execution_authority: true",
        "qi_readout_not_intervention_license: true",
    ]:
        require(token in text, f"missing contract token: {token}")


def test_validation_cases_keep_soft_concern_advisory_only() -> None:
    text = CASES.read_text(encoding="utf-8")
    marker = "id: pass_bounded_candidate_with_no_null_witness"
    require(marker in text, "missing soft-concern validation case")
    block = text.split(marker, 1)[1].split("\n  - id:", 1)[0]
    require("novelty" in block, "soft-concern case must include novelty")
    require("expected: ADVISORY_ONLY" in block, "novelty-only case must remain advisory-only")


def test_runner_invokes_validator() -> None:
    text = RUNNER.read_text(encoding="utf-8")
    require("validate_regge_zero_governance_v0_1.py" in text, "runner must invoke validator")
    require("REGGE_ZERO_GOVERNANCE_CHECKS: PASS" in text, "runner must expose pass receipt")


def main() -> int:
    tests = [
        test_validator_passes,
        test_contract_preserves_minimal_null_and_non_authority,
        test_validation_cases_keep_soft_concern_advisory_only,
        test_runner_invokes_validator,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as exc:  # pragma: no cover - script-style test harness
            failures.append(f"{test.__name__}: {exc}")
            print(f"FAIL: {test.__name__}: {exc}")
    if failures:
        print("REGGE_ZERO_GOVERNANCE_REGRESSION: FAIL")
        return 1
    print("REGGE_ZERO_GOVERNANCE_REGRESSION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
