#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime import kuuos_current_root_sequence_v0_85 as current_root
from runtime import kuuos_self_organization_review_packet_v0_85 as packet

VERSION = "kuuos_self_organization_review_decision_v0_86"
DEPENDS_ON = packet.VERSION
CURRENT_ROOT_SEQUENCE = current_root.VERSION
REVIEW_DECISION_PATH = "status/self_organization_review_decision_v0_86.json"
DECISION_SCHEMA_VERSION = "v0.86"

REQUIRED_DECISION_KEYS: tuple[str, ...] = (
    "authority_boundary",
    "current_root_check",
    "current_root_sequence",
    "decision_frontier",
    "decision_mode",
    "decision_schema_version",
    "decision_status",
    "next_request_artifact",
    "next_request_stage",
    "packet_checks",
    "source_packet",
    "source_packet_frontier",
    "source_packet_runtime",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_review_decision() -> dict[str, Any]:
    return json.loads((_repo_root() / REVIEW_DECISION_PATH).read_text(encoding="utf-8"))


def expected_review_decision() -> dict[str, Any]:
    return {
        "authority_boundary": "review_decision_not_grant",
        "current_root_check": "runtime/kuuos_current_check.py",
        "current_root_sequence": CURRENT_ROOT_SEQUENCE,
        "decision_frontier": VERSION,
        "decision_mode": "decision_record_only",
        "decision_schema_version": DECISION_SCHEMA_VERSION,
        "decision_status": "review_packet_accepted_for_next_request",
        "next_request_artifact": "status/self_organization_bounded_request_v0_87.json",
        "next_request_stage": "v0.87",
        "packet_checks": [
            "packet_is_review_only",
            "packet_sources_are_recorded",
            "packet_requested_v0_86",
            "no_grant_boundary_is_preserved",
        ],
        "source_packet": packet.REVIEW_PACKET_PATH,
        "source_packet_frontier": packet.VERSION,
        "source_packet_runtime": "runtime/kuuos_self_organization_review_packet_v0_85.py",
    }


def review_decision_issues() -> tuple[str, ...]:
    issues: list[str] = []
    try:
        decision = load_review_decision()
    except FileNotFoundError:
        return ("review_decision_missing",)
    except json.JSONDecodeError:
        return ("review_decision_invalid_json",)
    missing = set(REQUIRED_DECISION_KEYS).difference(decision)
    if missing:
        issues.append("missing_review_decision_keys:" + ",".join(sorted(missing)))
    extra = set(decision).difference(REQUIRED_DECISION_KEYS)
    if extra:
        issues.append("extra_review_decision_keys:" + ",".join(sorted(extra)))
    if decision != expected_review_decision():
        issues.append("review_decision_mismatch")
    if decision.get("authority_boundary") != "review_decision_not_grant":
        issues.append("authority_boundary")
    if decision.get("decision_mode") != "decision_record_only":
        issues.append("decision_mode")
    if decision.get("decision_status") != "review_packet_accepted_for_next_request":
        issues.append("decision_status")
    source = packet.load_review_packet()
    if source.get("requested_next_stage") != "v0.86":
        issues.append("source_packet_requested_stage")
    if source.get("requested_next_stage_artifact") != REVIEW_DECISION_PATH:
        issues.append("source_packet_requested_artifact")
    if source.get("packet_mode") != "review_only":
        issues.append("source_packet_mode")
    if not packet.verify_review_packet():
        issues.append("review_packet_not_verified")
    if not current_root.verify_current_root_sequence():
        issues.append("current_root_sequence_not_verified")
    return tuple(issues)


def verify_review_decision() -> bool:
    return review_decision_issues() == ()


def review_decision_json() -> str:
    return json.dumps(load_review_decision(), ensure_ascii=False, sort_keys=True, indent=2)


if __name__ == "__main__":
    issues = review_decision_issues()
    if issues:
        print("\n".join(issues))
        raise SystemExit(1)
    print(review_decision_json())
