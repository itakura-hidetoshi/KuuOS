#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_emptiness_runtime_attestation_v0_1.py"
ATTEST = ROOT / "specs" / "emptiness_runtime_attestation_v0_1.generated.json"
BUNDLE = ROOT / "specs" / "emptiness_runtime_bundle_v0_1.generated.json"
CHAIN = ROOT / "specs" / "emptiness_runtime_audit_chain_v0_1.generated.jsonl"
WORM = ROOT / "specs" / "emptiness_runtime_worm_receipt_v0_1.generated.json"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chain_root() -> str:
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty emptiness runtime audit chain")
    return json.loads(lines[-1])["entry_hash"]


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    att = read_json(ATTEST)
    bundle = read_json(BUNDLE)
    worm = read_json(WORM)
    root = chain_root()
    if att.get("authority_note") != "emptiness_runtime_attestation_is_integrity_summary_only":
        errors.append("authority_note mismatch")
    if att.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if att.get("bundle_root_hash") != bundle.get("bundle_root_hash"):
        errors.append("bundle root mismatch")
    if att.get("audit_chain_root_hash") != root:
        errors.append("audit chain root mismatch")
    if att.get("worm_receipt_source_chain_root_hash") != worm.get("source_chain_root_hash"):
        errors.append("worm root mismatch")
    if att.get("audit_chain_root_hash") != att.get("worm_receipt_source_chain_root_hash"):
        errors.append("audit and worm roots must match")
    for flag in FLAGS:
        if att.get(flag) is not False:
            errors.append(f"{flag} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Emptiness runtime attestation checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
