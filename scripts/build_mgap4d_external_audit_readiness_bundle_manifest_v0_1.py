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
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR10_MERGE_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR11_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr9_merge_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr10_merge_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr11_merge_closure_v0_1.py",
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
    return {"path": path_text, "sha256": sha256_bytes(data), "size_bytes": len(data)}


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
        "pr9_merge_closure_included": True,
        "pr10_merge_closure_included": True,
        "pr11_merge_closure_included": True,
        "bundle_root_hash": sha256_bytes(root_material),
        "artifact_count": len(artifact_entries),
        "artifacts": artifact_entries,
        "pr11_merge_closure_reference": {
            "pull_request": "#11",
            "pull_request_title": "Add MGAP4D PR10 merge closure v0.1",
            "pr_head_commit": "d633a7c60fff5da9cd86c7a85e51aae60bed3fa8",
            "base_before_merge": "fb082f7caa0b5d009cd0dbca34412047ffe6599e",
            "squash_merge_commit": "d76fc29c09a3c87b27878bb5ec3969512e288cfd",
            "merged_at": "2026-05-17T03:32:18Z",
            "closure_pass_line": "PASS: MGAP4D external audit readiness PR11 merge closure checked",
        },
        **BOUNDARY_FLAGS,
        "notes": [
            "Bundle manifest records hash evidence through PR11 merge closure.",
            "CI green does not grant proof/truth/clinical/execution/governance-bypass authority.",
            "PR merge success is integration evidence, not theorem truth.",
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
