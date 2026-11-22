#!/usr/bin/env python3
"""Actual v1.90 native CodeAI research: source-bound Lean MCP diagnosis -> bounded
namespace candidate synthesis -> KuuOS-native CANDIDATE/REJECT -> local Lean.
This is deterministic error-feedback synthesis, not live LLM inference and
NOT the fully sealed Verification-Guided Regeneration v0.1 predecessor chain.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from scripts.ci_kuuos_v176_exact_source_audit_v1 import verify_inputs
from scripts.check_kuuos_lean_mcp_fullsource_v1 import create_report,git_blob
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import MCPClient,PROTOCOL_VERSION,call_tool,tool_map
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics,mask_lean_comments

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationV1_90.lean"
BASE="formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointV1_89.lean"
OWNER="formal/KUOS/DependentOriginationNativeInfinityTwoScaledV1_19.lean"
CANDIDATE="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90.lean"
OLD_NS="KUOS.DependentOriginationSingleTriangleScalingFiltrationV1_90"
NEW_NS="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90"
ORIGINAL_BLOB="d6a76712776b4a1b289b89bd691fa6213f8d36ce"
BASE_BLOB="d29c5cb0984688ea5fc915a5c7bfa4dd6d8ca4a8"
OWNER_BLOB="d05efb10005d646752b8cca90f5fdcc11267c101"
SOURCE_BASE_HEAD="92f2a271514b445b95812c2e74bb94642bf5af93"
OUT=Path("/tmp/kuuos-v190-r1-real-mcp-codeai")
INSERT="open Simplicial\n"
REPLACE="open Simplicial\nopen KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\n"
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([^\s(:]+)")
BANNED=re.compile(r"(?m)^\s*(sorry|admit|axiom|unsafe|native_decide)\b")

def write_json(name,value):
    (OUT/name).write_text(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+"\n")

def main():
    verify_inputs()
    execution=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch("[0-9a-f]{40}",execution):
        raise RuntimeError("V190_R1_NO_EXECUTION_HEAD")
    if os.environ.get("GITHUB_REPOSITORY")!="itakura-hidetoshi/KuuOS":
        raise RuntimeError("V190_R1_WRONG_REPOSITORY")
    original=(ROOT/ORIGINAL).read_bytes()
    if (git_blob(original)!=ORIGINAL_BLOB or
        git_blob((ROOT/BASE).read_bytes())!=BASE_BLOB or
        git_blob((ROOT/OWNER).read_bytes())!=OWNER_BLOB):
        raise RuntimeError("V190_R1_ORIGINAL_DEPENDENCY_OR_OWNER_CHANGED")
    owner=(ROOT/OWNER).read_text()
    if ("namespace KUOS.DependentOriginationNativeInfinityTwoScaledV1_19" not in owner or
        "structure ScaledSimplicialSet" not in owner):
        raise RuntimeError("V190_R1_PINNED_TYPE_OWNER_UNCONFIRMED")
    if (ROOT/CANDIDATE).exists():
        raise RuntimeError("V190_R1_CANDIDATE_MUST_BE_UNCOMMITTED")
    if OUT.exists() and any(OUT.iterdir()):
        raise RuntimeError("V190_R1_OUTPUT_APPEND_ONLY_CONFLICT")
    OUT.mkdir(parents=True,exist_ok=True)
    rec={"kind":"KUUOS_V190_R1_REAL_MCP_TYPED_NAMESPACE_PROPOSAL",
        "head":execution,"source_head_parent":SOURCE_BASE_HEAD,
        "original_blob":ORIGINAL_BLOB,"original_sha256":hashlib.sha256(original).hexdigest(),
        "owner_blob":OWNER_BLOB,"base_v189_blob":BASE_BLOB,
        "source_unchanged":False,
        "mcp_status":"NO_DATA_NOT_OBSERVED","mcp_goal_status":"NOT_APPLICABLE_NON_TACTIC_TYPE_ERROR",
        "codeai_native_status":"NO_DATA_NOT_RUN",
        "verification_guided_regeneration_v01":"NO_DATA_NO_SEALED_EXECUTION_LINEAGE",
        "candidate_git_blob":None,"formal_certified":False,"independent_runner_certified":False,
        "memory_promoted":False,"main_or_PR_adopted":False,"git_or_merge_authority":False,
        "status":"NO_DATA"}
    def persist():
        rec["source_unchanged"]=(ROOT/ORIGINAL).read_bytes()==original
        write_json("receipt.json",rec)
        print("KUUOS_V190_R1_ACTUAL_TYPED_CODEAI "+json.dumps(rec,ensure_ascii=False),flush=True)
    try:
        # First reproduce the actual pinned original error, not an invented diagnostic.
        original_build=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
           "-KleanArgs=-DsorryAsError=true","build",OLD_NS],cwd=ROOT,
           capture_output=True,text=True,timeout=2800)
        rawlog=original_build.stdout+"\n"+original_build.stderr
        (OUT/"original-strict-Lean.log").write_text(rawlog)
        if original_build.returncode==0 or "ScaledSimplicialSet" not in rawlog:
            rec["status"]="HOLD_ORIGINAL_DIAGNOSTICS_DIFFER"
            return 2
        plan={"schema_version":"kuuos-lean-fullsource-v1",
            "source_head":execution,"scope":"scoped",
            "targets":[{"path":ORIGINAL,"git_blob_sha":ORIGINAL_BLOB}],
            "api_probes":[]}
        snapshot=create_report(ROOT,plan,rawlog,OUT/"fullsource",
            max_deps=1800,probe_api=False,api_timeout=90)
        rec["full_source_status"]=snapshot["status"]
        rec["full_source_count"]=snapshot["full_source_snapshot_count"]
        rec["full_import_closure_captured"]=snapshot["full_import_closure_captured"]
        rec["source_obstructions"]=snapshot["obstructions"]
        if snapshot["status"]!="SOURCE_OBSERVATION_READY":
            rec["status"]="HOLD_FULL_SOURCE_OBSTRUCTION"
            return 2
        # Real pinned Lean MCP semantic evidence, not static compiler strings alone.
        disabled=",".join(["lean_run_code","lean_build","lean_profile_proof",
           "lean_minimal_hypotheses","lean_leansearch","lean_loogle",
           "lean_leanfinder","lean_state_search","lean_hammer_premise"])
        cmd=["uvx","--from","lean-lsp-mcp==0.30.0","lean-lsp-mcp","--transport","stdio"]
        env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
           "LEAN_MCP_DISABLED_TOOLS":disabled,"LEAN_MCP_SCRATCH_SLOTS":"1"}
        client=MCPClient(cmd,cwd=ROOT,env=env,timeout_seconds=240)
        try:
            client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,
              "capabilities":{},"clientInfo":{"name":"V190R1CodeAI","version":"1"}})
            client.notify("notifications/initialized")
            available=tool_map(client.request("tools/list"))
            if ("lean_diagnostic_messages" not in available or
                "lean_run_code" in available or "lean_build" in available):
                rec["status"]="HOLD_MCP_TOOL_SCOPE"
                return 2
            raw=call_tool(client,"lean_diagnostic_messages",{"file_path":ORIGINAL,"timeout_s":120})
            typed=require_semantics(structured(raw),original)
        finally:
            client.close()
        rec["mcp_status"]="ACTUAL_TYPED_PINNED_SOURCE_DIAGNOSTICS"
        rec["mcp_error_count"]=len(typed.errors)
        rec["mcp_partial"]=typed.partial
        rec["mcp_diagnostic_digest"]=hashlib.sha256(
          json.dumps(typed.diagnostics,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        rec["mcp_error_excerpt"]=typed.errors[:8]
        if (typed.success or typed.partial or
            not any("ScaledSimplicialSet" in str(e.get("message","")) for e in typed.errors)):
            rec["status"]="HOLD_MCP_DID_NOT_CONFIRM_NAMESPACE_FAILURE"
            return 2
        source=original.decode("utf8")
        if source.count(INSERT)!=1 or source.count(OLD_NS)!=2:
            rec["status"]="HOLD_AMBIGUOUS_SOURCE_TRANSFORM"
            return 2
        candidate=source.replace(INSERT,REPLACE).replace(OLD_NS,NEW_NS)
        original_names=DECL.findall(mask_lean_comments(source))
        generated_names=DECL.findall(mask_lean_comments(candidate))
        if original_names!=generated_names or len(original_names)!=27:
            rec["status"]="HOLD_PUBLIC_DECLARATION_CHANGE"
            return 2
        if BANNED.search(mask_lean_comments(candidate)):
            rec["status"]="HOLD_TRUST_BYPASS"
            return 2
        rec["candidate_git_blob"]=git_blob(candidate.encode())
        rec["candidate_sha256"]=hashlib.sha256(candidate.encode()).hexdigest()
        rec["source_owner_scope_verified"]=True
        rec["R1_generator"]="deterministic_one_open_statement_after_actual_typed_MCP_error"
        (OUT/"candidate_R1_generated.lean").write_text(candidate)
        cpath=ROOT/CANDIDATE
        try:
            cpath.write_text(candidate)
            native_env=dict(os.environ)
            native_env["KUUOS_V190_R1_SOURCE_BLOB"]=rec["candidate_git_blob"]
            nr=subprocess.run([sys.executable,
              "scripts/ci_kuuos_v190_r1_after_mcp_native_codeai_v1.py"],
              cwd=ROOT,env=native_env,capture_output=True,text=True,timeout=240)
            (OUT/"native-codeai.log").write_text(nr.stdout+"\n"+nr.stderr)
            if nr.returncode:
                rec["status"]="HOLD_NATIVE_CODEAI_CANDIDATE_GOVERNANCE"
                rec["codeai_exception_excerpt"]=(nr.stdout+"\n"+nr.stderr)[-1400:]
                return 2
            nrec=json.loads((ROOT/"artifacts/codeai-v190-r1-mcp-native-governance/receipt.json").read_text())
            if (nrec["candidate_source_blob"]!=rec["candidate_git_blob"] or
                nrec["boundary_statuses"]!=["CANDIDATE","REJECT"] or
                nrec["proof_certified_by_codeai"] or nrec["memory_admission"] or
                nrec["git_or_merge_authority"]):
                rec["status"]="HOLD_NATIVE_CODEAI_RECEIPT_MISMATCH"
                return 2
            shutil.copy2(ROOT/"artifacts/codeai-v190-r1-mcp-native-governance/receipt.json",
                OUT/"native-codeai-receipt.json")
            rec["codeai_native_status"]="ACTUAL_NATIVE_CANDIDATE_AND_REJECT"
            rec["native_synthesis_digest"]=nrec["codeai_synthesis_receipt_digest"]
            rec["native_observation_digest"]=nrec["codeai_observation_receipt_digest"]
            # Distinct from CodeAI governance: real pinned Lean candidate compilation.
            build=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true","build",NEW_NS],cwd=ROOT,
                capture_output=True,text=True,timeout=3800)
            log=build.stdout+"\n"+build.stderr
            (OUT/"candidate-strict-Lean.log").write_text(log)
            rec["local_Lean_returncode"]=build.returncode
            if build.returncode:
                errs=[ln for ln in log.splitlines() if
                      "error:" in ln or "unsolved goals" in ln or "timed out" in ln]
                rec["local_error_count"]=len(errs)
                rec["local_error_lines"]=errs[:60]
                rec["status"]="HOLD_R1_FURTHER_TYPED_ELABORATION_ERRORS"
                return 2
            rec["status"]="LOCAL_TYPED_MCP_NATIVE_CODEAI_AND_LEAN_GREEN_UNADOPTED"
            return 0
        finally:
            cpath.unlink(missing_ok=True)
    except Exception as e:
        rec["status"]="HOLD_EXECUTION_EXCEPTION"
        rec["exception"]=type(e).__name__+": "+str(e)[:750]
        return 3
    finally:
        persist()

if __name__=="__main__":
    sys.exit(main())
