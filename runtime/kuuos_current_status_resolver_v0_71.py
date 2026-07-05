#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

from runtime import kuuos_current_status_pointer_v0_70 as pointer
from runtime import kuuos_self_organization_status_snapshot_v0_68 as snapshot
from runtime import kuuos_status_index_v0_69 as status_index

VERSION = "kuuos_current_status_resolver_v0_71"
DEPENDS_ON = pointer.VERSION
RESOLVER_SCHEMA_VERSION = "v0.71"
STABLE_ENTRYPOINT = "runtime/kuuos_current_status.py"

REQUIRED_RESOLVED_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_pointer",
    "current_status_index",
    "current_status_snapshot",
    "pointer_verified",
    "resolver_frontier",
    "resolver_schema_version",
    "snapshot_verified",
    "status_index_verified",
    "stable_entrypoint",
)


def resolved_status() -> dict[str, Any]:
    current_pointer = pointer.load_pointer()
    current_index = status_index.load_index()
    current_snapshot = snapshot.load_snapshot()
    return {
        "authority_boundary": "resolver_not_authority_grant",
        "current_pointer": current_pointer,
        "current_status_index": current_index,
        "current_status_snapshot": current_snapshot,
        "pointer_verified": pointer.verify_pointer(),
        "resolver_frontier": VERSION,
        "resolver_schema_version": RESOLVER_SCHEMA_VERSION,
        "snapshot_verified": snapshot.verify_snapshot(),
        "status_index_verified": status_index.verify_index(),
        "stable_entrypoint": STABLE_ENTRYPOINT,
    }


def resolver_issues() -> tuple[str, ...]:
    issues: list[str] = []
    resolved = resolved_status()
    missing = set(REQUIRED_RESOLVED_KEYS).difference(resolved)
    if missing:
        issues.append("missing_resolved_keys:" + ",".join(sorted(missing)))
    extra = set(resolved).difference(REQUIRED_RESOLVED_KEYS)
    if extra:
        issues.append("extra_resolved_keys:" + ",".join(sorted(extra)))
    if resolved.get("resolver_schema_version") != "v0.71":
        issues.append("resolver_schema_version")
    if resolved.get("resolver_frontier") != VERSION:
        issues.append("resolver_frontier")
    if resolved.get("stable_entrypoint") != "runtime/kuuos_current_status.py":
        issues.append("stable_entrypoint")
    if resolved.get("authority_boundary") != "resolver_not_authority_grant":
        issues.append("authority_boundary")
    if resolved.get("pointer_verified") is not True:
        issues.append("pointer_verified")
    if resolved.get("status_index_verified") is not True:
        issues.append("status_index_verified")
    if resolved.get("snapshot_verified") is not True:
        issues.append("snapshot_verified")
    current_pointer = resolved.get("current_pointer", {})
    if current_pointer.get("current_status_index") != "status/kuuos_status_index_v0_69.json":
        issues.append("current_pointer_target")
    current_index = resolved.get("current_status_index", {})
    if current_index.get("latest_self_organization_snapshot") != "status/kuuos_self_organization_status_v0_68.json":
        issues.append("current_index_snapshot_target")
    current_snapshot = resolved.get("current_status_snapshot", {})
    if current_snapshot.get("active") is not True:
        issues.append("current_snapshot_active")
    return tuple(issues)


def verify_resolver() -> bool:
    return resolver_issues() == ()


def resolved_status_json() -> str:
    return json.dumps(resolved_status(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = resolver_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(resolved_status_json())
