#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_71 as current_root
from runtime import kuuos_current_status_resolver_v0_71 as resolver

VERSION = "kuuos_current_resolved_status_artifact_v0_72"
DEPENDS_ON = resolver.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
RESOLVED_STATUS_PATH = "status/current.resolved.json"
ARTIFACT_SCHEMA_VERSION = "v0.72"

REQUIRED_ARTIFACT_KEYS: tuple[str, ...] = resolver.REQUIRED_RESOLVED_KEYS


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_resolved_artifact() -> dict[str, Any]:
    return json.loads((_repo_root() / RESOLVED_STATUS_PATH).read_text(encoding="utf-8"))


def expected_resolved_artifact() -> dict[str, Any]:
    return resolver.resolved_status()


def artifact_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        artifact = load_resolved_artifact()
    except FileNotFoundError:
        return ("resolved_artifact_missing",)
    except json.JSONDecodeError:
        return ("resolved_artifact_invalid_json",)
    missing = set(REQUIRED_ARTIFACT_KEYS).difference(artifact)
    if missing:
        issues.append("missing_resolved_artifact_keys:" + ",".join(sorted(missing)))
    extra = set(artifact).difference(REQUIRED_ARTIFACT_KEYS)
    if extra:
        issues.append("extra_resolved_artifact_keys:" + ",".join(sorted(extra)))
    expected = expected_resolved_artifact()
    if artifact != expected:
        issues.append("resolved_artifact_mismatch")
    if not resolver.verify_resolver():
        issues.append("resolver_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    if artifact.get("authority_boundary") != "resolver_not_authority_grant":
        issues.append("authority_boundary")
    if artifact.get("stable_entrypoint") != "runtime/kuuos_current_status.py":
        issues.append("stable_entrypoint")
    return tuple(issues)


def verify_artifact() -> bool:
    return artifact_issues() == ()


def artifact_json() -> str:
    return json.dumps(load_resolved_artifact(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = artifact_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(artifact_json())
