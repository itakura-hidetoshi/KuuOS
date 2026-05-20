#!/usr/bin/env python3
"""Guard Samvrti Qi to Physical Motion evidence builder integrity source-of-truth discipline v0.1.

This regression guard prevents the integrity builder/validator from drifting
back to hand-written chain file lists or fixed entry counts. The chain index
must remain the single source of truth for integrity entries.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List, Sequence

ROOT = Path(__file__).resolve().parents[1]
BASE = "samvrti_qi_to_physical_motion_evidence_builder"
BUILDER_PATH = ROOT / "scripts" / f"build_{BASE}_integrity_manifest_v0_1.py"
VALIDATOR_PATH = ROOT / "scripts" / f"validate_{BASE}_integrity_manifest_v0_1.py"
CHAIN_INDEX_FILENAME = f"{BASE}_chain_index_v0_1.json"
CHAIN_INDEX_REL = "chain_indexes/" + CHAIN_INDEX_FILENAME

FORBIDDEN_BUILDER_MARKERS = [
    "CHAIN_FILES = [",
    "EXPECTED_ENTRY_COUNT",
]

FORBIDDEN_VALIDATOR_MARKERS = [
    "EXPECTED_ENTRY_COUNT =",
    "exactly 12 entries",
    "exactly 13 entries",
    "exactly 14 entries",
]

REQUIRED_BUILDER_GROUPS = [
    ["CHAIN_INDEX_PATH"],
    [CHAIN_INDEX_REL, CHAIN_INDEX_FILENAME],
    ["source_of_truth"],
    ["chain_files_from_index"],
    ["chain_stage_count"],
]

REQUIRED_VALIDATOR_GROUPS = [
    ["CHAIN_INDEX_PATH"],
    [CHAIN_INDEX_REL, CHAIN_INDEX_FILENAME],
    ["chain_paths_from_index"],
    ["source_of_truth"],
    ["actual_paths != expected_paths"],
    ["entry count must match chain_order length"],
]


def fail(message: str) -> int:
    print(f"[samvrti-qi-to-physical-motion-evidence-builder-sot] FAIL: {message}", file=sys.stderr)
    return 1


def check_text(path: Path, required_groups: Sequence[Sequence[str]], forbidden: Sequence[str], label: str) -> List[str]:
    errors: List[str] = []
    if not path.exists():
        return [f"missing {label}: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    for group in required_groups:
        if not any(marker in text for marker in group):
            expected = " OR ".join(group)
            errors.append(f"{label} missing required marker group: {expected}")
    for marker in forbidden:
        if marker in text:
            errors.append(f"{label} contains forbidden marker: {marker}")
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(check_text(BUILDER_PATH, REQUIRED_BUILDER_GROUPS, FORBIDDEN_BUILDER_MARKERS, "builder"))
    errors.extend(check_text(VALIDATOR_PATH, REQUIRED_VALIDATOR_GROUPS, FORBIDDEN_VALIDATOR_MARKERS, "validator"))
    if errors:
        for err in errors:
            print(f"[samvrti-qi-to-physical-motion-evidence-builder-sot] ERROR: {err}", file=sys.stderr)
        return 1
    print("[samvrti-qi-to-physical-motion-evidence-builder-sot] PASS: chain index remains integrity source of truth")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
