#!/usr/bin/env python3
"""CodeAI v1.90 R2: genuine R1 failed Lean/MCP feedback -> exact pinned notation
repair -> actual KuuOS-native synthesis -> fixed Lean. Never claim proof/learning
success from the static candidate or CodeAI advisory receipts alone.
"""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT,verify_inputs
from scripts.check_kuuos_lean_mcp_fullsource_v1 import create_report,git_blob
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import MCPClient,PROTOCOL_VERSION,call_tool,tool_map
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import require_semantics,mask_lean_comments

R1="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90.lean"
R2="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR2V1_90.lean"
ORIGINAL="formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationV1_90.lean"
OWNER="formal/KUOS/DependentOriginationNativeInfinityTwoScaledV1_19.lean"
R1_BLOB="58acbbfdebd045edf4826ded588b9d73071803ac"
R2_EXPECTED_BLOB="72758aebb1843c5a0e85ae0cd6c03835ac0a9084"
ORIGINAL_BLOB="d6a76712776b4a1b289b89bd691fa6213f8d36ce"
OWNER_BLOB="d05efb10005d646752b8cca90f5fdcc11267c101"
R1_NS="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90"
R2_NS="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR2V1_90"
SOURCE_BASE_HEAD="394a985a3707a01024926a21f78226fe00eb88af"
OUT=Path("/tmp/kuuos-v190-r2-real-mcp-codeai")
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([^\s(:]+)")
BANNED=re.compile(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b")

def main()->int:
    verify_inputs()
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch(r"[a-f0-9]{40}",head) or os.environ.get("GITHUB_REPOSITORY")!="itakura-hidetoshi/KuuOS":
        raise RuntimeError("V190_R2_NO_EXACT_GITHUB_EXECUTION_CONTEXT")
    source=(ROOT/R1).read_bytes()
    if (git_blob(source)!=R1_BLOB or
        git_blob((ROOT/ORIGINAL).read_bytes())!=ORIGINAL_BLOB or
        git_blob((ROOT/OWNER).read_bytes())!=OWNER_BLOB):
        raise RuntimeError("V190_R2_SOURCE_OR_OWNER_GIT_BLOB_CHANGED")
    if (ROOT/R2).exists():raise RuntimeError("V190_R2_MUST_BE_UNCOMMITTED")
    if OUT.exists() and list(OUT.iterdir()):raise RuntimeError("V190_R2_APPEND_ONLY_OUTPUT_CONFLICT")
    OUT.mkdir(parents=True,exist_ok=True)
    receipt={"kind":"KUUOS_V190_R2_GETELEM_DIAGNOSTIC_GUIDED_CODEAI",
        "execution_head":head,"source_parent_head":SOURCE_BASE_HEAD,
        "R1_negative_source_blob":R1_BLOB,"R1_source_sha256":hashlib.sha256(source).hexdigest(),
        "original_source_blob":ORIGINAL_BLOB,"owner_v119_blob":OWNER_BLOB,
        "R2_generated_blob":None,"status":"NO_DATA",
        "real_lean_mcp_status":"NO_DATA","native_codeai_status":"NO_DATA",
        "independent_lean_certified":False,
        "full_sealed_verification_guided_regeneration":"NO_DATA",
        "four_family_learning_admission":"HOLD",
        "git_write_or_merge_authority":False,"PR_adopted":False}
    def persist():
        receipt["R1_source_restored"]=(ROOT/R1).read_bytes()==source
        (OUT/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
        print("KUUOS_V190_R2_ACTUAL_CODEAI_RESULT "+json.dumps(receipt,ensure_ascii=False),flush=True)
    try:
        # Actual fixed Lean rerun must fail for the observed previous reason.
        lean=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
            "-KleanArgs=-DsorryAsError=true","build",R1_NS],
            capture_output=True,text=True,cwd=ROOT,timeout=3600)
        raw=lean.stdout+"\n"+lean.stderr
        (OUT/"R1-exact-failed-Lean.log").write_text(raw)
        if lean.returncode==0 or "GetElem" not in raw or "typeclass instance problem is stuck" not in raw:
            receipt["status"]="HOLD_NO_ACTUAL_R1_GETELEM_ERROR"
            return 2
        # Scan full R1/original sources and their entire pinned local dependency closure.
        plan={"schema_version":"kuuos-lean-fullsource-v1","source_head":head,"scope":"scoped",
              "targets":[{"path":R1,"git_blob_sha":R1_BLOB},
                         {"path":ORIGINAL,"git_blob_sha":ORIGINAL_BLOB}],
              "api_probes":[]}
        snap=create_report(ROOT,plan,raw,OUT/"fullsource",
                           max_deps=1800,probe_api=False,api_timeout=90)
        receipt["fullsource_status"]=snap["status"]
        receipt["fullsource_module_count"]=snap["full_source_snapshot_count"]
        receipt["full_import_closure_captured"]=snap["full_import_closure_captured"]
        receipt["full_source_obstructions"]=snap["obstructions"]
        if snap["status"]!="SOURCE_OBSERVATION_READY":
            receipt["status"]="HOLD_FULLSOURCE_OBSTRUCTION"
            return 2
        # CodeAI observes actual typed Lean MCP, never substitutes CI strings for MCP.
        disabled=",".join(["lean_run_code","lean_build","lean_profile_proof",
            "lean_minimal_hypotheses","lean_leansearch","lean_loogle",
            "lean_leanfinder","lean_state_search","lean_hammer_premise"])
        client=MCPClient(["uvx","--from","lean-lsp-mcp==0.30.0","lean-lsp-mcp",
                          "--transport","stdio"],cwd=ROOT,
                          env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
                               "LEAN_MCP_DISABLED_TOOLS":disabled,"LEAN_MCP_SCRATCH_SLOTS":"1"},
                          timeout_seconds=240)
        try:
            client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,
                  "capabilities":{},"clientInfo":{"name":"KuuOSCodeAIV190R2","version":"1"}})
            client.notify("notifications/initialized")
            tools=tool_map(client.request("tools/list"))
            if "lean_diagnostic_messages" not in tools or "lean_run_code" in tools or "lean_build" in tools:
                receipt["status"]="HOLD_REAL_LEAN_MCP_TOOL_SCOPE"
                return 2
            semantic=require_semantics(structured(call_tool(client,"lean_diagnostic_messages",
                                 {"file_path":R1,"timeout_s":120})),source)
        finally:
            client.close()
        receipt["real_lean_mcp_status"]="ACTUAL_TYPED_ERRORS"
        receipt["real_mcp_error_count"]=len(semantic.errors)
        receipt["real_mcp_diagnostic_digest"]=hashlib.sha256(
            json.dumps(semantic.diagnostics,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        receipt["real_mcp_first_errors"]=semantic.errors[:5]
        if semantic.success or semantic.partial or not any(
            "GetElem" in str(e.get("message","")) for e in semantic.errors):
            receipt["status"]="HOLD_MCP_NO_GETELEM_ERROR"
            return 2
        original=source.decode()
        if original.count("Delta[")!=41 or original.count(R1_NS)!=2:
            receipt["status"]="HOLD_R1_NOT_EXACT_ASCII_DELTA_REPAIR_SCOPE"
            return 2
        # All 41 malformed ASCII simplex terms, including documentary mentions,
        # normalized to the actual pinned Mathlib notation Δ[n].
        generated=original.replace("Delta[","Δ[").replace(R1_NS,R2_NS)
        names=DECL.findall(mask_lean_comments(original))
        if (len(names)!=27 or names!=DECL.findall(mask_lean_comments(generated)) or
            BANNED.search(mask_lean_comments(generated))):
            receipt["status"]="HOLD_R2_DECLARATION_OR_TRUST_BOUNDARY_CHANGED"
            return 2
        blob=git_blob(generated.encode())
        if blob!=R2_EXPECTED_BLOB:
            receipt["status"]="HOLD_R2_REGENERATED_BLOB_DIFFERS"
            return 2
        receipt["R2_generated_blob"]=blob
        receipt["R2_generated_sha256"]=hashlib.sha256(generated.encode()).hexdigest()
        receipt["repair_generator"]="deterministic_actual_GetElem_diagnostic_bound_Delta_to_UnicodeDelta"
        (OUT/"candidate_R2_generated.lean").write_text(generated)
        p=ROOT/R2
        try:
            p.write_text(generated)
            env=dict(os.environ)
            env["KUUOS_V190_R2_SOURCE_BLOB"]=blob
            n=subprocess.run([sys.executable,"scripts/ci_kuuos_v190_r2_after_mcp_native_codeai_v1.py"],
                cwd=ROOT,capture_output=True,text=True,timeout=300,env=env)
            (OUT/"native-codeai.log").write_text(n.stdout+"\n"+n.stderr)
            if n.returncode:
                receipt["status"]="HOLD_NATIVE_CODEAI_REJECTED_R2"
                receipt["native_error_excerpt"]=(n.stdout+"\n"+n.stderr)[-1400:]
                return 2
            native=json.loads((ROOT/"artifacts/codeai-v190-r2-mcp-native-governance/receipt.json").read_text())
            if (native["candidate_source_blob"]!=blob or
                native["boundary_statuses"]!=["CANDIDATE","REJECT"] or
                native["proof_certified_by_codeai"] or native["memory_admission"] or
                native["git_or_merge_authority"]):
                receipt["status"]="HOLD_NATIVE_CODEAI_SCOPE_MISMATCH"
                return 2
            receipt["native_codeai_status"]="CANDIDATE_AND_REJECT"
            receipt["native_synthesis_digest"]=native["codeai_synthesis_receipt_digest"]
            receipt["native_observation_digest"]=native["codeai_observation_receipt_digest"]
            shutil.copy2(ROOT/"artifacts/codeai-v190-r2-mcp-native-governance/receipt.json",
                        OUT/"native-codeai-receipt.json")
            compiled=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true","build",R2_NS],
                capture_output=True,text=True,cwd=ROOT,timeout=4500)
            text=compiled.stdout+"\n"+compiled.stderr
            (OUT/"R2-strict-Lean.log").write_text(text)
            receipt["R2_direct_Lean_exit"]=compiled.returncode
            if compiled.returncode:
                errors=[t for t in text.splitlines() if
                       "error:" in t or "unsolved goals" in t or "timed out" in t]
                receipt["R2_remaining_error_count"]=len(errors)
                receipt["R2_error_lines"]=errors[:70]
                receipt["status"]="HOLD_R2_REMAINING_TYPED_ERRORS"
                return 2
            receipt["status"]="LOCAL_R2_TYPED_MCP_CODEAI_LEAN_GREEN_UNADOPTED"
            return 0
        finally:
            p.unlink(missing_ok=True)
    except Exception as e:
        receipt["status"]="HOLD_EXCEPTION"
        receipt["exception"]=type(e).__name__+": "+str(e)[:1000]
        return 3
    finally:persist()

if __name__=="__main__":
    sys.exit(main())
