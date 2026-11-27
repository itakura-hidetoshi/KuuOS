#!/usr/bin/env python3
"""R42: consume the certified capsule, discover only aligned missing targets."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_capsule_dispatch_v1_r41 as r41
import check_codeai_olean_proof_dag_v1_r21 as r21
from runtime import kuuos_codeai_olean_contextual_capsule_fallback_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r41.r29
r23=r41.r23
r39=r41.r39
v=r41.v
ROOT=r41.ROOT
load=r41.load
FILES=r41.FILES+("capsule-dispatch-layer-v1.json",)
RUN=45949441584
HEAD="cedcf06d140693b37781c37be6cea76be37a143a"
ARTS=((15176417745,"codeai-olean-r41-local-45949441584-1","sha256:0bb568ca9202acc726352c65e3e1b72f329465a7c5a7897e234024351515c3f2"),
      (15176107873,"codeai-olean-r41-independent-45949441584-1","sha256:26c49209766a13e50d338ecda239f3a1c4635b6e68055bfce2bc6a884ff1dc29"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R41 run")
    for jid,steps in ((140341620267,["Verify R41 contextual capsule dispatch","Actual Lean MCP R41 dispatch audit"]),
                      (140343071506,["Independently verify R41 contextual capsule dispatch"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R41 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R41 artifact")
    d=load(a.r41_local/"direct.json");mp=load(a.r41_local/"mcp.json");ind=load(a.r41_independent/"independent.json")
    v.need(d==load(a.r41_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R41 evidence")
    for name in FILES:
        raw=(a.r41_local/name).read_bytes()
        v.need(raw==(a.r41_independent/name).read_bytes(),"R41 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.prev.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r41_local/"capsule";other=a.r41_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.prev.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawR42",names)
    v.need(raw==r39.raw_read(other,out,"RawR42Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    qs=gate.prev.requests(mem)
    obs=r29.parse(r23.run_lean([],out/"ObserveR42.lean",gate.prev.observe(qs)),"KUUOS_R41_CONTEXT ")
    decisions=gate.admit(prior,mp,ind,index,mem,qs,obs)
    r20,_=r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"] and inv["index_rows"]==47705 and
           len(inv["unobserved_modules"])==695 and
           (a.r20_local/"inventory.json").read_bytes()==(a.r20_independent/"inventory.json").read_bytes(),"R20 index lineage")
    plans={k:gate.plan(index,q,obs[k],decisions[k],inv) for k,q in sorted(qs.items())}
    active=[k for k,p in plans.items() if p["status"]=="EXACT_CLOSED_COMPARISON_REQUIRED"]
    v.need(active==["alternate"] and all(p["status"]=="HOLD_FALLBACK_NOT_AUTHORIZED" and not p["candidates"]
           for k,p in plans.items() if k not in active),"fallback authorization")
    k=active[0];p=plans[k]
    log=r23.run_lean([],out/"SearchR42.lean",gate.render(qs,k,p))
    v.need(r29.parse(log,"KUUOS_R41_CONTEXT ")==obs,"live search context drift")
    trace=r29.parse(log,gate.MARK)
    result=gate.decide(p,trace)
    v.need(result["status"]=="INDEXED_APPLICATION_REQUIRED" and
           {x["polarity"] for x in result["matches"]}=={"positive"} and
           gate.prev.ALT in {x["name"] for x in result["matches"]},"alternate positive discovery")
    # A separately known theorem is checked as a control only after discovery.
    body,refs=gate.prev.consumer(qs,decisions)
    body=body.replace(gate.prev.NS,gate.NS)
    refs={n.replace(gate.prev.NS,gate.NS):rs for n,rs in refs.items()}
    imports={gate.prev.MODULE};parts=[body.split("\n",1)[1]];mcp_parts=list(parts)
    hist=mem["source_observations"]
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs);expected[gate.prev.ALT]=[];expected[gate.prev.EQUAL]=[]
    witnesses={}
    for i,c in enumerate(result["matches"]):
        req=typed.make_request("r42_alt_"+str(i),c["module"],c["name"],qs[k]["target"],[],c["polarity"])
        w=typed.names(req)[1];imports.add(c["module"])
        parts.append(typed.render(req).split("\n",1)[1])
        mcp_parts.append(typed.declarations(req).split("\n",1)[1])
        expected[w]=[c["name"]];expected.setdefault(c["name"],[])
        witnesses[w]={"request":req,"source":c}
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"ApplyR42.lean",imp+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in names:
        v.need(all(by[n][f]==hist[n][f] for f in ("type_expr_repr","type_expr_sha256","type_constants","proof_constants","axioms","universe_parameters")),"capsule proof drift "+n)
    rows=[json.loads(x[len(typed.MARK):]) for x in log.splitlines() if x.startswith(typed.MARK)]
    by_w={x["witness_name"]:x for x in rows}
    v.need(len(rows)==len(by_w)==len(witnesses) and set(by_w)==set(witnesses),"application inventory")
    for n,x in witnesses.items():
        c=x["source"];z=by_w[n]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==obs[k]["goal_expr"] and
               z["witness_type_repr"]==by[n]["type_expr_repr"] and c["type_expr"]==by[c["name"]]["type_expr_repr"] and
               set(by[n]["axioms"])<=set(by[c["name"]]["axioms"]),"discovered exact application "+n)
        x["application"]=z
    for n,rs in refs.items():
        v.need(set(by[n]["axioms"])<={a for ref in rs for a in by[ref]["axioms"]},"replay axiom drift "+n)
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R42_DIRECT_CONTEXTUAL_CAPSULE_FALLBACK","source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r41_direct_digest":gate.DIRECT,"r41_mcp_digest":gate.MCP,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"capsule_manifest":manifest,
       "requests":qs,"observations":obs,"decisions":decisions,"plans":plans,"trace":trace,"fallback":result,
       "witnesses":witnesses,"fallback_requests":1,"root_trials":result["comparison_count"],
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)}}
    v.save(out/"direct.json",d)
    print("KUUOS_R42_DIRECT",json.dumps({"direct_digest":old.digest(d),"dispatch_layer_key":index["key"],
        "fallback_requests":1,"root_trials":d["root_trials"],"fallback_witnesses":len(witnesses),
        "selected_sources":[c["name"] for c in result["matches"]],"capsule_rebuilds":0,"audits":len(audit),
        "decisions":{k:z["status"] for k,z in plans.items()}},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual capsule fallback","version":"1"}})
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
    result={"status":"R42_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R42_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R42_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES:
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    result={"status":"R42_INDEPENDENT_CONTEXTUAL_CAPSULE_FALLBACK_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "capsule_layer_key":d["capsule_layer_key"],"dispatch_layer_key":d["dispatch_layer_key"],
            "capsule_manifest":d["capsule_manifest"],"fallback_requests":1,"root_trials":d["root_trials"],
            "fallback_witnesses":len(d["witnesses"]),"selected_sources":[x["name"] for x in d["fallback"]["matches"]],
            "mcp_audits":len(rows),"decisions":{k:z["status"] for k,z in d["plans"].items()},
            "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"imported_certified_capsule":True,
            "capsule_rebuilds":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R42_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r41-local","r41-independent","r20-local","r20-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
