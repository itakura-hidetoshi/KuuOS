#!/usr/bin/env python3
"""Validate the Samvrti Qi to Physical Motion evidence builder release surface v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

ROOT = Path(__file__).resolve().parents[1]
BASE = "samvrti_qi_to_physical_motion_evidence_builder"

PATHS = {
    "manifest": ROOT / "manifests" / f"{BASE}_manifest_v0_1.json",
    "release": ROOT / "packets" / f"{BASE}_release_packet_v0_1.json",
    "finality": ROOT / "packets" / f"{BASE}_finality_packet_v0_1.json",
    "closure": ROOT / "packets" / f"{BASE}_release_closure_packet_v0_1.json",
    "baseline": ROOT / "packets" / f"{BASE}_validated_baseline_packet_v0_1.json",
    "chain": ROOT / "chain_indexes" / f"{BASE}_chain_index_v0_1.json",
    "runtime_validator": ROOT / "scripts" / f"validate_{BASE}_v0_1.py",
    "runner": ROOT / "scripts" / "run_qi_motion_chain_checks_v0_1.py",
}

REQUIRED_REPO_PATHS = {
    "docs/SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md",
    "examples/samvrti_qi_to_physical_motion_evidence_builder_minimal.py",
    "validation_cases/samvrti_qi_to_physical_motion_evidence_builder_cases_v0_1.json",
    "scripts/validate_samvrti_qi_to_physical_motion_evidence_builder_v0_1.py",
    "scripts/validate_samvrti_qi_to_physical_motion_evidence_builder_release_packet_v0_1.py",
    "manifests/samvrti_qi_to_physical_motion_evidence_builder_manifest_v0_1.json",
    "packets/samvrti_qi_to_physical_motion_evidence_builder_release_packet_v0_1.json",
    "packets/samvrti_qi_to_physical_motion_evidence_builder_finality_packet_v0_1.json",
    "packets/samvrti_qi_to_physical_motion_evidence_builder_release_closure_packet_v0_1.json",
    "packets/samvrti_qi_to_physical_motion_evidence_builder_validated_baseline_packet_v0_1.json",
    "chain_indexes/samvrti_qi_to_physical_motion_evidence_builder_chain_index_v0_1.json",
    "scripts/run_qi_motion_chain_checks_v0_1.py",
}

REQUIRED_INVARIANTS = {
    "Samvrti Qi acceptance is not PhysicalQi or FullPathQi",
    "Samvrti Qi acceptance opens only conservative evidence packet construction",
    "KuStringQiBridge remains the evidence projection gate",
    "physical classifier remains the validated_type authority",
    "builder output is routed to the motion pipeline as observe-only support",
    "medical modality boundary is neutral",
    "Qi is not denied by boundary wording",
    "East Asian medical reasoning is not denied by boundary wording",
    "biomedicine is not privileged by wording",
    "professional judgment remains required",
    "patient context remains required",
}


def fail(message: str) -> int:
    print(f"[samvrti-qi-to-physical-motion-evidence-builder-release] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_manifest_files(manifest: Dict[str, Any]) -> Set[str]:
    files: Set[str] = set()
    for value in manifest.get("files", {}).values():
        if isinstance(value, list):
            files.update(str(item) for item in value)
    return files


def check_true(mapping: Dict[str, Any], key: str, label: str, errors: List[str]) -> None:
    if mapping.get(key) is not True:
        errors.append(f"{label}.{key} must be true")


def main() -> int:
    for label, path in PATHS.items():
        if not path.exists():
            return fail(f"missing {label}: {path.relative_to(ROOT)}")

    try:
        manifest = load_json(PATHS["manifest"])
        release = load_json(PATHS["release"])
        finality = load_json(PATHS["finality"])
        closure = load_json(PATHS["closure"])
        baseline = load_json(PATHS["baseline"])
        chain = load_json(PATHS["chain"])
    except Exception as exc:
        return fail(f"json load failed: {exc}")

    errors: List[str] = []
    expected_ids = {
        "manifest_id": f"{BASE}_manifest_v0_1",
        "release_packet_id": f"{BASE}_release_packet_v0_1",
        "finality_packet_id": f"{BASE}_finality_packet_v0_1",
        "closure_packet_id": f"{BASE}_release_closure_packet_v0_1",
        "baseline_packet_id": f"{BASE}_validated_baseline_packet_v0_1",
        "chain_index_id": f"{BASE}_chain_index_v0_1",
    }

    if manifest.get("manifest_id") != expected_ids["manifest_id"]:
        errors.append("manifest_id mismatch")
    if release.get("packet_id") != expected_ids["release_packet_id"]:
        errors.append("release packet_id mismatch")
    if finality.get("packet_id") != expected_ids["finality_packet_id"]:
        errors.append("finality packet_id mismatch")
    if closure.get("packet_id") != expected_ids["closure_packet_id"]:
        errors.append("closure packet_id mismatch")
    if baseline.get("packet_id") != expected_ids["baseline_packet_id"]:
        errors.append("baseline packet_id mismatch")
    if chain.get("chain_index_id") != expected_ids["chain_index_id"]:
        errors.append("chain_index_id mismatch")

    for doc, label in [(manifest, "manifest"), (chain, "chain")]:
        if doc.get("update_policy") != "additive_only":
            errors.append(f"{label}.update_policy must be additive_only")
        if doc.get("overwrite_policy") != "forbidden":
            errors.append(f"{label}.overwrite_policy must be forbidden")
        check_true(doc, "same_root_required", label, errors)

    files = flatten_manifest_files(manifest)
    missing_manifest = sorted(REQUIRED_REPO_PATHS - files - {"scripts/run_qi_motion_chain_checks_v0_1.py"})
    if missing_manifest:
        errors.append("manifest missing required file entries: " + ", ".join(missing_manifest))
    for relpath in files:
        if not (ROOT / relpath).exists():
            errors.append(f"manifest references missing repository file: {relpath}")

    chain_paths = {entry.get("path") for entry in chain.get("chain_order", [])}
    missing_chain = sorted(REQUIRED_REPO_PATHS - chain_paths)
    if missing_chain:
        errors.append("chain_order missing paths: " + ", ".join(missing_chain))
    for relpath in chain_paths:
        if relpath and not (ROOT / relpath).exists():
            errors.append(f"chain_order references missing repository file: {relpath}")

    for label, packet in [("release", release), ("finality", finality), ("closure", closure), ("baseline", baseline)]:
        text = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        for invariant in REQUIRED_INVARIANTS:
            if invariant not in text:
                errors.append(f"{label} missing invariant marker: {invariant}")

    required_runner_markers = [
        "samvrti-to-physical-motion-builder-release",
        f"scripts/validate_{BASE}_release_packet_v0_1.py",
    ]
    runner_text = PATHS["runner"].read_text(encoding="utf-8")
    for marker in required_runner_markers:
        if marker not in runner_text:
            errors.append(f"runner missing marker: {marker}")

    if errors:
        for err in errors:
            print(f"[samvrti-qi-to-physical-motion-evidence-builder-release] ERROR: {err}", file=sys.stderr)
        return 1

    print("[samvrti-qi-to-physical-motion-evidence-builder-release] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
