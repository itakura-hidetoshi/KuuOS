#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_74 as current_root
from runtime import kuuos_current_status_surface_v0_74 as surface

VERSION = "kuuos_current_status_surface_artifact_v0_75"
DEPENDS_ON = surface.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SURFACE_ARTIFACT_PATH = "status/current.surface.json"
ARTIFACT_SCHEMA_VERSION = "v0.75"

REQUIRED_ARTIFACT_KEYS: tuple[str, ...] = surface.REQUIRED_SURFACE_KEYS


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_surface_artifact() -> dict[str, Any]:
    return json.loads((_repo_root() / SURFACE_ARTIFACT_PATH).read_text(encoding="utf-8"))


def expected_surface_artifact() -> dict[str, Any]:
    return surface.status_surface()


def artifact_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        artifact = load_surface_artifact()
    except FileNotFoundError:
        return ("surface_artifact_missing",)
    except json.JSONDecodeError:
        return ("surface_artifact_invalid_json",)
    missing = set(REQUIRED_ARTIFACT_KEYS).difference(artifact)
    if missing:
        issues.append("missing_surface_artifact_keys:" + ",".join(sorted(missing)))
    extra = set(artifact).difference(REQUIRED_ARTIFACT_KEYS)
    if extra:
        issues.append("extra_surface_artifact_keys:" + ",".join(sorted(extra)))
    expected = expected_surface_artifact()
    if artifact != expected:
        issues.append("surface_artifact_mismatch")
    if not surface.verify_surface():
        issues.append("surface_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if artifact.get("authority_boundary") != "surface_not_authority_grant":
        issues.append("authority_boundary")
    if artifact.get("stable_manifest") != "status/current.manifest.json":
        issues.append("stable_manifest")
    if artifact.get("stable_resolved_status") != "status/current.resolved.json":
        issues.append("stable_resolved_status")
    return tuple(issues)


def verify_artifact() -> bool:
    return artifact_issues() == ()


def artifact_json() -> str:
    return json.dumps(load_surface_artifact(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = artifact_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(artifact_json())
