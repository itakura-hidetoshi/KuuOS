#!/usr/bin/env python3
"""R65 R2: retain direct certified pair-cut reference; preserve R1 propositions and computations."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_incremental_transversal_ledger_v1_r65 as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_incremental_transversal_ledger_v1_r2.lean")
HEAD="32aef41d17cf6e308ed454e99502dab0e76eaa45"
RUN=46081554510
JOB=140781458865
ART=15237093974
DIGEST="sha256:1ce4919cea73552e47645ec66251c72b013c38fbb4d3b29f8406665c5ac97397"
OLD_BLOCK="  simp only [List.mem_toFinset, mem_pair_cut, Finset.mem_insert, Finset.mem_singleton]"
NEW_BLOCK="  have hl : z ∈ (pairCut x y).toFinset ↔ z = x ∨ z = y :=\n    List.mem_toFinset.trans (mem_pair_cut x y z)\n  have hr : z ∈ ({x, y} : Finset Nat) ↔ z = x ∨ z = y :=\n    Finset.mem_insert.trans (or_congr Iff.rfl Finset.mem_singleton)\n  exact hl.trans hr.symm"

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    v.need(original.count(OLD_BLOCK)==1 and repaired.count(NEW_BLOCK)==1 and
           repaired.replace(NEW_BLOCK,OLD_BLOCK)==original,"R65 R1 all propositions and other bytes retained")
    run=v.cache.api("actions/runs/"+str(RUN))
    job=v.cache.api("actions/jobs/"+str(JOB))
    art=v.cache.api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R65 incremental transversal ledger" and s["conclusion"]=="failure" for s in job["steps"]),"R65 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r65-local-46081554510-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R65 R1 artifact lineage")
    v.need((a.r1_failure/"formal-source.lean").read_bytes()==OLD.read_bytes(),"R65 R1 original source")
    lines=(a.r1_failure/"RecoveryDualityR62.log").read_text(encoding="utf-8").splitlines()
    prefix="KUUOS_RECALL_KERNEL "
    observed=[json.loads(x[len(prefix):]) for x in lines if x.startswith(prefix)]
    by={x["name"]:x for x in observed}
    v.need(len(observed)==len(by)==182,"R65 R1 kernel inventory")
    parent=r1.load(a.r1_failure/"parent-r64-receipts"/"direct.json")
    v.need(r1.old.digest(parent)==r1.DIRECT,"R65 R1 parent receipt")
    ledger=r1.load(a.r1_failure/r1.r63.NEW)
    v.need(ledger["key"]==r1.r64.KEY,"R65 R1 parent ledger")
    _,_,items,refs=r1.ledger_source(ledger)
    expected={x["name"]:x["expected_direct_refs"] for x in parent["fresh_application"]["observations"]}
    expected.update({r1.NS+n:r1.REFS.get(n,[]) for n in r1.GENERAL})
    expected.update(refs)
    v.need(set(expected)==set(by),"R65 R1 audit inventory")
    missing={n:sorted(set(rs)-set(by[n]["proof_constants"])) for n,rs in expected.items() if set(rs)-set(by[n]["proof_constants"])}
    v.need(missing=={"KuuOSR65.pair_list_to_finset":["KuuOSR63.mem_pair_cut"]},"R65 R1 exact missing direct reference")
    marker="KUUOS_R65_COMPUTE "
    computations=[json.loads(x[len(marker):]) for x in lines if x.startswith(marker)]
    v.need(len(computations)==7 and all(x["exact"] is True and x["expected"]==x["observed"] for x in computations) and
           sum(x["observed"] for x in computations)==1856,"R65 R1 actual computation record")
    r1.FORMAL=NEW
    return missing,computations

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r64-local","r64-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":
        r1.mcp(out);return
    missing,computations=bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes() and
           d["actual_computations"]==computations,"R65 R2 exact source and unchanged actual computation")
    for name in ("ledger-application.lean","ledger-computation.lean"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R65 R1 ledger source unchanged "+name)
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    repair={"status":"R65_R2_IDENTICAL_STATEMENTS_AND_LEDGER_COMPUTATION","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_propositions_unchanged":True,"r1_ledger_source_bytes_equal":True,
        "r1_actual_computations_equal":True,"r1_missing_direct_refs":missing,
        "r1_source_sha256":r1.r63.r62.r23.sha(OLD.read_bytes()),
        "r2_source_sha256":r1.r63.r62.r23.sha(NEW.read_bytes()),
        "repair":"explicit Iff.trans of List.mem_toFinset and KuuOSR63.mem_pair_cut; keep exact direct-reference gate"}
    v.save(out/"r65-r2-repair.json",repair)
    print("KUUOS_R65_R2_REPAIR",repair,flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","r65-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R65 R2 repair byte identity")
        r1.independent(d,a.first,out)

if __name__=="__main__":main()
