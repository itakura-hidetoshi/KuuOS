#!/usr/bin/env python3
"""R71 R2: remove two surplus closing parentheses in the generated computation only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registered_basis_path_v1_r71_r3_core as r1
v=r1.v
HEAD="6bd354e686bc4b75d3d33091e8b452b81166e124"
RUN=46111603187
JOB=140876150708
ART=15249837109
DIGEST="sha256:d1d683fe3f69694273bceddc3684e8a29097b32623f81be079fcc1f2a8db283b"
RETRY_HEAD="2abcbc756a1d0489db366aba466b06aaffcdaddd"
RETRY_RUN=46111619725
RETRY_JOB=140877860571
FORMAL_SHA="1b7840ec21ce9522f2621d61e1cd9c82bd717d1c71483ec7f437750cbf657e44"
APP_SHA="2544e7bed820c688ce7f210179f52a5af924aaed59c6de146ee4482c522f69a8"
COMPUTE_SHA="71e408af56ad0048ac795f44596501a0d1b271476627df7f31e3002a703c979c"
LOG_SHA="2e935fdcb12294174f92a925a2b424e509836239610f1488996dc3b12d36fb93"
BEFORE="    (\"unknown_alias_tagged_accepts\", Lean.toJson (decide (KuuOSR70.checkedTaggedPath unknownKey unknownKey f f [] = some ((∅ : KuuOSR69.Basis Nat), (∅ : KuuOSR69.Basis Nat)))))),"
AFTER="    (\"unknown_alias_tagged_accepts\", Lean.toJson (decide (KuuOSR70.checkedTaggedPath unknownKey unknownKey f f [] = some ((∅ : KuuOSR69.Basis Nat), (∅ : KuuOSR69.Basis Nat))))),"
ORIGINAL=r1.registry_sources

def bind(a):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN));job=api("actions/jobs/"+str(JOB))
    art=api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="failure" and
           job["head_sha"]==HEAD and job["run_id"]==RUN and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R71 registered basis path" and s["conclusion"]=="failure" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R71 new declarations and exact prior receipt reuse" and s["conclusion"]=="skipped" for s in job["steps"]),
           "R71 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r71-local-46111603187-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R71 R1 artifact lineage")
    retry=api("actions/runs/"+str(RETRY_RUN));rj=api("actions/jobs/"+str(RETRY_JOB))
    ra=api("actions/runs/"+str(RETRY_RUN)+"/artifacts")
    v.need(retry["head_sha"]==RETRY_HEAD and retry["status"]=="completed" and retry["conclusion"]=="failure" and
           rj["head_sha"]==RETRY_HEAD and rj["run_id"]==RETRY_RUN and rj["status"]=="completed" and rj["conclusion"]=="failure" and
           any(s["name"]=="Require original R71 run absent before retry" and s["conclusion"]=="failure" for s in rj["steps"]) and
           any(s["name"]=="Install pinned Lean" and s["conclusion"]=="skipped" for s in rj["steps"]) and
           any(s["name"]=="Verify R71 registered basis path" and s["conclusion"]=="skipped" for s in rj["steps"]) and
           ra["total_count"]==0 and not ra["artifacts"],"R71 duplicate launch stopped before Lean")
    sha=r1.r63.r62.r23.sha;fail=a.r1_failure
    v.need((fail/"formal-source.lean").read_bytes()==r1.FORMAL.read_bytes() and sha(r1.FORMAL.read_bytes())==FORMAL_SHA and
           sha((fail/"registry-application.lean").read_bytes())==APP_SHA and
           sha((fail/"registry-computation.lean").read_bytes())==COMPUTE_SHA and
           sha((fail/"RecoveryDualityR62.log").read_bytes())==LOG_SHA,"R71 original source and log identity")
    log=(fail/"RecoveryDualityR62.log").read_text(encoding="utf-8")
    errors=[x for x in log.splitlines() if x.startswith("/home/") and ("error:" in x or "error(" in x or "warning:" in x)]
    v.need(len(errors)==2 and all("error: unexpected token ')'; expected ']'" in x for x in errors) and
           "3900:176:" in errors[0] and "3928:176:" in errors[1],"R71 exact parser failure")
    v.need(not any(l.startswith("KUUOS_R71_COMPUTE ") for l in log.splitlines()),"R71 failed computation inventory")
    def repaired_sources(*args):
        app,compute,items,refs=ORIGINAL(*args)
        v.need(app.encode()==(fail/"registry-application.lean").read_bytes() and
               compute.encode()==(fail/"registry-computation.lean").read_bytes() and
               compute.count(BEFORE)==2 and BEFORE.count(")")-BEFORE.count("(")==1 and
               AFTER.count(")")==AFTER.count("(") and AFTER not in compute,"R71 exact generated source and surplus parenthesis")
        changed=compute.replace(BEFORE,AFTER)
        v.need(changed.count(AFTER)==2 and changed.replace(AFTER,BEFORE)==compute,"R71 two parentheses only")
        return app,changed,items,refs
    r1.registry_sources=repaired_sources
    return log

def verify_failed_raw(log,d,out):
    marker="KUUOS_RECALL_KERNEL "
    rows=d["fresh_application"]["observations"]
    kernel=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    by={x["name"]:x for x in kernel}
    v.need(len(kernel)==len(by)==len(rows)==280 and set(by)=={x["name"] for x in rows} and
           all(set(x["expected_direct_refs"])<=set(by[x["name"]]["proof_constants"]) and
               set(by[x["name"]]["axioms"])<= {"Classical.choice","Quot.sound","propext"} for x in rows),
           "R71 R1 kernel inventory and standard axioms")
    for i,layer in ((62,r1.r63.r62.NEW),(63,r1.r63.NEW),(64,r1.r64.NEW),(65,r1.r65.NEW),
                    (66,r1.r66.NEW),(67,r1.r67.NEW),(68,r1.r68.NEW),(69,r1.r69.NEW),(70,r1.r70.NEW),(71,r1.NEW)):
        mark="KUUOS_R"+str(i)+"_RAW "
        records=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
        v.need(len(records)==len({x["name"] for x in records}) and
               {x["name"]:x for x in records}==r1.load(out/layer)["raw_theorems"],"R71 R1 exact raw replay "+str(i))


# Preserve the R2 completed direct result and the actual failed MCP response.
R2_HEAD="4b13a0a736cdcf244c85b96085cfd89369ba9a79"
R2_RUN=46112438688
R2_JOB=140878760892
R2_ART=15250985780
R2_ART_DIGEST="sha256:e399545421bcb2933666fc407c202e6650ef8394bba53cef67b1cce18d0fbda0"
R2_DIRECT="ae6b8c39e50c82d58be2ef8ad615b555d4e7f494587422fd055fa3ccf575a529"
R2_KEY="a6825ecef0a9f1b9509f32097c07d5056bcdd261b0616263aef7279249515285"
R2_DIAG_SHA="c501323231488b15faca4b5e6a6c37346c0d7ad412d11cfc48a6051a19047665"
R2_DIRECT_SHA="c89a98f3b558cb26d25e09617afef4033752f727e8ad6b40d8a9d72cc3a84954"
R2_REPAIR_SHA="12dfc390c47bc06c6074a9182dd2560779230aa3c0fea6d6e4e41a86c4c17cb1"

def bind_r2(a):
    api=v.cache.api;sha=r1.r63.r62.r23.sha
    run=api("actions/runs/"+str(R2_RUN));job=api("actions/jobs/"+str(R2_JOB))
    art=api("actions/artifacts/"+str(R2_ART))
    v.need(run["head_sha"]==R2_HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="failure" and
           job["head_sha"]==R2_HEAD and job["run_id"]==R2_RUN and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R71 R2 registered basis path" and s["status"]=="completed" and s["conclusion"]=="success" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R71 R2 new declarations and exact prior receipt reuse" and s["status"]=="completed" and
               s["conclusion"]=="failure" for s in job["steps"]),"R71 R2 direct success and actual MCP failure lineage")
    v.need(art["id"]==R2_ART and art["name"]=="codeai-olean-r71-r2-local-46112438688-1" and art["digest"]==R2_ART_DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==R2_RUN and art["workflow_run"]["head_sha"]==R2_HEAD,
           "R71 R2 exact artifact")
    p=a.r2_failure
    v.need(sha((p/"direct.json").read_bytes())==R2_DIRECT_SHA and
           sha((p/"r71-r2-repair.json").read_bytes())==R2_REPAIR_SHA and
           sha((p/"McpApplication.lean").read_bytes())==r1.R2_MCP_SOURCE_SHA and
           sha((p/"mcp-diagnostics.json").read_bytes())==R2_DIAG_SHA,"R71 R2 exact evidence bytes")
    d=r1.load(p/"direct.json")
    v.need(r1.old.digest(d)==R2_DIRECT and d["status"]=="R71_DIRECT_REGISTERED_BASIS_PATH" and d["registered_path_key"]==R2_KEY and
           len(d["fresh_application"]["observations"])==280 and
           d["fresh_application"]["mcp_source"].encode()==(p/"McpApplication.lean").read_bytes() and
           not (p/"mcp.json").exists() and not list(p.glob("mcp-verify-*.json")),"R71 R2 direct receipt; no per-declaration MCP receipt")
    raw=r1.load(p/"mcp-diagnostics.json");diag=v.structured(raw)
    v.need(raw["result"]["isError"] is False and diag["partial"] is True and diag["timed_out"] is True and
           diag["success"] is False and diag["still_elaborating_lines"]==[[3842,3842],[3849,3849],[3857,3872],[3873,3873]] and
           diag["failed_dependencies"]==[] and len(diag["items"])==28 and all(x["severity"]=="info" for x in diag["items"]),
           "R71 R2 actual incomplete full-source MCP report")
    return d,{"status":"R71_R3_MCP_TIMEOUT_REPAIR","r2_head":R2_HEAD,"r2_run":R2_RUN,"r2_job":R2_JOB,
              "r2_artifact":R2_ART,"r2_artifact_digest":R2_ART_DIGEST,"r2_direct_digest":R2_DIRECT,"r2_registered_path_key":R2_KEY,
              "r2_mcp_source_sha256":r1.R2_MCP_SOURCE_SHA,"r2_partial_diagnostic_sha256":R2_DIAG_SHA,
              "r2_partial_diagnostic_bytes":(p/"mcp-diagnostics.json").stat().st_size,
              "r2_partial":True,"r2_timed_out":True,"r2_success":False,"r2_per_declaration_mcp_audits":0,
              "r2_info_items":28,"r2_still_elaborating_lines":diag["still_elaborating_lines"],
              "r2_timeout_s":180,"r3_timeout_s_per_severity":r1.DIAG_TIMEOUT,
              "r3_client_timeout_s":r1.DIAG_CLIENT_TIMEOUT,
              "r3_diagnostic_scope":"full_source_error_and_warning","r3_info_and_hint_not_transferred":True,
              "r3_diagnostic_api_blob":r1.DIAG_API_BLOB,"r3_diagnostic_processor_blob":r1.DIAG_PROCESS_BLOB,
              "r3_exact_direct_receipt_required":True,"r2_mcp_failure_not_admitted":True}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r70-local","r70-independent","first","r1-failure","r2-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":r1.mcp(out);return
    failed_log=bind(a)
    prior,repair3=bind_r2(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    verify_failed_raw(failed_log,d,out)
    v.need((out/"formal-source.lean").read_bytes()==r1.FORMAL.read_bytes() and
           (out/"registry-application.lean").read_bytes()==(a.r1_failure/"registry-application.lean").read_bytes() and
           (out/"registry-computation.lean").read_text(encoding="utf-8").replace(AFTER,BEFORE).encode()==
               (a.r1_failure/"registry-computation.lean").read_bytes(),"R71 exact unchanged formal and application inputs")
    for name in ("historical-scope.json","script-bridge.json","script-observation-bridge-r69.json"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R71 original scope bytes "+name)
    shutil.copyfile(a.r1_failure/"registry-computation.lean",out/"registry-computation-r1.lean")
    repair={"status":"R71_R2_TWO_PARENTHESIS_COMPUTATION_REPAIR","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_formal_and_application_bytes_unchanged":True,
        "r1_all_raw_proofs_equal":True,"r1_kernel_inventory":280,"r1_computation_status":"FAILED_PARSER",
        "r2_removed_surplus_parentheses":2,"r1_computation_sha256":COMPUTE_SHA,
        "r2_computation_sha256":d["computation_source_sha256"],"duplicate_retry_run":RETRY_RUN,
        "duplicate_retry_stopped_before_lean":True,
        "repair":"remove exactly one extra closing parenthesis in each unknown_alias_tagged_accepts calculation; all assertions retained"}
    v.save(out/"r71-r2-repair.json",repair)
    print("KUUOS_R71_R2_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    v.need(d==prior and r1.old.digest(d)==R2_DIRECT,"R71 R3 unchanged successful R2 direct receipt")
    for name in ("direct.json",r1.NEW,"formal-source.lean","registry-application.lean","registry-computation.lean",
                 "registry-computation.json","registry-computation-r1.lean","r71-r2-repair.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,71))):
        v.need((out/name).read_bytes()==(a.r2_failure/name).read_bytes(),"R71 R3 exact R2 proof and calculation bytes "+name)
    repair3.update({"r2_direct_receipt_equal":True,"r2_formal_application_computation_bytes_equal":True,
                    "r2_raw_replay_bytes_equal":True})
    v.save(out/"r71-r3-repair.json",repair3)
    print("KUUOS_R71_R3_REPAIR",json.dumps(repair3,sort_keys=True),flush=True)
    if a.phase=="independent":
        for name in ("registry-computation-r1.lean","r71-r2-repair.json","r71-r3-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R71 R2 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
