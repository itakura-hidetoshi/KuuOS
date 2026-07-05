#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_resolved_status_artifact_v0_72 as resolved_artifact
from runtime import kuuos_current_root_sequence_v0_72 as current_root
from runtime import kuuos_current_status_pointer_v0_70 as pointer
from runtime import kuuos_self_organization_status_snapshot_v0_68 as snapshot
from runtime import kuuos_status_index_v0_69 as status_index

VERSION = "kuuos_current_status_manifest_v0_73"
DEPENDS_ON = resolved_artifact.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
MANIFEST_PATH = "status/current.manifest.json"
MANIFEST_SCHEMA_VERSION = "v0.73"

REQUIRED_MANIFEST_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_pointer",
    "current_resolved_status",
    "current_resolved_status_runtime",
    "current_root_check",
    "current_root_sequence",
    "current_status_cli",
    "current_status_index",
    "current_status_snapshot",
    "manifest_frontier",
    "manifest_schema_version",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest() -> dict[str, Any]:
    return json.loads((_repo_root() / MANIFEST_PATH).read_text(encoding="utf-8"))


def expected_manifest() -> dict[str, Any]:
    return {
        "authority_boundary": "manifest_not_authority_grant",
        "current_pointer": pointer.POINTER_PATH,
        "current_resolved_status": resolved_artifact.RESOLVED_STATUS_PATH,
        "current_resolved_status_runtime": "runtime/kuuos_current_resolved_status_artifact_v0_72.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "current_status_cli": "runtime/kuuos_current_status.py",
        "current_status_index": status_index.INDEX_PATH,
        "current_status_snapshot": snapshot.SNAPSHOT_PATH,
        "manifest_frontier": VERSION,
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
    }


def manifest_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        manifest = load_manifest()
    except FileNotFoundError:
        return ("manifest_missing",)
    except json.JSONDecodeError:
        return ("manifest_invalid_json",)
    missing = set(REQUIRED_MANIFEST_KEYS).difference(manifest)
    if missing:
        issues.append("missing_manifest_keys:" + ",".join(sorted(missing)))
    extra = set(manifest).difference(REQUIRED_MANIFEST_KEYS)
    if extra:
        issues.append("extra_manifest_keys:" + ",".join(sorted(extra)))
    expected = expected_manifest()
    for key, value in expected.items():
        if manifest.get(key) != value:
            issues.append("manifest_mismatch:" + key)
    if not pointer.verify_pointer():
        issues.append("pointer_not_verified")
    if not status_index.verify_index():
        issues.append("status_index_not_verified")
    if not snapshot.verify_snapshot():
        issues.append("snapshot_not_verified")
    if not resolved_artifact.verify_artifact():
        issues.append("resolved_artifact_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if manifest.get("authority_boundary") != "manifest_not_authority_grant":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_manifest() -> bool:
    return manifest_issues() == ()


def manifest_json() -> str:
    return json.dumps(load_manifest(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = manifest_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(manifest_json())
