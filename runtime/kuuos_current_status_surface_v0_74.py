#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

from runtime import kuuos_current_resolved_status_artifact_v0_72 as resolved_artifact
from runtime import kuuos_current_root_sequence_v0_73 as current_root
from runtime import kuuos_current_status_manifest_v0_73 as manifest

VERSION = "kuuos_current_status_surface_v0_74"
DEPENDS_ON = manifest.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SURFACE_SCHEMA_VERSION = "v0.74"
STABLE_MANIFEST = manifest.MANIFEST_PATH
STABLE_RESOLVED_STATUS = resolved_artifact.RESOLVED_STATUS_PATH

REQUIRED_SURFACE_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_sequence",
    "manifest",
    "manifest_verified",
    "resolved_status",
    "resolved_status_verified",
    "stable_manifest",
    "stable_resolved_status",
    "surface_frontier",
    "surface_schema_version",
)


def status_surface() -> dict[str, Any]:
    return {
        "authority_boundary": "surface_not_authority_grant",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "manifest": manifest.load_manifest(),
        "manifest_verified": manifest.verify_manifest(),
        "resolved_status": resolved_artifact.load_resolved_artifact(),
        "resolved_status_verified": resolved_artifact.verify_artifact(),
        "stable_manifest": STABLE_MANIFEST,
        "stable_resolved_status": STABLE_RESOLVED_STATUS,
        "surface_frontier": VERSION,
        "surface_schema_version": SURFACE_SCHEMA_VERSION,
    }


def surface_issues() -> tuple[str, ...]:
    issues: list[str] = []
    surface = status_surface()
    missing = set(REQUIRED_SURFACE_KEYS).difference(surface)
    if missing:
        issues.append("missing_surface_keys:" + ",".join(sorted(missing)))
    extra = set(surface).difference(REQUIRED_SURFACE_KEYS)
    if extra:
        issues.append("extra_surface_keys:" + ",".join(sorted(extra)))
    if surface.get("surface_schema_version") != "v0.74":
        issues.append("surface_schema_version")
    if surface.get("surface_frontier") != VERSION:
        issues.append("surface_frontier")
    if surface.get("stable_manifest") != "status/current.manifest.json":
        issues.append("stable_manifest")
    if surface.get("stable_resolved_status") != "status/current.resolved.json":
        issues.append("stable_resolved_status")
    if surface.get("current_root_sequence") != "kuuos_current_root_sequence_v0_73":
        issues.append("current_root_sequence")
    if surface.get("authority_boundary") != "surface_not_authority_grant":
        issues.append("authority_boundary")
    if surface.get("manifest_verified") is not True:
        issues.append("manifest_verified")
    if surface.get("resolved_status_verified") is not True:
        issues.append("resolved_status_verified")
    current_manifest = surface.get("manifest", {})
    if current_manifest.get("current_resolved_status") != "status/current.resolved.json":
        issues.append("manifest_resolved_status_target")
    resolved = surface.get("resolved_status", {})
    if resolved.get("stable_entrypoint") != "runtime/kuuos_current_status.py":
        issues.append("resolved_stable_entrypoint")
    return tuple(issues)


def verify_surface() -> bool:
    return surface_issues() == ()


def surface_json() -> str:
    return json.dumps(status_surface(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = surface_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(surface_json())
