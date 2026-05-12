#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/PROVIDER_BOUNDARY_CLOSURE_PACKET_v0_1.md",
    "docs/PROVIDER_BOUNDARY_ATTESTATION_v0_1.md",
    "docs/PROVIDER_BOUNDARY_FINALITY_PACKET_v0_1.md",
    "scripts/validate_provider_boundary_closure_packet_v0_1.py",
    "scripts/validate_provider_boundary_attestation_v0_1.py",
]

TEXT = [
    "Operational finality",
    "not truth finality",
    "does not grant authority",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    doc = ROOT / "docs" / "PROVIDER_BOUNDARY_FINALITY_PACKET_v0_1.md"
    if doc.is_file():
        body = doc.read_text(encoding="utf-8")
        for token in TEXT:
            if token not in body:
                errors.append(f"missing text: {token}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: provider boundary finality packet check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
