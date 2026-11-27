#!/usr/bin/env python3
"""R41: exact single-target routing from the admitted composite capsule."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_capsule_recall_v1_r40 as r40
from runtime import kuuos_codeai_olean_contextual_capsule_dispatch_v1 as gate
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r40.r29
r23=r40.r23
r39=r40.r39
v=r40.v
ROOT=r40.ROOT
load=r40.load
FILES=r40.FILES+("composite-capsule-layer-v1.json",)
RUN=45946064427
HEAD="9560ab10741776f05f0e165d93c9edd24ac16369"
ARTS=((15173959456,"codeai-olean-r40-local-45946064427-1","sha256:b4c436d1d10c006104b8529029940fd9452a70ea344fb9ae841b450b1dd2dac2"),
      (15174917862,"codeai-olean-r40-independent-45946064427-1","sha256:4319590a1dd931d3a1960c6a5f47d34a719c41439db9ca10e7001f6b31983598"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R40 run")
    for jid,steps in ((140330935853,["Verify R40 contextual capsule recall and projections","Actual Lean MCP R40 projection audit"]),
                      (140332275354,["Independently verify R40 contextual capsule recall and projections"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R40 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R40 artifact")
    d=load(a.r40_local/"direct.json");mp=load(a.r40_local/"mcp.json");ind=load(a.r40_independent/"independent.json")
    v.need(d==load(a.r40_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R40 evidence")
    for name in FILES:
        raw=(a.r40_local/name).read_bytes()
        v.need(raw==(a.r40_independent/name).read_bytes(),"R40 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");view=load(out/"context-view-v2.json");layer=load(out/"route-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r40_local/"capsule";other=a.r40_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawR41",names)
    v.need(raw==r39.raw_read(other,out,"RawR41Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"]==prior["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    qs=gate.requests(mem)
    obs=r29.parse(r23.run_lean([],out/"ObserveR41.lean",gate.observe(qs)),"KUUOS_R41_CONTEXT ")
    v.need(set(obs)==set(qs),"observation inventory")
    index=gate.project(prior,mp,ind,mem,view,layer,qs,obs)
    v.save(out/"capsule-dispatch-layer-v1.json",index)
    decisions={k:gate.dispatch(index,index,q,obs[k],gate.base.CURRENT) for k,q in sorted(qs.items())}
    v.need(decisions["shadow"]["status"]==decisions["raw"]["status"]=="EXACT_CAPSULE_PROJECTION_REQUIRED" and
           decisions["shadow"]["polarity"]=="positive" and decisions["raw"]["polarity"]=="negative" and
           decisions["wrong_source"]["status"]=="HOLD_CONTEXT_MISMATCH" and
           decisions["alternate"]["status"]=="HOLD_CAPSULE_MISS" and
           obs["alternate"]["aligned"] and obs["alternate"]["goal_expr"]!=obs["raw"]["goal_expr"] and
           not decisions["alternate"]["routes"],"dispatch outcomes")
    bad=copy.deepcopy(index);bad["records"].pop()
    controls={"tampered":gate.dispatch(bad,index,qs["shadow"],obs["shadow"],gate.base.CURRENT)["status"],
              "resealed":gate.dispatch(gate.base.portable.seal(bad),index,qs["shadow"],obs["shadow"],gate.base.CURRENT)["status"],
              "old_head":gate.dispatch(index,index,qs["shadow"],obs["shadow"],old.HEAD)["status"]}
    v.need(controls=={"tampered":"HOLD_DISPATCH_INTEGRITY","resealed":"HOLD_UNADMITTED_DISPATCH","old_head":"HOLD_DISPATCH_SCOPE"},"dispatch controls")
    body,refs=gate.consumer(qs,decisions)
    hist=mem["source_observations"]
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs);expected[gate.ALT]=[];expected[gate.EQUAL]=[]
    log=r23.run_lean([],out/"ApplyR41.lean",body+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in names:
        v.need(all(by[n][k]==hist[n][k] for k in ("type_expr_repr","type_expr_sha256","type_constants","proof_constants","axioms","universe_parameters")),"capsule proof drift "+n)
    for n,rs in refs.items():
        v.need(set(by[n]["axioms"])<={a for ref in rs for a in by[ref]["axioms"]},"dispatch axiom drift "+n)
        if n.startswith(gate.NS+".shadow"):
            v.need(by[n]["type_expr_repr"]==obs["shadow"]["goal_expr"],"shadow kernel type")
        if n==gate.NS+".alternateControl":
            v.need(by[n]["type_expr_repr"]==obs["alternate"]["goal_expr"],"alternate kernel type")
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R41_DIRECT_CONTEXTUAL_CAPSULE_DISPATCH","source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r40_direct_digest":gate.DIRECT,"r40_mcp_digest":gate.MCP,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"capsule_manifest":manifest,
       "requests":qs,"observations":obs,"decisions":decisions,"controls":controls,"dispatch_refs":refs,
       "positive_witnesses":3,"negative_witnesses":3,"canonical_control_witnesses":2,
       "capsule_rebuilds":0,"root_trials":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R41_DIRECT",json.dumps({"direct_digest":old.digest(d),"dispatch_layer_key":index["key"],
        "decisions":{k:z["status"] for k,z in decisions.items()},"positive_witnesses":3,"negative_witnesses":3,
        "canonical_control_witnesses":2,"capsule_rebuilds":0,"root_trials":0,"controls":controls,"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual capsule dispatch","version":"1"}})
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
    result={"status":"R41_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R41_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R41_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+("capsule-dispatch-layer-v1.json",):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    result={"status":"R41_INDEPENDENT_CONTEXTUAL_CAPSULE_DISPATCH_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "capsule_layer_key":d["capsule_layer_key"],"dispatch_layer_key":d["dispatch_layer_key"],
            "capsule_manifest":d["capsule_manifest"],"positive_witnesses":3,"negative_witnesses":3,"canonical_control_witnesses":2,
            "mcp_audits":len(rows),"decisions":{k:z["status"] for k,z in d["decisions"].items()},"controls":d["controls"],
            "parent_bytes_preserved":True,"dispatch_layer_bytes_equal":True,"raw_type_and_proof_equal":True,
            "imported_certified_capsule":True,"capsule_rebuilds":0,"root_trials":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R41_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r40-local","r40-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
