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
ALL_RUNNER = ROOT / "scripts" / "run_all_governance_full_checks_v0_1.py"
MAKEFILE = ROOT / "Makefile"

REQUIRED_NON_AUTHORITY = [
    "candidate_not_authority: true",
    "validation_not_truth: true",
    "ci_pass_not_theorem_authority: true",
    "runtime_tick_not_autonomous_execution_authority: true",
    "qi_readout_not_intervention_license: true",
    "memory_persistence_not_belief_sovereignty: true",
    "reflection_summary_not_root_rewrite: true",
    "audit_not_infinite_escalation: true",
]

REQUIRED_INVARIANTS = [
    "minimal_null_constraint_only",
    "nested_null_inheritance",
    "no_extra_blocker_without_witness",
    "no_single_scalar_authority_collapse",
    "cyclic_consistency_required_for_promotion",
]

REQUIRED_NULL_CONDITIONS = [
    "authority_shortcut:",
    "proof_shortcut:",
    "qi_intervention_shortcut:",
    "memory_sovereignty_shortcut:",
    "over_audit_extra_zero:",
    "cyclic_inconsistency:",
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

REQUIRED_BUNDLE_PATHS = [
    "docs/REGGE_ZERO_GOVERNANCE_v0_1.md",
    "docs/REGGE_ZERO_GOVERNANCE_RUNBOOK_v0_1.md",
    "contracts/kuos_regge_zero_governance_contract_v0_1.yaml",
    "validation_cases/regge_zero_governance_validation_cases_v0_1.yaml",
    "validators/validate_regge_zero_governance_v0_1.py",
    "scripts/run_regge_zero_governance_checks_v0_1.py",
    "tests/test_regge_zero_governance_validator_v0_1.py",
    "formal/ReggeZeroGovernance.lean",
    "manifests/regge_zero_governance_runner_manifest_v0_1.json",
    "packets/regge_zero_governance_established_packet_v0_1.yaml",
    "packets/regge_zero_governance_ci_receipt_v0_1.yaml",
    "chain_indexes/regge_zero_governance_chain_index_v0_1.yaml",
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


def validate_contract(text: str) -> List[str]:
    errors: List[str] = []
    errors.extend(require_contains(text, ["id: kuos_regge_zero_governance_contract_v0_1"], "contract"))
    errors.extend(require_contains(text, ["same_root_required: true", "overwrite_forbidden: true", "destructive_replacement_forbidden: true"], "contract.lineage"))
    errors.extend(require_contains(text, REQUIRED_NON_AUTHORITY, "contract.non_authority_boundary"))
    errors.extend(require_contains(text, REQUIRED_INVARIANTS, "contract.invariants"))
    errors.extend(require_contains(text, REQUIRED_NULL_CONDITIONS, "contract.null_conditions"))
    errors.extend(require_contains(text, ["ReggeZeroGate", "PASS", "HOLD", "REPAIR", "REJECT", "QUARANTINE", "ADVISORY_ONLY"], "contract.canonical_gate"))
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
        if expected in {"HOLD", "REPAIR", "REJECT", "QUARANTINE"}:
            if not any(token in block for token in ["authority_shortcut", "medical_authorization_shortcut", "proof_authority_shortcut", "provenance_gap", "cyclic_inconsistency", "silent_overwrite_risk"]):
                errors.append(f"{case_id}: blocking case lacks an explicit blocker witness")
        if case_id == "pass_bounded_candidate_with_no_null_witness":
            if "novelty" not in block or "ADVISORY_ONLY" not in block:
                errors.append(f"{case_id}: novelty-only case must remain advisory-only")
    return errors


def validate_manifest(path: Path, require_runner: bool = False, require_bundle_paths: bool = False) -> List[str]:
    errors: List[str] = []
    try:
        manifest = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(ROOT)} is not valid JSON: {exc}"]
    if manifest.get("authority") != "non_authoritative_governance_addendum":
        errors.append(f"{path.relative_to(ROOT)} authority must remain non_authoritative_governance_addendum")
    paths = manifest.get("paths", [])
    for rel in paths:
        if not (ROOT / rel).exists():
            errors.append(f"manifest path missing: {rel}")
    if require_bundle_paths:
        for rel in REQUIRED_BUNDLE_PATHS:
            if rel not in paths:
                errors.append(f"bundle manifest missing path: {rel}")
    if require_runner and not (ROOT / manifest.get("runner_path", "")).exists():
        errors.append("runner manifest points to missing runner_path")
    return errors


def validate_packet(text: str) -> List[str]:
    return require_contains(text, ["id: regge_zero_governance_established_packet_v0_1", "append_only: true", "same_root_required: true", "overwrite_forbidden: true", "authority_expansion_forbidden: true"], "packet")


def validate_ci_receipt(text: str) -> List[str]:
    return require_contains(text, ["id: regge_zero_governance_ci_receipt_v0_1"], "ci_receipt")


def validate_chain_index(text: str) -> List[str]:
    return require_contains(text, ["id: regge_zero_governance_chain_index_v0_1", "same_root_required: true", "overwrite_forbidden: true", "authority_expansion_forbidden: true"], "chain_index")


def validate_formal(text: str) -> List[str]:
    return require_contains(text, ["namespace KuuOS", "namespace ReggeZeroGovernance", "def reggeZeroGate", "theorem no_soft_concern_blocks_without_witness"], "formal")


def main() -> int:
    errors: List[str] = []
    errors.extend(require_contains(read_text(DOC), ["Regge Zero Governance v0.1", "Only consistency-mandated null constraints may block a candidate"], "doc"))
    errors.extend(require_contains(read_text(RUNBOOK), ["Regge Zero Governance Runbook v0.1", "REGGE_ZERO_GOVERNANCE_VALIDATION: PASS"], "runbook"))
    errors.extend(validate_contract(read_text(CONTRACT)))
    errors.extend(validate_cases(read_text(CASES)))
    errors.extend(validate_manifest(MANIFEST, require_bundle_paths=True))
    errors.extend(validate_manifest(RUNNER_MANIFEST, require_runner=True))
    errors.extend(validate_packet(read_text(PACKET)))
    errors.extend(validate_ci_receipt(read_text(CI_RECEIPT)))
    errors.extend(validate_chain_index(read_text(CHAIN_INDEX)))
    errors.extend(validate_formal(read_text(FORMAL)))
    errors.extend(require_contains(read_text(RUNNER), ["validate_regge_zero_governance_v0_1.py", "tests/test_regge_zero_governance_validator_v0_1.py", "REGGE_ZERO_GOVERNANCE_CHECKS: PASS"], "runner"))
    errors.extend(require_contains(read_text(REGRESSION), ["REGGE_ZERO_GOVERNANCE_REGRESSION: PASS", "test_validation_cases_keep_soft_concern_advisory_only", "expected: ADVISORY_ONLY"], "regression"))
    errors.extend(require_contains(read_text(WORKFLOW), ["Regge Zero Governance Validation", "tests/test_regge_zero_governance_validator_v0_1.py", "scripts/run_regge_zero_governance_checks_v0_1.py"], "workflow"))
    errors.extend(require_contains(read_text(ALL_RUNNER), ["scripts/run_regge_zero_governance_checks_v0_1.py"], "all_governance_runner"))
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
