#!/usr/bin/env python3
"""R23: isolated compiled proof capsule, exact source/type/proof transport.
Reuse the admitted R22 R2 specialized subtree. Build the capsule independently
on both runners; on the independent runner import the actual sandbox bytes.
No modification of canonical sources or published canonical build caches.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_shared_specialized_subproof_v1_r22 as r22
import check_codeai_olean_shared_specialized_subproof_v1_r22_r2 as repair
from runtime import kuuos_codeai_olean_proof_dag_v1 as sharing
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r22.v
load=r22.load
ROOT=r22.ROOT
MODULE="KuuOSCodeAIR23Capsule"
SHARED="KuuOSR23.shared"
WITNESS=typed.NS+".r23_capsule_joint.witness"
TARGET=typed.NS+".r23_capsule_joint.target"
RUN=45882835148
HEAD="7d6505af634f77e70ed81014002767bca994cf19"
GATE="d702decdce00900a8e2775b6acc3de8c4bb374baab4e753d1fe0ac13109f93a2"
ARTS=((15148226372,"codeai-olean-r22-r2-gate-45882835148-1","sha256:264a2bb5bc4beaa7955101dcf4fa722a081d10e0bae0c1951d85612e1c249b97",RUN,HEAD),
      (15148567155,"codeai-olean-r22-r2-independent-45882835148-1","sha256:2391d85205559a2a702cb5a18f6104edaa923c1b85ce46ba4a5e35741197a33e",RUN,HEAD),
      (15115354804,"codeai-olean-r22-local-45817298015-1","sha256:2af5bb990e3ed696288415e1e37eefa48dda0c2094fbc62598084efff5228ae7",repair.R1_RUN,repair.R1_HEAD))
DIRECT=repair.DIRECT
MCP=repair.MCP
RAW="KUUOS_R23_RAW "
CONSUMER="KUUOS_R23_CONSUMER "

def sha(b):return hashlib.sha256(b).hexdigest()

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R22 R2 lineage")
    for jid,n in [(140126155981,"Verify R22 R2 original sandbox evidence and exact JSON transport"),
                  (140126301786,"Independently reconstruct R22 R2 unchanged Lean proof and verify receipt")]:
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success" and
               any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]),"R22 R2 job")
    for aid,n,dig,r,h in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==r and x["workflow_run"]["head_sha"]==h,"R22 artifact lineage")
    d=load(a.r22_local/"direct.json");mp=load(a.r22_local/"mcp.json")
    gate=load(a.r22_gate/"gate.json");ind=load(a.r22_independent/"r2-receipt.json")
    v.need(d==load(a.r22_independent/"direct.json") and
           (a.r22_local/"direct.json").read_bytes()==(a.r22_independent/"direct.json").read_bytes() and
           old.digest(d)==DIRECT and old.digest(mp)==MCP and mp["status"]=="R22_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           old.digest(gate)==GATE and gate["status"]=="R22_R2_ARCHIVED_SANDBOX_ADMITTED" and
           ind["status"]=="R22_R2_INDEPENDENT_SPECIALIZED_SUBPROOF_GREEN" and ind["r2_head"]==HEAD and
           ind["sandbox_admission_digest"]==GATE and ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           ind["source_and_receipt_bytes_equal"] is True and ind["tuple_list_transport_verified"] is True and
           ind["routes"]["joint_specialized_subproof"]=="REUSE_EXISTING" and
           ind["routes"]["original_refined_global"]=="REFUTED_EXACT_TARGET_REUSED_R21" and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,
           "R22 admitted receipt")
    v.need((a.r22_local/"SharedSpecializedApplication.lean").read_bytes()==
           (a.r22_independent/"SharedSpecializedApplication.lean").read_bytes(),"R22 source bytes")
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD and
           old.digest(v.cache.remote_scope(v.cache.api,old.HEAD))==old.SCOPE,"canonical proof scope")
    return d,ind

def sources(d):
    text=d["fresh_application"]["mcp_source"]
    imports="".join(l+"\n" for l in text.splitlines() if l.startswith("import "))
    v.need(imports and text.startswith(imports),"import boundary")
    tree=d["plan"]["shared_tree"]
    v.need(len(tree)==2 and len(tree[1])==1 and tree[1][0][1]==[] and
           d["plan"]["shared_tree_nodes"]==2 and d["dag"]["shared_binding_uses"]==2,"R22 subtree")
    root=typed.name(tree[0]);leaf=typed.name(tree[1][0][0])
    v.need(root==d["dag"]["source"] and d["dag"]["same_type_defeq"] is True and
           d["dag"]["wrong_type_defeq"] is False and d["dag"]["inferred_type_defeq"] is True,"R22 sharing")
    start="  let shared0 : "
    stop="\n  by\n    change "
    v.need(text.count(start)==1 and text.count(stop)==1,"shared binding boundary")
    pre,rest=text.split(start,1);body,post=rest.split(stop,1)
    ty,proof=body.split(" := by\n",1)
    # Derive the type from the certified closed global target, not arbitrary Lean text.
    L=r22.r17.r13.LEC;c=r22.r17.r13.c
    joint=d["request"]["target"]["apply"];global_target=joint[1]["apply"]
    v.need(joint[0]==c("And") and global_target[0]==c(L+".HasGlobal") and len(global_target)==6,"R22 target structure")
    shared_goal={"apply":[c(L+".Compatible")]+global_target[1:]}
    v.need(ty==typed.term(shared_goal),"R22 exact source annotation")
    expected="    apply @"+root+"\n    · apply @"+leaf
    v.need(proof==expected,"R22 original subtree source")
    wrong=d["reused_exact_negative"]["request"]["target"]["apply"]
    v.need(wrong[0]==c(L+".HasGlobal") and len(wrong)==6,"R22 negative source structure")
    wrong_goal={"apply":[c(L+".Compatible")]+wrong[1:]}
    capsule=imports+"\nset_option autoImplicit false\nset_option maxHeartbeats 4000000\n"
    capsule+="theorem "+SHARED+" : "+ty+" := by\n"+proof+"\n"
    old_ns=typed.NS+"."+d["request"]["case_id"]
    new_ns=typed.NS+".r23_capsule_joint"
    consumer=("import "+MODULE+"\n"+pre+start+ty+" := @"+SHARED+stop+post).replace(old_ns,new_ns)
    v.need(consumer.count(" := @"+SHARED)==1 and expected not in consumer,"consumer recomputes subtree")
    tick=chr(96)*2
    audit=[sharing.HELPER,"","def KuuOSR23WrongTarget : Prop := "+typed.term(wrong_goal),
           "open Lean Meta KuuOSR21","run_cmd do","  let env ← getEnv",
           "  let n := "+tick+SHARED,
           '  let some s := env.find? n | throwError "missing capsule theorem"',
           '  let some idx := env.getModuleIdxFor? n | throwError "missing capsule origin"',
           '  unless env.allImportedModuleNames[idx]!.toString == "'+MODULE+'" do throwError "capsule origin changed"',
           '  let some proof := s.value? (allowOpaque := true) | throwError "missing capsule proof"',
           "  let some wi := env.find? "+tick+WITNESS+' | throwError "missing witness"',
           '  let some w := wi.value? (allowOpaque := true) | throwError "missing witness proof"',
           "  let some ti := env.find? "+tick+TARGET+' | throwError "missing target"',
           '  let some target := ti.value? (allowOpaque := true) | throwError "missing target value"',
           "  let some bi := env.find? "+tick+"KuuOSR23WrongTarget"+' | throwError "missing wrong type"',
           '  let some bad := bi.value? (allowOpaque := true) | throwError "missing wrong type body"',
           "  let mismatch ← Lean.Elab.Command.liftTermElabM do",
           "    withNewMCtxDepth <| isDefEq s.type bad",
           "  let uses := sharedBindings n w",
           "  let occurrences := countConst n w",
           "  let rebuilt := countConst "+tick+root+" w",
           '  unless s.isTheorem && !mismatch && uses == [2] && occurrences == 1 && rebuilt == 0 do throwError "capsule use mismatch"',
           '  let payload := Json.mkObj [("origin", toJson env.allImportedModuleNames[idx]!.toString),',
           '    ("type_expr", toJson (reprStr s.type)), ("proof_expr", toJson (reprStr proof)),',
           '    ("target_expr", toJson (reprStr target)), ("binding_uses", toJson uses),',
           '    ("source_occurrences", toJson occurrences), ("subtree_root_occurrences", toJson rebuilt),',
           '    ("wrong_type_defeq", toJson mismatch)]',
           '  Lean.Elab.Command.liftIO <| IO.println ("'+CONSUMER+'" ++ payload.compress)',""]
    return capsule,consumer,consumer+"\n"+"\n".join(audit),root,leaf

def run_lean(args,path,src):
    if src is not None:path.write_text(src,encoding="utf-8")
    opts=v.canonical_direct_options((ROOT/"lakefile.toml").read_bytes())
    p=subprocess.run(["lake","env","lean",*opts,*args,str(path)],cwd=ROOT,capture_output=True,text=True,timeout=300)
    log=p.stdout+"\n"+p.stderr
    path.with_suffix(".log").write_text(log,encoding="utf-8")
    if p.returncode or re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",log):
        print(log[-20000:],flush=True);raise ValueError("R23 Lean failure:"+path.name)
    return log

def manifest(folder):
    base=folder/(MODULE+".olean")
    files=[base,Path(str(base)+".server"),Path(str(base)+".private")]
    present=[p.is_file() and not p.is_symlink() for p in files]
    v.need(present[0] and present[1]==present[2],"capsule incomplete parts")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p in files if p.is_file()]

def raw_read(folder,out,label):
    files=manifest(folder)
    tick=chr(96)*2
    paths=[str(folder/x["name"]) for x in files]
    if len(paths)==1:
        get="    let (data, _) ← Lean.readModuleData (System.FilePath.mk "+json.dumps(paths[0])+")\n"
        get+='    if data.isModule then throw <| IO.userError "missing module parts"\n'
    else:
        args=", ".join("System.FilePath.mk "+json.dumps(p) for p in paths)
        get="    let parts ← Lean.readModuleDataParts #["+args+"]\n"
        get+='    unless parts.size == 3 do throw <| IO.userError "incomplete module parts"\n'
        get+='    let some (data, _) := parts[2]? | throw <| IO.userError "missing private data"\n'
    src="import Lean\nopen Lean\nrun_cmd do\n  Lean.Elab.Command.liftIO do\n"+get
    src+='    unless data.constNames == data.constants.map (·.name) do throw <| IO.userError "constant inventory"\n'
    src+="    let some info := data.constants.find? (fun c => c.name == "+tick+SHARED+") | throw <| IO.userError \"missing theorem\"\n"
    src+='    unless info.isTheorem && info.levelParams.isEmpty do throw <| IO.userError "open theorem"\n'
    src+='    let some proof := info.value? (allowOpaque := true) | throw <| IO.userError "missing proof"\n'
    src+='    if info.type.hasMVar || info.type.hasFVar || info.type.hasLooseBVars || proof.hasMVar || proof.hasFVar || proof.hasLooseBVars then throw <| IO.userError "open proof"\n'
    src+='    let payload := Json.mkObj [("name", toJson info.name.toString), ("type_expr", toJson (reprStr info.type)), ("proof_expr", toJson (reprStr proof))]\n'
    src+='    IO.println ("'+RAW+'" ++ payload.compress)\n'
    log=run_lean([],out/(label+".lean"),src)
    xs=[json.loads(l[len(RAW):]) for l in log.splitlines() if l.startswith(RAW)]
    v.need(len(xs)==1,"raw capsule receipt")
    return xs[0]

def install(folder,files):
    v.need(manifest(folder)==files,"capsule byte manifest mismatch")
    dest=ROOT/".lake/build/lib/lean"
    v.need(dest.is_dir(),"canonical cache missing")
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"isolated capsule destination already exists")
    for x in files:
        p=folder/x["name"];q=dest/x["name"]
        with q.open("xb") as f:f.write(p.read_bytes())
        v.need(sha(q.read_bytes())==x["sha256"],"installed capsule byte drift")

def direct(a,out):
    hist,prior=admit(a)
    capsule,consumer,audit,root,leaf=sources(hist)
    folder=out/"capsule";folder.mkdir()
    p=folder/(MODULE+".lean");p.write_text(capsule,encoding="utf-8")
    run_lean(["--root="+str(folder),"-o",str(folder/(MODULE+".olean"))],p,None)
    files=manifest(folder);v.save(out/"capsule-manifest.json",{"module":MODULE,"source_sha256":sha(p.read_bytes()),"files":files})
    raw=raw_read(folder,out,"RawRebuilt")
    v.need(raw["name"]==SHARED and raw["type_expr"]==hist["dag"]["specialized_type"] and
           raw["proof_expr"]==hist["dag"]["specialized_proof"],"compiled capsule differs from R22 exact specialized proof")
    source_folder=folder;source_files=files
    if a.phase=="independent":
        source_folder=a.first/"capsule";record=load(a.first/"capsule-manifest.json")
        v.need(record["module"]==MODULE and record["source_sha256"]==sha(p.read_bytes()) and
               (source_folder/(MODULE+".lean")).read_bytes()==p.read_bytes(),"sandbox capsule source drift")
        source_files=record["files"]
        v.need(manifest(source_folder)==source_files,"sandbox capsule transport")
        transported=raw_read(source_folder,out,"RawTransported")
        v.need(transported==raw,"transported capsule kernel content differs")
    install(source_folder,source_files)
    names=sorted([SHARED,WITNESS])
    log=run_lean([],out/"Consumer.lean",audit+"\n"+v.suffix(names))
    xs=[json.loads(l[len(CONSUMER):]) for l in log.splitlines() if l.startswith(CONSUMER)]
    v.need(len(xs)==1,"consumer receipt")
    obs=xs[0]
    v.need(obs["origin"]==MODULE and obs["type_expr"]==raw["type_expr"] and obs["proof_expr"]==raw["proof_expr"] and
           obs["target_expr"]==hist["application"]["target_expr_repr"] and obs["binding_uses"]==[2] and
           obs["source_occurrences"]==1 and obs["subtree_root_occurrences"]==0 and obs["wrong_type_defeq"] is False,
           "imported exact proof use")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":[SHARED,"And.intro"] if n==WITNESS else [root,leaf]} for n in names])
    by_n={r["name"]:r for r in rows}
    prior_obs={r["name"]:r for r in hist["fresh_application"]["observations"]}
    _,old_w=typed.names(hist["request"])
    v.need(by_n[WITNESS]["axioms"]==prior_obs[old_w]["axioms"] and root not in by_n[WITNESS]["proof_constants"],"consumer proof drift")
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD,"source moved")
    d={"status":"R23_DIRECT_PROOF_CAPSULE","source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "r22_direct_digest":DIRECT,"r22_mcp_digest":MCP,"r22_gate_digest":GATE,"prior_r22_routes":prior["routes"],
       "capsule_source_sha256":sha(capsule.encode()),"raw":raw,"consumer":obs,
       "fresh_application":{"observations":rows,"mcp_source":consumer},
       "reused_exact_negative":hist["reused_exact_negative"],"provider_calls":0,
       "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R23_DIRECT",json.dumps({"direct_digest":old.digest(d),"module":MODULE,
       "capsule_parts":len(source_files),"binding_uses":obs["binding_uses"],"subtree_root_occurrences":0,
       "wrong_type_defeq":False,"imported_sandbox_bytes":a.phase=="independent"},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS proof capsule","version":"1"}})
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
    result={"status":"R23_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R23_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R23_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R23_INDEPENDENT_PROOF_CAPSULE_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"compiled_shared_subproof":"REUSE_EXISTING",
            "wrong_specialization":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "original_refined_global":"REFUTED_EXACT_TARGET_REUSED_R22"},
            "capsule_source_sha256":d["capsule_source_sha256"],
            "imported_capsule_from_sandbox":True,"fresh_independent_capsule_builds":1,
            "consumer_shared_subtree_rebuilds":0,"kernel_binding_uses":d["consumer"]["binding_uses"],
            "mcp_audits":len(rows),"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R23_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r22-local","r22-gate","r22-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
