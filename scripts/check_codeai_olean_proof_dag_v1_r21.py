#!/usr/bin/env python3
"""R21 kernel proof sharing, admitted R20 route, no repeated root search."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_recursive_premise_v1_r17 as r17
from runtime import kuuos_codeai_olean_proof_dag_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r17.v
r12=r17.r12
r8=r17.r8
ROOT=v.ROOT
load=r17.load
RUN=45811079734
HEAD="6a6610768ddf3c821af0e7cfd7f40137c488345e"
DIRECT="60440d5ee31efa992eb11aa814a1f8fbfeb966984ebb6bab32fe208d7ddeb8c5"
MCP="5b8df607eb95cc3f8190a45b7b119c3555a20f14374a2a40722445928717a1b9"
ARTS=(
 (15112982660,"codeai-olean-r20-r2-local-45811079734-1","sha256:4cdb399c585bd08a39dc3687671f33f0fe95cab974a23a4ae68fd3862205a07d"),
 (15114527208,"codeai-olean-r20-r2-independent-45811079734-1","sha256:2b25a0de4163b8164f1e665eb4f545e7c9b37a6c5da68915409697ac0f562e91"),
)
def admit_r20(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R20 R2 lineage")
    for jid,names in ((139878833239,["Verify R20 R2 unnamed root discovery and exact application",
                                    "Actual Lean MCP R20 R2 new application audit"]),
                      (139881773222,["Independently reconstruct R20 R2 unnamed root discovery and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R20 R2 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R20 R2 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R20_R2_INDEPENDENT_ROOT_DISCOVERY_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD
           and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R20 R2 evidence changed")
    return d,res

def direct(a,out):
    hist,prior=admit_r20(a.r20_local,a.r20_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==hist["inventory_digest"],"R20 inventory mismatch")
    plans={k:gate.plan(hist["requests"][k],inv,hist,k) for k in hist["applications"]}
    good=[k for k,p in plans.items() if p["status"]=="DAG_CANDIDATE"]
    v.need(len(good)==1,"shared terminal fixture inventory")
    k=good[0];q=hist["requests"][k];p=plans[k]
    v.need(len(p["shared"])==1 and p["shared"][0]["uses"]==2,"repeated terminal fixture")
    wrong=hist["requests"]["original_refined_global"]
    changed=gate.prev.make_request(q["case_id"],q["target"],wrong["context_args"],q["context_modules"])
    rejected=gate.plan(changed,inv,hist,k)
    v.need(rejected["status"]=="HOLD_REQUEST_CONTEXT_CHANGED" and rejected["shared"]==[],
           "cross-context plan reuse")
    v.need(prior["routes"]["original_refined_global"]=="REFUTED_EXACT_TARGET_REUSED_R19" and
           hist["reused_exact_negative"]["application"]["exact_kernel_type_match"] is True and
           hist["reused_exact_negative"]["target_expr_repr"]==hist["results"]["original_refined_global"]["goal_expr"],
           "prior exact negative lost")
    req,plan,src,mcp_src=gate.application(q,inv,hist,k,wrong)
    v.need(plan==p,"plan changed")
    _,w=typed.names(req)
    original=hist["applications"][k]
    names=sorted(set(original["source_refs"])|{w})
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    modules=sorted(set(q["context_modules"]+[selected[n]["module"] for n in original["source_refs"]]))
    imports="".join("import "+m+"\n" for m in modules)
    src=imports+src.split("\n",1)[1]+"\n"+v.suffix(names)
    mcp_src=imports+mcp_src.split("\n",1)[1]
    materials={}
    for n in original["source_refs"]:
        mod=selected[n]["module"];key=mod+"::"+n
        v.need(key in hist["materials"],"R20 source material missing")
        item=r17.material(db,receipt,hist,mod,n,out/("exact-"+str(len(materials))))
        v.need(item.pop("reused_r16",False),"prior complete type should be reused")
        item["reused_r20"]=True;materials[key]=item
    rc,log=r12.prior.compile_source(out/"SharedApplication.lean",src)
    if rc:print(log[-20000:],flush=True);raise ValueError("R21 shared application failed")
    dag=[json.loads(s[len(gate.MARK):]) for s in log.splitlines() if s.startswith(gate.MARK)]
    apps=[json.loads(s[len(typed.MARK):]) for s in log.splitlines() if s.startswith(typed.MARK)]
    v.need(len(dag)==1 and len(apps)==1,"R21 kernel receipts")
    dag,app=dag[0],apps[0]
    leaf=p["shared"][0]
    v.need(dag["source"]==leaf["name"] and dag["proof_constant_occurrences"]==1 and
           dag["shared_binding_uses"]==[leaf["uses"]] and dag["same_target_defeq"] is True and
           dag["wrong_target_defeq"] is False and
           dag["wrong_target_expr"]==hist["results"]["original_refined_global"]["goal_expr"],
           "R21 exact sharing or mismatch control")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":original["source_refs"] if n==w else []} for n in names])
    by_n={r["name"]:r for r in rows}
    v.need(app["exact_kernel_type_match"] is True and app["target_expr_repr"]==original["target_expr_repr"] and
           app["witness_type_repr"]==by_n[w]["type_expr_repr"] and
           dag["source_type"]==by_n[leaf["name"]]["type_expr_repr"] and
           by_n[leaf["name"]]["type_expr_sha256"]==leaf["type_expr_sha256"],"exact proof/type provenance")
    for m in materials.values():
        v.need(by_n[m["name"]]["type_expr_sha256"]==m["type_expr_sha256"],"imported full type drift")
    prior_obs={r["name"]:r for r in hist["fresh_application"]["observations"]}
    v.need(by_n[w]["axioms"]==prior_obs[original["witness"]]["axioms"],"proof axiom drift")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"observations":rows,"mcp_source":mcp_src+"\n"+"\n".join("#check @"+n for n in names)+"\n"}
    d={"status":"R21_DIRECT_PROOF_DAG","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r20_direct_digest":DIRECT,"r20_mcp_digest":MCP,"prior_r20_routes":prior["routes"],
       "case":k,"plan":plan,"plan_controls":plans,"changed_context_control":rejected,
       "request":req,"application":app,"dag":dag,"materials":materials,"fresh_application":fresh,
       "reused_exact_negative":hist["reused_exact_negative"],"unobserved_module_count":695,
       "semantic_search_complete":False,"proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",d)
    print("KUUOS_R21_DIRECT",json.dumps({"direct_digest":old.digest(d),"case":k,
      "shared_nodes":len(plan["shared"]),"prior_route_leaf_uses":leaf["uses"],
      "kernel_source_occurrences":dag["proof_constant_occurrences"],
      "kernel_binding_uses":dag["shared_binding_uses"],"wrong_target_defeq":dag["wrong_target_defeq"],
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
                                     "clientInfo":{"name":"KuuOS shared proof DAG","version":"1"}})
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
    result={"status":"R21_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R21_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R21_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R21_INDEPENDENT_PROOF_DAG_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"shared_closed_terminal":"REUSE_EXISTING",
            "changed_request_context":"HOLD_REQUEST_CONTEXT_CHANGED",
            "wrong_source_type":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "original_refined_global":"REFUTED_EXACT_TARGET_REUSED_R20"},
            "prior_r20_routes":d["prior_r20_routes"],"shared_nodes":len(d["plan"]["shared"]),
            "prior_route_leaf_uses":d["plan"]["shared"][0]["uses"],
            "kernel_source_occurrences":d["dag"]["proof_constant_occurrences"],
            "kernel_binding_uses":d["dag"]["shared_binding_uses"],
            "new_typed_applications":1,"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R21_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r20-local","r20-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
