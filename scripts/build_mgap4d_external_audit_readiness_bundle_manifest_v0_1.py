#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "specs" / "mgap4d_external_audit_readiness_bundle_manifest_v0_1.generated.json"

ARTIFACTS = [
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
]

BOUNDARY_FLAGS = {
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "clinical_authority_granted": False,
    "execution_authority_granted": False,
    "governance_bypass_authority_granted": False,
    "external_auditor_acceptance_granted": False,
    "journal_acceptance_granted": False,
    "community_acceptance_granted": False,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_entry(path_text: str) -> dict:
    path = ROOT / path_text
    data = path.read_bytes()
    return {
        "path": path_text,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def main() -> int:
    missing = [p for p in ARTIFACTS if not (ROOT / p).is_file()]
    if missing:
        for path in missing:
            print(f"ERROR: missing artifact: {path}")
        return 1

    artifact_entries = [file_entry(p) for p in ARTIFACTS]
    root_material = json.dumps(artifact_entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest = {
        "schema": "mgap4d_external_audit_readiness_bundle_manifest_v0_1",
        "status": "CANDIDATE",
        "implementation_not_proof": True,
        "finality_packet_included": True,
        "bundle_root_hash": sha256_bytes(root_material),
        "artifact_count": len(artifact_entries),
        "artifacts": artifact_entries,
        "ci_green_reference": {
            "workflow_run_id": "25973305278",
            "workflow_job_id": "76349030859",
            "checked_commit": "a9f53bad85037169a04aabf13f0296a96bff4530",
            "ledger_pass_line": "PASS: MGAP4D external audit readiness CI ledger checked",
            "chain_index_pass_line": "PASS: MGAP4D external audit readiness chain index checked",
        },
        "all_governance_green_reference": {
            "workflow_run_id": "25974130236",
            "workflow_job_id": "76351200926",
            "checked_commit": "9147dc5a00e3ffd74b85336e8a26e33091fec9f1",
            "job_name": "Validate all governance checks",
            "bundle_manifest_pass_line": "PASS: MGAP4D external audit readiness bundle manifest checked",
            "all_governance_pass_line": "PASS: KuuOS all governance full checks completed",
        },
        **BOUNDARY_FLAGS,
        "notes": [
            "Bundle manifest records hash evidence for ledger, chain index, finality packet, checkers, and dedicated workflow.",
            "CI green does not grant proof/truth/clinical/execution/governance-bypass authority.",
            "External audit readiness is not external audit acceptance.",
            "Further tightening is same-root and append-only.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
