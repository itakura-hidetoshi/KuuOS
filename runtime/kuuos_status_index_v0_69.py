#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_68 as current_root
from runtime import kuuos_self_organization_status_snapshot_v0_68 as snapshot

VERSION = "kuuos_status_index_v0_69"
DEPENDS_ON = snapshot.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
INDEX_PATH = "status/kuuos_status_index_v0_69.json"
INDEX_SCHEMA_VERSION = "v0.69"

REQUIRED_INDEX_KEYS: tuple[str, ...] = (
    "active_self_organization",
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "index_schema_version",
    "latest_self_organization_snapshot",
    "latest_self_organization_snapshot_runtime",
    "status_index_frontier",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_index() -> dict[str, Any]:
    return json.loads((_repo_root() / INDEX_PATH).read_text(encoding="utf-8"))


def expected_index() -> dict[str, Any]:
    return {
        "active_self_organization": True,
        "authority_boundary": "status_index_not_authority_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "latest_self_organization_snapshot": snapshot.SNAPSHOT_PATH,
        "latest_self_organization_snapshot_runtime": "runtime/kuuos_self_organization_status_snapshot_v0_68.py",
        "status_index_frontier": VERSION,
    }


def index_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        index = load_index()
    except FileNotFoundError:
        return ("index_missing",)
    except json.JSONDecodeError:
        return ("index_invalid_json",)
    missing = set(REQUIRED_INDEX_KEYS).difference(index)
    if missing:
        issues.append("missing_index_keys:" + ",".join(sorted(missing)))
    extra = set(index).difference(REQUIRED_INDEX_KEYS)
    if extra:
        issues.append("extra_index_keys:" + ",".join(sorted(extra)))
    expected = expected_index()
    for key, value in expected.items():
        if index.get(key) != value:
            issues.append("index_mismatch:" + key)
    if not snapshot.verify_snapshot():
        issues.append("latest_snapshot_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if index.get("authority_boundary") != "status_index_not_authority_grant":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_index() -> bool:
    return index_issues() == ()


if __name__ == "__main__":
    issues = index_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(json.dumps(load_index(), ensure_ascii=False, sort_keys=True, indent=2))
