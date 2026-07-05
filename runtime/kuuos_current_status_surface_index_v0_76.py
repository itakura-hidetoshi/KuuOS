#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_75 as current_root
from runtime import kuuos_current_status_manifest_v0_73 as manifest
from runtime import kuuos_current_status_surface_artifact_v0_75 as surface_artifact
from runtime import kuuos_current_status_surface_v0_74 as surface_runtime

VERSION = "kuuos_current_status_surface_index_v0_76"
DEPENDS_ON = surface_artifact.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SURFACE_INDEX_PATH = "status/current.surface.index.json"
SURFACE_INDEX_SCHEMA_VERSION = "v0.76"

REQUIRED_SURFACE_INDEX_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "stable_manifest",
    "stable_resolved_status",
    "surface_artifact",
    "surface_artifact_runtime",
    "surface_index_frontier",
    "surface_index_schema_version",
    "surface_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_surface_index() -> dict[str, Any]:
    return json.loads((_repo_root() / SURFACE_INDEX_PATH).read_text(encoding="utf-8"))


def expected_surface_index() -> dict[str, Any]:
    return {
        "authority_boundary": "surface_index_not_authority_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "stable_manifest": manifest.MANIFEST_PATH,
        "stable_resolved_status": surface_runtime.STABLE_RESOLVED_STATUS,
        "surface_artifact": surface_artifact.SURFACE_ARTIFACT_PATH,
        "surface_artifact_runtime": "runtime/kuuos_current_status_surface_artifact_v0_75.py",
        "surface_index_frontier": VERSION,
        "surface_index_schema_version": SURFACE_INDEX_SCHEMA_VERSION,
        "surface_runtime": "runtime/kuuos_current_status_surface_v0_74.py",
    }


def surface_index_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        index = load_surface_index()
    except FileNotFoundError:
        return ("surface_index_missing",)
    except json.JSONDecodeError:
        return ("surface_index_invalid_json",)
    missing = set(REQUIRED_SURFACE_INDEX_KEYS).difference(index)
    if missing:
        issues.append("missing_surface_index_keys:" + ",".join(sorted(missing)))
    extra = set(index).difference(REQUIRED_SURFACE_INDEX_KEYS)
    if extra:
        issues.append("extra_surface_index_keys:" + ",".join(sorted(extra)))
    expected = expected_surface_index()
    for key, value in expected.items():
        if index.get(key) != value:
            issues.append("surface_index_mismatch:" + key)
    if not manifest.verify_manifest():
        issues.append("manifest_not_verified")
    if not surface_runtime.verify_surface():
        issues.append("surface_runtime_not_verified")
    if not surface_artifact.verify_artifact():
        issues.append("surface_artifact_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if index.get("authority_boundary") != "surface_index_not_authority_grant":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_surface_index() -> bool:
    return surface_index_issues() == ()


def surface_index_json() -> str:
    return json.dumps(load_surface_index(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = surface_index_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(surface_index_json())
