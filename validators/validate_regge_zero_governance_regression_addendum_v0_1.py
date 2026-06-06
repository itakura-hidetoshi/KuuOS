#!/usr/bin/env python3
"""Validate Regge Zero Governance regression addendum v0.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]

ADDENDUM = ROOT / "chain_indexes" / "regge_zero_governance_regression_addendum_v0_1.yaml"
MANIFEST = ROOT / "manifests" / "regge_zero_governance_bundle_manifest_v0_1.json"
RUNNER = ROOT / "scripts" / "run_regge_zero_governance_checks_v0_1.py"
REGRESSION = ROOT / "tests" / "test_regge_zero_governance_validator_v0_1.py"
WORKFLOW = ROOT / ".github" / "workflows" / "regge_zero_governance_validation.yml"
CI_RECEIPT = ROOT / "packets" / "regge_zero_governance_ci_receipt_v0_1.yaml"

REQUIRED_PATHS = [
    "chain_indexes/regge_zero_governance_regression_addendum_v0_1.yaml",
    "tests/test_regge_zero_governance_validator_v0_1.py",
    "scripts/run_regge_zero_governance_checks_v0_1.py",
    ".github/workflows/regge_zero_governance_validation.yml",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_contains(text: str, needles: Iterable[str], label: str) -> List[str]:
    errors: List[str] = []
    for needle in needles:
        if needle not in text:
            errors.append(f"{label} missing required text: {needle}")
    return errors


def validate_addendum() -> List[str]:
    text = read_text(ADDENDUM)
    return require_contains(
        text,
        [
            "id: regge_zero_governance_regression_addendum_v0_1",
            "parent_chain: regge_zero_governance_chain_index_v0_1",
            "same_root_required: true",
            "overwrite_forbidden: true",
            "dependency_free_regression_test",
            "runner_invokes_regression_test",
            "workflow_triggers_on_regression_test",
        ],
        "regression_addendum",
    )


def validate_manifest() -> List[str]:
    errors: List[str] = []
    try:
        manifest = json.loads(read_text(MANIFEST))
    except json.JSONDecodeError as exc:
        return [f"manifest is not valid JSON: {exc}"]
    paths = manifest.get("paths", [])
    for rel in REQUIRED_PATHS:
        if rel not in paths:
            errors.append(f"manifest missing regression addendum path: {rel}")
        if not (ROOT / rel).exists():
            errors.append(f"manifest regression path does not exist: {rel}")
    return errors


def validate_runtime_links() -> List[str]:
    errors: List[str] = []
    errors.extend(require_contains(read_text(RUNNER), ["tests/test_regge_zero_governance_validator_v0_1.py"], "runner"))
    errors.extend(require_contains(read_text(REGRESSION), ["REGGE_ZERO_GOVERNANCE_REGRESSION: PASS", "expected: ADVISORY_ONLY"], "regression"))
    errors.extend(require_contains(read_text(WORKFLOW), ["tests/test_regge_zero_governance_validator_v0_1.py", "chain_indexes/regge_zero_governance_regression_addendum_v0_1.yaml"], "workflow"))
    errors.extend(require_contains(read_text(CI_RECEIPT), ["regression_test: tests/test_regge_zero_governance_validator_v0_1.py", "dedicated_workflow_runs_regression: true"], "ci_receipt"))
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(validate_addendum())
    errors.extend(validate_manifest())
    errors.extend(validate_runtime_links())
    if errors:
        print("REGGE_ZERO_GOVERNANCE_REGRESSION_ADDENDUM_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REGGE_ZERO_GOVERNANCE_REGRESSION_ADDENDUM_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
