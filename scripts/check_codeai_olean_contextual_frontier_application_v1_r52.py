#!/usr/bin/env python3
"""R52: exact-premise selection, then kernel-checked typed applications."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_frontier_reference_v1_r51_r3 as r51
from runtime import kuuos_codeai_olean_contextual_frontier_application_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r50=r51.r50
r49=r51.r49
r48=r51.r48
r46=r51.r46
r45=r51.r45
r29=r51.r29
r23=r51.r23
r39=r51.r39
v=r51.v
ROOT=r51.ROOT
load=r51.load
FILES=r51.FILES+(r51.NEW,)
NEW="frontier-typed-application-v1.json"
RUN=45969326740
HEAD="5a62820aeb0018e8697380599348b76817516b26"
ARTS=((15184322323,"codeai-olean-r51-r3-local-45969326740-1","sha256:a3cc893b0640a1c6beaae182a31caec559a8b61b1ae50f84483221c115d921e4"),
      (15185365268,"codeai-olean-r51-r3-independent-45969326740-1","sha256:b7be612d77523bdbec762966596007a3274b5409b8c7a3533d7244b826bc2584"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R51 R3 run")
    for jid,steps in ((140405594601,["Verify R51 R3 contextual frontier reference","Actual Lean MCP R51 R3 exact reference audit"]),
                      (140407466044,["Independently verify R51 R3 contextual frontier reference"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R51 R3 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R51 R3 artifact")
    d=load(a.r51_local/"direct.json");mp=load(a.r51_local/"mcp.json");ind=load(a.r51_independent/"independent.json")
    v.need(d==load(a.r51_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R51 R3 evidence")
    for name in FILES:
        raw=(a.r51_local/name).read_bytes()
        v.need(raw==(a.r51_independent/name).read_bytes(),"R51 R3 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r51_local/"capsule";other=a.r51_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR52",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR52Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    memory=load(out/r48.NEW);graph=load(out/r49.NEW)
    frontier=load(out/r50.NEW)
    reference=load(out/r51.NEW)
    hist,candidates=gate.admit(prior,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference)
    joint=load(out/r45.NEW);a0=a.r51_local/"joint-capsule";b0=a.r51_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR52",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR52Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    source=prior["fresh_application"]["mcp_source"]+gate.goals()
    observe=gate.observer(candidates,hist)
    def run(label,src):
        p=out/(label+".lean")
        try:return r23.run_lean([],p,src)
        except ValueError:
            if p.with_suffix(".log").is_file():
                print("\n".join(x for x in p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
                    if len(x)<5000 and ("error:" in x or "error(" in x or "warning:" in x))[:16000],flush=True)
            raise
    log=run("ObservePremisesR52",source+observe)
    rows=[json.loads(x[len(gate.MARK):]) for x in log.splitlines() if x.startswith(gate.MARK)]
    v.need(len(rows)==len(gate.GOALS),"premise observation count")
    observations={x["goal"]:x for x in rows}
    decisions,chosen=gate.choose(candidates,hist,observations)
    controls=gate.controls(candidates,hist,observations)
    body,checks,refs=gate.consumer(candidates,chosen)
    expected={n:x["expected_direct_refs"] for n,x in hist.items()};expected.update(refs)
    log=run("ApplyR52",source+body+checks+v.suffix(sorted(expected)))
    v.need(gate.TARGET_MARK+"GREEN" in log,"typed application marker")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"parent audit drift")
    rr=[json.loads(x[len(gate.prev.MARK):]) for x in log.splitlines() if x.startswith(gate.prev.MARK)]
    records=gate.prev.check_references(candidates,frontier,{x["source"]:x for xs in rr for x in xs},by)
    v.need(len(rr)==4 and records==reference["records"],"R51 exact proof identity drift")
    for n,rs in refs.items():
        v.need(set(rs)<=set(by[n]["proof_constants"]) and
            set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"typed application dependency "+n)
    v.need(len(audit)==64 and r29.observe_scope()==scope,"audit scope")
    record=gate.base.portable.seal({"schema":"kuuos.codeai.frontier-typed-application.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_reference_key":reference["key"],"r51_direct_digest":gate.DIRECT,"r51_mcp_digest":gate.MCP,
        "observations":observations,"decisions":decisions,"chosen":chosen,"application_refs":refs,
        "witnesses":{n:by[n] for n in refs},"controls":controls,"semantic_search_complete":False,"proof_authority":False})
    v.save(out/NEW,record)
    d={"status":"R52_DIRECT_CONTEXTUAL_FRONTIER_APPLICATION","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r51_direct_digest":gate.DIRECT,"r51_mcp_digest":gate.MCP,
       "capsule_manifest":manifest,"joint_capsule_manifest":joint,"capsule_layer_key":mem["key"],
       "dispatch_layer_key":index["key"],"extension_key":extension["key"],"derived_layer_key":layer["key"],
       "transport_layer_key":memory["key"],"graph_key":graph["key"],"frontier_key":frontier["key"],
       "reference_key":reference["key"],"application_key":record["key"],"premise_trials":sum(len(x["trials"]) for x in rows),
       "premise_goal_count":len(rows),"selected_premises":len(chosen),"typed_witnesses":len(refs),
       "positive_witnesses":1,"negative_witnesses":2,"polymorphic_rule_specialized":True,
       "raw_positive_hold":True,"historical_hold_retained":True,"raw_negative_retained":True,
       "controls":controls,"capsule_rebuilds":0,"provider_calls":0,"root_search_complete":False,
       "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":source+body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R52_DIRECT",json.dumps({k:d[k] for k in ("application_key","premise_trials","premise_goal_count",
        "selected_premises","typed_witnesses","positive_witnesses","negative_witnesses","polymorphic_rule_specialized",
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
                                     "clientInfo":{"name":"KuuOS contextual frontier application","version":"1"}})
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
    result={"status":"R52_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R52_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R52_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R52_INDEPENDENT_CONTEXTUAL_FRONTIER_APPLICATION_GREEN","source_head":d["source_head"],
        "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        **{k:d[k] for k in ("capsule_layer_key","dispatch_layer_key","extension_key","derived_layer_key","transport_layer_key",
        "graph_key","frontier_key","reference_key","application_key","premise_trials","premise_goal_count","selected_premises",
        "typed_witnesses","positive_witnesses","negative_witnesses","polymorphic_rule_specialized","raw_positive_hold",
        "historical_hold_retained","raw_negative_retained","controls","capsule_rebuilds","provider_calls","root_search_complete",
        "all_repository_dependencies_observed","semantic_search_complete","proof_authority")},
        "parent_bytes_preserved":True,"application_bytes_equal":True,"raw_type_and_proof_equal":True,
        "mcp_audits":len(rows),"unobserved_module_count":695}
    v.save(out/"independent.json",result)
    print("KUUOS_R52_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r51-local","r51-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
