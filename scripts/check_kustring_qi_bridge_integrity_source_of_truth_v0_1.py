#!/usr/bin/env python3
"""Guard KuString Qi Bridge integrity source-of-truth discipline v0.1.

This regression guard prevents the integrity builder/validator from drifting
back to hand-written chain file lists or fixed entry counts. The chain index
must remain the single source of truth for integrity entries.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List

ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_kustring_qi_bridge_integrity_manifest_v0_1.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_kustring_qi_bridge_integrity_manifest_v0_1.py"
CHAIN_INDEX_REL = "specs/kustring_qi_bridge_chain_index_v0_1.json"

FORBIDDEN_BUILDER_MARKERS = [
    "CHAIN_FILES = [",
    "EXPECTED_ENTRY_COUNT",
]

FORBIDDEN_VALIDATOR_MARKERS = [
    "EXPECTED_ENTRY_COUNT =",
    "len(entries) != 16",
    "exactly 16 entries",
]

REQUIRED_BUILDER_MARKERS = [
    "CHAIN_INDEX_PATH",
    CHAIN_INDEX_REL,
    "source_of_truth",
    "chain_files_from_index",
    "chain_stage_count",
]

REQUIRED_VALIDATOR_MARKERS = [
    "CHAIN_INDEX_PATH",
    CHAIN_INDEX_REL,
    "chain_paths_from_index",
    "source_of_truth",
    "actual_paths != expected_paths",
    "entry count must match chain_order length",
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge-sot] FAIL: {message}", file=sys.stderr)
    return 1


def check_text(path: Path, required: List[str], forbidden: List[str], label: str) -> List[str]:
    errors: List[str] = []
    if not path.exists():
        return [f"missing {label}: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    for marker in required:
        if marker not in text:
            errors.append(f"{label} missing required marker: {marker}")
    for marker in forbidden:
        if marker in text:
            errors.append(f"{label} contains forbidden marker: {marker}")
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(check_text(BUILDER_PATH, REQUIRED_BUILDER_MARKERS, FORBIDDEN_BUILDER_MARKERS, "builder"))
    errors.extend(check_text(VALIDATOR_PATH, REQUIRED_VALIDATOR_MARKERS, FORBIDDEN_VALIDATOR_MARKERS, "validator"))

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge-sot] ERROR: {err}", file=sys.stderr)
        return 1

    print("[kustring-qi-bridge-sot] PASS: chain index remains integrity source of truth")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())