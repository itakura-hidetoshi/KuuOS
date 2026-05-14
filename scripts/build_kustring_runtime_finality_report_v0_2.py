#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
FINALITY_SUITE = ROOT / "scripts" / "run_kustring_runtime_finality_suite_v0_2.py"
BUNDLE = ROOT / "specs" / "kustring_runtime_bundle_v0_2.generated.json"
ATTEST = ROOT / "specs" / "kustring_runtime_attestation_v0_2.generated.json"
WORM = ROOT / "specs" / "kustring_runtime_worm_receipt_v0_2.generated.json"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"
OUT = ROOT / "specs" / "kustring_runtime_finality_report_v0_2.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chain_root_and_count() -> tuple[str, int]:
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty runtime audit chain")
    return json.loads(lines[-1])["entry_hash"], len(lines)


def main() -> int:
    code = subprocess.run([sys.executable, str(FINALITY_SUITE)], cwd=ROOT).returncode
    if code != 0:
        return code

    bundle = read_json(BUNDLE)
    attest = read_json(ATTEST)
    worm = read_json(WORM)
    chain_root, chain_count = chain_root_and_count()

    report = {
        "id": "kustring_runtime_finality_report_v0_2",
        "version": "0.2",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "suite": "scripts/run_kustring_runtime_finality_suite_v0_2.py",
        "suite_result": "PASS",
        "implementation_not_proof": True,
        "authority_note": "generated_report_is_integrity_summary_only",
        "bundle_root_hash": bundle["bundle_root_hash"],
        "audit_chain_root_hash": chain_root,
        "audit_chain_entry_count": chain_count,
        "worm_receipt_source_chain_root_hash": worm["source_chain_root_hash"],
        "attestation_bundle_root_hash": attest["bundle_root_hash"],
        "attestation_audit_chain_root_hash": attest["audit_chain_root_hash"],
        "attestation_worm_root_hash": attest["worm_receipt_source_chain_root_hash"],
        "artifact_hashes": {
            "bundle": file_hash(BUNDLE),
            "attestation": file_hash(ATTEST),
            "worm_receipt": file_hash(WORM),
            "audit_chain": file_hash(CHAIN),
        },
        **FLAGS,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {report['bundle_root_hash']}")
    print(f"audit_chain_root_hash: {report['audit_chain_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
