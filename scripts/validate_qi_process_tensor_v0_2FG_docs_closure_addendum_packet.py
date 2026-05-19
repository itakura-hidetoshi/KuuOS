#!/usr/bin/env python3
"""Validate the Qi Process Tensor v0.2FG docs closure addendum packet.

This validator intentionally checks more than the packet itself.  The addendum is
valid only when the packet is visible in the manifest, chain index, Makefile,
and the full governance runner, so the documentation closure cannot silently
fall out of the release surface.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET_REL = "packets/physical_quantum_qi_deepening_v0_2FG_docs_closure_addendum_packet.json"
VALIDATOR_REL = "scripts/validate_qi_process_tensor_v0_2FG_docs_closure_addendum_packet.py"
PACKET = ROOT / PACKET_REL
MANIFEST = ROOT / "manifests" / "physical_quantum_qi_deepening_manifest_v0_2.json"
CHAIN_INDEX = ROOT / "chain_indexes" / "physical_quantum_qi_deepening_chain_index_v0_2.json"
MAKEFILE = ROOT / "Makefile"
FULL_RUNNER = ROOT / "scripts" / "run_all_governance_full_checks_v0_1.py"

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

REQUIRED_MANIFEST_PHRASES = {
    "Qi_Process_Tensor_v0_2FG_Docs_Closure_Addendum",
    PACKET_REL,
    VALIDATOR_REL,
    "Qi Process Tensor v0.2FG docs closure addendum must remain additive-only, same-root, and non-authoritative",
    "python3 scripts/validate_qi_process_tensor_v0_2FG_docs_closure_addendum_packet.py",
}

REQUIRED_CHAIN_PHRASES = {
    PACKET_REL,
    VALIDATOR_REL,
    "qi_process_tensor_v0_2FG_docs_closure_addendum_packet",
    "qi_process_tensor_v0_2FG_docs_closure_addendum_validator",
    "python3 scripts/validate_qi_process_tensor_v0_2FG_docs_closure_addendum_packet.py",
    "Qi_Process_Tensor_v0_2FG_Docs_Closure_Addendum is additive-only, same-root, documentation-closure-only, and non-authoritative",
}

REQUIRED_ENTRYPOINT_PHRASES = {
    "python3 scripts/validate_qi_process_tensor_v0_2FG_docs_closure_addendum_packet.py",
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_text(path: Path, phrases: set[str], label: str) -> list[str]:
    if not path.exists():
        return [f"missing {label}: {path}"]
    text = read_text(path)
    return [f"{label} missing phrase: {phrase}" for phrase in sorted(phrases) if phrase not in text]


def main() -> int:
    errors: list[str] = []
    if not PACKET.exists():
        errors.append(f"missing packet: {PACKET}")
    else:
        packet = load_json(PACKET)
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

    errors.extend(require_text(MANIFEST, REQUIRED_MANIFEST_PHRASES, "manifest"))
    errors.extend(require_text(CHAIN_INDEX, REQUIRED_CHAIN_PHRASES, "chain_index"))
    errors.extend(require_text(MAKEFILE, REQUIRED_ENTRYPOINT_PHRASES, "Makefile"))
    errors.extend(require_text(FULL_RUNNER, REQUIRED_ENTRYPOINT_PHRASES, "full governance runner"))

    if errors:
        print("Qi Process Tensor v0.2FG docs closure addendum validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Process Tensor v0.2FG docs closure addendum validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
