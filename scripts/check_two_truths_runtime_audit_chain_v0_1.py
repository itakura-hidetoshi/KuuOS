#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_two_truths_runtime_audit_chain_v0_1.py"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]
FALSE_FIELDS = [
    "paramartha_objectification_allowed",
    "samvrti_denial_allowed",
    "ultimate_to_conventional_collapse_allowed",
    "conventional_to_ultimate_collapse_allowed",
    "bridge_final_theorem_authority",
    "bridge_execution_authority",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    prev = "GENESIS"
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        errors.append("empty audit chain")
    for i, raw in enumerate(lines, start=1):
        entry = json.loads(raw)
        if entry.get("sequence") != i:
            errors.append(f"line {i}: sequence mismatch")
        if entry.get("previous_hash") != prev:
            errors.append(f"line {i}: previous_hash mismatch")
        event_hash = canonical_hash(entry.get("event"))
        if entry.get("event_hash") != event_hash:
            errors.append(f"line {i}: event_hash mismatch")
        payload = {"sequence": entry.get("sequence"), "previous_hash": entry.get("previous_hash"), "event_hash": entry.get("event_hash")}
        if entry.get("entry_hash") != canonical_hash(payload):
            errors.append(f"line {i}: entry_hash mismatch")
        event = entry.get("event", {})
        for field in FALSE_FIELDS:
            if event.get(field) is not False:
                errors.append(f"line {i}: {field} must be false")
        for flag in FLAGS:
            if event.get(flag) is not False:
                errors.append(f"line {i}: {flag} must be false")
        if event.get("mass_gap_bridge_authority") != "forbidden":
            errors.append(f"line {i}: mass_gap_bridge_authority must be forbidden")
        prev = entry.get("entry_hash")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: Two Truths runtime audit chain checked root={prev} entries={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
