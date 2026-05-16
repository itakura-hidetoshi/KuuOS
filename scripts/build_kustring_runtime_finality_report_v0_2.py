#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "specs" / "kustring_runtime_bundle_v0_2.generated.json"
ATTEST = ROOT / "specs" / "kustring_runtime_attestation_v0_2.generated.json"
WORM = ROOT / "specs" / "kustring_runtime_worm_receipt_v0_2.generated.json"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"
INDEX = ROOT / "docs" / "KUSTRING_RUNTIME_CHAIN_INDEX_v0_2.md"
FINALITY = ROOT / "docs" / "KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md"
LEDGER = ROOT / "docs" / "kustring_runtime_finality_ci_ledger_v0_2.md"
OUT = ROOT / "specs" / "kustring_runtime_finality_report_v0_2.generated.json"

PREPARE_COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/run_kustring_runtime_closure_suite_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_finality_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_finality_ci_v0_2.py"],
    [sys.executable, "scripts/check_kustring_runtime_chain_index_v0_2.py"],
]

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}

CI_GREEN = {
    "run_id": "25960729451",
    "job_id": "76315481134",
    "head_sha": "8eae6d696b6128cfecb71430b19123ca6ed43003",
    "artifact_id": "7033005445",
    "artifact_name": "kustring-runtime-finality-report-v0-2",
    "artifact_digest": "sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad",
}


def run_command(cmd: Sequence[str]) -> int:
    print("\n>>> " + " ".join(cmd), flush=True)
    return subprocess.run(list(cmd), cwd=ROOT).returncode


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
    for cmd in PREPARE_COMMANDS:
        code = run_command(cmd)
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
        "ci_green_reference": CI_GREEN,
        "chain_index_path": "docs/KUSTRING_RUNTIME_CHAIN_INDEX_v0_2.md",
        "finality_packet_path": "docs/KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md",
        "ci_ledger_path": "docs/kustring_runtime_finality_ci_ledger_v0_2.md",
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
            "chain_index": file_hash(INDEX),
            "finality_packet": file_hash(FINALITY),
            "ci_ledger": file_hash(LEDGER),
        },
        **FLAGS,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {report['bundle_root_hash']}")
    print(f"audit_chain_root_hash: {report['audit_chain_root_hash']}")
    print(f"chain_index_hash: {report['artifact_hashes']['chain_index']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())