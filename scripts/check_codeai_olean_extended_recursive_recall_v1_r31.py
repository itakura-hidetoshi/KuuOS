#!/usr/bin/env python3
"""R31: use a certified cumulative ledger inside the original recursive engine."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_memory_extension_v1_r30 as r30
from runtime import kuuos_codeai_olean_extended_recursive_recall_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r29=r30.r29
r23=r30.r23
v=r30.v
ROOT=r30.ROOT
load=r30.load
RUN=45907621139
HEAD="5db598a74e3f62efb1139cda50e2c048076cdbca"
ARTS=((15158616870,"codeai-olean-r30-local-45907621139-1","sha256:49e8be6557cce9010350eea5ec42c6480b713d9d767214f8cf13b2c1691d2a46"),
      (15158558295,"codeai-olean-r30-independent-45907621139-1","sha256:bda9ada26d4400d21d86f35a4b2d9ee1756add88587decb31e6188d00ba78869"))

def admit(a,scope):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R30 lineage")
    for jid,steps in ((140208049138,["Verify R30 append only proof memory and exact application","Actual Lean MCP R30 new application audit"]),
                      (140209597128,["Independently reconstruct R30 append only proof memory and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R30 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R30 artifact")
    d=load(a.r30_local/"direct.json");mp=load(a.r30_local/"mcp.json");ind=load(a.r30_independent/"independent.json")
    v.need(d==load(a.r30_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP and
           d["status"]=="R30_DIRECT_APPEND_ONLY_MEMORY" and mp["status"]=="R30_REAL_MCP_GREEN" and
           mp["direct_digest"]==gate.DIRECT and ind["status"]=="R30_INDEPENDENT_APPEND_ONLY_MEMORY_GREEN" and
           ind["direct_digest"]==gate.DIRECT and ind["mcp_digest"]==gate.MCP and
           d["extension_key"]==ind["extension_key"]==gate.KEY and d["parent_memory_key"]==ind["parent_memory_key"]==gate.prev.R28_MEMORY and
           ind["historical_memory_bytes_preserved"] is True and ind["raw_proof_equality"] is True and ind["imported_sandbox_capsule"] is True and
           ind["new_records"]==3 and ind["distinct_target_count"]==9 and ind["global_alternatives"]==2 and ind["mcp_audits"]==14 and
           d["source_head"]==gate.prev.CURRENT and d["source_tree"]==gate.prev.CURRENT_TREE and d["scope_digest"]==old.SCOPE,"R30 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R30 audit binding")
    for name in ("portable-memory.json","extension.json","transport.json","capsule-manifest.json"):
        v.need((a.r30_local/name).read_bytes()==(a.r30_independent/name).read_bytes(),"R30 exact bytes "+name)
    mem=load(a.r30_local/"portable-memory.json");layer=load(a.r30_local/"extension.json");bridge=load(a.r30_local/"transport.json")
    v.need(layer["key"]==gate.KEY and bridge["key"]==d["transport_key"]==r30.BRIDGE and
           gate.portable.seal(bridge)["key"]==bridge["key"] and bridge["scope"]==scope and
           layer["capsule_manifest"]==d["capsule_manifest"] and layer["r29_direct_digest"]==r30.DIRECT,"R30 scope binding")
    return d,mem,layer,bridge

def direct(a,out):
    scope=r29.observe_scope()
    prior,mem,layer,bridge=admit(a,scope)
    reg=prior["registry"];rows=gate.ledger(mem,layer,bridge,reg)
    for name in ("portable-memory.json","extension.json","transport.json"):
        (out/name).write_bytes((a.r30_local/name).read_bytes())
        if a.phase=="independent":v.need((out/name).read_bytes()==(a.first/name).read_bytes(),"R31 ledger bytes")
    v.save(out/"ledger-view.json",rows)
    capsule=r29.admit_capsule(a)
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["source_sha256"]==r29.r24.SOURCE and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==r29.r24.SOURCE,"R23 exact bytes")
    v.need(r23.raw_read(folder,out,"RawR23")==capsule["raw"],"R23 raw proof")
    r23.install(folder,manifest["files"])
    folder=a.r30_local/"capsule";man=prior["capsule_manifest"]
    v.need(man==load(a.r30_local/"capsule-manifest.json") and man["module"]==gate.ext.MODULE and
           r30.capsule_files(folder)==man["files"] and r23.sha((folder/(gate.ext.MODULE+".lean")).read_bytes())==man["source_sha256"],"R30 capsule bytes")
    names=sorted(prior["raw"])
    v.need(r30.raw_read(folder,out,"RawR30",names)==prior["raw"] and
           r30.raw_read(a.r30_independent/"capsule",out,"RawR30Independent",names)==prior["raw"],"R30 complete type/proof equality")
    r30.install(folder,man)
    hist={x["name"]:x for x in prior["fresh_application"]["observations"]}
    types={c["name"]:hist[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    log=r23.run_lean([],out/"ExtendedBranches.lean",gate.fixture(rows,reg))
    gate.check_live(log,rows,reg,types)
    branch=r29.parse(log,gate.MARK)
    left,right,unknown,fresh=(branch[k] for k in ("left","right","unknown","fresh"))
    blocked=gate.hits(left["trace"],rows);alt=gate.hits(right["trace"],rows)
    v.need(left["route"] is None and len([x for x in blocked if x["status"]==gate.NEG])==1 and
           any(x["rule"]==gate.ext.NEGATIVE for x in blocked) and
           len(alt)==2 and all(x["status"]==gate.POS for x in alt) and
           sorted(len(x["matches"]) for x in alt)==[1,2],"new recursive branches")
    v.need(unknown["route"] is None and unknown["trace"][0]["status"]==gate.MISS and
           unknown["trace"][0]["candidate_comparison_searches"]==3,"historical miss must compare new candidates only")
    v.need(fresh["route"]==[{"rule":"KuuOSR31Fixture.truth","arity":0}] and fresh["trace"][0]["status"]==gate.FRESH and
           fresh["trace"][0]["candidate_comparison_searches"]==8,"new target must reach indexed fallback")
    fix,refs=gate.fixture_proofs(rows,branch)
    expected={c["name"]:[] for c in reg["candidates"]};expected[gate.ext.NEGATIVE_LEAF]=[]
    expected.update(refs)
    imports={c["module"] for c in reg["candidates"]}
    parts=[];mcp_parts=[];apps={};roots={};root_hits={}
    registered={c["name"]:c for c in reg["candidates"]}
    r20,_=r29.r28.r27.r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"],"R20 inventory")
    selected={x["name"]:x for pool in inv["selected"].values() for x in pool}
    def application(req,src,mcp_src,refs,expr):
        _,w=typed.names(req);expected[w]=refs
        apps[w]={"request":req,"expected_target_expr":expr}
        parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        for n in refs:
            expected.setdefault(n,[])
            imports.add((registered[n] if n in registered else selected[n])["module"])
    for key,r in sorted(rows.items()):
        for i,c in enumerate(r["matches"]):
            req=typed.make_request("r31_"+r["alias"]+"_"+str(i),c["module"],c["name"],r["target"],[],c["polarity"])
            application(req,typed.render(req),typed.declarations(req),[c["name"]],r["target_expr"])
    for k in ("local_refined_context","global_identity_context","wrong_source_context"):
        q=r20["requests"][k]
        log=r23.run_lean([],out/(k+".lean"),gate.render(q,inv,rows,reg))
        gate.check_live(log,rows,reg,types)
        r=r29.parse(log,gate.root.MARK);roots[k]=r
        v.need({x["rule"] for x in r["root_trials"]}=={x["name"] for x in inv["selected"][r["root_head"]]},"root inventory")
        route=r["chosen"]["route"]
        if k=="wrong_source_context":
            v.need(route is None,"wrong context must HOLD")
            continue
        v.need(route is not None and route[0]["arity"] in (2,3),"root discovery")
        bs=[b for b in r["branches"] if b["rule"]==route[0]["rule"] and b["first"]["route"]==route]
        v.need(len(bs)==1,"root branch identity")
        root_hits[k]=gate.hits(bs[0]["first"]["trace"],rows)
        req,src,mcp_src=gate.root.application(q,inv,route,"r31_"+k)
        imports.update(q["context_modules"])
        application(req,src,mcp_src,sorted({x["rule"] for x in route}),r["goal_expr"])
    v.need(sum(len(x) for x in root_hits.values())>0,"no actual root memory recall")
    imp="".join("import "+m+"\n" for m in sorted(imports))
    log=r23.run_lean([],out/"R31Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+fix+"\n"+v.suffix(sorted(expected)))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by_n={x["name"]:x for x in audit}
    for n in list(registered)+[gate.ext.NEGATIVE_LEAF]:
        v.need(by_n[n]["type_expr_repr"]==hist[n]["type_expr_repr"] and
               by_n[n]["proof_constants"]==hist[n]["proof_constants"] and by_n[n]["axioms"]==hist[n]["axioms"],"imported proof drift "+n)
    for n in ("KuuOSR31Proof.alternate0","KuuOSR31Proof.alternate1"):
        v.need(gate.ext.NEGATIVE not in by_n[n]["proof_constants"],"negative leaked into positive proof")
    obs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    ws={r["witness_name"]:r for r in obs}
    v.need(len(ws)==len(obs)==len(apps)==11,"fresh witness inventory")
    for w,x in apps.items():
        r=ws[w]
        v.need(r["exact_kernel_type_match"] is True and r["target_expr_repr"]==x["expected_target_expr"] and
               r["witness_type_repr"]==by_n[w]["type_expr_repr"],"typed witness "+w)
        x["application"]=r
    v.need(r29.observe_scope()==scope,"main moved")
    d={"status":"R31_DIRECT_EXTENDED_RECURSIVE_RECALL","source_head":gate.prev.CURRENT,"source_tree":gate.prev.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r30_direct_digest":gate.DIRECT,"r30_mcp_digest":gate.MCP,
       "extension_key":layer["key"],"parent_memory_key":mem["key"],"transport_key":bridge["key"],
       "ledger_view_digest":old.digest(rows),"branch_control":branch,"root_results":roots,"root_memory_hits":root_hits,
       "applications":apps,"fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)+"\n"+fix},
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R31_DIRECT",json.dumps({"direct_digest":old.digest(d),"extension_key":layer["key"],
       "distinct_targets":len(rows),"ledger_witnesses":sum(len(r["matches"]) for r in rows.values()),
       "global_alternatives":len(gate.case(rows,"global_identity_context")[1]["matches"]),
       "blocked_route":left["route"],"alternate_route":right["route"],"new_target_route":fresh["route"],
       "historical_miss_comparisons":3,"new_target_comparisons":8,"root_memory_hits":{k:len(x) for k,x in root_hits.items()},
       "fresh_applications":len(apps),"audits":len(audit),"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS extended recursive recall","version":"1"}})
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
    result={"status":"R31_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R31_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R31_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in ("portable-memory.json","extension.json","transport.json","ledger-view.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    result={"status":"R31_INDEPENDENT_EXTENDED_RECURSIVE_RECALL_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
            "extension_key":d["extension_key"],"ledger_view_digest":d["ledger_view_digest"],"parent_memory_key":d["parent_memory_key"],
            "transport_key":d["transport_key"],"ledger_bytes_equal":True,"global_alternatives":2,
            "root_memory_hits":{k:len(x) for k,x in d["root_memory_hits"].items()},
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),"capsule_rebuilds":0,"provider_calls":0,
            "historical_miss_comparisons":3,"new_target_comparisons":8,
            "routes":{"alternate_0":"REUSE_EXISTING","alternate_1":"REUSE_EXISTING",
                      "negative_conjunctive_premise":"BLOCKED_EXACT_PREMISE","historical_miss":"HOLD_SEARCH_CONTINUES",
                      "fresh_target":"INDEXED_FALLBACK_PROVED","wrong_source_context":"HOLD"},
            "unobserved_module_count":695,"semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R31_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r30-local","r30-independent","r20-local","r20-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
