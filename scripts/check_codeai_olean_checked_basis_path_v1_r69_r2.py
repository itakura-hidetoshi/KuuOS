#!/usr/bin/env python3
"""R69 R2: qualify the four actual computation calls; preserve all Lean statements."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_checked_basis_path_v1_r69 as r1
v=r1.v
HEAD="7cf984e4215858cd8098e94bdf365ba9183a0b2a"
RUN=46103903288
JOB=140852253983
ART=15246549909
DIGEST="sha256:e6eeb5647e89127a479d2f1b4dba0c5555ae980a23339803663e6114881246b0"
FORMAL_SHA="bae6164f778bb89d1cd14d89f4e0653271c53b31e9b5de592732b84842d56500"
APP_SHA="f08680aae603a07ffab1b7d949d309908ef0610290b4fd466bfb767ab4b6a985"
COMPUTE_SHA="93bea183c97bd762fa76ea958a549ee402117f620f380b73a531177d7679042e"
ORIGINAL=r1.path_sources
OLD="(decide (checkedBoundPatch "
NEW="(decide (KuuOSR67.checkedBoundPatch "

def bind(a):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    job=api("actions/jobs/"+str(JOB))
    art=api("actions/artifacts/"+str(ART))
    v.need(run["head_sha"]==HEAD and run["status"]=="completed" and run["conclusion"]=="failure" and run["run_attempt"]==1 and
           job["run_id"]==RUN and job["head_sha"]==HEAD and job["status"]=="completed" and job["conclusion"]=="failure" and
           any(s["name"]=="Verify R69 checked basis path" and s["conclusion"]=="failure" for s in job["steps"]),"R69 R1 failure lineage")
    v.need(art["id"]==ART and art["name"]=="codeai-olean-r69-local-46103903288-1" and art["digest"]==DIGEST and
           not art["expired"] and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD,"R69 R1 artifact lineage")
    sha=r1.r63.r62.r23.sha
    fail=a.r1_failure
    v.need((fail/"formal-source.lean").read_bytes()==r1.FORMAL.read_bytes() and
           sha(r1.FORMAL.read_bytes())==FORMAL_SHA and
           sha((fail/"path-application.lean").read_bytes())==APP_SHA and
           sha((fail/"path-computation.lean").read_bytes())==COMPUTE_SHA,"R69 R1 exact source identities")
    log=(fail/"RecoveryDualityR62.log").read_text(encoding="utf-8")
    errors=[x for x in log.splitlines() if x.startswith("/home/") and ("error:" in x or "error(" in x or "warning:" in x)]
    v.need(len(errors)==4 and all("error(lean.unknownIdentifier): Unknown identifier "+chr(96)+"checkedBoundPatch"+chr(96) in x for x in errors),
           "R69 exact R1 computation name-resolution failure")
    def repaired_sources(*args):
        app,compute,items,refs=ORIGINAL(*args)
        v.need(app.encode()==(fail/"path-application.lean").read_bytes() and
               compute.encode()==(fail/"path-computation.lean").read_bytes() and
               compute.count(OLD)==4 and NEW not in compute,"R69 R1 exact generated input")
        changed=compute.replace(OLD,NEW)
        v.need(changed.count(NEW)==4 and changed.replace(NEW,OLD)==compute,"R69 name qualification only")
        return app,changed,items,refs
    r1.path_sources=repaired_sources
    return log

def verify_failed_raw(log,d,out):
    prefix="KUUOS_RECALL_KERNEL "
    rows=d["fresh_application"]["observations"]
    by={x["name"]:x for x in (json.loads(l[len(prefix):]) for l in log.splitlines() if l.startswith(prefix))}
    v.need(len(by)==len(rows)==247 and all(x["name"] in by and
           set(x["expected_direct_refs"])<=set(by[x["name"]]["proof_constants"]) for x in rows),"R69 R1 kernel inventory and references")
    # The earlier run did not complete the computation or the enclosing gate.
    # Compare all raw proof/type/axiom objects against the new certified replay.
    for i,layer in ((62,r1.r63.r62.NEW),(63,r1.r63.NEW),(64,r1.r64.NEW),(65,r1.r65.NEW),
                    (66,r1.r66.NEW),(67,r1.r67.NEW),(68,r1.r68.NEW),(69,r1.NEW)):
        mark="KUUOS_R"+str(i)+"_RAW "
        obs=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
        v.need(len(obs)==len({x["name"]:x for x in obs}) and
               {x["name"]:x for x in obs}==r1.load(out/layer)["raw_theorems"],"R69 R1 exact raw replay "+str(i))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r68-local","r68-independent","first","r1-failure"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(r1.ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":
        r1.mcp(out);return
    failed_log=bind(a)
    out.mkdir(parents=True,exist_ok=False)
    d=r1.direct(a,out)
    verify_failed_raw(failed_log,d,out)
    v.need((out/"formal-source.lean").read_bytes()==r1.FORMAL.read_bytes() and
           (out/"path-application.lean").read_bytes()==(a.r1_failure/"path-application.lean").read_bytes() and
           (out/"path-computation.lean").read_text(encoding="utf-8").replace(NEW,OLD).encode()==
             (a.r1_failure/"path-computation.lean").read_bytes() and
           (out/"historical-scope.json").read_bytes()==(a.r1_failure/"historical-scope.json").read_bytes() and
           (out/"script-bridge.json").read_bytes()==(a.r1_failure/"script-bridge.json").read_bytes(),
           "R69 R2 unchanged formal, application and scope inputs")
    shutil.copyfile(a.r1_failure/"path-computation.lean",out/"path-computation-r1.lean")
    repair={"status":"R69_R2_QUALIFIED_COMPUTATION_ONLY","r1_run":RUN,"r1_head":HEAD,"r1_artifact":ART,
        "r1_artifact_digest":DIGEST,"r1_all_formal_and_application_bytes_unchanged":True,
        "r1_all_raw_proofs_equal":True,"r1_kernel_inventory":247,
        "r1_computation_status":"FAILED_NAME_RESOLUTION","r2_qualified_calls":4,
        "r1_computation_sha256":COMPUTE_SHA,"r2_computation_sha256":d["computation_source_sha256"],
        "repair":"qualify checkedBoundPatch as KuuOSR67.checkedBoundPatch; preserve all assertions and proof gates"}
    v.save(out/"r69-r2-repair.json",repair)
    print("KUUOS_R69_R2_REPAIR",json.dumps(repair,sort_keys=True),flush=True)
    if a.phase=="independent":
        for name in ("path-computation-r1.lean","r69-r2-repair.json"):
            v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R69 R2 repair byte identity")
        r1.independent(d,a.first,out)
if __name__=="__main__":main()
