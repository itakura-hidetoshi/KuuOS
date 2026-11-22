#!/usr/bin/env python3
"""CodeAI v0.61 real Lean-LSP MCP confirmation on a pinned disposable candidate.

Must run AFTER actual CodeAI candidate portfolio and direct pinned Lean
verification of A and B, NEVER before. The candidate is materialized ONLY in
a disposable runner checkout, original source was absent, and this wrapper
removes it unconditionally. The actual repository Lean-MCP implementation
is used; the local receipt is not independent CI or a Git authority grant.
"""
from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copyfile
import hashlib
import json

from scripts import codeai_v061_two_stage_proof_proposal as base
from scripts.kuuos_lean_mcp_repair_loop_v1 import run_loop, mcp_tactic_provider

ROOT=base.ROOT
SOURCE=ROOT/base.PROPOSAL_SOURCE
TARGET=ROOT/base.CANDIDATE_PATH
RECEIPT_DIR=ROOT/"artifacts/codeai-v061-real-mcp-a"
EVIDENCE_FILE=ROOT/"artifacts/codeai-v061-independent-verification/verified-candidates.json"

def main() -> int:
    base._read_pinned_snapshot()
    verified=json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
    assert verified["canonical_parent_main"]==base.MAIN_HEAD
    row=verified["results"][0]
    assert row["label"]=="model-a"
    assert row["status"]=="INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED"
    source=SOURCE.read_bytes()
    expected=hashlib.sha256(source).hexdigest()
    assert expected==row["source_sha256"]
    assert expected=="2a33b3acccf3d18aa4caedb15b95e546e2bd6bb8d25f601175f44abd507c9642"
    assert not TARGET.exists()
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    try:
        with TARGET.open("xb") as f:
            f.write(source)
        # The actual KuuOS Lean-MCP repair loop prohibits exporting into
        # the repository root. Preserve that isolation: the MCP export stays
        # outside ROOT, and we copy only its read-only receipt back as an
        # artifact after validating the independent source correspondence.
        with TemporaryDirectory(prefix="kuuos-codeai-v061-mcp-") as temporary:
            external_mcp_dir=Path(temporary)/"export"
            result=run_loop(
                root=ROOT,
                rel_file=base.CANDIDATE_PATH,
                output_dir=external_mcp_dir,
                expected_sha256=expected,
                provider=mcp_tactic_provider,
                max_iterations=1,
                compile_timeout=300,
            )
            exported_receipt=external_mcp_dir/"receipt.json"
            assert exported_receipt.is_file()
            RECOVERY_DIR=RECEIPT_DIR
            RECOVERY_DIR.mkdir(parents=True,exist_ok=False)
            copyfile(exported_receipt,RECOVERY_DIR/"receipt.json")
        assert result["status"]=="LOCAL_LEAN_GREEN_CANDIDATE_ONLY",result
        assert result["source_restored"] is True
        assert result["provider_calls"]==0
        assert result["git_write_performed"] is False
        assert result["independent_ci_success"] is False
        assert result["original_sha256"]==expected
        assert result["candidate_sha256"]==expected
        assert len(result["rounds"])==1
        observation=result["rounds"][0]
        assert observation["source_sha256"]==expected
        assert observation["semantic_success"] is True
        assert observation["partial"] is False
        assert observation["errors"]==0
        assert observation["direct_lean"]["exit_code"]==0
        assert observation["forbidden_final_count"]==0
        entry={
            "schema":"kuuos.codeai.v061.actual-lean-mcp-reobservation.v1",
            "canonical_main_source_sha":base.MAIN_HEAD,
            "local_candidate_sha256":expected,
            "real_lean_mcp_version":"0.30.0",
            "actual_kernel_status":result["status"],
            "semantic_success":True,
            "partial":False,
            "errors":0,
            "provider_calls":0,
            "candidate_source_restored":True,
            "original_main_mutated":False,
            "independent_CI_proof_claimed":False,
            "git_authority":False,
        }
        (RECEIPT_DIR/"summary.json").write_text(
            json.dumps(entry,sort_keys=True,indent=2)+"\n",encoding="utf-8")
        print("V061_REAL_LEAN_MCP_CONFIRMED",json.dumps(entry,sort_keys=True))
    finally:
        if TARGET.exists():
            if TARGET.read_bytes()!=source:
                raise AssertionError("disposable_candidate_source_modified_no_silent_cleanup")
            TARGET.unlink()
        assert not TARGET.exists(),"disposable_file_was_not_removed"
        # Original pinned imports and canonical source remain byte-identical.
        base._read_pinned_snapshot()
    return 0

if __name__=="__main__":
    raise SystemExit(main())
