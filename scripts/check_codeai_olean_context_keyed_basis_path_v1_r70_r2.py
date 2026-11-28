#!/usr/bin/env python3
"""R70 R2: prove the empty key-check equivalence with the two typed directions."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_context_keyed_basis_path_v1_r70 as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_context_keyed_basis_path_v1_r2.lean")
HEAD="3a169d95c969b4572e633a219bf0e5b4236ffdc1"
RUN=46109011233
JOB=140868121127
ART=15248534397
DIGEST="sha256:92f584573cc6b7f34c015c24a91577a0801d17ad55b392deb104683cccf21405"
FORMAL_SHA="63da5b3bf4e237b638c3222dd0ccd00c470e61ab1bebe3287f02a231f94f2531"
APP_SHA="3c0228ac6ee77e6f9781cc3a0cd055589915a6ed97580bb2cfac75641fd7a31a"
COMPUTE_SHA="3146ba4f919224eabd69ef0a20a72ca2396a42e9fe834531155b0483fe9cd6bf"
BEFORE="      exact decide_eq_true_eq"
AFTER="      exact ⟨of_decide_eq_true (p := k = l), decide_eq_true (p := k = l)⟩"
STANDARD={"Classical.choice","Quot.sound","propext"}

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    v.need(original.count(BEFORE)==1 and repaired.count(AFTER)==1 and
           repaired.replace(AFTER,BEFORE)==original,"R70 R1 all original statements and other source bytes retained")
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    job=api("actions/jobs/"+str(JOB))
    art=api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R70 context keyed basis path" and s["conclusion"]=="failure" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R70 new declarations and exact prior receipt reuse" and s["conclusion"]=="skipped" for s in job["steps"]),
           "R70 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r70-local-46109011233-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R70 R1 artifact lineage")
    fail=a.r1_failure;sha=r1.r63.r62.r23.sha
    v.need((fail/"formal-source.lean").read_bytes()==OLD.read_bytes() and sha(OLD.read_bytes())==FORMAL_SHA and
           sha((fail/"keyed-application.lean").read_bytes())==APP_SHA and
           sha((fail/"keyed-computation.lean").read_bytes())==COMPUTE_SHA,"R70 R1 exact formal and computation inputs")
    log=(fail/"RecoveryDualityR62.log").read_text(encoding="utf-8")
    errors=[x for x in log.splitlines() if x.startswith("/home/") and ("error:" in x or "error(" in x or "warning:" in x)]
    v.need(len(errors)==1 and "3479:12: error: typeclass instance problem is stuck" in errors[0] and
           "Decidable ?m.25" in log,"R70 exact R1 elaboration failure")
    r1.FORMAL=NEW
    return log

def verify_failed_observations(log,d,out):
    mark="KUUOS_RECALL_KERNEL "
    kernel=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(len(kernel)==len({x["name"] for x in kernel})==263,"R70 R1 kernel inventory")
    layers=((62,r1.r63.r62.NEW),(63,r1.r63.NEW),(64,r1.r64.NEW),(65,r1.r65.NEW),
            (66,r1.r66.NEW),(67,r1.r67.NEW),(68,r1.r68.NEW),(69,r1.r69.NEW))
    for i,layer in layers:
        mark="KUUOS_R"+str(i)+"_RAW "
        obs=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
        v.need(len(obs)==len({x["name"] for x in obs}) and
               {x["name"]:x for x in obs}==r1.load(out/layer)["raw_theorems"],"R70 R1 exact prior raw replay "+str(i))
    mark="KUUOS_R70_RAW "
    records=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    by={x["name"]:x for x in records}
    current=r1.load(out/r1.NEW)["raw_theorems"]
    v.need(len(records)==len(by)==len(current)==16 and set(by)==set(current),"R70 R1 new raw inventory")
    failed=[n for n,x in by.items() if "sorryAx" in x["axioms"]]
    v.need(len(failed)==14 and "KuuOSR70.key_check_iff" in failed,"R70 R1 contamination retained as failure evidence")
    for n,x in current.items():
        v.need(x["type_expr"]==by[n]["type_expr"] and x["universe_parameters"]==by[n]["universe_parameters"] and
               set(x["axioms"])<=STANDARD and "sorryAx" not in x["proof_expr"],"R70 exact theorem type and valid R2 proof "+n)
    mark="KUUOS_R70_COMPUTE "
    computed=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(computed==d["actual_computations"] and len(computed)==2,"R70 identical observed computation outputs")
    return sorted(failed)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r69-local","r69-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":r1.mcp(out);return
    failed_log=bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    failed=verify_failed_observations(failed_log,d,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes(),"R70 R2 exact formal source")
    for name in ("keyed-application.lean","keyed-computation.lean","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R70 R1 input bytes unchanged "+name)
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    repair={"status":"R70_R2_EXACT_STATEMENTS_AND_COMPUTATIONS","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_propositions_unchanged":True,"r1_kernel_types_equal":True,
        "r1_prior_raw_replay_equal":True,"r1_computation_bytes_equal":True,"r1_actual_computations_equal":True,
        "r1_sorryAx_affected_declarations":failed,"r2_sorryAx_affected_declarations":[],
        "r1_source_sha256":FORMAL_SHA,"r2_source_sha256":d["formal_source_sha256"],
        "repair":"explicit Iff pair of of_decide_eq_true and decide_eq_true with p := k = l; preserve all audit conditions"}
    v.save(out/"r70-r2-repair.json",repair)
    print("KUUOS_R70_R2_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","r70-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R70 R2 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
