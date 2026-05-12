#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_provider_boundary_bundle_v0_1.py"
MANIFEST = ROOT / "specs" / "provider_boundary_bundle_v0_1.generated.json"

REQUIRED = [
    "docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_EVENT_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/AI_PROVIDER_BOUNDARY_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/PROVIDER_BOUNDARY_BUNDLE_v0_1.md",
    "specs/ai_provider_boundary_fixtures_v0_1.json",
    "specs/ai_provider_boundary_audit_hash_chain_fixture_v0_1.jsonl",
    "specs/ai_provider_boundary_audit_worm_export_receipt_fixture_v0_1.json",
    "scripts/validate_ai_provider_boundary_runtime_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_event_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_hash_chain_v0_1.py",
    "scripts/validate_ai_provider_boundary_audit_worm_export_receipt_v0_1.py",
    "scripts/build_provider_boundary_bundle_v0_1.py",
    "scripts/validate_provider_boundary_bundle_v0_1.py",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_root(files: list[dict[str, Any]]) -> str:
    ordered = sorted(files, key=lambda x: x["path"])
    payload = "".join(item["path"] + item["sha256"] for item in ordered)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    result = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("authority_note") != "integrity_surface_only":
        errors.append("authority_note mismatch")
    files = manifest.get("files", [])
    listed = {item.get("path") for item in files if isinstance(item, dict)}
    for rel in REQUIRED:
        if rel not in listed:
            errors.append(f"missing required file: {rel}")
    for item in files:
        path = ROOT / item["path"]
        if item.get("sha256") != sha256_file(path):
            errors.append(f"sha mismatch: {item['path']}")
        if item.get("size_bytes") != path.stat().st_size:
            errors.append(f"size mismatch: {item['path']}")
    if manifest.get("bundle_root_hash") != compute_root(files):
        errors.append("bundle_root_hash mismatch")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: provider boundary bundle validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
