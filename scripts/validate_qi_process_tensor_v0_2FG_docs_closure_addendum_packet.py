#!/usr/bin/env python3
"""Validate the Qi Process Tensor v0.2FG docs closure addendum packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "packets" / "physical_quantum_qi_deepening_v0_2FG_docs_closure_addendum_packet.json"

REQUIRED_TOP_LEVEL = {
    "packet_id": "physical_quantum_qi_deepening_v0_2FG_docs_closure_addendum_packet",
    "packet_type": "closure_addendum_packet",
    "root_closure_packet": "packets/physical_quantum_qi_deepening_release_closure_packet_v0_2.json",
    "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
    "chain_index": "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
}

REQUIRED_SURFACES = {
    "qi_process_tensor_release_chain_document": "docs/KUUOS_QI_PROCESS_TENSOR_RELEASE_CHAIN_v0_2FG.md",
    "qi_process_tensor_release_chain_docs_validator": "scripts/validate_qi_process_tensor_release_chain_docs_v0_2FG.py",
    "qi_process_tensor_release_chain_validator": "scripts/validate_qi_process_tensor_release_chain_v0_2FG.py",
}

REQUIRED_INVARIANT_PHRASES = {
    "multi-time non-Markov temporal structure",
    "conventional-truth temporal substrate",
    "not ultimate truth",
    "not-ungated-execution",
    "safety-gated-candidate-generation",
    "silent loss of release-chain invariants",
}

REQUIRED_VALIDATION = {
    "python3 scripts/validate_qi_process_tensor_release_chain_docs_v0_2FG.py",
    "python3 scripts/validate_qi_process_tensor_release_chain_v0_2FG.py",
    "python3 scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
    "make physical-quantum-qi-deepening-checks",
    "make all-governance-checks",
}

AUTHORITY_FALSE_FIELDS = {
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "commit_authority",
    "belief_commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "truth_authority",
    "safety_override_authority",
}


def load_packet() -> dict[str, Any]:
    with PACKET.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []
    if not PACKET.exists():
        errors.append(f"missing packet: {PACKET}")
    else:
        packet = load_packet()
        for key, expected in REQUIRED_TOP_LEVEL.items():
            if packet.get(key) != expected:
                errors.append(f"{key} mismatch: expected {expected!r}, got {packet.get(key)!r}")
        if packet.get("additive_only") is not True:
            errors.append("additive_only must be true")
        if packet.get("overwrite_forbidden") is not True:
            errors.append("overwrite_forbidden must be true")
        if packet.get("same_root_required") is not True:
            errors.append("same_root_required must be true")

        surfaces = packet.get("surfaces", {})
        for key, expected_path in REQUIRED_SURFACES.items():
            if surfaces.get(key) != expected_path:
                errors.append(f"surface {key} must be {expected_path}")
            if not (ROOT / expected_path).exists():
                errors.append(f"surface path missing in repository: {expected_path}")

        text = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        for phrase in sorted(REQUIRED_INVARIANT_PHRASES):
            if phrase not in text:
                errors.append(f"missing invariant phrase: {phrase}")

        validations = set(packet.get("required_validation", []))
        for item in sorted(REQUIRED_VALIDATION - validations):
            errors.append(f"missing required validation: {item}")

        authority = packet.get("authority_boundary", {})
        for key in sorted(AUTHORITY_FALSE_FIELDS):
            if authority.get(key) is not False:
                errors.append(f"authority_boundary.{key} must be false")

        closure = packet.get("closure_statement", "")
        for phrase in ["grants no proof", "execution", "truth", "safety override authority"]:
            if phrase not in closure:
                errors.append(f"closure_statement missing phrase: {phrase}")

    if errors:
        print("Qi Process Tensor v0.2FG docs closure addendum validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Process Tensor v0.2FG docs closure addendum validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
