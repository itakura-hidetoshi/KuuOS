#!/usr/bin/env python3
"""CodeAI v1.90 R4: failed R3 pinned kernel / real Lean MCP diagnostics ->
exact bounded dependent-rewrite trial -> actual native CodeAI -> pinned Lean.
Not a proof or a verified-useful Memory hint unless separate independent CI passes.
"""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT,verify_inputs
from scripts.check_kuuos_lean_mcp_fullsource_v1 import create_report,git_blob
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import MCPClient,PROTOCOL_VERSION,call_tool,tool_map
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics,mask_lean_comments

R3="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR3V1_90.lean"
R4="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR4V1_90.lean"
ORIGINAL="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationV1_90.lean"
R3_BLOB="d40387a3f2993d20c706cff01effd5ca8df91fb2"
R4_BLOB="e6db5e9fa5ea2201c2f93448da481234ba6b5728"
ORIGINAL_BLOB="d6a76712776b4a1b289b89bd691fa6213f8d36ce"
SOURCE_BASE_HEAD="8a1705dcc48844408837877886d5a7c6a23ca184"
NS3="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR3V1_90"
NS4="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR4V1_90"
OUT=Path("/tmp/kuuos-v190-r4-real-mcp-codeai")
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([^\s(:]+)")
BANNED=re.compile(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b")
PATCHES=[
 ("    dsimp [scalingEnrichmentPushoutScaling] at hu\n",
  "    change (finiteTriangleScaling F).thin u ∨\n"
  "      (∃ x : (Δ[n] : SSet.{u}).obj (op ⦋2⦌),\n"
  "        (singleTriangleScaling t).thin x ∧ (𝟙 (Δ[n] : SSet.{u})).app (op ⦋2⦌) x = u) at hu\n"),
 ("  rw [hscale] at hpush\n","  simp only [hscale] at hpush\n"),
 ("      rw [finiteTriangleScaling_empty]\n","      simp only [finiteTriangleScaling_empty] at *\n"),
 ("  rw [hscale] at hfinite\n","  simp only [hscale] at hfinite\n"),
]

def main()->int:
    verify_inputs()
    head=os.getenv("SOURCE_HEAD","")
    if not re.fullmatch("[0-9a-f]{40}",head) or os.getenv("GITHUB_REPOSITORY")!="itakura-hidetoshi/KuuOS":
        raise RuntimeError("V190_R4_UNPINNED_RUN_CONTEXT")
    source=(ROOT/R3).read_bytes()
    if git_blob(source)!=R3_BLOB or git_blob((ROOT/ORIGINAL).read_bytes())!=ORIGINAL_BLOB:
        raise RuntimeError("V190_R4_EXACT_SOURCE_DRIFT")
    if (ROOT/R4).exists():raise RuntimeError("V190_R4_CANDIDATE_PREEXISTS")
    if OUT.exists() and list(OUT.iterdir()):raise RuntimeError("V190_R4_APPEND_ONLY_OUTPUT")
    OUT.mkdir(parents=True,exist_ok=True)
    receipt={"kind":"KUUOS_V190_R4_REAL_TYPED_REWRITE_CODEAI",
       "execution_head":head,"source_parent_head":SOURCE_BASE_HEAD,
       "R3_source_blob":R3_BLOB,"R3_source_sha256":hashlib.sha256(source).hexdigest(),
       "R4_generated_blob":None,"status":"NO_DATA","fullsource_status":"NO_DATA",
       "real_lean_mcp_status":"NO_DATA","native_codeai_status":"NO_DATA",
       "PR_adopted":False,"independent_lean_certified":False,
       "verified_useful_Memory":"HOLD","full_sealed_regeneration_v01":"NO_DATA",
       "git_or_merge_authority":False}
    def save():
        receipt["R3_source_restored"]=(ROOT/R3).read_bytes()==source
        (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2,
             sort_keys=True,ensure_ascii=False)+"\n")
        print("KUUOS_V190_R4_ACTUAL_TYPED_CODEAI "+json.dumps(receipt,ensure_ascii=False),flush=True)
    try:
        original=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true","build",NS3],
                cwd=ROOT,capture_output=True,text=True,timeout=4400)
        log=original.stdout+"\n"+original.stderr
        (OUT/"R3-original-fixed-Lean.log").write_text(log)
        if original.returncode==0:
            receipt["status"]="HOLD_R3_ALREADY_KERNEL_GREEN_NO_REPAIR_NEEDED"
            return 2
        reason_dsimp="dsimp" in log and "made no progress" in log
        reason_rewrite="motive is not type correct" in log
        receipt["actual_r3_dsimp_error"]=reason_dsimp
        receipt["actual_r3_dependent_rewrite_error"]=reason_rewrite
        if not reason_dsimp and not reason_rewrite:
            receipt["status"]="HOLD_R3_FAILURE_NOT_THE_TARGETED_PROOF_ERROR"
            return 2
        plan={"schema_version":"kuuos-lean-fullsource-v1",
              "source_head":head,"scope":"scoped",
              "targets":[{"path":R3,"git_blob_sha":R3_BLOB},
                         {"path":ORIGINAL,"git_blob_sha":ORIGINAL_BLOB}],"api_probes":[]}
        report=create_report(ROOT,plan,log,OUT/"fullsource",
                             max_deps=1800,probe_api=False,api_timeout=90)
        receipt["fullsource_status"]=report["status"]
        receipt["full_source_count"]=report["full_source_snapshot_count"]
        receipt["full_import_closure_captured"]=report["full_import_closure_captured"]
        receipt["full_source_obstructions"]=report["obstructions"]
        if report["status"]!="SOURCE_OBSERVATION_READY":
            receipt["status"]="HOLD_FULL_SOURCE_OBSTRUCTION"
            return 2
        disabled=",".join(["lean_run_code","lean_build","lean_profile_proof","lean_minimal_hypotheses",
          "lean_leansearch","lean_loogle","lean_leanfinder","lean_state_search","lean_hammer_premise"])
        client=MCPClient(["uvx","--from","lean-lsp-mcp==0.30.0","lean-lsp-mcp","--transport","stdio"],
                cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
                "LEAN_MCP_DISABLED_TOOLS":disabled,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
        try:
            client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,
               "capabilities":{},"clientInfo":{"name":"CodeAIV190R4","version":"1"}})
            client.notify("notifications/initialized")
            tools=tool_map(client.request("tools/list"))
            if "lean_diagnostic_messages" not in tools or "lean_run_code" in tools or "lean_build" in tools:
                receipt["status"]="HOLD_UNSAFE_MCP_TOOLS"
                return 2
            observation=require_semantics(structured(call_tool(client,"lean_diagnostic_messages",
                             {"file_path":R3,"timeout_s":120})),source)
        finally:
            client.close()
        receipt["real_lean_mcp_status"]="ACTUAL_TYPED_ERRORS"
        receipt["mcp_error_count"]=len(observation.errors)
        receipt["mcp_diagnostic_digest"]=hashlib.sha256(json.dumps(observation.diagnostics,
           ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        receipt["mcp_first_error_excerpt"]=observation.errors[:8]
        if observation.success or observation.partial or not any(
               ("rewrite" in str(x.get("message","")).lower() or
               "dsimp" in str(x.get("message","")).lower()) for x in observation.errors):
            receipt["status"]="HOLD_TYPED_MCP_DOES_NOT_SUPPORT_REWRITE_REPAIR"
            return 2
        text=source.decode()
        if text.count(NS3)!=2 or any(text.count(old)!=1 for old,_ in PATCHES):
            receipt["status"]="HOLD_R4_EDIT_ANCHOR_SCOPE"
            return 2
        generated=text.replace(NS3,NS4)
        for old,new in PATCHES:generated=generated.replace(old,new,1)
        if (DECL.findall(mask_lean_comments(generated))!=
            DECL.findall(mask_lean_comments(text)) or
            len(DECL.findall(mask_lean_comments(generated)))!=27 or
            BANNED.search(mask_lean_comments(generated))):
            receipt["status"]="HOLD_R4_PUBLIC_PROOF_INTERFACE_OR_TRUST_BYPASS"
            return 2
        candidate=git_blob(generated.encode())
        if candidate!=R4_BLOB:
            receipt["status"]="HOLD_R4_UNEXPECTED_CANDIDATE_BLOB"
            return 2
        receipt["R4_generated_blob"]=candidate
        receipt["R4_generated_sha256"]=hashlib.sha256(generated.encode()).hexdigest()
        receipt["generator"]="deterministic_actual_R3_dependent_rewrite_or_dsimp_error_bounded_patch"
        (OUT/"candidate_R4_generated.lean").write_text(generated)
        p=ROOT/R4
        try:
            p.write_text(generated)
            env=dict(os.environ);env["KUUOS_V190_R4_SOURCE_BLOB"]=candidate
            n=subprocess.run([sys.executable,"scripts/ci_kuuos_v190_r4_after_mcp_native_codeai_v1.py"],
               cwd=ROOT,env=env,capture_output=True,text=True,timeout=260)
            (OUT/"native-codeai.log").write_text(n.stdout+"\n"+n.stderr)
            if n.returncode:
                receipt["status"]="HOLD_NATIVE_CODEAI_PROPOSAL_REJECTED"
                receipt["native_error_excerpt"]=(n.stdout+"\n"+n.stderr)[-1600:]
                return 2
            nr=json.loads((ROOT/"artifacts/codeai-v190-r4-mcp-native-governance/receipt.json").read_text())
            if nr["candidate_source_blob"]!=candidate or nr["boundary_statuses"]!=["CANDIDATE","REJECT"] or nr["proof_certified_by_codeai"] or nr["memory_admission"] or nr["git_or_merge_authority"]:
                receipt["status"]="HOLD_NATIVE_RECEIPT_AUTHORITY"
                return 2
            receipt["native_codeai_status"]="ACTUAL_NATIVE_CANDIDATE_AND_REJECT"
            shutil.copy2(ROOT/"artifacts/codeai-v190-r4-mcp-native-governance/receipt.json",
                         OUT/"native-codeai-receipt.json")
            b=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
                 "-KleanArgs=-DsorryAsError=true","build",NS4],
                 cwd=ROOT,capture_output=True,text=True,timeout=4800)
            out=b.stdout+"\n"+b.stderr
            (OUT/"R4-strict-Lean.log").write_text(out)
            receipt["direct_Lean_exit"]=b.returncode
            if b.returncode:
                errs=[line for line in out.splitlines() if "error:" in line or "unsolved goals" in line or "timed out" in line]
                receipt["remaining_errors"]=errs[:70]
                receipt["remaining_error_count"]=len(errs)
                receipt["status"]="HOLD_R4_REMAINING_TYPED_LEAN_ERRORS"
                return 2
            receipt["status"]="LOCAL_R4_MCP_NATIVE_CODEAI_AND_LEAN_GREEN_UNADOPTED"
            return 0
        finally:
            p.unlink(missing_ok=True)
    except Exception as e:
        receipt["status"]="HOLD_EXCEPTION"
        receipt["exception"]=type(e).__name__+": "+str(e)[:950]
        return 3
    finally:save()
if __name__=="__main__":
    sys.exit(main())
