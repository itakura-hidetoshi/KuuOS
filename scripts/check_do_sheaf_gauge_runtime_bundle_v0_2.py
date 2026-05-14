#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_do_sheaf_gauge_runtime_bundle_v0_2.py"
MANIFEST = ROOT / "specs" / "do_sheaf_gauge_runtime_bundle_v0_2.generated.json"
TRUE_FIELDS = [
    "site_cover_required",
    "gluing_required",
    "gauge_connection_required",
    "holonomy_record_required",
    "curvature_visibility_required",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_root(files: list[dict[str, Any]]) -> str:
    ordered = sorted(files, key=lambda x: x["path"])
    payload = "".join(e["path"] + e["sha256"] for e in ordered)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("authority_note") != "do_sheaf_gauge_runtime_integrity_surface_only":
        errors.append("authority_note mismatch")
    if manifest.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if manifest.get("graph_only_model_allowed") is not False:
        errors.append("graph_only_model_allowed must be false")
    for field in TRUE_FIELDS:
        if manifest.get(field) is not True:
            errors.append(f"{field} must be true")
    files = manifest.get("files", [])
    if not files:
        errors.append("bundle files empty")
    for item in files:
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append(f"missing file: {item['path']}")
            continue
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
    print(f"PASS: DO sheaf gauge runtime bundle checked root={manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
