#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_102 as current_root
from runtime import kuuos_self_organization_completion_receipt_v0_102 as receipt

VERSION = "kuuos_self_organization_next_cycle_seed_v0_103"
DEPENDS_ON = receipt.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
NEXT_CYCLE_SEED_PATH = "status/self_organization_next_cycle_seed_v0_103.json"
NEXT_CYCLE_SEED_SCHEMA_VERSION = "v0.103"

REQUIRED_NEXT_CYCLE_SEED_KEYS: tuple[str, ...] = (
    "completed_cycle_receipt",
    "completed_cycle_receipt_frontier",
    "completed_cycle_receipt_runtime",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_cycle_seed_frontier",
    "next_cycle_seed_schema_version",
    "next_stage",
    "seed_items",
    "seed_mode",
    "seed_scope",
    "source_receipt",
    "source_receipt_frontier",
    "source_receipt_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_next_cycle_seed() -> dict[str, Any]:
    return json.loads((_repo_root() / NEXT_CYCLE_SEED_PATH).read_text(encoding="utf-8"))


def expected_next_cycle_seed() -> dict[str, Any]:
    return {
        "completed_cycle_receipt": receipt.COMPLETION_RECEIPT_PATH,
        "completed_cycle_receipt_frontier": receipt.VERSION,
        "completed_cycle_receipt_runtime": "runtime/kuuos_self_organization_completion_receipt_v0_102.py",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_candidate_queue_v0_104.json",
        "next_cycle_seed_frontier": VERSION,
        "next_cycle_seed_schema_version": NEXT_CYCLE_SEED_SCHEMA_VERSION,
        "next_stage": "v0.104",
        "seed_items": [
            "completion_receipt_verified",
            "prior_cycle_closed",
            "next_candidate_queue_named",
            "current_root_sequence_connected",
        ],
        "seed_mode": "next_cycle_seed_only",
        "seed_scope": "self_organization_candidate_queue_seed",
        "source_receipt": receipt.COMPLETION_RECEIPT_PATH,
        "source_receipt_frontier": receipt.VERSION,
        "source_receipt_runtime": "runtime/kuuos_self_organization_completion_receipt_v0_102.py",
    }


def next_cycle_seed_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        seed = load_next_cycle_seed()
    except FileNotFoundError:
        return ("next_cycle_seed_missing",)
    except json.JSONDecodeError:
        return ("next_cycle_seed_invalid_json",)
    missing = set(REQUIRED_NEXT_CYCLE_SEED_KEYS).difference(seed)
    if missing:
        issues.append("missing_next_cycle_seed_keys:" + ",".join(sorted(missing)))
    extra = set(seed).difference(REQUIRED_NEXT_CYCLE_SEED_KEYS)
    if extra:
        issues.append("extra_next_cycle_seed_keys:" + ",".join(sorted(extra)))
    if seed != expected_next_cycle_seed():
        issues.append("next_cycle_seed_mismatch")
    if seed.get("seed_mode") != "next_cycle_seed_only":
        issues.append("seed_mode")
    if seed.get("seed_scope") != "self_organization_candidate_queue_seed":
        issues.append("seed_scope")
    if seed.get("next_artifact") != "status/self_organization_candidate_queue_v0_104.json":
        issues.append("next_artifact")
    if seed.get("next_stage") != "v0.104":
        issues.append("next_stage")
    source = receipt.load_completion_receipt()
    if source.get("next_artifact") != NEXT_CYCLE_SEED_PATH:
        issues.append("source_next_artifact")
    if source.get("next_stage") != "v0.103":
        issues.append("source_next_stage")
    if source.get("receipt_mode") != "completion_receipt_only":
        issues.append("source_receipt_mode")
    if source.get("completed_stage") != "v0.101":
        issues.append("source_completed_stage")
    if not receipt.verify_completion_receipt():
        issues.append("completion_receipt_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_next_cycle_seed() -> bool:
    return next_cycle_seed_issues() == ()


def next_cycle_seed_json() -> str:
    return json.dumps(load_next_cycle_seed(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = next_cycle_seed_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(next_cycle_seed_json())
