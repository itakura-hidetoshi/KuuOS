#!/usr/bin/env python3
"""Validate Regge Zero Governance v0.1 artifacts.

This validator is intentionally small and conservative. It checks that the
contract, validation cases, manifest, and established packet preserve the
non-authority and minimal-null-constraint boundaries.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts" / "kuos_regge_zero_governance_contract_v0_1.yaml"
CASES = ROOT / "validation_cases" / "regge_zero_governance_validation_cases_v0_1.yaml"
MANIFEST = ROOT / "manifests" / "regge_zero_governance_bundle_manifest_v0_1.json"
PACKET = ROOT / "packets" / "regge_zero_governance_established_packet_v0_1.yaml"

REQUIRED_NON_AUTHORITY = [
    "candidate_not_authority",
    "validation_not_truth",
    "ci_pass_not_theorem_authority",
    "runtime_tick_not_autonomous_execution_authority",
    "qi_readout_not_intervention_license",
    "memory_persistence_not_belief_sovereignty",
    "reflection_summary_not_root_rewrite",
    "audit_not_infinite_escalation",
]

REQUIRED_INVARIANTS = {
    "minimal_null_constraint_only",
    "nested_null_inheritance",
    "no_extra_blocker_without_witness",
    "no_single_scalar_authority_collapse",
    "cyclic_consistency_required_for_promotion",
}

ALLOWED_BLOCKING_RESULTS = {"HOLD", "REPAIR", "REJECT", "QUARANTINE"}
NON_BLOCKING_RESULTS = {"PASS", "ADVISORY_ONLY", "PASS_WITH_ADVISORY"}


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        raise AssertionError("PyYAML is required to validate YAML artifacts")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise AssertionError(f"expected mapping in {path}")
    return data


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"expected object in {path}")
    return data


def validate_contract(contract: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if contract.get("id") != "kuos_regge_zero_governance_contract_v0_1":
        errors.append("contract id mismatch")
    lineage = contract.get("lineage", {})
    for key in ["same_root_required", "overwrite_forbidden", "destructive_replacement_forbidden"]:
        if lineage.get(key) is not True:
            errors.append(f"lineage.{key} must be true")
    non_auth = contract.get("non_authority_boundary", {})
    for key in REQUIRED_NON_AUTHORITY:
        if non_auth.get(key) is not True:
            errors.append(f"non_authority_boundary.{key} must be true")
    invariants = contract.get("invariants", [])
    invariant_ids = {item.get("id") for item in invariants if isinstance(item, dict)}
    missing = REQUIRED_INVARIANTS - invariant_ids
    if missing:
        errors.append(f"missing invariants: {sorted(missing)}")
    gate = contract.get("canonical_gate", {})
    outputs = set(gate.get("output_values", []))
    expected_outputs = ALLOWED_BLOCKING_RESULTS | {"PASS", "ADVISORY_ONLY"}
    if not expected_outputs.issubset(outputs):
        errors.append("canonical_gate.output_values is incomplete")
    null_conditions = contract.get("null_conditions", {})
    for key in ["authority_shortcut", "proof_shortcut", "qi_intervention_shortcut", "memory_sovereignty_shortcut", "over_audit_extra_zero", "cyclic_inconsistency"]:
        if key not in null_conditions:
            errors.append(f"missing null condition: {key}")
    non_claims = set(contract.get("non_claims", []))
    for key in [
        "does_not_prove_string_theory",
        "does_not_create_autonomous_execution_authority",
        "does_not_create_medical_authorization",
        "does_not_turn_CI_success_into_theorem_authority",
        "does_not_turn_validation_into_truth",
    ]:
        if key not in non_claims:
            errors.append(f"missing non-claim: {key}")
    return errors


def validate_cases(cases_doc: Dict[str, Any], contract: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    cases = cases_doc.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["validation cases must be a non-empty list"]
    allowed_witnesses = set(contract.get("allowed_blocker_witnesses", []))
    forbidden_without_witness = set(contract.get("forbidden_blocker_bases_without_witness", []))
    seen_ids = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case must be mapping")
            continue
        cid = case.get("id")
        if not cid or cid in seen_ids:
            errors.append(f"invalid or duplicate case id: {cid}")
        seen_ids.add(cid)
        expected = case.get("expected")
        candidate = case.get("candidate", {})
        basis = set(candidate.get("concern_basis", []) or [])
        inherited = set(candidate.get("inherited_null_conditions", []) or [])
        has_blocker_witness = bool((basis | inherited) & allowed_witnesses)
        only_forbidden_soft_basis = bool(basis) and basis.issubset(forbidden_without_witness)
        if expected in ALLOWED_BLOCKING_RESULTS and not has_blocker_witness:
            errors.append(f"{cid}: blocking result without allowed blocker witness")
        if only_forbidden_soft_basis and expected not in NON_BLOCKING_RESULTS:
            errors.append(f"{cid}: soft basis without witness must not block")
        if candidate.get("cyclic_consistency_receipt") == "FAIL" and expected not in ALLOWED_BLOCKING_RESULTS:
            errors.append(f"{cid}: cyclic FAIL must block or repair")
    return errors


def validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    paths = manifest.get("paths", [])
    if not isinstance(paths, list):
        return ["manifest.paths must be a list"]
    for rel in paths:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"manifest path missing: {rel}")
    if manifest.get("authority") != "non_authoritative_governance_addendum":
        errors.append("manifest authority must remain non_authoritative_governance_addendum")
    return errors


def validate_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("id") != "regge_zero_governance_established_packet_v0_1":
        errors.append("packet id mismatch")
    locks = packet.get("semantic_locks", {})
    for key in ["append_only", "same_root_required", "overwrite_forbidden", "authority_expansion_forbidden"]:
        if locks.get(key) is not True:
            errors.append(f"semantic_locks.{key} must be true")
    if packet.get("execution_authority") is not False:
        errors.append("execution_authority must be false")
    if packet.get("medical_authorization") is not False:
        errors.append("medical_authorization must be false")
    return errors


def main() -> int:
    errors: List[str] = []
    contract = load_yaml(CONTRACT)
    cases_doc = load_yaml(CASES)
    manifest = load_json(MANIFEST)
    packet = load_yaml(PACKET)

    errors.extend(validate_contract(contract))
    errors.extend(validate_cases(cases_doc, contract))
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_packet(packet))

    if errors:
        print("REGGE_ZERO_GOVERNANCE_VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REGGE_ZERO_GOVERNANCE_VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
