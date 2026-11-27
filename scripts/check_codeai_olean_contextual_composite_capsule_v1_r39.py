#!/usr/bin/env python3
"""R39 composite capsule: preserve exact R38 route proofs and replay imports."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_composite_v1_r38 as r38
from runtime import kuuos_codeai_olean_contextual_composite_capsule_v1 as gate
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r38.r29
r23=r38.r23
v=r38.v
ROOT=r38.ROOT
load=r38.load
FILES=r38.FILES+("route-layer-v1.json",)
RUN=45937019627
HEAD="5cc6c21248aa342e0f819143551e4a3cd8e026ea"
ARTS=((15171277637,"codeai-olean-r38-local-45937019627-1","sha256:acec8d08c549c558bd730df78de76e8524c568984e105ba326464e2e4af3c4b0"),
      (15171725466,"codeai-olean-r38-independent-45937019627-1","sha256:4fa5b921a0a2f5a87fa5738fd79e5ca1ee5768152ba3f7d980bf28a3b6b1f5e7"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R38 run")
    for jid,steps in ((140302456839,["Verify R38 contextual composite and exact application","Actual Lean MCP R38 new application audit"]),
                      (140303932616,["Independently reconstruct R38 contextual composite and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R38 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R38 artifact")
    d=load(a.r38_local/"direct.json");mp=load(a.r38_local/"mcp.json");ind=load(a.r38_independent/"independent.json")
    v.need(d==load(a.r38_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R38 evidence")
    for name in FILES:
        raw=(a.r38_local/name).read_bytes()
        v.need(raw==(a.r38_independent/name).read_bytes(),"R38 historical bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def capsule_files(folder):
    p=folder/(gate.MODULE+".olean")
    files=[p,Path(str(p)+".server"),Path(str(p)+".private")]
    ok=[f.is_file() and not f.is_symlink() for f in files]
    v.need(ok[0] and ok[1]==ok[2],"new capsule parts")
    return [{"name":f.name,"sha256":r23.sha(f.read_bytes()),"bytes":f.stat().st_size} for f in files if f.is_file()]

def raw_read(folder,out,label,names):
    paths=[str(folder/x["name"]) for x in capsule_files(folder)]
    if len(paths)==1:
        get="    let (data, _) ← Lean.readModuleData (System.FilePath.mk "+json.dumps(paths[0])+")\n"
        get+='    if data.isModule then throw <| IO.userError "missing module parts"\n'
    else:
        args=", ".join("System.FilePath.mk "+json.dumps(p) for p in paths)
        get="    let parts ← Lean.readModuleDataParts #["+args+"]\n"
        get+='    unless parts.size == 3 do throw <| IO.userError "incomplete module parts"\n'
        get+='    let some (data, _) := parts[2]? | throw <| IO.userError "missing private data"\n'
    def lname(n):
        x="Name.anonymous"
        for p in n.split("."):x="(Name.str "+x+" "+json.dumps(p)+")"
        return x
    # Name.str tree without importing or elaborating capsule declarations.
    wanted=", ".join(lname(n) for n in names)
    src="import Lean\nopen Lean\nrun_cmd do\n  Lean.Elab.Command.liftIO do\n"+get
    src+='    unless data.constNames == data.constants.map (·.name) do throw <| IO.userError "constant inventory"\n'
    src+="    let wanted : Array Name := #["+wanted+"]\n"
    src+=r'''    let mut rows : Array Json := #[]
    for n in wanted do
      let some info := data.constants.find? (fun c => c.name == n) | throw <| IO.userError "missing theorem"
      unless info.isTheorem && info.levelParams.isEmpty do throw <| IO.userError "open theorem"
      let some proof := info.value? (allowOpaque := true) | throw <| IO.userError "missing proof"
      if info.type.hasMVar || info.type.hasFVar || info.type.hasLooseBVars || proof.hasMVar || proof.hasFVar || proof.hasLooseBVars then
        throw <| IO.userError "open proof"
      rows := rows.push (Json.mkObj [("name", toJson n.toString), ("type_expr", toJson (reprStr info.type)), ("proof_expr", toJson (reprStr proof))])
'''
    src+='    IO.println ("'+gate.RAW_MARK+'" ++ (toJson rows).compress)\n'
    rows=r29.parse(r23.run_lean([],out/(label+".lean"),src),gate.RAW_MARK)
    v.need(len(rows)==len(names) and {r["name"] for r in rows}==set(names),"raw capsule inventory")
    return {r["name"]:r for r in rows}

def install(folder,manifest):
    v.need(capsule_files(folder)==manifest["files"],"new capsule transport mismatch")
    dest=ROOT/".lake/build/lib/lean"
    for x in manifest["files"]:
        p=folder/x["name"];q=dest/x["name"]
        with q.open("xb") as f:f.write(p.read_bytes())
        v.need(r23.sha(q.read_bytes())==x["sha256"],"installed capsule byte drift")

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    view=load(out/"context-view-v2.json");layer=load(out/"route-layer-v1.json")
    source,names,hist,p=gate.material(prior,mp,ind,view,layer)
    new=out/("capsule" if a.phase=="direct" else "rebuilt");new.mkdir()
    lean=new/(gate.MODULE+".lean")
    r23.run_lean(["--root="+str(new),"-o",str(new/(gate.MODULE+".olean"))],lean,source)
    manifest={"module":gate.MODULE,"source_sha256":r23.sha(lean.read_bytes()),"files":capsule_files(new)}
    raw=raw_read(new,out,"RawR39",names)
    v.need(all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"historical full type drift")
    selected=new;selected_manifest=manifest
    if a.phase=="independent":
        selected=a.first/"capsule";selected_manifest=load(a.first/"capsule-manifest.json")
        v.need(selected_manifest["module"]==gate.MODULE and selected_manifest["source_sha256"]==manifest["source_sha256"] and
               (selected/(gate.MODULE+".lean")).read_bytes()==lean.read_bytes() and capsule_files(selected)==selected_manifest["files"],"sandbox capsule transport")
        v.need(raw_read(selected,out,"RawR39Transported",names)==raw,"full independent raw proof equality")
        saved=out/"capsule";saved.mkdir()
        for n in [gate.MODULE+".lean"]+[x["name"] for x in selected_manifest["files"]]:
            (saved/n).write_bytes((selected/n).read_bytes())
        v.need(capsule_files(saved)==selected_manifest["files"],"independent artifact bytes")
    v.save(out/"capsule-manifest.json",selected_manifest)
    install(selected,selected_manifest)
    body,check,refs=gate.consumer(p)
    expected={n:hist[n]["expected_direct_refs"] for n in names}
    expected.update(refs)
    log=r23.run_lean([],out/"ReplayComposite.lean",body+check+v.suffix(sorted(expected)))
    v.need("KUUOS_R39_EXACT_REPLAY" in log.splitlines(),"exact replay marker")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in names:
        v.need(all(by[n][k]==hist[n][k] for k in ("type_expr_repr","type_expr_sha256","type_constants","proof_constants","axioms","universe_parameters")),"R38 proof observation drift "+n)
    for n,rs in refs.items():
        v.need(set(by[n]["axioms"])<=set(by[rs[0]]["axioms"]),"replay axiom drift "+n)
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R39_DIRECT_COMPOSITE_CAPSULE","source_head":gate.prev.prev.CURRENT,"source_tree":gate.prev.prev.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r38_direct_digest":gate.DIRECT,"r38_mcp_digest":gate.MCP,"context_view_key":view["key"],
       "route_layer_key":layer["key"],"capsule_manifest":selected_manifest,"raw":raw,"composite_plan":p,
       "composite_refs":prior["composite_refs"],"replay_refs":refs,"capsule_theorems":len(raw),"replay_witnesses":len(refs),
       "consumer_proof_body_rebuilds":0,"root_trials":0,"provider_calls":0,
       "fresh_application":{"observations":audit,"mcp_source":body},"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R39_DIRECT",json.dumps({"direct_digest":old.digest(d),"capsule_theorems":len(raw),"replay_witnesses":len(refs),
          "capsule_manifest":selected_manifest,"consumer_proof_body_rebuilds":0,"root_trials":0,"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS composite capsule","version":"1"}})
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
    result={"status":"R39_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R39_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R39_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+("capsule-manifest.json",):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(capsule_files(out/"capsule")==capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    result={"status":"R39_INDEPENDENT_COMPOSITE_CAPSULE_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "context_view_key":d["context_view_key"],"route_layer_key":d["route_layer_key"],
            "capsule_manifest":d["capsule_manifest"],"capsule_theorems":d["capsule_theorems"],"replay_witnesses":d["replay_witnesses"],
            "mcp_audits":len(rows),"raw_type_and_proof_equal":True,"imported_sandbox_capsule":True,"parent_bytes_preserved":True,
            "consumer_proof_body_rebuilds":0,"root_trials":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R39_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r38-local","r38-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
