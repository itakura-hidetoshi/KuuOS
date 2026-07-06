#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_79 as current_root
from runtime import kuuos_self_organization_candidate_queue_v0_79 as candidate_queue

VERSION = "kuuos_self_organization_candidate_receipt_v0_80"
DEPENDS_ON = candidate_queue.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
CANDIDATE_RECEIPT_PATH = "status/self_organization_candidate_receipt_v0_80.json"
RECEIPT_SCHEMA_VERSION = "v0.80"

REQUIRED_RECEIPT_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "candidate_count",
    "candidate_ids",
    "candidate_queue",
    "candidate_queue_frontier",
    "candidate_queue_runtime",
    "current_root_check",
    "current_root_sequence",
    "receipt_frontier",
    "receipt_mode",
    "receipt_schema_version",
    "selection_authorized",
    "source_surface_index",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_candidate_receipt() -> dict[str, Any]:
    return json.loads((_repo_root() / CANDIDATE_RECEIPT_PATH).read_text(encoding="utf-8"))


def candidate_ids_from_queue() -> list[str]:
    queue = candidate_queue.load_candidate_queue()
    return [str(candidate["candidate_id"]) for candidate in queue["candidates"]]


def expected_candidate_receipt() -> dict[str, Any]:
    ids = candidate_ids_from_queue()
    return {
        "authority_boundary": "candidate_receipt_not_authority_grant",
        "candidate_count": len(ids),
        "candidate_ids": ids,
        "candidate_queue": candidate_queue.CANDIDATE_QUEUE_PATH,
        "candidate_queue_frontier": candidate_queue.VERSION,
        "candidate_queue_runtime": "runtime/kuuos_self_organization_candidate_queue_v0_79.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "receipt_frontier": VERSION,
        "receipt_mode": "queue_receipt_only",
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "selection_authorized": False,
        "source_surface_index": "status/current.surface.index.json",
    }


def candidate_receipt_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        receipt = load_candidate_receipt()
    except FileNotFoundError:
        return ("candidate_receipt_missing",)
    except json.JSONDecodeError:
        return ("candidate_receipt_invalid_json",)
    missing = set(REQUIRED_RECEIPT_KEYS).difference(receipt)
    if missing:
        issues.append("missing_candidate_receipt_keys:" + ",".join(sorted(missing)))
    extra = set(receipt).difference(REQUIRED_RECEIPT_KEYS)
    if extra:
        issues.append("extra_candidate_receipt_keys:" + ",".join(sorted(extra)))
    if receipt != expected_candidate_receipt():
        issues.append("candidate_receipt_mismatch")
    if receipt.get("authority_boundary") != "candidate_receipt_not_authority_grant":
        issues.append("authority_boundary")
    if receipt.get("receipt_mode") != "queue_receipt_only":
        issues.append("receipt_mode")
    if receipt.get("selection_authorized") is not False:
        issues.append("selection_authorized")
    if receipt.get("candidate_count") != len(candidate_ids_from_queue()):
        issues.append("candidate_count")
    if receipt.get("candidate_ids") != candidate_ids_from_queue():
        issues.append("candidate_ids")
    if not candidate_queue.verify_candidate_queue():
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
