#!/usr/bin/env python3
"""R73 R3: close the remaining none.bind goal with the pinned Option.bind_none."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_batch_v1_r73_r2 as r2
r1=r2.r1
v=r1.v
NEW=r2.NEW.with_name("codeai_registry_batch_v1_r3.lean")
R2_HEAD="5dc4276a836397c8535c78198e58c70dd8038e62"
R2_RUN=46119424704
R2_JOB=140900416395
R2_ART=15252819695
R2_DIGEST="sha256:95d041b30d5590d42ba055d70c4a24735bcaa172265423e586abb88ec9031708"
R2_FORMAL_SHA="5bb3d504667943ecc54acbdada0982e2eaeda9dcd9f29bc3a6f48c5c7ee28d18"
R2_APP_SHA="9684a1ec41d2a692bbb7d3c3aab9f2bab8c743f54d9619655f439a4984106ca5"
R2_COMPUTE_SHA="ac23992bfb45b69c9b19d068b22c437d8fd71d4d49092982901df818c4e43f2f"
R2_LOG_SHA="6ff4f743b7f20a8e279a061f2dd4b93efd830913e91794665767f22d4497337e"
BEFORE="          rw [hl, hr]\n      | some mid =>"
AFTER="          rw [hl, hr]\n          exact (Option.bind_none (fun mid : κ → Option (Basis α) => checkedBatch mid ys)).symm\n      | some mid =>"
FAILED_NAME="KuuOSR73.checked_batch_append"
STANDARD={"Classical.choice","Quot.sound","propext"}
OPTION_BASIC_BLOB="707348ca449af4fadbc6ead40d6ad9f76c468bcd"

def bind_r2(a):
    old_source=r2.NEW.read_text(encoding="utf-8")
    new_source=NEW.read_text(encoding="utf-8")
    v.need(old_source.count(BEFORE)==1 and new_source.count(AFTER)==1 and
           new_source.replace(AFTER,BEFORE)==old_source,"R73 R3 exact one-line repair and all propositions unchanged")
    api=v.cache.api
    run=api("actions/runs/"+str(R2_RUN));job=api("actions/jobs/"+str(R2_JOB))
    art=api("actions/artifacts/"+str(R2_ART))
    v.need(run["id"]==R2_RUN and run["head_sha"]==R2_HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="failure" and
           job["head_sha"]==R2_HEAD and job["run_id"]==R2_RUN and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R73 R2 registry batch" and s["conclusion"]=="failure" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R73 R2 new declarations and exact prior receipt reuse" and s["conclusion"]=="skipped" for s in job["steps"]),
           "R73 R2 failure lineage")
    v.need(art["id"]==R2_ART and art["name"]=="codeai-olean-r73-r2-local-46119424704-1" and art["digest"]==R2_DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==R2_RUN and art["workflow_run"]["head_sha"]==R2_HEAD,"R73 R2 artifact identity")
    p=a.r2_failure;sha=r1.r63.r62.r23.sha
    v.need((p/"formal-source.lean").read_bytes()==r2.NEW.read_bytes() and sha(r2.NEW.read_bytes())==R2_FORMAL_SHA and
           sha((p/"batch-application.lean").read_bytes())==R2_APP_SHA and
           sha((p/"batch-computation.lean").read_bytes())==R2_COMPUTE_SHA and
           sha((p/"RecoveryDualityR62.log").read_bytes())==R2_LOG_SHA and
           not (p/"direct.json").exists(),"R73 R2 exact sources and failed direct log")
    log=(p/"RecoveryDualityR62.log").read_text(encoding="utf-8")
    errors=[l for l in log.splitlines() if l.startswith("/home/") and ("error:" in l or "error(" in l or "warning:" in l)]
    v.need(len(errors)==1 and "4155:13: error: unsolved goals" in errors[0] and
           "case cons.none" in log and "⊢ none = none.bind fun mid => checkedBatch mid ys" in log,
           "R73 R2 observed single unresolved none.bind goal")
    r1.FORMAL=NEW
    return log

def verify_r2(log,d,out):
    marker="KUUOS_RECALL_KERNEL "
    old_rows=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    by={x["name"]:x for x in old_rows};rows=d["fresh_application"]["observations"]
    v.need(len(old_rows)==len(by)==len(rows)==313 and set(by)=={x["name"] for x in rows},"R73 R2 exact kernel inventory")
    layers=((62,r1.r63.r62.NEW),(63,r1.r63.NEW),(64,r1.r64.NEW),(65,r1.r65.NEW),
            (66,r1.r66.NEW),(67,r1.r67.NEW),(68,r1.r68.NEW),(69,r1.r69.NEW),(70,r1.r70.NEW),
            (71,r1.r71.NEW),(72,r1.r72.NEW))
    for i,layer in layers:
        mark="KUUOS_R"+str(i)+"_RAW "
        records=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
        v.need(len(records)==len({x["name"] for x in records}) and
               {x["name"]:x for x in records}==r1.load(out/layer)["raw_theorems"],"R73 R2 prior exact raw replay "+str(i))
    mark="KUUOS_R73_RAW "
    records=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    prior={x["name"]:x for x in records};current=r1.load(out/r1.NEW)["raw_theorems"]
    v.need(len(records)==len(prior)==len(current)==16 and set(prior)==set(current),"R73 R2 raw inventory")
    failed={n for n,x in prior.items() if "sorryAx" in x["proof_expr"] or "sorryAx" in x["type_expr"] or "sorryAx" in x["axioms"]}
    v.need(failed=={FAILED_NAME} and all("sorryAx" not in x["type_expr"] for x in prior.values()),"R73 R2 single proof failure, all types elaborated")
    for n,x in current.items():
        v.need(x["type_expr"]==prior[n]["type_expr"] and x["universe_parameters"]==prior[n]["universe_parameters"] and
               "sorryAx" not in x["type_expr"] and "sorryAx" not in x["proof_expr"] and set(x["axioms"])<=STANDARD,
               "R73 R3 all R2 types preserved and proof valid "+n)
        if n!=FAILED_NAME:
            v.need(x==prior[n],"R73 unchanged complete R2 raw proof "+n)
    mark="KUUOS_R73_COMPUTE "
    computed=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(computed==d["actual_computations"] and len(computed)==2,"R73 exact R2 computation results")
    return sorted(failed)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r72-local","r72-independent","first","r1-failure","r2-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":r1.mcp(out);return
    # R2's exact R1 source repair, diagnostics and complete provenance checks.
    log1=r2.bind(a)
    log2=bind_r2(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    failed1,type_failed1=r2.verify_failed_observations(log1,d,out)
    failed2=verify_r2(log2,d,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes() and
           (out/"formal-source.lean").read_text(encoding="utf-8").replace(AFTER,BEFORE).replace(r2.AFTER,r2.BEFORE).encode()==
             (a.r1_failure/"formal-source.lean").read_bytes(),"R73 exact R1 to R2 to R3 source proof repair chain")
    for name in ("batch-application.lean","batch-computation.lean","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json"):
        v.need((out/name).read_bytes()==(a.r2_failure/name).read_bytes(),"R73 exact R2 application and computation bytes "+name)
    for name in ("batch-computation.lean","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R73 exact R1 computation and scope bytes "+name)
    v.need((out/"batch-application.lean").read_text(encoding="utf-8").replace(r2.NEW_SUFFIX,r2.OLD_SUFFIX).replace(
        r2.OPTIONS+"theorem actual_batch_duplicate_hold_","theorem actual_batch_duplicate_hold_").encode()==
        (a.r1_failure/"batch-application.lean").read_bytes(),"R73 exact R1 application propositions")
    shutil.copyfile(r2.OLD,out/"formal-source-r1.lean")
    shutil.copyfile(r2.NEW,out/"formal-source-r2.lean")
    shutil.copyfile(a.r1_failure/"batch-application.lean",out/"batch-application-r1.lean")
    repair={"status":"R73_R3_EXPLICIT_NONE_BIND",
        "r1_run":r2.RUN,"r1_head":r2.HEAD,"r1_artifact":r2.ART,"r1_artifact_digest":r2.DIGEST,
        "r2_run":R2_RUN,"r2_head":R2_HEAD,"r2_artifact":R2_ART,"r2_artifact_digest":R2_DIGEST,
        "r1_source_sha256":r2.FORMAL_SHA,"r2_source_sha256":R2_FORMAL_SHA,"r3_source_sha256":d["formal_source_sha256"],
        "r2_application_sha256":R2_APP_SHA,"r2_computation_sha256":R2_COMPUTE_SHA,
        "all_source_propositions_unchanged":True,"r1_previously_elaborated_types_equal":14,
        "r1_type_elaboration_failed":type_failed1,"r1_sorryAx_affected_declarations":failed1,
        "r2_sorryAx_affected_declarations":failed2,"r2_all_types_equal":True,
        "r2_unchanged_raw_proofs":15,"r3_sorryAx_affected_declarations":[],
        "r1_r2_prior_raw_replay_equal":True,"r1_r2_computation_bytes_equal":True,
        "r1_r2_actual_computations_equal":True,"pinned_option_basic_blob":OPTION_BASIC_BLOB,
        "repair":"close only the none.bind branch using the symmetric pinned Option.bind_none theorem; preserve R2 duplicate proof repair"}
    v.save(out/"r73-r3-repair.json",repair)
    print("KUUOS_R73_R3_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","formal-source-r2.lean","batch-application-r1.lean","r73-r3-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R73 R3 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
