#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_kustring_runtime_audit_v0_2.py"
EVENTS = ROOT / "specs" / "kustring_runtime_audit_events_v0_2.generated.jsonl"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def main() -> int:
    code = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    lines = [x for x in EVENTS.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        errors.append("no audit events")
    for i, raw in enumerate(lines, 1):
        event = json.loads(raw)
        if event.get("runtime") != "kustring_runtime_v0_2":
            errors.append(f"line {i}: runtime mismatch")
        if not event.get("event_id"):
            errors.append(f"line {i}: missing event_id")
        for flag in FLAGS:
            if event.get(flag) is not False:
                errors.append(f"line {i}: {flag} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: KuString runtime audit events checked events={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
