#!/usr/bin/env python3
"""R25: fresh closed proof requests without historical request identity."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_capsule_registry_v1_r24 as r24
from runtime import kuuos_codeai_olean_capsule_typed_lookup_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r23=r24.r23
v=r24.v
load=r24.load
ROOT=r24.ROOT
RUN=45895057363
HEAD="7c41da4f1a8d44f07f360e8596defecc4c9c1a7e"
DIRECT="9bc8688856a238d47e831fb0e5c645c93fb37893be254d062f43d54e1b04d093"
MCP="24bf9f6283279e6961c3ff08c057a6c7206e150cf8b9d431f1389f3c97e7e707"
KEY="2c9024e6182148ebd4fdf190b0face6cef31b2b860d6c5fba99db383ec16cdbe"
ARTS=((15153462254,"codeai-olean-r24-local-45895057363-1","sha256:f0c87c9782fb70d3ae75e319621d3635f3a066e2cbd9a8707ec58dfc0ce725c5"),
      (15152874367,"codeai-olean-r24-independent-45895057363-1","sha256:36591ac4030fef5164d6dc1f36b36c7bdeb4c4ea27ff8aac9d0b252bce875e4b"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R24 lineage")
    for jid,steps in ((140166801743,["Verify R24 capsule registry and exact application","Actual Lean MCP R24 new application audit"]),
                      (140168472193,["Independently reconstruct R24 capsule registry and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R24 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R24 artifact")
    d=load(a.r24_local/"direct.json");mp=load(a.r24_local/"mcp.json");ind=load(a.r24_independent/"independent.json")
    v.need(d==load(a.r24_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R24_DIRECT_CAPSULE_REGISTRY" and mp["status"]=="R24_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R24_INDEPENDENT_CAPSULE_REGISTRY_GREEN" and ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           d["registry"]==load(a.r24_local/"registry.json") and d["registry"]["key"]==ind["registry_key"]==KEY and
           ind["routes"]=={"global_identity_context":"REUSE_EXISTING","local_refined_context":"REUSE_EXISTING"} and
           ind["capsule_rebuilds"]==ind["new_root_searches"]==0 and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R24 evidence")
    return d,ind

def queries(d):
    c=r23.r22.r17.r13.c;ap=r23.r22.r17.r13.ap;L=r23.r22.r17.r13.LEC
    g=d["applications"]["global_identity_context"]["request"]["target"]
    bad=d["reused_exact_negative"]["request"]["target"]
    def compat(t):
        a=t["apply"];v.need(len(a)==6 and a[0]==c(L+".HasGlobal"),"global target form")
        return {"apply":[c(L+".Compatible")]+a[1:]}
    def identity(t):
        a=t["apply"];X,I,A,U,s=a[1:]
        shadow=ap(L+".shadowSections",X,I,A,A,U,ap("id",A),s)
        return {"apply":a[:-1]+[shadow]}
    good=compat(g);wrong=compat(bad)
    return {k:gate.request(k,t) for k,t in {
      "exact_new":good,"defeq_new":identity(good),"negative_new":bad,"negative_defeq":identity(bad),
      "wrong_atlas":wrong,"other_global":g}.items()}

def direct(a,out):
    hist,prior=admit(a);capsule,capind=r24.admit(a)
    e=hist["registry"]
    v.need(hist["r23_direct_digest"]==r24.DIRECT and hist["r23_mcp_digest"]==r24.MCP and
           hist["reused_exact_negative"]==capsule["reused_exact_negative"] and
           e["provenance"]["direct_digest"]==r24.DIRECT and e["provenance"]["mcp_digest"]==r24.MCP and
           e["provenance"]["artifact_id"]==r24.ARTS[0][0] and e["provenance"]["artifact_digest"]==r24.ARTS[0][2],"prior capsule lineage")
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest==e["manifest"] and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==e["manifest"]["source_sha256"],"capsule bytes")
    raw=r23.raw_read(folder,out,"RawTypedLookupCapsule")
    v.need(raw==capsule["raw"] and r24.gate.sha(raw["type_expr"])==e["type_sha256"] and
           r24.gate.sha(raw["proof_expr"])==e["proof_sha256"],"raw type/proof drift")
    inv=gate.inventory(e,hist["reused_exact_negative"]);v.save(out/"inventory.json",inv)
    qs=queries(hist)
    v.need(not set(qs)&set(e["request_digests"]) and all(q["request_digest"] not in e["request_digests"].values() for q in qs.values()),
           "requests must be fresh")
    wrong_inv=copy.deepcopy(inv);wrong_inv["candidates"][0]["name"]="KuuOSR23.changed"
    controls={"changed_inventory":gate.preflight(wrong_inv,qs["exact_new"],old.SCOPE),
              "changed_scope":gate.preflight(inv,qs["exact_new"],"0"*64)}
    v.need(controls=={"changed_inventory":"HOLD_INVENTORY_INTEGRITY","changed_scope":"HOLD_SCOPE"},"preflight controls")
    r23.install(folder,manifest["files"])
    log=r23.run_lean([],out/"TypedLookup.lean",gate.render(inv,qs))
    found=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    rows={r["case"]:r for r in found}
    v.need(len(found)==len(rows)==len(qs) and set(rows)==set(qs),"Lean lookup inventory")
    v.need(all(r["positive_type"]==raw["type_expr"] for r in rows.values()),"candidate type drift")
    expected={"exact_new":(True,False),"defeq_new":(True,False),"negative_new":(False,True),
              "negative_defeq":(False,True),"wrong_atlas":(False,False),"other_global":(False,False)}
    v.need(all((r["positive_defeq"],r["negative_defeq"])==expected[k] for k,r in rows.items()),"typed applicability matrix")
    v.need(rows["exact_new"]["positive_structural_equal"] is True and
           rows["defeq_new"]["positive_structural_equal"] is False and
           rows["negative_defeq"]["target_expr"]!=rows["negative_new"]["target_expr"] and
           rows["negative_new"]["target_expr"]==hist["reused_exact_negative"]["target_expr_repr"],"exact vs defeq fixtures")
    sources=[];mcp_sources=[];apps={};holds={};names={}
    for k,q in sorted(qs.items()):
        result=gate.decide(inv,q,rows[k])
        if result["status"]!="EXACT_APPLICATION_REQUIRED":
            holds[k]=result["status"];continue
        req,src,mcp=gate.application(inv,q,rows[k]);_,w=typed.names(req)
        apps[k]={"request":req,"lookup":result,"witness":w}
        names[w]=[req["source"]]
        sources.append(src.split("\n",1)[1]);mcp_sources.append(mcp.split("\n",1)[1])
    v.need(holds=={"other_global":"HOLD_NO_TYPED_MATCH","wrong_atlas":"HOLD_NO_TYPED_MATCH"} and len(apps)==4,"lookup route separation")
    # Audit the actual source declarations too, not just the fresh witnesses.
    for cand in inv["candidates"]:names[cand["name"]]=[]
    mods=sorted({x["module"] for x in inv["candidates"]})
    imports="".join("import "+m+"\n" for m in mods)
    log=r23.run_lean([],out/"FreshApplications.lean",imports+"\n"+"\n".join(sources)+"\n"+v.suffix(sorted(names)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":names[n]} for n in sorted(names)])
    by_n={x["name"]:x for x in audit}
    v.need(by_n[e["name"]]["type_expr_repr"]==raw["type_expr"] and
           by_n[inv["candidates"][1]["name"]]["type_expr_repr"]==rows["negative_new"]["negative_type"],"source full type drift")
    observed=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    by_w={r["witness_name"]:r for r in observed}
    v.need(len(observed)==len(by_w)==len(apps),"fresh proof inventory")
    for k,x in apps.items():
        w=x["witness"];z=by_w[w]
        v.need(z["exact_kernel_type_match"] is True and z["target_expr_repr"]==rows[k]["target_expr"] and
               z["witness_type_repr"]==by_n[w]["type_expr_repr"] and
               set(by_n[w]["axioms"])<=set(by_n[x["request"]["source"]]["axioms"]),"exact witness binding")
        x["application"]=z
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD,"source moved")
    d={"status":"R25_DIRECT_CAPSULE_TYPED_LOOKUP","source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "r24_direct_digest":DIRECT,"r24_mcp_digest":MCP,"registry_key":KEY,"inventory":inv,
       "requests":qs,"comparisons":rows,"applications":apps,"holds":holds,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":imports+"\n"+"\n".join(mcp_sources)},
       "reused_exact_negative":hist["reused_exact_negative"],"provider_calls":0,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R25_DIRECT",json.dumps({"direct_digest":old.digest(d),"fresh_requests":len(qs),
       "comparisons":{k:{"positive_defeq":r["positive_defeq"],"negative_defeq":r["negative_defeq"],
       "positive_structural_equal":r["positive_structural_equal"]} for k,r in rows.items()},
       "applications":sorted(apps),"holds":holds,"controls":controls,"capsule_rebuilds":0,"new_root_searches":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS typed capsule lookup","version":"1"}})
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
    result={"status":"R25_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R25_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R25_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R25_INDEPENDENT_CAPSULE_TYPED_LOOKUP_GREEN","direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"registry_key":d["registry_key"],"inventory_key":d["inventory"]["key"],
            "routes":{k:("REUSE_EXISTING" if a["request"]["polarity"]=="positive" else "REFUTED_EXACT_TARGET") for k,a in d["applications"].items()},
            "holds":d["holds"],"controls":d["controls"],"new_typed_applications":len(d["applications"]),
            "capsule_rebuilds":0,"new_root_searches":0,"mcp_audits":len(rows),
            "provider_calls":0,"unobserved_module_count":695,"semantic_search_complete":False,
            "proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R25_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r24-local","r24-independent","r23-local","r23-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
