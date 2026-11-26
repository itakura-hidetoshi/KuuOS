#!/usr/bin/env python3
"""R15 global ranking over the certified R7 index, exact Lean checks."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_premise_type_discovery_v1_r14_r2 as r14
from runtime import kuuos_codeai_olean_global_premise_search_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import exact_lookup
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob
from check_codeai_no_go_memory_v1_r2 import normalize

v=r14.v
r13=r14.r13
r12=r14.r12
r8=r14.r8
r5=r14.r5
ROOT=v.ROOT
load=r14.load
RUN=45792026744
HEAD="a3c80aa2179f46f797fdc5b220dbf72a15d6cefe"
DIRECT="1e824afa9544ab6f8be613cec455f25196e632b3ec393d2d1e2404564ca139b8"
MCP="45f967026c129d700f11ce3588219b5638a878faeffe1b1f3a63ab8ec83a10d0"
ARTS=(
 (15103965594,"codeai-olean-r14-local-45792026744-1","sha256:b66539e958dcca4b218dfa397317e2980171705ce92f9b9dc58f766f3c926efc"),
 (15103202263,"codeai-olean-r14-independent-45792026744-1","sha256:cae1e71c92b936984abae99a8ae18036a5fceadc3c5c65ef9febca1277c0c9c0"),
)
def admit_r14(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R14 lineage")
    for jid,names in ((139813172121,["Verify R14 actual premise domains and exact Lean application",
                                    "Actual Lean MCP R14 new application audit"]),
                      (139815416075,["Independently reconstruct R14 premise type discovery and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R14 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R14 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R14_INDEPENDENT_PREMISE_TYPE_DISCOVERY_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT,"R14 evidence changed")
    comparisons={}
    for k,di in d["comparison_digests"].items():
        c=load(local/(k+"-comparisons.json"))
        v.need(c==load(independent/(k+"-comparisons.json")) and old.digest(c)==di,"R14 comparison receipt")
        comparisons[k]=c
    return d,res,comparisons

def queries():
    base=r14.queries();out={}
    for k in ("collision","alternative","original","compatible"):
        q=base[k]
        out[k]=gate.make_query(k,q["module"],q["source"],q["target"],q["fixed"],
                                q["polarity"],q["context_modules"],len(q["slot_modules"]))
    c=r13.c;ap=r13.ap
    fixed=[c("Unit"),c("Bool"),c(r13.LEC+".NorthNativeF55Shadow"),
           c(r13.LEC+".northNativeF55TwoChartCover"),c(r13.LEC+".northNativeF55TwoChartShadow")]
    out["shadow"]=gate.make_query("shadow",r13.SCOPED,r13.LEC+".global_implies_compatible",
                                   ap(r13.LEC+".Compatible",*fixed),fixed,"positive",[r13.F55],1)
    return out

def probe(q,pools,out,label):
    src=gate.render(q,pools)
    rc,log=r12.prior.compile_source(out/(label+".lean"),src)
    if rc:
        print(log[-12000:],flush=True);raise ValueError("R15 probe failed:"+label)
    rows=[json.loads(l[len(gate.local.MARK):]) for l in log.splitlines() if l.startswith(gate.local.MARK)]
    v.need(len(rows)==q["slot_count"] and [x["slot"] for x in rows]==list(range(q["slot_count"])),
           "premise feature inventory")
    return rows

def material(db,receipt,h13,h14,mod,name,out):
    key=mod+"::"+name
    if key not in h14["materials"]:return r14.material(db,receipt,h13,mod,name,out)
    req=exact_lookup(db,receipt,old.R7,old.HEAD,mod,name)
    v.need(req["status"]=="EXACT_OLEAN_MATERIALIZATION_REQUIRED","R14 material lookup")
    sources=req["coverage"]["sources"]
    v.need(len(sources)==1 and git_blob((ROOT/sources[0]["path"]).read_bytes())==sources[0]["blob"],"source changed")
    bound,why=r5.bind_files(mod,ROOT/".lake/build/lib/lean"/(mod.replace(".","/")+".olean"),sources[0])
    v.need(why is None and bound==req["binding"],"R14 artifact binding changed")
    x=h14["materials"][key]
    v.need(x["module"]==mod and x["name"]==name,"R14 material identity")
    return {"module":mod,"name":name,"type_expr_sha256":x["type_expr_sha256"],"reused_r14":True}

def direct(a,out):
    h14,res14,oldcomp=admit_r14(a.r14_local,a.r14_independent)
    h13,ctx13=r14.admit_r13(a.r13_local,a.r13_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    eligible,df,coverage=gate.catalog(db,receipt)
    v.save(out/"global-coverage.json",coverage)
    qs=queries();summary={};plans={};all_rows={};new_count=0;cached_count=0
    for k,q in qs.items():
        domains=probe(q,[[] for _ in range(q["slot_count"])],out,"Domains_"+k)
        if k in oldcomp:
            v.need([x["domain_expr_repr"] for x in domains]==[x["domain_expr_repr"] for x in oldcomp[k]],
                   "historical premise domains changed")
        ranks=[gate.rank(eligible,df,x) for x in domains]
        for j,x in enumerate(ranks):v.save(out/(k+"-rank-"+str(j)+".json"),x)
        selected=[x["selected"] for x in ranks]
        todo=[];cached=[]
        for j,pool in enumerate(selected):
            past={(x["module"],x["name"]):x for x in oldcomp[k][j]["comparisons"]} if k in oldcomp else {}
            cached.append(past)
            todo.append([p for p in pool if (p["module"],p["name"]) not in past])
        # Do not import candidate modules from historical successful or failed comparisons again.
        fresh=probe(q,todo,out,"Compare_"+k) if any(todo) else domains
        rows=[]
        for j,pool in enumerate(selected):
            v.need(fresh[j]["domain_expr_repr"]==domains[j]["domain_expr_repr"],"candidate imports changed premise domain")
            actual={(x["module"],x["name"]):x for x in fresh[j]["comparisons"]}
            v.need(set(actual)=={(x["module"],x["name"]) for x in todo[j]},"new comparison inventory")
            combined=[]
            for p in pool:
                key=(p["module"],p["name"])
                if key in cached[j]:combined.append(cached[j][key]);cached_count+=1
                else:combined.append(actual[key]);new_count+=1
            rows.append({**domains[j],"comparisons":combined})
        plan=gate.plan(q,selected,rows);plans[k]=plan;all_rows[k]=rows
        v.save(out/(k+"-comparisons.json"),rows)
        v.save(out/(k+"-plan.json"),plan)
        summary[k]={"ranked_per_slot":[x["ranked_count"] for x in ranks],
                    "ranking_digests":[x["ranking_digest"] for x in ranks],
                    "deferred_per_slot":[x["deferred_count"] for x in ranks],
                    "selected_per_slot":[len(x) for x in selected],"matches":[len(x) for x in plan["pools"]],
                    "observations_digest":old.digest(rows)}
    # Prior proof certificates are separate from the new priority queue.
    # Their target/premise identity has been rechecked; selection rank cannot erase them.
    historical={}
    for k in ("collision","alternative","compatible"):
        q=qs[k];prev=h14["queries"][k]
        v.need(all(q[z]==prev[z] for z in ("module","source","target","fixed","polarity","context_modules")),
               "historical target changed")
        if k=="compatible":
            h=h14["fresh_application"]
            historical[k]={"status":res14["routes"][k],"request_digest":h["request"]["request_digest"],
                           "target_expr_digest":old.digest(h["application"]["target_expr_repr"])}
        else:
            h=h14["historical_routes"][k]
            historical[k]={"status":h["status"],"request_digest":h["historical_request_digest"],
                           "target_expr_digest":h["target_expr_digest"]}
    q=qs["shadow"];p=plans["shadow"]
    v.need(p["combination_count"]>0,"global shadow premise not discovered within budget")
    combo=p["combinations"][0];req=gate.application(q,combo,"global_shadow_new")
    mods=sorted(set([q["module"]]+q["context_modules"]+[x["module"] for x in combo]))
    prefix="import "+q["module"]+"\n"
    def imports(src):
        v.need(src.startswith(prefix),"renderer boundary")
        return "".join("import "+m+"\n" for m in mods)+src[len(prefix):]
    _,w=typed.names(req);names=sorted({req["source"],w}|{p["name"] for p in combo})
    materials={}
    for j,p in enumerate([{"module":req["module"],"name":req["source"]}]+combo):
        key=p["module"]+"::"+p["name"]
        materials[key]=material(db,receipt,h13,h14,p["module"],p["name"],out/("exact-"+str(j)))
        if "type_expr_sha256" in p:v.need(materials[key]["type_expr_sha256"]==p["type_expr_sha256"],"matched full type")
    src=imports(typed.render(req))+"\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplication.lean",src)
    if rc:print(log[-12000:],flush=True);raise ValueError("global discovered application failed")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":[req["source"]]+[p["name"] for p in combo] if n==w else []}
                            for n in names])
    apps=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    v.need(len(apps)==1 and apps[0]["exact_kernel_type_match"] is True,"exact witness")
    for p in [{"module":req["module"],"name":req["source"]}]+combo:
        v.need(next(x for x in rows if x["name"]==p["name"])["type_expr_sha256"]
               ==materials[p["module"]+"::"+p["name"]]["type_expr_sha256"],"imported type changed")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"request":req,"premises":combo,"observations":rows,"application":apps[0],
           "mcp_source":imports(typed.declarations(req))+"\nset_option pp.universes false\n"+"\n".join("#check @"+n for n in names)+"\n",
           "pending_combination_count":plans["shadow"]["combination_count"]-1}
    result={"status":"R15_DIRECT_GLOBAL_PREMISE_SEARCH","source_head":old.HEAD,"source_tree":old.TREE,
            "scope_digest":old.SCOPE,"r14_direct_digest":DIRECT,"coverage_digest":old.digest(coverage),
            "coverage_counts":{k:coverage[k] for k in ("index_rows","eligible","excluded")},
            "queries":qs,"summary":summary,"plans":plans,"historical_routes":historical,"materials":materials,
            "fresh_application":fresh,"cached_comparisons":cached_count,"new_comparisons":new_count,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",result)
    print("KUUOS_R15_DIRECT",json.dumps({"direct_digest":old.digest(result),"coverage":result["coverage_counts"],
          "summary":summary,"cached_comparisons":cached_count,"new_comparisons":new_count,
          "reused_routes":len(historical),"new_application":req["request_digest"]},sort_keys=True),flush=True)
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
    result={"status":"R15_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R15_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R15_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    routes={k:v["status"] for k,v in d["historical_routes"].items()}
    # A candidate match alone, if any, cannot change original to REUSE.
    routes.update(original="HOLD_TYPED_APPLICABILITY_REVIEW",shadow="REUSE_EXISTING")
    result={"status":"R15_INDEPENDENT_GLOBAL_PREMISE_SEARCH_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":routes,"coverage_counts":d["coverage_counts"],
            "cached_comparisons":d["cached_comparisons"],"new_comparisons":d["new_comparisons"],
            "reused_r14_routes":3,"new_typed_applications":1,"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,
            "candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R15_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r13-local","r13-independent","r14-local","r14-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
