#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_96 as current_root
from runtime import kuuos_self_organization_next_cycle_seed_v0_96 as seed

VERSION = "kuuos_self_organization_candidate_queue_v0_97"
DEPENDS_ON = seed.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
CANDIDATE_QUEUE_PATH = "status/self_organization_candidate_queue_v0_97.json"
CANDIDATE_QUEUE_SCHEMA_VERSION = "v0.97"

REQUIRED_CANDIDATE_QUEUE_KEYS: tuple[str, ...] = (
    "candidate_count",
    "candidate_ids",
    "candidate_queue_frontier",
    "candidate_queue_schema_version",
    "current_root_check",
    "current_root_sequence",
    "next_artifact",
    "next_stage",
    "queue_mode",
    "queue_scope",
    "seed",
    "seed_frontier",
    "seed_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_candidate_queue() -> dict[str, Any]:
    return json.loads((_repo_root() / CANDIDATE_QUEUE_PATH).read_text(encoding="utf-8"))


def expected_candidate_ids() -> list[str]:
    return [
        "candidate-receipt-v0-98",
        "selection-policy-v0-99",
        "selected-next-action-v0-100",
        "bounded-change-plan-v0-101",
    ]


def expected_candidate_queue() -> dict[str, Any]:
    return {
        "candidate_count": len(expected_candidate_ids()),
        "candidate_ids": expected_candidate_ids(),
        "candidate_queue_frontier": VERSION,
        "candidate_queue_schema_version": CANDIDATE_QUEUE_SCHEMA_VERSION,
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "next_artifact": "status/self_organization_candidate_receipt_v0_98.json",
        "next_stage": "v0.98",
        "queue_mode": "candidate_queue_only",
        "queue_scope": "self_organization_next_cycle",
        "seed": seed.NEXT_CYCLE_SEED_PATH,
        "seed_frontier": seed.VERSION,
        "seed_runtime": "runtime/kuuos_self_organization_next_cycle_seed_v0_96.py",
    }


def candidate_queue_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        queue = load_candidate_queue()
    except FileNotFoundError:
        return ("candidate_queue_missing",)
    except json.JSONDecodeError:
        return ("candidate_queue_invalid_json",)
    missing = set(REQUIRED_CANDIDATE_QUEUE_KEYS).difference(queue)
    if missing:
        issues.append("missing_candidate_queue_keys:" + ",".join(sorted(missing)))
    extra = set(queue).difference(REQUIRED_CANDIDATE_QUEUE_KEYS)
    if extra:
        issues.append("extra_candidate_queue_keys:" + ",".join(sorted(extra)))
    if queue != expected_candidate_queue():
        issues.append("candidate_queue_mismatch")
    if queue.get("candidate_count") != len(queue.get("candidate_ids", [])):
        issues.append("candidate_count")
    if queue.get("candidate_ids") != expected_candidate_ids():
        issues.append("candidate_ids")
    if queue.get("queue_mode") != "candidate_queue_only":
        issues.append("queue_mode")
    if queue.get("queue_scope") != "self_organization_next_cycle":
        issues.append("queue_scope")
    if queue.get("next_artifact") != "status/self_organization_candidate_receipt_v0_98.json":
        issues.append("next_artifact")
    if queue.get("next_stage") != "v0.98":
        issues.append("next_stage")
    source = seed.load_next_cycle_seed()
    if source.get("next_artifact") != CANDIDATE_QUEUE_PATH:
        issues.append("seed_next_artifact")
    if source.get("next_stage") != "v0.97":
        issues.append("seed_next_stage")
    if source.get("seed_mode") != "next_cycle_seed_only":
        issues.append("seed_mode")
    if not seed.verify_next_cycle_seed():
        issues.append("next_cycle_seed_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_candidate_queue() -> bool:
    return candidate_queue_issues() == ()


def candidate_queue_json() -> str:
    return json.dumps(load_candidate_queue(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = candidate_queue_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(candidate_queue_json())
