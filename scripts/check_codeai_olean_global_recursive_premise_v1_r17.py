#!/usr/bin/env python3
"""R17 globally selected polymorphic premise rules, bounded recursive Lean search."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_polymorphic_premise_v1_r16 as r16
from runtime import kuuos_codeai_olean_global_recursive_premise_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import exact_lookup
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob
from check_codeai_no_go_memory_v1_r2 import normalize

v=r16.v
r14=r16.r14
r13=r16.r13
r12=r16.r12
r8=r16.r8
r5=r14.r5
ROOT=v.ROOT
load=r16.load
RUN=45798171576
HEAD="b476b53089dad4e98e8c3de4219c297fdd0d66ef"
DIRECT="26cc41afcb94dbe708b3f9f88dd37289d37ca84c2f23c563d3731ec0ac8c2aea"
MCP="9c930ca221cae32d8ce265a4d026953ca670a1836cdf649331ba02c54d2db8a6"
ARTS=(
 (15106322210,"codeai-olean-r16-local-45798171576-1","sha256:f9cf3e716fcec31fb7b90ce399629c3a0b28153109767762cad3a2a1b5f2d853"),
 (15106871609,"codeai-olean-r16-independent-45798171576-1","sha256:7e004fa68030ac691b9aca036a7ada164506b35e95b6869e7c5ad6ce0b3db05a"),
)
def admit_r16(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R16 lineage")
    for jid,names in ((139834122963,["Verify R16 universe inference and dependent premise chain",
                                    "Actual Lean MCP R16 new application audit"]),
                      (139836964517,["Independently reconstruct R16 polymorphic premise chain and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R16 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R16 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R16_INDEPENDENT_POLYMORPHIC_PREMISE_CHAIN_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R16 evidence changed")
    return d,res

def queries():
    c=r13.c;ap=r13.ap;L=r13.LEC
    raw=c(L+".NorthNativeF55Raw");shadow=c(L+".NorthNativeF55Shadow")
    cover=c(L+".northNativeF55TwoChartCover");obs=c(L+".northNativeF55Observe")
    prod=ap("Prod",shadow,raw);read=ap(L+".sourceAwareReadout",raw,shadow,obs)
    out={}
    for k,atlas in (("refined_constant","northNativeF55TwoChartConstantRaw"),
                    ("refined_original","northNativeF55TwoChartRaw")):
        s=c(L+"."+atlas)
        readout=ap(L+".shadowSections",c("Unit"),c("Bool"),raw,prod,cover,read,s)
        target=ap(L+".Compatible",c("Unit"),c("Bool"),prod,cover,readout)
        out[k]=gate.poly.make_query(k,r13.CRITERION,L+".sourceCompatible_implies_shadowCompatible",
                                   target,"positive",[r13.F55],[])
    return out

def material(db,receipt,historical,mod,name,out):
    key=mod+"::"+name
    if key not in historical["materials"]:return r14.material(db,receipt,{"materials":{}},mod,name,out)
    req=exact_lookup(db,receipt,old.R7,old.HEAD,mod,name)
    v.need(req["status"]=="EXACT_OLEAN_MATERIALIZATION_REQUIRED","R16 material lookup")
    sources=req["coverage"]["sources"]
    v.need(len(sources)==1 and git_blob((ROOT/sources[0]["path"]).read_bytes())==sources[0]["blob"],"source changed")
    bound,why=r5.bind_files(mod,ROOT/".lake/build/lib/lean"/(mod.replace(".","/")+".olean"),sources[0])
    v.need(why is None and bound==req["binding"],"R16 artifact binding changed")
    x=historical["materials"][key]
    v.need(x["module"]==mod and x["name"]==name,"R16 material identity")
    return {"module":mod,"name":name,"type_expr_sha256":x["type_expr_sha256"],"reused_r16":True}

def probe(q,inv,out,label):
    src=gate.render(q,inv);rc,log=r12.prior.compile_source(out/(label+".lean"),src)
    if rc:print(log[-16000:],flush=True);raise ValueError("R17 search failed:"+label)
    rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(rows)==1,"search receipt")
    return rows[0]

def direct(a,out):
    hist,res=admit_r16(a.r16_local,a.r16_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    inv=gate.inventory(db,receipt,hist);v.save(out/"global-inventory.json",inv)
    qs=queries();results={};candidates={p["name"]:p for ps in inv["selected"].values() for p in ps}
    v.need(len(candidates)==sum(map(len,inv["selected"].values())),"ambiguous selected rule")
    for k,q in qs.items():
        row=probe(q,inv,out,"Search_"+k);results[k]=row
        v.save(out/(k+"-search.json"),row)
        first,replay=row["first"],row["replay"]
        v.need(first["route"]==replay["route"] and first["cache_entries"]==replay["cache_entries"]
               and replay["cache_hits"]>0,"same-context memo replay")
        v.need(row["cycle_fixture"]["route"] is None and
               row["cycle_fixture"]["trace"][0]["status"]=="HOLD_EXACT_CYCLE"
               and row["budget_fixture"]["route"] is None and
               row["budget_fixture"]["trace"][0]["status"]=="HOLD_DEPTH_BUDGET","cycle/depth fixtures")
        v.need(all(t["rule"] in candidates for t in first["trace"] if "rule" in t),"unindexed rule")
    good=results["refined_constant"];bad=results["refined_original"]
    v.need(good["first"]["route"] is not None and len(good["first"]["route"])>=2
           and bad["first"]["route"] is None,"bounded recursive control")
    v.need(good["goal_expr"]!=hist["specializations"]["constant"]["goal_expr"],"old target replayed as new")
    q=qs["refined_constant"];route=[candidates[n] for n in good["first"]["route"]]
    req,src,mcp_src=gate.application(q,route,"global_recursive_refined")
    _,w=typed.names(req);sources=[{"module":req["module"],"name":req["source"]}]+route
    names=sorted({p["name"] for p in sources}|{w})
    materials={}
    for j,p in enumerate(sources):
        key=p["module"]+"::"+p["name"]
        if key not in materials:materials[key]=material(db,receipt,hist,p["module"],p["name"],out/("exact-"+str(j)))
    src+="\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplication.lean",src)
    if rc:print(log[-16000:],flush=True);raise ValueError("R17 final application failed")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":sorted({p["name"] for p in sources}) if n==w else []}
                            for n in names])
    apps=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    v.need(len(apps)==1 and apps[0]["exact_kernel_type_match"] is True
           and apps[0]["target_expr_repr"]==good["goal_expr"],"exact target binding")
    for p in sources:
        v.need(next(x for x in rows if x["name"]==p["name"])["type_expr_sha256"]
               ==materials[p["module"]+"::"+p["name"]]["type_expr_sha256"],"imported full type changed")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"request":req,"premises":route,"observations":rows,"application":apps[0],
           "mcp_source":mcp_src+"\nset_option pp.universes false\n"+"\n".join("#check @"+n for n in names)+"\n"}
    counts={"index_rows":inv["index_rows"],"selected":sum(map(len,inv["selected"].values())),
            "selected_polymorphic":sum(bool(p["binder_count"] or p["universe_parameters"]) for p in candidates.values()),
            "deferred_matching":sum(map(len,inv["deferred_matching"].values())),
            "other_deferred":sum(inv["other_deferred_counts"].values())}
    d={"status":"R17_DIRECT_GLOBAL_RECURSIVE_PREMISE_SEARCH","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r16_direct_digest":DIRECT,"historical_routes":hist["historical_routes"],
       "r16_routes":res["routes"],"inventory_digest":old.digest(inv),"coverage":counts,
       "queries":qs,"results":results,"materials":materials,"fresh_application":fresh,
       "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R17_DIRECT",json.dumps({"direct_digest":old.digest(d),"coverage":counts,
        "route":[p["name"] for p in route],"first_trials":{k:x["first"]["cache_entries"] for k,x in results.items()},
        "replay_hits":{k:x["replay"]["cache_hits"] for k,x in results.items()},
        "cycle_controls":len(results),"budget_controls":len(results),
        "reused_complete_types":sum(x.get("reused_r16",False) for x in materials.values()),
        "new_applications":1},sort_keys=True),flush=True)
    return d

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
                                     "clientInfo":{"name":"KuuOS global recursive premise search","version":"1"}})
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
    result={"status":"R17_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R17_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R17_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R17_INDEPENDENT_GLOBAL_RECURSIVE_PREMISE_SEARCH_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"refined_constant":"REUSE_EXISTING",
            "refined_original":"HOLD_TYPED_APPLICABILITY_REVIEW"},"r16_routes":d["r16_routes"],
            "historical_routes":d["historical_routes"],"coverage":d["coverage"],"new_typed_applications":1,
            "mcp_audits":len(mp["audits"]),"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R17_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r16-local","r16-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
