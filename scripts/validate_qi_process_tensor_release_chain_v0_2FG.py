#!/usr/bin/env python3
"""Validate Qi Process Tensor v0.2F/v0.2G release-chain presence.

This narrow validator protects the release surface from silently dropping:
- Qi Process Tensor v0.2F
- Qi Process Tensor conventional autonomy v0.2G
- Qi Process Tensor v0.2FG release-chain docs and docs validator

It accepts both machine tags and human-readable release prose, because some
packets use canonical identifiers such as ``Qi_Process_Tensor_v0_2F`` while
others use release-facing prose such as ``Qi Process Tensor v0.2F``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]

PACKETS = {
    "manifest": ROOT / "manifests" / "physical_quantum_qi_deepening_manifest_v0_2.json",
    "chain_index": ROOT / "chain_indexes" / "physical_quantum_qi_deepening_chain_index_v0_2.json",
    "release": ROOT / "packets" / "physical_quantum_qi_deepening_release_packet_v0_2.json",
    "finality": ROOT / "packets" / "physical_quantum_qi_deepening_finality_packet_v0_2.json",
    "closure": ROOT / "packets" / "physical_quantum_qi_deepening_release_closure_packet_v0_2.json",
    "validated_baseline": ROOT / "packets" / "physical_quantum_qi_deepening_validated_baseline_packet_v0_2.json",
    "baseline_established_final": ROOT / "packets" / "physical_quantum_qi_deepening_baseline_established_final_packet_v0_2.json",
}

# Each tuple is a logical requirement followed by accepted textual realizations.
REQUIRED_PHRASE_GROUPS: dict[str, tuple[str, ...]] = {
    "Qi Process Tensor v0.2F module": (
        "Qi_Process_Tensor_v0_2F",
        "Qi Process Tensor v0.2F",
        "qi_process_tensor_v0_2F",
    ),
    "Qi Process Tensor conventional autonomy v0.2G module": (
        "Qi_Process_Tensor_Conventional_Autonomy_v0_2G",
        "Qi Process Tensor conventional autonomy v0.2G",
        "qi_process_tensor_conventional_autonomy_v0_2G",
    ),
    "multi-time non-Markov temporal structure": (
        "multi-time non-Markov temporal structure",
    ),
    "history-bearing relational/action flow": (
        "history-bearing relational/action flow",
    ),
    "conventional-truth temporal substrate": (
        "conventional-truth temporal substrate",
    ),
    "safety-gated candidate generation": (
        "safety-gated candidate generation",
    ),
    "not ultimate truth": (
        "not ultimate truth",
    ),
    "not ungated execution": (
        "not ungated execution",
        "not ultimate truth, fixed ontology, ungated execution",
        "not ultimate truth, fixed ontology, ungated execution, or execution authority",
    ),
}

REQUIRED_PATHS = {
    "src/physical_quantum_qi_process_tensor_runtime_v0_2F.py",
    "examples/physical_quantum_qi_process_tensor_packet_v0_2F.json",
    "docs/KUUOS_QI_PROCESS_TENSOR_CONVENTIONAL_AUTONOMY_v0_2G.md",
    "examples/kuuos_qi_process_tensor_conventional_autonomy_packet_v0_2G.json",
    "scripts/validate_physical_quantum_qi_process_tensor_v0_2F.py",
    "tests/test_physical_quantum_qi_process_tensor_v0_2F.py",
    "scripts/validate_kuuos_qi_process_tensor_conventional_autonomy_v0_2G.py",
    "tests/test_kuuos_qi_process_tensor_conventional_autonomy_v0_2G.py",
}

REQUIRED_DOC_PATHS = {
    "docs/KUUOS_QI_PROCESS_TENSOR_RELEASE_CHAIN_v0_2FG.md",
    "scripts/validate_qi_process_tensor_release_chain_docs_v0_2FG.py",
}

AUTHORITY_FIELDS = {
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


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def as_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def missing(required: Iterable[str], text: str) -> List[str]:
    return sorted(item for item in required if item not in text)


def missing_phrase_groups(groups: dict[str, Sequence[str]], text: str) -> List[str]:
    errors: List[str] = []
    for label, variants in groups.items():
        if not any(variant in text for variant in variants):
            errors.append(label)
    return errors


def validate_authority(label: str, doc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    candidates = [
        doc.get("authority_boundary"),
        doc.get("declared_boundaries"),
    ]
    found = False
    for candidate in candidates:
        if isinstance(candidate, dict):
            found = True
            for key in AUTHORITY_FIELDS:
                if candidate.get(key) is not False:
                    errors.append(f"{label}.{key} must be false")
    if not found and label not in {"manifest", "chain_index"}:
        errors.append(f"{label} missing authority boundary")
    return errors


def validate_packet(label: str, path: Path) -> List[str]:
    doc = load_json(path)
    text = as_text(doc)
    errors = [
        f"{label} missing phrase group: {group}"
        for group in missing_phrase_groups(REQUIRED_PHRASE_GROUPS, text)
    ]
    if label in {"manifest", "chain_index", "release", "finality", "closure"}:
        errors.extend([f"{label} missing path: {p}" for p in missing(REQUIRED_PATHS, text)])
    if label in {"manifest", "chain_index"}:
        errors.extend([f"{label} missing docs path: {p}" for p in missing(REQUIRED_DOC_PATHS, text)])
    errors.extend(validate_authority(label, doc))
    return errors


def validate_repository_doc_paths() -> List[str]:
    return [
        f"missing repository docs surface: {path}"
        for path in sorted(REQUIRED_DOC_PATHS)
        if not (ROOT / path).exists()
    ]


def main() -> int:
    errors: List[str] = []
    errors.extend(validate_repository_doc_paths())
    for label, path in PACKETS.items():
        if not path.exists():
            errors.append(f"missing packet file: {path}")
            continue
        errors.extend(validate_packet(label, path))

    if errors:
        print("Qi Process Tensor v0.2F/v0.2G release-chain validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Qi Process Tensor v0.2F/v0.2G release-chain validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
