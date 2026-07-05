#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_67 as current_root
from runtime import kuuos_self_organization_status_v0_67 as live_status

VERSION = "kuuos_self_organization_status_snapshot_v0_68"
DEPENDS_ON = live_status.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
SNAPSHOT_PATH = "status/kuuos_self_organization_status_v0_68.json"
SNAPSHOT_SCHEMA_VERSION = "v0.68"

REQUIRED_SNAPSHOT_KEYS: tuple[str, ...] = live_status.REQUIRED_STATUS_KEYS + (
    "snapshot_schema_version",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_snapshot() -> dict[str, Any]:
    return json.loads((_repo_root() / SNAPSHOT_PATH).read_text(encoding="utf-8"))


def expected_snapshot() -> dict[str, Any]:
    status = live_status.build_status()
    status["current_root_sequence"] = CURRENT_ROOT_SEQUENCE
    status["current_root_sequence_verified"] = current_root.verify_current_root_sequence()
    status["snapshot_schema_version"] = SNAPSHOT_SCHEMA_VERSION
    return status


def snapshot_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        snapshot = load_snapshot()
    except FileNotFoundError:
        return ("snapshot_missing",)
    except json.JSONDecodeError:
        return ("snapshot_invalid_json",)
    expected = expected_snapshot()
    missing = set(REQUIRED_SNAPSHOT_KEYS).difference(snapshot)
    if missing:
        issues.append("missing_snapshot_keys:" + ",".join(sorted(missing)))
    extra = set(snapshot).difference(REQUIRED_SNAPSHOT_KEYS)
    if extra:
        issues.append("extra_snapshot_keys:" + ",".join(sorted(extra)))
    for key, value in expected.items():
        if snapshot.get(key) != value:
            issues.append("snapshot_mismatch:" + key)
    if snapshot.get("snapshot_schema_version") != "v0.68":
        issues.append("snapshot_schema_version")
    if snapshot.get("authority_boundary") != "active_state_not_unbounded_authority":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_snapshot() -> bool:
    return snapshot_issues() == ()


if __name__ == "__main__":
    issues = snapshot_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(json.dumps(load_snapshot(), ensure_ascii=False, sort_keys=True, indent=2))
