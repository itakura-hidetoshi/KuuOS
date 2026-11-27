#!/usr/bin/env python3
"""R33: persist R32 context-bound evidence and reapply without searching."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_root_recall_v1_r32 as r32
from runtime import kuuos_codeai_olean_contextual_memory_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r31=r32.r31
r30=r32.r30
r29=r32.r29
r23=r32.r23
v=r32.v
ROOT=r32.ROOT
load=r32.load
RUN=45911864187
HEAD="5f32ba167457c15b8d806874c429d1e6fb4c37c5"
ARTS=((15161111445,"codeai-olean-r32-local-45911864187-1","sha256:48f7670a5c4d310f21cd0dcde41bd4d386170a12fc31c2a3ca487e5af72c07d4"),
      (15160289185,"codeai-olean-r32-independent-45911864187-1","sha256:85846761c7683f118415cce7f3e79b4a875caf907d8a16818a18b7b30a2c4c74"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R32 lineage")
    for jid,steps in ((140221870219,["Verify R32 contextual root recall and exact application","Actual Lean MCP R32 new application audit"]),
                      (140223541352,["Independently reconstruct R32 contextual root recall and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R32 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R32 artifact")
    d=load(a.r32_local/"direct.json");mp=load(a.r32_local/"mcp.json");ind=load(a.r32_independent/"independent.json")
    v.need(d==load(a.r32_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R32_DIRECT_CONTEXTUAL_ROOT_RECALL" and mp["status"]=="R32_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R32_INDEPENDENT_CONTEXTUAL_ROOT_RECALL_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and
           d["ledger_view_digest"]==ind["ledger_view_digest"]==gate.VIEW and ind["mcp_audits"]==17 and
           ind["new_typed_applications"]==6 and ind["context_holds"]==2 and
           d["source_head"]==gate.CURRENT and d["source_tree"]==gate.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R32 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R32 audit binding")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((a.r32_local/name).read_bytes()==(a.r32_independent/name).read_bytes(),"R32 exact bytes "+name)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    previous,mp,ind=admit(a)
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
    trusted=gate.projection(previous,mp,ind,reg,rows,bridge)
    memory=load(a.first/"context-memory.json") if a.phase=="independent" else trusted
    v.need(memory==trusted and memory["key"]==gate.portable.seal(memory)["key"],"context memory transport")
    v.save(out/"context-memory.json",memory)
    if a.phase=="independent":
        v.need((out/"context-memory.json").read_bytes()==(a.first/"context-memory.json").read_bytes(),"context memory bytes")
    qs=gate.requests(previous)
    log=r23.run_lean([],out/"ObserveContexts.lean",gate.render(qs,memory))
    observed=r29.parse(log,gate.portable.MARK)
    observations=r29.parse(log,gate.MARK)
    by_case={x["case"]:x for x in observations}
    reg=memory["registry"]
    hist={x["name"]:x for x in previous["fresh_application"]["observations"]}
    live={x["name"]:x["type_expr"] for x in observed["types"]}
    expected_live={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    v.need(len(live)==len(observed["types"])==10 and live==expected_live and
           {n:gate.portable.hash_type(t) for n,t in live.items()}=={c["name"]:c["type_sha256"] for c in reg["candidates"]} and
           len(by_case)==len(observations)==len(qs) and set(by_case)==set(qs),"live source/context inventory")
    target_obs={x["case"]:x["expr"] for x in observed["targets"]}
    v.need(len(target_obs)==len(observed["targets"])==2*len(qs)+len(memory["records"]),"live target inventory")
    for i,(k,q) in enumerate(sorted(qs.items())):
        v.need(target_obs["q"+str(i)]==by_case[k]["goal_expr"] and target_obs["e"+str(i)]==by_case[k]["context_goal_expr"],"query observation")
    for i,(key,r) in enumerate(sorted(memory["records"].items())):
        v.need(target_obs["r"+str(i)]==r["target_expr"],"historical goal drift")
    decisions={k:gate.decide(memory,trusted,q,by_case[k],live,expected_live,gate.CURRENT) for k,q in qs.items()}
    for k,r in decisions.items():
        status="HOLD_CONTEXT_MISMATCH" if k in ("wrong_source","wrong_observer") else "HOLD_SEARCH_REQUIRED" if k=="new_original_compat" else "EXACT_CONTEXT_APPLICATION_REQUIRED"
        v.need(r["status"]==status,"context memory outcome "+k+" "+json.dumps(r,sort_keys=True))
        if status=="EXACT_CONTEXT_APPLICATION_REQUIRED":
            v.need(memory["records"][r["context_key"]]["case"]==k and r["candidate_comparison_searches"]==0,"wrong record reused")
    v.need(len(decisions["global"]["matches"])==2 and
           [c["polarity"] for c in decisions["faithful_constant"]["matches"]]==["positive"] and
           [c["polarity"] for c in decisions["faithful_original"]["matches"]]==["negative"],"positive/negative alternatives")
    forged=copy.deepcopy(memory);forged["records"]={}
    stale=copy.deepcopy(live);stale[next(iter(stale))]="drift"
    q=qs["local"];obs=by_case["local"]
    controls={"tampered":gate.decide(forged,trusted,q,obs,live,expected_live,gate.CURRENT)["status"],
              "resealed":gate.decide(gate.portable.seal(forged),trusted,q,obs,live,expected_live,gate.CURRENT)["status"],
              "old_head":gate.decide(memory,trusted,q,obs,live,expected_live,old.HEAD)["status"],
              "live_type":gate.decide(memory,trusted,q,obs,stale,expected_live,gate.CURRENT)["status"]}
    v.need(controls=={"tampered":"HOLD_MEMORY_INTEGRITY","resealed":"HOLD_UNADMITTED_MEMORY",
                      "old_head":"HOLD_CURRENT_SCOPE","live_type":"HOLD_SOURCE_TYPE_DRIFT"},"memory controls")
    imports={c["module"] for c in reg["candidates"]}
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.ext.NEGATIVE_LEAF]=[]
    parts=[];mcp_parts=[];apps={}
    for k,r in sorted(decisions.items()):
        for i,c in enumerate(r["matches"]):
            q=qs[k];req=typed.make_request("r33_"+k+"_"+str(i),c["module"],c["name"],q["target"],[],c["polarity"])
            _,w=typed.names(req);expected[w]=[c["name"]]
            apps[w]={"case":k,"request":req,"context_key":r["context_key"],
                     "current_binding":old.digest({"context_memory_key":memory["key"],"request":q,
                        "context_key":r["context_key"],"current_head":gate.CURRENT})}
            parts.append(typed.render(req).split("\n",1)[1])
            mcp_parts.append(typed.declarations(req).split("\n",1)[1])
            imports.update(q["context_modules"])
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R33Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={r["name"]:r for r in audit}
    for n in list(live)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==6,"fresh witness inventory")
    for w,a0 in apps.items():
        z=ws[w];q=a0["request"]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==by_case[a0["case"]]["goal_expr"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and q["source"] in by_n[w]["proof_constants"] and
               set(by_n[w]["axioms"])<=set(by_n[q["source"]]["axioms"]),"typed proof "+w)
        a0["application"]=z
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R33_DIRECT_CONTEXTUAL_MEMORY","source_head":gate.CURRENT,"source_tree":gate.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r32_direct_digest":gate.DIRECT,"r32_mcp_digest":gate.MCP,
       "parent_ledger_view":gate.VIEW,"transport_key":bridge["key"],"context_memory_key":memory["key"],
       "requests":qs,"observations":by_case,"decisions":decisions,"applications":apps,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)},
       "context_records":len(memory["records"]),"new_candidates":len(memory["new_candidate_names"]),
       "historical_holds":len(memory["historical_holds"]),"candidate_comparison_searches":0,"root_searches":0,
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R33_DIRECT",json.dumps({"direct_digest":old.digest(d),"context_memory_key":memory["key"],
       "context_records":d["context_records"],"registry_candidates":len(reg["candidates"]),
       "new_candidates":d["new_candidates"],"fresh_applications":len(apps),"audits":len(audit),
       "routes":{k:x["status"] for k,x in decisions.items()},"controls":controls,
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
                                     "clientInfo":{"name":"KuuOS contextual memory","version":"1"}})
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
    result={"status":"R33_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R33_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R33_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    result={"status":"R33_INDEPENDENT_CONTEXTUAL_MEMORY_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "parent_ledger_view":d["parent_ledger_view"],"context_memory_key":d["context_memory_key"],
            "context_records":d["context_records"],"new_candidates":d["new_candidates"],
            "historical_holds":d["historical_holds"],"new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),
            "routes":{k:("REFUTED_EXACT_CONTEXT" if x["matches"][0]["polarity"]=="negative" else "REUSE_EXACT_CONTEXT")
                      if x["status"]=="EXACT_CONTEXT_APPLICATION_REQUIRED" else x["status"] for k,x in d["decisions"].items()},
            "controls":d["controls"],"memory_bytes_equal":True,"candidate_comparison_searches":0,"root_searches":0,
            "capsule_rebuilds":0,"provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R33_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r32-local","r32-independent","r31-local","r31-independent","r30-local","r30-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
