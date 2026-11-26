#!/usr/bin/env python3
"""R29: new canonical scope admission and persistent recall in R20 recursion."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_portable_exact_recall_v1_r28 as r28
from runtime import kuuos_codeai_olean_portable_recursive_recall_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
v=r28.v
r23=r28.r23
r24=r28.r24
load=r28.load
ROOT=r28.ROOT
RUN=45902979815
HEAD="c05a986ecd571a1b00da255a7552ee8a54b4a709"
DIRECT=gate.R28_DIRECT
MCP=gate.R28_MCP
ARTS=((15156164812,"codeai-olean-r28-local-45902979815-1","sha256:c70156caa2cca261c94796353f5ae065ebf9398e13f52fdd22458f745397f77e"),
      (15156941455,"codeai-olean-r28-independent-45902979815-1","sha256:9f8f6c5274bdae9e3d4f07565868f33d7f77c6c9675b945a7d391e3556b671d7"))

def observe_scope():
    api=v.cache.api
    v.need(api("git/ref/heads/main")["object"]["sha"]==gate.CURRENT,"current main moved")
    oldc=api("git/commits/"+old.HEAD);newc=api("git/commits/"+gate.CURRENT)
    v.need(oldc["sha"]==old.HEAD and oldc["tree"]["sha"]==old.TREE and
           newc["sha"]==gate.CURRENT and newc["tree"]["sha"]==gate.CURRENT_TREE and
           v.cache.ancestor(api,old.HEAD,gate.CURRENT),"canonical ancestry")
    h=v.cache.remote_scope(api,old.HEAD);c=v.cache.remote_scope(api,gate.CURRENT)
    v.need(h==c==v.cache.local_scope(ROOT,gate.CURRENT) and old.digest(h)==old.SCOPE,"proof scope mismatch")
    diff=api("compare/"+old.HEAD+"..."+gate.CURRENT+"?per_page=100")
    paths=sorted(x["filename"] for x in diff["files"])
    v.need(diff["status"]=="ahead" and diff["merge_base_commit"]["sha"]==old.HEAD and
           paths==["README.md","ROADMAP.md","docs/history/README-SNAPSHOT-20261122.md","docs/history/ROADMAP-SNAPSHOT-20261122.md"],
           "unexpected canonical change")
    a=api("git/trees/"+old.TREE);b=api("git/trees/"+gate.CURRENT_TREE)
    v.need(not a["truncated"] and not b["truncated"],"incomplete roots")
    def non_docs(t):
        return {x["path"]:(x["mode"],x["type"],x["sha"]) for x in t["tree"] if x["path"] not in ("README.md","ROADMAP.md","docs")}
    v.need(non_docs(a)==non_docs(b),"non-document root changed")
    # Serialize root identity tuples explicitly; no historical receipt changes.
    return {"historical_head":old.HEAD,"historical_tree":old.TREE,"current_head":gate.CURRENT,
            "current_tree":gate.CURRENT_TREE,"scope_digest":old.SCOPE,"historical_scope":h,"current_scope":c,
            "changed_paths":paths,"unchanged_non_document_roots":{k:list(x) for k,x in non_docs(b).items()}}

def admit(a):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R28 lineage")
    for jid,steps in ((140192957037,["Verify R28 portable exact recall and exact application","Actual Lean MCP R28 new application audit"]),
                      (140194736625,["Independently reconstruct R28 portable exact recall and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R28 job lineage")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R28 artifact")
    d=load(a.r28_local/"direct.json");mp=load(a.r28_local/"mcp.json");ind=load(a.r28_independent/"independent.json")
    v.need(d==load(a.r28_independent/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           d["status"]=="R28_DIRECT_PORTABLE_EXACT_RECALL" and mp["status"]=="R28_REAL_MCP_GREEN" and
           mp["direct_digest"]==DIRECT and ind["status"]=="R28_INDEPENDENT_PORTABLE_EXACT_RECALL_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["memory_key"]==d["memory_key"]==gate.R28_MEMORY and
           ind["inventory_key"]==d["inventory_key"]==r28.KEY and ind["transport_bytes_equal"] is True and
           ind["new_typed_applications"]==6 and ind["mcp_audits"]==11 and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R28 evidence")
    v.need([(x["name"],x["axioms"]) for x in d["fresh_application"]["observations"]]==
           [(x["name"],x["axioms"]) for x in mp["audits"]],"R28 audit binding")
    mem=load(a.r28_local/"portable-memory.json")
    v.need(mem["key"]==gate.R28_MEMORY and (a.r28_local/"portable-memory.json").read_bytes()==
           (a.r28_independent/"portable-memory.json").read_bytes(),"R28 memory bytes")
    return d,mp,ind,mem

def admit_capsule(a):
    # R24's existing exact-live-main gate stays untouched. This is a distinct
    # historical admission; observe_scope() separately proves the new scope.
    run=v.cache.api("actions/runs/"+str(r24.RUN))
    v.need(run["head_sha"]==r24.HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R23 lineage")
    for jid,steps in ((140162968764,["Verify R23 R2 proof capsule and exact application","Actual Lean MCP R23 R2 new application audit"]),
                      (140164550622,["Independently reconstruct R23 R2 proof capsule and application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==r24.RUN and j["head_sha"]==r24.HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R23 job lineage")
    for aid,n,dig in r24.ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==r24.RUN and x["workflow_run"]["head_sha"]==r24.HEAD,"R23 artifact")
    d=load(a.r23_local/"direct.json");mp=load(a.r23_local/"mcp.json");ind=load(a.r23_independent/"independent.json")
    v.need(d==load(a.r23_independent/"direct.json") and old.digest(d)==r24.DIRECT and old.digest(mp)==r24.MCP and
           d["status"]=="R23_R2_DIRECT_PROOF_CAPSULE" and mp["status"]=="R23_R2_REAL_MCP_GREEN" and mp["direct_digest"]==r24.DIRECT and
           ind["status"]=="R23_R2_INDEPENDENT_PROOF_CAPSULE_GREEN" and ind["direct_digest"]==r24.DIRECT and ind["mcp_digest"]==r24.MCP and
           ind["imported_capsule_from_sandbox"] is True and ind["consumer_shared_subtree_rebuilds"]==0 and
           ind["capsule_source_sha256"]==d["capsule_source_sha256"]==r24.SOURCE and
           d["source_head"]==old.HEAD and d["source_tree"]==old.TREE and d["scope_digest"]==old.SCOPE,"R23 historical evidence")
    return d

def parse(log,mark):
    rows=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(len(rows)==1,"expected one receipt "+mark)
    return rows[0]

def direct(a,out):
    scope=observe_scope()
    previous,mp,ind,mem=admit(a)
    r27,r27mp,r27ind=r28.admit(a)
    reg=r27["registry"]
    targets={k[6:]:t for k,t in previous["targets"].items() if k.startswith("fresh_")}
    trusted=gate.portable.memory(r27,r27mp,r27ind,targets)
    v.need(mem==trusted and len(mem["records"])==7,"R28 memory projection")
    bridge=gate.transport(scope,mem,reg)
    if a.phase=="independent":
        v.need(load(a.first/"transport.json")==bridge and
               (a.first/"portable-memory.json").read_bytes()==(a.r28_local/"portable-memory.json").read_bytes(),"R29 transported receipt bytes")
    v.save(out/"transport.json",bridge)
    # Preserve the exact historical artifact bytes, not a rewritten HEAD.
    (out/"portable-memory.json").write_bytes((a.r28_local/"portable-memory.json").read_bytes())
    wrong=copy.deepcopy(bridge);wrong["scope"]["current_tree"]="0"*40
    forged=gate.portable.seal(wrong)
    controls={"transport":gate.preflight(bridge,bridge,mem,trusted,reg,gate.CURRENT),
              "changed_bridge":gate.preflight(wrong,bridge,mem,trusted,reg,gate.CURRENT),
              "resealed_bridge":gate.preflight(forged,bridge,mem,trusted,reg,gate.CURRENT),
              "old_live_head":gate.preflight(bridge,bridge,mem,trusted,reg,old.HEAD)}
    v.need(controls=={"transport":"EXACT_OBSERVATION_REQUIRED","changed_bridge":"HOLD_TRANSPORT_INTEGRITY",
                     "resealed_bridge":"HOLD_UNADMITTED_TRANSPORT","old_live_head":"HOLD_CURRENT_HEAD"},"transport controls")
    capsule=admit_capsule(a)
    folder=a.r23_local/"capsule";manifest=load(a.r23_local/"capsule-manifest.json")
    v.need(manifest["source_sha256"]==r24.SOURCE and r23.manifest(folder)==manifest["files"] and
           r23.sha((folder/(r23.MODULE+".lean")).read_bytes())==r24.SOURCE,"historical capsule bytes")
    raw=r23.raw_read(folder,out,"RawR29Capsule")
    v.need(raw==capsule["raw"],"historical capsule full type/proof")
    r23.install(folder,manifest["files"])
    histobs={x["name"]:x for x in r27["fresh_application"]["observations"]}
    historical_types={c["name"]:histobs[c["name"]]["type_expr_repr"] for c in reg["candidates"]}
    r20,_=r28.r27.r21.admit_r20(a.r20_local,a.r20_independent)
    inv=load(a.r20_local/"inventory.json")
    v.need(old.digest(inv)==r20["inventory_digest"]==r27["root_inventory_digest"],"R20 historical index")
    v.need(set(gate.targets(mem))==set(targets),"memory target set")
    log=r23.run_lean([],out/"PortableProbe.lean",gate.probe(mem,reg))
    gate.check_live(log,mem,reg,historical_types)
    probes={x["case"]:x for x in parse(log,gate.multi.PROBE)}
    v.need(set(probes)==set(targets)|{"new_target"},"probe target inventory")
    memrows={x["case"]:x for x in mem["records"].values()}
    for k,x in probes.items():
        if k=="new_target":
            v.need(x["first"]["route"] is None and x["replay"]["route"] is None and
                   x["first"]["trace"][0]["status"]=="HOLD_NO_TYPED_MATCH_CONTINUE" and
                   x["replay"]["cache_hits"]==len(reg["candidates"]),"unseen target fallback")
            continue
        row=memrows[k];c=row["candidate"]
        expected=gate.MISS if c is None else gate.POS if c["polarity"]=="positive" else gate.NEG
        for mode in ("first","replay"):
            r=x[mode];hits=gate.trace_memory(r["trace"],mem)
            v.need(len(hits)==1 and hits[0]["status"]==expected and hits[0]["record_key"]==row["target_key"] and
                   r["route"]==([{"rule":c["name"],"arity":0}] if expected==gate.POS else None),"portable probe "+k)
    selected={x["name"]:x for pool in inv["selected"].values() for x in pool}
    registered={x["name"]:x for x in reg["candidates"]}
    expected={n:[] for n in registered};imports={x["module"] for x in registered.values()}
    parts=[];mcp_parts=[];apps={};roots={};root_hits={}
    def application(k,req,src,mcp_src,refs,expr):
        _,w=typed.names(req)
        expected[w]=refs
        apps[k]={"renderer_request":req,"witness":w,"expected_target_expr":expr,
                 "current_binding":old.digest({"current_head":gate.CURRENT,"current_tree":gate.CURRENT_TREE,
                     "transport_key":bridge["key"],"renderer_request":req})}
        parts.append(src.split("\n",1)[1]);mcp_parts.append(mcp_src.split("\n",1)[1])
        for n in refs:
            expected.setdefault(n,[])
            imports.add((registered[n] if n in registered else selected[n])["module"])
    for k,row in sorted(memrows.items()):
        c=row["candidate"]
        if c is None:continue
        req=typed.make_request("r29_"+k,c["module"],c["name"],row["target"],[],c["polarity"])
        application(k,req,typed.render(req),typed.declarations(req),[c["name"]],row["target_expr"])
    for k in ("local_refined_context","global_identity_context","wrong_source_context"):
        q=r20["requests"][k]
        log=r23.run_lean([],out/(k+".lean"),gate.render(q,inv,mem,reg))
        gate.check_live(log,mem,reg,historical_types)
        row=parse(log,gate.root.MARK);roots[k]=row
        v.need({t["rule"] for t in row["root_trials"]}=={x["name"] for x in inv["selected"][row["root_head"]]},"root inventory")
        route=row["chosen"]["route"]
        if k=="wrong_source_context":
            v.need(route is None and row["exact_target_negative_candidate"] is None,"wrong context must HOLD")
            continue
        v.need(route is not None and route[0]["arity"] in (2,3),"root not solved")
        branches=[x for x in row["branches"] if x["rule"]==route[0]["rule"] and x["first"]["route"]==route]
        v.need(len(branches)==1,"selected branch identity")
        root_hits[k]=gate.trace_memory(branches[0]["first"]["trace"],mem)
        req,src,mcp_src=gate.root.application(q,inv,route,"r29_"+k)
        imports.update(q["context_modules"])
        application(k,req,src,mcp_src,sorted({x["rule"] for x in route}),row["goal_expr"])
    v.need(any(t["status"]==gate.POS for ts in root_hits.values() for t in ts),"no persistent recall in selected recursive root")
    log=r23.run_lean([],out/"AlternativeRoutes.lean",gate.fixture(mem,reg))
    gate.check_live(log,mem,reg,historical_types)
    branch=parse(log,gate.multi.MARK)
    left,right,unknown=(branch[k] for k in ("left","right","unknown"))
    p=memrows["capsule_exact"]["candidate"]["name"];n=memrows["refined_negative"]["candidate"]["name"]
    blocked=gate.trace_memory(left["trace"],mem);alt=gate.trace_memory(right["trace"],mem);hold=gate.trace_memory(unknown["trace"],mem)
    v.need(left["route"] is None and right["route"]==[{"rule":"KuuOSR26Fixture.rightRule","arity":2},{"rule":p,"arity":0},{"rule":p,"arity":0}] and
           unknown["route"] is None and [t["status"] for t in blocked].count(gate.NEG)==1 and
           len(alt)==2 and all(t["status"]==gate.POS for t in alt) and len(hold)==1 and hold[0]["status"]==gate.MISS,
           "persistent branch separation")
    qs,base=gate.base_fixture(mem)
    fix=gate.multi.prev.fixture_application(qs,base)
    expected.update({"KuuOSR26Proof.alternative":[p,"KuuOSR26Fixture.rightRule"],
                     "KuuOSR26Fixture.rightRule":["Or.inr"],
                     "KuuOSR26Proof.blockedPair":["KuuOSR26Proof.negativeLeaf"],
                     "KuuOSR26Proof.negativeLeaf":[n],
                     "KuuOSR26Proof.exactLeaf":[p],"KuuOSR26Proof.defeqLeaf":[p]})
    imp="".join("import "+m+"\n" for m in sorted(imports));names=sorted(expected)
    log=r23.run_lean([],out/"R29Applications.lean",imp+"\n"+"\n".join(parts)+"\n"+fix+"\n"+v.suffix(names))
    audit=v.read_direct(log,[{"name":name,"expected_direct_refs":expected[name]} for name in names])
    by_n={x["name"]:x for x in audit}
    oldroots={x["name"]:x for x in r20["fresh_application"]["observations"]}
    for name,x in by_n.items():
        v.need(set(x["axioms"])<=typed.STANDARD,"unexpected axiom")
        historical=histobs.get(name,oldroots.get(name))
        if name in registered or name in selected:
            v.need(historical is not None and x["type_expr_repr"]==historical["type_expr_repr"] and
                   x["axioms"]==historical["axioms"],"imported source drift "+name)
        if name=="KuuOSR26Proof.alternative":v.need(n not in x["proof_constants"],"negative leaked into alternative")
    xs=[json.loads(l[len(typed.MARK):]) for l in log.splitlines() if l.startswith(typed.MARK)]
    by_w={x["witness_name"]:x for x in xs}
    v.need(len(by_w)==len(xs)==len(apps)==8,"fresh witness inventory")
    for k,x in apps.items():
        w=by_w[x["witness"]];z=by_n[x["witness"]]
        v.need(w["exact_kernel_type_match"] is True and w["target_expr_repr"]==x["expected_target_expr"] and
               w["witness_type_repr"]==z["type_expr_repr"],"exact witness "+k)
        x["application"]=w
    v.need(observe_scope()==scope,"canonical moved during proof replay")
    d={"status":"R29_DIRECT_PORTABLE_RECURSIVE_RECALL","source_head":gate.CURRENT,"source_tree":gate.CURRENT_TREE,
       "historical_source_head":old.HEAD,"scope_digest":old.SCOPE,"r28_direct_digest":DIRECT,"r28_mcp_digest":MCP,
       "transport_key":bridge["key"],"memory_key":mem["key"],"inventory_key":reg["key"],"controls":controls,
       "probe_results":probes,"root_results":roots,"root_memory_hits":root_hits,"branch_control":branch,"applications":apps,
       "fresh_application":{"observations":audit,"mcp_source":imp+"\n"+"\n".join(mcp_parts)+"\n"+fix},
       "capsule_rebuilds":0,"provider_calls":0,"semantic_search_complete":False,"proof_authority":False}
    v.save(out/"direct.json",d)
    print("KUUOS_R29_DIRECT",json.dumps({"direct_digest":old.digest(d),"transport_key":bridge["key"],"memory_key":mem["key"],
       "portable_records":len(mem["records"]),"fresh_applications":len(apps),"audits":len(audit),
       "root_memory_hits":{k:len(x) for k,x in root_hits.items()},"portable_comparison_searches":0,
       "novel_target_fallback":True,"blocked_route":left["route"],"alternative_route":right["route"],
       "controls":controls,"capsule_rebuilds":0},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS portable recursive recall","version":"1"}})
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
    result={"status":"R29_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R29_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R29_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    v.need((out/"transport.json").read_bytes()==(first/"transport.json").read_bytes() and
           (out/"portable-memory.json").read_bytes()==(first/"portable-memory.json").read_bytes(),"independent transport bytes")
    result={"status":"R29_INDEPENDENT_PORTABLE_RECURSIVE_RECALL_GREEN","source_head":d["source_head"],"source_tree":d["source_tree"],
            "historical_source_head":d["historical_source_head"],"scope_digest":d["scope_digest"],
            "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"transport_key":d["transport_key"],"memory_key":d["memory_key"],
            "transport_bytes_equal":True,"root_memory_hits":{k:len(x) for k,x in d["root_memory_hits"].items()},
            "new_typed_applications":len(d["applications"]),"mcp_audits":len(rows),"portable_comparison_searches":0,
            "routes":{"local_refined_context":"REUSE_EXISTING","global_identity_context":"REUSE_EXISTING",
                      "wrong_source_context":"HOLD","negative_premise_route":"BLOCKED_EXACT_PREMISE",
                      "alternative_route":"REUSE_EXISTING","historical_no_match":"HOLD_SEARCH_CONTINUES","new_target":"HOLD_SEARCH_REQUIRED"},
            "controls":d["controls"],"capsule_rebuilds":0,"provider_calls":0,"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False,"candidate_generation_allowed":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R29_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r28-local","r28-independent","r27-local","r27-independent","r20-local","r20-independent","r23-local","r23-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
