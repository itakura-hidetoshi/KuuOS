#!/usr/bin/env python3
"""R38: compose exact contextual positive routes and a genuine negative premise."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_extension_v2_r35 as r35
from runtime import kuuos_codeai_olean_contextual_premise_v1 as gate
from runtime import kuuos_codeai_olean_contextual_route_memory_v1 as memory
from runtime import kuuos_codeai_olean_contextual_composite_v1 as composite
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r31=r35.r31
r30=r35.r30
r29=r35.r29
r23=r35.r23
v=r35.v
ROOT=r35.ROOT
load=r35.load
RUN=45922490339
HEAD="7ce6f5af614c1b1915884a81ecc3ac9c2519a165"
ARTS=((15165092189,"codeai-olean-r35-local-45922490339-1","sha256:2c5b048b61ec7791cd43198828feae01c8070a31270d087abe691fd0029f0422"),
      (15165291644,"codeai-olean-r35-independent-45922490339-1","sha256:6201e275d0317cb9541d7e960383f98f8bdb69b197082127e5798af6892f035a"))
FILES=("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json","context-extension-v2.json","context-view-v2.json")

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R35 lineage")
    for jid,steps in ((140256190960,["Verify R35 contextual extension and exact application","Actual Lean MCP R35 new application audit"]),
                      (140257339625,["Independently reconstruct R35 contextual extension and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R35 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R35 artifact")
    d=load(a.r35_local/"direct.json");mp=load(a.r35_local/"mcp.json");ind=load(a.r35_independent/"independent.json")
    v.need(d==load(a.r35_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R35_DIRECT_CONTEXTUAL_EXTENSION" and mp["status"]=="R35_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R35_INDEPENDENT_CONTEXTUAL_EXTENSION_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and
           d["context_view_key"]==ind["context_view_key"]==gate.VIEW and
           d["extension_key"]==ind["extension_key"]==gate.LAYER and ind["parent_bytes_preserved"] is True and ind["extension_bytes_equal"] is True and
           ind["combined_context_records"]==7 and ind["registry_candidates"]==12 and ind["mcp_audits"]==21 and
           ind["new_typed_applications"]==8 and d["source_head"]==gate.CURRENT and
           d["source_tree"]==gate.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R35 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R35 audit binding")
    for name in FILES:
        v.need((a.r35_local/name).read_bytes()==(a.r35_independent/name).read_bytes(),"R35 bytes "+name)
    return d

def admit37(a,out):
    run=v.cache.api("actions/runs/45936077268")
    v.need(run["head_sha"]=="d7c54a76ac6f95c03427f083e4133b7483f5c303" and run["run_attempt"]==1 and
           run["status"]=="completed" and run["conclusion"]=="success","R37 run lineage")
    for jid,steps in ((140299473625,["Verify R37 contextual route memory and exact application","Actual Lean MCP R37 new application audit"]),
                      (140300721746,["Independently reconstruct R37 contextual route memory and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==45936077268 and j["head_sha"]=="d7c54a76ac6f95c03427f083e4133b7483f5c303" and
               j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R37 jobs")
    for aid,n,dig in ((15171170552,"codeai-olean-r37-local-45936077268-1","sha256:0eb26756af58b78b16f0b12d5af0e83e764fc624e3f39d5fdd77551ff1d07cff"),
                      (15170533288,"codeai-olean-r37-independent-45936077268-1","sha256:4effa51a26cdc13c84cd7e1b42c1f49babd73f2b6fa0468e4929635895fd927b")):
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==45936077268 and x["workflow_run"]["head_sha"]=="d7c54a76ac6f95c03427f083e4133b7483f5c303","R37 artifact")
    d=load(a.r37_local/"direct.json");mp=load(a.r37_local/"mcp.json");ind=load(a.r37_independent/"independent.json")
    v.need(d==load(a.r37_independent/"direct.json") and old.digest(d)==composite.DIRECT and
           old.digest(mp)==composite.MCP and d["status"]=="R37_DIRECT_CONTEXTUAL_ROUTE_MEMORY" and
           mp["status"]=="R37_REAL_MCP_GREEN" and mp["direct_digest"]==composite.DIRECT and
           ind["status"]=="R37_INDEPENDENT_CONTEXTUAL_ROUTE_MEMORY_GREEN" and
           ind["direct_digest"]==composite.DIRECT and ind["mcp_digest"]==composite.MCP and
           ind["parent_bytes_preserved"] is True and ind["route_layer_bytes_equal"] is True and
           ind["root_trials"]==0 and ind["route_alternatives"]==2 and ind["mcp_audits"]==25 and
           ind["new_typed_applications"]==10 and d["source_head"]==ind["source_head"]==gate.CURRENT and
           d["source_tree"]==ind["source_tree"]==gate.CURRENT_TREE and d["scope_digest"]==ind["scope_digest"]==old.SCOPE and
           d["context_view_key"]==ind["context_view_key"]==gate.VIEW and
           d["route_layer_key"]==ind["route_layer_key"]==composite.LAYER,"R37 receipt")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R37 audit binding")
    for name in FILES:
        v.need((out/name).read_bytes()==(a.r37_local/name).read_bytes()==(a.r37_independent/name).read_bytes(),"R37 immutable bytes "+name)
    name="route-layer-v1.json"
    v.need((a.r37_local/name).read_bytes()==(a.r37_independent/name).read_bytes(),"R37 route bytes")
    (out/name).write_bytes((a.r37_local/name).read_bytes())
    layer=load(out/name)
    v.need(layer["key"]==composite.LAYER==gate.portable.seal(layer)["key"] and
           layer["parent_view_key"]==gate.VIEW and layer["observed_shared_dependency"]==d["observed_shared_dependency"],"R37 layer")
    return d,layer

def direct(a,out):
    scope=r29.observe_scope()
    prior35=admit(a)
    prior30,mem,old_layer,bridge=r31.admit(a,scope)
    for name in FILES:
        (out/name).write_bytes((a.r35_local/name).read_bytes())
        if a.phase=="independent":v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R36 input bytes "+name)
    for name in ("portable-memory.json","extension.json","transport.json"):
        v.need((out/name).read_bytes()==(a.r30_local/name).read_bytes(),"historical capsule lineage "+name)
    rows=gate.base.ledger(mem,old_layer,bridge,prior30["registry"])
    v.need(old.digest(rows)==gate.prev.VIEW and rows==load(out/"ledger-view.json"),"historical ledger")
    parent=load(out/"context-memory.json");layer=load(out/"context-extension-v2.json")
    view=load(out/"context-view-v2.json")
    v.need(parent["key"]==gate.prev.KEY==gate.portable.seal(parent)["key"] and
           layer["key"]==gate.LAYER==gate.portable.seal(layer)["key"] and
           view["key"]==gate.VIEW==gate.portable.seal(view)["key"] and
           parent["transport_key"]==bridge["key"] and gate.prev.merged(parent,layer,parent,layer)==view,
           "independently admitted immutable contextual view")
    capsule=r29.admit_capsule(a)
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["source_sha256"]==r29.r24.SOURCE and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==r29.r24.SOURCE,"R23 bytes")
    v.need(r23.raw_read(folder,out,"RawR23")==capsule["raw"],"R23 full type/proof")
    r23.install(folder,manifest["files"])
    folder=a.r30_local/"capsule";man=prior30["capsule_manifest"]
    v.need(man==load(a.r30_local/"capsule-manifest.json") and man["module"]==gate.ext.MODULE and
           r30.capsule_files(folder)==man["files"] and r23.sha((folder/(gate.ext.MODULE+".lean")).read_bytes())==man["source_sha256"],"R30 bytes")
    names=sorted(prior30["raw"])
    v.need(r30.raw_read(folder,out,"RawR30",names)==prior30["raw"] and
           r30.raw_read(a.r30_independent/"capsule",out,"RawR30Independent",names)==prior30["raw"],"R30 type/proof")
    r30.install(folder,man)
    qs=gate.requests(prior35)
    log=r23.run_lean([],out/"ObserveContexts.lean",gate.cm.render(qs,view))
    observed=r29.parse(log,gate.portable.MARK);observations=r29.parse(log,gate.cm.MARK)
    by_case={x["case"]:x for x in observations};reg=view["registry"]
    hist={x["name"]:x for x in prior35["fresh_application"]["observations"]}
    live={x["name"]:x["type_expr"] for x in observed["types"]}
    expected_live={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    v.need(len(live)==len(observed["types"])==12 and live==expected_live and
           {n:gate.portable.hash_type(t) for n,t in live.items()}=={c["name"]:c["type_sha256"] for c in reg["candidates"]} and
           len(by_case)==len(observations)==len(qs)==12 and by_case==prior35["observations"],"live R35 observation drift")
    target_obs={x["case"]:x["expr"] for x in observed["targets"]}
    v.need(len(target_obs)==len(observed["targets"])==2*len(qs)+len(view["records"]),"target inventory")
    for i,(key,r) in enumerate(sorted(view["records"].items())):
        v.need(target_obs["r"+str(i)]==r["target_expr"],"stored target drift")
    decisions={k:gate.cm.decide(view,view,q,by_case[k],live,expected_live,gate.CURRENT) for k,q in qs.items()}
    v.need(decisions==prior35["decisions"],"R35 decision regression")
    pending=[k for k,r in decisions.items() if r["status"]=="HOLD_SEARCH_REQUIRED"]
    v.need(pending==["new_shadow_compat"],"unexpected fallback authorization")
    prior37,route_layer=admit37(a,out)
    v.need(prior37["observations"]==by_case and prior37["decisions"]==decisions and prior37["requests"]==qs,"R37 context binding")
    k=pending[0];q=qs[k];rawkey="new_original_compat"
    recall=memory.recall(route_layer,route_layer,view,q,by_case[k],gate.CURRENT)
    v.need(recall==prior37["recall"] and recall["status"]=="EXACT_CONTEXT_ROUTE_APPLICATION_REQUIRED","route replay")
    routes=recall["routes"]
    p=composite.plan(view,route_layer,q,by_case[k],recall,qs[rawkey],by_case[rawkey],decisions[rawkey])
    controls={}
    def rejected(label,rq,ro,rd):
        try:
            composite.plan(view,route_layer,q,by_case[k],recall,rq,ro,rd)
        except ValueError as e:
            controls[label]=str(e)
        else:raise ValueError("unlawful composite accepted "+label)
    rejected("wrong_raw_context",q,by_case[k],decisions[rawkey])
    rejected("unknown_negative",qs[rawkey],by_case[rawkey],{"status":"HOLD_SEARCH_REQUIRED"})
    rejected("positive_for_negative",qs[rawkey],by_case[rawkey],decisions["new_shadow_global"])
    v.need(controls=={"wrong_raw_context":"HOLD_COMPOSITE_CONTEXT","unknown_negative":"HOLD_COMPOSITE_NEGATIVE_PREMISE",
                      "positive_for_negative":"HOLD_COMPOSITE_NEGATIVE_PREMISE"},"composite controls")
    imports={c["module"] for c in reg["candidates"]}
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.ext.NEGATIVE_LEAF]=[]
    parts=[];mcp_parts=[];apps={}
    def application(case,req,src,mcp_src,refs,route):
        _,w=typed.names(req);expected[w]=refs
        apps[w]={"case":case,"request":req,"route":route,
                 "current_binding":old.digest({"context_view_key":view["key"],"request":qs[case],
                    "route":route,"current_head":gate.CURRENT})}
        for n in refs:expected.setdefault(n,[])
        parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        imports.add(req["module"]);imports.update(qs[case]["context_modules"])
    for case,d in sorted(decisions.items()):
        for i,c in enumerate(d["matches"]):
            req=typed.make_request("r38_"+case+"_"+str(i),c["module"],c["name"],qs[case]["target"],[],c["polarity"])
            application(case,req,typed.render(req),typed.declarations(req),[c["name"]],{"kind":"exact_context","context_key":d["context_key"]})
    for i,r in enumerate(routes):
        req,s,m=gate.application(q,r,"r38_"+k+"_"+str(i))
        refs=[r["rule"]]
        if r["premise"] is not None:
            c=r["premise"]["candidate"];refs.append(c["name"]);imports.add(c["module"])
        application(k,req,s,m,refs,r)
    positive=[w for w,a0 in apps.items() if a0["case"]==k]
    negative=[w for w,a0 in apps.items() if a0["case"]==rawkey and a0["request"]["polarity"]=="negative"]
    v.need(len(positive)==2 and len(negative)==1,"composite witness inventory")
    body,check,composite_refs=composite.declarations(p,positive,negative[0])
    parts.append(body+check);mcp_parts.append(body);imports.add(composite.MODULE)
    for n,refs in composite_refs.items():
        expected[n]=refs
        for x in refs:expected.setdefault(x,[])
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R38Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={r["name"]:r for r in audit}
    v.need("KUUOS_R38_COMPOSITE_EXACT" in log.splitlines(),"composite exact kernel type")
    for n,refs in composite_refs.items():
        v.need(set(refs)<=set(by_n[n]["proof_constants"]) and set(by_n[n]["axioms"])<={a for x in refs for a in by_n[x]["axioms"]},"composite source proof binding "+n)
    for n in list(live)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    for n,x in route_layer["source_observations"].items():
        v.need(by_n[n]==x,"route source proof drift "+n)
    v.need(memory.COMPAT in by_n[memory.GLOBAL]["proof_constants"],"shared proof dependency drift")
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==8+len(routes),"fresh applications")
    for w,a0 in apps.items():
        z=ws[w];q0=a0["request"];refs=expected[w]
        ax={a for n in refs for a in by_n[n]["axioms"]}
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==by_case[a0["case"]]["goal_expr"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and set(refs)<=set(by_n[w]["proof_constants"]) and
               set(by_n[w]["axioms"])<=ax,"fresh typed proof "+w)
        a0["application"]=z
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R38_DIRECT_CONTEXTUAL_COMPOSITE","source_head":gate.CURRENT,"source_tree":gate.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r37_direct_digest":composite.DIRECT,"r37_mcp_digest":composite.MCP,
       "context_view_key":view["key"],"route_layer_key":route_layer["key"],"requests":qs,
       "observations":by_case,"decisions":decisions,"recall":recall,"controls":controls,"applications":apps,
       "composite_plan":p,"composite_refs":composite_refs,"composite_exact_kernel_type":True,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)},
       "root_trials":0,"exact_context_comparisons":0,"capsule_rebuilds":0,"provider_calls":0,
       "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R38_DIRECT",json.dumps({"direct_digest":old.digest(d),"route_layer_key":route_layer["key"],
        "fresh_leaf_applications":len(apps),"composite_witnesses":len(composite_refs),"audits":len(audit),
        "root_trials":0,"controls":controls,"composite_exact_kernel_type":True},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual composite","version":"1"}})
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
    result={"status":"R38_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R38_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R38_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+("route-layer-v1.json",):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    result={"status":"R38_INDEPENDENT_CONTEXTUAL_COMPOSITE_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"context_view_key":d["context_view_key"],"route_layer_key":d["route_layer_key"],
            "root_trials":0,"exact_context_comparisons":0,"fresh_leaf_applications":len(d["applications"]),
            "composite_witnesses":len(d["composite_refs"]),"composite_exact_kernel_type":True,
            "mcp_audits":len(rows),"controls":d["controls"],"composite_refs":d["composite_refs"],
            "parent_bytes_preserved":True,"route_layer_bytes_equal":True,"capsule_rebuilds":0,"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R38_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r35-local","r35-independent","r30-local","r30-independent","r37-local","r37-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
