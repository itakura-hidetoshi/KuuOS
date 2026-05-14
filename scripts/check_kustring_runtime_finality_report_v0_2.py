#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_kustring_runtime_finality_report_v0_2.py"
REPORT = ROOT / "specs" / "kustring_runtime_finality_report_v0_2.generated.json"
BUNDLE = ROOT / "specs" / "kustring_runtime_bundle_v0_2.generated.json"
ATTEST = ROOT / "specs" / "kustring_runtime_attestation_v0_2.generated.json"
WORM = ROOT / "specs" / "kustring_runtime_worm_receipt_v0_2.generated.json"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chain_root_and_count() -> tuple[str, int]:
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty runtime audit chain")
    return json.loads(lines[-1])["entry_hash"], len(lines)


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    report = read_json(REPORT)
    bundle = read_json(BUNDLE)
    attest = read_json(ATTEST)
    worm = read_json(WORM)
    root, count = chain_root_and_count()

    if report.get("suite_result") != "PASS":
        errors.append("suite_result must be PASS")
    if report.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if report.get("bundle_root_hash") != bundle.get("bundle_root_hash"):
        errors.append("bundle root mismatch")
    if report.get("audit_chain_root_hash") != root:
        errors.append("audit chain root mismatch")
    if report.get("audit_chain_entry_count") != count:
        errors.append("audit chain count mismatch")
    if report.get("worm_receipt_source_chain_root_hash") != worm.get("source_chain_root_hash"):
        errors.append("worm root mismatch")
    if report.get("attestation_bundle_root_hash") != attest.get("bundle_root_hash"):
        errors.append("attestation bundle root mismatch")
    if report.get("attestation_audit_chain_root_hash") != attest.get("audit_chain_root_hash"):
        errors.append("attestation audit root mismatch")
    if report.get("attestation_worm_root_hash") != attest.get("worm_receipt_source_chain_root_hash"):
        errors.append("attestation worm root mismatch")
    for flag in FLAGS:
        if report.get(flag) is not False:
            errors.append(f"{flag} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: KuString runtime finality report checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
