#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE_CHECKER = ROOT / "scripts" / "check_kustring_runtime_closure_v0_2.py"
DOC = ROOT / "docs" / "KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md"

REQUIRED = [
    "docs/KUSTRING_RUNTIME_CLOSURE_PACKET_v0_2.md",
    "docs/KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md",
    "specs/kustring_runtime_attestation_v0_2.generated.json",
    "specs/kustring_runtime_bundle_v0_2.generated.json",
    "specs/kustring_runtime_worm_receipt_v0_2.generated.json",
    "scripts/check_kustring_runtime_closure_v0_2.py",
]


def main() -> int:
    code = subprocess.run([sys.executable, str(CLOSURE_CHECKER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
    for token in ["implementation finality only", "not proof", "not proof, truth, clinical authority, or execution authority"]:
        if token not in text:
            errors.append(f"finality doc missing: {token}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: KuString runtime finality checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
