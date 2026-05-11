#!/usr/bin/env python3
"""
validate_invariant_pipeline_bundle_closure_inclusion_v0_1.py

Stdlib-only validator that ensures release closure packet surfaces are included
in the generated invariant pipeline release bundle manifest.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_invariant_pipeline_release_bundle_manifest_v0_1.py"
MANIFEST = ROOT / "specs" / "invariant_pipeline_release_bundle_manifest_v0_1.generated.json"

REQUIRED_CLOSURE_FILES = [
    "docs/INVARIANT_PIPELINE_RELEASE_CLOSURE_PACKET_v0_1.md",
    "scripts/validate_invariant_pipeline_release_closure_packet_v0_1.py",
]


def main() -> int:
    result = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    listed_paths = {item.get("path") for item in manifest.get("files", []) if isinstance(item, dict)}

    errors: list[str] = []
    for rel in REQUIRED_CLOSURE_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing closure file on disk: {rel}")
        if rel not in listed_paths:
            errors.append(f"closure file missing from bundle manifest: {rel}")

    if manifest.get("authority_note") != "integrity_surface_not_authority":
        errors.append("bundle authority_note must remain integrity_surface_not_authority")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Invariant Pipeline release closure files included in bundle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
