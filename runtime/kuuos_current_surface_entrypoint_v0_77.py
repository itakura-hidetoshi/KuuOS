#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

from runtime import kuuos_current_root_sequence_v0_76 as current_root
from runtime import kuuos_current_status_surface_artifact_v0_75 as surface_artifact
from runtime import kuuos_current_status_surface_index_v0_76 as surface_index

VERSION = "kuuos_current_surface_entrypoint_v0_77"
DEPENDS_ON = surface_index.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
STABLE_ENTRYPOINT = "runtime/kuuos_current_surface.py"
STABLE_INDEX = surface_index.SURFACE_INDEX_PATH
STABLE_SURFACE_ARTIFACT = surface_artifact.SURFACE_ARTIFACT_PATH
ENTRYPOINT_SCHEMA_VERSION = "v0.77"


def current_surface() -> dict[str, Any]:
    return surface_artifact.load_surface_artifact()


def current_surface_index() -> dict[str, Any]:
    return surface_index.load_surface_index()


def entrypoint_issues() -> tuple[str, ...]:
    issues: list[str] = []
    index = current_surface_index()
    surface = current_surface()
    if STABLE_ENTRYPOINT != "runtime/kuuos_current_surface.py":
        issues.append("stable_entrypoint")
    if STABLE_INDEX != "status/current.surface.index.json":
        issues.append("stable_index")
    if STABLE_SURFACE_ARTIFACT != "status/current.surface.json":
        issues.append("stable_surface_artifact")
    if not surface_index.verify_surface_index():
        issues.append("surface_index_not_verified")
    if not surface_artifact.verify_artifact():
        issues.append("surface_artifact_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if index.get("surface_artifact") != STABLE_SURFACE_ARTIFACT:
        issues.append("index_surface_artifact_target")
    if index.get("surface_artifact_runtime") != "runtime/kuuos_current_status_surface_artifact_v0_75.py":
        issues.append("index_surface_artifact_runtime_target")
    if surface.get("authority_boundary") != "surface_not_authority_grant":
        issues.append("surface_authority_boundary")
    if surface.get("stable_manifest") != "status/current.manifest.json":
        issues.append("surface_stable_manifest")
    if surface.get("stable_resolved_status") != "status/current.resolved.json":
        issues.append("surface_stable_resolved_status")
    return tuple(issues)


def verify_entrypoint() -> bool:
    return entrypoint_issues() == ()


def current_surface_json() -> str:
    return json.dumps(current_surface(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = entrypoint_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(current_surface_json())
