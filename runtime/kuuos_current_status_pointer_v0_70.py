#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_70 as current_root
from runtime import kuuos_status_index_v0_69 as status_index

VERSION = "kuuos_current_status_pointer_v0_70"
DEPENDS_ON = status_index.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
POINTER_PATH = "status/current.json"
POINTER_SCHEMA_VERSION = "v0.70"

REQUIRED_POINTER_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_pointer_frontier",
    "current_root_check",
    "current_root_sequence",
    "current_status_index",
    "current_status_index_runtime",
    "pointer_schema_version",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_pointer() -> dict[str, Any]:
    return json.loads((_repo_root() / POINTER_PATH).read_text(encoding="utf-8"))


def expected_pointer() -> dict[str, Any]:
    return {
        "authority_boundary": "current_pointer_not_authority_grant",
        "current_pointer_frontier": VERSION,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "current_status_index": status_index.INDEX_PATH,
        "current_status_index_runtime": "runtime/kuuos_status_index_v0_69.py",
        "pointer_schema_version": POINTER_SCHEMA_VERSION,
    }


def pointer_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        pointer = load_pointer()
    except FileNotFoundError:
        return ("pointer_missing",)
    except json.JSONDecodeError:
        return ("pointer_invalid_json",)
    missing = set(REQUIRED_POINTER_KEYS).difference(pointer)
    if missing:
        issues.append("missing_pointer_keys:" + ",".join(sorted(missing)))
    extra = set(pointer).difference(REQUIRED_POINTER_KEYS)
    if extra:
        issues.append("extra_pointer_keys:" + ",".join(sorted(extra)))
    expected = expected_pointer()
    for key, value in expected.items():
        if pointer.get(key) != value:
            issues.append("pointer_mismatch:" + key)
    if not status_index.verify_index():
        issues.append("current_status_index_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if pointer.get("authority_boundary") != "current_pointer_not_authority_grant":
        issues.append("authority_boundary")
    return tuple(issues)


def verify_pointer() -> bool:
    return pointer_issues() == ()


if __name__ == "__main__":
    issues = pointer_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(json.dumps(load_pointer(), ensure_ascii=False, sort_keys=True, indent=2))
