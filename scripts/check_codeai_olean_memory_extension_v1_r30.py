#!/usr/bin/env python3
"""R30: proof capsule growth from admitted R29, with append-only memory."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_portable_recursive_recall_v1_r29 as r29
from runtime import kuuos_codeai_olean_memory_extension_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r29.v
r23=r29.r23
load=r29.load
ROOT=r29.ROOT
RUN=45904959211
HEAD="7ae9d1e454b53d49768fc85cbbf72716ec1b219c"
DIRECT="50c801618f84a577cf882a6388a97a3b3373327edff8e5c3f05b4c37822aaf3b"
MCP="66a7298add784cf7561fac36dd7e61c4c4e9c7aedbe72a6dc015cda0f3cb4c76"
BRIDGE="8898e40d56997ad7f3a9ea8e17a97ae2aa9b7facb563d464eaca749d98ab0a89"
ARTS=((15157647066,"codeai-olean-r29-local-45904959211-1","sha256:73e6fe791b53d4c7bd5571d44892fa7e01bb07cc423edb7290c0f43c08a38ab2"),
      (15158255577,"codeai-olean-r29-independent-45904959211-1","sha256:291b76c850e270480006ebe376ec7568f1b4d069832d1a3260df24181feb828e"))

def admit(a,scope):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R29 lineage")
    for jid,steps in ((140199389769,["Verify R29 portable recursive recall and exact application","Actual Lean MCP R29 new application audit"]),
                      (140201025330,["Independently reconstruct R29 portable recursive recall and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R29 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R29 artifact")
    d=load(a.r29_local/"direct.json");mp=load(a.r29_local/"mcp.json");ind=load(a.r29_independent/"independent.json")
    v.need(d==load(a.r29_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R29_DIRECT_PORTABLE_RECURSIVE_RECALL" and mp["status"]=="R29_REAL_MCP_GREEN" and
           mp["direct_digest"]==DIRECT and ind["status"]=="R29_INDEPENDENT_PORTABLE_RECURSIVE_RECALL_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["transport_key"]==d["transport_key"]==BRIDGE and
           ind["memory_key"]==d["memory_key"]==gate.prev.R28_MEMORY and ind["transport_bytes_equal"] is True and
           ind["new_typed_applications"]==8 and ind["mcp_audits"]==24 and
           d["source_head"]==gate.prev.CURRENT and d["source_tree"]==gate.prev.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R29 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R29 audit binding")
    mem=load(a.r29_local/"portable-memory.json");bridge=load(a.r29_local/"transport.json")
    for name in ("portable-memory.json","transport.json"):
        v.need((a.r29_local/name).read_bytes()==(a.r29_independent/name).read_bytes(),"R29 exact bytes "+name)
    v.need(mem["key"]==gate.prev.R28_MEMORY and gate.portable.seal(mem)["key"]==mem["key"] and
           bridge["key"]==BRIDGE and gate.portable.seal(bridge)["key"]==BRIDGE and bridge["scope"]==scope and
           bridge["historical_memory_key"]==mem["key"] and bridge["registry_key"]==d["inventory_key"],"R29 memory scope")
    return d,mem,bridge

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
    prior,mem,bridge=admit(a,scope)
    capsule=r29.admit_capsule(a)
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["source_sha256"]==r29.r24.SOURCE and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==r29.r24.SOURCE,"R23 bytes")
    v.need(r23.raw_read(folder,out,"RawR23")==capsule["raw"],"R23 exact type/proof")
    r23.install(folder,manifest["files"])
    source,items=gate.material(prior,mem)
    histobs={x["name"]:x for x in prior["fresh_application"]["observations"]}
    names=sorted({x["name"] for x in items.values()}|{gate.NEGATIVE_LEAF})
    new=out/"capsule";new.mkdir()
    p=new/(gate.MODULE+".lean")
    r23.run_lean(["--root="+str(new),"-o",str(new/(gate.MODULE+".olean"))],p,source)
    new_manifest={"module":gate.MODULE,"source_sha256":r23.sha(p.read_bytes()),"files":capsule_files(new)}
    raw=raw_read(new,out,"RawNewCapsule",names)
    for n in names:
        v.need(raw[n]["type_expr"]==histobs[n]["type_expr_repr"],"historical theorem type "+n)
    selected=new;selected_manifest=new_manifest
    if a.phase=="independent":
        selected=a.first/"capsule";selected_manifest=load(a.first/"capsule-manifest.json")
        v.need(selected_manifest["module"]==gate.MODULE and selected_manifest["source_sha256"]==new_manifest["source_sha256"] and
               (selected/(gate.MODULE+".lean")).read_bytes()==p.read_bytes() and capsule_files(selected)==selected_manifest["files"],"sandbox capsule transport")
        v.need(raw_read(selected,out,"RawTransportedCapsule",names)==raw,"independent raw proof equality")
    v.save(out/"capsule-manifest.json",selected_manifest)
    install(selected,selected_manifest)
    reg=gate.candidates(mem,items,raw,histobs)
    memrows={r["case"]:r for r in mem["records"].values()}
    targets={k:x["target"] for k,x in items.items()}
    targets.update(old_exact=memrows["capsule_exact"]["target"],old_unknown=memrows["unknown"]["target"],new_unknown={"const":"True"})
    x=r29.parse(r23.run_lean([],out/"ObserveExtension.lean",gate.portable.render(targets,reg)),gate.portable.MARK)
    exprs={z["case"]:z["expr"] for z in x["targets"]}
    live={z["name"]:gate.portable.hash_type(z["type_expr"]) for z in x["types"]}
    expected_live={c["name"]:c["type_sha256"] for c in reg["candidates"]}
    v.need(set(exprs)==set(targets) and len(x["targets"])==len(exprs) and len(x["types"])==len(live) and live==expected_live,"live candidate/target drift")
    layer=gate.journal(mem,bridge,items,exprs,reg,selected_manifest,DIRECT)
    v.need(len(layer["additions"])==3 and sum(len(vv) for vv in layer["additions"].values())==3,"extension inventory")
    v.save(out/"extension.json",layer)
    (out/"portable-memory.json").write_bytes((a.r29_local/"portable-memory.json").read_bytes())
    v.save(out/"transport.json",bridge)
    if a.phase=="independent":
        for path in ("extension.json","portable-memory.json","transport.json"):
            v.need((out/path).read_bytes()==(a.first/path).read_bytes(),"append-only transport "+path)
    routes={k:gate.lookup(mem,layer,layer,bridge,e,live,expected_live) for k,e in exprs.items()}
    v.need(routes["old_unknown"]["status"]=="HOLD_HISTORICAL_NO_MATCH" and routes["new_unknown"]["status"]=="HOLD_SEARCH_REQUIRED" and
           routes["old_exact"]["status"]=="EXACT_APPLICATION_REQUIRED" and len(routes["old_exact"]["matches"])==1 and
           len(routes["global_identity_context"]["matches"])==2 and
           items["global_identity_context"]["name"] in {c["name"] for c in routes["global_identity_context"]["matches"]} and
           len(routes["local_refined_context"]["matches"])>=1 and
           routes["blocked_pair"]["status"]=="EXACT_APPLICATION_REQUIRED" and
           [c["polarity"] for c in routes["blocked_pair"]["matches"]]==["negative"],"append/alternative recall outcomes")
    forged=copy.deepcopy(layer);forged["additions"]={}
    changed_live=copy.deepcopy(live);changed_live[next(iter(live))]="0"*64
    e=exprs["local_refined_context"]
    controls={"tampered":gate.lookup(mem,forged,layer,bridge,e,live,expected_live)["status"],
              "resealed":gate.lookup(mem,gate.portable.seal(forged),layer,bridge,e,live,expected_live)["status"],
              "live_type":gate.lookup(mem,layer,layer,bridge,e,changed_live,expected_live)["status"]}
    v.need(controls=={"tampered":"HOLD_EXTENSION_INTEGRITY","resealed":"HOLD_UNADMITTED_EXTENSION","live_type":"HOLD_SOURCE_TYPE_DRIFT"},"extension controls")
    # Freshly apply ALL alternatives, including both positive witnesses for the
    # existing global target. No original root proof text is in the consumer.
    imports="".join("import "+m+"\n" for m in sorted({c["module"] for c in reg["candidates"]}))
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.NEGATIVE_LEAF]=[]
    apps={};parts=[];mcp_parts=[]
    for k,r in sorted(routes.items()):
        if r["status"]!="EXACT_APPLICATION_REQUIRED":continue
        for i,c in enumerate(r["matches"]):
            req=typed.make_request("r30_"+k+"_"+str(i),c["module"],c["name"],targets[k],[],c["polarity"])
            _,w=typed.names(req);expected[w]=[c["name"]]
            apps[w]={"case":k,"request":req}
            parts.append(typed.render(req).split("\n",1)[1])
            mcp_parts.append(typed.declarations(req).split("\n",1)[1])
    mcp_source=imports+"\n"+"\n".join(mcp_parts)
    log=r23.run_lean([],out/"ExtensionApplications.lean",imports+"\n"+"\n".join(parts)+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={r["name"]:r for r in audit}
    for n in expected_live:
        a0=by_n[n];h=histobs[n]
        v.need(a0["type_expr_repr"]==h["type_expr_repr"] and a0["proof_constants"]==h["proof_constants"] and a0["axioms"]==h["axioms"],"imported proof drift "+n)
    n=gate.NEGATIVE_LEAF
    v.need(by_n[n]["type_expr_repr"]==histobs[n]["type_expr_repr"] and by_n[n]["proof_constants"]==histobs[n]["proof_constants"] and
           by_n[n]["axioms"]==histobs[n]["axioms"],"negative dependency drift")
    rows=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in rows}
    v.need(len(rows)==len(ws)==len(apps) and len(apps)>=5,"new application inventory")
    for w,a0 in apps.items():
        r=ws[w];q=a0["request"];z=by_n[w]
        v.need(r["exact_kernel_type_match"] is True and r["target_expr_repr"]==exprs[a0["case"]] and
               r["witness_type_repr"]==z["type_expr_repr"] and q["source"] in z["proof_constants"] and
               set(z["axioms"])<=set(by_n[q["source"]]["axioms"]),"fresh typed application")
        a0["application"]=r
    v.need(r29.observe_scope()==scope,"main scope moved")
    d={"status":"R30_DIRECT_APPEND_ONLY_MEMORY","source_head":gate.prev.CURRENT,"source_tree":gate.prev.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r29_direct_digest":DIRECT,"r29_mcp_digest":MCP,
       "parent_memory_key":mem["key"],"extension_key":layer["key"],"transport_key":bridge["key"],
       "capsule_manifest":selected_manifest,"raw":raw,"registry":reg,"routes":routes,"targets":targets,
       "applications":apps,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":mcp_source},
       "new_records":3,"distinct_target_count":len(set(mem["records"])|set(layer["additions"])),
       "historical_capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R30_DIRECT",json.dumps({"direct_digest":old.digest(d),"extension_key":layer["key"],
        "parent_records":len(mem["records"]),"new_records":3,"distinct_target_count":d["distinct_target_count"],
        "global_alternatives":len(routes["global_identity_context"]["matches"]),"fresh_applications":len(apps),
        "audits":len(audit),"controls":controls,"historical_capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS append only proof memory","version":"1"}})
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
    result={"status":"R30_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R30_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R30_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R30_INDEPENDENT_APPEND_ONLY_MEMORY_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "parent_memory_key":d["parent_memory_key"],"extension_key":d["extension_key"],"transport_key":d["transport_key"],
            "new_records":d["new_records"],"distinct_target_count":d["distinct_target_count"],
            "global_alternatives":len(d["routes"]["global_identity_context"]["matches"]),
            "fresh_applications":len(d["applications"]),"mcp_audits":len(rows),
            "historical_memory_bytes_preserved":True,"imported_sandbox_capsule":True,"raw_proof_equality":True,
            "historical_capsule_rebuilds":0,"new_independent_capsule_builds":1,"provider_calls":0,
            "controls":d["controls"],"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R30_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r29-local","r29-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
