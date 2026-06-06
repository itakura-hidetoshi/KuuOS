#!/usr/bin/env python3
"""Validate Regge Zero Governance v0.1 artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "REGGE_ZERO_GOVERNANCE_v0_1.md"
RUNBOOK = ROOT / "docs" / "REGGE_ZERO_GOVERNANCE_RUNBOOK_v0_1.md"
CONTRACT = ROOT / "contracts" / "kuos_regge_zero_governance_contract_v0_1.yaml"
CASES = ROOT / "validation_cases" / "regge_zero_governance_validation_cases_v0_1.yaml"
MANIFEST = ROOT / "manifests" / "regge_zero_governance_bundle_manifest_v0_1.json"
RUNNER_MANIFEST = ROOT / "manifests" / "regge_zero_governance_runner_manifest_v0_1.json"
PACKET = ROOT / "packets" / "regge_zero_governance_established_packet_v0_1.yaml"
CI_RECEIPT = ROOT / "packets" / "regge_zero_governance_ci_receipt_v0_1.yaml"
CHAIN_INDEX = ROOT / "chain_indexes" / "regge_zero_governance_chain_index_v0_1.yaml"
FORMAL = ROOT / "formal" / "ReggeZeroGovernance.lean"
RUNNER = ROOT / "scripts" / "run_regge_zero_governance_checks_v0_1.py"
REGRESSION = ROOT / "tests" / "test_regge_zero_governance_validator_v0_1.py"
WORKFLOW = ROOT / ".github" / "workflows" / "regge_zero_governance_validation.yml"
MAKEFILE = ROOT / "Makefile"

REQUIRED_INVARIANTS = [
    "minimal_null_constraint_only",
    "nested_null_inheritance",
    "no_extra_blocker_without_witness",
    "no_single_scalar_authority_collapse",
    "cyclic_consistency_required_for_promotion",
]

REQUIRED_CASE_IDS = {
    "pass_bounded_candidate_with_no_null_witness": "ADVISORY_ONLY",
    "hold_runtime_tick_authority_shortcut": "HOLD",
    "hold_qi_readout_medical_authorization_shortcut": "HOLD",
    "hold_ci_pass_theorem_authority_shortcut": "HOLD",
    "inherit_lower_tier_hold": "HOLD",
    "hold_cyclic_inconsistency": "HOLD",
    "reject_silent_root_rewrite": "REJECT",
}


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


def split_case_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    matches = list(re.finditer(r"^\s*- id: ([A-Za-z0-9_\-]+)\s*$", text, flags=re.MULTILINE))
    for idx, match in enumerate(matches):
        case_id = match.group(1)
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks[case_id] = text[start:end]
    return blocks


def validate_cases(text: str) -> List[str]:
    errors: List[str] = []
    blocks = split_case_blocks(text)
    for case_id, expected in REQUIRED_CASE_IDS.items():
        block = blocks.get(case_id)
        if block is None:
            errors.append(f"validation case missing: {case_id}")
            continue
        if f"expected: {expected}" not in block:
            errors.append(f"{case_id}: expected outcome must be {expected}")
    return errors


def validate_json_manifest(path: Path) -> List[str]:
    errors: List[str] = []
    try:
        manifest = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(ROOT)} is not valid JSON: {exc}"]
    for rel in manifest.get("paths", []):
        if not (ROOT / rel).exists():
            errors.append(f"manifest path missing: {rel}")
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(require_contains(read_text(DOC), ["Regge Zero Governance v0.1", "Only consistency-mandated null constraints may block a candidate"], "doc"))
    errors.extend(require_contains(read_text(RUNBOOK), ["Regge Zero Governance Runbook v0.1", "REGGE_ZERO_GOVERNANCE_VALIDATION: PASS"], "runbook"))
    errors.extend(require_contains(read_text(CONTRACT), ["id: kuos_regge_zero_governance_contract_v0_1", *REQUIRED_INVARIANTS], "contract"))
    errors.extend(validate_cases(read_text(CASES)))
    errors.extend(validate_json_manifest(MANIFEST))
    errors.extend(validate_json_manifest(RUNNER_MANIFEST))
    errors.extend(require_contains(read_text(PACKET), ["id: regge_zero_governance_established_packet_v0_1"], "packet"))
    errors.extend(require_contains(read_text(CI_RECEIPT), ["id: regge_zero_governance_ci_receipt_v0_1"], "ci_receipt"))
    errors.extend(require_contains(read_text(CHAIN_INDEX), ["id: regge_zero_governance_chain_index_v0_1"], "chain_index"))
    errors.extend(require_contains(read_text(FORMAL), ["namespace KuuOS", "namespace ReggeZeroGovernance", "def reggeZeroGate"], "formal"))
    errors.extend(require_contains(read_text(RUNNER), ["validate_regge_zero_governance_v0_1.py", "REGGE_ZERO_GOVERNANCE_CHECKS: PASS"], "runner"))
    errors.extend(require_contains(read_text(REGRESSION), ["REGGE_ZERO_GOVERNANCE_REGRESSION: PASS", "expected: ADVISORY_ONLY"], "regression"))
    errors.extend(require_contains(read_text(WORKFLOW), ["Regge Zero Governance Validation", "scripts/run_regge_zero_governance_checks_v0_1.py"], "workflow"))
    errors.extend(require_contains(read_text(MAKEFILE), ["regge-zero-governance-checks:", "scripts/run_regge_zero_governance_checks_v0_1.py"], "makefile"))

    if errors:
        print("REGGE_ZERO_GOVERNANCE_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REGGE_ZERO_GOVERNANCE_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
