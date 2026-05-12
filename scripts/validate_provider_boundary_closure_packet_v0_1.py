#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PROVIDER_BOUNDARY_CLOSURE_PACKET_v0_1.md"

REQUIRED = [
    "docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_EVENT_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/PROVIDER_BOUNDARY_BUNDLE_v0_1.md",
    "docs/PROVIDER_BOUNDARY_ATTESTATION_v0_1.md",
    "docs/PROVIDER_BOUNDARY_CLOSURE_PACKET_v0_1.md",
]

CHECKS = [
    "scripts/validate_ai_provider_boundary_runtime_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_event_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_hash_chain_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_worm_export_receipt_v0_1.py",
    "scripts/validate_provider_boundary_bundle_v0_1.py",
    "scripts/validate_provider_boundary_attestation_v0_1.py",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    if DOC.is_file():
        text = DOC.read_text(encoding="utf-8")
        for token in ["operational closure", "does not grant authority"]:
            if token not in text:
                errors.append(f"missing text: {token}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    for rel in CHECKS:
        print("\n>>> " + rel, flush=True)
        result = subprocess.run([sys.executable, rel], cwd=ROOT)
        if result.returncode != 0:
            print(f"FAIL: {rel} exited with {result.returncode}")
            return result.returncode
    print("PASS: provider boundary closure packet validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
