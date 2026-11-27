#!/usr/bin/env python3
"""R57: observe bounded Lean dependency availability and verify policy-filtered dispatch."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_budget_selection_v1_r56 as r56
r55=r56.r55
r54=r55.r54
from runtime import kuuos_codeai_olean_contextual_dependency_availability_v1 as gate
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r53=r54.r53
r52=r54.r52
r51=r54.r51
r50=r54.r50
r49=r54.r49
r48=r54.r48
r46=r54.r46
r45=r54.r45
r29=r54.r29
r23=r54.r23
r39=r54.r39
v=r54.v
ROOT=r54.ROOT
load=r54.load
FILES=r56.FILES+(r56.NEW,)
NEW="contextual-dependency-availability-v1.json"
RUN=45978687579
HEAD="0859ae59428c8c1ae65e269c4391938fbc0f42c7"
ARTS=((15188975837,"codeai-olean-r56-local-45978687579-1","sha256:e5bb33754469210d20c4ba250e17abd41ea0f868790d28909202f40839ded932"),
      (15188249545,"codeai-olean-r56-independent-45978687579-1","sha256:ab3a8de4d8f8c5c6cae32a1b7be6211f600d7c8f41f1fc87fe9e3c0650245b19"))

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R56 run")
    for jid,steps in ((140436788157,["Verify R56 contextual budget selection","Actual Lean MCP R56 typed budget audit"]),
                      (140439936680,["Independently verify R56 contextual budget selection"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R56 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R56 artifact")
    d=load(a.r56_local/"direct.json");mp=load(a.r56_local/"mcp.json");ind=load(a.r56_independent/"independent.json")
    v.need(d==load(a.r56_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R56 evidence")
    for name in FILES:
        raw=(a.r56_local/name).read_bytes()
        v.need(raw==(a.r56_independent/name).read_bytes(),"R56 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.comparison_gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r56_local/"capsule";other=a.r56_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.comparison_gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR57",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR57Independent",names) and
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
    comparison=load(out/r54.NEW)
    pref=load(out/r55.NEW)
    budget=load(out/r56.NEW)
    hist=gate.admit(prior,mp,ind,comparison,selection,pref,budget)
    joint=load(out/r45.NEW);a0=a.r56_local/"joint-capsule";b0=a.r56_independent/"joint-capsule"
    v.need(joint==gate.comparison_gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.comparison_gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR57",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR57Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)

    # Preserve original receipts separately; the new receipts cannot overwrite them.
    receipts=out/"parent-r56-receipts";receipts.mkdir()
    for name,src in (("direct.json",a.r56_local),("mcp.json",a.r56_local),("independent.json",a.r56_independent)):
        (receipts/name).write_bytes((src/name).read_bytes())
    for folder in ("parent-r54-receipts","parent-r55-receipts"):
        ancestor=out/folder;ancestor.mkdir()
        for name in ("direct.json","mcp.json","independent.json"):
            raw=(a.r56_local/folder/name).read_bytes()
            v.need(raw==(a.r56_independent/folder/name).read_bytes(),"ancestor receipt byte drift")
            (ancestor/name).write_bytes(raw)
    a54=out/"parent-r54-receipts";a55=out/"parent-r55-receipts"
    parent_hist=gate.prev.prev.require_parent(load(a54/"direct.json"),load(a54/"mcp.json"),
        load(a54/"independent.json"),comparison,selection)
    r55_hist=gate.prev.admit(load(a55/"direct.json"),load(a55/"mcp.json"),
        load(a55/"independent.json"),comparison,selection,pref)
    v.need(all(hist[n]==x for n,x in r55_hist.items()) and all(hist[n]==x for n,x in parent_hist.items()),"ancestor identity")
    # First observe actual kernel availability. No root rule discovery is needed.
    prefix=prior["fresh_application"]["mcp_source"]+"\n"+gate.observer(comparison)
    q=out/"AvailabilityProbeR57.lean"
    try:probe=r23.run_lean([],q,prefix)
    except ValueError:
        if q.with_suffix(".log").is_file():
            print("\n".join(x for x in q.with_suffix(".log").read_text(encoding="utf-8").splitlines()
                if len(x)<5000 and ("error:" in x or "error(" in x or "warning:" in x))[:16000],flush=True)
        raise
    env_rows=[json.loads(x[len(gate.MARK):]) for x in probe.splitlines() if x.startswith(gate.MARK)]
    env_obs={x["route"]:x for x in env_rows}
    v.need(len(env_rows)==5 and len(env_obs)==5,"environment observation inventory")
    availability=gate.project(comparison,parent_hist,frontier,env_obs)
    decisions,selected=gate.plan(budget,pref,comparison,selection,availability)
    controls=gate.controls(budget,pref,comparison,selection,availability,parent_hist,frontier,env_obs)
    source=gate.render(prefix,selected)
    v.need(all(('name := '+chr(96)*2+n) not in source for n in selected),"fresh names must be constructed")
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({n:[x["route"]] for n,x in selected.items()})
    p=out/"AvailabilityR57.lean"
    try:log=r23.run_lean([],p,source+v.suffix(sorted(expected)))
    except ValueError:
        if p.with_suffix(".log").is_file():
            print("\n".join(x for x in p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
                if len(x)<5000 and ("error:" in x or "error(" in x or "warning:" in x))[:16000],flush=True)
        raise
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R56 complete audit drift")
    rows=[json.loads(x[len(gate.comparison_gate.MARK):]) for x in log.splitlines() if x.startswith(gate.comparison_gate.MARK)]
    observations={x["name"]:x for x in rows}
    v.need(len(rows)==5 and observations==comparison["replay_observations"],"R54 exact replay proof drift")
    replay_env=[json.loads(x[len(gate.MARK):]) for x in log.splitlines() if x.startswith(gate.MARK)]
    v.need(len(replay_env)==5 and {x["route"]:x for x in replay_env}==env_obs,"environment replay drift")
    projected=gate.comparison_gate.project(selection,parent_hist,frontier,observations)
    v.need(all(comparison[k]==x for k,x in projected.items()),"R54 preference projection drift")
    for n,x in selected.items():
        row=by[n];parent=hist[x["route"]]
        v.need(row["type_expr_repr"]==x["goal_expr"]==parent["type_expr_repr"] and
               row["proof_constants"]==[x["route"]] and row["axioms"]==parent["axioms"] and
               row["universe_parameters"]==[],"R57 exact typed dispatch")
    record=gate.base.portable.seal({"schema":"kuuos.codeai.contextual-dependency-availability.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_budget_key":budget["key"],"parent_preference_key":pref["key"],"r56_direct_digest":gate.DIRECT,"r56_mcp_digest":gate.MCP,
        "environment_observations":env_obs,"availability":availability,"decisions":decisions,
        "retained_records":pref["retained_records"],"retained_groups":pref["retained_groups"],
        "dispatches":{n:{**x,"observation":by[n]} for n,x in selected.items()},"controls":controls,
        "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "boundary_body_audited":False,"policy_is_refutation":False,"proof_authority":False,"action_authority":False,
        "semantic_search_complete":False})
    v.save(out/NEW,record)
    v.need(len(audit)==89 and r29.observe_scope()==scope,"audit scope")
    d={"status":"R57_DIRECT_CONTEXTUAL_DEPENDENCY_AVAILABILITY","source_head":gate.base.CURRENT,
        "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"parent_budget_key":budget["key"],
        "r56_direct_digest":gate.DIRECT,"r56_mcp_digest":gate.MCP,"availability_key":record["key"],
        "capsule_manifest":manifest,"joint_capsule_manifest":joint,"request_count":len(decisions),
        "typed_dispatches":len(selected),"fallbacks":sum(x["fallback"] for x in decisions.values()),
        "policy_holds":sum(x["status"]=="HOLD_ENV_OR_POLICY" for x in decisions.values()),
        "budget_holds":sum(x["status"]=="HOLD_ROUTE_BUDGET" for x in decisions.values()),
        "search_holds":sum(x["status"]=="HOLD_NO_RULE_ROUTE" for x in decisions.values()),
        "retained_routes":len(pref["retained_records"]),
        "environment_counts":{n:{k:len(x[k]) for k in ("known","boundary","present","missing","expanded")} for n,x in availability.items()},
        "distinct_present_names":len({n for x in availability.values() for n in x["present"]}),
        "decisions":{n:{k:x[k] for k in ("status","preferred","parent_preferred","eligible","missing_environment","policy_excluded","fallback","parent_polarity")} for n,x in decisions.items()},
        "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "new_root_discovery_trials":0,"parent_replayed_routes":len(rows),"parent_replay_premise_probes":sum(x["probes"] for x in rows),
        "capsule_rebuilds":0,"controls":controls,"boundary_body_audited":False,"policy_is_refutation":False,
        "proof_authority":False,"action_authority":False,"semantic_search_complete":False,
        "all_repository_dependencies_observed":False,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",d)
    print("KUUOS_R57_DIRECT",json.dumps({k:x for k,x in d.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
          {"direct_digest":old.digest(d),"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual dependency availability","version":"1"}})
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
    result={"status":"R57_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R57_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R57_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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

    for folder in ("parent-r54-receipts","parent-r55-receipts","parent-r56-receipts"):
        for name in ("direct.json","mcp.json","independent.json"):
            v.need((out/folder/name).read_bytes()==(first/folder/name).read_bytes(),"ancestor receipt byte drift")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R57_INDEPENDENT_CONTEXTUAL_DEPENDENCY_AVAILABILITY_GREEN","direct_digest":old.digest(d),
                   "mcp_digest":old.digest(mp),"mcp_audits":len(rows),"availability_bytes_equal":True,
                   "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R57_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r56-local","r56-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
