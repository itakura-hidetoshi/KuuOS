#!/usr/bin/env python3
"""R13: real indexed candidate vocabulary -> closed premise trials -> actual Lean/MCP."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_general_application_v1_r12 as r12
from runtime import kuuos_codeai_olean_premise_search_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob
from check_codeai_no_go_memory_v1_r2 import normalize

v=r12.v
r8=r12.r8
r5=r12.r5
ROOT=v.ROOT
load=r12.load
RUN=45784651518
HEAD="5156349343badb4626705b9c9e99b2c5ec12dbbb"
DIRECT="08b63523e2f694178d0e005c502538e08022ba4396f15ddd1f49ecf43ffb5239"
MCP="8e4ec07e6bac458fc86300059cec9a2f7a10dfab62acfa38a0a27d4ff9e0c039"
CTX="874f91c98b67cedfa7a2a7bd49a30a8f72a486d6176bee1668182c03fc945b11"
ARTS=(
 (15099113999,"codeai-olean-r12-local-45784651518-1","sha256:7f26e0b49bbff24f7cd24f10feaa28e5db8a2a62c99a64e519cf547a6bba61a9"),
 (15100232806,"codeai-olean-r12-independent-45784651518-1","sha256:6b9942d29738aa1f77e1b3c755b1738d3fff86643d8d121dd0b8db5ce0d86665"),
)
LEC=r12.LEC
F55=r12.F55
PROOF=LEC+".NativeF55ProofHistoryBoundary"
SCOPED=LEC+".ScopedGluing"
CRITERION=LEC+".SourceAwareOverlapDescentCriterion"

def admit_r12(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R12 run lineage")
    for jid,names in ((139788253535,["Verify R12 exact indexed source applications and deliberate mismatch controls",
                                    "Actual Lean MCP R12 application and source axiom audit"]),
                      (139790681138,["Independently reconstruct R12 exact applications and project closed target routes"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R12 job or step")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R12 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");ctx=load(independent/"routes.json");receipt=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP and old.digest(ctx)==CTX
           and typed.project(d,i,m)==ctx and receipt["status"]=="R12_INDEPENDENT_GENERAL_APPLICATION_GREEN"
           and receipt["context_digest"]==CTX and receipt["direct_digest"]==DIRECT
           and receipt["mcp_digest"]==MCP,"R12 exact evidence changed")
    return d

def c(n):return {"const":n}
def ap(f,*xs):return {"apply":[c(f),*xs]}
def slot(n):return {"slot":n}

def queries():
    raw=c(LEC+".NorthNativeF55Raw");shadow=c(LEC+".NorthNativeF55Shadow")
    observe=c(LEC+".northNativeF55Observe");identity=ap("id",raw)
    x=c("Kuu.F112.Physical.northNativeF55PentagonCell")
    y=c("Kuu.F112.Physical.northNativeF55PentagonWithUnit")
    s={"modules":[PROOF],"names":["northNativeF55_observed_equal","northNativeF55_raw_distinct"]}
    no_distinct={"modules":[PROOF],"names":["northNativeF55_observed_equal"]}
    target=ap(LEC+".Factors",raw,shadow,raw,observe,identity)
    fixed=[raw,shadow,raw,observe,identity,x,y,slot(0),slot(1)]
    out={}
    for k,pools in (("collision",[s,s]),("collision_missing",[s,no_distinct])):
        out[k]=gate.make_query(k,SCOPED,LEC+".no_factor_of_collision",target,fixed,"negative",[PROOF],pools)
    pool={"modules":[F55],"names":["nativeF55_twoChart_constant_raw_global",
                                 "nativeF55_twoChart_raw_no_global","nativeF55_twoChart_shadow_global"]}
    for k,atlas in (("alternative","northNativeF55TwoChartConstantRaw"),("original","northNativeF55TwoChartRaw")):
        prefix=[c("Unit"),c("Bool"),raw,shadow,c(LEC+".northNativeF55TwoChartCover"),observe,c(LEC+"."+atlas)]
        out[k]=gate.make_query(k,CRITERION,LEC+".sourceGlobal_implies_overlapFaithful",
                ap(LEC+".OverlapFiberFaithful",*prefix),prefix+[slot(0)],"positive",[],[pool])
    return out

EXPECTED={"collision":"REFUTED_EXACT_TARGET","collision_missing":"HOLD_TYPED_APPLICABILITY_REVIEW",
          "alternative":"REUSE_EXISTING","original":"HOLD_TYPED_APPLICABILITY_REVIEW"}

def direct(a,out):
    historical=admit_r12(a.r12_local,a.r12_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED"
           and transport["current_source_head"]==old.HEAD,"current proof scope")
    receipt,db=r8.admit(a.index,old.HEAD)
    qs=queries();plans={k:gate.discover(db,receipt,q) for k,q in qs.items()}
    v.need({k:x["combination_count"] for k,x in plans.items()}==
           {"collision":4,"collision_missing":2,"alternative":3,"original":3},"candidate discovery inventory")
    for k,p in plans.items():
        v.need(p["status"]=="BOUNDED_PREMISE_PLAN"
               and all(len(s["unobserved_modules"])==695 and s["omitted_matches"]==0
                       for s in p["search_evidence"]),"incomplete index context")
        v.save(out/(k+"-plan.json"),p)
    pairs={(q["module"],q["source"]) for q in qs.values()}
    pairs.update((p["module"],p["name"]) for plan in plans.values() for t in plan["trials"] for p in t["premises"])
    plan=r8.prepare(db,receipt,old.R7,old.HEAD,[n for _,n in sorted(pairs)],
                    "R13 premise source complete types",[{"module":m,"name":n} for m,n in sorted(pairs)])
    v.need(plan["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and len(plan["requests"])==len(pairs),
           "complete materialization plan unavailable")
    v.save(out/"materials-plan.json",plan)
    materials={};env=r5.fixed_lean()
    for j,req in enumerate(plan["requests"]):
        mod,n=req["module"],req["name"];key=mod+"::"+n
        sources=req["coverage"]["sources"]
        v.need(len(sources)==1 and git_blob((ROOT/sources[0]["path"]).read_bytes())==sources[0]["blob"],
               "source identity")
        bound,why=r5.bind_files(mod,ROOT/".lake/build/lib/lean"/(mod.replace(".","/")+".olean"),sources[0])
        v.need(why is None and bound==req["binding"],"olean identity")
        if key in historical["materialized_sources"]:
            x=historical["materialized_sources"][key]
            v.need(x["request_digest"]==req["request_digest"] and x["artifact_binding_digest"]==old.digest(bound),
                   "R12 historical type binding")
            reuse=True
        else:
            x=r8.materialize(out/f"exact-{j:02}",req,{mod:sources},env);reuse=False
        materials[key]={"module":mod,"name":n,"type_expr_sha256":x["type_expr_sha256"],
                        "request_digest":req["request_digest"],"reused_r12":reuse}
    results={}
    for k,q in qs.items():
        results[k]=[]
        for tr in plans[k]["trials"]:
            req=tr["request"];cid=req["case_id"];_,w=typed.names(req)
            premises=sorted({p["name"] for p in tr["premises"]})
            audits=sorted(set([req["source"]]+premises+[w]))
            src=gate.render(q,tr)+"\n"+v.suffix(audits)
            try:rc,log=r12.prior.compile_source(out/(cid+".lean"),src)
            except subprocess.TimeoutExpired:
                results[k].append({"status":"HOLD_LEAN_APPLICATION","reason":"TIMEOUT",
                                   "request_digest":req["request_digest"]});continue
            if rc:
                print("KUUOS_R13_HOLD",cid,log[-2200:],flush=True)
                results[k].append({"status":"HOLD_LEAN_APPLICATION","reason":"LEAN_REJECTED" if "error:" in log else "RUNNER_FAILURE",
                                   "request_digest":req["request_digest"]});continue
            rows=v.read_direct(log,[{"name":n,"expected_direct_refs":[req["source"]]+premises if n==w else []}
                                    for n in audits])
            apps=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
            v.need(len(apps)==1,"application marker")
            for p in [{"module":req["module"],"name":req["source"]}]+tr["premises"]:
                v.need(next(x for x in rows if x["name"]==p["name"])["type_expr_sha256"]
                       ==materials[p["module"]+"::"+p["name"]]["type_expr_sha256"],"source full type changed")
            results[k].append({"status":"EXACT_TYPED_APPLICATION","request_digest":req["request_digest"],
                               "observations":rows,"application":apps[0],"probe_sha256":v.sha(src.encode())})
    counts={k:sum(x["status"]=="EXACT_TYPED_APPLICATION" for x in rows) for k,rows in results.items()}
    v.need(counts=={"collision":1,"collision_missing":0,"alternative":1,"original":0}
           and all(x.get("reason")=="LEAN_REJECTED" for rows in results.values() for x in rows
                   if x["status"]=="HOLD_LEAN_APPLICATION"),"unexpected trial behavior")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    d={"status":"R13_DIRECT_PREMISE_TRIALS","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r12_context_digest":CTX,"r7_receipt_digest":old.R7,
       "unobserved_module_count":695,"queries":qs,"plans":{k:{x:y for x,y in p.items() if x!="search_evidence"}
                                                        for k,p in plans.items()},
       "search_evidence_digests":{k:old.digest(p["search_evidence"]) for k,p in plans.items()},
       "materials":materials,"results":results,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R13_DIRECT",json.dumps({"direct_digest":old.digest(d),"trials":sum(map(len,results.values())),
          "successful":counts,"reused_types":sum(x["reused_r12"] for x in materials.values()),
          "new_types":sum(not x["reused_r12"] for x in materials.values())},sort_keys=True),flush=True)
    return d

def mcp(out):
    d=load(out/"direct.json")
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    audits={}
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS premise search","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        for k,rows in d["results"].items():
            for tr,x in zip(d["plans"][k]["trials"],rows):
                if x["status"]!="EXACT_TYPED_APPLICATION":continue
                cid=tr["request"]["case_id"];p=out/("Mcp_"+cid+".lean")
                p.write_text(gate.render(d["queries"][k],tr,False)+"\nset_option pp.universes false\n"+
                             "\n".join("#check @"+z["name"] for z in x["observations"])+"\n",encoding="utf-8")
                rel=str(p.relative_to(ROOT))
                raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
                v.save(out/("mcp-diag-"+cid+".json"),raw);diag=v.structured(raw)
                v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
                       and diag["timed_out"] is False and diag["failed_dependencies"]==[]
                       and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnostics")
                audits[cid]=[]
                for j,row in enumerate(x["observations"]):
                    raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
                    v.save(out/f"mcp-verify-{cid}-{j}.json",raw);val=v.structured(raw);ax=normalize(val["axioms"])
                    v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"MCP axioms")
                    audits[cid].append({"name":row["name"],"axioms":ax})
    finally:client.close()
    result={"status":"R13_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":audits,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R13_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":sum(map(len,audits.values()))}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d,"independent direct evidence differs")
    for k,rows in a["results"].items():
        for tr,x in zip(a["plans"][k]["trials"],rows):
            if x["status"]!="EXACT_TYPED_APPLICATION":continue
            cid=tr["request"]["case_id"];diag=v.structured(load(first/("mcp-diag-"+cid+".json")))
            v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
                   and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnosis")
            for j,row in enumerate(x["observations"]):
                raw=load(first/f"mcp-verify-{cid}-{j}.json");val=v.structured(raw)
                v.need(raw["result"]["isError"] is False and val["warnings"]==[]
                       and normalize(val["axioms"])==row["axioms"]==mp["audits"][cid][j]["axioms"]
                       and row["name"]==mp["audits"][cid][j]["name"],"MCP evidence changed")
    ctx=gate.project(a,d,mp)
    v.need(ctx["status"]=="R13_INDEPENDENT_PREMISE_ROUTES_OBSERVED","projection failed")
    digest=old.digest(ctx)
    routes={k:gate.pre_provider(ctx,digest,q) for k,q in d["queries"].items()}
    v.need({k:x["status"] for k,x in routes.items()}==EXPECTED,"route mismatch")
    q=d["queries"]["collision"]
    controls={"changed_query":gate.pre_provider(ctx,digest,dict(q,polarity="positive")),
              "wrong_context":gate.pre_provider(ctx,"0"*64,q),
              "missing_mcp":gate.project(a,d,{}),
              "changed_independent":gate.project(a,dict(d,unobserved_module_count=0),mp)}
    v.need(all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and not x["candidate_generation_allowed"]
               for x in controls.values()),"unsafe promotion")
    v.save(out/"routes.json",ctx)
    v.save(out/"controls.json",controls)
    result={"status":"R13_INDEPENDENT_PREMISE_SEARCH_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"context_digest":digest,
            "routes":{k:x["status"] for k,x in routes.items()},
            "successful_premises":{k:x["successful_routes"] for k,x in routes.items()},
            "hold_controls":len(controls),"provider_calls":0,"unobserved_modules":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R13_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r12-local","r12-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
