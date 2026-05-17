#!/usr/bin/env python3
"""Validate the public Physical Quantum Qi runtime contract v0.1.

This validator is intentionally dependency-free. It checks that Qi packets are
classified from evidence, not from claimed type, and that Qi never grants
authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "physical_quantum_qi_runtime_contract_v0_1.json"
EXAMPLE_PATH = ROOT / "examples" / "physical_quantum_qi_runtime_packet_v0_1.json"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_runtime_validation_cases_v0_1.json"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def evidence_pass(packet: Dict[str, Any], key: str) -> bool:
    return packet.get("evidence_status", {}).get(key) == "pass"


def all_evidence(packet: Dict[str, Any], keys: List[str]) -> bool:
    return all(evidence_pass(packet, key) for key in keys)


def authority_clear(packet: Dict[str, Any], authority_keys: List[str]) -> bool:
    authority = packet.get("authority", {})
    return all(authority.get(key) is False for key in authority_keys)


def has_fatal_error(packet: Dict[str, Any], fatal_flags: List[str]) -> bool:
    present = set(packet.get("fatal_flags", []))
    if present.intersection(fatal_flags):
        return True
    if packet.get("mass_gap_floor", {}).get("not_source_of_qi") is False:
        return True
    return False


def classify(packet: Dict[str, Any], spec: Dict[str, Any]) -> Tuple[str, str]:
    physical_keys = spec["physical_qi_required_evidence"]
    full_path_keys = spec["full_path_qi_additional_evidence"]
    fatal_flags = spec["fatal_reject_flags"]
    authority_keys = spec["authority_must_be_false"]

    if has_fatal_error(packet, fatal_flags):
        return "Reject", "fatal Qi runtime error"

    if not authority_clear(packet, authority_keys):
        return "Reject", "Qi packet attempted to grant forbidden authority"

    # Ordered evidence-bound ladder. The claim is not authoritative.
    if not evidence_pass(packet, "delta_rel_in_K_perp"):
        if evidence_pass(packet, "K_non_reification"):
            return "NonQi", "K non-reification present but no K_perp dependent-origination difference"
        return "Reject", "no dependent-origination difference in K_perp"

    if not evidence_pass(packet, "string_mode_consistency") or not evidence_pass(packet, "brane_boundary_support"):
        return "PreQi", "missing string/brane organization"

    if not evidence_pass(packet, "gauge_connection_A_mu"):
        return "ProtoQi", "missing gauge connection"

    if not evidence_pass(packet, "curvature_F_munu") or not evidence_pass(packet, "Wilson_loop_residue"):
        return "TransportableQi", "missing curvature or holonomy residue"

    if not evidence_pass(packet, "current_J_Qi_mu"):
        return "CurvedQi", "missing Qi current coupling"

    if not evidence_pass(packet, "Ward_or_leak_identity"):
        return "CurrentQi", "missing Ward/leak identity"

    if not all_evidence(packet, physical_keys):
        return "CurrentQi", "missing PhysicalQi evidence bundle"

    if all_evidence(packet, full_path_keys):
        return "FullPathQi", "PhysicalQi evidence plus SK/FV history evidence present"

    return "PhysicalQi", "PhysicalQi evidence present; SK/FV history incomplete"


def validate_spec(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected_schema = "physical_quantum_qi_runtime_contract_v0_1"
    if spec.get("schema_id") != expected_schema:
        errors.append(f"schema_id must be {expected_schema}")
    if spec.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if spec.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    if spec.get("mass_gap_floor", {}).get("not_source_of_qi") is not True:
        errors.append("mass_gap_floor.not_source_of_qi must be true")
    for required in ["physical_qi_required_evidence", "full_path_qi_additional_evidence", "authority_must_be_false"]:
        if not spec.get(required):
            errors.append(f"missing nonempty {required}")
    return errors


def validate_example(example: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    validated, reason = classify(example, spec)
    if validated != "FullPathQi":
        errors.append(f"example should validate as FullPathQi, got {validated}: {reason}")
    if example.get("validated_type") not in (None, validated):
        errors.append("example validated_type must be null or match computed type")
    return errors


def validate_cases(cases_doc: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for case in cases_doc.get("cases", []):
        name = case.get("name", "<unnamed>")
        packet = case.get("packet", {})
        expected = case.get("expected_validated_type")
        actual, reason = classify(packet, spec)
        if actual != expected:
            errors.append(f"case {name}: expected {expected}, got {actual}: {reason}")
    return errors


def main() -> int:
    spec = load_json(SPEC_PATH)
    example = load_json(EXAMPLE_PATH)
    cases = load_json(CASES_PATH)

    errors: List[str] = []
    errors.extend(validate_spec(spec))
    errors.extend(validate_example(example, spec))
    errors.extend(validate_cases(cases, spec))

    if errors:
        print("Physical Quantum Qi runtime validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi runtime validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
