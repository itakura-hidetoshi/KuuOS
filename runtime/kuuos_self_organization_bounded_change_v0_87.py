#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_86 as current_root
from runtime import kuuos_self_organization_review_decision_v0_86 as decision

VERSION = "kuuos_self_organization_bounded_change_v0_87"
DEPENDS_ON = decision.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
BOUNDED_CHANGE_PATH = "status/self_organization_bounded_change_v0_87.json"
BOUNDED_CHANGE_SCHEMA_VERSION = "v0.87"

REQUIRED_BOUNDED_CHANGE_KEYS: tuple[str, ...] = (
    "bounded_change_frontier",
    "bounded_change_schema_version",
    "change_items",
    "change_mode",
    "change_scope",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "review_loop_closed",
    "scope_boundary",
    "source_decision",
    "source_decision_frontier",
    "source_decision_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_bounded_change() -> dict[str, Any]:
    return json.loads((_repo_root() / BOUNDED_CHANGE_PATH).read_text(encoding="utf-8"))


def expected_bounded_change() -> dict[str, Any]:
    return {
        "bounded_change_frontier": VERSION,
        "bounded_change_schema_version": BOUNDED_CHANGE_SCHEMA_VERSION,
        "change_items": [
            "bounded_change_artifact_v0_87",
            "bounded_change_runtime_v0_87",
            "bounded_change_tests_v0_87",
            "current_root_sequence_v0_87",
        ],
        "change_mode": "bounded_repository_change",
        "change_scope": "self_organization_current_root_artifact",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_completion_receipt_v0_88.json",
        "next_stage": "v0.88",
        "review_loop_closed": True,
        "scope_boundary": "bounded_change_record_only",
        "source_decision": decision.REVIEW_DECISION_PATH,
        "source_decision_frontier": decision.VERSION,
        "source_decision_runtime": "runtime/kuuos_self_organization_review_decision_v0_86.py",
    }


def bounded_change_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        bounded = load_bounded_change()
    except FileNotFoundError:
        return ("bounded_change_missing",)
    except json.JSONDecodeError:
        return ("bounded_change_invalid_json",)
    missing = set(REQUIRED_BOUNDED_CHANGE_KEYS).difference(bounded)
    if missing:
        issues.append("missing_bounded_change_keys:" + ",".join(sorted(missing)))
    extra = set(bounded).difference(REQUIRED_BOUNDED_CHANGE_KEYS)
    if extra:
        issues.append("extra_bounded_change_keys:" + ",".join(sorted(extra)))
    if bounded != expected_bounded_change():
        issues.append("bounded_change_mismatch")
    if bounded.get("change_mode") != "bounded_repository_change":
        issues.append("change_mode")
    if bounded.get("scope_boundary") != "bounded_change_record_only":
        issues.append("scope_boundary")
    if bounded.get("review_loop_closed") is not True:
        issues.append("review_loop_closed")
    source = decision.load_review_decision()
    if source.get("review_loop_closed") is not True:
        issues.append("source_decision_review_loop_closed")
    if source.get("decision_mode") != "bounded_action_transition":
        issues.append("source_decision_mode")
    if source.get("next_stage_kind") != "bounded_repository_change":
        issues.append("source_next_stage_kind")
    if source.get("next_artifact") != BOUNDED_CHANGE_PATH:
        issues.append("source_next_artifact")
    if source.get("next_stage") != "v0.87":
        issues.append("source_next_stage")
    if not decision.verify_review_decision():
        issues.append("review_decision_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_bounded_change() -> bool:
    return bounded_change_issues() == ()


def bounded_change_json() -> str:
    return json.dumps(load_bounded_change(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = bounded_change_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(bounded_change_json())
