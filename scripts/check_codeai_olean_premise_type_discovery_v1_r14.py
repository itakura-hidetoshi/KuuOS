#!/usr/bin/env python3
"""R14 real premise type discovery without theorem-name vocabulary."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_premise_search_v1_r13 as r13
from runtime import kuuos_codeai_olean_premise_type_discovery_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import exact_lookup
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob
from check_codeai_no_go_memory_v1_r2 import normalize

v=r13.v
r12=r13.r12
r8=r13.r8
r5=r13.r5
ROOT=v.ROOT
load=r13.load
RUN=45786634957
HEAD="6f876d934534842b5728082b708130ac5de8504b"
DIRECT="c3c0376f3d65bb33182c3ef6236d7604c56d90b8cc0ad887d09842172ec0227f"
MCP="f695444968fb9a846d7601b073ca2dce159c6c07dc5de8b1f64f809f0fa38dc6"
CTX="fe40993bd10ba28dbe4f39df9fbf4b973515ee156e0cf159144775bf6cbeaf75"
ARTS=(
 (15100529117,"codeai-olean-r13-local-45786634957-1","sha256:ab2de5f56e18d854588a6d8a0fe3e0c44957e43faa4554fcf7c17df3777dd445"),
 (15102035530,"codeai-olean-r13-independent-45786634957-1","sha256:178f0ae93399246b1d77217498d206bd1d1a56718095c00c243a7ace71e96f1a"),
)

def admit_r13(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R13 run lineage")
    for jid,names in ((139794928784,["Verify R13 indexed premise discovery and exact Lean trials",
                                    "Actual Lean MCP R13 premise and application audit"]),
                      (139797765959,["Independently reconstruct R13 premise trials and project typed routes"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R13 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R13 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");ctx=load(independent/"routes.json");r=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP and old.digest(ctx)==CTX
           and r13.gate.project(d,i,m)==ctx and r["status"]=="R13_INDEPENDENT_PREMISE_SEARCH_GREEN"
           and r["direct_digest"]==DIRECT and r["mcp_digest"]==MCP and r["context_digest"]==CTX,"R13 receipt")
    return d,ctx

def queries():
    base=r13.queries();out={}
    for k in ("collision","alternative","original"):
        q=base[k]
        out[k]=gate.make_query(k,q["module"],q["source"],q["target"],
                      [x for x in q["arguments"] if "slot" not in x],q["polarity"],
                      q["context_modules"],[s["modules"] for s in q["slots"]])
    q=out["collision"]
    out["missing"]=gate.make_query("missing",q["module"],q["source"],q["target"],q["fixed"],
                                   q["polarity"],q["context_modules"],[[r13.PROOF],[r12.WORLD]])
    c=r13.c;ap=r13.ap
    raw=c(r13.LEC+".NorthNativeF55Raw")
    fixed=[c("Unit"),c("Bool"),raw,c(r13.LEC+".northNativeF55TwoChartCover"),
           c(r13.LEC+".northNativeF55TwoChartConstantRaw")]
    out["compatible"]=gate.make_query("compatible",r13.SCOPED,r13.LEC+".global_implies_compatible",
        ap(r13.LEC+".Compatible",*fixed),fixed,"positive",[r13.F55],[[r13.F55]])
    return out

def material(db,receipt,historical,mod,name,out):
    req=exact_lookup(db,receipt,old.R7,old.HEAD,mod,name)
    v.need(req["status"]=="EXACT_OLEAN_MATERIALIZATION_REQUIRED","exact lookup unavailable")
    sources=req["coverage"]["sources"]
    v.need(len(sources)==1 and git_blob((ROOT/sources[0]["path"]).read_bytes())==sources[0]["blob"],"source changed")
    bound,why=r5.bind_files(mod,ROOT/".lake/build/lib/lean"/(mod.replace(".","/")+".olean"),sources[0])
    v.need(why is None and bound==req["binding"],"olean binding changed")
    key=mod+"::"+name
    if key in historical["materials"]:
        x=historical["materials"][key]
        v.need(x["request_digest"]==req["request_digest"],"R13 material request changed")
        return {"module":mod,"name":name,"type_expr_sha256":x["type_expr_sha256"],"reused_r13":True}
    x=r8.materialize(out,req,{mod:sources},r5.fixed_lean())
    return {"module":mod,"name":name,"type_expr_sha256":x["type_expr_sha256"],"reused_r13":False}

def historical_route(q,plan,hist,ctx):
    if q["case_id"] not in ("collision","alternative"):return None
    k=q["case_id"];routes=ctx["routes"][k]["successful_routes"]
    for combo in plan["combinations"]:
        req=gate.application_request(q,combo,"r14_compare")
        for t,row in zip(hist["plans"][k]["trials"],hist["results"][k]):
            if row["status"]!="EXACT_TYPED_APPLICATION" or not gate.same_application(req,t["request"]):continue
            if not all(hist["materials"][p["module"]+"::"+p["name"]]["type_expr_sha256"]==p["type_expr_sha256"] for p in combo):
                continue
            winner=next((x for x in routes if x["request_digest"]==t["request"]["request_digest"]),None)
            if winner is not None:
                return {"status":ctx["routes"][k]["status"],"historical_request_digest":winner["request_digest"],
                        "target_expr_digest":winner["target_expr_digest"],"premises":combo,
                        "historical_context_digest":CTX,"fresh_proof_elaboration":False}
    return None

def direct(a,out):
    hist,ctx=admit_r13(a.r13_local,a.r13_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    qs=queries();plans={};obs={};invs={};historical={};materials={}
    for k,q in qs.items():
        inv=gate.inventory(db,receipt,q);invs[k]=inv
        src=gate.render(q,inv)
        # Source theorem's full type is audited in the actual same imported environment.
        src+="\n"+v.suffix([q["source"]])
        rc,log=r12.prior.compile_source(out/("Discover_"+k+".lean"),src)
        if rc:
            print(log[-12000:],flush=True);raise ValueError("premise extraction failed:"+k)
        rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
        audited=v.read_direct(log,[{"name":q["source"],"expected_direct_refs":[]}])[0]
        key=q["module"]+"::"+q["source"]
        if key not in materials:
            materials[key]=material(db,receipt,hist,q["module"],q["source"],out/("exact-source-"+k))
        v.need(audited["type_expr_sha256"]==materials[key]["type_expr_sha256"],"imported source type differs")
        plan=gate.match_plan(q,inv,rows);plans[k]=plan;obs[k]=rows
        v.save(out/(k+"-inventory.json"),inv);v.save(out/(k+"-comparisons.json"),rows)
        v.save(out/(k+"-plan.json"),plan)
        historical[k]=historical_route(q,plan,hist,ctx)
    v.need(historical["collision"] is not None and historical["alternative"] is not None
           and plans["missing"]["combination_count"]==0 and plans["original"]["combination_count"]==0
           and plans["compatible"]["combination_count"]>0,"premise discovery controls")
    # A genuinely new application of a different source theorem. Retain all
    # matched combinations; any not attempted remains explicitly pending.
    q=qs["compatible"];combo=plans["compatible"]["combinations"][0]
    req=gate.application_request(q,combo,"compatible_new")
    mods=sorted(set([q["module"]]+q["context_modules"]+[p["module"] for p in combo]))
    prefix="import "+q["module"]+"\n"
    def imports(src):
        v.need(src.startswith(prefix),"render boundary")
        return "".join("import "+m+"\n" for m in mods)+src[len(prefix):]
    _,w=typed.names(req);names=sorted({req["source"],w}|{p["name"] for p in combo})
    for j,p in enumerate(combo):
        key=p["module"]+"::"+p["name"]
        if key not in materials:materials[key]=material(db,receipt,hist,p["module"],p["name"],out/("exact-premise-"+str(j)))
        v.need(materials[key]["type_expr_sha256"]==p["type_expr_sha256"],"matched complete premise type differs")
    src=imports(typed.render(req))+"\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplication.lean",src)
    if rc:print(log[-12000:],flush=True);raise ValueError("new typed application failed")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":[req["source"]]+[p["name"] for p in combo] if n==w else []}
                            for n in names])
    apps=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    v.need(len(apps)==1 and apps[0]["exact_kernel_type_match"] is True,"new application marker")
    for p in [{"module":req["module"],"name":req["source"]}]+combo:
        v.need(next(x for x in rows if x["name"]==p["name"])["type_expr_sha256"]
               ==materials[p["module"]+"::"+p["name"]]["type_expr_sha256"],"application type changed")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"request":req,"premises":combo,"observations":rows,"application":apps[0],
           "mcp_source":imports(typed.declarations(req))+"\nset_option pp.universes false\n"+"\n".join("#check @"+n for n in names)+"\n",
           "pending_combination_count":len(plans["compatible"]["combinations"])-1}
    result={"status":"R14_DIRECT_PREMISE_TYPE_DISCOVERY","source_head":old.HEAD,"scope_digest":old.SCOPE,
            "source_tree":old.TREE,"r13_context_digest":CTX,"queries":qs,"plans":plans,"historical_routes":historical,
            "inventory_digests":{k:old.digest(x) for k,x in invs.items()},
            "comparison_digests":{k:old.digest(x) for k,x in obs.items()},"materials":materials,"fresh_application":fresh,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",result)
    print("KUUOS_R14_DIRECT",json.dumps({"direct_digest":old.digest(result),
         "comparison_counts":{k:sum(len(s["comparisons"]) for s in rows) for k,rows in obs.items()},
         "matches":{k:[len(p) for p in x["pools"]] for k,x in plans.items()},
         "reused_routes":sum(x is not None for x in historical.values()),"new_applications":1},sort_keys=True),flush=True)
    return result

def mcp(out):
    d=load(out/"direct.json");x=d["fresh_application"]
    p=out/"McpApplication.lean";p.write_text(x["mcp_source"],encoding="utf-8")
    rel=str(p.relative_to(ROOT))
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS premise type discovery","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        v.save(out/"mcp-diagnostics.json",raw);diag=v.structured(raw)
        v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
               and diag["timed_out"] is False and diag["failed_dependencies"]==[]
               and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnostics")
        for j,row in enumerate(x["observations"]):
            raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
            v.save(out/f"mcp-verify-{j}.json",raw);val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"MCP axiom audit")
            rows.append({"name":row["name"],"axioms":ax})
    finally:client.close()
    result={"status":"R14_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R14_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R14_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
           and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnosis")
    x=d["fresh_application"];_,w=typed.names(x["request"])
    v.need(len(mp["audits"])==len(x["observations"]),"MCP inventory")
    for j,row in enumerate(x["observations"]):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[]
               and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"]
               and row["name"]==mp["audits"][j]["name"],"MCP evidence mismatch")
    witness=next(r for r in x["observations"] if r["name"]==w)
    v.need(x["application"]["witness_type_repr"]==witness["type_expr_repr"]
           and x["application"]["exact_kernel_type_match"] is True
           and x["request"]["source"] in witness["proof_constants"]
           and {p["name"] for p in x["premises"]}<=set(witness["proof_constants"]),"new witness evidence")
    routes={"collision":d["historical_routes"]["collision"]["status"],
            "alternative":d["historical_routes"]["alternative"]["status"],
            "original":"HOLD_TYPED_APPLICABILITY_REVIEW","missing":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "compatible":"REUSE_EXISTING"}
    result={"status":"R14_INDEPENDENT_PREMISE_TYPE_DISCOVERY_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":routes,"matched_combinations":{k:p["combination_count"] for k,p in d["plans"].items()},
            "reused_r13_routes":2,"new_typed_applications":1,"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,
            "candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R14_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r13-local","r13-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
