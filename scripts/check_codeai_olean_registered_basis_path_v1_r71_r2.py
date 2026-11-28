#!/usr/bin/env python3
"""R71 R2: remove two surplus closing parentheses in the generated computation only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registered_basis_path_v1_r71 as r1
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

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r70-local","r70-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":r1.mcp(out);return
    failed_log=bind(a)
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
    if a.phase=="independent":
        for name in ("registry-computation-r1.lean","r71-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R71 R2 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
