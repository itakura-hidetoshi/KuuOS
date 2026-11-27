#!/usr/bin/env python3
"""R53: select root rules from typed candidates, retain all checked routes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_frontier_application_v1_r52 as r52
from runtime import kuuos_codeai_olean_contextual_rule_selection_v1_r2 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r51=r52.r51
r50=r52.r50
r49=r52.r49
r48=r52.r48
r46=r52.r46
r45=r52.r45
r29=r52.r29
r23=r52.r23
r39=r52.r39
v=r52.v
ROOT=r52.ROOT
load=r52.load
FILES=r52.FILES+(r52.NEW,)
NEW="contextual-rule-selection-v1.json"
RUN=45970860992
HEAD="b1d69f65a9417ea2665de19fda2c60e38bd14663"
ARTS=((15185731364,"codeai-olean-r52-local-45970860992-1","sha256:5c430415fe1f71c430cdb21eefb88498be0e266039b5117d007f037e557610ac"),
      (15185767051,"codeai-olean-r52-independent-45970860992-1","sha256:0c8b1a181df88dc9c72335575508bc20b104d0ade1dbcf5dc0c1e5547cbd4c62"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R52 run")
    for jid,steps in ((140410668757,["Verify R52 contextual frontier application","Actual Lean MCP R52 typed application audit"]),
                      (140412677351,["Independently verify R52 contextual frontier application"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R52 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R52 artifact")
    d=load(a.r52_local/"direct.json");mp=load(a.r52_local/"mcp.json");ind=load(a.r52_independent/"independent.json")
    v.need(d==load(a.r52_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R52 evidence")
    for name in FILES:
        raw=(a.r52_local/name).read_bytes()
        v.need(raw==(a.r52_independent/name).read_bytes(),"R52 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r52_local/"capsule";other=a.r52_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR53",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR53Independent",names) and
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
    hist,candidates=gate.admit(prior,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference,application)
    joint=load(out/r45.NEW);a0=a.r52_local/"joint-capsule";b0=a.r52_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR53",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR53Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    observer=gate.observer(candidates,hist)
    v.need(observer.count('IO.println ("'+gate.MARK+'" ++')==len(gate.GOALS),"generated observation marker drift")
    source=prior["fresh_application"]["mcp_source"]+"\n"+observer
    def run(label,src):
        p=out/(label+".lean")
        try:return r23.run_lean([],p,src)
        except ValueError:
            if p.with_suffix(".log").is_file():
                print("\n".join(x for x in p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
                    if len(x)<5000 and ("error:" in x or "error(" in x or "warning:" in x))[:16000],flush=True)
            raise
    def observe(log):
        rows=[json.loads(x[len(gate.MARK):]) for x in log.splitlines() if x.startswith(gate.MARK)]
        v.need(len(rows)==len(gate.GOALS),"rule observation count")
        return {x["goal"]:x for x in rows}
    observations=observe(run("SelectR53",source))
    refs,routes,decisions=gate.project(candidates,hist,application,observations)
    controls=gate.controls(candidates,hist,application,observations)
    expected={n:x["expected_direct_refs"] for n,x in hist.items()};expected.update(refs)
    log=run("AuditR53",source+v.suffix(sorted(expected)))
    v.need(observe(log)==observations,"rule replay drift")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"parent audit drift")
    rr=[json.loads(x[len(gate.prev.prev.MARK):]) for x in log.splitlines() if x.startswith(gate.prev.prev.MARK)]
    records=gate.prev.prev.check_references(candidates,frontier,{x["source"]:x for xs in rr for x in xs},by)
    v.need(len(rr)==4 and records==reference["records"],"R51 exact proof identity drift")
    for n,x in routes.items():
        v.need(by[n]["type_expr_repr"]==observations[x["goal"]]["goal_expr"] and
               not by[n]["universe_parameters"] and set(refs[n])<=set(by[n]["proof_constants"]) and
               by[n]["axioms"]==sorted(set(x["axioms"])),"selected exact proof "+n)
    v.need(len(audit)==64+len(refs) and r29.observe_scope()==scope,"audit scope")
    record=gate.base.portable.seal({"schema":"kuuos.codeai.contextual-rule-selection.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_application_key":application["key"],"r52_direct_digest":gate.DIRECT,"r52_mcp_digest":gate.MCP,
        "observations":observations,"routes":routes,"decisions":decisions,"application_refs":refs,
        "witnesses":{n:by[n] for n in refs},"controls":controls,"semantic_search_complete":False,"proof_authority":False})
    v.save(out/NEW,record)
    pool,facts=gate.pool(candidates,hist)
    d={"status":"R53_DIRECT_CONTEXTUAL_RULE_SELECTION","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r52_direct_digest":gate.DIRECT,"r52_mcp_digest":gate.MCP,
       "capsule_manifest":manifest,"joint_capsule_manifest":joint,"capsule_layer_key":mem["key"],
       "dispatch_layer_key":index["key"],"extension_key":extension["key"],"derived_layer_key":layer["key"],
       "transport_layer_key":memory["key"],"graph_key":graph["key"],"frontier_key":frontier["key"],
       "reference_key":reference["key"],"application_key":application["key"],"selection_key":record["key"],
       "rule_candidates":len(pool),"fact_candidates":len(facts),"goal_count":len(observations),
       "rule_trials":sum(len(x["trials"]) for x in observations.values()),
       "premise_probes":sum(t["probes"] for x in observations.values() for t in x["trials"]),
       "checked_routes":len(refs),"positive_routes":sum(x["goal"]!="rawNoGlobal" for x in routes.values()),
       "negative_routes":sum(x["goal"]=="rawNoGlobal" for x in routes.values()),
       "selected_rules":sorted({x["rule"] for x in routes.values()}),
       "route_counts":{k:len(x["witnesses"]) for k,x in decisions.items()},
       "raw_positive_hold":True,"historical_hold_retained":True,"raw_negative_retained":True,
       "controls":controls,"capsule_rebuilds":0,"provider_calls":0,"root_search_complete":False,
       "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",d)
    print("KUUOS_R53_DIRECT",json.dumps({k:d[k] for k in ("selection_key","rule_candidates","fact_candidates","goal_count",
        "rule_trials","premise_probes","checked_routes","positive_routes","negative_routes","selected_rules","route_counts",
        "raw_positive_hold","controls","capsule_rebuilds")}|{"direct_digest":old.digest(d),"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual rule selection","version":"1"}})
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
    result={"status":"R53_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R53_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R53_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R53_INDEPENDENT_CONTEXTUAL_RULE_SELECTION_GREEN","source_head":d["source_head"],
        "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        **{k:d[k] for k in ("capsule_layer_key","dispatch_layer_key","extension_key","derived_layer_key","transport_layer_key",
        "graph_key","frontier_key","reference_key","application_key","selection_key","rule_candidates","fact_candidates","goal_count",
        "rule_trials","premise_probes","checked_routes","positive_routes","negative_routes","selected_rules","route_counts",
        "raw_positive_hold","historical_hold_retained","raw_negative_retained","controls","capsule_rebuilds","provider_calls",
        "root_search_complete","all_repository_dependencies_observed","semantic_search_complete","proof_authority")},
        "parent_bytes_preserved":True,"selection_bytes_equal":True,"raw_type_and_proof_equal":True,
        "mcp_audits":len(rows),"unobserved_module_count":695}
    v.save(out/"independent.json",result)
    print("KUUOS_R53_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r52-local","r52-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
