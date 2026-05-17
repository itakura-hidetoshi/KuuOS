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
PR11 = {
    "pull_request": "#11",
    "pull_request_title": "Add MGAP4D PR10 merge closure v0.1",
    "pr_head_commit": "d633a7c60fff5da9cd86c7a85e51aae60bed3fa8",
    "base_before_merge": "fb082f7caa0b5d009cd0dbca34412047ffe6599e",
    "squash_merge_commit": "d76fc29c09a3c87b27878bb5ec3969512e288cfd",
    "merged_at": "2026-05-17T03:32:18Z",
    "closure_pass_line": "PASS: MGAP4D external audit readiness PR11 merge closure checked",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_entry(path_text: str) -> dict:
    data = (ROOT / path_text).read_bytes()
    return {"path": path_text, "sha256": sha256_bytes(data), "size_bytes": len(data)}


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_artifacts = [expected_entry(p) for p in ARTIFACTS]
    expected_root = sha256_bytes(json.dumps(expected_artifacts, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    checks = {
        "schema": "mgap4d_external_audit_readiness_bundle_manifest_v0_1",
        "status": "CANDIDATE",
        "implementation_not_proof": True,
        "pr11_merge_closure_included": True,
        "artifact_count": len(ARTIFACTS),
        "bundle_root_hash": expected_root,
        "pr11_merge_closure_reference": PR11,
    }
    for key, value in checks.items():
        if manifest.get(key) != value:
            errors.append(f"{key} mismatch")
    if manifest.get("artifacts") != expected_artifacts:
        errors.append("artifact hashes mismatch")
    notes = "\n".join(manifest.get("notes", []))
    if "through PR11 merge closure" not in notes:
        errors.append("missing PR11 note")
    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1
    print("PASS: MGAP4D external audit readiness bundle manifest checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
