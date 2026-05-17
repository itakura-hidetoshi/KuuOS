#!/usr/bin/env python3
"""Manifest validator for Superstring Emptiness String / Brane / Membrane Runtime v0.2."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_ROLES = {
    "runtime_document",
    "contract",
    "validator",
    "validation_case_runner",
    "validation_cases",
    "example_packet",
    "lean_skeleton",
}

REQUIRED_GOVERNANCE_TRUE = [
    "additive_only",
    "overwrite_forbidden",
    "same_root_required",
    "fail_closed",
    "authority_non_expansion",
    "advisory_by_default",
]

REQUIRED_FIXED_POINTS = {
    "string_is_not_substance",
    "brane_is_not_absolute_world",
    "membrane_is_not_final_authority",
    "two_truths_gap_required",
    "indranet_graph_only_reduction_forbidden",
    "physics_bridge_does_not_open_execution_authority",
}


def validate_manifest(data: Dict[str, Any], repo_root: Path) -> List[str]:
    errors: List[str] = []
    if not data.get("id"):
        errors.append("manifest.id is required")
    if not data.get("version"):
        errors.append("manifest.version is required")

    files = data.get("files", [])
    if not isinstance(files, list) or not files:
        errors.append("manifest.files must be a non-empty list")
        return errors

    roles = set()
    for entry in files:
        if not isinstance(entry, dict):
            errors.append("each manifest file entry must be an object")
            continue
        path = entry.get("path")
        role = entry.get("role")
        if not path:
            errors.append("manifest file entry missing path")
        else:
            if not (repo_root / path).exists():
                errors.append(f"manifest path does not exist: {path}")
        if not role:
            errors.append(f"manifest file entry missing role for path: {path}")
        else:
            roles.add(role)

    missing_roles = sorted(REQUIRED_ROLES - roles)
    for role in missing_roles:
        errors.append(f"manifest missing required role: {role}")

    fixed_points = set(data.get("fixed_points", []))
    for fp in sorted(REQUIRED_FIXED_POINTS - fixed_points):
        errors.append(f"manifest missing fixed point: {fp}")

    governance = data.get("governance", {})
    if not isinstance(governance, dict):
        errors.append("manifest.governance must be an object")
    else:
        for key in REQUIRED_GOVERNANCE_TRUE:
            if governance.get(key) is not True:
                errors.append(f"manifest.governance.{key} must be true")

    return errors


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_superstring_emptiness_sbm_manifest_v0_2.py manifest.json", file=sys.stderr)
        return 2
    path = Path(argv[1])
    repo_root = Path.cwd()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_manifest(data, repo_root)
    except Exception as exc:
        errors = [str(exc)]
    ok = not errors
    print(json.dumps({"ok": ok, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
