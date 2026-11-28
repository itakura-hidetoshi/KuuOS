#!/usr/bin/env python3
"""R75 R2: avoid the reserved partial token and expose exact direct proof
references in two Iff proofs. Preserve the imported certified parent.
No failure receipt or source proposition is rewritten."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_recovery_v1_r75 as r1
v=r1.v
sha=r1.sha
digest=r1.digest
load=r1.load
OLD=r1.FORMAL
NEW=OLD.with_name("codeai_registry_recovery_v1_r2.lean")
HEAD="958ad512f91792666c5dc261650224f4edc44d54"
RUN=46136975850
JOB=140954336648
ART=15260197350
ART_DIGEST="sha256:98ee24f38e56189bdb5ba902713c987730d3279cb35dbbfe6e7622a67858041c"
OLD_FORMAL="6410723cf746b8463b1a77064125ccd879f1ec7c3ca9b22b5aa1ba813344e0fc"
OLD_APP="3127c080278b6567f672dc8b8fb36c9010ee3946524259b04b2c890a90745b5f"
OLD_COMPUTE="1575e8e45d45c60d29eac5f4dbf81d09fe9f0960bd06af61b1a3ed50ea1642aa"
OLD_SOURCE="c1f290119a955df443c96f7b7e295799c95c421ac559fd0696e81554fa7c25b3"
OLD_LOG="8dd877817440db4b7f47c7503578320785db5035a07db09778694ab42a7c83eb"
NEW_FORMAL="1dba6076b71be986d912b3e9aa1320282117b5cd05489d9862e3d49b95cc54c4"
NEW_COMPUTE="838c3c6dd42ed59580e4bb1652b3e631122d17a220f751988a5bd0a706b014a3"
NEW_SOURCE="5475b43a251e84c94ede759ea05fdd9f73a2689bc6e3df40781099935962f117"
PARSER_BLOB="9b8d6b4eb39a611ffd3b9db0f9d17b1e7f653f70"
REPAIR="r75-r2-repair.json"
BEFORE1="      simp only [covers_cons, ih]"
AFTER1="      have hs := covers_cons reg (s.sourceKey,s.patch.source)\n        ((s.targetKey,s.patch.target) :: StepRequirements tail)\n      have ht := covers_cons reg (s.targetKey,s.patch.target) (StepRequirements tail)\n      constructor\n      · intro h\n        obtain ⟨hsource, hrest⟩ := hs.mp h\n        obtain ⟨htarget, htail⟩ := ht.mp hrest\n        exact ⟨hsource, htarget, ih.mp htail⟩\n      · intro h\n        exact hs.mpr ⟨h.1, ht.mpr ⟨h.2.1, ih.mpr h.2.2⟩⟩"
BEFORE2="  unfold RequiredBindings RegistryValid\n  simp only [covers_cons, step_requirements_iff]"
AFTER2="  change CoversBindings reg ((k,F) :: (l,H) :: StepRequirements path) ↔\n    reg k = some F ∧ reg l = some H ∧ RegisteredSteps reg path\n  have hk := covers_cons reg (k,F) ((l,H) :: StepRequirements path)\n  have hl := covers_cons reg (l,H) (StepRequirements path)\n  have hp := step_requirements_iff reg path\n  constructor\n  · intro h\n    obtain ⟨hsource, hrest⟩ := hk.mp h\n    obtain ⟨htarget, htail⟩ := hl.mp hrest\n    exact ⟨hsource, htarget, hp.mp htail⟩\n  · intro h\n    exact hk.mpr ⟨h.1, hl.mpr ⟨h.2.1, hp.mpr h.2.2⟩⟩"
CHANGED={"KuuOSR75.step_requirements_iff","KuuOSR75.required_bindings_iff"}
MISSING={
    "KuuOSR75.step_requirements_iff":{"KuuOSR75.covers_cons"},
    "KuuOSR75.required_bindings_iff":{"KuuOSR75.covers_cons","KuuOSR75.step_requirements_iff"},
}
STANDARD={"Classical.choice","Quot.sound","propext"}
ORIGINAL_SOURCES=r1.recovery_sources
ORIGINAL_RUN=r1.r63.r62.r23.run_lean
SOURCE_REPAIRS=("formal-source-r1.lean","recovery-computation-r1.lean",
                "RegistryRecoveryR75-r1.lean","RegistryRecoveryR75-r1.log")

def rows(log,marker):
    items=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    by={x["name"]:x for x in items}
    v.need(len(items)==len(by)==17,"R75 R2 exact declaration inventory "+marker)
    return by

def bind_failure(a):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN));job=api("actions/jobs/"+str(JOB));art=api("actions/artifacts/"+str(ART))
    v.need(run["id"]==RUN and run["head_sha"]==HEAD and run["run_attempt"]==1 and
           run["status"]=="completed" and run["conclusion"]=="failure" and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R75 registry recovery obligations" and s["status"]=="completed" and s["conclusion"]=="failure" for s in job["steps"]) and
           any(s["name"]=="Actual Lean MCP R75 new declarations and exact prior receipt reuse" and s["conclusion"]=="skipped" for s in job["steps"]),
           "R75 R1 failed computation lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r75-local-46136975850-1" and
           art["digest"]==ART_DIGEST and not art["expired"] and
           art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,
           "R75 exact failed artifact")
    p=a.r1_failure
    for name,expected in (("formal-source.lean",OLD_FORMAL),("recovery-application.lean",OLD_APP),
                          ("recovery-computation.lean",OLD_COMPUTE),(r1.SOURCE,OLD_SOURCE),
                          ("RegistryRecoveryR75.log",OLD_LOG),
                          (r1.PARENT_CAP/"RecoveryDualityR62.olean" if isinstance(r1.PARENT_CAP,Path)
                           else r1.PARENT_CAP+"/RecoveryDualityR62.olean",r1.PARENT_OLEAN)):
        v.need(sha((p/name).read_bytes())==expected,"R75 R1 exact input or output "+str(name))
    v.need(not (p/"direct.json").exists() and not (p/"mcp.json").exists() and
           not list((p/r1.CAP).glob("*.olean")),"R75 failed delta not admitted")
    old=OLD.read_text(encoding="utf-8");new=NEW.read_text(encoding="utf-8")
    v.need(sha(old.encode())==OLD_FORMAL and sha(new.encode())==NEW_FORMAL and
           old.encode()==(p/"formal-source.lean").read_bytes() and
           old.count(BEFORE1)==old.count(BEFORE2)==new.count(AFTER1)==new.count(AFTER2)==1 and
           new.replace(AFTER1,BEFORE1).replace(AFTER2,BEFORE2)==old,
           "R75 only two proof bodies changed, no statement changes")
    log=(p/"RegistryRecoveryR75.log").read_text(encoding="utf-8")
    errors=[l for l in log.splitlines() if l.startswith("/home/") and re.search(r"error[:(]|warning:",l)]
    v.need(len(errors)==10 and
           sum("unexpected token 'partial'" in l for l in errors)==2 and
           any(":230:5: error:" in l for l in errors) and any(":266:5: error:" in l for l in errors) and
           not any(l.startswith("KUUOS_R75_COMPUTE ") for l in log.splitlines()),"R75 exact observed parser failure")
    k=rows(log,"KUUOS_RECALL_KERNEL ");raw=rows(log,"KUUOS_R75_RAW ")
    v.need(set(k)==set(raw) and CHANGED<=set(k),"R75 R1 proof names")
    for n,x in raw.items():
        y=k[n]
        v.need(x["type_expr"]==y["type_expr_repr"] and x["universe_parameters"]==y["universe_parameters"] and
               bool(x["proof_expr"]) and "sorryAx" not in x["type_expr"] and "sorryAx" not in x["proof_expr"] and
               set(x["axioms"])==set(y["axioms"]) and set(x["axioms"])<=STANDARD,"R75 R1 local proof evidence "+n)
    for n in CHANGED:
        v.need(any(t.startswith(n+"._simp_") for t in k[n]["proof_constants"]),"R75 observed auxiliary simp proof "+n)
    return k,raw

def direct(a,out):
    k,prior=bind_failure(a)
    fail=a.r1_failure
    def fixed_sources(*args):
        app,compute,items,refs=ORIGINAL_SOURCES(*args)
        v.need(app.encode()==(fail/"recovery-application.lean").read_bytes() and
               compute.encode()==(fail/"recovery-computation.lean").read_bytes(),
               "R75 exact failed source generator outputs")
        expected={r1.NS+n:r1.REFS.get(n,[]) for n in r1.GENERAL};expected.update(refs)
        v.need(set(expected)==set(k),"R75 exact required reference inventory")
        missing={n:set(rs)-set(k[n]["proof_constants"]) for n,rs in expected.items()
                 if set(rs)-set(k[n]["proof_constants"])}
        v.need(missing==MISSING,"R75 exact additional direct dependency obstruction")
        v.need(len(re.findall(r"\bpartial\b",compute))==6,"R75 exact reserved token occurrences")
        fixed=re.sub(r"\bpartial\b","partialBatch",compute)
        v.need(sha(fixed.encode())==NEW_COMPUTE and re.sub(r"\bpartialBatch\b","partial",fixed)==compute,
               "R75 computation variable rename only")
        return app,fixed,items,refs
    calls=0
    def checked_run(args,path,src):
        nonlocal calls
        if path==out/r1.SOURCE:
            v.need(calls==0 and sha(src.encode())==NEW_SOURCE and
                   src.replace(NEW.read_text(encoding="utf-8"),OLD.read_text(encoding="utf-8"),1)
                      .replace(re.sub(r"\bpartial\b","partialBatch",(fail/"recovery-computation.lean").read_text(encoding="utf-8")),
                               (fail/"recovery-computation.lean").read_text(encoding="utf-8"),1).encode()==
                        (fail/r1.SOURCE).read_bytes(),"R75 exact source reverse repair")
            calls+=1
        return ORIGINAL_RUN(args,path,src)
    r1.FORMAL=NEW
    r1.recovery_sources=fixed_sources
    r1.r63.r62.r23.run_lean=checked_run
    try:
        d=r1.direct(a,out)
    finally:
        r1.FORMAL=OLD;r1.recovery_sources=ORIGINAL_SOURCES
        r1.r63.r62.r23.run_lean=ORIGINAL_RUN
    v.need(calls==1 and d["parent_source_recompiled"] is False and d["delta_compilation_count"]==1 and
           d["delta_source_sha256"]==NEW_SOURCE and d["formal_source_sha256"]==NEW_FORMAL and
           d["application_source_sha256"]==OLD_APP and d["computation_source_sha256"]==NEW_COMPUTE,
           "R75 only one delta compilation")
    current=load(out/r1.NEW)["raw_theorems"]
    actual={x["name"]:x for x in d["fresh_application"]["observations"]}
    v.need(set(current)==set(prior) and len(current)==17 and len(actual)==344,"R75 new and cumulative inventory")
    for n,x in current.items():
        old=prior[n]
        v.need(x["type_expr"]==old["type_expr"] and x["universe_parameters"]==old["universe_parameters"] and
               set(x["axioms"])<=set(old["axioms"]) and "sorryAx" not in x["type_expr"] and "sorryAx" not in x["proof_expr"],
               "R75 unchanged theorem type and no increased axioms "+n)
        if n not in CHANGED:
            v.need(x["proof_expr"]==old["proof_expr"],"R75 unchanged prior full proof expression "+n)
        else:
            v.need(MISSING[n]<=set(actual[n]["proof_constants"]),"R75 restored explicit direct references "+n)
    for name in r1.FILES+("historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                         "recovery-application.lean",*r1.HIST_RAW):
        v.need((out/name).read_bytes()==(fail/name).read_bytes(),"R75 preserved parent byte evidence "+name)
    v.need((out/r1.PARENT_CAP/"RecoveryDualityR62.olean").read_bytes()==(fail/r1.PARENT_CAP/"RecoveryDualityR62.olean").read_bytes(),
           "R75 unchanged certified parent olean")
    for name,origin in zip(SOURCE_REPAIRS,("formal-source.lean","recovery-computation.lean",r1.SOURCE,"RegistryRecoveryR75.log")):
        shutil.copyfile(fail/origin,out/name)
    repair={"status":"R75_R2_RESERVED_TOKEN_AND_EXPLICIT_DIRECT_REFERENCES","r1_run":RUN,"r1_head":HEAD,"r1_job":JOB,
            "r1_artifact":ART,"r1_artifact_digest":ART_DIGEST,"r1_log_sha256":OLD_LOG,
            "r1_parser_diagnostics":10,"r1_reserved_token_occurrences":6,"r1_compute_rows":0,
            "r1_new_raw_theorems":17,"r1_nonstandard_axioms":0,"r1_sorryAx_affected_theorems":[],
            "r1_missing_direct_refs":{n:sorted(x) for n,x in MISSING.items()},
            "r1_source_sha256":OLD_SOURCE,"r2_source_sha256":NEW_SOURCE,"r1_formal_sha256":OLD_FORMAL,
            "r2_formal_sha256":NEW_FORMAL,"r1_computation_sha256":OLD_COMPUTE,"r2_computation_sha256":NEW_COMPUTE,
            "all_source_propositions_unchanged":True,"all_17_raw_types_equal":True,"unchanged_full_proof_expressions":15,
            "repaired_direct_reference_theorems":sorted(CHANGED),"direct_dependency_requirements_unchanged":True,
            "axiom_sets_not_increased":True,"computation_change_only_local_identifier":True,
            "pinned_lean_parser_blob":PARSER_BLOB,"r1_failure_not_admitted":True,
            "parent_olean_sha256":r1.PARENT_OLEAN,"parent_source_recompiled":False,
            "r2_direct_digest":digest(d),"proof_authority":False,"action_authority":False}
    v.save(out/REPAIR,repair)
    print("KUUOS_R75_R2_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    return d

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r74-local","r74-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out==r1.ROOT/"artifacts/olean-r75","R75 exact isolated module path")
    if a.phase=="mcp":
        v.need(load(out/REPAIR)["r2_direct_digest"]==digest(load(out/"direct.json")),"R75 repair receipt required before MCP")
        r1.mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":
        for name in (*SOURCE_REPAIRS,REPAIR):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R75 independent repair byte equality "+name)
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
