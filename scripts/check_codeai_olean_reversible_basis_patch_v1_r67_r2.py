#!/usr/bin/env python3
"""R67 R2: expose the executable condition before if_pos, without weakening any theorem."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_reversible_basis_patch_v1_r67 as r1
v=r1.v
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_reversible_basis_patch_v1_r2.lean")
HEAD="5bfe8be7483981a56634688edd4d272bc3640ab9"
RUN=46095605105
JOB=140826113199
ART=15243551679
DIGEST="sha256:002f96a23cc5b5f9d6f83d03c09a21140e090ca46d44697beebb0e54a06fec99"
CHANGES=(("  unfold checkedPatch\n  rw [if_pos (actual_patch_valid F G)]\n  exact congrArg some (apply_diff_exact F G)","  unfold checkedPatch\n  have hv : F \\ G ⊆ F ∧ ∀ x ∈ G \\ F, x ∉ F := actual_patch_valid F G\n  calc\n    _ = some (applyPatch F (F \\ G) (G \\ F)) := if_pos hv\n    _ = some G := congrArg some (apply_diff_exact F G)"),
    ("  unfold checkedPatch\n  rw [if_pos (reverse_valid F R N h)]\n  exact congrArg some (rollback_exact F R N h)","  unfold checkedPatch\n  have hv : N ⊆ applyPatch F R N ∧ ∀ x ∈ R, x ∉ applyPatch F R N :=\n    reverse_valid F R N h\n  calc\n    _ = some (applyPatch (applyPatch F R N) N R) := if_pos hv\n    _ = some F := congrArg some (rollback_exact F R N h)"),)

def bind(a):
    original=OLD.read_text(encoding="utf-8")
    repaired=NEW.read_text(encoding="utf-8")
    restored=repaired
    for old,new in reversed(CHANGES):
        v.need(original.count(old)==1 and restored.count(new)==1,"R67 R1 repair boundary")
        restored=restored.replace(new,old)
    v.need(restored==original,"R67 all original statements and other proof bytes retained")
    run=v.cache.api("actions/runs/"+str(RUN))
    job=v.cache.api("actions/jobs/"+str(JOB))
    art=v.cache.api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R67 reversible basis patch" and s["conclusion"]=="failure" for s in job["steps"]),"R67 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r67-local-46095605105-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R67 R1 artifact lineage")
    v.need((a.r1_failure/"formal-source.lean").read_bytes()==OLD.read_bytes(),"R67 R1 source bytes")
    r1.FORMAL=NEW

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r66-local","r66-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":
        r1.mcp(out);return
    bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    v.need((out/"formal-source.lean").read_bytes()==NEW.read_bytes(),"R67 R2 exact source")
    for name in ("patch-application.lean","patch-computation.lean","historical-scope.json"):
        v.need((out/name).read_bytes()==(a.r1_failure/name).read_bytes(),"R67 R1 input bytes unchanged "+name)
    shutil.copyfile(OLD,out/"formal-source-r1.lean")
    repair={"status":"R67_R2_IDENTICAL_STATEMENTS_AND_PATCH_INPUTS","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_propositions_unchanged":True,"r1_patch_input_bytes_equal":True,
        "r1_source_sha256":r1.r63.r62.r23.sha(OLD.read_bytes()),
        "r2_source_sha256":r1.r63.r62.r23.sha(NEW.read_bytes()),
        "repair":"two explicit condition witnesses and typed if_pos equalities; no required proof reference removed"}
    v.save(out/"r67-r2-repair.json",repair)
    print("KUUOS_R67_R2_REPAIR",repair,flush=True)
    if a.phase=="independent":
        for name in ("formal-source-r1.lean","r67-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R67 R2 repair byte identity")
        r1.independent(d,a.first,out)

if __name__=="__main__":main()
