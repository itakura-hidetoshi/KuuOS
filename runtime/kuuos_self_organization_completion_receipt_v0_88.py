#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_87 as current_root
from runtime import kuuos_self_organization_bounded_change_v0_87 as bounded_change

VERSION = "kuuos_self_organization_completion_receipt_v0_88"
DEPENDS_ON = bounded_change.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
COMPLETION_RECEIPT_PATH = "status/self_organization_completion_receipt_v0_88.json"
COMPLETION_RECEIPT_SCHEMA_VERSION = "v0.88"

REQUIRED_COMPLETION_RECEIPT_KEYS: tuple[str, ...] = (
    "completion_receipt_frontier",
    "completion_receipt_schema_version",
    "completed_stage",
    "completed_stage_artifact",
    "completed_stage_frontier",
    "completed_stage_runtime",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "receipt_items",
    "receipt_mode",
    "source_bounded_change",
    "source_bounded_change_frontier",
    "source_bounded_change_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_completion_receipt() -> dict[str, Any]:
    return json.loads((_repo_root() / COMPLETION_RECEIPT_PATH).read_text(encoding="utf-8"))


def expected_completion_receipt() -> dict[str, Any]:
    return {
        "completion_receipt_frontier": VERSION,
        "completion_receipt_schema_version": COMPLETION_RECEIPT_SCHEMA_VERSION,
        "completed_stage": "v0.87",
        "completed_stage_artifact": bounded_change.BOUNDED_CHANGE_PATH,
        "completed_stage_frontier": bounded_change.VERSION,
        "completed_stage_runtime": "runtime/kuuos_self_organization_bounded_change_v0_87.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_next_cycle_seed_v0_89.json",
        "next_stage": "v0.89",
        "receipt_items": [
            "bounded_change_artifact_verified",
            "bounded_change_runtime_verified",
            "bounded_change_tests_connected",
            "current_root_sequence_connected",
            "review_loop_closed",
        ],
        "receipt_mode": "completion_receipt_only",
        "source_bounded_change": bounded_change.BOUNDED_CHANGE_PATH,
        "source_bounded_change_frontier": bounded_change.VERSION,
        "source_bounded_change_runtime": "runtime/kuuos_self_organization_bounded_change_v0_87.py",
    }


def completion_receipt_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        receipt = load_completion_receipt()
    except FileNotFoundError:
        return ("completion_receipt_missing",)
    except json.JSONDecodeError:
        return ("completion_receipt_invalid_json",)
    missing = set(REQUIRED_COMPLETION_RECEIPT_KEYS).difference(receipt)
    if missing:
        issues.append("missing_completion_receipt_keys:" + ",".join(sorted(missing)))
    extra = set(receipt).difference(REQUIRED_COMPLETION_RECEIPT_KEYS)
    if extra:
        issues.append("extra_completion_receipt_keys:" + ",".join(sorted(extra)))
    if receipt != expected_completion_receipt():
        issues.append("completion_receipt_mismatch")
    if receipt.get("receipt_mode") != "completion_receipt_only":
        issues.append("receipt_mode")
    if receipt.get("completed_stage") != "v0.87":
        issues.append("completed_stage")
    source = bounded_change.load_bounded_change()
    if source.get("next_artifact") != COMPLETION_RECEIPT_PATH:
        issues.append("source_next_artifact")
    if source.get("next_stage") != "v0.88":
        issues.append("source_next_stage")
    if source.get("change_mode") != "bounded_repository_change":
        issues.append("source_change_mode")
    if source.get("review_loop_closed") is not True:
        issues.append("source_review_loop_closed")
    if not bounded_change.verify_bounded_change():
        issues.append("bounded_change_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_completion_receipt() -> bool:
    return completion_receipt_issues() == ()


def completion_receipt_json() -> str:
    return json.dumps(load_completion_receipt(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = completion_receipt_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(completion_receipt_json())
