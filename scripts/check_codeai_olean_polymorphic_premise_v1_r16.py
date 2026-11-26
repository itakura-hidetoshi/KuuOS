#!/usr/bin/env python3
"""R16 bounded dependent argument inference with a two-step premise chain."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_global_premise_search_v1_r15 as r15
from runtime import kuuos_codeai_olean_polymorphic_premise_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import exact_lookup
from check_codeai_no_go_memory_v1_r2 import normalize

v=r15.v
r14=r15.r14
r13=r15.r13
r12=r15.r12
r8=r15.r8
ROOT=v.ROOT
load=r15.load
RUN=45795963449
HEAD="2443c3baa4e31d2d825f4c10416a8eddb54a17d5"
DIRECT="b072d5f26ae9f65df8d04a1568bbb5fbdc7af0acd3575134449c3dac31390e24"
MCP="68105afb21826642edf8ccf68d10ea3bb4a2ea2edaa43087b380bbcb05b18c37"
ARTS=(
 (15105116746,"codeai-olean-r15-local-45795963449-1","sha256:878969c32b93f268d09d435166511cafd9bf3da4142a7623e807612fe8b87d6b"),
 (15105202228,"codeai-olean-r15-independent-45795963449-1","sha256:34c472b9c3d7a13b6a916f96b9bcc5bf13df7319b5bcf77a7fe6ef9c79ea6db5"),
)
def admit_r15(local,independent):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R15 lineage")
    for jid,names in ((139826546633,["Verify R15 global ranking and exact Lean application",
                                    "Actual Lean MCP R15 new application audit"]),
                      (139828815831,["Independently reconstruct R15 global ranking and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success"
                           for s in j["steps"]) for n in names),"R15 job lineage")
    for aid,n,dig in ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==RUN and a["workflow_run"]["head_sha"]==HEAD,"R15 artifact")
    d,i=load(local/"direct.json"),load(independent/"direct.json")
    m=load(local/"mcp.json");res=load(independent/"independent.json")
    v.need(d==i and old.digest(d)==DIRECT and old.digest(m)==MCP
           and res["status"]=="R15_INDEPENDENT_GLOBAL_PREMISE_SEARCH_GREEN"
           and res["direct_digest"]==DIRECT and res["mcp_digest"]==MCP
           and m["direct_digest"]==DIRECT and d["source_head"]==old.HEAD,"R15 evidence changed")
    return d,res

def queries():
    c=r13.c;ap=r13.ap;L=r13.LEC
    raw=c(L+".NorthNativeF55Raw");shadow=c(L+".NorthNativeF55Shadow")
    cover=c(L+".northNativeF55TwoChartCover");obs=c(L+".northNativeF55Observe")
    out={}
    for k,atlas in (("constant","northNativeF55TwoChartConstantRaw"),("original","northNativeF55TwoChartRaw")):
        s=c(L+"."+atlas)
        readout=ap(L+".shadowSections",c("Unit"),c("Bool"),raw,shadow,cover,obs,s)
        target=ap(L+".Compatible",c("Unit"),c("Bool"),shadow,cover,readout)
        out[k]=gate.make_query(k,r13.CRITERION,L+".sourceCompatible_implies_shadowCompatible",
                                target,"positive",[r13.F55],[r13.SCOPED])
    # A different conclusion cannot be promoted from the same source.
    out["wrong_goal"]=gate.make_query("wrong_goal",r13.CRITERION,L+".sourceCompatible_implies_shadowCompatible",
        ap(L+".HasGlobal",c("Unit"),c("Bool"),raw,cover,c(L+".northNativeF55TwoChartRaw")),
        "positive",[r13.F55],[r13.SCOPED])
    return out

def probe(q,secondary,leaves,out,label):
    src=gate.render(q,secondary,leaves)
    rc,log=r12.prior.compile_source(out/(label+".lean"),src)
    if rc:
        print(log[-16000:],flush=True);raise ValueError("R16 probe failed:"+label)
    rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(rows)==1,"specialization receipt")
    return rows[0]

def direct(a,out):
    h15,res15=admit_r15(a.r15_local,a.r15_independent)
    h14,res14,_=r15.admit_r14(a.r14_local,a.r14_independent)
    h13,ctx13=r14.admit_r13(a.r13_local,a.r13_independent)
    transport=r12.r11.gate.observe_scope(v.cache.api)
    v.need(transport["status"]=="SAME_PROOF_SCOPE_OBSERVED" and transport["current_source_head"]==old.HEAD,"scope drift")
    receipt,db=r8.admit(a.index,old.HEAD)
    # The closed leaf is the same proof already used in R14/R15.
    leaf=h14["fresh_application"]["premises"][0]
    v.need(len(h14["fresh_application"]["premises"])==1
           and any(leaf==p for combo in h15["plans"]["compatible"]["combinations"] for p in combo)
           and res15["routes"]["compatible"]=="REUSE_EXISTING","historical leaf not independently admitted")
    qs=queries();results={};inventories={};winners={}
    for k,q in qs.items():
        first=probe(q,[],[],out,"Domain_"+k)
        if first["primary"]["status"]!="MATCH_RESIDUAL":
            results[k]=first;continue
        v.need(len(first["primary"]["residuals"])==1,"bounded single residual")
        inv=gate.candidates(db,q,first["primary"]["heads"][0]);inventories[k]=inv
        v.save(out/(k+"-candidate-inventory.json"),inv)
        row=probe(q,inv["selected"],[leaf],out,"Chain_"+k)
        v.need(row["goal_expr"]==first["goal_expr"] and row["primary"]==first["primary"],"import context drift")
        v.need([x["secondary"]["name"] for x in row["branches"]]==[p["name"] for p in inv["selected"]],
               "secondary candidate inventory")
        results[k]=row
        for b,p in zip(row["branches"],inv["selected"]):
            if b["secondary"]["status"]=="MATCH_RESIDUAL":
                v.need([x["name"] for x in b["leaves"]]==[leaf["name"]],"leaf comparison inventory")
                if b["leaves"][0]["status"]=="MATCH_COMPLETE":
                    winners.setdefault(k,[]).append(p)
    v.need(set(winners)=={"constant"} and len(winners["constant"])==1,"specialization controls")
    v.need(results["constant"]["primary"]["universe_parameters"]>0
           and results["constant"]["primary"]["inferred"]>0
           and results["original"]["primary"]["status"]=="MATCH_RESIDUAL"
           and any(b["secondary"]["status"]=="MATCH_RESIDUAL" and
                   b["leaves"][0]["status"]=="HOLD_NOT_DEFEQ" for b in results["original"]["branches"])
           and results["wrong_goal"]["primary"]["status"]=="HOLD_NOT_DEFEQ","HOLD controls")
    q=qs["constant"];secondary=winners["constant"][0]
    req,src,mcp_src=gate.application(q,secondary,leaf,"polymorphic_chain")
    _,w=typed.names(req);sources=[{"module":req["module"],"name":req["source"]},secondary,leaf]
    names=sorted({p["name"] for p in sources}|{w})
    materials={}
    for j,p in enumerate(sources):
        key=p["module"]+"::"+p["name"]
        materials[key]=r15.material(db,receipt,h13,h14,p["module"],p["name"],out/("exact-"+str(j)))
        if "type_expr_sha256" in p:
            v.need(materials[key]["type_expr_sha256"]==p["type_expr_sha256"],"historical leaf type")
    src+="\n"+v.suffix(names)
    rc,log=r12.prior.compile_source(out/"NewApplication.lean",src)
    if rc:print(log[-16000:],flush=True);raise ValueError("R16 final application failed")
    rows=v.read_direct(log,[{"name":n,"expected_direct_refs":[p["name"] for p in sources] if n==w else []}
                            for n in names])
    apps=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    v.need(len(apps)==1 and apps[0]["exact_kernel_type_match"] is True
           and apps[0]["target_expr_repr"]==results["constant"]["goal_expr"],"exact goal binding")
    for p in sources:
        v.need(next(x for x in rows if x["name"]==p["name"])["type_expr_sha256"]
               ==materials[p["module"]+"::"+p["name"]]["type_expr_sha256"],"imported type changed")
    v.need(r12.r11.gate.observe_scope(v.cache.api)==transport,"source moved")
    fresh={"request":req,"premises":[secondary,leaf],"observations":rows,"application":apps[0],
           "mcp_source":mcp_src+"\nset_option pp.universes false\n"+"\n".join("#check @"+n for n in names)+"\n"}
    d={"status":"R16_DIRECT_POLYMORPHIC_PREMISE_CHAIN","source_head":old.HEAD,"source_tree":old.TREE,
       "scope_digest":old.SCOPE,"r15_direct_digest":DIRECT,"historical_routes":res15["routes"],
       "queries":qs,"inventories":inventories,"specializations":results,"materials":materials,"fresh_application":fresh,
       "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R16_DIRECT",json.dumps({"direct_digest":old.digest(d),
          "primary":{k:{z:p for z,p in row["primary"].items() if z!="residuals"} for k,row in results.items()},
          "secondary_candidates":{k:len(x["selected"]) for k,x in inventories.items()},
          "secondary_winner":secondary["name"],"leaf":leaf["name"],"new_applications":1,
          "historical_routes_retained":len(res15["routes"])},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS polymorphic premise specialization","version":"1"}})
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
    result={"status":"R16_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R16_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R16_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
           and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnosis")
    x=d["fresh_application"];_,w=typed.names(x["request"])
    v.need(len(mp["audits"])==len(x["observations"]),"MCP inventory")
    for j,row in enumerate(x["observations"]):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[]
               and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"]
               and row["name"]==mp["audits"][j]["name"],"MCP evidence mismatch")
    witness=next(r for r in x["observations"] if r["name"]==w)
    v.need(x["application"]["witness_type_repr"]==witness["type_expr_repr"]
           and x["application"]["exact_kernel_type_match"] is True
           and x["request"]["source"] in witness["proof_constants"]
           and {p["name"] for p in x["premises"]}<=set(witness["proof_constants"]),"new witness evidence")
    result={"status":"R16_INDEPENDENT_POLYMORPHIC_PREMISE_CHAIN_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"routes":{"constant":"REUSE_EXISTING","original":"HOLD_TYPED_APPLICABILITY_REVIEW",
            "wrong_goal":"HOLD_TYPED_APPLICABILITY_REVIEW"},"historical_routes":d["historical_routes"],
            "new_typed_applications":1,"mcp_audits":len(mp["audits"]),"provider_calls":0,
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,
            "candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R16_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r13-local","r13-independent","r14-local","r14-independent","r15-local","r15-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
