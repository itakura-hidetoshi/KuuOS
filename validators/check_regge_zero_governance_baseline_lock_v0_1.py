#!/usr/bin/env python3
"""Check Regge Zero Governance baseline lock v0.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]

LOCK = ROOT / "packets" / "regge_zero_governance_baseline_lock_v0_1.yaml"
MANIFEST = ROOT / "manifests" / "regge_zero_governance_bundle_manifest_v0_1.json"
RUNNER_MANIFEST = ROOT / "manifests" / "regge_zero_governance_runner_manifest_v0_1.json"
RUNNER = ROOT / "scripts" / "run_regge_zero_governance_checks_v0_1.py"
WORKFLOW = ROOT / ".github" / "workflows" / "regge_zero_governance_validation.yml"
CI_RECEIPT = ROOT / "packets" / "regge_zero_governance_ci_receipt_v0_1.yaml"

REQUIRED_LOCK_TOKENS = [
    "id: regge_zero_governance_baseline_lock_v0_1",
    "status: additive_baseline_lock",
    "minimal_null_constraint_only",
    "nested_null_inheritance",
    "no_extra_blocker_without_witness",
    "no_single_scalar_authority_collapse",
    "cyclic_consistency_required_for_promotion",
    "append_only: true",
    "same_root_required: true",
    "overwrite_forbidden: true",
    "destructive_replacement_forbidden: true",
    "authority_expansion_forbidden: true",
    "v0_1_overwrite_forbidden: true",
    "v0_2_plus_additive_extension_allowed: true",
]

REQUIRED_MANIFEST_PATHS = [
    "packets/regge_zero_governance_baseline_lock_v0_1.yaml",
    "validators/check_regge_zero_governance_baseline_lock_v0_1.py",
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


def validate_manifest() -> List[str]:
    errors: List[str] = []
    try:
        manifest = json.loads(read_text(MANIFEST))
    except json.JSONDecodeError as exc:
        return [f"manifest is not valid JSON: {exc}"]
    paths = manifest.get("paths", [])
    for rel in REQUIRED_MANIFEST_PATHS:
        if rel not in paths:
            errors.append(f"manifest missing baseline lock path: {rel}")
        if not (ROOT / rel).exists():
            errors.append(f"manifest baseline lock path does not exist: {rel}")
    return errors


def validate_links() -> List[str]:
    errors: List[str] = []
    errors.extend(require_contains(read_text(RUNNER), ["check_regge_zero_governance_baseline_lock_v0_1.py"], "runner"))
    errors.extend(require_contains(read_text(RUNNER_MANIFEST), ["check_regge_zero_governance_baseline_lock_v0_1.py"], "runner_manifest"))
    errors.extend(require_contains(read_text(WORKFLOW), ["check_regge_zero_governance_baseline_lock_v0_1.py", "packets/regge_zero_governance_baseline_lock_v0_1.yaml"], "workflow"))
    errors.extend(require_contains(read_text(CI_RECEIPT), ["baseline_lock: packets/regge_zero_governance_baseline_lock_v0_1.yaml", "baseline_lock_validator: validators/check_regge_zero_governance_baseline_lock_v0_1.py"], "ci_receipt"))
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(require_contains(read_text(LOCK), REQUIRED_LOCK_TOKENS, "baseline_lock"))
    errors.extend(validate_manifest())
    errors.extend(validate_links())
    if errors:
        print("REGGE_ZERO_GOVERNANCE_BASELINE_LOCK_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REGGE_ZERO_GOVERNANCE_BASELINE_LOCK_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
