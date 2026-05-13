#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_kustring_runtime_audit_chain_v0_2.py"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
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
        entry_payload = {"sequence": entry.get("sequence"), "previous_hash": entry.get("previous_hash"), "event_hash": entry.get("event_hash")}
        entry_hash = canonical_hash(entry_payload)
        if entry.get("entry_hash") != entry_hash:
            errors.append(f"line {i}: entry_hash mismatch")
        event = entry.get("event", {})
        for flag in FLAGS:
            if event.get(flag) is not False:
                errors.append(f"line {i}: {flag} must be false")
        prev = entry.get("entry_hash")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: KuString runtime audit chain validated root={prev} entries={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
