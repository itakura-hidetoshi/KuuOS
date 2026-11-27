#!/usr/bin/env python3
"""R54: replay only the five certified routes, compare without pruning."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_rule_selection_v1_r53_r2 as r53
from runtime import kuuos_codeai_olean_contextual_route_comparison_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r52=r53.r52
r51=r53.r51
r50=r53.r50
r49=r53.r49
r48=r53.r48
r46=r53.r46
r45=r53.r45
r29=r53.r29
r23=r53.r23
r39=r53.r39
v=r53.v
ROOT=r53.ROOT
load=r53.load
FILES=r53.FILES+(r53.NEW,)
NEW="contextual-route-comparison-v1.json"
RUN=45972570933
HEAD="bd72c08f137736ad08d6be406fca7e5123299a68"
ARTS=((15185554017,"codeai-olean-r53-r2-local-45972570933-1","sha256:8f5078d4213d323b761eb51342fc4a5b59519e673d8ea8f3ea68f1f866eb917f"),
      (15185329357,"codeai-olean-r53-r2-independent-45972570933-1","sha256:287c4ab41683376d3ea4347aefaaa096ad73244e5b7bcc0cf0b466ea546033f8"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R53 R2 run")
    for jid,steps in ((140416318486,["Verify R53 R2 contextual rule selection","Actual Lean MCP R53 R2 selected rule audit"]),
                      (140419146992,["Independently verify R53 R2 contextual rule selection"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R53 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R53 R2 artifact")
    d=load(a.r53_local/"direct.json");mp=load(a.r53_local/"mcp.json");ind=load(a.r53_independent/"independent.json")
    v.need(d==load(a.r53_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R53 R2 evidence")
    for name in FILES:
        raw=(a.r53_local/name).read_bytes()
        v.need(raw==(a.r53_independent/name).read_bytes(),"R53 R2 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r53_local/"capsule";other=a.r53_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR54",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR54Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    memory=load(out/r48.NEW);graph=load(out/r49.NEW)
    frontier=load(out/r50.NEW)
    reference=load(out/r51.NEW)
    application=load(out/r52.NEW)
    selection=load(out/r53.NEW)
    hist,candidates,earlier=gate.admit(prior,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference,application,selection)
    joint=load(out/r45.NEW);a0=a.r53_local/"joint-capsule";b0=a.r53_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR54",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR54Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    source=gate.replay(prior["fresh_application"]["mcp_source"],candidates,earlier,selection)
    v.need(source.count('IO.println ("'+gate.MARK+'" ++')==5 and gate.prev.MARK not in source,
           "replay generation boundary")
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    p=out/"ReplayR54.lean"
    try:log=r23.run_lean([],p,source+v.suffix(sorted(expected)))
    except ValueError:
        if p.with_suffix(".log").is_file():
            print("\n".join(x for x in p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
                if len(x)<5000 and ("error:" in x or "error(" in x or "warning:" in x))[:16000],flush=True)
        raise
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need(by==hist,"R53 complete audit drift")
    rr=[json.loads(x[len(gate.prev.prev.prev.MARK):]) for x in log.splitlines() if x.startswith(gate.prev.prev.prev.MARK)]
    records=gate.prev.prev.prev.check_references(candidates,frontier,{x["source"]:x for xs in rr for x in xs},by)
    v.need(len(rr)==4 and records==reference["records"],"R51 exact proof identity drift")
    rows=[json.loads(x[len(gate.MARK):]) for x in log.splitlines() if x.startswith(gate.MARK)]
    v.need(len(rows)==5 and len({x["name"] for x in rows})==5,"replay inventory")
    observations={x["name"]:x for x in rows}
    comparison=gate.project(selection,by,frontier,observations)
    controls=gate.controls(selection,by,frontier,observations)
    record=gate.base.portable.seal({**comparison,"schema":"kuuos.codeai.contextual-route-comparison.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_selection_key":selection["key"],"r53_direct_digest":gate.DIRECT,"r53_mcp_digest":gate.MCP,
        "replay_observations":observations,"controls":controls})
    v.save(out/NEW,record)
    v.need(len(audit)==69 and r29.observe_scope()==scope,"audit scope")
    metrics={n:{k:x[k] for k in ("goal","rule","mode","proof_nodes","historical_probes","observed_dependency_count","boundary_count")}
             for n,x in comparison["records"].items()}
    prefs={g:{p:x["preferred"] for p,x in group["preferences"].items()} for g,group in comparison["groups"].items()}
    common={g:len(group.get("common_observed_dependencies",[])) for g,group in comparison["groups"].items()}
    d={"status":"R54_DIRECT_CONTEXTUAL_ROUTE_COMPARISON","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r53_direct_digest":gate.DIRECT,"r53_mcp_digest":gate.MCP,
       "capsule_manifest":manifest,"joint_capsule_manifest":joint,"capsule_layer_key":mem["key"],
       "dispatch_layer_key":index["key"],"extension_key":extension["key"],"derived_layer_key":layer["key"],
       "transport_layer_key":memory["key"],"graph_key":graph["key"],"frontier_key":frontier["key"],
       "reference_key":reference["key"],"application_key":application["key"],"selection_key":selection["key"],
       "comparison_key":record["key"],"replayed_routes":len(rows),"new_root_discovery_trials":0,
       "historical_root_trials":prior["rule_trials"],"historical_premise_probes":prior["premise_probes"],
       "replay_premise_probes":sum(x["probes"] for x in rows),"route_counts":gate.COUNTS,
       "route_metrics":metrics,"preferences":prefs,"shared_observed_dependency_counts":common,
       "metrics":"structural_proxy_not_wall_clock","all_routes_retained":True,"mathematical_independence_claimed":False,
       "raw_positive_hold":True,"historical_hold_retained":True,"raw_negative_retained":True,
       "controls":controls,"capsule_rebuilds":0,"provider_calls":0,"root_search_complete":False,
       "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",d)
    print("KUUOS_R54_DIRECT",json.dumps({k:d[k] for k in ("comparison_key","replayed_routes","new_root_discovery_trials",
        "historical_root_trials","historical_premise_probes","replay_premise_probes","route_counts","route_metrics",
        "preferences","shared_observed_dependency_counts","controls","capsule_rebuilds","all_routes_retained")}|{
        "direct_digest":old.digest(d),"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual route comparison","version":"1"}})
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
    result={"status":"R54_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R54_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R54_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+(NEW,):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    v.need(r45.capsule_files(out/"joint-capsule")==r45.capsule_files(first/"joint-capsule")==d["joint_capsule_manifest"]["files"],
           "joint capsule bytes")
    result={"status":"R54_INDEPENDENT_CONTEXTUAL_ROUTE_COMPARISON_GREEN","source_head":d["source_head"],
        "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        **{k:d[k] for k in ("capsule_layer_key","dispatch_layer_key","extension_key","derived_layer_key","transport_layer_key",
        "graph_key","frontier_key","reference_key","application_key","selection_key","comparison_key","replayed_routes",
        "new_root_discovery_trials","historical_root_trials","historical_premise_probes","replay_premise_probes","route_counts",
        "route_metrics","preferences","shared_observed_dependency_counts","metrics","all_routes_retained",
        "mathematical_independence_claimed","raw_positive_hold","historical_hold_retained","raw_negative_retained","controls",
        "capsule_rebuilds","provider_calls","root_search_complete","all_repository_dependencies_observed",
        "semantic_search_complete","proof_authority")},
        "parent_bytes_preserved":True,"comparison_bytes_equal":True,"raw_type_and_proof_equal":True,
        "mcp_audits":len(rows),"unobserved_module_count":695}
    v.save(out/"independent.json",result)
    print("KUUOS_R54_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r53-local","r53-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
