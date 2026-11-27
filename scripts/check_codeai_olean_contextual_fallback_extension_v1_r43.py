#!/usr/bin/env python3
"""R43: append only the independently observed R42 route, then recall it."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_capsule_fallback_v1_r42 as r42
from runtime import kuuos_codeai_olean_contextual_fallback_extension_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r42.r29
r23=r42.r23
r39=r42.r39
v=r42.v
ROOT=r42.ROOT
load=r42.load
FILES=r42.FILES
EXT="fallback-extension-v1.json"
RUN=45952017213
HEAD="e860297052f48dcfdd6324c82b4b79916d63f89a"
ARTS=((15177308034,"codeai-olean-r42-r2-local-45952017213-1","sha256:a1481f6672c240bd1f6892e39db9a566c375f7ba7a63981cca873a188ea14233"),
      (15177602015,"codeai-olean-r42-r2-independent-45952017213-1","sha256:bac40271040eaa59263da80257fb8541612f1486c2f5ed93a7e6d2f5b62873b5"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R42 run")
    for jid,steps in ((140349831031,["Verify R42 contextual capsule fallback","Actual Lean MCP R42 fallback audit"]),
                      (140351440651,["Independently verify R42 contextual capsule fallback"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R42 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R42 artifact")
    d=load(a.r42_local/"direct.json");mp=load(a.r42_local/"mcp.json");ind=load(a.r42_independent/"independent.json")
    v.need(d==load(a.r42_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R42 evidence")
    for name in FILES:
        raw=(a.r42_local/name).read_bytes()
        v.need(raw==(a.r42_independent/name).read_bytes(),"R42 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.prev.prev.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r42_local/"capsule";other=a.r42_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.prev.prev.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawR43",names)
    v.need(raw==r39.raw_read(other,out,"RawR43Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    dispatch=gate.prev.prev
    qs=dispatch.requests(mem)
    # Real unregistered proposition in the same admitted F55 language, not a synthetic True.
    alt=qs["alternate"]
    t=copy.deepcopy(alt["target"])
    t["apply"][0]={"const":gate.base.LEC+"Compatible"}
    qs["unknown"]=gate.base.root.make_request("r43_unknown",t,alt["context_args"],alt["context_modules"])
    obs=r29.parse(r23.run_lean([],out/"ObserveR43.lean",dispatch.observe(qs)),"KUUOS_R41_CONTEXT ")
    v.need(set(obs)==set(qs) and obs["unknown"]["aligned"],"live context inventory")
    extension=gate.project(prior,mp,ind,index,mem,qs,obs)
    v.save(out/EXT,extension)
    decisions={k:gate.dispatch(index,extension,extension,q,obs[k],gate.base.CURRENT) for k,q in sorted(qs.items())}
    v.need(decisions["shadow"]==prior["decisions"]["shadow"] and
           decisions["raw"]==prior["decisions"]["raw"] and
           decisions["wrong_source"]["status"]=="HOLD_CONTEXT_MISMATCH" and
           decisions["unknown"]["status"]=="HOLD_UNREGISTERED_TARGET" and
           decisions["alternate"]["status"]=="EXACT_FALLBACK_MEMORY_APPLICATION_REQUIRED" and
           decisions["alternate"]["polarity"]=="positive" and len(decisions["alternate"]["routes"])==1 and
           len(decisions["shadow"]["routes"])==len(decisions["raw"]["routes"])==3 and
           decisions["shadow"]["polarity"]=="positive" and decisions["raw"]["polarity"]=="negative",
           "append-only dispatch outcomes")
    bad=copy.deepcopy(extension);bad["records"]=[]
    altered=copy.deepcopy(obs["alternate"]);altered["context_exprs"]=obs["raw"]["context_exprs"]
    def check(e,tr,q,o,h):return gate.dispatch(index,e,tr,q,o,h)["status"]
    controls={"tampered":check(bad,extension,alt,obs["alternate"],gate.base.CURRENT),
              "resealed":check(gate.base.portable.seal(bad),extension,alt,obs["alternate"],gate.base.CURRENT),
              "old_head":check(extension,extension,alt,obs["alternate"],old.HEAD),
              "wrong_context":check(extension,extension,alt,altered,gate.base.CURRENT)}
    v.need(controls=={"tampered":"HOLD_EXTENSION_INTEGRITY","resealed":"HOLD_UNADMITTED_EXTENSION",
                     "old_head":"HOLD_EXTENSION_SCOPE","wrong_context":"HOLD_CONTEXT_MISMATCH"},"extension controls")
    # Replay only already selected roots. Do not call inventory, plan, search, or decide.
    body,refs=dispatch.consumer(qs,decisions)
    body=body.replace(dispatch.NS,gate.NS)
    refs={n.replace(dispatch.NS,gate.NS):rs for n,rs in refs.items()}
    record=decisions["alternate"]["routes"][0]
    previous=record["application_request"]
    req=typed.make_request("r43_alt_recall",previous["module"],previous["source"],
                           alt["target"],previous["arguments"],previous["polarity"])
    w=typed.names(req)[1];c=record["source"]
    imports="".join("import "+m+"\n" for m in sorted({dispatch.MODULE,req["module"]}))
    declarations=body.split("\n",1)[1]
    hist=mem["source_observations"]
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs);expected[dispatch.ALT]=[];expected[dispatch.EQUAL]=[]
    expected[w]=[req["source"]];expected.setdefault(req["source"],[])
    log=r23.run_lean([],out/"ApplyR43.lean",imports+declarations+
                     typed.render(req).split("\n",1)[1]+"\n"+v.suffix(sorted(expected)))
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
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R43_DIRECT_CONTEXTUAL_FALLBACK_EXTENSION","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r42_direct_digest":gate.DIRECT,
       "r42_mcp_digest":gate.MCP,"capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],
       "extension_key":extension["key"],"capsule_manifest":manifest,"requests":qs,"observations":obs,
       "decisions":decisions,"controls":controls,"new_contexts":len(extension["records"]),
       "root_trials":0,"capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,
       "proof_authority":False,"recalled_application":z,
       "fresh_application":{"observations":audit,"mcp_source":imports+declarations+typed.declarations(req).split("\n",1)[1]}}
    v.save(out/"direct.json",d)
    print("KUUOS_R43_DIRECT",json.dumps({"direct_digest":old.digest(d),"extension_key":extension["key"],
          "new_contexts":d["new_contexts"],"root_trials":0,"capsule_rebuilds":0,"audits":len(audit),
          "decisions":{k:x["status"] for k,x in decisions.items()},"controls":controls},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual fallback extension","version":"1"}})
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
    result={"status":"R43_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R43_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R43_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+(EXT,):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    result={"status":"R43_INDEPENDENT_CONTEXTUAL_FALLBACK_EXTENSION_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "capsule_manifest":d["capsule_manifest"],"new_contexts":d["new_contexts"],
            "root_trials":0,"capsule_rebuilds":0,"provider_calls":0,
            "shadow_routes":len(d["decisions"]["shadow"]["routes"]),"raw_negative_routes":len(d["decisions"]["raw"]["routes"]),
            "alternate_positive_routes":len(d["decisions"]["alternate"]["routes"]),
            "decisions":{k:x["status"] for k,x in d["decisions"].items()},"controls":d["controls"],
            "parent_bytes_preserved":True,"extension_bytes_equal":True,"raw_type_and_proof_equal":True,
            "mcp_audits":len(rows),"unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R43_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r42-local","r42-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
