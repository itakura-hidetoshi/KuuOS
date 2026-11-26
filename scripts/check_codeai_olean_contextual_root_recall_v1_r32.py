#!/usr/bin/env python3
"""R32: context-bound top-level recall and genuine F55 indexed fallback."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_extended_recursive_recall_v1_r31 as r31
from runtime import kuuos_codeai_olean_contextual_root_recall_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r30=r31.r30
r29=r31.r29
r23=r31.r23
v=r31.v
ROOT=r31.ROOT
load=r31.load
RUN=45909055188
HEAD="595b203eef29ed2a9a1f346b09f5f5b9400a66b6"
ARTS=((15158828266,"codeai-olean-r31-local-45909055188-1","sha256:97bee7a049b6483e3e877bf3a04632a7b523659017b3a1d6a89eec84a64d415c"),
      (15158803911,"codeai-olean-r31-independent-45909055188-1","sha256:e4cc3842f7653027fa28a232d08380c843ebe999774b28645294be6b41555c3e"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R31 lineage")
    for jid,steps in ((140212720459,["Verify R31 extended recursive recall and exact application","Actual Lean MCP R31 new application audit"]),
                      (140214350459,["Independently reconstruct R31 extended recursive recall and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R31 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R31 artifact")
    d=load(a.r31_local/"direct.json");mp=load(a.r31_local/"mcp.json");ind=load(a.r31_independent/"independent.json")
    v.need(d==load(a.r31_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R31_DIRECT_EXTENDED_RECURSIVE_RECALL" and mp["status"]=="R31_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R31_INDEPENDENT_EXTENDED_RECURSIVE_RECALL_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and ind["ledger_bytes_equal"] is True and
           d["ledger_view_digest"]==ind["ledger_view_digest"]==gate.VIEW and ind["mcp_audits"]==30 and
           d["source_head"]==gate.prev.CURRENT and d["source_tree"]==gate.prev.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R31 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R31 audit binding")
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((a.r31_local/name).read_bytes()==(a.r31_independent/name).read_bytes(),"R31 exact bytes "+name)
    return d

def direct(a,out):
    scope=r29.observe_scope()
    previous=admit(a)
    prior,mem,layer,bridge=r31.admit(a,scope)
    reg=prior["registry"];rows=gate.ledger(mem,layer,bridge,reg)
    for name in ("portable-memory.json","extension.json","transport.json"):
        (out/name).write_bytes((a.r30_local/name).read_bytes())
        if a.phase=="independent":v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R31 ledger bytes")
    v.need(old.digest(rows)==gate.VIEW and rows==load(a.r31_local/"ledger-view.json"),"admitted ledger view")
    for name in ("portable-memory.json","extension.json","transport.json"):
        v.need((a.r30_local/name).read_bytes()==(a.r31_local/name).read_bytes(),"historical ledger bytes")
    v.save(out/"ledger-view.json",rows)
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
    r20,_=r29.r28.r27.r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"],"R20 inventory")
    requests=gate.requests(r20["requests"],rows)
    selected={x["name"]:x for pool in inv["selected"].values() for x in pool}
    registered={c["name"]:c for c in reg["candidates"]}
    expected={n:[] for n in registered};expected[gate.ext.NEGATIVE_LEAF]=[]
    imports={c["module"] for c in reg["candidates"]}
    parts=[];mcp_parts=[];apps={};results={};decisions={};bindings={}
    expected_status={"local":"EXACT_ROOT_POSITIVE_CANDIDATES","global":"EXACT_ROOT_POSITIVE_CANDIDATES",
       "wrong_source":"HOLD_CONTEXT_MISMATCH","wrong_observer":"HOLD_CONTEXT_MISMATCH",
       "raw_negative":"EXACT_ROOT_NEGATIVE_CANDIDATE","faithful_constant":"INDEXED_POSITIVE_CANDIDATE",
       "faithful_original":"INDEXED_NEGATIVE_CANDIDATE"}
    for k,(q,ctx) in requests.items():
        v.need("source" not in q,"named root source")
        log=r23.run_lean([],out/(k+".lean"),gate.render(q,ctx,inv,rows,reg))
        gate.base.check_live(log,rows,reg,types)
        row=r29.parse(log,gate.MARK);results[k]=row
        dec=gate.decision(row,rows);decisions[k]=dec
        v.need(dec["status"]==expected_status[k],"contextual root outcome "+k+" "+json.dumps({"decision":dec,"row":row},sort_keys=True))
        bindings[k]=old.digest({"request":q,"admitted_context":ctx,"current_head":gate.prev.CURRENT,"transport_key":bridge["key"],"ledger_view":gate.VIEW})
        if k=="global":v.need(len(dec["routes"])==2,"global alternatives")
        if k=="wrong_source":v.need(not row["target_aligned"] and not row["context_aligned"],"wrong atlas control")
        if k=="wrong_observer":v.need(row["target_aligned"] and not row["context_aligned"],"same target different observer control")
        for i,route in enumerate(dec["routes"]):
            neg=dec["status"] in ("EXACT_ROOT_NEGATIVE_CANDIDATE","INDEXED_NEGATIVE_CANDIDATE")
            req,src,mcp_src=gate.application(q,inv,reg,route,"r32_"+k+"_"+str(i),neg)
            _,w=typed.names(req);refs=sorted({x["rule"] for x in route})
            expected[w]=refs
            apps[w]={"case":k,"request":req,"expected_target_expr":row["goal_expr"],"current_binding":bindings[k]}
            parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
            imports.update(q["context_modules"])
            for n in refs:
                expected.setdefault(n,[])
                imports.add((registered[n] if n in registered else selected[n])["module"])
    v.need(results["local"]["goal_expr"]==results["wrong_source"]["goal_expr"]==results["wrong_observer"]["goal_expr"],"context contrast changed target")
    v.need(all(results[k]["goal_expr"] not in {x["target_expr"] for x in rows.values()} for k in ("faithful_constant","faithful_original")),"novel target already stored")
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R32Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={x["name"]:x for x in audit}
    for n in list(registered)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==6,"fresh application inventory")
    for w,x in apps.items():
        r=ws[w];q=x["request"]
        v.need(r["exact_kernel_type_match"] is True and r["target_expr_repr"]==x["expected_target_expr"] and
               r["witness_type_repr"]==by_n[w]["type_expr_repr"] and q["source"] in by_n[w]["proof_constants"],"typed witness "+w)
        x["application"]=r
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R32_DIRECT_CONTEXTUAL_ROOT_RECALL","source_head":gate.prev.CURRENT,"source_tree":gate.prev.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r31_direct_digest":gate.DIRECT,"r31_mcp_digest":gate.MCP,
       "ledger_view_digest":gate.VIEW,"transport_key":bridge["key"],"requests":{k:{"request":q,"admitted_context":ctx} for k,(q,ctx) in requests.items()},
       "request_bindings":bindings,"results":results,"decisions":decisions,"applications":apps,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)},
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R32_DIRECT",json.dumps({"direct_digest":old.digest(d),"routes":decisions,
       "context_holds":2,"exact_root_comparisons":0,"new_target_comparisons":16,
       "fresh_applications":len(apps),"audits":len(audit),"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual root recall","version":"1"}})
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
    result={"status":"R32_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R32_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R32_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    result={"status":"R32_INDEPENDENT_CONTEXTUAL_ROOT_RECALL_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "ledger_view_digest":d["ledger_view_digest"],"transport_key":d["transport_key"],
            "routes":{"local":"REUSE_EXISTING","global":"REUSE_EXISTING_TWO_ALTERNATIVES",
                      "wrong_source":"HOLD_CONTEXT_MISMATCH","wrong_observer":"HOLD_CONTEXT_MISMATCH",
                      "raw_negative":"REFUTED_EXACT_TARGET","faithful_constant":"INDEXED_PROVED",
                      "faithful_original":"INDEXED_REFUTED_EXACT_TARGET"},
            "exact_root_comparisons":0,"new_target_comparisons":16,"context_holds":2,
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),"capsule_rebuilds":0,"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R32_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r31-local","r31-independent","r30-local","r30-independent","r20-local","r20-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
