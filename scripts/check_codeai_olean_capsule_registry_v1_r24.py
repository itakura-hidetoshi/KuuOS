#!/usr/bin/env python3
"""R24: independently consume the admitted R23 capsule in two R20 requests."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_proof_capsule_v1_r23_r2 as r23
import check_codeai_olean_proof_dag_v1_r21 as r21
from runtime import kuuos_codeai_olean_capsule_registry_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r23.v
load=r23.load
ROOT=r23.ROOT
RUN=45893906832
HEAD="027e20df48e81f595c92171ed6b36e17cd0855b2"
DIRECT="3697741aa9d705459880e5230c3866d6b5618b6e1ae8c8ecad81e02619d3d80d"
MCP="71c67a061de044af871857ebf922318616143c70d741da125e0eeb751697a54c"
ARTS=((15152817449,"codeai-olean-r23-r2-local-45893906832-1","sha256:ed729f3781a22da6a6dfe7286b2823f6f55a70434ed041b793a1b804b864760e"),
      (15152179328,"codeai-olean-r23-r2-independent-45893906832-1","sha256:00203ba85102beea8faa1b512f0184c873e57f7dbb13d8466c8c3846d57f9f75"))
SOURCE="00007c1cece02d7b25753418ee0409c759f64de391ce98ce5165b3fd4d4e6303"
MARK="KUUOS_R24_TYPE_CONTROL "

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R23 lineage")
    for jid,steps in ((140162968764,["Verify R23 R2 proof capsule and exact application","Actual Lean MCP R23 R2 new application audit"]),
                      (140164550622,["Independently reconstruct R23 R2 proof capsule and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R23 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R23 artifact")
    d=load(a.r23_local/"direct.json");mp=load(a.r23_local/"mcp.json");ind=load(a.r23_independent/"independent.json")
    v.need(d==load(a.r23_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R23_R2_DIRECT_PROOF_CAPSULE" and mp["status"]=="R23_R2_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R23_R2_INDEPENDENT_PROOF_CAPSULE_GREEN" and ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           ind["imported_capsule_from_sandbox"] is True and ind["consumer_shared_subtree_rebuilds"]==0 and
           ind["capsule_source_sha256"]==d["capsule_source_sha256"]==SOURCE and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R23 evidence")
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD and
           old.digest(v.cache.remote_scope(v.cache.api,old.HEAD))==old.SCOPE,"canonical scope")
    return d,ind

def direct(a,out):
    hist,prior=admit(a)
    r20,r20ind=r21.admit_r20(a.r20_local,a.r20_independent)
    r22=load(a.r22_local/"direct.json")
    v.need(old.digest(r22)==r23.DIRECT and old.digest(r20)==r22["r20_direct_digest"] and
           r22["reused_exact_negative"]==hist["reused_exact_negative"]==r20["reused_exact_negative"],"prior lineage")
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"],"R20 inventory")
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["module"]==r23.MODULE and manifest["source_sha256"]==SOURCE and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==SOURCE and r23.manifest(folder)==manifest["files"],"capsule bytes")
    raw=r23.raw_read(folder,out,"RawRegistryCapsule")
    v.need(raw==hist["raw"] and raw["type_expr"]==r22["dag"]["specialized_type"] and
           raw["proof_expr"]==r22["dag"]["specialized_proof"],"raw capsule differs")
    prov={"run":RUN,"head":HEAD,"artifact_id":ARTS[0][0],"artifact_digest":ARTS[0][2],
          "direct_digest":DIRECT,"mcp_digest":MCP}
    e=gate.entry(hist,manifest,prov,r22["plan"]);v.save(out/"registry.json",e)
    cases=sorted(r20["applications"])
    q0=r20["requests"][cases[0]]
    altered=copy.deepcopy(e);altered["manifest"]["files"][0]["sha256"]="0"*64
    wrong=r20["requests"]["wrong_source_context"]
    controls={
      "altered_manifest":gate.lookup(altered,q0,cases[0],e["type_sha256"],old.SCOPE)["status"],
      "scope_changed":gate.lookup(e,q0,cases[0],e["type_sha256"],"0"*64)["status"],
      "wrong_type":gate.lookup(e,q0,cases[0],"0"*64,old.SCOPE)["status"],
      "wrong_context":gate.lookup(e,wrong,wrong["case_id"],e["type_sha256"],old.SCOPE)["status"]}
    v.need(controls=={"altered_manifest":"HOLD_REGISTRY_INTEGRITY","scope_changed":"HOLD_SCOPE",
          "wrong_type":"HOLD_TYPE","wrong_context":"HOLD_CONTEXT"},"registry negative controls")
    r23.install(folder,manifest["files"])
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    root=e["shared_tree"][0];leaf=e["shared_tree"][1][0][0]
    names=[e["name"]];apps={};expected={e["name"]:[root,leaf]};sources=[];mcp_sources=[]
    modules=set()
    for k in cases:
        q=r20["requests"][k];a0=r20["applications"][k]
        v.need(a0["route"]==r20["results"][k]["chosen"]["route"] and a0["application"]["exact_kernel_type_match"] is True,
               "R20 request proof route")
        hit=gate.lookup(e,q,k,e["type_sha256"],old.SCOPE)
        v.need(hit["status"]=="CAPSULE_CANDIDATE","registry miss")
        req,src,mcp_src=gate.application(e,q,a0["route"],inv,k)
        _,w=typed.names(req);names.append(w)
        refs=[n for n in a0["source_refs"] if n!=root]
        # The original leaf can still occur outside the replaced subtree.
        tree=gate.sub.tree(a0["route"])
        if sum(1 for n in gate.sub.nodes(tree) if n[0]==leaf)==1:refs.remove(leaf)
        expected[w]=sorted(set(refs)|{e["name"]})
        modules.update(q["context_modules"]);modules.update(selected[n]["module"] for n in a0["source_refs"])
        apps[k]={"request":req,"witness":w,"registry_hit":hit,"prior_target":a0["target_expr_repr"]}
        sources.append(src.split("\n",1)[1]);mcp_sources.append(mcp_src.split("\n",1)[1])
    imports="import "+r23.MODULE+"\n"+"".join("import "+m+"\n" for m in sorted(modules))
    wrong_goal=r22["reused_exact_negative"]["request"]["target"]
    L=r23.r22.r17.r13.LEC;c=r23.r22.r17.r13.c
    wrong_goal={"apply":[c(L+".Compatible")]+wrong_goal["apply"][1:]}
    tick=chr(96)*2
    check="\n".join([r23.sharing.HELPER,"","def KuuOSR24WrongType : Prop := "+typed.term(wrong_goal),
          "open Lean Meta KuuOSR21","run_cmd do","  let env ← getEnv","  let n := "+tick+e["name"],
          '  let some s := env.find? n | throwError "missing capsule"',
          '  let some idx := env.getModuleIdxFor? n | throwError "missing origin"',
          '  unless env.allImportedModuleNames[idx]!.toString == "'+e["module"]+'" do throwError "capsule origin"',
          "  let some bad := env.find? "+tick+"KuuOSR24WrongType"+' | throwError "missing wrong type"',
          '  let some b := bad.value? (allowOpaque := true) | throwError "missing wrong body"',
          "  let mismatch ← Lean.Elab.Command.liftTermElabM do",
          "    withNewMCtxDepth <| isDefEq s.type b",
          '  unless !mismatch do throwError "wrong specialization admitted"',
          '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ (Json.mkObj [("wrong_type_defeq", toJson mismatch)]).compress)',""])
    log=r23.run_lean([],out/"RegistryConsumers.lean",imports+"\n"+"\n".join(sources)+"\n"+check+"\n"+v.suffix(sorted(names)))
    controls["actual_wrong_specialization"]=[json.loads(s[len(MARK):]) for s in log.splitlines() if s.startswith(MARK)]
    v.need(controls["actual_wrong_specialization"]==[{"wrong_type_defeq":False}],"Lean mismatch control")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(names)])
    by_n={r["name"]:r for r in rows}
    prior_rows={r["name"]:r for r in r20["fresh_application"]["observations"]}
    obs=[json.loads(s[len(typed.MARK):]) for s in log.splitlines() if s.startswith(typed.MARK)]
    v.need(len(obs)==len(apps),"application count")
    by_w={r["witness_name"]:r for r in obs}
    for k,x in apps.items():
        w=x["witness"];a0=r20["applications"][k]
        z=by_w[w]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==x["prior_target"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and root not in by_n[w]["proof_constants"] and
               set(by_n[w]["axioms"])<=set(prior_rows[a0["witness"]]["axioms"]),"consumer proof drift:"+k)
        x["application"]=z
    v.need(gate.sha(by_n[e["name"]]["type_expr_repr"])==e["type_sha256"],"imported full type drift")
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD,"source moved")
    d={"status":"R24_DIRECT_CAPSULE_REGISTRY","source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "r23_direct_digest":DIRECT,"r23_mcp_digest":MCP,"registry":e,"controls":controls,"applications":apps,
       "fresh_application":{"observations":rows,"mcp_source":imports+"\n"+"\n".join(mcp_sources)},
       "reused_exact_negative":hist["reused_exact_negative"],"provider_calls":0,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R24_DIRECT",json.dumps({"direct_digest":old.digest(d),"registry_key":e["key"],
       "consumers":sorted(apps),"capsule_rebuilds":0,"new_root_searches":0,"controls":controls},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS capsule registry","version":"1"}})
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
    result={"status":"R24_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R24_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R24_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R24_INDEPENDENT_CAPSULE_REGISTRY_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"registry_key":d["registry"]["key"],
            "routes":{k:"REUSE_EXISTING" for k in d["applications"]},
            "controls":d["controls"],"new_typed_applications":len(d["applications"]),
            "capsule_rebuilds":0,"new_root_searches":0,"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R24_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r23-local","r23-independent","r22-local","r20-local","r20-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
