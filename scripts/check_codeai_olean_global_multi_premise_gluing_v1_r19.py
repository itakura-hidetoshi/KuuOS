#!/usr/bin/env python3
"""R19 whole-index selection, exact negative controls and evidence-derived closed terminals."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_recursive_premise_v1_r17 as r17
from runtime import kuuos_codeai_olean_global_multi_premise_gluing_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r17.v
r13=r17.r13
r12=r17.r12
r8=r17.r8
ROOT=v.ROOT
load=r17.load
RUN=45806400380
HEAD="cb491b56f39081b8e08cc5b12a11feff2c793c29"
DIRECT="f0cb1d60d3ddf655123a72abb3e05e36437b1742f6a01b6e40db9b2e99a5ac36"
MCP="f6b6a9e2d83af3cd84a020a9e61f8be246bcfd27845ca2e1e1325a94db84720f"
ARTS=(
 (15110660982,"codeai-olean-r18-r2-local-45806400380-1","sha256:597c9fea8956ab7f97e0a9334f4ecca76293cbee7123a3d9254f0395c689ef9d"),
 (15110083143,"codeai-olean-r18-r2-independent-45806400380-1","sha256:68eb04b2d1aa338e2e0cae5192ff56ca8b753aa442902ff2c8db0ed2d5f9b267"),
)
def admit_r18(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R18 R2 lineage")
    for jid,names in ((139862722416,["Verify R18 R2 multi-premise gluing and exact application",
                                    "Actual Lean MCP R18 R2 new application audit"]),
                      (139865818321,["Independently reconstruct R18 R2 multi-premise gluing and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R18 R2 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R18 R2 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R18_R2_INDEPENDENT_MULTI_PREMISE_GLUING_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R18 R2 evidence changed")
    return d,res

def queries():
    c=r13.c;ap=r13.ap;L=r13.LEC
    raw=c(L+".NorthNativeF55Raw");shadow=c(L+".NorthNativeF55Shadow")
    cover=c(L+".northNativeF55TwoChartCover");obs=c(L+".northNativeF55Observe")
    prod=ap("Prod",shadow,raw);read=ap(L+".sourceAwareReadout",raw,shadow,obs)
    out={}
    for k,atlas in (("refined_observer_constant","northNativeF55TwoChartConstantRaw"),
                    ("refined_observer_original","northNativeF55TwoChartRaw")):
        s=c(L+"."+atlas)
        args=[c("Unit"),c("Bool"),raw,prod,cover,read,s]
        target=ap(L+".HasGlobal",c("Unit"),c("Bool"),raw,cover,s)
        q=gate.poly.make_query(k,r13.CRITERION,L+".shadowGlobal_and_overlapFaithful_implies_sourceGlobal",
                                  target,"positive",[r13.F55,r13.SCOPED],[])
        out[k]=(q,args)
    return out

def probe(q,args,inv,out,label):
    src=gate.render(q,args,inv);rc,log=r12.prior.compile_source(out/(label+".lean"),src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R19 search failed:"+label)
    rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(rows)==1,"search receipt")
    row=rows[0]
    v.need(row["first"]["route"]==row["replay"]["route"] and row["replay"]["cache_hits"]>0
           and row["first"]["cache_entries"]==row["replay"]["cache_entries"],"same-context replay")
    v.need(row["cycle"]["route"] is None and row["cycle"]["trace"][0]["status"]=="HOLD_EXACT_CYCLE"
           and row["budget"]["route"] is None and row["budget"]["trace"][0]["status"]=="HOLD_DEPTH_BUDGET","controls")
    v.save(out/(label+"-search.json"),row)
    # Compact actual Lean trace, including all failed rule statuses.
    trace=[{"rule":t.get("rule"),"status":t.get("status",t.get("trial",{}).get("status")),
            "residual_count":len(t.get("trial",{}).get("residuals",[]))}
           for t in row["first"]["trace"]]
    print("KUUOS_R19_SEARCH_SUMMARY",json.dumps({"case":label,
        "root_heads":row["primary"]["heads"],"route":row["first"]["route"],
        "trace":trace},sort_keys=True),flush=True)
    return row

def direct(a,out):
    hist,prior=admit_r18(a.r18_local,a.r18_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    historical=load(a.r18_local/"inventory.json")
    inv=gate.inventory(db,historical,hist);v.save(out/"inventory.json",inv)
    qs=queries();results={}
    for k,(q,args) in qs.items():
        row=probe(q,args,inv,out,k);results[k]=row
        v.need(len(row["primary"]["residuals"])==3,"root residual inventory")
        v.need((row["first"]["route"] is not None)==k.endswith("_constant"),"refined observer control:"+k)
        v.need(row["primary"]["residuals"]!=hist["results"]["global_constant" if k.endswith("_constant") else "global_original"]["primary"]["residuals"],
               "old observer replayed as new")
    good=results["refined_observer_constant"];bad=results["refined_observer_original"]
    v.need(good["first"]["route"][0]["arity"]==3,"AND root")
    oldneg=gate.LEC+"nativeF55_twoChart_not_overlapFiberFaithful"
    faith_goal=bad["primary"]["residuals"][2]
    mismatch=[t for t in bad["first"]["trace"] if t.get("rule")==oldneg and t.get("goal_expr")==faith_goal]
    v.need(len(mismatch)>0 and all(t["status"]=="HOLD_NEGATIVE_TRIAL" and t["trial"]["status"]!="MATCH_COMPLETE" for t in mismatch),
           "old-observer negative must not transfer")
    blocked=[t for t in bad["first"]["trace"] if t.get("status")=="HOLD_PENDING_EXACT_NEGATIVE_AUDIT" and
             t.get("goal_expr")==bad["primary"]["residuals"][1]]
    v.need(len(blocked)==1 and blocked[0]["rule"]==gate.LEC+"nativeF55_twoChart_refined_no_global",
           "refined premise exact negative not found")
    neg_target=bad["exact_target_negative_candidate"]
    v.need(neg_target==gate.LEC+"nativeF55_twoChart_raw_no_global","original target exact negative missing")
    appspec=[]
    q,args=qs["refined_observer_constant"]
    appspec.append(("refined_observer_constant",q,args,good["first"]["route"],good["goal_expr"]))
    q,args=qs["refined_observer_original"];r=q["request"];ap=r13.ap
    refined=ap(gate.LEC+"shadowSections",*args)
    # shadowSections has the same explicit X,I,Raw,Obs,U,q,s prefix.
    target=ap(gate.LEC+"HasGlobal",args[0],args[1],args[3],args[4],refined)
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    for k,name,tgt,expr in [
        ("negative_refined_premise",blocked[0]["rule"],target,blocked[0]["goal_expr"]),
        ("negative_original_target",neg_target,r["target"],bad["goal_expr"])]:
        p=selected[name]
        nq=gate.poly.make_query(k,p["module"],name,tgt,"negative",[],[])
        appspec.append((k,nq,[],[{"rule":name,"arity":0}],expr))
    candidates={p["name"]:p for ps in inv["selected"].values() for p in ps}
    materials={};expected={};app_rows={};source_parts=[];mcp_parts=[];used_modules=set(gate.base.MODULES)
    for k,q,args,route,expr in appspec:
        req,src,mcp_src=gate.application(q,args,route,"r19_"+k)
        _,w=typed.names(req)
        sources=[{"module":req["module"],"name":req["source"]}]
        sources += [candidates[p["rule"]] for p in route[1:]]
        used_modules.update(p["module"] for p in sources)
        refs=sorted({p["name"] for p in sources})
        expected[w]=refs
        for p in sources:
            expected.setdefault(p["name"],[])
            key=p["module"]+"::"+p["name"]
            if key not in materials:
                item=r17.material(db,receipt,hist,p["module"],p["name"],out/("exact-"+str(len(materials))))
                if item.pop("reused_r16",False):item["reused_r18"]=True
                materials[key]=item
        source_parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        app_rows[k]={"request":req,"route":route,"target_expr_repr":expr,"witness":w,"source_refs":refs}
    imports="".join("import "+m+"\n" for m in sorted(used_modules))
    names=sorted(expected)
    src=imports+"\n"+"\n".join(source_parts)+"\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplications.lean",src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R19 exact application failed")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in names])
    app_evidence=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    by_w={x["witness_name"]:x for x in app_evidence}
    v.need(len(app_evidence)==len(app_rows) and len(by_w)==len(app_rows),"application inventory")
    by_n={x["name"]:x for x in rows}
    for k,x in app_rows.items():
        obs=by_w[x["witness"]]
        v.need(obs["exact_kernel_type_match"] is True and obs["target_expr_repr"]==x["target_expr_repr"]
               and obs["witness_type_repr"]==by_n[x["witness"]]["type_expr_repr"]
               and set(x["source_refs"])<=set(by_n[x["witness"]]["proof_constants"]),"exact target binding:"+k)
        x["application"]=obs
    for p in materials.values():
        v.need(by_n[p["name"]]["type_expr_sha256"]==p["type_expr_sha256"],"imported complete type drift")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"observations":rows,"mcp_source":imports+"\n"+"\n".join(mcp_parts)+"\n"+
           "\n".join("#check @"+n for n in names)+"\n"}
    coverage={"index_rows":inv["index_rows"],"selected":sum(map(len,inv["selected"].values())),
              "capped":sum(map(len,inv["capped"].values())),"other_deferred":sum(inv["deferred_counts"].values()),
              "selected_negative":len(inv["selected"]["Not"]),"closed_recall_candidates":len(inv["closed_recall"])}
    d={"status":"R19_DIRECT_GLOBAL_MULTI_PREMISE_GLUING","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r18_direct_digest":DIRECT,"r18_mcp_digest":MCP,"prior_r18_routes":prior["routes"],
       "inventory_digest":old.digest(inv),"coverage":coverage,"results":results,"materials":materials,
       "applications":app_rows,"fresh_application":fresh,"unobserved_module_count":695,
       "semantic_search_complete":False,"proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",d)
    print("KUUOS_R19_DIRECT",json.dumps({"direct_digest":old.digest(d),"coverage":coverage,
      "applications":list(app_rows),"replay_hits":{k:x["replay"]["cache_hits"] for k,x in results.items()},
      "reused_complete_types":sum(x.get("reused_r18",False) for x in materials.values())},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS global multi premise gluing","version":"1"}})
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
    result={"status":"R19_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R19_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R19_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
           and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnosis")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[]
               and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"]
               and row["name"]==mp["audits"][j]["name"],"MCP evidence mismatch")
    result={"status":"R19_INDEPENDENT_GLOBAL_MULTI_PREMISE_GLUING_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"refined_observer_constant":"REUSE_EXISTING",
            "refined_observer_original_gluing_path":"BLOCKED_BY_REFUTED_PREMISE",
            "negative_refined_premise":"REFUTED_EXACT_PREMISE",
            "negative_original_target":"REFUTED_EXACT_TARGET",
            "old_observer_negative_for_refined_faithfulness":"HOLD_TYPED_APPLICABILITY_REVIEW"},
            "prior_r18_routes":d["prior_r18_routes"],"coverage":d["coverage"],
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R19_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r18-local","r18-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
