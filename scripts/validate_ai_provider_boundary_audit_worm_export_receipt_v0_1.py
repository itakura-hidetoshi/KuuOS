#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AI_PROVIDER_BOUNDARY_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md"
LEDGER = ROOT / "specs" / "ai_provider_boundary_audit_hash_chain_fixture_v0_1.jsonl"
RECEIPT = ROOT / "specs" / "ai_provider_boundary_audit_worm_export_receipt_fixture_v0_1.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "memory_truth_granted",
    "decision_authority_granted",
    "teni_authority_granted",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def ledger_root_and_count() -> tuple[str, int]:
    prev = "GENESIS"
    final = ""
    count = 0
    for raw in [x for x in LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]:
        entry = json.loads(raw)
        event_hash = canonical_hash(entry["event"])
        if entry.get("event_hash") != event_hash:
            raise ValueError("event_hash mismatch")
        payload = {"sequence": entry["sequence"], "previous_hash": entry["previous_hash"], "event_hash": entry["event_hash"]}
        entry_hash = canonical_hash(payload)
        if entry.get("entry_hash") != entry_hash:
            raise ValueError("entry_hash mismatch")
        if entry.get("previous_hash") != prev:
            raise ValueError("previous_hash mismatch")
        prev = entry_hash
        final = entry_hash
        count += 1
    if not final:
        raise ValueError("empty ledger")
    return final, count


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing WORM receipt doc")
    if not LEDGER.is_file():
        errors.append("missing source ledger")
    if not RECEIPT.is_file():
        errors.append("missing WORM receipt fixture")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    try:
        root, count = ledger_root_and_count()
    except ValueError as exc:
        print("ERROR:", exc)
        return 1

    if receipt.get("source_ledger_root_hash") != root:
        errors.append("source_ledger_root_hash mismatch")
    if receipt.get("exported_entry_count") != count:
        errors.append("exported_entry_count mismatch")
    if receipt.get("export_mode") != "WORM":
        errors.append("export_mode must be WORM")
    for field in FALSE_FIELDS:
        if receipt.get(field) is not False:
            errors.append(f"{field} must be false")
    if "does not create" not in receipt.get("non_authority_note", ""):
        errors.append("non_authority_note must state non-authority")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: AI Provider Boundary audit WORM receipt validated root={root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
