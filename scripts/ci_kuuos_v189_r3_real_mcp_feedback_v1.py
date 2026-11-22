#!/usr/bin/env python3
"""v1.89 R2 real full-source/Lean MCP failure -> bounded diagnostic-guided R3 synthesis.

Uses KuuOS's actual pinned full-source scanner and actual bounded Lean MCP repair
loop, not a prewritten candidate. A deterministic provider is allowed to propose
one proof-only edit ONLY after actual matching Lean errors. This is not the
sealed Verification-Guided Candidate Repair Regeneration v0.1 runtime and does
not claim its receipts, independent kernel certification or Memory promotion.
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
import time
from scripts.check_kuuos_lean_mcp_fullsource_v1 import create_report, git_blob
from scripts.kuuos_lean_mcp_repair_loop_v1 import run_loop, digest, Obstruction
from scripts.ci_kuuos_v176_exact_source_audit_v1 import verify_inputs

ROOT=Path(__file__).resolve().parents[1]
SOURCE_HEAD="14bfe7522997b6ca0b2f33390f5de6ae23c9bcf4"
TARGET="formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR2V1_89.lean"
R3="formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR3V1_89.lean"
SOURCE_BLOB="556208d79118b5b8f332e7fc49ba3657c15b4c20"
V188="formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
V188_BLOB="60283850a5de58e88705735379f208dd31d797df"
OLD_NS="KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR2V1_89"
NEXT_NS="KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR3V1_89"
OUT=Path("/tmp/kuuos-v189-r3-feedback-real-mcp")
OLD="  simpa [arbitrarySimplexScalingPresentation.{u}, standardABCPresentation.{u},\n"
NEW="  simpa [arbitrarySimplexScalingPresentation, standardABCPresentation,\n"

def emit(tag, fields):
    print(tag+" "+json.dumps(fields,sort_keys=True,ensure_ascii=False),flush=True)

def main():
    verify_inputs()
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch("[0-9a-f]{40}",head):
        raise RuntimeError("NO_DATA_EXECUTION_HEAD")
    if os.environ.get("GITHUB_REPOSITORY")!="itakura-hidetoshi/KuuOS":
        raise RuntimeError("NO_DATA_GITHUB_REPOSITORY")
    src=ROOT/TARGET
    raw=src.read_bytes()
    if git_blob(raw)!=SOURCE_BLOB or git_blob((ROOT/V188).read_bytes())!=V188_BLOB:
        raise RuntimeError("SOURCE_OR_IMPORT_BLOB_CHANGED")
    if (ROOT/R3).exists():
        raise RuntimeError("NEW_CANDIDATE_MUST_NOT_PREEXIST")
    if OUT.exists() and list(OUT.iterdir()):
        raise RuntimeError("APPEND_ONLY_OUTPUT_ALREADY_EXISTS")
    OUT.mkdir(parents=True,exist_ok=True)
    record={
        "schema":"kuuos.v189.codeai.r3.actual-mcp-feedback.v1",
        "research_execution_head":head,"parent_source_head":SOURCE_HEAD,
        "R2_source_blob":SOURCE_BLOB,"R2_source_sha256":hashlib.sha256(raw).hexdigest(),
        "R3_source_git_blob":None,"fullsource_ready":False,
        "actual_mcp_called":False,"codeai_native_synthesis_status":"NO_DATA_NOT_RUN",
        "actual_verification_guided_regeneration_v01":"NO_DATA_NO_SEALED_EXECUTION_LINEAGE",
        "independent_ci_certified":False,"PR_adopted":False,
        "verified_useful_memory_admitted":False,"git_write_performed":False,
        "source_restored":False,"status":"NO_DATA"
    }
    def save():
        record["source_restored"]=src.read_bytes()==raw
        (OUT/"receipt.json").write_text(json.dumps(record,sort_keys=True,
            indent=2,ensure_ascii=False)+"\n")
        emit("KUUOS_V189_R3_REAL_MCP_STATUS",record)
    try:
        baseline=subprocess.run(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",TARGET],cwd=ROOT,text=True,
            capture_output=True,timeout=1200)
        failure_text=baseline.stdout+"\n"+baseline.stderr
        (OUT/"r2-real-compiler.log").write_text(failure_text)
        if baseline.returncode==0 or failure_text.count("Invalid simp theorem")<2:
            record["status"]="HOLD_R2_ERROR_CONTEXT_CHANGED"
            return 2
        plan={"schema_version":"kuuos-lean-fullsource-v1",
          "source_head":head,"scope":"scoped",
          "targets":[{"path":TARGET,"git_blob_sha":SOURCE_BLOB}],
          "api_probes":[]}
        report=create_report(ROOT,plan,failure_text,OUT/"full_source",
            max_deps=1800,probe_api=False,api_timeout=90)
        record["fullsource_ready"]=report["status"]=="SOURCE_OBSERVATION_READY"
        record["import_closure_captured"]=report["full_import_closure_captured"]
        record["source_snapshot_count"]=report["full_source_snapshot_count"]
        record["source_obstructions"]=report["obstructions"]
        record["ci_log_source"]="actual same-run pinned direct Lean, not externally signed"
        if not record["fullsource_ready"]:
            record["status"]="HOLD_FULL_SOURCE_OBSTRUCTION"
            return 2

        proposed=[]
        def diagnostic_provider(current, observations):
            actual=json.dumps(observations[-1].get("errors",[]),ensure_ascii=False)
            if "Invalid simp theorem" not in actual:
                raise Obstruction("NO_DATA_ACTUAL_MCP_INVALID_SIMP_DIAGNOSTIC")
            if current.count(OLD)!=1:
                raise Obstruction("R2_INVALID_SIMP_PROOF_SPAN_NOT_UNIQUE")
            proposal={
                "expected_sha256":digest(current),"old_text":OLD,
                "new_text":NEW,
                "reason":"Real Lean MCP reported invalid simp theorem at exact v1.89 proof; remove explicit universe instantiations only from simp-unfolding argument list, preserve theorem/type universes",
            }
            proposed.append({"source_sha256":digest(current),
                "diagnostic_sha256":digest(actual),"old_text":OLD,"new_text":NEW,
                "origin":"algorithmic_diagnostic_guided_provider_not_live_LLM"})
            return proposal

        record["actual_mcp_called"]=True
        loop=run_loop(root=ROOT,rel_file=TARGET,
            output_dir=OUT/"mcp_loop",expected_sha256=hashlib.sha256(raw).hexdigest(),
            provider=diagnostic_provider,max_iterations=2,compile_timeout=1200)
        record["bounded_loop_status"]=loop["status"]
        record["bounded_loop_source_restored"]=loop.get("source_restored")
        record["mcp_rounds"]=loop.get("rounds",[])
        record["mcp_provider_calls"]=loop.get("provider_calls",0)
        record["feedback_driven_proposals"]=proposed
        record["actual_goal_observed"]=any("goal_digest" in item for item in loop.get("rounds",[]))
        record["actual_multi_attempt_observed"]=any("preliminary_tactic_details" in item for item in loop.get("rounds",[]))
        record["selected_tactic_line"]=next((item.get("selected_tactic_line") for item in loop.get("rounds",[])
             if item.get("selected_tactic_line") is not None),None)
        if (not record["actual_goal_observed"] or not record["actual_multi_attempt_observed"]
            or record["selected_tactic_line"] is None):
            record["status"]="HOLD_NO_TYPED_GOAL_AND_TACTIC_PROBES"
            return 2
        if loop["status"]!="LOCAL_LEAN_GREEN_CANDIDATE_ONLY":
            record["status"]="HOLD_MCP_OR_LEAN_ELABORATION"
            return 2
        candidate=(OUT/"mcp_loop"/"candidate.lean").read_text(encoding="utf8")
        before=raw.decode("utf8")
        if candidate!=before.replace(OLD,NEW) or candidate.count(OLD_NS)!=2:
            record["status"]="HOLD_NOT_EXACT_FEEDBACK_REPAIR"
            return 2
        if not loop.get("source_restored") or src.read_bytes()!=raw:
            record["status"]="HOLD_SOURCE_RESTORATION"
            return 2
        (OUT/"candidate_R2_repaired.lean").write_text(candidate,encoding="utf8")
        full=candidate.replace(OLD_NS,NEXT_NS)
        if full.count(NEXT_NS)!=2:
            record["status"]="HOLD_NAMESPACE_RENAME_NOT_EXACT"
            return 2
        (OUT/"candidate_R3_generated.lean").write_text(full,encoding="utf8")
        record["R3_source_git_blob"]=git_blob(full.encode("utf8"))
        record["R3_source_sha256"]=hashlib.sha256(full.encode("utf8")).hexdigest()
        # Candidate was generated in this job FROM actual Lean MCP typed
        # diagnostics. Only now present this ephemeral result to genuine
        # KuuOS-native CodeAI source-observation / structured-synthesis kernels.
        r3path=ROOT/R3
        if r3path.exists():
            raise RuntimeError("R3_ALREADY_EXISTS_NOT_ALGORITHM_GENERATED")
        try:
            r3path.write_text(full,encoding="utf8")
            native_env=dict(os.environ)
            native_env["KUUOS_R3_SOURCE_BLOB"]=record["R3_source_git_blob"]
            native=subprocess.run([sys.executable,
                "scripts/ci_kuuos_v189_r3_after_mcp_native_codeai_v1.py"],
                cwd=ROOT,env=native_env,capture_output=True,text=True,timeout=240)
            (OUT/"codeai-native.log").write_text(native.stdout+"\n"+native.stderr)
            if native.returncode:
                record["status"]="HOLD_NATIVE_CODEAI_REJECTED_DYNAMIC_R3"
                record["codeai_native_obstruction"]=(native.stdout+"\n"+native.stderr)[-1200:]
                return 2
            native_receipt=ROOT/"artifacts/codeai-v189-r3-live-mcp-native-governance/receipt.json"
            receipt=json.loads(native_receipt.read_text())
            if (receipt["candidate_source_blob"]!=record["R3_source_git_blob"] or
                receipt["boundary_statuses"]!=["CANDIDATE","REJECT"] or
                receipt["proof_certified_by_codeai"] or receipt["memory_admission"] or
                receipt["git_or_merge_authority"]):
                record["status"]="HOLD_NATIVE_CODEAI_RECEIPT_BOUNDARY"
                return 2
            shutil.copy2(native_receipt,OUT/"codeai-native-receipt.json")
            record["codeai_native_synthesis_status"]="ACTUAL_CODEAI_CANDIDATE_AND_REJECT"
            record["codeai_synthesis_receipt_digest"]=receipt["codeai_synthesis_receipt_digest"]
            record["codeai_observation_receipt_digest"]=receipt["codeai_observation_receipt_digest"]
        finally:
            r3path.unlink(missing_ok=True)
        record["status"]="LOCAL_REAL_MCP_CODEAI_AND_DIRECT_LEAN_GREEN_UNADOPTED"
        return 0
    except Exception as exc:
        record["status"]="HOLD_RUNTIME_EXCEPTION"
        record["obstruction"]=type(exc).__name__+": "+str(exc)[:700]
        return 3
    finally:
        save()

if __name__=="__main__":
    sys.exit(main())
