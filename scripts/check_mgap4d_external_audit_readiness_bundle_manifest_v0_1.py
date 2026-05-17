#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_mgap4d_external_audit_readiness_bundle_manifest_v0_1.py"
MANIFEST = ROOT / "specs" / "mgap4d_external_audit_readiness_bundle_manifest_v0_1.generated.json"
ARTIFACTS = [
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CI_LEDGER_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_CHAIN_INDEX_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_FINALITY_PACKET_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_GREEN_RECEIPT_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_POST_MERGE_RECEIPT_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR8_MERGE_CLOSURE_v0_1.md",
    "docs/MGAP4D_EXTERNAL_AUDIT_READINESS_PR9_MERGE_CLOSURE_v0_1.md",
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_finality_packet_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_green_receipt_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_post_merge_receipt_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr8_merge_closure_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_pr9_merge_closure_v0_1.py",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
]
FALSE_FLAGS = [
    "proof_authority_granted",
    "truth_authority_granted",
    "clinical_authority_granted",
    "execution_authority_granted",
    "governance_bypass_authority_granted",
    "external_auditor_acceptance_granted",
    "journal_acceptance_granted",
    "community_acceptance_granted",
]
CI_GREEN = {
    "workflow_run_id": "25973305278",
    "workflow_job_id": "76349030859",
    "checked_commit": "a9f53bad85037169a04aabf13f0296a96bff4530",
    "ledger_pass_line": "PASS: MGAP4D external audit readiness CI ledger checked",
    "chain_index_pass_line": "PASS: MGAP4D external audit readiness chain index checked",
}
ALL_GOVERNANCE_GREEN = {
    "workflow_run_id": "25974130236",
    "workflow_job_id": "76351200926",
    "checked_commit": "9147dc5a00e3ffd74b85336e8a26e33091fec9f1",
    "job_name": "Validate all governance checks",
    "bundle_manifest_pass_line": "PASS: MGAP4D external audit readiness bundle manifest checked",
    "all_governance_pass_line": "PASS: KuuOS all governance full checks completed",
}
POST_MERGE_GREEN = {
    "workflow_run_id": "25974409859",
    "workflow_job_id": "76351949971",
    "checked_commit": "e20d244d93eb85b3cfc9b46cf4bb4625923a8d82",
    "branch": "main",
    "job_name": "Validate all governance checks",
    "post_merge_bundle_root_hash": "94c379c61e1a405b54dee326a5faad545e0e2c711afbd16f56b9d66e26ea0dff",
    "post_merge_receipt_pass_line": "PASS: MGAP4D external audit readiness post-merge green receipt checked",
    "bundle_manifest_pass_line": "PASS: MGAP4D external audit readiness bundle manifest checked",
    "all_governance_pass_line": "PASS: KuuOS all governance full checks completed",
}
POST_MERGE_RECEIPT_CLOSURE = {
    "pull_request": "#7",
    "pull_request_title": "Add MGAP4D post-merge green receipt v0.1",
    "pr_head_commit": "dec5e66ee46c2649cddb6273b55136cf844d4bbc",
    "base_before_merge": "e20d244d93eb85b3cfc9b46cf4bb4625923a8d82",
    "squash_merge_commit": "7f53a0adff847b59f7356875e1102fb7e3faf9fe",
    "merged_at": "2026-05-17T00:35:13Z",
    "closure_pass_line": "PASS: MGAP4D external audit readiness post-merge receipt closure checked",
}
PR8_MERGE_CLOSURE = {
    "pull_request": "#8",
    "pull_request_title": "Add MGAP4D post-merge receipt closure v0.1",
    "pr_head_commit": "98792d7e7ebd426f16c4b74eb868162d3cce09a2",
    "base_before_merge": "7f53a0adff847b59f7356875e1102fb7e3faf9fe",
    "squash_merge_commit": "d29468a831baff2c1cda847124f43a05d5574fb1",
    "merged_at": "2026-05-17T02:02:06Z",
    "closure_pass_line": "PASS: MGAP4D external audit readiness PR8 merge closure checked",
}
PR9_MERGE_CLOSURE = {
    "pull_request": "#9",
    "pull_request_title": "Add MGAP4D PR8 merge closure v0.1",
    "pr_head_commit": "0563ea21fd1922ca4979f7bc876aa11246aa4837",
    "base_before_merge": "d29468a831baff2c1cda847124f43a05d5574fb1",
    "squash_merge_commit": "f840ab0e8d497049ab232f187bb681c3337a3f30",
    "merged_at": "2026-05-17T02:32:35Z",
    "closure_pass_line": "PASS: MGAP4D external audit readiness PR9 merge closure checked",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_entry(path_text: str) -> dict:
    path = ROOT / path_text
    data = path.read_bytes()
    return {
        "path": path_text,
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code

    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_artifacts = [expected_entry(p) for p in ARTIFACTS]
    expected_root = sha256_bytes(json.dumps(expected_artifacts, sort_keys=True, separators=(",", ":")).encode("utf-8"))

    if manifest.get("schema") != "mgap4d_external_audit_readiness_bundle_manifest_v0_1":
        errors.append("schema mismatch")
    if manifest.get("status") != "CANDIDATE":
        errors.append("status must be CANDIDATE")
    if manifest.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if manifest.get("finality_packet_included") is not True:
        errors.append("finality_packet_included must be true")
    if manifest.get("post_merge_green_receipt_included") is not True:
        errors.append("post_merge_green_receipt_included must be true")
    if manifest.get("post_merge_receipt_closure_included") is not True:
        errors.append("post_merge_receipt_closure_included must be true")
    if manifest.get("pr8_merge_closure_included") is not True:
        errors.append("pr8_merge_closure_included must be true")
    if manifest.get("pr9_merge_closure_included") is not True:
        errors.append("pr9_merge_closure_included must be true")
    if manifest.get("artifact_count") != len(ARTIFACTS):
        errors.append("artifact_count mismatch")
    if manifest.get("artifacts") != expected_artifacts:
        errors.append("artifact hashes mismatch")
    if manifest.get("bundle_root_hash") != expected_root:
        errors.append("bundle_root_hash mismatch")
    if manifest.get("ci_green_reference") != CI_GREEN:
        errors.append("ci_green_reference mismatch")
    if manifest.get("all_governance_green_reference") != ALL_GOVERNANCE_GREEN:
        errors.append("all_governance_green_reference mismatch")
    if manifest.get("post_merge_green_reference") != POST_MERGE_GREEN:
        errors.append("post_merge_green_reference mismatch")
    if manifest.get("post_merge_receipt_closure_reference") != POST_MERGE_RECEIPT_CLOSURE:
        errors.append("post_merge_receipt_closure_reference mismatch")
    if manifest.get("pr8_merge_closure_reference") != PR8_MERGE_CLOSURE:
        errors.append("pr8_merge_closure_reference mismatch")
    if manifest.get("pr9_merge_closure_reference") != PR9_MERGE_CLOSURE:
        errors.append("pr9_merge_closure_reference mismatch")
    for flag in FALSE_FLAGS:
        if manifest.get(flag) is not False:
            errors.append(f"{flag} must be false")
    notes = "\n".join(manifest.get("notes", []))
    for token in [
        "Bundle manifest records hash evidence for ledger, chain index, finality packet, post-merge receipt, post-merge receipt closure, PR8 merge closure, PR9 merge closure, checkers, and dedicated workflow",
        "CI green does not grant proof/truth/clinical/execution/governance-bypass authority",
        "PR merge success is integration evidence, not theorem truth",
        "External audit readiness is not external audit acceptance",
        "Post-merge green confirms repository integration, not independent mathematical acceptance",
        "Post-merge receipt closure records integration of the receipt, not independent acceptance",
        "PR8 merge closure records integration of the closure layer, not independent acceptance",
        "PR9 merge closure records integration of the closure layer, not independent acceptance",
        "same-root and append-only",
    ]:
        if token not in notes:
            errors.append(f"missing note token: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1
    print("PASS: MGAP4D external audit readiness bundle manifest checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
