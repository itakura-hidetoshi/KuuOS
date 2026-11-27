#!/usr/bin/env python3
"""R35: append two certified contexts and independently reapply the combined view."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_fallback_v1_r34 as r34
from runtime import kuuos_codeai_olean_contextual_extension_v2 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r33=r34.r33
r32=r34.r32
r31=r34.r31
r30=r34.r30
r29=r34.r29
r23=r34.r23
v=r34.v
ROOT=r34.ROOT
load=r34.load
RUN=45919551835
HEAD="1ca66316713b65d7f0e809526302520a277f4e36"
ARTS=((15164356538,"codeai-olean-r34-local-45919551835-1","sha256:6730ab11135dbe872905ce2a7d0953dccd2b74a02c55ae3e3740221589e04466"),
      (15164516306,"codeai-olean-r34-independent-45919551835-1","sha256:5b85ac562b9910ad47844a32324d2eb0c4cd253372042ec42bfca9fae43ba141"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R34 lineage")
    for jid,steps in ((140246750560,["Verify R34 contextual fallback and exact application","Actual Lean MCP R34 new application audit"]),
                      (140248297497,["Independently reconstruct R34 contextual fallback and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R34 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R34 artifact")
    d=load(a.r34_local/"direct.json");mp=load(a.r34_local/"mcp.json");ind=load(a.r34_independent/"independent.json")
    v.need(d==load(a.r34_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R34_DIRECT_CONTEXTUAL_FALLBACK" and mp["status"]=="R34_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R34_INDEPENDENT_CONTEXTUAL_FALLBACK_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and
           d["context_memory_key"]==ind["context_memory_key"]==gate.KEY and ind["memory_bytes_equal"] is True and
           d["parent_ledger_view"]==ind["parent_ledger_view"]==gate.VIEW and ind["mcp_audits"]==21 and
           ind["fallback_requests"]==2 and ind["new_typed_applications"]==8 and
           d["source_head"]==gate.CURRENT and d["source_tree"]==gate.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R34 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R34 audit binding")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json"):
        v.need((a.r34_local/name).read_bytes()==(a.r34_independent/name).read_bytes(),"R34 bytes "+name)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    latest,latest_mp,latest_ind=admit(a)
    last=r34.admit(a)
    previous,mp,ind=r33.admit(a)
    r32.admit(a)
    prior,mem,layer,bridge=r31.admit(a,scope)
    reg=prior["registry"];rows=gate.base.ledger(mem,layer,bridge,reg)
    for name in ("portable-memory.json","extension.json","transport.json"):
        (out/name).write_bytes((a.r30_local/name).read_bytes())
        if a.phase=="independent":v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R31 ledger bytes")
    v.need(old.digest(rows)==gate.VIEW and rows==load(a.r31_local/"ledger-view.json"),"admitted ledger view")
    for name in ("portable-memory.json","extension.json","transport.json"):
        v.need((a.r30_local/name).read_bytes()==(a.r31_local/name).read_bytes(),"historical ledger bytes")
    v.save(out/"ledger-view.json",rows)
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((out/name).read_bytes()==(a.r33_local/name).read_bytes(),"R33 inherited bytes")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((out/name).read_bytes()==(a.r32_local/name).read_bytes(),"R32 inherited ledger bytes")
    capsule=r29.admit_capsule(a)
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["source_sha256"]==r29.r24.SOURCE and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==r29.r24.SOURCE,"R23 exact bytes")
    v.need(r23.raw_read(folder,out,"RawR23")==capsule["raw"],"R23 raw proof")
    r23.install(folder,manifest["files"])
    folder=a.r30_local/"capsule";man=prior["capsule_manifest"]
    v.need(man==load(a.r30_local/"capsule-manifest.json") and man["module"]==gate.ext.MODULE and
           r30.capsule_files(folder)==man["files"] and r23.sha((folder/(gate.ext.MODULE+".lean")).read_bytes())==man["source_sha256"],"R30 capsule bytes")
    names=sorted(prior["raw"])
    v.need(r30.raw_read(folder,out,"RawR30",names)==prior["raw"] and
           r30.raw_read(a.r30_independent/"capsule",out,"RawR30Independent",names)==prior["raw"],"R30 complete type/proof equality")
    r30.install(folder,man)
    hist={x["name"]:x for x in prior["fresh_application"]["observations"]}
    types={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    trusted=gate.cm.projection(previous,mp,ind,reg,rows,bridge)
    memory=load(a.r33_local/"context-memory.json")
    v.need(memory==trusted and memory["key"]==gate.KEY==gate.portable.seal(memory)["key"],"admitted context memory")
    (out/"context-memory.json").write_bytes((a.r33_local/"context-memory.json").read_bytes())
    if a.phase=="independent":
        v.need((out/"context-memory.json").read_bytes()==(a.first/"context-memory.json").read_bytes(),"context memory bytes")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json"):
        v.need((out/name).read_bytes()==(a.r34_local/name).read_bytes(),"R34 inherited bytes")
    parent=memory
    trusted_layer=gate.projection(parent,latest,latest_mp,latest_ind)
    layer=load(a.first/"context-extension-v2.json") if a.phase=="independent" else trusted_layer
    view=gate.merged(parent,layer,trusted,trusted_layer)
    v.save(out/"context-extension-v2.json",layer)
    v.save(out/"context-view-v2.json",view)
    if a.phase=="independent":
        for n in ("context-extension-v2.json","context-view-v2.json"):
            v.need((out/n).read_bytes()==(a.first/n).read_bytes(),"extension exact bytes "+n)
    v.need(all(view["records"][k]==r for k,r in parent["records"].items()) and
           view["historical_holds"]==parent["historical_holds"] and
           (out/"context-memory.json").read_bytes()==(a.r33_local/"context-memory.json").read_bytes(),"parent unchanged")
    def rejected(bad,expected):
        try:gate.merged(parent,bad,trusted,trusted_layer)
        except ValueError as e:
            v.need(str(e)==expected,"wrong layer hold");return str(e)
        raise ValueError("forged layer admitted")
    bad=copy.deepcopy(layer);bad["additions"]={}
    controls={"tampered":rejected(bad,"HOLD_LAYER_INTEGRITY"),
              "resealed":rejected(gate.portable.seal(bad),"HOLD_UNADMITTED_LAYER")}
    qs=gate.requests(latest)
    log=r23.run_lean([],out/"ObserveExtendedContexts.lean",gate.cm.render(qs,view))
    observed=r29.parse(log,gate.portable.MARK);observations=r29.parse(log,gate.cm.MARK)
    by_case={x["case"]:x for x in observations};reg=view["registry"]
    hist={x["name"]:x for x in latest["fresh_application"]["observations"]}
    live={x["name"]:x["type_expr"] for x in observed["types"]}
    expected_live={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    v.need(len(live)==len(observed["types"])==12 and live==expected_live and
           {n:gate.portable.hash_type(t) for n,t in live.items()}=={c["name"]:c["type_sha256"] for c in reg["candidates"]} and
           len(by_case)==len(observations)==len(qs)==12 and set(by_case)==set(qs),"live source/context inventory")
    target_obs={x["case"]:x["expr"] for x in observed["targets"]}
    v.need(len(target_obs)==len(observed["targets"])==2*len(qs)+len(view["records"]),"live target inventory")
    for i,(k,q) in enumerate(sorted(qs.items())):
        v.need(target_obs["q"+str(i)]==by_case[k]["goal_expr"] and target_obs["e"+str(i)]==by_case[k]["context_goal_expr"],"query observation")
        if k in latest["observations"]:
            oldobs=latest["observations"][k];now=by_case[k]
            v.need(all(now[f]==oldobs[f] for f in ("goal_expr","context_goal_expr","target_aligned","context_exprs")),"R34 context drift "+k)
    for i,(key,r) in enumerate(sorted(view["records"].items())):
        v.need(target_obs["r"+str(i)]==r["target_expr"],"stored target drift")
    decisions={k:gate.cm.decide(view,view,q,by_case[k],live,expected_live,gate.CURRENT) for k,q in qs.items()}
    held={"wrong_source","wrong_observer","wrong_shadow_as_raw","wrong_raw_observer"}
    for k,r in decisions.items():
        status="HOLD_CONTEXT_MISMATCH" if k in held else "HOLD_SEARCH_REQUIRED" if k=="new_shadow_compat" else "EXACT_CONTEXT_APPLICATION_REQUIRED"
        v.need(r["status"]==status,"extended memory outcome "+k+" "+json.dumps(r,sort_keys=True))
        if status=="EXACT_CONTEXT_APPLICATION_REQUIRED":
            v.need(view["records"][r["context_key"]]["case"]==k and r["candidate_comparison_searches"]==0,"wrong record reused")
    v.need(len(decisions["global"]["matches"])==2 and
           [c["polarity"] for c in decisions["new_original_compat"]["matches"]]==["negative"] and
           [c["polarity"] for c in decisions["new_shadow_global"]["matches"]]==["positive"] and
           by_case["wrong_raw_observer"]["target_aligned"] and not by_case["wrong_raw_observer"]["context_matches"] and
           not by_case["wrong_shadow_as_raw"]["target_aligned"],"source/shadow distinction")
    stale=copy.deepcopy(live);stale[next(iter(stale))]="drift"
    q=qs["new_original_compat"];obs=by_case["new_original_compat"]
    controls["live_type"]=gate.cm.decide(view,view,q,obs,stale,expected_live,gate.CURRENT)["status"]
    controls["old_head"]=gate.cm.decide(view,view,q,obs,live,expected_live,old.HEAD)["status"]
    v.need(controls["live_type"]=="HOLD_SOURCE_TYPE_DRIFT" and controls["old_head"]=="HOLD_CURRENT_SCOPE","live scope controls")
    imports={c["module"] for c in reg["candidates"]}
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.ext.NEGATIVE_LEAF]=[]
    parts=[];mcp_parts=[];apps={}
    for k,r in sorted(decisions.items()):
        for i,c in enumerate(r["matches"]):
            q=qs[k];req=typed.make_request("r35_"+k+"_"+str(i),c["module"],c["name"],q["target"],[],c["polarity"])
            _,w=typed.names(req);expected[w]=[c["name"]]
            apps[w]={"case":k,"request":req,"context_key":r["context_key"],
                     "current_binding":old.digest({"context_view_key":view["key"],"request":q,
                        "context_key":r["context_key"],"current_head":gate.CURRENT})}
            parts.append(typed.render(req).split("\n",1)[1])
            mcp_parts.append(typed.declarations(req).split("\n",1)[1])
            imports.update(q["context_modules"])
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R35Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={r["name"]:r for r in audit}
    for n in list(live)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==8,"fresh witness inventory")
    for w,a0 in apps.items():
        z=ws[w];q=a0["request"]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==by_case[a0["case"]]["goal_expr"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and q["source"] in by_n[w]["proof_constants"] and
               set(by_n[w]["axioms"])<=set(by_n[q["source"]]["axioms"]),"typed proof "+w)
        a0["application"]=z
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R35_DIRECT_CONTEXTUAL_EXTENSION","source_head":gate.CURRENT,"source_tree":gate.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r34_direct_digest":gate.DIRECT,"r34_mcp_digest":gate.MCP,
       "parent_memory_key":parent["key"],"extension_key":layer["key"],"context_view_key":view["key"],
       "parent_ledger_view":gate.VIEW,"transport_key":bridge["key"],"requests":qs,"observations":by_case,
       "decisions":decisions,"applications":apps,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)},
       "parent_context_records":len(parent["records"]),"new_context_records":len(layer["additions"]),
       "combined_context_records":len(view["records"]),"registry_candidates":len(reg["candidates"]),
       "context_holds":len(held),"candidate_comparison_searches":0,"root_searches":0,
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R35_DIRECT",json.dumps({"direct_digest":old.digest(d),"extension_key":layer["key"],"context_view_key":view["key"],
       "parent_context_records":d["parent_context_records"],"new_context_records":d["new_context_records"],
       "combined_context_records":d["combined_context_records"],"registry_candidates":d["registry_candidates"],
       "context_holds":d["context_holds"],"fresh_applications":len(apps),"audits":len(audit),
       "routes":{k:r["status"] for k,r in decisions.items()},"controls":controls,
       "candidate_comparison_searches":0,"root_searches":0,"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual extension","version":"1"}})
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
    result={"status":"R35_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R35_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R35_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json","context-extension-v2.json","context-view-v2.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    result={"status":"R35_INDEPENDENT_CONTEXTUAL_EXTENSION_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "parent_memory_key":d["parent_memory_key"],"extension_key":d["extension_key"],"context_view_key":d["context_view_key"],
            "parent_context_records":d["parent_context_records"],"new_context_records":d["new_context_records"],
            "combined_context_records":d["combined_context_records"],"registry_candidates":d["registry_candidates"],
            "context_holds":d["context_holds"],"new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),
            "routes":{k:("REFUTED_EXACT_CONTEXT" if x["matches"][0]["polarity"]=="negative" else "REUSE_EXACT_CONTEXT")
                      if x["status"]=="EXACT_CONTEXT_APPLICATION_REQUIRED" else x["status"] for k,x in d["decisions"].items()},
            "controls":d["controls"],"parent_bytes_preserved":True,"extension_bytes_equal":True,
            "candidate_comparison_searches":0,"root_searches":0,"capsule_rebuilds":0,"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R35_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r34-local","r34-independent","r33-local","r33-independent","r32-local","r32-independent","r31-local","r31-independent","r30-local","r30-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
