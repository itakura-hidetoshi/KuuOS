#!/usr/bin/env python3
"""R12 data-driven application sandbox: existing WORLD and native F55 scopes."""
from __future__ import annotations
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_scope_transport_v1_r11 as r11
import check_codeai_olean_research_entry_v1_r10 as r10
import check_codeai_olean_typed_applicability_v1_r9 as r9
from runtime import kuuos_codeai_olean_general_application_v1 as gate
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob
from check_codeai_no_go_memory_v1_r2 import normalize

v=r9.v
r8=r9.r8
r5=r9.r5
prior=r9.prior
ROOT=v.ROOT
load=r5.load
WORLD=r9.MODULE
LEC="Kuu.LivingEngi"
F55=LEC+".NativeF55CechSourceGluingObstruction"
R11_RUN=45782188174
R11_HEAD="9b7bd6703e44f1f9571588dc58cc4f018e0a171a"
R11_ARTS=(
 (15098129613,"codeai-olean-r11-local-45782188174-1","sha256:8be75eddccea0888683ea0b2e4fa5d74c69e5b29e35123d48ed6bc89863fe394"),
 (15099630180,"codeai-olean-r11-independent-45782188174-1","sha256:86d5d4f4b1d3de8e4e7e38d090c23e00c003cbee4cee573d78f2893a201efedb"),
)
def admit_r11(local,independent):
    run=v.cache.api("actions/runs/"+str(R11_RUN))
    v.need(run["head_sha"]==R11_HEAD and run["run_attempt"]==1 and run["status"]=="completed"
           and run["conclusion"]=="success","R11 run lineage")
    for jid,step in ((139780087203,"Observe scope transport and actual pinned Lake library module closure"),
                     (139780889527,"Independently replay R11 and compare scope and Lake receipts")):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==R11_RUN and j["status"]=="completed" and j["conclusion"]=="success"
               and any(s["name"]==step and s["status"]=="completed" and s["conclusion"]=="success"
                       for s in j["steps"]),"R11 job/step lineage")
    for aid,n,dig in R11_ARTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==n and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==R11_RUN and a["workflow_run"]["head_sha"]==R11_HEAD,
               "R11 artifact lineage")
    a,b=load(local/"receipt.json"),load(independent/"receipt.json")
    cv=load(local/"lake-module-coverage.json")
    v.need(a==b and cv==load(independent/"lake-module-coverage.json")
           and a["status"]=="R11_SCOPE_TRANSPORT_AND_LAKE_CLOSURE_GREEN"
           and a["lake_coverage_digest"]==old.digest(cv)=="d9ca1a2a7e1ede70e729e96fa8365ae4a1fac048cc681a13e03e47cff24fde00"
           and a["transport_digest"]==old.digest(a["transport"])=="7063ff6c9a32cfe94ec5d0053130d7197fe82cb8ee08fcdaf3be97b46976dea6"
           and a["transport"]==r11.gate.observe_scope(v.cache.api)
           and cv["lake_module_count"]==2120 and cv["missing_inside_closure"]==0
           and cv["missing_outside_closure"]==695,"R11 evidence changed")
    return a

def c(n):return {"const":n}
def n(x):return {"nat":x}
def ap(f,*args):return {"apply":[c(f),*args]}
def lt(a,b):return ap("Nat.lt",n(a),n(b))
def global_target(atlas):
    return ap(LEC+".HasGlobal",c("Unit"),c("Bool"),c(LEC+".NorthNativeF55Raw"),
              c(LEC+".northNativeF55TwoChartCover"),c(LEC+"."+atlas))
def request(k,module,source,target,args,pol):
    return gate.make_request(k,module,source,target,args,pol)
