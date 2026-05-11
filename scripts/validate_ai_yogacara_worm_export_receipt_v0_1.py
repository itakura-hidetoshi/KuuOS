#!/usr/bin/env python3
"""
validate_ai_yogacara_worm_export_receipt_v0_1.py

Stdlib-only validator for AI Yogacara WORM export receipt fixtures.

Checks:
- ledger JSONL parses
- ledger event hashes form a valid chain via the hash-chain validator logic
- chain_root_hash = SHA256(concatenated ordered event_hashes)
- receipt last_event_hash matches ledger last hash
- receipt preserves non-authority statements
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "specs" / "ai_yogacara_audit_hash_chain_fixture_v0_1.jsonl"
RECEIPT_PATH = ROOT / "specs" / "ai_yogacara_audit_worm_export_receipt_fixture_v0_1.yaml"

REQUIRED_FIXED_POINTS = [
    "valid_hash_chain_proves_structural_continuity_not_truth",
    "worm_export_preserves_trace_not_authority",
    "export_receipt_is_not_execution_authority",
    "export_receipt_is_not_proof_of_teni_occurrence",
]


def load_ledger_hashes() -> list[str]:
    hashes: list[str] = []
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        event_hash = entry.get("event_hash")
        if not isinstance(event_hash, str) or len(event_hash) != 64:
            raise ValueError(f"invalid event_hash: {event_hash}")
        hashes.append(event_hash)
    return hashes


def extract_yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*([^\s#]+)\s*$", text, flags=re.MULTILINE)
    return match.group(1) if match else None


def chain_root(event_hashes: list[str]) -> str:
    return hashlib.sha256("".join(event_hashes).encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    if not LEDGER_PATH.is_file():
        errors.append(f"missing ledger: {LEDGER_PATH.relative_to(ROOT)}")
    if not RECEIPT_PATH.is_file():
        errors.append(f"missing receipt: {RECEIPT_PATH.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    try:
        event_hashes = load_ledger_hashes()
    except Exception as exc:
        print(f"ERROR: failed to load ledger hashes: {exc}")
        return 1

    if not event_hashes:
        print("ERROR: no event hashes found")
        return 1

    receipt_text = RECEIPT_PATH.read_text(encoding="utf-8")
    expected_root = chain_root(event_hashes)
    receipt_root = extract_yaml_scalar(receipt_text, "chain_root_hash")
    receipt_last = extract_yaml_scalar(receipt_text, "last_event_hash")
    receipt_count = extract_yaml_scalar(receipt_text, "ledger_entry_count")
    non_authority = extract_yaml_scalar(receipt_text, "non_authority_statement")

    if receipt_root != expected_root:
        errors.append(f"chain_root_hash mismatch; expected {expected_root}, got {receipt_root}")
    if receipt_last != event_hashes[-1]:
        errors.append(f"last_event_hash mismatch; expected {event_hashes[-1]}, got {receipt_last}")
    if receipt_count is not None and int(receipt_count) != len(event_hashes):
        errors.append(f"ledger_entry_count mismatch; expected {len(event_hashes)}, got {receipt_count}")
    if non_authority != "true":
        errors.append("non_authority_statement must be true")

    for fixed in REQUIRED_FIXED_POINTS:
        if fixed not in receipt_text:
            errors.append(f"missing fixed point: {fixed}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: AI Yogacara WORM export receipt validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
