#!/usr/bin/env python3
"""R45: compile the admitted joint proof and infer compatibility by import."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_joint_memory_v1_r44 as r44
from runtime import kuuos_codeai_olean_contextual_joint_capsule_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r44.r29
r23=r44.r23
r39=r44.r39
v=r44.v
ROOT=r44.ROOT
load=r44.load
FILES=r44.FILES
NEW="joint-capsule-manifest.json"
RUN=45954739297
HEAD="7b913a59f4e08493b0f4d62049edabf37915ef31"
ARTS=((15178024744,"codeai-olean-r44-local-45954739297-1","sha256:74da6d0f5aa0cd34e93e2267d8090533bddf5097556b9de9d4b93e8ed8b914a0"),
      (15178537404,"codeai-olean-r44-independent-45954739297-1","sha256:b61847b7c10770b36d1a1e24fa1756b5e533683d8c483305073b564362431384"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R44 run")
    for jid,steps in ((140358489947,["Verify R44 contextual joint memory","Actual Lean MCP R44 joint audit"]),
                      (140360029166,["Independently verify R44 contextual joint memory"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R44 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R44 artifact")
    d=load(a.r44_local/"direct.json");mp=load(a.r44_local/"mcp.json");ind=load(a.r44_independent/"independent.json")
    v.need(d==load(a.r44_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R44 evidence")
    for name in FILES:
        raw=(a.r44_local/name).read_bytes()
        v.need(raw==(a.r44_independent/name).read_bytes(),"R44 immutable bytes "+name)
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
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r44_local/"capsule";other=a.r44_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR45",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR45Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    dispatch=gate.dispatch
    qs=prior["requests"]
    obs=r29.parse(r23.run_lean([],out/"ObserveR45.lean",dispatch.observe(qs)),"KUUOS_R41_CONTEXT ")
    extension=load(out/r44.r43.EXT)
    src,selected_names,historical=gate.material(prior,mp,ind,index,extension,mem,obs)
    requests=gate.requests(qs)
    # R1 hit the Lean recursion-depth limit in the eight-context run_cmd.
    # Retain all canonical controls in each independent four-context batch.
    # The original five-context observation has already been checked above.
    new_obs={}
    for k,q in sorted(requests.items()):
        controls={n:qs[n] for n in ("shadow","raw","alternate")}
        label="compat_"+k
        batch={**controls,label:q}
        row=r29.parse(r23.run_lean([],out/("ObserveCompatibilityR45_"+k+".lean"),dispatch.observe(batch)),"KUUOS_R41_CONTEXT ")
        v.need(set(row)==set(batch) and all(row[n]==obs[n] for n in controls),"prior context drift "+k)
        new_obs[k]=row[label]
    v.need(new_obs["alternate"]==obs["unknown"] and all(new_obs[k]["context_exprs"]==obs[k]["context_exprs"] for k in requests),
           "compatibility context binding")
    p=gate.plan(qs,requests,new_obs)
    bad=copy.deepcopy(new_obs);bad["alternate"]["aligned"]=False
    try:gate.plan(qs,requests,bad)
    except ValueError as e:control=str(e)
    else:raise ValueError("unaligned compatibility accepted")
    v.need(control=="HOLD_COMPATIBILITY_CONTEXT","compatibility control")
    new=out/("joint-capsule" if a.phase=="direct" else "joint-rebuilt");new.mkdir()
    lean=new/(gate.MODULE+".lean")
    r23.run_lean(["--root="+str(new),"-o",str(new/(gate.MODULE+".olean"))],lean,src)
    joint_manifest={"module":gate.MODULE,"source_sha256":r23.sha(lean.read_bytes()),"files":capsule_files(new)}
    raw_joint=raw_read(new,out,"RawJointR45",selected_names)
    v.need(all(raw_joint[n]["type_expr"]==historical[n]["type_expr_repr"] for n in selected_names),"R44 full type drift")
    selected=new;selected_manifest=joint_manifest
    if a.phase=="independent":
        selected=a.first/"joint-capsule";selected_manifest=load(a.first/NEW)
        v.need(selected_manifest["module"]==gate.MODULE and selected_manifest["source_sha256"]==joint_manifest["source_sha256"] and
               (selected/(gate.MODULE+".lean")).read_bytes()==lean.read_bytes() and capsule_files(selected)==selected_manifest["files"],
               "joint capsule transport")
        v.need(raw_read(selected,out,"RawJointTransportR45",selected_names)==raw_joint,"joint full raw equality")
        saved=out/"joint-capsule";saved.mkdir()
        for n in [gate.MODULE+".lean"]+[x["name"] for x in selected_manifest["files"]]:
            (saved/n).write_bytes((selected/n).read_bytes())
        v.need(capsule_files(saved)==selected_manifest["files"],"joint transported bytes")
    v.save(out/NEW,selected_manifest)
    install(selected,selected_manifest)
    body,check,refs=gate.consumer(p)
    expected={n:historical[n]["expected_direct_refs"] for n in historical}
    for rule in (gate.BACK,gate.GLUE,gate.COVER):expected.setdefault(rule,[])
    expected.update(refs)
    log=r23.run_lean([],out/"ApplyR45.lean",body+check+v.suffix(sorted(expected)))
    observed=r29.parse(log,gate.MARK)
    v.need(observed=={k:o["goal_expr"] for k,o in new_obs.items()},"derived exact target drift")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n in historical:
        v.need(all(by[n][k]==historical[n][k] for k in ("type_expr_repr","type_expr_sha256","type_constants",
              "proof_constants","axioms","universe_parameters")),"R44 proof observation drift "+n)
    for n,rs in refs.items():
        v.need(set(rs)<=set(by[n]["proof_constants"]) and
               set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"compatibility proof dependency "+n)
    v.need(all(set(x["axioms"])<=typed.STANDARD for x in audit),"standard axioms")
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R45_DIRECT_CONTEXTUAL_JOINT_CAPSULE","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r44_direct_digest":gate.DIRECT,
       "r44_mcp_digest":gate.MCP,"capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],
       "extension_key":extension["key"],"capsule_manifest":manifest,"joint_capsule_manifest":selected_manifest,
       "joint_raw":raw_joint,"joint_capsule_theorems":len(raw_joint),"compatibility_plan":p,
       "compatibility_refs":refs,"compatibility_witnesses":len(refs),
       "positive_witnesses":6,"negative_witnesses":3,"historical_hold_retained":True,
       "exact_kernel_type":True,"control":control,"root_trials":0,"parent_capsule_rebuilds":0,
       "new_capsule_builds":1,"consumer_proof_body_rebuilds":0,"provider_calls":0,
       "semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R45_DIRECT",json.dumps({"direct_digest":old.digest(d),"joint_capsule_theorems":len(raw_joint),
          "compatibility_witnesses":len(refs),"positive_witnesses":6,"negative_witnesses":3,
          "joint_capsule_manifest":selected_manifest,"root_trials":0,"parent_capsule_rebuilds":0,
          "new_capsule_builds":1,"consumer_proof_body_rebuilds":0,"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual joint capsule","version":"1"}})
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
    result={"status":"R45_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R45_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R45_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+(NEW,):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    v.need(capsule_files(out/"joint-capsule")==capsule_files(first/"joint-capsule")==d["joint_capsule_manifest"]["files"],
           "joint capsule bytes")
    result={"status":"R45_INDEPENDENT_CONTEXTUAL_JOINT_CAPSULE_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
            "joint_capsule_theorems":d["joint_capsule_theorems"],"compatibility_witnesses":d["compatibility_witnesses"],
            "compatibility_refs":d["compatibility_refs"],"positive_witnesses":6,"negative_witnesses":3,
            "historical_hold_retained":True,"exact_kernel_type":True,"parent_bytes_preserved":True,
            "raw_type_and_proof_equal":True,"imported_sandbox_joint_capsule":True,"root_trials":0,
            "parent_capsule_rebuilds":0,"new_capsule_builds":1,"consumer_proof_body_rebuilds":0,"provider_calls":0,
            "mcp_audits":len(rows),"unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R45_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r44-local","r44-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
