#!/usr/bin/env python3
"""R73 R2: restrict recursive unfolding and avoid simp over large basis values."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_batch_v1_r73 as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_registry_batch_v1_r2.lean")
HEAD="4f8212827143d6a4def93f16b5994aaf8b63b863"
RUN=46118653890
JOB=140898033012
ART=15251994848
DIGEST="sha256:6add6ab271a196aae1a9209916d8a841dfafcefcb9426bdf3a90da34105df02f"
FORMAL_SHA="47ff8b00c27122104b09c0c443dccc7b628eac7511211ef58322600aac16ea08"
APP_SHA="7e98b2b50e17940ece011b6b8363faafbde9586beea2f1fa33ea4da88008826a"
COMPUTE_SHA="ac23992bfb45b69c9b19d068b22c437d8fd71d4d49092982901df818c4e43f2f"
LOG_SHA="05e6ef663f5a87dd9ce4d44ff3e3c451128aba96ed333e7c6c8d54a4fa8beb3b"
BEFORE="      change (match checkedInsert reg a.1 a.2 with\n        | none => none\n        | some mid => checkedBatch mid (tail ++ ys)) =\n        (checkedBatch reg (a :: tail)).bind (fun mid => checkedBatch mid ys)\n      unfold checkedBatch\n      cases hm : checkedInsert reg a.1 a.2 with\n      | none => rfl\n      | some mid => exact ih mid"
AFTER="      change checkedBatch reg (a :: (tail ++ ys)) =\n        (checkedBatch reg (a :: tail)).bind (fun mid => checkedBatch mid ys)\n      cases hm : checkedInsert reg a.1 a.2 with\n      | none =>\n          have hl : checkedBatch reg (a :: (tail ++ ys)) = none := by\n            rw [checkedBatch, hm]\n          have hr : checkedBatch reg (a :: tail) = none := by\n            rw [checkedBatch, hm]\n          rw [hl, hr]\n      | some mid =>\n          have hl : checkedBatch reg (a :: (tail ++ ys)) = checkedBatch mid (tail ++ ys) := by\n            rw [checkedBatch, hm]\n          have hr : checkedBatch reg (a :: tail) = checkedBatch mid tail := by\n            rw [checkedBatch, hm]\n          rw [hl, hr]\n          exact ih mid"
OLD_SUFFIX=" (by simp) rfl"
NEW_SUFFIX=" (List.mem_cons_self) rfl"
OPTIONS="set_option maxRecDepth 16384 in\nset_option maxHeartbeats 12000000 in\n"
ORIGINAL=r1.batch_sources
FAILED={"KuuOSR73.checked_batch_append","KuuOSR73.actual_batch_duplicate_hold_0","KuuOSR73.actual_batch_duplicate_hold_1"}
TYPE_FAILED={"KuuOSR73.actual_batch_duplicate_hold_0","KuuOSR73.actual_batch_duplicate_hold_1"}

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    v.need(original.count(BEFORE)==1 and repaired.count(AFTER)==1 and
           repaired.replace(AFTER,BEFORE)==original,"R73 exact general theorem statement and other proof source identity")
    api=v.cache.api
    run=api("actions/runs/"+str(RUN));job=api("actions/jobs/"+str(JOB))
    art=api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="failure" and
           job["head_sha"]==HEAD and job["run_id"]==RUN and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R73 registry batch" and s["conclusion"]=="failure" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R73 new declarations and exact prior receipt reuse" and s["conclusion"]=="skipped" for s in job["steps"]),
           "R73 original failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r73-local-46118653890-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,
           "R73 exact original artifact")
    fail=a.r1_failure;sha=r1.r63.r62.r23.sha
    v.need((fail/"formal-source.lean").read_bytes()==OLD.read_bytes() and sha(OLD.read_bytes())==FORMAL_SHA and
           sha((fail/"batch-application.lean").read_bytes())==APP_SHA and
           sha((fail/"batch-computation.lean").read_bytes())==COMPUTE_SHA and
           sha((fail/"RecoveryDualityR62.log").read_bytes())==LOG_SHA,"R73 original exact sources and log")
    log=(fail/"RecoveryDualityR62.log").read_text(encoding="utf-8")
    errors=[x for x in log.splitlines() if x.startswith("/home/") and ("error:" in x or "error(" in x or "warning:" in x)]
    v.need(len(errors)==3 and "4159:20: error: Type mismatch" in errors[0] and
           "4206:0: error: maximum recursion depth has been reached" in errors[1] and
           "4218:0: error: maximum recursion depth has been reached" in errors[2],"R73 exact observed diagnostics")
    def repaired_sources(*args):
        app,compute,items,refs=ORIGINAL(*args)
        v.need(app.encode()==(fail/"batch-application.lean").read_bytes() and
               compute.encode()==(fail/"batch-computation.lean").read_bytes() and app.count(OLD_SUFFIX)==2 and
               app.count("theorem actual_batch_duplicate_hold_")==2,"R73 exact generated inputs")
        changed=app.replace(OLD_SUFFIX,NEW_SUFFIX).replace("theorem actual_batch_duplicate_hold_",OPTIONS+"theorem actual_batch_duplicate_hold_")
        v.need(changed.count(NEW_SUFFIX)==2 and changed.count(OPTIONS+"theorem actual_batch_duplicate_hold_")==2 and
               changed.replace(NEW_SUFFIX,OLD_SUFFIX).replace(OPTIONS+"theorem actual_batch_duplicate_hold_","theorem actual_batch_duplicate_hold_")==app,
               "R73 only duplicate proof terms and local options changed")
        return changed,compute,items,refs
    r1.FORMAL=NEW
    r1.batch_sources=repaired_sources
    return log

def verify_failed_observations(log,d,out):
    mark="KUUOS_RECALL_KERNEL "
    kernel=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(len(kernel)==len({x["name"] for x in kernel})==313,"R73 original kernel inventory")
    layers=((62,r1.r63.r62.NEW),(63,r1.r63.NEW),(64,r1.r64.NEW),(65,r1.r65.NEW),(66,r1.r66.NEW),
            (67,r1.r67.NEW),(68,r1.r68.NEW),(69,r1.r69.NEW),(70,r1.r70.NEW),(71,r1.r71.NEW),(72,r1.r72.NEW))
    for i,layer in layers:
        mark="KUUOS_R"+str(i)+"_RAW "
        obs=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
        v.need(len(obs)==len({x["name"]:x for x in obs}) and
               {x["name"]:x for x in obs}==r1.load(out/layer)["raw_theorems"],"R73 original prior raw equality "+str(i))
    mark="KUUOS_R73_RAW "
    records=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    by={x["name"]:x for x in records};current=r1.load(out/r1.NEW)["raw_theorems"]
    v.need(len(records)==len(by)==len(current)==16 and set(by)==set(current),"R73 original new raw inventory")
    failed={n for n,x in by.items() if "sorryAx" in x["proof_expr"] or "sorryAx" in x["type_expr"] or "sorryAx" in x["axioms"]}
    type_failed={n for n,x in by.items() if "sorryAx" in x["type_expr"]}
    v.need(failed==FAILED and type_failed==TYPE_FAILED,"R73 preserve failed elaboration evidence, not false successful types")
    for n,x in current.items():
        v.need("sorryAx" not in x["type_expr"] and "sorryAx" not in x["proof_expr"] and
               not set(x["axioms"])-{"Classical.choice","Quot.sound","propext"},"R73 valid repaired theorem "+n)
        if n not in TYPE_FAILED:
            v.need(x["type_expr"]==by[n]["type_expr"] and x["universe_parameters"]==by[n]["universe_parameters"],
                   "R73 exact previously elaborated type "+n)
    mark="KUUOS_R73_COMPUTE "
    computed=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(computed==d["actual_computations"] and len(computed)==2,"R73 exact original computation outputs")
    return sorted(failed),sorted(type_failed)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r72-local","r72-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":r1.mcp(out);return
    failed_log=bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    failed,type_failed=verify_failed_observations(failed_log,d,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes() and
           (out/"batch-application.lean").read_text(encoding="utf-8").replace(NEW_SUFFIX,OLD_SUFFIX).replace(
               OPTIONS+"theorem actual_batch_duplicate_hold_","theorem actual_batch_duplicate_hold_").encode()==
               (a.r1_failure/"batch-application.lean").read_bytes(),"R73 unchanged source propositions")
    for name in ("batch-computation.lean","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R73 original computation and scope bytes "+name)
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    shutil.copyfile(a.r1_failure/"batch-application.lean",out/"batch-application-r1.lean")
    repair={"status":"R73_R2_ONE_STEP_RECURSION_AND_EXPLICIT_MEMBERSHIP",
        "r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,"r1_artifact_digest":DIGEST,
        "r1_source_sha256":FORMAL_SHA,"r2_source_sha256":d["formal_source_sha256"],
        "r1_application_sha256":APP_SHA,"r2_application_sha256":d["application_source_sha256"],
        "all_source_propositions_unchanged":True,"r1_previously_elaborated_types_equal":14,
        "r1_type_elaboration_failed":type_failed,"r1_sorryAx_affected_declarations":failed,
        "r2_sorryAx_affected_declarations":[],"r1_prior_raw_replay_equal":True,
        "r1_computation_bytes_equal":True,"r1_actual_computations_equal":True,
        "repair":"use explicit checkedBatch one-step equations for append; List.mem_cons_self for concrete duplicate membership; local recursion options only for two duplicate declarations"}
    v.save(out/"r73-r2-repair.json",repair)
    print("KUUOS_R73_R2_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","batch-application-r1.lean","r73-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R73 R2 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
