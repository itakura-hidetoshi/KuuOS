#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_two_truths_runtime_audit_v0_1.py"
EVENTS = ROOT / "specs" / "two_truths_runtime_audit_events_v0_1.generated.jsonl"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT).returncode
    if code != 0:
        return code
    prev = "GENESIS"
    entries = []
    lines = [x for x in EVENTS.read_text(encoding="utf-8").splitlines() if x.strip()]
    for seq, raw in enumerate(lines, start=1):
        event = json.loads(raw)
        event_hash = canonical_hash(event)
        payload = {"sequence": seq, "previous_hash": prev, "event_hash": event_hash}
        entry_hash = canonical_hash(payload)
        entries.append({"sequence": seq, "previous_hash": prev, "event": event, "event_hash": event_hash, "entry_hash": entry_hash})
        prev = entry_hash
    CHAIN.write_text("".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in entries), encoding="utf-8")
    print(f"WROTE: {CHAIN.relative_to(ROOT)}")
    print(f"entries: {len(entries)}")
    print(f"root: {prev if entries else 'EMPTY'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
