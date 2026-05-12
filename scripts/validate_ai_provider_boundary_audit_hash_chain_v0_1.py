#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AI_PROVIDER_BOUNDARY_AUDIT_HASH_CHAIN_LEDGER_v0_1.md"
FIXTURE = ROOT / "specs" / "ai_provider_boundary_audit_hash_chain_fixture_v0_1.jsonl"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "memory_truth_granted",
    "decision_authority_granted",
    "teni_authority_granted",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing provider boundary hash-chain doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["record surface only", "event_hash = sha256", "GENESIS"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    if not FIXTURE.is_file():
        errors.append("missing provider boundary hash-chain fixture")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    prev = "GENESIS"
    expected_seq = 1
    final_hash = ""
    for line in [x for x in FIXTURE.read_text(encoding="utf-8").splitlines() if x.strip()]:
        entry = json.loads(line)
        seq = entry.get("sequence")
        if seq != expected_seq:
            errors.append(f"sequence expected {expected_seq}, got {seq}")
        if entry.get("previous_hash") != prev:
            errors.append(f"sequence {seq}: previous_hash mismatch")
        event = entry.get("event", {})
        if entry.get("event_hash") != canonical_hash(event):
            errors.append(f"sequence {seq}: event_hash mismatch")
        payload = {"sequence": seq, "previous_hash": entry.get("previous_hash"), "event_hash": entry.get("event_hash")}
        if entry.get("entry_hash") != canonical_hash(payload):
            errors.append(f"sequence {seq}: entry_hash mismatch")
        for field in FALSE_FIELDS:
            if event.get(field) is not False:
                errors.append(f"sequence {seq}: {field} must be false")
        prev = entry.get("entry_hash")
        final_hash = prev
        expected_seq += 1

    if not final_hash:
        errors.append("fixture must have at least one entry")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: AI Provider Boundary audit hash-chain validated root={final_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
