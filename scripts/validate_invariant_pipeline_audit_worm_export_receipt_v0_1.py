#!/usr/bin/env python3
"""
validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py

Stdlib-only validator for the KuuOS Invariant Pipeline Audit WORM Export Receipt fixture.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md"
RECEIPT_PATH = ROOT / "specs" / "invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json"
LEDGER_PATH = ROOT / "specs" / "invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "clinical_authority_granted",
    "truth_authority_granted",
    "teni_authority_granted",
]

REQUIRED_DOC_STRINGS = [
    "WORM export preserves lineage. It does not create authority.",
    "source_ledger_root_hash",
    "export_mode is WORM",
    "non-authority fields remain false",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def compute_ledger_root_and_count() -> tuple[str, int]:
    previous_hash = "GENESIS"
    expected_sequence = 1
    final_hash = ""
    lines = [line for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    for line in lines:
        entry = json.loads(line)
        seq = entry.get("sequence")
        if seq != expected_sequence:
            raise ValueError(f"sequence expected {expected_sequence}, got {seq}")
        if entry.get("previous_hash") != previous_hash:
            raise ValueError(f"sequence {seq}: previous_hash mismatch")
        expected_event_hash = canonical_hash(entry["event"])
        if entry.get("event_hash") != expected_event_hash:
            raise ValueError(f"sequence {seq}: event_hash mismatch")
        expected_entry_hash = canonical_hash({
            "sequence": seq,
            "previous_hash": entry.get("previous_hash"),
            "event_hash": entry.get("event_hash"),
        })
        if entry.get("entry_hash") != expected_entry_hash:
            raise ValueError(f"sequence {seq}: entry_hash mismatch")
        previous_hash = entry["entry_hash"]
        final_hash = previous_hash
        expected_sequence += 1
    if not lines:
        raise ValueError("ledger has no entries")
    return final_hash, len(lines)


def validate_doc() -> list[str]:
    errors: list[str] = []
    if not DOC_PATH.is_file():
        return [f"missing WORM receipt doc: {DOC_PATH.relative_to(ROOT)}"]
    text = DOC_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_DOC_STRINGS:
        if item not in text:
            errors.append(f"doc missing required string: {item}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_doc())
    if not RECEIPT_PATH.is_file():
        errors.append(f"missing receipt fixture: {RECEIPT_PATH.relative_to(ROOT)}")
    if not LEDGER_PATH.is_file():
        errors.append(f"missing source ledger: {LEDGER_PATH.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    try:
        root_hash, entry_count = compute_ledger_root_and_count()
    except ValueError as exc:
        print(f"ERROR: ledger validation failed: {exc}")
        return 1

    if receipt.get("source_ledger") != "specs/invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl":
        errors.append("source_ledger mismatch")
    if receipt.get("source_ledger_root_hash") != root_hash:
        errors.append(f"source_ledger_root_hash mismatch: expected {root_hash}, got {receipt.get('source_ledger_root_hash')}")
    if receipt.get("exported_entry_count") != entry_count:
        errors.append(f"exported_entry_count mismatch: expected {entry_count}, got {receipt.get('exported_entry_count')}")
    if receipt.get("export_mode") != "WORM":
        errors.append("export_mode must be WORM")
    if receipt.get("object_lock_mode") not in {"compliance", "governance", "local_fixture"}:
        errors.append("object_lock_mode invalid")
    if "does not create" not in receipt.get("non_authority_note", ""):
        errors.append("non_authority_note must state non-authority")
    for field in FALSE_FIELDS:
        if receipt.get(field) is not False:
            errors.append(f"{field} must be false")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print(f"PASS: Invariant Pipeline audit WORM export receipt validated root={root_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
