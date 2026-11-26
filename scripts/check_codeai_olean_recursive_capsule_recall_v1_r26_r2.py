#!/usr/bin/env python3
"""R26: admitted R25 capsule recall inside the R20 recursive premise engine."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_capsule_typed_lookup_v1_r25 as r25
import check_codeai_olean_proof_dag_v1_r21 as r21
from runtime import kuuos_codeai_olean_recursive_capsule_recall_v1_r2 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r25.v
r23=r25.r23
r24=r25.r24
load=r25.load
ROOT=r25.ROOT
RUN=45896476614
HEAD="2d6ce86a2288631be735284f9071e05786960b56"
DIRECT="cc82208be4329856af19fa1bdc96397883ca76ff8e91fb5188e6dccc458ba7d6"
MCP="b862baeb4b62bde77ccee23faf43e173f7238c95aaf2e9f59fea22147107c204"
KEY="abe9396c32af452b8077bbcb7de2c16471bd61e4dc7972ccdb7a4c901611c619"
ARTS=((15154182116,"codeai-olean-r25-local-45896476614-1","sha256:3867b886fe066374d2e993cf150ea8e089797a86b6614ad9e155372cf98febb9"),
      (15154311770,"codeai-olean-r25-independent-45896476614-1","sha256:2f0f919236c7a46995d86edbef75f857baceab7dbc030c1ff786a45c8bd94577"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R25 lineage")
    for jid,steps in ((140171511971,["Verify R25 capsule typed lookup and exact application","Actual Lean MCP R25 new application audit"]),
                      (140172879095,["Independently reconstruct R25 capsule typed lookup and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R25 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R25 artifact")
    d=load(a.r25_local/"direct.json");mp=load(a.r25_local/"mcp.json");ind=load(a.r25_independent/"independent.json")
    v.need(d==load(a.r25_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R25_DIRECT_CAPSULE_TYPED_LOOKUP" and mp["status"]=="R25_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R25_INDEPENDENT_CAPSULE_TYPED_LOOKUP_GREEN" and ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           d["inventory"]["key"]==ind["inventory_key"]==KEY and d["registry_key"]==ind["registry_key"]==r25.KEY and
           ind["routes"]=={"exact_new":"REUSE_EXISTING","defeq_new":"REUSE_EXISTING","negative_new":"REFUTED_EXACT_TARGET","negative_defeq":"REFUTED_EXACT_TARGET"} and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R25 evidence")
    return d

def direct(a,out):
    prior=admit(a);hist,_=r25.admit(a);capsule,_=r24.admit(a)
    r20,_=r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"],"R20 inventory drift")
    e=hist["registry"];ci=gate.lookup.inventory(e,hist["reused_exact_negative"])
    v.need(ci==prior["inventory"] and prior["requests"]==r25.queries(hist) and
           hist["reused_exact_negative"]==capsule["reused_exact_negative"]==prior["reused_exact_negative"],"R25 registry lineage")
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest==e["manifest"] and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==manifest["source_sha256"],"capsule bytes")
    raw=r23.raw_read(folder,out,"RawRecallCapsule")
    v.need(raw==capsule["raw"] and r24.gate.sha(raw["type_expr"])==e["type_sha256"] and
           r24.gate.sha(raw["proof_expr"])==e["proof_sha256"],"capsule full type/proof")
    qs=prior["requests"];p,n=ci["candidates"]
    altered=copy.deepcopy(ci);altered["candidates"][0]["name"]="KuuOSR23.changed"
    controls={"changed_inventory":gate.lookup.preflight(altered,qs["exact_new"],old.SCOPE),
              "changed_scope":gate.lookup.preflight(ci,qs["exact_new"],"0"*64)}
    v.need(controls=={"changed_inventory":"HOLD_INVENTORY_INTEGRITY","changed_scope":"HOLD_SCOPE"},"recall preflight")
    r23.install(folder,manifest["files"])
    results={};parts=[];mcp_parts=[];expected={p["name"]:[],n["name"]:[]}
    imports={p["module"],n["module"]}
    selected={x["name"]:x for pool in inv["selected"].values() for x in pool}
    for k in ("local_refined_context","global_identity_context","wrong_source_context"):
        q=r20["requests"][k]
        log=r23.run_lean([],out/(k+".lean"),gate.render(q,inv,ci))
        rows=[json.loads(l[len(gate.root.MARK):]) for l in log.splitlines() if l.startswith(gate.root.MARK)]
        v.need(len(rows)==1,"R26 R20 root probe")
        row=rows[0];results[k]=row
        v.need({t["rule"] for t in row["root_trials"]}=={x["name"] for x in inv["selected"][row["root_head"]]},"root inventory")
        route=row["chosen"]["route"]
        if k=="wrong_source_context":
            v.need(route is None and row["exact_target_negative_candidate"] is None,"wrong source must HOLD")
            continue
        v.need(route is not None and route[0]["arity"] in (2,3),"R20 root not solved")
        req,src,mcp_src=gate.root.application(q,inv,route,"r26_"+k)
        _,w=typed.names(req)
        refs=sorted({x["rule"] for x in route})
        expected[w]=refs
        for name in refs:
            expected.setdefault(name,[])
            if name!=p["name"]:imports.add(selected[name]["module"])
        imports.update(q["context_modules"])
        parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
    v.need(any(any(x["rule"]==p["name"] for x in results[k]["chosen"]["route"])
               for k in ("local_refined_context","global_identity_context")),"no capsule recall in actual R20 route")
    log=r23.run_lean([],out/"AlternativeRoutes.lean",gate.fixture(qs,ci))
    xs=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(xs)==1,"OR control receipt")
    branch=xs[0]
    left=branch["left"];right=branch["right"];unknown=branch["unknown"]
    v.need(left["route"] is None and right["route"] is not None and unknown["route"] is None,"branch separation")
    blocked=[t for t in left["trace"] if t.get("status")=="HOLD_ROUTE_EXACT_NEGATIVE"]
    recalled=[t for t in right["trace"] if t.get("status")=="CAPSULE_EXACT_LEAF_CANDIDATE"]
    v.need(len(blocked)==1 and blocked[0]["rule"]==n["name"] and len(recalled)==2 and
           all(x["rule"]==p["name"] for x in recalled) and
           {x["structural_equal"] for x in recalled}=={True,False} and
           all(t.get("status")!="HOLD_ROUTE_EXACT_NEGATIVE" for t in unknown["trace"]),"typed premise recall")
    v.need(right["route"]==[{"rule":"KuuOSR26Fixture.rightRule","arity":2},
        {"rule":p["name"],"arity":0},{"rule":p["name"],"arity":0}],"alternative route changed")
    # The blocked leaf and both admitted leaves must be the exact R25 types
    # selected by the Lean comparison in the newly specialized root.
    v.need(blocked[0]["goal_expr"]==prior["comparisons"]["negative_defeq"]["target_expr"] and
           {x["goal_expr"] for x in recalled}=={prior["comparisons"][k]["target_expr"] for k in ("exact_new","defeq_new")},
           "residual target lineage")
    fix=gate.fixture_application(qs,ci)
    expected.update({"KuuOSR26Proof.alternative":[p["name"],"KuuOSR26Fixture.rightRule"],
                     "KuuOSR26Fixture.rightRule":["Or.inr"],
                     "KuuOSR26Proof.blockedPair":["KuuOSR26Proof.negativeLeaf"],
                     "KuuOSR26Proof.negativeLeaf":[n["name"]],
                     "KuuOSR26Proof.exactLeaf":[p["name"]],
                     "KuuOSR26Proof.defeqLeaf":[p["name"]]})
    import_src="".join("import "+m+"\n" for m in sorted(imports))
    names=sorted(expected)
    log=r23.run_lean([],out/"RecursiveApplications.lean",import_src+"\n"+"\n".join(parts)+"\n"+fix+"\n"+v.suffix(names))
    audit=v.read_direct(log,[{"name":name,"expected_direct_refs":expected[name]} for name in names])
    by_n={x["name"]:x for x in audit}
    v.need(by_n[p["name"]]["type_expr_repr"]==raw["type_expr"] and
           by_n[n["name"]]["type_expr_repr"]==prior["comparisons"]["negative_new"]["negative_type"],"source type changed")
    for name,x in by_n.items():
        v.need(set(x["axioms"])<=typed.STANDARD,"new axiom")
        if name.startswith("KuuOSR26Proof.") and name not in ("KuuOSR26Proof.negativeLeaf","KuuOSR26Proof.blockedPair"):
            v.need(n["name"] not in x["proof_constants"],"negative leaked into alternate proof")
    for k in ("local_refined_context","global_identity_context"):
        w=typed.NS+".r26_"+k+".witness"
        xs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
        matches=[x for x in xs if x["witness_name"]==w]
        v.need(len(matches)==1 and matches[0]["exact_kernel_type_match"] is True and
               matches[0]["target_expr_repr"]==results[k]["goal_expr"],"fresh R20 witness type")
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD,"source moved")
    d={"status":"R26_DIRECT_RECURSIVE_CAPSULE_RECALL","source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "r25_direct_digest":DIRECT,"r25_mcp_digest":MCP,"r20_direct_digest":old.digest(r20),
       "inventory_key":KEY,"root_inventory_digest":old.digest(inv),"results":results,"branch_control":branch,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":import_src+"\n"+"\n".join(mcp_parts)+"\n"+fix},
       "provider_calls":0,"capsule_rebuilds":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R26_DIRECT",json.dumps({"direct_digest":old.digest(d),"root_routes":{k:x["chosen"]["route"] for k,x in results.items()},
       "blocked_route":left["route"],"alternate_route":right["route"],"recalled":len(recalled),"controls":controls,
       "audits":len(audit),"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS recursive capsule recall","version":"1"}})
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
    result={"status":"R26_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R26_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R26_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R26_INDEPENDENT_RECURSIVE_CAPSULE_RECALL_GREEN","direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "routes":{"local_refined_context":"REUSE_EXISTING","global_identity_context":"REUSE_EXISTING",
                      "wrong_source_context":"HOLD","negative_premise_route":"BLOCKED_EXACT_PREMISE",
                      "alternative_route":"REUSE_EXISTING","unknown_premise":"HOLD"},
            "controls":d["controls"],"inventory_key":d["inventory_key"],"capsule_rebuilds":0,
            "mcp_audits":len(rows),"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R26_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r20-local","r20-independent","r25-local","r25-independent","r24-local","r24-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
