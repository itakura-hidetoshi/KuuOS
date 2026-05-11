#!/usr/bin/env python3
"""
validate_ai_yogacara_release_bundle_manifest_v0_1.py

Stdlib-only validator for the KuuOS AI Yogacara / Ten'i release bundle manifest.

Checks:
- all bundle files exist
- file SHA256 values match current contents
- bundle_root_hash matches ordered path+sha256 digest lines
- non-authority fixed points are present

No external dependencies and no external API calls.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "specs" / "ai_yogacara_release_bundle_manifest_v0_1.generated.json"
BUILDER_PATH = ROOT / "scripts" / "build_ai_yogacara_release_bundle_manifest_v0_1.py"

REQUIRED_FIXED_POINTS = [
    "release_bundle_manifest_is_integrity_surface_not_authority",
    "bundle_root_hash_proves_file_set_integrity_not_truth",
    "bundle_manifest_does_not_prove_teni_occurrence",
    "bundle_manifest_does_not_grant_execution_authority",
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


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("authority_note") != "integrity_surface_not_authority":
        errors.append("authority_note must be integrity_surface_not_authority")

    fixed_points = set(manifest.get("fixed_points", []))
    for fp in REQUIRED_FIXED_POINTS:
        if fp not in fixed_points:
            errors.append(f"missing fixed point: {fp}")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        return errors + ["manifest files must be a non-empty list"]

    for item in files:
        rel = item.get("path")
        expected_sha = item.get("sha256")
        expected_size = item.get("size_bytes")
        if not isinstance(rel, str):
            errors.append("file entry missing path string")
            continue
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing bundle file: {rel}")
            continue
        actual_sha = sha256_file(path)
        if expected_sha != actual_sha:
            errors.append(f"sha256 mismatch for {rel}: expected {expected_sha}, got {actual_sha}")
        if expected_size != path.stat().st_size:
            errors.append(f"size mismatch for {rel}: expected {expected_size}, got {path.stat().st_size}")

    actual_root = compute_root(files)
    if manifest.get("bundle_root_hash") != actual_root:
        errors.append(f"bundle_root_hash mismatch: expected {actual_root}, got {manifest.get('bundle_root_hash')}")
    return errors


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"ERROR: missing generated manifest: {MANIFEST_PATH.relative_to(ROOT)}")
        print(f"Run: python3 {BUILDER_PATH.relative_to(ROOT)}")
        return 1

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: manifest JSON invalid: {exc}")
        return 1

    errors = validate_manifest(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: AI Yogacara release bundle manifest validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
