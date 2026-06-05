#!/usr/bin/env python3
"""Check Regge Zero Governance finality packet v0.1.

Dependency-free finality check.  This is a non-authoritative closure validator:
finality is checked as a governance receipt, not as truth, theorem authority,
execution authority, or medical authorization.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]

FINALITY = ROOT / "packets" / "regge_zero_governance_finality_packet_v0_1.yaml"
MANIFEST = ROOT / "manifests" / "regge_zero_governance_bundle_manifest_v0_1.json"
RUNNER_MANIFEST = ROOT / "manifests" / "regge_zero_governance_runner_manifest_v0_1.json"
RUNNER = ROOT / "scripts" / "run_regge_zero_governance_checks_v0_1.py"
WORKFLOW = ROOT / ".github" / "workflows" / "regge_zero_governance_validation.yml"
CI_RECEIPT = ROOT / "packets" / "regge_zero_governance_ci_receipt_v0_1.yaml"

REQUIRED_FINALITY_TOKENS = [
    "id: regge_zero_governance_finality_packet_v0_1",
    "status: additive_finality_packet",
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
    "finality_not_truth: true",
    "finality_not_theorem_authority: true",
    "finality_not_execution_authority: true",
    "finality_not_medical_authorization: true",
    "truth_authority: false",
    "theorem_authority: false",
    "execution_authority: false",
    "medical_authorization: false",
    "Finality does not prove string theory.",
    "Finality does not turn validation into truth.",
]

REQUIRED_PATHS = [
    "packets/regge_zero_governance_finality_packet_v0_1.yaml",
    "validators/check_regge_zero_governance_finality_packet_v0_1.py",
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
    for rel in REQUIRED_PATHS:
        if rel not in paths:
            errors.append(f"manifest missing finality path: {rel}")
        if not (ROOT / rel).exists():
            errors.append(f"manifest finality path does not exist: {rel}")
    if manifest.get("authority") != "non_authoritative_governance_addendum":
        errors.append("manifest authority must remain non_authoritative_governance_addendum")
    locks = manifest.get("semantic_locks", {})
    for key in ["append_only", "same_root_required", "overwrite_forbidden", "authority_expansion_forbidden"]:
        if locks.get(key) is not True:
            errors.append(f"manifest semantic_locks.{key} must be true")
    for key in ["execution_authority_created", "medical_authorization_created", "theorem_authority_created"]:
        if locks.get(key) is not False:
            errors.append(f"manifest semantic_locks.{key} must be false")
    return errors


def validate_links() -> List[str]:
    errors: List[str] = []
    errors.extend(require_contains(read_text(RUNNER), ["check_regge_zero_governance_finality_packet_v0_1.py"], "runner"))
    errors.extend(require_contains(read_text(RUNNER_MANIFEST), ["check_regge_zero_governance_finality_packet_v0_1.py"], "runner_manifest"))
    errors.extend(require_contains(read_text(WORKFLOW), ["check_regge_zero_governance_finality_packet_v0_1.py", "packets/regge_zero_governance_finality_packet_v0_1.yaml"], "workflow"))
    errors.extend(require_contains(read_text(CI_RECEIPT), ["finality_validator: validators/check_regge_zero_governance_finality_packet_v0_1.py", "finality_packet: packets/regge_zero_governance_finality_packet_v0_1.yaml"], "ci_receipt"))
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(require_contains(read_text(FINALITY), REQUIRED_FINALITY_TOKENS, "finality_packet"))
    errors.extend(validate_manifest())
    errors.extend(validate_links())
    if errors:
        print("REGGE_ZERO_GOVERNANCE_FINALITY_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REGGE_ZERO_GOVERNANCE_FINALITY_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
