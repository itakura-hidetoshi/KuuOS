#!/usr/bin/env python3
"""R22 bounded specialized subtree sharing across two admitted R20 routes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_recursive_premise_v1_r17 as r17
import check_codeai_olean_proof_dag_v1_r21 as r21
from runtime import kuuos_codeai_olean_shared_specialized_subproof_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r17.v
r12=r17.r12
r8=r17.r8
ROOT=v.ROOT
load=r17.load
RUN=45813837876
HEAD="60454d0bce872bdcab7eb44ebb1208382fce648e"
DIRECT="37c10092291b9d81b18322c37c84603ddd46684a418f658f67f08f63fe986202"
MCP="a87cc85e4dd27891c38da977fdd70b09c7240ae488c4f5f50e4cb788f2f583aa"
ARTS=(
 (15113319030,"codeai-olean-r21-local-45813837876-1","sha256:ce84d0ea47b6e3976248a10efe16563f60d67da918570212aa404a5b7be41a3f"),
 (15115830161,"codeai-olean-r21-independent-45813837876-1","sha256:c47dcf2097266b08641ba56bc2ecd9f53d139909102750db2d34fb948c62bf6f"),
)
def admit_r21(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R21 lineage")
    for jid,names in ((139888310787,["Verify R21 shared proof DAG and exact application",
                                    "Actual Lean MCP R21 new application audit"]),
                      (139890306834,["Independently reconstruct R21 shared proof DAG and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R21 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R21 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R21_INDEPENDENT_PROOF_DAG_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R21 evidence changed")
    return d,res

def direct(a,out):
    hist,prior=admit_r21(a.r21_local,a.r21_independent)
    r20,old_routes=r21.admit_r20(a.r20_local,a.r20_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    inv=load(a.r20_local/"inventory.json")
    p=gate.plan(inv,r20,hist)
    v.need(p["status"]=="SPECIALIZED_SUBTREE_CANDIDATE" and p["shared_tree_nodes"]==2 and p["uses"]==2,
           "common subtree fixture")
    L=r17.r13.LEC;c=r17.r13.c
    def compatible(target):
        xs=target["apply"]
        v.need(xs[0]==c(L+".HasGlobal") and len(xs)==6,"global target shape")
        return {"apply":[c(L+".Compatible")]+xs[1:]}
    # Typed target schema for this bounded fixture, not a generic theorem
    # instantiation oracle. Lean must verify both actual proof uses.
    shared_goal=compatible(r20["requests"]["global_identity_context"]["target"])
    wrong_goal=compatible(r20["requests"]["original_refined_global"]["target"])
    v.need(shared_goal!=wrong_goal,"mismatch fixture changed")
    v.need(prior["routes"]["shared_closed_terminal"]=="REUSE_EXISTING" and
           prior["routes"]["original_refined_global"]=="REFUTED_EXACT_TARGET_REUSED_R20" and
           hist["reused_exact_negative"]==r20["reused_exact_negative"],"R21 evidence changed")
    req,plan,src,mcp_src=gate.application(inv,r20,hist,shared_goal,wrong_goal)
    v.need(plan==p,"plan changed")
    _,w=typed.names(req)
    refs=sorted({n for k in p["cases"] for n in r20["applications"][k]["source_refs"]})
    names=sorted(set(refs)|{w})
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    modules=sorted({m for k in p["cases"] for m in r20["requests"][k]["context_modules"]}|
                   {selected[n]["module"] for n in refs})
    imports="".join("import "+m+"\n" for m in modules)
    src=imports+src.split("\n",1)[1]+"\n"+v.suffix(names)
    mcp_src=imports+mcp_src.split("\n",1)[1]
    materials={}
    for n in refs:
        mod=selected[n]["module"];key=mod+"::"+n
        v.need(key in r20["materials"],"R20 source material missing")
        item=r17.material(db,receipt,r20,mod,n,out/("exact-"+str(len(materials))))
        v.need(item.pop("reused_r16",False),"prior complete type should be reused")
        item["reused_r20"]=True;materials[key]=item
    rc,log=r12.prior.compile_source(out/"SharedSpecializedApplication.lean",src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R22 shared specialized application failed")
    dag=[json.loads(s[len(gate.MARK):]) for s in log.splitlines() if s.startswith(gate.MARK)]
    apps=[json.loads(s[len(typed.MARK):]) for s in log.splitlines() if s.startswith(typed.MARK)]
    v.need(len(dag)==1 and len(apps)==1,"kernel receipts")
    dag,app=dag[0],apps[0]
    v.need(dag["source"]==p["shared_root"] and dag["proof_constant_occurrences"]==1 and
           dag["shared_binding_uses"]==2 and dag["same_type_defeq"] is True and
           dag["wrong_type_defeq"] is False and dag["inferred_type_defeq"] is True,
           "specialized sharing evidence")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":refs if n==w else []} for n in names])
    by_n={r["name"]:r for r in rows}
    v.need(app["exact_kernel_type_match"] is True and app["witness_type_repr"]==by_n[w]["type_expr_repr"] and
           "And.intro" in by_n[w]["proof_constants"],"joint witness evidence")
    for m in materials.values():
        v.need(by_n[m["name"]]["type_expr_sha256"]==m["type_expr_sha256"],"imported full type drift")
    prior_obs={r["name"]:r for r in r20["fresh_application"]["observations"]}
    allowed={ax for k in p["cases"] for ax in prior_obs[r20["applications"][k]["witness"]]["axioms"]}
    v.need(set(by_n[w]["axioms"])<=allowed,"proof axiom drift")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"observations":rows,"mcp_source":mcp_src+"\n"+"\n".join("#check @"+n for n in names)+"\n"}
    d={"status":"R22_DIRECT_SPECIALIZED_SUBPROOF","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r21_direct_digest":DIRECT,"r21_mcp_digest":MCP,"prior_r21_routes":prior["routes"],
       "r20_direct_digest":old.digest(r20),"plan":plan,"request":req,"application":app,"dag":dag,
       "materials":materials,"fresh_application":fresh,"reused_exact_negative":hist["reused_exact_negative"],
       "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",d)
    print("KUUOS_R22_DIRECT",json.dumps({"direct_digest":old.digest(d),"shared_root":p["shared_root"],
      "shared_subtree_nodes":p["shared_tree_nodes"],"kernel_source_occurrences":dag["proof_constant_occurrences"],
      "kernel_binding_uses":dag["shared_binding_uses"],"wrong_type_defeq":dag["wrong_type_defeq"],
      "reused_complete_types":len(materials),"new_root_searches":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS shared specialized subproof","version":"1"}})
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
    result={"status":"R22_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R22_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R22_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R22_INDEPENDENT_SPECIALIZED_SUBPROOF_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"joint_specialized_subproof":"REUSE_EXISTING",
            "wrong_specialization":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "original_refined_global":"REFUTED_EXACT_TARGET_REUSED_R21"},
            "prior_r21_routes":d["prior_r21_routes"],"shared_subtree_nodes":d["plan"]["shared_tree_nodes"],
            "kernel_source_occurrences":d["dag"]["proof_constant_occurrences"],
            "kernel_binding_uses":d["dag"]["shared_binding_uses"],
            "new_typed_applications":1,"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R22_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r20-local","r20-independent","r21-local","r21-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
