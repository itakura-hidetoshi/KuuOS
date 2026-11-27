#!/usr/bin/env python3
"""R40: admit and import an R39 capsule without recompiling its proof bodies."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_composite_capsule_v1_r39 as r39
from runtime import kuuos_codeai_olean_contextual_capsule_recall_v1 as gate
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r39.r29
r23=r39.r23
v=r39.v
ROOT=r39.ROOT
load=r39.load
FILES=r39.FILES+("capsule-manifest.json",)
RUN=45944025433
HEAD="7567bbcca3731e1c03efdff75aff230774e67023"
ARTS=((15174261364,"codeai-olean-r39-local-45944025433-1","sha256:3fc5c6906725caad3de91194141d8e24cadd369b76382a467a187b341de7bb70"),
      (15174206416,"codeai-olean-r39-independent-45944025433-1","sha256:78f7b7e60151af9fcbcd24373f38ec42f13d282396c9f2f0ecc2d4898943ba91"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R39 run")
    for jid,steps in ((140324509975,["Verify R39 composite capsule and exact replay","Actual Lean MCP R39 capsule replay audit"]),
                      (140325685789,["Independently reconstruct R39 composite capsule and replay"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R39 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R39 artifact")
    d=load(a.r39_local/"direct.json");mp=load(a.r39_local/"mcp.json");ind=load(a.r39_independent/"independent.json")
    v.need(d==load(a.r39_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R39 evidence")
    x=v.cache.api("actions/artifacts/15171277637")
    v.need(x["name"]=="codeai-olean-r38-local-45937019627-1" and
           x["digest"]=="sha256:acec8d08c549c558bd730df78de76e8524c568984e105ba326464e2e4af3c4b0" and
           not x["expired"] and x["workflow_run"]["id"]==45937019627 and
           x["workflow_run"]["head_sha"]=="5cc6c21248aa342e0f819143551e4a3cd8e026ea","R38 context artifact")
    prior=load(a.r38_local/"direct.json")
    v.need(old.digest(prior)==gate.prev.DIRECT,"historical live context receipt")
    for name in FILES:
        raw=(a.r39_local/name).read_bytes()
        v.need(raw==(a.r39_independent/name).read_bytes(),"R39 immutable bytes "+name)
        if name!="capsule-manifest.json":v.need(raw==(a.r38_local/name).read_bytes(),"R38 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind,prior

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind,prior38=admit(a,out)
    view=load(out/"context-view-v2.json");layer=load(out/"route-layer-v1.json")
    mem=gate.project(prior,mp,ind,prior38,view,layer)
    v.save(out/"composite-capsule-layer-v1.json",mem)
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(prior["raw"]);local=a.r39_local/"capsule";other=a.r39_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawAdmittedR39",names)
    v.need(raw==r39.raw_read(other,out,"RawIndependentR39",names)==prior["raw"],"admitted full raw proofs")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    v.need(r39.capsule_files(saved)==manifest["files"],"retained bytes")
    r39.install(saved,manifest)
    request=copy.deepcopy(mem["request"])
    log=r23.run_lean([],out/"ObserveR40.lean",gate.observe(request))
    observed=r29.parse(log,"KUUOS_R40_CONTEXT ")
    recall=gate.recall(mem,mem,view,layer,request,observed,gate.base.CURRENT)
    v.need(recall["status"]=="EXACT_COMPOSITE_CAPSULE_APPLICATION_REQUIRED" and recall["root_trials"]==0,"exact capsule recall")
    bad=copy.deepcopy(mem);bad["routes"].pop()
    swapped=copy.deepcopy(request);swapped["negative_request"]=request["positive_request"]
    wrong=copy.deepcopy(observed);wrong["negative"]=observed["positive"]
    controls={"tampered":gate.recall(bad,mem,view,layer,request,observed,gate.base.CURRENT)["status"],
              "resealed":gate.recall(gate.base.portable.seal(bad),mem,view,layer,request,observed,gate.base.CURRENT)["status"],
              "old_head":gate.recall(mem,mem,view,layer,request,observed,old.HEAD)["status"],
              "wrong_request":gate.recall(mem,mem,view,layer,swapped,observed,gate.base.CURRENT)["status"],
              "wrong_live_context":gate.recall(mem,mem,view,layer,request,wrong,gate.base.CURRENT)["status"]}
    v.need(controls=={"tampered":"HOLD_CAPSULE_LAYER_INTEGRITY","resealed":"HOLD_UNADMITTED_CAPSULE_LAYER",
                     "old_head":"HOLD_CAPSULE_SCOPE","wrong_request":"HOLD_CAPSULE_CONTEXT_MISMATCH",
                     "wrong_live_context":"HOLD_CAPSULE_CONTEXT_MISMATCH"},"capsule recall controls")
    body,check,refs=gate.consumer(request,recall["routes"])
    hist=mem["source_observations"]
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs);expected[gate.SOUND]=[]
    log=r23.run_lean([],out/"ApplyR40.lean",body+check+v.suffix(sorted(expected)))
    v.need("KUUOS_R40_EXACT_PROJECTIONS" in log.splitlines(),"exact projection marker")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in names:
        v.need(all(by[n][k]==hist[n][k] for k in ("type_expr_repr","type_expr_sha256","type_constants","proof_constants","axioms","universe_parameters")),"capsule proof drift "+n)
    for n,rs in refs.items():
        v.need(set(by[n]["axioms"])<={a for ref in rs for a in by[ref]["axioms"]},"projection axiom drift "+n)
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R40_DIRECT_CONTEXTUAL_CAPSULE_RECALL","source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r39_direct_digest":gate.DIRECT,"r39_mcp_digest":gate.MCP,
       "context_view_key":view["key"],"route_layer_key":layer["key"],"capsule_layer_key":mem["key"],
       "capsule_manifest":manifest,"raw_digests":mem["raw_digests"],"request":request,"observations":observed,
       "recall":recall,"controls":controls,"projection_refs":refs,"capsule_theorems":len(names),
       "positive_witnesses":3,"negative_witnesses":3,"no_promotion_witnesses":3,
       "capsule_rebuilds":0,"root_trials":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R40_DIRECT",json.dumps({"direct_digest":old.digest(d),"capsule_layer_key":mem["key"],
        "capsule_theorems":len(names),"positive_witnesses":3,"negative_witnesses":3,"no_promotion_witnesses":3,
        "capsule_rebuilds":0,"root_trials":0,"controls":controls,"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual capsule recall","version":"1"}})
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
    result={"status":"R40_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R40_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R40_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+("composite-capsule-layer-v1.json",):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    result={"status":"R40_INDEPENDENT_CONTEXTUAL_CAPSULE_RECALL_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "context_view_key":d["context_view_key"],"route_layer_key":d["route_layer_key"],"capsule_layer_key":d["capsule_layer_key"],
            "capsule_manifest":d["capsule_manifest"],"capsule_theorems":d["capsule_theorems"],
            "positive_witnesses":3,"negative_witnesses":3,"no_promotion_witnesses":3,"mcp_audits":len(rows),
            "controls":d["controls"],"parent_bytes_preserved":True,"capsule_layer_bytes_equal":True,
            "raw_type_and_proof_equal":True,"imported_certified_capsule":True,"capsule_rebuilds":0,"root_trials":0,
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R40_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r39-local","r39-independent","r38-local","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
