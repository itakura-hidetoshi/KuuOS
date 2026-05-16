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
    "scripts/check_mgap4d_external_audit_readiness_ci_ledger_v0_1.py",
    "scripts/check_mgap4d_external_audit_readiness_chain_index_v0_1.py",
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
    if manifest.get("artifact_count") != len(ARTIFACTS):
        errors.append("artifact_count mismatch")
    if manifest.get("artifacts") != expected_artifacts:
        errors.append("artifact hashes mismatch")
    if manifest.get("bundle_root_hash") != expected_root:
        errors.append("bundle_root_hash mismatch")
    if manifest.get("ci_green_reference") != CI_GREEN:
        errors.append("ci_green_reference mismatch")
    for flag in FALSE_FLAGS:
        if manifest.get(flag) is not False:
            errors.append(f"{flag} must be false")
    notes = "\n".join(manifest.get("notes", []))
    for token in [
        "Bundle manifest records hash evidence",
        "CI green does not grant proof/truth/clinical/execution/governance-bypass authority",
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
