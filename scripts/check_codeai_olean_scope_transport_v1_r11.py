#!/usr/bin/env python3
"""R11: replay actual R10 artifacts, test scope transport, query Lake's real library module closure."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_research_entry_v1_r10 as r10
from runtime import kuuos_codeai_olean_scope_transport_v1 as gate
from runtime import kuuos_codeai_olean_typed_route_preflight_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

v=r10.v
cache=gate.cache
load=r10.load
RUN=45781051747
COMMIT="9fb37d6d7f97545a67caf59741ed73c20fbec706"
ARTIFACTS=(
 (15097699370,"codeai-olean-r10-local-45781051747-1","sha256:4699ac26c287bd1546b152d7ed9f6216d2ae9e0cf6d8fa7bde0d69013a995e83"),
 (15097584911,"codeai-olean-r10-independent-45781051747-1","sha256:00de8d4f2cd8c094b98f8c534d2213bc367a0bc655ef8d92c175ce12fb6d609b"),
)
JOBS={139776320310:"Replay R10 production research entry with historical actual Lean and MCP evidence",
      139776639684:"Independently replay R10 and compare exact receipts"}

def admit_r10(local,independent):
    run=cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==COMMIT and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R10 run lineage")
    for jid,name in JOBS.items():
        j=cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and any(s["name"]==name and s["status"]=="completed" and s["conclusion"]=="success"
                       for s in j["steps"]),"R10 job or step")
    for aid,name,sha in ARTIFACTS:
        a=cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==name and a["digest"]==sha and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==COMMIT,
               "R10 artifact lineage")
    a,b=load(local/"receipt.json"),load(independent/"receipt.json")
    v.need(a==b and a["status"]=="R10_VERSIONED_RESEARCH_ENTRY_GREEN"
           and a["source_head"]==old.HEAD and a["source_tree"]==old.TREE
           and a["r9_context_digest"]==old.R9_CONTEXT and a["provider_calls"]==0
           and len(a["hold_controls"])==12,"R10 receipt mismatch")
    return a

def coverage(db, out):
    # This is the actual pinned Lake library modules facet, which the pinned
    # library leanArts build consumes. No source regexp approximates it.
    cp=subprocess.run(["lake","query","--json","KuuOSFormal:modules"],
                      text=True,capture_output=True,timeout=300,check=False)
    (out/"lake-query.stdout").write_text(cp.stdout,encoding="utf-8")
    (out/"lake-query.stderr").write_text(cp.stderr,encoding="utf-8")
    v.need(cp.returncode==0,"Lake module query failed: "+cp.stderr[-4000:])
    rows=json.loads(cp.stdout)
    v.need(isinstance(rows,list) and all(isinstance(x,str) and x for x in rows)
           and len(rows)==len(set(rows)),"Lake query module format/identity")
    modules=set(rows)
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        inv=[json.loads(x[0]) for x in con.execute("SELECT row_json FROM modules ORDER BY module")]
    finally:
        con.close()
    v.need(len(inv)==2815 and "KuuOSFormal" in modules,"module inventory mismatch")
    missing=[x for x in inv if x["state"]=="HOLD_MISSING_OLEAN"]
    v.need(len(missing)==695,"missing inventory changed")
    known={x["module"] for x in inv}
    detail=[{"module":x["module"],"sources":x["sources"],
             "lake_module_closure_membership":x["module"] in modules,
             "status":"HOLD_MISSING_OLEAN","actual_missing_reason":"NO_DATA"}
            for x in missing]
    result={"status":"ACTUAL_LAKE_LIBRARY_MODULE_CLOSURE_OBSERVED",
            "query":"lake query --json KuuOSFormal:modules",
            "lake_module_count":len(modules),"lake_module_names":sorted(modules),
            "indexed_module_count":len(inv),"missing_module_count":len(missing),
            "missing_inside_closure":sum(x["lake_module_closure_membership"] for x in detail),
            "missing_outside_closure":sum(not x["lake_module_closure_membership"] for x in detail),
            "lake_modules_outside_index":sorted(modules-known),"missing_rows":detail,
            "full_edge_graph_exported":False,"missing_artifact_cause_certified":False,
            "proof_authority":False}
    v.save(out/"lake-module-coverage.json",result)
    return result

def main():
    p=argparse.ArgumentParser()
    for x in ("index","r8-local","r8-independent","r9-local","r9-independent","r10-local","r10-independent","out"):
        p.add_argument("--"+x,type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args()
    transport=gate.observe_scope(cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED","canonical transport unavailable")
    # The research checkout must itself have the same exact proof inputs as
    # the observed canonical scope before making the actual Lake query.
    checkout=cache.git(Path.cwd(),"rev-parse","HEAD")
    v.need(cache.local_scope(Path.cwd(),checkout)==transport["proof_scope"],"local proof scope differs")
    receipt,db=r10.r9.r8.admit(a.index,old.HEAD)
    oldtype,req=r10.r9.historical_r8(a.r8_local,a.r8_independent,old.HEAD)
    r10.admit_r9()
    historical=admit_r10(a.r10_local,a.r10_independent)
    d=load(a.r9_local/"direct.json")
    i=load(a.r9_independent/"direct.json")
    m=load(a.r9_local/"mcp.json")
    ctx=load(a.r9_independent/"routes.json")
    replay=load(a.r9_independent/"independent.json")
    v.need(any(x["name"]==oldtype["name"] and x["type_expr_sha256"]==oldtype["type_expr_sha256"]
               and x["request_digest"]==req["request_digest"] for x in d["materialized_sources"]),"R8 type lineage")
    calls=[]
    class ForbiddenProvider:
        def generate(self,prompt):
            calls.append(prompt)
            raise AssertionError("no provider allowed")
    common=dict(db=db,index_receipt=receipt,direct=d,independent=i,mcp=m,routes=ctx,replay=replay,
                provider_adapters=[ForbiddenProvider()])
    def invoke(t,key,**changes):
        req=gate.make_request(t,ctx["routes"][key]["target"],typed.make_request(ctx,key))
        args=dict(common,transport=t,expected_transport_digest=old.digest(t),request=req)
        args.update(changes)
        return gate.build_scope_bound_research_synthesis(**args)
    actual={k:invoke(transport,k) for k in typed.CASES}
    v.need({k:x["status"] for k,x in actual.items()}==historical["routes"]
           and all(old.digest(x["historical_result"])==historical["route_digests"][k]
                   for k,x in actual.items()),"actual R10 route changed")
    # Adversarial transport fixtures emulate metadata-only and changed-scope
    # descendants; they are never submitted or recorded as actual GitHub refs.
    base_commit=cache.api("git/commits/"+old.HEAD)
    root=cache.api("git/trees/"+old.TREE)
    new_head="1"*40;new_tree="2"*40
    def fixture(mode):
        ref={"ref":"refs/heads/main","object":{"type":"commit","sha":new_head}}
        c=copy.deepcopy(base_commit);c["sha"]=new_head;c["tree"]["sha"]=new_tree
        t=copy.deepcopy(root);t["sha"]=new_tree
        if mode=="changed_formal":
            next(x for x in t["tree"] if x["path"]=="formal")["sha"]="3"*40
        elif mode=="alternate_lake":
            t["tree"].append({"path":"lakefile.lean","mode":"100644","type":"blob","sha":"3"*40})
        else:
            t["tree"].append({"path":"R11-fixture-doc-only.md","mode":"100644","type":"blob","sha":"3"*40})
        if mode=="truncated":
            t["truncated"]=True
        def get(path):
            if path=="git/ref/heads/main":return ref
            if path=="git/commits/"+new_head:return c
            if path=="git/trees/"+new_tree:return t
            if path.startswith("compare/"+old.HEAD+"..."+new_head):
                return {"status":"diverged" if mode=="diverged" else "ahead",
                        "base_commit":{"sha":old.HEAD},"merge_base_commit":{"sha":old.HEAD}}
            return cache.api(path)
        return gate.observe_scope(get)
    simulated=fixture("doc_only")
    v.need(simulated["status"]=="SAME_PROOF_SCOPE_OBSERVED"
           and simulated["historical_source_head"]==old.HEAD
           and simulated["current_source_head"]==new_head,"same-scope descendant fixture")
    sim={k:invoke(simulated,k) for k in typed.CASES}
    v.need(all(x["status"]==historical["routes"][k]
               and x["current_source_head"]==new_head
               and old.digest(x["historical_result"])==historical["route_digests"][k]
               for k,x in sim.items()),"historical result did not survive metadata-only fixture")
    controls={k:fixture(k) for k in ("changed_formal","alternate_lake","truncated","diverged")}
    original=gate.make_request(transport,ctx["routes"]["reverse"]["target"],typed.make_request(ctx,"reverse"))
    controls.update({
        "stale_request":invoke(simulated,"reverse",request=original),
        "forged_scope":invoke(dict(transport,scope_digest="0"*64),"reverse"),
        "wrong_transport_digest":invoke(transport,"reverse",expected_transport_digest="0"*64),
        "changed_current_head":invoke(transport,"reverse",request=dict(original,current_source_head="0"*40)),
        "unknown_target":invoke(transport,"reverse",request=gate.make_request(transport,"new goal",terms=["r11zzzznohitzzzz"])),
    })
    v.need(all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW"
               and x["candidate_generation_allowed"] is False for x in controls.values())
           and not calls,"scope or target control promoted")
    miss=controls["unknown_target"]["historical_result"]["search_plan"]["search"]
    v.need(miss["status"]=="HOLD_NO_DATA" and len(miss["unobserved_modules"])==695,"missing coverage not retained")
    a.out.mkdir(parents=True,exist_ok=False)
    cv=coverage(db,a.out)
    v.need(gate.observe_scope(cache.api)==transport
           and cache.local_scope(Path.cwd(),checkout)==transport["proof_scope"],"source moved during query")
    result={"status":"R11_SCOPE_TRANSPORT_AND_LAKE_CLOSURE_GREEN",
            "historical_r10_receipt_digest":old.digest(historical),
            "transport":transport,"transport_digest":old.digest(transport),
            "actual_routes":{k:x["status"] for k,x in actual.items()},
            "actual_route_digests":{k:old.digest(x) for k,x in actual.items()},
            "simulated_metadata_descendant_routes":{k:x["status"] for k,x in sim.items()},
            "fixture_is_actual_canonical_observation":False,
            "hold_controls":sorted(controls),"provider_calls":len(calls),
            "lake_coverage_digest":old.digest(cv),"lake_module_count":cv["lake_module_count"],
            "missing_inside_closure":cv["missing_inside_closure"],
            "missing_outside_closure":cv["missing_outside_closure"],
            "lake_modules_outside_index_count":len(cv["lake_modules_outside_index"]),
            "unobserved_modules":695,"fresh_proof_elaboration":False,
            "historical_lean_and_mcp_reused":True,"semantic_search_complete":False,
            "proof_authority":False,"residual_generation_authorized":False}
    v.save(a.out/"receipt.json",result)
    if a.first is not None:
        v.need(result==load(a.first/"receipt.json")
               and cv==load(a.first/"lake-module-coverage.json"),"independent R11 replay differs")
    print("KUUOS_R11_SCOPE_LAKE",json.dumps(result,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
