#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_emptiness_middle_way_core_attestation_v0_1.py"
ATTESTATION = ROOT / "specs" / "emptiness_middle_way_core_attestation_v0_1.generated.json"
BUNDLE = ROOT / "specs" / "emptiness_middle_way_core_bundle_v0_1.generated.json"
LEDGER = ROOT / "specs" / "emptiness_middle_way_core_audit_hash_chain_fixture_v0_1.jsonl"
WORM = ROOT / "specs" / "emptiness_middle_way_core_audit_worm_export_receipt_fixture_v0_1.json"
DOC = ROOT / "docs" / "EMPTINESS_MIDDLE_WAY_CORE_ATTESTATION_v0_1.md"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_root() -> str:
    lines = [x for x in LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]
    return json.loads(lines[-1])["entry_hash"]


def main() -> int:
    errors: list[str] = []
    for path in [DOC, BUILDER, LEDGER, WORM]:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    result = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    att = read_json(ATTESTATION)
    bundle = read_json(BUNDLE)
    worm = read_json(WORM)
    root = ledger_root()

    if att.get("authority_note") != "integrity_summary_only":
        errors.append("authority_note mismatch")
    if att.get("bundle_root_hash") != bundle.get("bundle_root_hash"):
        errors.append("bundle_root_hash mismatch")
    if att.get("audit_hash_chain_root_hash") != root:
        errors.append("audit_hash_chain_root_hash mismatch")
    if att.get("worm_receipt_source_ledger_root_hash") != worm.get("source_ledger_root_hash"):
        errors.append("worm root mismatch")
    if att.get("worm_receipt_source_ledger_root_hash") != att.get("audit_hash_chain_root_hash"):
        errors.append("worm root must equal audit root")
    for field in FALSE_FIELDS:
        if att.get(field) is not False:
            errors.append(f"{field} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: emptiness middle way core attestation validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
