#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_kustring_runtime_audit_v0_2.py"
EVENTS = ROOT / "specs" / "kustring_runtime_audit_events_v0_2.generated.jsonl"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"


def canonical_hash(obj: Any) -> str:
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT).returncode
    if code != 0:
        return code

    prev = "GENESIS"
    entries = []
    for seq, raw in enumerate([x for x in EVENTS.read_text(encoding="utf-8").splitlines() if x.strip()], start=1):
        event = json.loads(raw)
        event_hash = canonical_hash(event)
        entry_payload = {"sequence": seq, "previous_hash": prev, "event_hash": event_hash}
        entry_hash = canonical_hash(entry_payload)
        entry = {
            "sequence": seq,
            "previous_hash": prev,
            "event": event,
            "event_hash": event_hash,
            "entry_hash": entry_hash,
        }
        entries.append(entry)
        prev = entry_hash

    CHAIN.write_text("".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in entries), encoding="utf-8")
    print(f"WROTE: {CHAIN.relative_to(ROOT)}")
    print(f"entries: {len(entries)}")
    print(f"root: {prev if entries else 'EMPTY'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
