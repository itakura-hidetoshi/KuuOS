#!/usr/bin/env python3
"""R20 unnamed root discovery from admitted R19 candidates and fixed context."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_recursive_premise_v1_r17 as r17
from runtime import kuuos_codeai_olean_root_discovery_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r17.v
r13=r17.r13
r12=r17.r12
r8=r17.r8
ROOT=v.ROOT
load=r17.load
RUN=45808574796
HEAD="d13c2955f4082fcbef39a5ee13c5b6fbb5e65f14"
DIRECT="877320fd21de02f54cd57383dabbb584285352bc4e8333fc5252badbf84858ca"
MCP="a305cd7d8fbe2d2ca4a26413951a2e0c34653470fd61b219c3a8f7a25d2d2354"
ARTS=(
 (15109949060,"codeai-olean-r19-local-45808574796-1","sha256:ba7ede973fb34b04d87f5ceb7483eca72d2d578606f576e58d09165750155755"),
 (15112510661,"codeai-olean-r19-independent-45808574796-1","sha256:57e6245feac99385a12cc943c4ca2fb005cbd8e094c06e30f93b29df008ac867"),
)
def admit_r19(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R19 lineage")
    for jid,names in ((139870172718,["Verify R19 multi-premise gluing and exact application",
                                    "Actual Lean MCP R19 new application audit"]),
                      (139872712600,["Independently reconstruct R19 multi-premise gluing and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R19 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R19 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R19_INDEPENDENT_GLOBAL_MULTI_PREMISE_GLUING_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R19 evidence changed")
    return d,res

def queries():
    c=r13.c;ap=r13.ap;L=r13.LEC
    raw=c(L+".NorthNativeF55Raw");shadow=c(L+".NorthNativeF55Shadow")
    cover=c(L+".northNativeF55TwoChartCover");obs=c(L+".northNativeF55Observe")
    prod=ap("Prod",shadow,raw);read=ap(L+".sourceAwareReadout",raw,shadow,obs)
    s=c(L+".northNativeF55TwoChartConstantRaw");orig=c(L+".northNativeF55TwoChartRaw")
    X=c("Unit");I=c("Bool")
    prefix=[X,I,raw,prod,cover,read,s]
    mods=[r13.CRITERION,r13.F55,r13.SCOPED]
    target=ap(L+".Compatible",X,I,raw,cover,s)
    refined=ap(L+".shadowSections",*prefix)
    refined_orig=ap(L+".shadowSections",*prefix[:-1],orig)
    identity=ap("id",prod)
    return {
        "local_refined_context":gate.make_request("local_refined_context",target,prefix,mods),
        "wrong_source_context":gate.make_request("wrong_source_context",target,prefix[:-1]+[orig],mods),
        "global_identity_context":gate.make_request("global_identity_context",
            ap(L+".HasGlobal",X,I,prod,cover,refined),[X,I,prod,prod,cover,identity,refined],mods),
        "original_refined_global":gate.make_request("original_refined_global",
            ap(L+".HasGlobal",X,I,prod,cover,refined_orig),[X,I,prod,prod,cover,identity,refined_orig],mods)
    }

def probe(q,inv,out,k):
    src=gate.render(q,inv);rc,log=r12.prior.compile_source(out/(k+".lean"),src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R20 search failed:"+k)
    rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(rows)==1,"root discovery receipt")
    row=rows[0]
    v.need("source" not in q and len(row["root_trials"])==len(inv["selected"][row["root_head"]]),
           "root discovery inventory")
    v.need({t["rule"] for t in row["root_trials"]}=={p["name"] for p in inv["selected"][row["root_head"]]},
           "root selection changed")
    for b in row["branches"]:
        v.need(b["first"]["route"]==b["replay"]["route"] and
            b["first"]["cache_entries"]==b["replay"]["cache_entries"] and b["replay"]["cache_hits"]>0,
            "same-context replay")
        v.need(b["cycle"]["route"] is None and b["cycle"]["trace"][0]["status"]=="HOLD_EXACT_CYCLE" and
            b["budget"]["route"] is None and b["budget"]["trace"][0]["status"]=="HOLD_DEPTH_BUDGET",
            "cycle/depth control")
    v.save(out/(k+"-search.json"),row)
    print("KUUOS_R20_ROOT_SUMMARY",json.dumps({"case":k,"root_head":row["root_head"],
        "root_trials":[{"name":t["rule"],"status":t["trial"]["status"],"eligible":t["eligible"]} for t in row["root_trials"]],
        "route":row["chosen"]["route"],"negative":row["exact_target_negative_candidate"]},sort_keys=True),flush=True)
    return row

def direct(a,out):
    hist,prior=admit_r19(a.r19_local,a.r19_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    historical=load(a.r19_local/"inventory.json")
    inv=gate.inventory(historical,hist);v.save(out/"inventory.json",inv)
    qs=queries();results={}
    for k,q in qs.items():results[k]=probe(q,inv,out,k)
    appspec=[]
    for k,arity in (("local_refined_context",2),("global_identity_context",3)):
        row=results[k];route=row["chosen"]["route"]
        v.need(route is not None and route[0]["arity"]==arity and row["exact_target_negative_candidate"] is None,
               "root discovery failed:"+k)
        v.need(any(t["rule"]==route[0]["rule"] and t["eligible"] for t in row["root_trials"]),"unselected root")
        appspec.append((k,qs[k],route,row["goal_expr"]))
    wrong=results["wrong_source_context"]
    v.need(wrong["chosen"]["route"] is None and wrong["exact_target_negative_candidate"] is None and
           not any(t["eligible"] for t in wrong["root_trials"]),"different source context must HOLD")
    bad=results["original_refined_global"];oldneg=hist["applications"]["negative_refined_premise"]
    v.need(bad["chosen"]["route"] is None and bad["exact_target_negative_candidate"]==oldneg["request"]["source"]
           and bad["goal_expr"]==oldneg["target_expr_repr"]
           and oldneg["application"]["exact_kernel_type_match"] is True
           and prior["routes"]["negative_refined_premise"]=="REFUTED_EXACT_PREMISE",
           "exact prior negative witness reuse")
    candidates={p["name"]:p for ps in inv["selected"].values() for p in ps}
    materials={};expected={};app_rows={};source_parts=[];mcp_parts=[];used_modules=set(gate.base.MODULES)
    for k,q,route,expr in appspec:
        req,src,mcp_src=gate.application(q,inv,route,"r20_"+k)
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
                if item.pop("reused_r16",False):item["reused_r19"]=True
                materials[key]=item
        source_parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        app_rows[k]={"request":req,"route":route,"target_expr_repr":expr,"witness":w,"source_refs":refs}
    imports="".join("import "+m+"\n" for m in sorted(used_modules))
    names=sorted(expected)
    src=imports+"\n"+"\n".join(source_parts)+"\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplications.lean",src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R20 exact application failed")
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
              "closed_recall_candidates":len(inv["closed_recall"]),
              "root_trials":sum(len(x["root_trials"]) for x in results.values())}
    d={"status":"R20_DIRECT_ROOT_DISCOVERY","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r19_direct_digest":DIRECT,"r19_mcp_digest":MCP,"prior_r19_routes":prior["routes"],
       "inventory_digest":old.digest(inv),"coverage":coverage,"requests":qs,"results":results,"materials":materials,
       "applications":app_rows,"fresh_application":fresh,"reused_exact_negative":oldneg,
       "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",d)
    print("KUUOS_R20_DIRECT",json.dumps({"direct_digest":old.digest(d),"coverage":coverage,
      "applications":list(app_rows),"reused_complete_types":sum(x.get("reused_r19",False) for x in materials.values()),
      "reused_exact_negative":True},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS root discovery","version":"1"}})
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
    result={"status":"R20_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R20_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R20_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R20_INDEPENDENT_ROOT_DISCOVERY_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"local_refined_context":"REUSE_EXISTING",
            "global_identity_context":"REUSE_EXISTING",
            "wrong_source_context":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "original_refined_global":"REFUTED_EXACT_TARGET_REUSED_R19"},
            "prior_r19_routes":d["prior_r19_routes"],"coverage":d["coverage"],
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R20_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r19-local","r19-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
