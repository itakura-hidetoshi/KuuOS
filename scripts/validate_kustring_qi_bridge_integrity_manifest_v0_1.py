#!/usr/bin/env python3
"""Validate KuString Qi Bridge integrity manifest v0.1."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_kustring_qi_bridge_integrity_manifest_v0_1.py"

FALSE_AUTHORITY_KEYS = [
    "integrity_manifest_grants_execution_authority",
    "integrity_manifest_grants_truth_authority",
    "integrity_manifest_grants_theorem_authority",
    "integrity_manifest_grants_medical_act_authorization",
]

TRUE_LINEAGE_KEYS = [
    "same_root_required",
    "append_only",
    "overwrite_forbidden",
    "destructive_replacement_forbidden",
]


def fail(message: str) -> int:
    print(f"[kustring-qi-bridge-integrity] FAIL: {message}", file=sys.stderr)
    return 1


def load_builder():
    spec = importlib.util.spec_from_file_location("build_kustring_qi_bridge_integrity_manifest_v0_1", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load integrity manifest builder")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("manifest_id") != "kustring_qi_bridge_integrity_manifest_v0_1":
        errors.append("manifest_id mismatch")
    if manifest.get("status") != "generated_integrity_manifest":
        errors.append("status must be generated_integrity_manifest")
    if manifest.get("module") != "KuStringQiBridge":
        errors.append("module must be KuStringQiBridge")
    if manifest.get("version") != "v0_1":
        errors.append("version must be v0_1")
    root = manifest.get("bundle_root_sha256", "")
    if not isinstance(root, str) or len(root) != 64:
        errors.append("bundle_root_sha256 must be 64 hex characters")
    entries = manifest.get("entries", [])
    if manifest.get("entry_count") != len(entries):
        errors.append("entry_count must equal number of entries")
    if len(entries) < 14:
        errors.append("integrity manifest must include at least 14 entries")
    seen = set()
    for entry in entries:
        rel_path = entry.get("path")
        if not rel_path:
            errors.append("entry path missing")
            continue
        if rel_path in seen:
            errors.append(f"duplicate manifest entry: {rel_path}")
        seen.add(rel_path)
        if not (ROOT / rel_path).exists():
            errors.append(f"manifest entry missing file: {rel_path}")
        digest = entry.get("sha256", "")
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append(f"entry {rel_path} sha256 must be 64 hex characters")
        if not isinstance(entry.get("size_bytes"), int) or entry.get("size_bytes") <= 0:
            errors.append(f"entry {rel_path} size_bytes must be positive")
    authority = manifest.get("authority_boundary", {})
    for key in FALSE_AUTHORITY_KEYS:
        if authority.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")
    lineage = manifest.get("lineage_policy", {})
    for key in TRUE_LINEAGE_KEYS:
        if lineage.get(key) is not True:
            errors.append(f"lineage_policy.{key} must be true")
    return errors


def main() -> int:
    if not BUILDER_PATH.exists():
        return fail("missing integrity manifest builder")
    try:
        builder = load_builder()
        manifest = builder.build_manifest()
        errors = validate_manifest(manifest)
    except Exception as exc:
        return fail(f"integrity manifest generation failed: {exc}")

    if errors:
        for err in errors:
            print(f"[kustring-qi-bridge-integrity] ERROR: {err}", file=sys.stderr)
        return 1

    print(f"[kustring-qi-bridge-integrity] PASS root={manifest['bundle_root_sha256']} entries={manifest['entry_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())