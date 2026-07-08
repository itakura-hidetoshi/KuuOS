#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_104 as current_root
from runtime import kuuos_self_organization_candidate_queue_v0_104 as queue

VERSION = "kuuos_self_organization_candidate_receipt_v0_105"
DEPENDS_ON = queue.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
CANDIDATE_RECEIPT_PATH = "status/self_organization_candidate_receipt_v0_105.json"
CANDIDATE_RECEIPT_SCHEMA_VERSION = "v0.105"

REQUIRED_CANDIDATE_RECEIPT_KEYS: tuple[str, ...] = (
    "candidate_count",
    "candidate_ids",
    "candidate_queue",
    "candidate_queue_frontier",
    "candidate_queue_runtime",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "receipt_frontier",
    "receipt_mode",
    "receipt_schema_version",
    "receipt_scope",
    "selection_authorized",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_candidate_receipt() -> dict[str, Any]:
    return json.loads((_repo_root() / CANDIDATE_RECEIPT_PATH).read_text(encoding="utf-8"))


def expected_candidate_receipt() -> dict[str, Any]:
    return {
        "candidate_count": len(queue.expected_candidate_ids()),
        "candidate_ids": queue.expected_candidate_ids(),
        "candidate_queue": queue.CANDIDATE_QUEUE_PATH,
        "candidate_queue_frontier": queue.VERSION,
        "candidate_queue_runtime": "runtime/kuuos_self_organization_candidate_queue_v0_104.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_selection_policy_v0_106.json",
        "next_stage": "v0.106",
        "receipt_frontier": VERSION,
        "receipt_mode": "candidate_receipt_only",
        "receipt_schema_version": CANDIDATE_RECEIPT_SCHEMA_VERSION,
        "receipt_scope": "self_organization_next_cycle",
        "selection_authorized": False,
    }


def candidate_receipt_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        receipt = load_candidate_receipt()
    except FileNotFoundError:
        return ("candidate_receipt_missing",)
    except json.JSONDecodeError:
        return ("candidate_receipt_invalid_json",)
    missing = set(REQUIRED_CANDIDATE_RECEIPT_KEYS).difference(receipt)
    if missing:
        issues.append("missing_candidate_receipt_keys:" + ",".join(sorted(missing)))
    extra = set(receipt).difference(REQUIRED_CANDIDATE_RECEIPT_KEYS)
    if extra:
        issues.append("extra_candidate_receipt_keys:" + ",".join(sorted(extra)))
    if receipt != expected_candidate_receipt():
        issues.append("candidate_receipt_mismatch")
    if receipt.get("candidate_count") != len(receipt.get("candidate_ids", [])):
        issues.append("candidate_count")
    if receipt.get("candidate_ids") != queue.expected_candidate_ids():
        issues.append("candidate_ids")
    if receipt.get("receipt_mode") != "candidate_receipt_only":
        issues.append("receipt_mode")
    if receipt.get("selection_authorized") is not False:
        issues.append("selection_authorized")
    if receipt.get("next_artifact") != "status/self_organization_selection_policy_v0_106.json":
        issues.append("next_artifact")
    if receipt.get("next_stage") != "v0.106":
        issues.append("next_stage")
    source = queue.load_candidate_queue()
    if source.get("next_artifact") != CANDIDATE_RECEIPT_PATH:
        issues.append("queue_next_artifact")
    if source.get("next_stage") != "v0.105":
        issues.append("queue_next_stage")
    if source.get("candidate_ids") != receipt.get("candidate_ids"):
        issues.append("queue_candidate_ids")
    if not queue.verify_candidate_queue():
        issues.append("candidate_queue_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_candidate_receipt() -> bool:
    return candidate_receipt_issues() == ()


def candidate_receipt_json() -> str:
    return json.dumps(load_candidate_receipt(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = candidate_receipt_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(candidate_receipt_json())
