#!/usr/bin/env python3
"""R22 R2: exact JSON transport, not a change to the proof or search.
Reuse the original GREEN sandbox and actual MCP on the identical R22
source, compare both archived direct receipts, then independently rerun
the unchanged direct verifier on a fresh runner. Preserve R1 failure.
"""
from __future__ import annotations
import argparse
import copy
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_shared_specialized_subproof_v1_r22 as r22
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob

v=r22.v
load=r22.load
ROOT=r22.ROOT
PILOT=Path(__file__).resolve().parents[1]
R1_HEAD="0e8f63ce56a8d62e393774d819e7e57fe59a5d8d"
R1_TREE="24104b74072148d10967855bcebabc64819546b6"
R1_RUN=45817298015
DIRECT="f898f5683e67d80209ad09643f36d14891f49352dd7ea63c5b98651d3f2f1b04"
MCP="ab2bf2329c5f2d59a8970bc5d69d7af71a793f8ee59f056ef8785046c7a82579"
ARTS=((15115354804,"codeai-olean-r22-local-45817298015-1","sha256:2af5bb990e3ed696288415e1e37eefa48dda0c2094fbc62598084efff5228ae7"),
      (15117020153,"codeai-olean-r22-independent-45817298015-1","sha256:5185d01ebf99ec9e807fc9c671179b7aab12e7828ed5c9e78a422679e69f1340"))
ADDITIONS={"scripts/check_codeai_olean_shared_specialized_subproof_v1_r22_r2.py",
           ".github/workflows/codeai-olean-shared-specialized-subproof-v1-r22-r2.yml"}
R1_SOURCES={
 "runtime/kuuos_codeai_olean_shared_specialized_subproof_v1.py":"7ef07ee9b8bbb03511f269e3c191f9f73974a2a0",
 "scripts/check_codeai_olean_shared_specialized_subproof_v1_r22.py":"95ae9e00d4bd7a8fca7e8e52c779a3958ea8c79a",
 ".github/workflows/codeai-olean-shared-specialized-subproof-v1-r22.yml":"221ff087dd502d67abe701358daec4a59c226826"}

def json_value(value):
    return json.loads(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False))

def compare_transport(raw,saved):
    # Only the known tree representation is permitted to change Python type.
    # Never omit a field, change a value, or compare only the digests.
    candidate=copy.deepcopy(raw)
    v.need(isinstance(raw["plan"]["shared_tree"],tuple),"expected in-memory tree tuple")
    v.need(isinstance(saved["plan"]["shared_tree"],list),"expected serialized tree list")
    candidate["plan"]["shared_tree"]=json_value(raw["plan"]["shared_tree"])
    v.need(raw!=saved and candidate==saved and json_value(raw)==saved,
           "not the exact R22 tuple/list transport discrepancy")
    v.need(old.digest(raw)==old.digest(saved)==DIRECT,"exact receipt digest")
    return candidate

