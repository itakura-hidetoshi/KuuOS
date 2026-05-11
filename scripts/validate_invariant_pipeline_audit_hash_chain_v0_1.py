#!/usr/bin/env python3
"""
validate_invariant_pipeline_audit_hash_chain_v0_1.py

Stdlib-only validator for the KuuOS Invariant Pipeline Audit Hash-Chain Ledger fixture.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_AUDIT_HASH_CHAIN_LEDGER_v0_1.md"
FIXTURE_PATH = ROOT / "specs" / "invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "clinical_authority_granted",
    "truth_authority_granted",
    "teni_authority_granted",
]

REQUIRED_EVENT_FIELDS = [
    "event_id",
    "timestamp",
    "pipeline_version",
    "transformation_axis",
    "required_invariants",
    "required_invariant_names",
    "violated_invariants",
    "matrix_status",
    "gate_status",
    "gate_closed",
    "required_repair_route",
    "reason",
    "notes",
]

REQUIRED_DOC_STRINGS = [
    "Audit events become lineage records, not authority.",
    "event_hash = sha256(canonical_json(event))",
    "entry_hash = sha256(canonical_json({sequence, previous_hash, event_hash}))",
    "entry[n].previous_hash == entry[n-1].entry_hash",
]


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def validate_doc() -> list[str]:
    errors: list[str] = []
    if not DOC_PATH.is_file():
        return [f"missing ledger doc: {DOC_PATH.relative_to(ROOT)}"]
    text = DOC_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_DOC_STRINGS:
        if item not in text:
            errors.append(f"doc missing required string: {item}")
    return errors


def validate_event(event: dict[str, Any], sequence: int) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_EVENT_FIELDS:
        if field not in event:
            errors.append(f"sequence {sequence}: event missing field: {field}")
    for field in FALSE_FIELDS:
        if event.get(field) is not False:
            errors.append(f"sequence {sequence}: {field} must be false")
    if event.get("matrix_status") not in {"PASS", "REJECT"}:
        errors.append(f"sequence {sequence}: invalid matrix_status")
    if event.get("gate_status") not in {"PASS", "HOLD", "REPAIR", "REJECT", "QUARANTINE"}:
        errors.append(f"sequence {sequence}: invalid gate_status")
    if "not authority" not in event.get("notes", ""):
        errors.append(f"sequence {sequence}: notes must state non-authority")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_doc())
    if not FIXTURE_PATH.is_file():
        errors.append(f"missing fixture: {FIXTURE_PATH.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    previous_hash = "GENESIS"
    expected_sequence = 1
    final_hash = None

    lines = [line for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        errors.append("fixture must contain at least one JSONL entry")

    for line in lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSONL: {exc}")
            continue

        seq = entry.get("sequence")
        if seq != expected_sequence:
            errors.append(f"sequence expected {expected_sequence}, got {seq}")
        if entry.get("previous_hash") != previous_hash:
            errors.append(f"sequence {seq}: previous_hash mismatch")

        event = entry.get("event")
        if not isinstance(event, dict):
            errors.append(f"sequence {seq}: event must be object")
            continue
        errors.extend(validate_event(event, seq))

        expected_event_hash = canonical_hash(event)
        if entry.get("event_hash") != expected_event_hash:
            errors.append(f"sequence {seq}: event_hash mismatch")

        entry_payload = {
            "sequence": seq,
            "previous_hash": entry.get("previous_hash"),
            "event_hash": entry.get("event_hash"),
        }
        expected_entry_hash = canonical_hash(entry_payload)
        if entry.get("entry_hash") != expected_entry_hash:
            errors.append(f"sequence {seq}: entry_hash mismatch")

        previous_hash = entry.get("entry_hash")
        final_hash = previous_hash
        expected_sequence += 1

    if final_hash is None:
        errors.append("missing final hash")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print(f"PASS: Invariant Pipeline audit hash-chain validated root={final_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
