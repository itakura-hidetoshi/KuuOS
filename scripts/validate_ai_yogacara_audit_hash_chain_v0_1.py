#!/usr/bin/env python3
"""
validate_ai_yogacara_audit_hash_chain_v0_1.py

Stdlib-only validator for AI Yogacara audit hash-chain fixtures.

Checks:
- JSONL entries parse
- event_hash equals SHA256(canonical JSON without event_hash)
- previous_hash links to previous event_hash
- raw_output_status is candidate
- all non-authority fields are explicitly false
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "specs" / "ai_yogacara_audit_hash_chain_fixture_v0_1.jsonl"

FALSE_FIELDS = [
    "authority_granted",
    "proof_authority_granted",
    "decision_authority_granted",
    "execution_authority_granted",
    "memory_truth_granted",
    "belief_authority_granted",
]


def canonical_hash(entry: dict[str, Any]) -> str:
    data = dict(entry)
    data.pop("event_hash", None)
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for lineno, line in enumerate(FIXTURE_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {lineno}: invalid JSON: {exc}") from exc
    return entries


def validate_entry(entry: dict[str, Any], index: int, previous_hash: str) -> list[str]:
    errors: list[str] = []
    event_id = entry.get("event_id", f"index-{index}")

    if entry.get("raw_output_status") != "candidate":
        errors.append(f"{event_id}: raw_output_status must be candidate")

    for field in FALSE_FIELDS:
        if entry.get(field) is not False:
            errors.append(f"{event_id}: {field} must be false")

    if entry.get("previous_hash") != previous_hash:
        errors.append(f"{event_id}: previous_hash mismatch; expected {previous_hash}, got {entry.get('previous_hash')}")

    expected_hash = canonical_hash(entry)
    if entry.get("event_hash") != expected_hash:
        errors.append(f"{event_id}: event_hash mismatch; expected {expected_hash}, got {entry.get('event_hash')}")

    if "RuntimeGovernance" not in entry.get("governance_route", []):
        errors.append(f"{event_id}: governance_route must include RuntimeGovernance")

    return errors


def main() -> int:
    if not FIXTURE_PATH.is_file():
        print(f"ERROR: missing fixture file: {FIXTURE_PATH.relative_to(ROOT)}")
        return 1

    try:
        entries = load_entries()
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not entries:
        print("ERROR: hash-chain fixture has no entries")
        return 1

    errors: list[str] = []
    previous_hash = "GENESIS"
    for index, entry in enumerate(entries):
        errors.extend(validate_entry(entry, index, previous_hash))
        previous_hash = entry.get("event_hash", "")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: AI Yogacara audit hash-chain fixture validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
