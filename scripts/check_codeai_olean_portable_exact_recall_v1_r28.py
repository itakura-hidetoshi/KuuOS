#!/usr/bin/env python3
"""R28: independent admission of persisted exact-goal recall memory."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_multi_typed_recall_v1_r27_r2 as r27
from runtime import kuuos_codeai_olean_portable_exact_recall_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r27.v
r23=r27.r23
r24=r27.r24
r25=r27.r25
load=r27.load
ROOT=r27.ROOT
RUN=45901313851
HEAD="4b3889aa3f5bb2c287721b772c4e9b580326cc5a"
DIRECT="f6c1a4d1b1ef6548af45b86f8b12ea430a5a1cde1e655e3822cd1736d81a0750"
MCP="da1c151e133d62a644eb3d3491ec21f90139cd6a1500e4dcebbefe614ac01c2f"
KEY="e8c2432768ea3dd062a0db14cf845e860f86335c19281e301294f8ec38ff905b"
ARTS=((15155193581,"codeai-olean-r27-r2-local-45901313851-1","sha256:ea93b8ed4f2fc89596cd5daa48dceb2654fa17fd74794c5f7737dc358f5e8d3e"),
      (15156532332,"codeai-olean-r27-r2-independent-45901313851-1","sha256:9ab61b990c4a07b707f8681e5b7fa129b12e47173acb12f9ce378f4031ed500a"))

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R27 lineage")
    for jid,steps in ((140187492000,["Verify R27 R2 multi typed recall and exact application","Actual Lean MCP R27 R2 new application audit"]),
                      (140189131473,["Independently reconstruct R27 R2 multi typed recall and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R27 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R27 artifact")
    d=load(a.r27_local/"direct.json");mp=load(a.r27_local/"mcp.json");ind=load(a.r27_independent/"independent.json")
    v.need(d==load(a.r27_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R27_DIRECT_MULTI_TYPED_RECALL" and mp["status"]=="R27_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R27_INDEPENDENT_MULTI_TYPED_RECALL_GREEN" and ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           d["inventory_key"]==ind["inventory_key"]==KEY and ind["candidate_count"]==5 and ind["mcp_audits"]==24 and
           len(ind["replay_hits"])==7 and sum(ind["replay_hits"].values())==35 and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R27 evidence")
    return d,mp,ind

def direct(a,out):
    previous,mp,ind=admit(a)
    prior=r27.admit(a);hist,_=r25.admit(a);capsule,_=r24.admit(a)
    r20,_=r27.r21.admit_r20(a.r20_local,a.r20_independent)
    e=hist["registry"];ci=gate.prior.lookup.inventory(e,hist["reused_exact_negative"])
    v.need(ci==prior["inventory"] and prior["requests"]==r25.queries(hist) and
           hist["reused_exact_negative"]==capsule["reused_exact_negative"]==prior["reused_exact_negative"],"R25 registry lineage")
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest==e["manifest"] and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==manifest["source_sha256"],"capsule bytes")
    raw=r23.raw_read(folder,out,"RawPortableCapsule")
    v.need(raw==capsule["raw"] and r24.gate.sha(raw["type_expr"])==e["type_sha256"] and
           r24.gate.sha(raw["proof_expr"])==e["proof_sha256"],"capsule full type/proof")
    r23.install(folder,manifest["files"])
    reg=previous["registry"];v.need(reg["parent_inventory_key"]==ci["key"],"registry lineage")
    targets=gate.prior.targets(prior["requests"],r20)
    trusted=gate.memory(previous,mp,ind,targets)
    v.need(len(trusted["records"])==7 and gate.validate(trusted,trusted,reg)=="EXACT_OBSERVATION_REQUIRED","memory projection")
    # Independent runner must admit the actual sandbox memory, not just a new copy.
    mem=load(a.first/"portable-memory.json") if a.phase=="independent" else trusted
    v.need(gate.validate(mem,trusted,reg)=="EXACT_OBSERVATION_REQUIRED","portable memory changed")
    v.save(out/"portable-memory.json",mem)
    if a.phase=="independent":
        v.need((out/"portable-memory.json").read_bytes()==(a.first/"portable-memory.json").read_bytes(),"memory transport bytes")
    fresh={"fresh_"+k:t for k,t in targets.items()}
    fresh["new_target"]={"const":"True"}
    log=r23.run_lean([],out/"ObservePortableTargets.lean",gate.render(fresh,reg))
    rows=[json.loads(l[len(gate.MARK):]) for l in log.splitlines() if l.startswith(gate.MARK)]
    v.need(len(rows)==1,"live target observation")
    obs=rows[0]
    exprs={x["case"]:x["expr"] for x in obs["targets"]}
    types={x["name"]:gate.hash_type(x["type_expr"]) for x in obs["types"]}
    v.need(set(exprs)==set(fresh) and len(obs["targets"])==len(fresh) and
           len(obs["types"])==len(types)==len(reg["candidates"]) and
           types=={c["name"]:c["type_sha256"] for c in reg["candidates"]},"live inventory drift")
    decisions={k:gate.decide(mem,trusted,reg,x,types) for k,x in exprs.items()}
    v.need(decisions["fresh_unknown"]["status"]=="HOLD_HISTORICAL_NO_MATCH" and
           decisions["new_target"]["status"]=="HOLD_SEARCH_REQUIRED" and
           sum(x["status"]=="EXACT_APPLICATION_REQUIRED" for x in decisions.values())==6,"portable recall outcomes")
    wrong=copy.deepcopy(mem);wrong["records"].clear()
    forged=gate.seal(wrong)
    scoped=gate.seal({**mem,"scope_digest":"0"*64})
    stale=copy.deepcopy(types);stale[next(iter(stale))]="0"*64
    wrongreg=copy.deepcopy(reg);wrongreg["candidates"][0]["type_sha256"]="0"*64
    x=exprs["fresh_capsule_exact"]
    controls={"tampered":gate.decide(wrong,trusted,reg,x,types)["status"],
              "self_resealed":gate.decide(forged,trusted,reg,x,types)["status"],
              "scope":gate.decide(scoped,trusted,reg,x,types)["status"],
              "registry":gate.decide(mem,trusted,wrongreg,x,types)["status"],
              "live_type":gate.decide(mem,trusted,reg,x,stale)["status"]}
    v.need(controls=={"tampered":"HOLD_MEMORY_INTEGRITY","self_resealed":"HOLD_UNADMITTED_MEMORY","scope":"HOLD_SCOPE",
                      "registry":"HOLD_INVENTORY_INTEGRITY","live_type":"HOLD_SOURCE_TYPE_DRIFT"},"portable negative controls")
    imports="".join("import "+m+"\n" for m in sorted({c["module"] for c in reg["candidates"]}))
    expected={c["name"]:[] for c in reg["candidates"]};parts=[];mcp_parts=[];applications={}
    for k,d in sorted(decisions.items()):
        if d["status"]!="EXACT_APPLICATION_REQUIRED":continue
        c=d["candidate"];row=mem["records"][d["record_key"]]
        v.need(row["target"]==fresh[k] and "fresh_"+row["case"]==k,"fresh goal identity")
        req=typed.make_request("r28_"+k,c["module"],c["name"],fresh[k],[],c["polarity"])
        _,w=typed.names(req)
        applications[k]={"request":req,"witness":w,"record_key":d["record_key"]}
        expected[w]=[c["name"]]
        parts.append(typed.render(req).split("\n",1)[1])
        mcp_parts.append(typed.declarations(req).split("\n",1)[1])
    names=sorted(expected)
    log=r23.run_lean([],out/"PortableApplications.lean",imports+"\n"+"\n".join(parts)+"\n"+v.suffix(names))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in names])
    by_n={r["name"]:r for r in audit}
    for c in reg["candidates"]:
        v.need(by_n[c["name"]]["type_expr_sha256"]==c["type_sha256"] and by_n[c["name"]]["axioms"]==c["axioms"],"live audited source drift")
    app_rows=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    by_w={r["witness_name"]:r for r in app_rows}
    v.need(len(by_w)==len(app_rows)==len(applications)==6,"fresh application inventory")
    for k,a0 in applications.items():
        w=by_w[a0["witness"]];q=a0["request"];z=by_n[a0["witness"]]
        v.need(w["exact_kernel_type_match"] is True and w["target_expr_repr"]==exprs[k] and
               w["witness_type_repr"]==z["type_expr_repr"] and q["source"] in z["proof_constants"] and
               set(z["axioms"])<=set(by_n[q["source"]]["axioms"]),"fresh witness binding")
        a0["application"]=w
    v.need(v.cache.api("git/ref/heads/main")["object"]["sha"]==old.HEAD and
           old.digest(v.cache.remote_scope(v.cache.api,old.HEAD))==old.SCOPE,"source moved")
    d={"status":"R28_DIRECT_PORTABLE_EXACT_RECALL","source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
       "r27_direct_digest":DIRECT,"r27_mcp_digest":MCP,"inventory_key":KEY,"memory_key":mem["key"],"decisions":decisions,
       "targets":fresh,"observations":obs,"applications":applications,"controls":controls,
       "fresh_application":{"observations":audit,"mcp_source":imports+"\n"+"\n".join(mcp_parts)},
       "root_searches":0,"capsule_rebuilds":0,"candidate_comparison_searches":0,"provider_calls":0,
       "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R28_DIRECT",json.dumps({"direct_digest":old.digest(d),"memory_key":mem["key"],"memory_records":len(mem["records"]),
        "fresh_targets":len(fresh),"applications":len(applications),"holds":{k:x["status"] for k,x in decisions.items() if k not in applications},
        "controls":controls,"audits":len(audit),"candidate_comparison_searches":0,"root_searches":0,"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS portable exact recall","version":"1"}})
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
    result={"status":"R28_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R28_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R28_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R28_INDEPENDENT_PORTABLE_EXACT_RECALL_GREEN","direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "memory_key":d["memory_key"],"inventory_key":d["inventory_key"],"transport_bytes_equal":True,
            "routes":{k:("REUSE_EXISTING" if x["request"]["polarity"]=="positive" else "REFUTED_EXACT_TARGET") for k,x in d["applications"].items()},
            "holds":{k:x["status"] for k,x in d["decisions"].items() if k not in d["applications"]},"controls":d["controls"],
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),"candidate_comparison_searches":0,
            "root_searches":0,"capsule_rebuilds":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R28_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r27-local","r27-independent","r20-local","r20-independent","r25-local","r25-independent","r24-local","r24-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
