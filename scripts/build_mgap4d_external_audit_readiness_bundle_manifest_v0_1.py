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
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
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
        "post_merge_green_receipt_included": True,
        "post_merge_receipt_closure_included": True,
        "pr8_merge_closure_included": True,
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
        "post_merge_green_reference": {
            "workflow_run_id": "25974409859",
            "workflow_job_id": "76351949971",
            "checked_commit": "e20d244d93eb85b3cfc9b46cf4bb4625923a8d82",
            "branch": "main",
            "job_name": "Validate all governance checks",
            "post_merge_bundle_root_hash": "94c379c61e1a405b54dee326a5faad545e0e2c711afbd16f56b9d66e26ea0dff",
            "post_merge_receipt_pass_line": "PASS: MGAP4D external audit readiness post-merge green receipt checked",
            "bundle_manifest_pass_line": "PASS: MGAP4D external audit readiness bundle manifest checked",
            "all_governance_pass_line": "PASS: KuuOS all governance full checks completed",
        },
        "post_merge_receipt_closure_reference": {
            "pull_request": "#7",
            "pull_request_title": "Add MGAP4D post-merge green receipt v0.1",
            "pr_head_commit": "dec5e66ee46c2649cddb6273b55136cf844d4bbc",
            "base_before_merge": "e20d244d93eb85b3cfc9b46cf4bb4625923a8d82",
            "squash_merge_commit": "7f53a0adff847b59f7356875e1102fb7e3faf9fe",
            "merged_at": "2026-05-17T00:35:13Z",
            "closure_pass_line": "PASS: MGAP4D external audit readiness post-merge receipt closure checked",
        },
        "pr8_merge_closure_reference": {
            "pull_request": "#8",
            "pull_request_title": "Add MGAP4D post-merge receipt closure v0.1",
            "pr_head_commit": "98792d7e7ebd426f16c4b74eb868162d3cce09a2",
            "base_before_merge": "7f53a0adff847b59f7356875e1102fb7e3faf9fe",
            "squash_merge_commit": "d29468a831baff2c1cda847124f43a05d5574fb1",
            "merged_at": "2026-05-17T02:02:06Z",
            "closure_pass_line": "PASS: MGAP4D external audit readiness PR8 merge closure checked",
        },
        **BOUNDARY_FLAGS,
        "notes": [
            "Bundle manifest records hash evidence for ledger, chain index, finality packet, post-merge receipt, post-merge receipt closure, PR8 merge closure, checkers, and dedicated workflow.",
            "CI green does not grant proof/truth/clinical/execution/governance-bypass authority.",
            "PR merge success is integration evidence, not theorem truth.",
            "External audit readiness is not external audit acceptance.",
            "Post-merge green confirms repository integration, not independent mathematical acceptance.",
            "Post-merge receipt closure records integration of the receipt, not independent acceptance.",
            "PR8 merge closure records integration of the closure layer, not independent acceptance.",
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
