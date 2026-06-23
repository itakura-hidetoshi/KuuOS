#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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
INDEX = ROOT / "docs" / "KUSTRING_RUNTIME_CHAIN_INDEX_v0_2.md"
FINALITY = ROOT / "docs" / "KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md"
LEDGER = ROOT / "docs" / "kustring_runtime_finality_ci_ledger_v0_2.md"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]
CI_GREEN = {
    "run_id": "25960729451",
    "job_id": "76315481134",
    "head_sha": "8eae6d696b6128cfecb71430b19123ca6ed43003",
    "artifact_id": "7033005445",
    "artifact_name": "kustring-runtime-finality-report-v0-2",
    "artifact_digest": "sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad",
}


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    if report.get("suite") != "scripts/check_kustring_runtime_finality_report_v0_2.py":
        errors.append("canonical validation entry point mismatch")
    if report.get("suite_result") != "PASS":
        errors.append("suite_result must be PASS")
    if report.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if report.get("ci_green_reference") != CI_GREEN:
        errors.append("ci green reference mismatch")
    if report.get("chain_index_path") != "docs/KUSTRING_RUNTIME_CHAIN_INDEX_v0_2.md":
        errors.append("chain index path mismatch")
    if report.get("finality_packet_path") != "docs/KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md":
        errors.append("finality packet path mismatch")
    if report.get("ci_ledger_path") != "docs/kustring_runtime_finality_ci_ledger_v0_2.md":
        errors.append("ci ledger path mismatch")
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

    artifact_hashes = report.get("artifact_hashes", {})
    expected_hashes = {
        "bundle": file_hash(BUNDLE),
        "attestation": file_hash(ATTEST),
        "worm_receipt": file_hash(WORM),
        "audit_chain": file_hash(CHAIN),
        "chain_index": file_hash(INDEX),
        "finality_packet": file_hash(FINALITY),
        "ci_ledger": file_hash(LEDGER),
    }
    for key, expected in expected_hashes.items():
        if artifact_hashes.get(key) != expected:
            errors.append(f"artifact hash mismatch: {key}")

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
