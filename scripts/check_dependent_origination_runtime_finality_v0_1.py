#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE_CHECKER = ROOT / "scripts" / "check_dependent_origination_runtime_closure_v0_1.py"
DOC = ROOT / "docs" / "DEPENDENT_ORIGINATION_RUNTIME_FINALITY_PACKET_v0_1.md"

REQUIRED = [
    "docs/DEPENDENT_ORIGINATION_RUNTIME_CLOSURE_PACKET_v0_1.md",
    "docs/DEPENDENT_ORIGINATION_RUNTIME_FINALITY_PACKET_v0_1.md",
    "specs/dependent_origination_runtime_attestation_v0_1.generated.json",
    "specs/dependent_origination_runtime_bundle_v0_1.generated.json",
    "specs/dependent_origination_runtime_worm_receipt_v0_1.generated.json",
    "scripts/check_dependent_origination_runtime_closure_v0_1.py",
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
    for token in ["implementation finality only", "not proof", "not proof, truth, essence authority, Ten'i authority, clinical authority, or execution authority"]:
        if token not in text:
            errors.append(f"finality doc missing: {token}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Dependent Origination runtime finality checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