def admit_archived(a):
    head=os.environ["GITHUB_SHA"]
    commit=v.cache.api("git/commits/"+R1_HEAD)
    v.need(commit["sha"]==R1_HEAD and commit["tree"]["sha"]==R1_TREE,"R22 R1 tree")
    cmp=v.cache.api("compare/"+R1_HEAD+"..."+head+"?per_page=100")
    files=cmp["files"]
    v.need(cmp["status"]=="ahead" and cmp["ahead_by"]==1 and cmp["behind_by"]==0 and
           cmp["merge_base_commit"]["sha"]==R1_HEAD and
           {f["filename"] for f in files}==ADDITIONS and len(files)==len(ADDITIONS) and
           all(f["status"]=="added" and f["deletions"]==0 for f in files),"not an audit-only additive change")
    for path,sha in R1_SOURCES.items():
        v.need(git_blob((PILOT/path).read_bytes())==sha,"R1 verifier source changed:"+path)
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD,"canonical HEAD drift")
    v.need(old.digest(v.cache.remote_scope(v.cache.api,old.HEAD))==old.SCOPE,"remote scope drift")
    run=v.cache.api("actions/runs/"+str(R1_RUN))
    v.need(run["head_sha"]==R1_HEAD and run["run_attempt"]==1 and
           run["status"]=="completed" and run["conclusion"]=="failure","R1 run identity")
    for jid,conclusion,steps in [
        (139900224224,"success",{"Verify R22 shared specialized subproof and exact application":"success",
                                "Actual Lean MCP R22 new application audit":"success"}),
        (139902326601,"failure",{"Independently reconstruct R22 shared specialized subproof and application":"failure"})]:
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==R1_RUN and j["status"]=="completed" and j["conclusion"]==conclusion and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]==c
                       for s in j["steps"]) for n,c in steps.items()),"R1 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==R1_RUN and x["workflow_run"]["head_sha"]==R1_HEAD,
               "R1 artifact identity")
    local=a.r22_local;ind=a.r22_independent
    d=load(local/"direct.json");i=load(ind/"direct.json");mp=load(local/"mcp.json")
    v.need(d==i and (local/"direct.json").read_bytes()==(ind/"direct.json").read_bytes() and
           old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R22_DIRECT_SPECIALIZED_SUBPROOF" and
           mp["status"]=="R22_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,
           "R1 receipt mismatch")
    filename="SharedSpecializedApplication.lean"
    v.need((local/filename).read_bytes()==(ind/filename).read_bytes(),"R1 generated source drift")
    diag=v.structured(load(local/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False and
           diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),
           "archived MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==len(mp["audits"])==9,"archived MCP audit count")
    for j,row in enumerate(rows):
        raw=load(local/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               r22.normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"],"archived MCP audit mismatch")
    return d

def controls(d):
    # Reconstruct exactly the observed Python tuple-tree representation,
    # then reject both an altered tree and a change elsewhere in the receipt.
    def as_tuple(t):
        v.need(isinstance(t,list) and len(t)==2 and isinstance(t[0],str) and isinstance(t[1],list),
               "tree JSON shape")
        return (t[0],tuple(as_tuple(c) for c in t[1]))
    raw=copy.deepcopy(d)
    raw["plan"]["shared_tree"]=as_tuple(d["plan"]["shared_tree"])
    v.need(compare_transport(raw,d)==d,"transport control")
    altered=copy.deepcopy(d);altered["plan"]["shared_tree"][0]+="_changed"
    try:compare_transport(raw,altered)
    except ValueError:pass
    else:raise ValueError("changed tree admitted")
    altered=copy.deepcopy(d);altered["provider_calls"]=1
    try:compare_transport(raw,altered)
    except ValueError:pass
    else:raise ValueError("changed non-tree field admitted")
    return {"tuple_list_only":True,"changed_tree_rejected":True,"changed_other_field_rejected":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("reuse-sandbox","independent"))
    for x in ("index","r20-local","r20-independent","r21-local","r21-independent","r22-local","r22-independent","gate"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    archived=admit_archived(a);cs=controls(archived)
    gate={"status":"R22_R2_ARCHIVED_SANDBOX_ADMITTED","r1_head":R1_HEAD,"r1_tree":R1_TREE,
          "r1_run":R1_RUN,"r2_head":os.environ["GITHUB_SHA"],"source_head":old.HEAD,
          "scope_digest":old.SCOPE,"direct_digest":DIRECT,"mcp_digest":MCP,
          "controls":cs,"provider_calls":0,"proof_authority":False}
    if a.phase=="reuse-sandbox":
        out.mkdir(parents=True,exist_ok=False)
        v.save(out/"gate.json",gate)
        print("KUUOS_R22_R2_SANDBOX_REUSE",json.dumps(gate,sort_keys=True),flush=True)
        return
    v.need(load(a.gate/"gate.json")==gate,"sandbox admission changed")
    out.mkdir(parents=True,exist_ok=False)
    raw=r22.direct(a,out)
    saved=load(out/"direct.json")
    d=compare_transport(raw,saved)
    v.need(d==archived and
           (out/"direct.json").read_bytes()==(a.r22_local/"direct.json").read_bytes() and
           (out/"SharedSpecializedApplication.lean").read_bytes()==(a.r22_local/"SharedSpecializedApplication.lean").read_bytes(),
           "fresh independent source or receipt differs")
    # Same original strict evidence verification, now comparing exact JSON values.
    r22.independent(d,a.r22_local,out)
    original=load(out/"independent.json")
    v.need(original["status"]=="R22_INDEPENDENT_SPECIALIZED_SUBPROOF_GREEN" and
           original["direct_digest"]==DIRECT and original["mcp_digest"]==MCP,"original audit")
    result={**original,"status":"R22_R2_INDEPENDENT_SPECIALIZED_SUBPROOF_GREEN",
            "r1_head":R1_HEAD,"r1_run":R1_RUN,"r2_head":os.environ["GITHUB_SHA"],
            "sandbox_admission_digest":old.digest(gate),"tuple_list_transport_verified":True,
            "source_and_receipt_bytes_equal":True,"new_sandbox_lean_runs":0,"fresh_independent_lean_runs":1}
    v.save(out/"r2-receipt.json",result)
    print("KUUOS_R22_R2_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

if __name__=="__main__":main()
