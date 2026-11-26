#!/usr/bin/env python3
"""R18 direct/actual-MCP/independent multi-premise gluing evidence."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_recursive_premise_v1_r17 as r17
from runtime import kuuos_codeai_olean_multi_premise_gluing_v1_r2 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r17.v
r13=r17.r13
r12=r17.r12
r8=r17.r8
ROOT=v.ROOT
load=r17.load
RUN=45801073560
HEAD="071b6dfdbac492bf3cc7d4f28946042afd621730"
DIRECT="158e97ec6f0fdc553d361c1693106983edfa1fb14528004abd773ed6437226d4"
MCP="c661e4d61851a1f45d71fbb0c29ed680ea40e303ff34ea5bf3e4626cc5e5dd45"
ARTS=(
 (15107965475,"codeai-olean-r17-local-45801073560-1","sha256:2b37ef4f73932621de9af6236da254fba7001b391058483bd433529343135355"),
 (15108021315,"codeai-olean-r17-independent-45801073560-1","sha256:af4ddfad53c738c488a18a585c43db4e7b6b632291a35492db04db02aba1e878"),
)
def admit_r17(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R17 lineage")
    for jid,names in ((139844122880,["Verify R17 global indexed recursive premise search and exact application",
                                    "Actual Lean MCP R17 new application audit"]),
                      (139846236921,["Independently reconstruct R17 global recursive premise search and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R17 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R17 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R17_INDEPENDENT_GLOBAL_RECURSIVE_PREMISE_SEARCH_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R17 evidence changed")
    return d,res

def queries():
    c=r13.c;ap=r13.ap;L=r13.LEC
    raw=c(L+".NorthNativeF55Raw");shadow=c(L+".NorthNativeF55Shadow")
    cover=c(L+".northNativeF55TwoChartCover");obs=c(L+".northNativeF55Observe")
    out={}
    for kind in ("compatible","global"):
        for atlas in ("constant","original"):
            s=c(L+".northNativeF55TwoChart"+("ConstantRaw" if atlas=="constant" else "Raw"))
            args=[c("Unit"),c("Bool"),raw,shadow,cover,obs,s]
            source=L+(".shadowCompatible_and_overlapFaithful_implies_sourceCompatible" if kind=="compatible"
                      else ".shadowGlobal_and_overlapFaithful_implies_sourceGlobal")
            target=ap(L+(".Compatible" if kind=="compatible" else ".HasGlobal"),c("Unit"),c("Bool"),raw,cover,s)
            k=kind+"_"+atlas
            q=gate.poly.make_query(k,r13.CRITERION,source,target,"positive",[r13.F55,r13.SCOPED],[])
            out[k]=(q,args)
    return out

def probe(q,args,inv,out,label):
    src=gate.render(q,args,inv);rc,log=r12.prior.compile_source(out/(label+".lean"),src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R18 search failed:"+label)
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
    print("KUUOS_R18_R2_SEARCH_SUMMARY",json.dumps({"case":label,
        "root_heads":row["primary"]["heads"],"route":row["first"]["route"],
        "trace":trace},sort_keys=True),flush=True)
    return row

def direct(a,out):
    hist,prior=admit_r17(a.r17_local,a.r17_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    historical=load(a.r17_local/"global-inventory.json")
    inv=gate.inventory(db,historical,hist)
    # This leaf was part of R17's independently verified source inventory.
    # Do not equate a cycle with a proof unless this admitted closed source
    # independently specializes to the repeated goal with no residuals.
    key=r13.F55+"::"+gate.CLOSED_RECALL
    v.need(key in hist["materials"] and hist["materials"][key]["name"]==gate.CLOSED_RECALL,
           "R17 closed recall source missing")
    inv["closed_recall"]=[gate.CLOSED_RECALL]
    v.save(out/"inventory.json",inv)
    qs=queries();results={}
    for k,(q,args) in qs.items():
        results[k]=probe(q,args,inv,out,k)
        expected=2 if k.startswith("compatible") else 3
        v.need(len(results[k]["primary"]["residuals"])==expected,"root residual inventory")
        v.need((results[k]["first"]["route"] is not None)==k.endswith("_constant"),"multi-premise control:"+k)
    missing=copy.deepcopy(inv);missing["selected"][gate.LEC+"OverlapFiberFaithful"]=[]
    missing["selected"]["Not"]=[]
    q,args=qs["compatible_constant"]
    results["missing"]=probe(q,args,missing,out,"missing")
    wrong=copy.deepcopy(inv);wrong["selected"]["Not"]=[]
    wrong["selected"][gate.LEC+"OverlapFiberFaithful"]=[
        x for x in wrong["selected"][gate.LEC+"OverlapFiberFaithful"]
        if x["name"]==gate.LEC+"nativeF55_constant_twoChart_overlapFiberFaithful"]
    v.need(len(wrong["selected"][gate.LEC+"OverlapFiberFaithful"])==1,"wrong source fixture")
    q,args=qs["compatible_original"]
    results["wrong_atlas"]=probe(q,args,wrong,out,"wrong_atlas")
    v.need(all(results[k]["first"]["route"] is None for k in ("missing","wrong_atlas")),"incomplete branches must HOLD")
    bad=results["compatible_original"]
    neg_name=gate.LEC+"nativeF55_twoChart_not_overlapFiberFaithful"
    blockers=[x for x in bad["first"]["trace"] if x.get("status")=="HOLD_PENDING_EXACT_NEGATIVE_AUDIT"
              and x.get("rule")==neg_name and x["goal_expr"] in bad["primary"]["residuals"]]
    v.need(len(blockers)>0,"exact premise negative candidate missing")
    neg_target=bad["exact_target_negative_candidate"]
    v.need(neg_target==gate.LEC+"nativeF55_twoChart_raw_incompatible","exact target negative candidate missing")
    # Positive witnesses must traverse the designated AND root. Negative
    # witnesses are separately compiled and never inferred from route failure.
    appspec=[]
    for k in ("compatible_constant","global_constant"):
        q,args=qs[k];route=results[k]["first"]["route"]
        v.need(route[0]["arity"]==(2 if k.startswith("compatible") else 3),"root arity")
        appspec.append((k,q,args,route,results[k]["goal_expr"]))
    q,args=qs["compatible_original"];r=q["request"];c=r13.c;ap=r13.ap
    faith=ap(gate.LEC+"OverlapFiberFaithful",*args)
    for k,name,target,expr,mod in [
        ("negative_premise",neg_name,faith,blockers[0]["goal_expr"],r13.CRITERION),
        ("negative_target",neg_target,r["target"],bad["goal_expr"],r13.F55)]:
        nq=gate.poly.make_query(k,mod,name,target,"negative",[r13.CRITERION,r13.F55] if mod!=r13.CRITERION else [r13.F55],[])
        appspec.append((k,nq,[],[{"rule":name,"arity":0}],expr))
    candidates={p["name"]:p for ps in inv["selected"].values() for p in ps}
    materials={};expected={};app_rows={};source_parts=[];mcp_parts=[]
    for k,q,args,route,expr in appspec:
        req,src,mcp_src=gate.application(q,args,route,"r18_"+k)
        _,w=typed.names(req)
        sources=[{"module":req["module"],"name":req["source"]}]
        sources += [candidates[p["rule"]] for p in route[1:]]
        refs=sorted({p["name"] for p in sources})
        expected[w]=refs
        for p in sources:
            expected.setdefault(p["name"],[])
            key=p["module"]+"::"+p["name"]
            if key not in materials:
                item=r17.material(db,receipt,hist,p["module"],p["name"],out/("exact-"+str(len(materials))))
                if item.pop("reused_r16",False):item["reused_r17"]=True
                materials[key]=item
        source_parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        app_rows[k]={"request":req,"route":route,"target_expr_repr":expr,"witness":w,"source_refs":refs}
    imports="".join("import "+m+"\n" for m in gate.MODULES)
    names=sorted(expected)
    src=imports+"\n"+"\n".join(source_parts)+"\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplications.lean",src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R18 exact application failed")
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
    d={"status":"R18_R2_DIRECT_MULTI_PREMISE_GLUING","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r17_direct_digest":DIRECT,"r17_mcp_digest":MCP,"r17_routes":prior["routes"],
       "inventory_digest":old.digest(inv),"results":results,"materials":materials,"applications":app_rows,
       "fresh_application":fresh,"unobserved_module_count":695,"semantic_search_complete":False,
       "proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",d)
    print("KUUOS_R18_R2_DIRECT",json.dumps({"direct_digest":old.digest(d),
      "scoped_rows":inv["scoped_rows"],"selected":len(candidates),"applications":list(app_rows),
      "root_arities":{k:len(results[k]["primary"]["residuals"]) for k in qs},
      "replay_hits":{k:x["replay"]["cache_hits"] for k,x in results.items()},
      "reused_complete_types":sum(x.get("reused_r17",False) for x in materials.values())},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS multi premise gluing","version":"1"}})
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
    result={"status":"R18_R2_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R18_R2_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R18_R2_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R18_R2_INDEPENDENT_MULTI_PREMISE_GLUING_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"compatible_constant":"REUSE_EXISTING",
            "global_constant":"REUSE_EXISTING","missing":"HOLD","wrong_atlas":"HOLD",
            "original_compatible_gluing_path":"BLOCKED_BY_REFUTED_PREMISE",
            "original_global_gluing_path":"HOLD","negative_premise":"REFUTED_EXACT_PREMISE",
            "negative_target":"REFUTED_EXACT_TARGET"},"new_typed_applications":len(d["applications"]),
            "mcp_audits":len(rows),"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R18_R2_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r17-local","r17-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
