#!/usr/bin/env python3
"""R34: consume context memory and route genuine misses to bounded live index."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_memory_v1_r33 as r33
from runtime import kuuos_codeai_olean_contextual_fallback_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r32=r33.r32
r31=r33.r31
r30=r33.r30
r29=r33.r29
r23=r33.r23
v=r33.v
ROOT=r33.ROOT
load=r33.load
RUN=45914416211
HEAD="5536f8f89cd698d16acc1683f3fe4d095ad1fd52"
ARTS=((15160914662,"codeai-olean-r33-local-45914416211-1","sha256:b2bc1ac8e3f023feb0cccfa2c0c2589dbf567e675d0753e5c2f3a25d53c39896"),
      (15160964969,"codeai-olean-r33-independent-45914416211-1","sha256:43d67efdf37f79130ed373a7410786d0e5336f6021247ed2a82e4de1632ba7de"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R33 lineage")
    for jid,steps in ((140230096039,["Verify R33 contextual memory and exact application","Actual Lean MCP R33 new application audit"]),
                      (140231304937,["Independently reconstruct R33 contextual memory and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R33 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R33 artifact")
    d=load(a.r33_local/"direct.json");mp=load(a.r33_local/"mcp.json");ind=load(a.r33_independent/"independent.json")
    v.need(d==load(a.r33_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R33_DIRECT_CONTEXTUAL_MEMORY" and mp["status"]=="R33_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R33_INDEPENDENT_CONTEXTUAL_MEMORY_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and
           d["context_memory_key"]==ind["context_memory_key"]==gate.KEY and ind["memory_bytes_equal"] is True and
           d["parent_ledger_view"]==ind["parent_ledger_view"]==gate.VIEW and ind["mcp_audits"]==17 and
           ind["context_records"]==5 and ind["new_typed_applications"]==6 and
           d["source_head"]==gate.CURRENT and d["source_tree"]==gate.CURRENT_TREE and d["scope_digest"]==old.SCOPE,
           "R33 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R33 audit binding")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json","context-memory.json"):
        v.need((a.r33_local/name).read_bytes()==(a.r33_independent/name).read_bytes(),"R33 bytes "+name)
    return d

def direct(a,out):
    scope=r29.observe_scope()
    last=admit(a)
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
    trusted=gate.prev.projection(previous,mp,ind,reg,rows,bridge)
    memory=load(a.r33_local/"context-memory.json")
    v.need(memory==trusted and memory["key"]==gate.KEY==gate.portable.seal(memory)["key"],"admitted context memory")
    (out/"context-memory.json").write_bytes((a.r33_local/"context-memory.json").read_bytes())
    if a.phase=="independent":
        v.need((out/"context-memory.json").read_bytes()==(a.first/"context-memory.json").read_bytes(),"context memory bytes")
    qs=gate.requests(last)
    log=r23.run_lean([],out/"ObserveContexts.lean",gate.prev.render(qs,memory))
    observed=r29.parse(log,gate.portable.MARK);observations=r29.parse(log,gate.prev.MARK)
    by_case={x["case"]:x for x in observations};reg=memory["registry"]
    hist={x["name"]:x for x in last["fresh_application"]["observations"]}
    live={x["name"]:x["type_expr"] for x in observed["types"]}
    expected_live={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    v.need(len(live)==len(observed["types"])==10 and live==expected_live and
           {n:gate.portable.hash_type(t) for n,t in live.items()}=={c["name"]:c["type_sha256"] for c in reg["candidates"]} and
           len(by_case)==len(observations)==len(qs)==9 and set(by_case)==set(qs),"live source/context inventory")
    target_obs={x["case"]:x["expr"] for x in observed["targets"]}
    v.need(len(target_obs)==len(observed["targets"])==2*len(qs)+len(memory["records"]),"live target inventory")
    for i,(k,q) in enumerate(sorted(qs.items())):
        v.need(target_obs["q"+str(i)]==by_case[k]["goal_expr"] and target_obs["e"+str(i)]==by_case[k]["context_goal_expr"],"query observation")
        if k in last["observations"]:
            v.need(by_case[k]==last["observations"][k],"R33 fresh observation drift "+k)
    for i,(key,r) in enumerate(sorted(memory["records"].items())):
        v.need(target_obs["r"+str(i)]==r["target_expr"],"historical target drift")
    decisions={k:gate.prev.decide(memory,trusted,q,by_case[k],live,expected_live,gate.CURRENT) for k,q in qs.items()}
    for k,r in decisions.items():
        status="HOLD_CONTEXT_MISMATCH" if k in ("wrong_source","wrong_observer") else "HOLD_SEARCH_REQUIRED" if k in ("new_original_compat","new_shadow_global") else "EXACT_CONTEXT_APPLICATION_REQUIRED"
        v.need(r["status"]==status,"context memory decision "+k)
        if k in last["decisions"]:v.need(r==last["decisions"][k],"R33 decision drift "+k)
    r20,_=r29.r28.r27.r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"] and len(inv["unobserved_modules"])==695,"R20 index inventory")
    plans={};traces={};fallback={}
    for k,q in sorted(qs.items()):
        if decisions[k]["status"]!="HOLD_SEARCH_REQUIRED":continue
        v.need(by_case[k]["target_aligned"] and not by_case[k]["target_matches"] and not by_case[k]["context_matches"],"unbound fallback "+k)
        plan=gate.inventory(q,memory,inv);plans[k]=plan
        log=r23.run_lean([],out/("Fallback_"+k+".lean"),gate.render(k,q,memory,plan))
        obs=r29.parse(log,gate.prev.MARK);srcobs=r29.parse(log,gate.portable.MARK)
        v.need(obs==[by_case[k]] and {x["name"]:x["type_expr"] for x in srcobs["types"]}==live,"fallback re-observation drift")
        tr=r29.parse(log,gate.MARK);traces[k]=tr
        fallback[k]=gate.decide(plan,tr,by_case[k]["goal_expr"],live)
    v.need(set(fallback)=={"new_original_compat","new_shadow_global"},"fallback authorization")
    expect={"new_original_compat":("negative",gate.LEC+"nativeF55_twoChart_raw_incompatible"),
            "new_shadow_global":("positive",gate.LEC+"nativeF55_twoChart_shadow_global")}
    for k,(pol,n) in expect.items():
        f=fallback[k]
        v.need(f["status"]=="INDEXED_APPLICATION_REQUIRED" and {x["polarity"] for x in f["matches"]}=={pol} and
               any(x["name"]==n and x["origin"]=="bounded_index" for x in f["matches"]),
               "indexed fallback outcome "+k+" "+json.dumps(f,sort_keys=True))
    imports={c["module"] for c in reg["candidates"]}
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.ext.NEGATIVE_LEAF]=[]
    parts=[];mcp_parts=[];apps={}
    for k,r in sorted(decisions.items()):
        matches=fallback[k]["matches"] if k in fallback else r["matches"]
        for i,c in enumerate(matches):
            q=qs[k];req=typed.make_request("r34_"+k+"_"+str(i),c["module"],c["name"],q["target"],[],c["polarity"])
            _,w=typed.names(req);expected[w]=[c["name"]];expected.setdefault(c["name"],[])
            apps[w]={"case":k,"request":req,"route_kind":"indexed" if k in fallback else "exact_context",
                     "current_binding":old.digest({"context_memory_key":memory["key"],"request":q,
                         "decision":fallback[k] if k in fallback else r,"current_head":gate.CURRENT})}
            parts.append(typed.render(req).split("\n",1)[1])
            mcp_parts.append(typed.declarations(req).split("\n",1)[1])
            imports.add(c["module"]);imports.update(q["context_modules"])
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R34Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={r["name"]:r for r in audit}
    for n in list(live)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    for f in fallback.values():
        for c in f["matches"]:
            v.need(by_n[c["name"]]["type_expr_repr"]==c["type_expr"],"new indexed source drift")
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==6+sum(len(f["matches"]) for f in fallback.values()),"fresh witness inventory")
    for w,a0 in apps.items():
        z=ws[w];q=a0["request"]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==by_case[a0["case"]]["goal_expr"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and q["source"] in by_n[w]["proof_constants"] and
               set(by_n[w]["axioms"])<=set(by_n[q["source"]]["axioms"]),"typed proof "+w)
        a0["application"]=z
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R34_DIRECT_CONTEXTUAL_FALLBACK","source_head":gate.CURRENT,"source_tree":gate.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r33_direct_digest":gate.DIRECT,"r33_mcp_digest":gate.MCP,
       "context_memory_key":memory["key"],"parent_ledger_view":gate.VIEW,"transport_key":bridge["key"],
       "requests":qs,"observations":by_case,"decisions":decisions,"plans":plans,"fallback_traces":traces,
       "fallback_decisions":fallback,"applications":apps,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)},
       "exact_context_comparisons":0,"fallback_comparisons":sum(x["comparison_count"] for x in fallback.values()),
       "fallback_requests":len(fallback),"context_holds":2,"capsule_rebuilds":0,"provider_calls":0,
       "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R34_DIRECT",json.dumps({"direct_digest":old.digest(d),"context_memory_key":memory["key"],
       "exact_context_comparisons":0,"fallback_comparisons":d["fallback_comparisons"],
       "fallback_routes":{k:[{"name":x["name"],"polarity":x["polarity"],"origin":x["origin"]} for x in f["matches"]] for k,f in fallback.items()},
       "fallback_requests":len(fallback),"context_holds":2,"fresh_applications":len(apps),"audits":len(audit),
       "capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual fallback","version":"1"}})
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
    result={"status":"R34_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R34_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R34_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R34_INDEPENDENT_CONTEXTUAL_FALLBACK_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "context_memory_key":d["context_memory_key"],"parent_ledger_view":d["parent_ledger_view"],
            "routes":{"local":"REUSE_EXACT_CONTEXT","global":"REUSE_EXACT_CONTEXT_TWO_ALTERNATIVES",
                      "faithful_constant":"REUSE_EXACT_CONTEXT","faithful_original":"REFUTED_EXACT_CONTEXT",
                      "raw_negative":"REFUTED_EXACT_CONTEXT","wrong_observer":"HOLD_CONTEXT_MISMATCH","wrong_source":"HOLD_CONTEXT_MISMATCH",
                      "new_original_compat":"INDEXED_REFUTED_EXACT_CONTEXT","new_shadow_global":"INDEXED_PROVED_EXACT_CONTEXT"},
            "fallback_sources":{k:[{"name":x["name"],"polarity":x["polarity"]} for x in f["matches"]] for k,f in d["fallback_decisions"].items()},
            "exact_context_comparisons":0,"fallback_comparisons":d["fallback_comparisons"],"fallback_requests":d["fallback_requests"],
            "context_holds":2,"new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),
            "memory_bytes_equal":True,"capsule_rebuilds":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R34_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r33-local","r33-independent","r32-local","r32-independent","r31-local","r31-independent","r30-local","r30-independent","r20-local","r20-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