def cases():
    step=ap(WORLD+".AlignmentStep.mk",n(4),n(0))
    valid=ap(WORLD+".AlignmentStep.Valid.mk",step,ap("Nat.zero_lt_succ",n(3)))
    fwd=WORLD+".valid_step_strictly_decreases"
    rev=WORLD+".opposite_strict_steps_are_impossible"
    reflex=WORLD+".strict_descent_is_not_reflexive"
    raw=LEC+".nativeF55_twoChart_raw_no_global"
    constant=LEC+".nativeF55_twoChart_constant_raw_global"
    a=global_target("northNativeF55TwoChartRaw")
    b=global_target("northNativeF55TwoChartConstantRaw")
    return {
     "new_forward":request("new_forward",WORLD,fwd,lt(0,4),[step,valid],"positive"),
     "new_reverse":request("new_reverse",WORLD,rev,lt(4,0),[n(4),n(0),ap("Nat.zero_lt_succ",n(3))],"negative"),
     "new_reflexive":request("new_reflexive",WORLD,reflex,lt(11,11),[n(11)],"negative"),
     "raw_atlas":request("raw_atlas",F55,raw,a,[],"negative"),
     "constant_atlas":request("constant_atlas",F55,constant,b,[],"positive"),
     "missing_premise":request("missing_premise",WORLD,rev,lt(4,0),[n(4),n(0)],"negative"),
     "wrong_target":request("wrong_target",WORLD,rev,lt(0,4),[n(4),n(0),ap("Nat.zero_lt_succ",n(3))],"negative"),
     "wrong_atlas":request("wrong_atlas",F55,raw,b,[],"negative"),
     "wrong_polarity":request("wrong_polarity",WORLD,reflex,lt(11,11),[n(11)],"positive"),
    }
EXPECTED={"new_forward":"REUSE_EXISTING","new_reverse":"REFUTED_EXACT_TARGET",
          "new_reflexive":"REFUTED_EXACT_TARGET","raw_atlas":"REFUTED_EXACT_TARGET",
          "constant_atlas":"REUSE_EXISTING"}
def archived(local,independent,lookup):
    for p in sorted(local.glob("exact-*")):
        if not (p/"receipt.json").is_file():continue
        a=load(p/"receipt.json")
        if a["module"]!=lookup["module"] or a["name"]!=lookup["name"]:continue
        b=independent/p.name
        v.need(a==load(b/"receipt.json") and lookup==load(p/"request.json")==load(b/"request.json"),
               "archived exact type request changed")
        with gzip.open(p/"kernel-types.jsonl.gz","rt",encoding="utf-8") as f:
            row=json.loads(f.readline())
            v.need(not f.read().strip() and row["name"]==a["name"]
                   and v.sha(row["type_expr_repr"].encode())==a["type_expr_sha256"],"archive type digest")
        return a
    return None

