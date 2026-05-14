#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_two_truths_runtime_bundle_v0_1.py"
MANIFEST = ROOT / "specs" / "two_truths_runtime_bundle_v0_1.generated.json"

FALSE_KEYS = [
    "paramartha_objectification_allowed",
    "samvrti_denial_allowed",
    "ultimate_to_conventional_collapse_allowed",
    "conventional_to_ultimate_collapse_allowed",
]


def calc_root(files: list[dict]) -> str:
    ordered = sorted(files, key=lambda x: x["path"])
    payload = "".join(x["path"] + x["sha256"] for x in ordered)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if manifest.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
        errors.append("mass_gap_bridge_role mismatch")
    if manifest.get("mass_gap_bridge_authority") != "forbidden":
        errors.append("mass_gap_bridge_authority must be forbidden")
    for key in FALSE_KEYS:
        if manifest.get(key) is not False:
            errors.append(f"{key} must be false")
    files = manifest.get("files", [])
    if manifest.get("bundle_root_hash") != calc_root(files):
        errors.append("bundle_root_hash mismatch")
    for item in files:
        if not (ROOT / item["path"]).is_file():
            errors.append(f"missing: {item['path']}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: Two Truths runtime bundle checked root={manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
