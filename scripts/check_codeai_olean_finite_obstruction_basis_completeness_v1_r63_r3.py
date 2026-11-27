#!/usr/bin/env python3
"""R63 R2: fix strict implicit Finset subset binder, preserve every proposition."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_finite_obstruction_basis_completeness_v1_r63_r3_core as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_finite_obstruction_basis_completeness_v1_r2.lean")
R1_HEAD="6c5b78b621431850f145eaca2a5bbd2dbba9afb8"
R1_RUN=45995740432
R1_JOB=140494559600
R1_ART=15196171408
R1_DIGEST="sha256:33fdeafb31e2578318b96182566e206b7df031c05c5c29b20e797d988f9e888d"
OLD_LINE="    exact ⟨M, fun hx => ht (hmt hx), hmin⟩"
NEW_LINE="    exact ⟨M, by intro x hx; exact ht (hmt hx), hmin⟩"

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    v.need(original.count(OLD_LINE)==1 and repaired.count(NEW_LINE)==1 and
           repaired.replace(NEW_LINE,OLD_LINE)==original,"R63 R1 all statements and other proof bytes retained")
    run=v.cache.api("actions/runs/"+str(R1_RUN))
    job=v.cache.api("actions/jobs/"+str(R1_JOB))
    art=v.cache.api("actions/artifacts/"+str(R1_ART))
    v.need(run["head_sha"]==R1_HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==R1_RUN and job["head_sha"]==R1_HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R63 finite obstruction basis completeness" and s["conclusion"]=="failure" for s in job["steps"]),
           "R63 R1 failure lineage")
    v.need(art["id"]==R1_ART and art["name"]=="codeai-olean-r63-local-45995740432-1" and art["digest"]==R1_DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==R1_RUN and art["workflow_run"]["head_sha"]==R1_HEAD,
           "R63 R1 artifact lineage")
    v.need((a.r1_failure/"formal-source.lean").read_bytes()==OLD.read_bytes(),"R63 R1 formal source")
    run=v.cache.api("actions/runs/45996539807")
    job=v.cache.api("actions/jobs/140497225120")
    art=v.cache.api("actions/artifacts/15195294953")
    v.need(run["head_sha"]=="d8a7133589419b8673bfc80113b3d9e52563c1cb" and run["status"]=="completed" and
           run["conclusion"]=="failure" and run["run_attempt"]==1 and job["run_id"]==45996539807 and
           job["head_sha"]==run["head_sha"] and job["status"]=="completed" and job["conclusion"]=="failure","R63 R2 failure lineage")
    v.need(art["name"]=="codeai-olean-r63-r2-local-45996539807-1" and
           art["digest"]=="sha256:5c1516c1ad800b822ba09a8e73b8e4de09f57a24b331095fe1b59929889fa212" and not art["expired"] and
           art["workflow_run"]["id"]==45996539807 and art["workflow_run"]["head_sha"]==run["head_sha"],"R63 R2 artifact lineage")
    v.need((a.r2_failure/"formal-source.lean").read_bytes()==NEW.read_bytes() and
           (a.r2_failure/"finite-ledger.lean").read_bytes()==(a.r1_failure/"finite-ledger.lean").read_bytes(),"R63 R2 source and finite ledger identity")
    r1.FORMAL=NEW

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r62-local","r62-independent","first","r1-failure","r2-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":
        r1.mcp(out);return
    bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes() and
           (out/"finite-ledger.lean").read_bytes()==(a.r1_failure/"finite-ledger.lean").read_bytes(),
           "R63 R1 finite ledger unchanged")
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    repair={"status":"R63_R2_IDENTICAL_STATEMENTS","r1_run":R1_RUN,"r1_head":R1_HEAD,"r1_artifact":R1_ART,
        "r1_artifact_digest":R1_DIGEST,"r1_all_statements_unchanged":True,"r1_finite_ledger_bytes_equal":True,
        "r1_source_sha256":r1.r62.r23.sha(OLD.read_bytes()),"r2_source_sha256":r1.r62.r23.sha(NEW.read_bytes()),
        "repair":"explicit intro x hx for strict implicit Finset subset binder"}
    v.save(out/"r63-r2-repair.json",repair)
    print("KUUOS_R63_R2_REPAIR",repair,flush=True)
    replay={"status":"R63_R3_EXACT_PARENT_RAW_REPLAY",
        "r2_run":45996539807,"r2_artifact":15195294953,
        "r2_all_formal_bytes_unchanged":True,"r1_r2_finite_ledger_bytes_equal":True,
        "parent_module_path":"artifacts/olean-r62/RecoveryDualityR62.lean",
        "parent_raw_replay_bytewise_equal":True,
        "r63_source_sha256":r1.r62.r23.sha(NEW.read_bytes())}
    v.save(out/"r63-r3-repair.json",replay)
    print("KUUOS_R63_R3_REPAIR",replay,flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","r63-r2-repair.json","r63-r3-repair.json","parent-r62-raw-replay.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R63 R2 repair identity")
        r1.independent(d,a.first,out)

if __name__=="__main__":main()