def direct(a,out):
    cov=admit_r11(a.r11_local,a.r11_independent)
    receipt,db=r8.admit(a.index,old.HEAD)
    r9.historical_r8(a.r8_local,a.r8_independent,old.HEAD)
    r10.admit_r9()
    d=load(a.r9_local/"direct.json");i=load(a.r9_independent/"direct.json")
    m=load(a.r9_local/"mcp.json");ctx=load(a.r9_independent/"routes.json")
    replay=load(a.r9_independent/"independent.json")
    old.admitted_context(receipt,d,i,m,ctx,replay)
    historical=load(a.r8_local/"direct.json")
    requests=cases()
    pairs=sorted({(r["module"],r["source"]) for r in requests.values()})
    plan=r8.prepare(db,receipt,old.R7,old.HEAD,[n for _,n in pairs],
                    "R12 exact selected WORLD and native F55 applications",
                    [{"module":m,"name":n} for m,n in pairs])
    v.need(plan["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and len(plan["requests"])==len(pairs)
           and len(plan["search"]["unobserved_modules"])==695 and plan["search"]["omitted_matches"]==0,
           "incomplete R7 search inventory")
    v.save(out/"search-plan.json",plan)
    env=r5.fixed_lean();materials={}
    for j,lookup in enumerate(plan["requests"]):
        module,name=lookup["module"],lookup["name"]
        source=lookup["coverage"]["sources"]
        v.need(len(source)==1 and git_blob((ROOT/source[0]["path"]).read_bytes())==source[0]["blob"],
               "source blob changed")
        bound,reason=r5.bind_files(module,ROOT/".lake/build/lib/lean"/(module.replace(".","/")+".olean"),source[0])
        v.need(reason is None and bound==lookup["binding"],"verified olean identity changed")
        x=archived(a.r9_local,a.r9_independent,lookup)
        reuse="R9" if x is not None else None
        if x is None:
            x=archived(a.r8_local,a.r8_independent,lookup)
            if x is not None:reuse="R8"
        if reuse=="R9":
            v.need(any(z["name"]==name and z["type_expr_sha256"]==x["type_expr_sha256"]
                       and z["request_digest"]==x["request_digest"] for z in d["materialized_sources"]),
                   "R9 reused type not in certified inventory")
        elif reuse=="R8":
            v.need({k:z for k,z in x.items() if k!="row"} in historical["selections"],
                   "R8 reused type not in certified inventory")
        else:
            x=r8.materialize(out/f"exact-{j:02}",lookup,{module:source},env)
        materials[module+"::"+name]={"module":module,"name":name,"type_expr_sha256":x["type_expr_sha256"],
             "request_digest":x["request_digest"],"artifact_binding_digest":x["artifact_binding_digest"],
             "reused":reuse}
    results={}
    for k,req in requests.items():
        t,w=gate.names(req)
        src=gate.render(req)+"\n"+v.suffix([req["source"],w])
        try:
            rc,log=prior.compile_source(out/(k+".lean"),src)
        except subprocess.TimeoutExpired:
            results[k]={"status":"HOLD_LEAN_APPLICATION","reason":"TIMEOUT","request_digest":req["request_digest"]}
            continue
        if rc:
            print("KUUOS_R12_HOLD_LEAN",k,log[-3500:],flush=True)
            results[k]={"status":"HOLD_LEAN_APPLICATION","reason":"LEAN_REJECTED" if "error:" in log else "RUNNER_FAILURE",
                        "request_digest":req["request_digest"]}
            continue
        rows=v.read_direct(log,[{"name":req["source"],"expected_direct_refs":[]},
                                 {"name":w,"expected_direct_refs":[req["source"]]}])
        apps=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
        v.need(len(apps)==1 and next(x for x in rows if x["name"]==req["source"])["type_expr_sha256"]
               ==materials[req["module"]+"::"+req["source"]]["type_expr_sha256"],"imported exact type mismatch")
        results[k]={"status":"EXACT_TYPED_APPLICATION","request_digest":req["request_digest"],
                    "observations":rows,"application":apps[0],"probe_sha256":v.sha(src.encode())}
    v.need({k for k,x in results.items() if x["status"]=="EXACT_TYPED_APPLICATION"}==set(EXPECTED)
           and all(x["reason"]=="LEAN_REJECTED" for k,x in results.items() if k not in EXPECTED),
           "positive or intentional mismatch controls did not behave as expected")
    v.need(r11.gate.observe_scope(v.cache.api)==cov["transport"],"source changed")
    result={"status":"R12_DIRECT_APPLICATIONS","source_head":old.HEAD,"source_tree":old.TREE,
            "scope_digest":old.SCOPE,"r11_receipt_digest":old.digest(cov),"r7_receipt_digest":old.R7,
            "search_plan_digest":plan["preflight_digest"],"unobserved_module_count":695,
            "requests":requests,"materialized_sources":materials,"results":results,"proof_authority":False}
    v.save(out/"direct.json",result)
    print("KUUOS_R12_DIRECT",json.dumps({"direct_digest":old.digest(result),
        "typed_applications":len(EXPECTED),"lean_hold_controls":len(results)-len(EXPECTED),
        "reused_types":sum(x["reused"] is not None for x in materials.values()),
        "new_types":sum(x["reused"] is None for x in materials.values())},sort_keys=True),flush=True)
    return result

def mcp(out):
    d=load(out/"direct.json")
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    audits={}
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS generalized typed applications","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools missing")
        for k,x in d["results"].items():
            if x["status"]!="EXACT_TYPED_APPLICATION":continue
            req=d["requests"][k]
            p=out/("Mcp_"+k+".lean")
            src=gate.declarations(req)+"\nset_option pp.universes false\n"+"\n".join("#check @"+r["name"] for r in x["observations"])+"\n"
            p.write_text(src,encoding="utf-8");rel=str(p.relative_to(ROOT))
            raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
            v.save(out/("mcp-diagnostics-"+k+".json"),raw);diag=v.structured(raw)
            v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
                   and diag["timed_out"] is False and diag["failed_dependencies"]==[]
                   and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"MCP diagnostic failed:"+k)
            audits[k]=[]
            for j,row in enumerate(x["observations"]):
                raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
                v.save(out/f"mcp-verify-{k}-{j}.json",raw);val=v.structured(raw)
                ax=normalize(val["axioms"])
                v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"MCP axiom mismatch")
                audits[k].append({"name":row["name"],"axioms":ax})
    finally:client.close()
    result={"status":"R12_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":audits,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R12_REAL_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":sum(map(len,audits.values()))}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d,"independent direct receipt differs")
    for k,x in a["results"].items():
        if x["status"]!="EXACT_TYPED_APPLICATION":continue
        diag=v.structured(load(first/("mcp-diagnostics-"+k+".json")))
        v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
               and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),
               "historical MCP diagnostics invalid")
        for j,row in enumerate(x["observations"]):
            raw=load(first/f"mcp-verify-{k}-{j}.json");val=v.structured(raw)
            v.need(raw["result"]["isError"] is False and val["warnings"]==[]
                   and normalize(val["axioms"])==row["axioms"]==mp["audits"][k][j]["axioms"]
                   and row["name"]==mp["audits"][k][j]["name"],"MCP response mismatch")
    ctx=gate.project(a,d,mp)
    v.need(ctx["status"]=="R12_INDEPENDENT_TYPED_ROUTES_OBSERVED","projection failed: "+str(ctx.get("issues")))
    cd=old.digest(ctx)
    routes={k:gate.pre_provider(ctx,cd,r) for k,r in d["requests"].items()}
    v.need({k:x["status"] for k,x in routes.items() if k in EXPECTED}==EXPECTED
           and all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" for k,x in routes.items() if k not in EXPECTED),
           "route control failed")
    req=d["requests"]["new_reverse"]
    controls={"changed_target":gate.pre_provider(ctx,cd,dict(req,target=lt(0,4))),
              "changed_arguments":gate.pre_provider(ctx,cd,dict(req,arguments=[])),
              "changed_source":gate.pre_provider(ctx,cd,dict(req,source=WORLD+".strict_descent_is_not_reflexive")),
              "wrong_context":gate.pre_provider(ctx,"0"*64,req),
              "missing_mcp":gate.project(a,d,{}),
              "changed_independent":gate.project(a,dict(d,unobserved_module_count=0),mp)}
    for k,bad in (("injected_command",{"const":"True\naxiom evil : False"}),("sorry_term",{"const":"sorry"})):
        try:gate.make_request(k,WORLD,req["source"],bad,[],"positive")
        except ValueError:controls[k]=gate.hold("invalid_term")
        else:raise ValueError("unsafe term accepted")
    v.need(all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and x["candidate_generation_allowed"] is False
               for x in list(controls.values())+list(routes.values()) if x["status"] not in EXPECTED.values()),
           "unsafe route")
    v.save(out/"routes.json",ctx);v.save(out/"controls.json",controls)
    result={"status":"R12_INDEPENDENT_GENERAL_APPLICATION_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"context_digest":cd,
            "routes":{k:x["status"] for k,x in routes.items()},"hold_controls":len(controls),
            "lean_hold_controls":len(routes)-len(EXPECTED),"provider_calls":0,
            "unobserved_module_count":695,"proof_authority":False,"semantic_search_complete":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R12_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("index","r8-local","r8-independent","r9-local","r9-independent","r11-local","r11-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":
    main()
