#!/usr/bin/env python3
"""R44: consume independently admitted R43 records and derive source separation."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_fallback_extension_v1_r43 as r43
from runtime import kuuos_codeai_olean_contextual_joint_memory_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r43.r29
r23=r43.r23
r39=r43.r39
v=r43.v
ROOT=r43.ROOT
load=r43.load
FILES=r43.FILES+(r43.EXT,)
RUN=45953369234
HEAD="6e2b511dd879d8e523462f4b10f35b366603ee87"
ARTS=((15176924453,"codeai-olean-r43-local-45953369234-1","sha256:61080eff064add3e8d7bc5aa642e2b015bb12610ff6eac6552c5dc5cb70cdab4"),
      (15178181678,"codeai-olean-r43-independent-45953369234-1","sha256:81f3d4c3899161a95109c374ac6c19055756ae51b7f7a6903b0e221ed6413604"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R43 run")
    for jid,steps in ((140354115913,["Verify R43 contextual fallback extension","Actual Lean MCP R43 fallback audit"]),
                      (140355636452,["Independently verify R43 contextual fallback extension"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R43 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R43 artifact")
    d=load(a.r43_local/"direct.json");mp=load(a.r43_local/"mcp.json");ind=load(a.r43_independent/"independent.json")
    v.need(d==load(a.r43_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R43 evidence")
    for name in FILES:
        raw=(a.r43_local/name).read_bytes()
        v.need(raw==(a.r43_independent/name).read_bytes(),"R43 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r43_local/"capsule";other=a.r43_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawR44",names)
    v.need(raw==r39.raw_read(other,out,"RawR44Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    dispatch=gate.dispatch
    qs=dispatch.requests(mem)
    # Real unregistered proposition in the same admitted F55 language, not a synthetic True.
    alt=qs["alternate"]
    t=copy.deepcopy(alt["target"])
    t["apply"][0]={"const":gate.base.LEC+"Compatible"}
    qs["unknown"]=gate.base.root.make_request("r43_unknown",t,alt["context_args"],alt["context_modules"])
    obs=r29.parse(r23.run_lean([],out/"ObserveR44.lean",dispatch.observe(qs)),"KUUOS_R41_CONTEXT ")
    v.need(set(obs)==set(qs) and obs["unknown"]["aligned"],"live context inventory")
    extension=load(out/r43.EXT)
    decisions=gate.admit(prior,mp,ind,index,extension,mem,qs,obs)
    roles={k:k for k in ("shadow","raw","alternate")}
    p=gate.plan(qs,obs,decisions,roles)
    controls={}
    def reject(label,r):
        try:gate.plan(qs,obs,decisions,r)
        except ValueError as e:controls[label]=str(e)
        else:raise ValueError("unlawful joint accepted "+label)
    reject("swap_sources",{"shadow":"shadow","raw":"alternate","alternate":"raw"})
    reject("unknown_as_positive",{"shadow":"shadow","raw":"raw","alternate":"unknown"})
    reject("wrong_context",{"shadow":"wrong_source","raw":"raw","alternate":"alternate"})
    reject("same_source",{"shadow":"shadow","raw":"raw","alternate":"raw"})
    v.need(controls=={"swap_sources":"HOLD_COMPOSITE_POLARITY","unknown_as_positive":"HOLD_COMPOSITE_POLARITY",
                     "wrong_context":"HOLD_COMPOSITE_POLARITY","same_source":"HOLD_COMPOSITE_CONTEXT"},"joint controls")
    # The two projections for each pair must originate in the same capsule route.
    v.need([r["capsule_theorem"] for r in p["paired_capsule_routes"]]==
           [r["capsule_theorem"] for r in decisions["raw"]["routes"]],"paired route order")
    # Replay only already selected roots. Do not call inventory, plan, search, or decide.
    body,refs=dispatch.consumer(qs,decisions)
    body=body.replace(dispatch.NS,gate.REPLAY)
    refs={n.replace(dispatch.NS,gate.REPLAY):rs for n,rs in refs.items()}
    record=decisions["alternate"]["routes"][0]
    previous=record["application_request"]
    req=typed.make_request("r44_alt_recall",previous["module"],previous["source"],
                           alt["target"],previous["arguments"],previous["polarity"])
    w=typed.names(req)[1];c=record["source"]
    imports="".join("import "+m+"\n" for m in sorted({dispatch.MODULE,req["module"]}))
    declarations=body.split("\n",1)[1]
    hist=mem["source_observations"]
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs);expected[dispatch.ALT]=[];expected[dispatch.EQUAL]=[]
    expected[w]=[req["source"]];expected.setdefault(req["source"],[])
    joint,check,joint_refs=gate.declarations(p,w)
    expected.update(joint_refs)
    log=r23.run_lean([],out/"ApplyR44.lean",imports+declarations+
                     typed.render(req).split("\n",1)[1]+"\n"+joint+check+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in names:
        v.need(all(by[n][f]==hist[n][f] for f in ("type_expr_repr","type_expr_sha256","type_constants",
                "proof_constants","axioms","universe_parameters")),"capsule proof drift "+n)
    for n,rs in refs.items():
        v.need(set(by[n]["axioms"])<={a for ref in rs for a in by[ref]["axioms"]},"replay axiom drift "+n)
    rows=[json.loads(x[len(typed.MARK):]) for x in log.splitlines() if x.startswith(typed.MARK)]
    v.need(len(rows)==1,"recall witness inventory")
    z=rows[0]
    v.need(z["witness_name"]==w and z["exact_kernel_type_match"] is True and
           z["target_expr_repr"]==obs["alternate"]["goal_expr"] and z["witness_type_repr"]==by[w]["type_expr_repr"] and
           all(by[c["name"]][f]==record["source_observation"][f] for f in
               ("type_expr_repr","type_expr_sha256","type_constants","proof_constants","axioms","universe_parameters")) and
           set(by[w]["axioms"])<=set(by[c["name"]]["axioms"]),"exact recalled application")
    for n in expected:
        v.need(set(by[n]["axioms"])<=typed.STANDARD,"nonstandard axiom")
    v.need(gate.MARK in log.splitlines(),"joint exact kernel type")
    for n,rs in joint_refs.items():
        v.need(set(rs)<=set(by[n]["proof_constants"]) and
               set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"joint proof dependency "+n)
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R44_DIRECT_CONTEXTUAL_JOINT_MEMORY","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r43_direct_digest":gate.DIRECT,
       "r43_mcp_digest":gate.MCP,"capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],
       "extension_key":extension["key"],"capsule_manifest":manifest,"requests":qs,"observations":obs,
       "decisions":decisions,"controls":controls,"joint_plan":p,"joint_refs":joint_refs,
       "joint_witnesses":3,"source_separation_witnesses":3,"exact_kernel_type":True,
       "root_trials":0,"capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,
       "proof_authority":False,"recalled_application":z,
       "fresh_application":{"observations":audit,"mcp_source":imports+declarations+
                           typed.declarations(req).split("\n",1)[1]+"\n"+joint}}
    v.save(out/"direct.json",d)
    print("KUUOS_R44_DIRECT",json.dumps({"direct_digest":old.digest(d),"extension_key":extension["key"],
          "joint_witnesses":3,"source_separation_witnesses":3,"root_trials":0,"capsule_rebuilds":0,
          "audits":len(audit),"controls":controls,"exact_kernel_type":True},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual joint memory","version":"1"}})
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
    result={"status":"R44_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R44_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R44_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R44_INDEPENDENT_CONTEXTUAL_JOINT_MEMORY_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "capsule_manifest":d["capsule_manifest"],"joint_witnesses":d["joint_witnesses"],
            "source_separation_witnesses":d["source_separation_witnesses"],"joint_refs":d["joint_refs"],
            "root_trials":0,"capsule_rebuilds":0,"provider_calls":0,"controls":d["controls"],
            "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"exact_kernel_type":True,
            "mcp_audits":len(rows),"unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R44_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r43-local","r43-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
