#!/usr/bin/env python3
"""KuuOS v1.104 4-simplex cocycle CodeAI portfolio, fixed Lean, real Lean MCP.

Exactly ordered: source-bound CodeAI proposals -> pinned direct Lean for all ->
real Lean MCP only for direct-green -> separate CI after explicit source promotion.
No theorem weakening, new axiom, sorry, unverified source promotion or Git writes.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import time

from runtime import kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as diff
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import (
    ROOT, REPO, TARGET as PREDECESSOR, require_event,
    read_example, source_observation,
)
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, require_pins, call_tool, tool_map,
)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured
from scripts.kuuos_lean_mcp_repair_loop_v1 import (
    require_semantics, forbidden_code_constructs, DISABLED_MCP_TOOLS,
)

TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104.lean"
MODULE="KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104"
ORIGINAL_V103_BLOB="ff2e6a09e2c064a23207ee1323bc14182c86d7cd"
OUT=Path("/tmp/kuuos-v1104-codeai-probes")
MCP_OUT=Path("/tmp/kuuos-v1104-real-mcp")
AXIOM_NAMES=[
    "NatFourSimplexTriangleLabels.strictLabel",
    "natFourCocycleOfLabels",
    "natFourTypeAIndex1Cocycle",
    "natFourTypeAIndex2Cocycle",
    "natFourTypeAIndex3Cocycle",
]

# Exact finite index labels: all remaining data are inherited from
# NatFourSimplexTriangleLabels in already-certified v1.99.
LABELS=[
    ("012","a012"),("013","a013"),("014","a014"),
    ("023","a023"),("024","a024"),("034","a034"),
    ("123","a123"),("124","a124"),("134","a134"),("234","a234"),
]

def source(tetra_tactic: str) -> str:
    label_cases="\n".join(
        f"  | {','.join(x)}, => L.{field}" if False else
        f"  | {x[0]}, {x[1]}, {x[2]} => L.{field}"
        for x,field in LABELS
    )
    return (
        "import KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103\n\n"
        "namespace "+MODULE+"\n\n"
        "open CategoryTheory\nopen Simplicial\n"
        "open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99\n"
        "open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100\n\n"
        "/-!\n"
        "The normalized four-dimensional additive Duskin cocycle constructed from\n"
        "the ten actual finite labels. This does not assert four-horn RLP:\n"
        "the geometric transport of all four visible face equations from a\n"
        "specified horn map remains an independent obligation.\n"
        "-/\n\n"
        "/-- Read a strict triangle from the exact ten-label table. -/\n"
        "def NatFourSimplexTriangleLabels.strictLabel\n"
        "    (L : NatFourSimplexTriangleLabels)\n"
        "    (a b c : Fin 5) : Nat :=\n"
        "  match a.val, b.val, c.val with\n"
        + label_cases + "\n  | _, _, _ => 0\n\n"
        "/-- All five ordinary tetrahedron equations induce a genuine,\n"
        "normalized Duskin cocycle on the ordinal of length five. -/\n"
        "def natFourCocycleOfLabels\n"
        "    (L : NatFourSimplexTriangleLabels)\n"
        "    (h0123 : L.eq0123) (h0124 : L.eq0124)\n"
        "    (h0134 : L.eq0134) (h0234 : L.eq0234)\n"
        "    (h1234 : L.eq1234) :\n"
        "    NatNormalizedDuskinCocycle 4 where\n"
        "  label a b c _ _ := L.strictLabel a b c\n"
        "  left_normalized := by\n"
        "    intro a b hab\n"
        "    fin_cases a <;> fin_cases b <;>\n"
        "      simp [NatFourSimplexTriangleLabels.strictLabel]\n"
        "  right_normalized := by\n"
        "    intro a b hab\n"
        "    fin_cases a <;> fin_cases b <;>\n"
        "      simp [NatFourSimplexTriangleLabels.strictLabel]\n"
        "  tetrahedron := by\n"
        "    intro a b c d hab hbc hcd\n"
        +tetra_tactic+"\n\n"
        "/-- The missing tetrahedron 0234 in type-A index 1 is forced by\n"
        "the other four faces; the output is a genuine cocycle. -/\n"
        "def natFourTypeAIndex1Cocycle\n"
        "    (L : NatFourSimplexTriangleLabels)\n"
        "    (h0123 : L.eq0123) (h0124 : L.eq0124)\n"
        "    (h0134 : L.eq0134) (h1234 : L.eq1234) :\n"
        "    NatNormalizedDuskinCocycle 4 :=\n"
        "  natFourCocycleOfLabels L h0123 h0124 h0134\n"
        "    (natFour_typeA_index1_missing_face L h0123 h0124 h0134 h1234) h1234\n\n"
        "/-- The missing tetrahedron 0134 in type-A index 2 is forced by\n"
        "the other four faces; the output is a genuine cocycle. -/\n"
        "def natFourTypeAIndex2Cocycle\n"
        "    (L : NatFourSimplexTriangleLabels)\n"
        "    (h0123 : L.eq0123) (h0124 : L.eq0124)\n"
        "    (h0234 : L.eq0234) (h1234 : L.eq1234) :\n"
        "    NatNormalizedDuskinCocycle 4 :=\n"
        "  natFourCocycleOfLabels L h0123 h0124\n"
        "    (natFour_typeA_index2_missing_face L h0123 h0124 h0234 h1234)\n"
        "    h0234 h1234\n\n"
        "/-- The missing tetrahedron 0124 in type-A index 3 is forced by\n"
        "the other four faces; the output is a genuine cocycle. -/\n"
        "def natFourTypeAIndex3Cocycle\n"
        "    (L : NatFourSimplexTriangleLabels)\n"
        "    (h0123 : L.eq0123) (h0134 : L.eq0134)\n"
        "    (h0234 : L.eq0234) (h1234 : L.eq1234) :\n"
        "    NatNormalizedDuskinCocycle 4 :=\n"
        "  natFourCocycleOfLabels L h0123\n"
        "    (natFour_typeA_index3_missing_face L h0123 h0134 h0234 h1234)\n"
        "    h0134 h0234 h1234\n\n"
        "end "+MODULE+"\n"
    )


def proposals() -> dict[str,str]:
    prefix=(
        "    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>\n"
        "      simp_all [NatFourSimplexTriangleLabels.strictLabel,\n"
        "        NatFourSimplexTriangleLabels.eq0123,\n"
        "        NatFourSimplexTriangleLabels.eq0124,\n"
        "        NatFourSimplexTriangleLabels.eq0134,\n"
        "        NatFourSimplexTriangleLabels.eq0234,\n"
        "        NatFourSimplexTriangleLabels.eq1234,\n"
        "        NatTetrahedronEquation]"
    )
    return {
        "round1-finite-simp-all":source(prefix),
        "round1-finite-simp-omega":source(prefix+" <;> omega"),
        "round1-finite-simp-omega-decide":source(prefix+" <;> omega <;> decide"),
    }


def mcp_verify(source_head: str,rows: list[dict],candidates: dict[str,str]) -> dict:
    passed=[r for r in rows if r.get("status")=="SUCCESS"
            and r.get("exit_code")==0 and r.get("olean_exists") is True
            and r.get("error_count")==0]
    MCP_OUT.mkdir(parents=True,exist_ok=False)
    record={
        "source_head":source_head,"candidate_count":len(rows),
        "direct_lean_green":[r["variant"] for r in passed],
        "selected":None,"mcp_success":False,"mcp_errors":None,
        "second_direct_success":False,"source_restored":False,
        "git_write_performed":False,"independent_ci_certified":False,
        "status":"DIRECT_LEAN_NO_GREEN",
    }
    target=ROOT/TARGET
    client=None
    try:
        if not passed:
            return record
        selected=passed[0]
        record["selected"]=selected["variant"]
        content=candidates[selected["variant"]].encode()
        if git_blob(content)!=selected["candidate_blob"]:
            raise RuntimeError("CodeAI source/Git-blob mismatch")
        if forbidden_code_constructs(content.decode()):
            raise RuntimeError("forbidden executable Lean construct")
        target.write_bytes(content)
        client=MCPClient(
            ["uvx","--from","lean-lsp-mcp==0.30.0","lean-lsp-mcp","--transport","stdio"],
            cwd=ROOT,
            env={
                "LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
                "LEAN_MCP_DISABLED_TOOLS":DISABLED_MCP_TOOLS,
                "LEAN_MCP_SCRATCH_SLOTS":"1",
            },timeout_seconds=240)
        client.request("initialize",{
            "protocolVersion":PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"KuuOS CodeAI v1.104","version":"1"},
        })
        client.notify("notifications/initialized")
        available=tool_map(client.request("tools/list"))
        required={"lean_diagnostic_messages","lean_goal","lean_multi_attempt"}
        if not required.issubset(available) or "lean_build" in available or "lean_run_code" in available:
            raise RuntimeError("missing or forbidden Lean MCP tools")
        diag=call_tool(client,"lean_diagnostic_messages",{
            "file_path":TARGET,"timeout_s":120,
        })
        check=require_semantics(structured(diag),content)
        record["mcp_success"]=check.success and not check.partial
        record["mcp_errors"]=len(check.errors)
        record["mcp_diagnostic_sha256"]=sha256(json.dumps(
            check.diagnostics,sort_keys=True).encode())
        if not check.success or check.partial or check.errors:
            raise RuntimeError("MCP diagnostics not completely green")
        for line in (1,55):
            for tool,params in (
                ("lean_goal",{"file_path":TARGET,"line":line}),
                ("lean_multi_attempt",{
                    "file_path":TARGET,"line":line,"snippets":["rfl","simp","omega"]}),
            ):
                try:
                    response=call_tool(client,tool,params)
                    record[tool+"_"+str(line)]=sha256(json.dumps(
                        response.get("result",{}),sort_keys=True).encode())
                except Exception as exc:
                    record[tool+"_"+str(line)+"_obstruction"]=str(exc)[:280]
        client.close();client=None
        with tempfile.TemporaryDirectory(prefix="v1104-mcp-second-") as directory:
            path=Path(directory)/"candidate.olean"
            result=subprocess.run(["lake","env","lean",
                "-DwarningAsError=true","-Dweak.sorryAsError=true",
                "-o",str(path),TARGET],
                cwd=ROOT,capture_output=True,text=True,timeout=500)
            log=result.stdout+"\n"+result.stderr
            (MCP_OUT/"second_direct_lean.log").write_text(log)
            record["second_direct_exit"]=result.returncode
            record["second_direct_log_sha256"]=sha256(log.encode())
            record["second_direct_success"]=result.returncode==0 and path.is_file()
            if not record["second_direct_success"] or "sorryAx" in log:
                raise RuntimeError("real MCP candidate failed second direct Lean")
        (MCP_OUT/"candidate.lean").write_bytes(content)
        record["selected_blob"]=git_blob(content)
        record["status"]="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI"
    except Exception as exc:
        record["status"]="MCP_OR_DIRECT_OBSTRUCTION"
        record["obstruction"]=type(exc).__name__+": "+str(exc)[:700]
    finally:
        if client is not None:
            try: client.close()
            except Exception as exc: record["close_obstruction"]=str(exc)[:200]
        target.unlink(missing_ok=True)
    return record


def main() -> int:
    head,branch,tree=require_event()
    require_pins(ROOT)
    if (ROOT/TARGET).exists():
        raise RuntimeError("v1.104 already exists: refuse to modify")
    predecessor=(ROOT/PREDECESSOR).read_bytes()
    if git_blob(predecessor)!=ORIGINAL_V103_BLOB:
        raise RuntimeError("v1.103 imported certificate blob drift")
    obs=source_observation(head,branch,tree,predecessor)
    candidates=proposals()
    sample=read_example("codeai_candidate_patch_envelope_v0_1.json")
    policy=deepcopy(sample["candidate_policy"])
    policy.update({
        "expected_source_observation_receipt_digest":obs[
            "codeai_intent_repository_observation_receipt_digest"],
        "expected_repository_full_name":REPO,
        "expected_source_commit_sha":head,
        "allowed_patch_formats":["unified_diff"],
        "maximum_changed_paths":1,
        "allowed_path_prefixes":["formal/KUOS"],
        "forbidden_path_prefixes":["legacy"],
        "allow_deletions":False,"allow_renames":False,
        "allow_binary_patches":False,"allow_submodule_patches":False,
        "allow_mode_changes":False,"require_requirement_trace":True,
        "require_test_plan":True,"allow_evidence_degradation":False,
        "known_risk_labels":["formal-proof"],"handover_risk_labels":[],
        "evaluation_epoch":int(time.time())+30,"maximum_candidate_age":3600,
    })
    policy=patch.seal(policy,patch.POLICY_DIGEST_FIELD)
    t=int(time.time())
    xs=[
        {
            "proposal_id":"v1104-"+name+"-"+head[:10],
            "candidate_revision":"r1",
            "producer_id":"codeai-finite-four-simplex-proof",
            "producer_session_id":"v1104-"+name+"-"+head[:8],
            "candidate_created_epoch":t,
            "edits":[{"path":TARGET,"operation":"add","new_content":src}],
            "requirement_trace_ids":["v1104:ten-labels-to-typed-normalized-four-simplex"],
            "test_plan_ids":["v1104:pinned-direct-lean-all-then-real-mcp"],
            "risk_labels":["formal-proof"],
            "unresolved_candidate_questions":[],
            "prior_candidate_digests":[],"prior_producer_session_ids":[],
        }
        for name,src in candidates.items()
    ]
    generated=diff.build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=obs,repository_files={},
        proposals=xs,candidate_policy=policy)
    if generated.status!=diff.STATUS_READY or generated.receipt is None or len(generated.candidates)!=len(xs):
        raise RuntimeError("CodeAI candidate set rejected:"+repr(generated.issues))
    OUT.mkdir(parents=True,exist_ok=False)
    results=[]
    try:
        for item in generated.candidates:
            name=next((n for n in candidates if
                item.patch_candidate["candidate_id"]=="v1104-"+n+"-"+head[:10]),None)
            if name is None:
                raise RuntimeError("CodeAI identity mismatch")
            if item.patch_candidate["added_paths"]!=[TARGET]:
                raise RuntimeError("CodeAI operation not a single added proof")
            s=candidates[name].encode()
            if forbidden_code_constructs(s.decode()):
                raise RuntimeError("candidate contains executable forbidden construct")
            row={"variant":name,"candidate_blob":git_blob(s),
                 "candidate_sha256":sha256(s),
                 "codeai_receipt":item.candidate_receipt[
                    "codeai_candidate_patch_receipt_digest"],
                 "status":"NO_DATA"}
            try:
                (ROOT/TARGET).write_bytes(s)
                with tempfile.TemporaryDirectory(prefix="v1104-lean-") as directory:
                    olean=Path(directory)/"candidate.olean"
                    try:
                        done=subprocess.run([
                            "lake","env","lean",
                            "-DwarningAsError=true",
                            "-Dweak.sorryAsError=true",
                            "-o",str(olean),TARGET],
                            cwd=ROOT,capture_output=True,text=True,timeout=600)
                        log=done.stdout+"\n"+done.stderr
                        row["exit_code"]=done.returncode
                        row["olean_exists"]=olean.is_file()
                        row["status"]="SUCCESS" if done.returncode==0 and olean.is_file() else "FAILURE"
                    except subprocess.TimeoutExpired as exc:
                        log=str(exc.stdout or "")+"\n"+str(exc.stderr or "")
                        row["status"]="TIMEOUT"
                    (OUT/(name+".log")).write_text(log)
                    row["log_sha256"]=sha256(log.encode())
                    errors=[x for x in log.splitlines() if "error:" in x or "error(" in x]
                    row["error_count"]=len(errors)
                    row["errors"]=[x[:700] for x in errors[:40]]
            finally:
                (ROOT/TARGET).unlink(missing_ok=True)
            results.append(row)
            print("KUUOS_V1104_CODEAI_DIRECT_CANDIDATE "+
                  json.dumps(row,ensure_ascii=False,sort_keys=True))
        mcp=mcp_verify(head,results,candidates)
        mcp["source_restored"]=not (ROOT/TARGET).exists()
        (MCP_OUT/"receipt.json").write_text(json.dumps(
            mcp,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
        print("KUUOS_V1104_REAL_MCP "+json.dumps(mcp,ensure_ascii=False,sort_keys=True))
        result={"source_head":head,"source_tree":tree,
                "imported_v1103_blob":ORIGINAL_V103_BLOB,
                "codeai_receipt":generated.receipt[
                    "codeai_autonomous_unified_diff_candidates_receipt_digest"],
                "candidate_count":len(results),"candidates":results,
                "source_restored":not (ROOT/TARGET).exists(),
                "independent_ci_certified":False,"git_write_performed":False}
        (OUT/"portfolio.json").write_text(json.dumps(
            result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
        print("KUUOS_V1104_CODEAI_SUMMARY "+json.dumps({
            "head":head,"candidate_count":len(results),
            "direct_green":sum(r["status"]=="SUCCESS" for r in results),
            "mcp_status":mcp["status"],
            "source_restored":result["source_restored"]},sort_keys=True))
        return 0 if result["source_restored"] else 3
    finally:
        (ROOT/TARGET).unlink(missing_ok=True)


if __name__=="__main__":
    raise SystemExit(main())
