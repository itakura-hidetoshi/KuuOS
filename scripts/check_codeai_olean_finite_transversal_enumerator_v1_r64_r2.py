#!/usr/bin/env python3
"""R64 R2: explicit head/tail list membership elimination; retain R1 propositions."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_finite_transversal_enumerator_v1_r64 as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_finite_transversal_enumerator_v1_r2.lean")
HEAD="aee763a31a89181539d2364de80d95787041a112"
RUN=46074784096
JOB=140759852999
ART=15234612761
DIGEST="sha256:9f39a0e28ccf0919174a3df860b3824cc329f85c4b06ada9b09397b78348dccd"
OLD_BLOCK="      simp only [List.mem_cons, List.mem_singleton] at hX\n      rcases hX with h | h\n      · subst X\n        exact ha\n      · subst X\n        exact hb"
NEW_BLOCK="      rcases List.mem_cons.mp hX with h | h\n      · subst X\n        exact ha\n      · have he : X = B := List.mem_singleton.mp h\n        subst X\n        exact hb"

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    v.need(original.count(OLD_BLOCK)==1 and repaired.count(NEW_BLOCK)==1 and
           repaired.replace(NEW_BLOCK,OLD_BLOCK)==original,"R64 R1 all propositions and other bytes retained")
    run=v.cache.api("actions/runs/"+str(RUN))
    job=v.cache.api("actions/jobs/"+str(JOB))
    art=v.cache.api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R64 finite transversal enumerator" and s["conclusion"]=="failure" for s in job["steps"]),"R64 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r64-local-46074784096-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R64 R1 artifact lineage")
    v.need((a.r1_failure/"formal-source.lean").read_bytes()==OLD.read_bytes(),"R64 R1 original source")
    r1.FORMAL=NEW

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r63-local","r63-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":
        r1.mcp(out);return
    bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes(),"R64 R2 exact source")
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    repair={"status":"R64_R2_IDENTICAL_STATEMENTS","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_propositions_unchanged":True,
        "r1_source_sha256":r1.r63.r62.r23.sha(OLD.read_bytes()),
        "r2_source_sha256":r1.r63.r62.r23.sha(NEW.read_bytes()),
        "repair":"explicit List.mem_cons.mp followed by List.mem_singleton.mp"}
    v.save(out/"r64-r2-repair.json",repair)
    print("KUUOS_R64_R2_REPAIR",repair,flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","r64-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R64 R2 repair byte identity")
        r1.independent(d,a.first,out)

if __name__=="__main__":main()
