#!/usr/bin/env python3
"""R49: verify the R48 observed dependency DAG and reject cyclic candidates."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_transport_memory_v1_r48 as r48
from runtime import kuuos_codeai_olean_contextual_dependency_audit_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r46=r48.r46
r45=r48.r45
r29=r48.r29
r23=r48.r23
r39=r48.r39
v=r48.v
ROOT=r48.ROOT
load=r48.load
FILES=r48.FILES+(r48.NEW,)
NEW="observed-dependency-dag-v1.json"
RUN=45961694025
HEAD="d6065e49a3401ada80f5d3ff8e8125cd697345ea"
ARTS=((15180364688,"codeai-olean-r48-local-45961694025-1","sha256:46bc7ad06f0265bc31eae6d260084be22dd68456b22c4b4d8cfaa8690708f2dc"),
      (15180909635,"codeai-olean-r48-independent-45961694025-1","sha256:70d1946218a3122271f078e3b07f16cbc029e6928a3e17465cd05e297db4e9f1"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R48 run")
    for jid,steps in ((140380760463,["Verify R48 contextual transport memory","Actual Lean MCP R48 transport audit"]),
                      (140382232838,["Independently verify R48 contextual transport memory"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R48 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R48 artifact")
    d=load(a.r48_local/"direct.json");mp=load(a.r48_local/"mcp.json");ind=load(a.r48_independent/"independent.json")
    v.need(d==load(a.r48_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R48 evidence")
    for name in FILES:
        raw=(a.r48_local/name).read_bytes()
        v.need(raw==(a.r48_independent/name).read_bytes(),"R48 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r48_local/"capsule";other=a.r48_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR49",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR49Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    dispatch=gate.dispatch
    global_qs=dispatch.requests(mem)
    alt=global_qs["alternate"]
    t=copy.deepcopy(alt["target"]);t["apply"][0]={"const":gate.base.LEC+"Compatible"}
    global_qs["unknown"]=gate.base.root.make_request("r43_unknown",t,alt["context_args"],alt["context_modules"])
    global_obs=r29.parse(r23.run_lean([],out/"ObserveR49.lean",dispatch.observe(global_qs)),"KUUOS_R41_CONTEXT ")
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    qs=gate.derived.prev.requests(global_qs)
    def observe(label,q):
        controls={n:global_qs[n] for n in ("shadow","raw","alternate")}
        batch={**controls,label:q}
        row=r29.parse(r23.run_lean([],out/("ObserveR49_"+label+".lean"),dispatch.observe(batch)),"KUUOS_R41_CONTEXT ")
        v.need(set(row)==set(batch) and all(row[n]==global_obs[n] for n in controls),"canonical control drift")
        return row[label]
    obs={k:observe("compat_"+k,q) for k,q in sorted(qs.items())}
    memory=load(out/r48.NEW)
    hist=gate.admit(prior,mp,ind,index,extension,layer,memory,mem)
    decisions={k:gate.derived.recall(index,extension,layer,layer,q,obs[k],gate.base.CURRENT) for k,q in sorted(qs.items())}
    joint=load(out/r45.NEW);a0=a.r48_local/"joint-capsule";b0=a.r48_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR49",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR49Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    targets=gate.transport.requests(qs["shadow"])
    observations={k:observe("transport_"+k,q) for k,q in sorted(targets.items())}
    requests=prior["requests"]
    v.need(observations==prior["observations"] and
           all(all(requests[k][f]==q[f] for f in ("target","context_args","context_modules","mode")) for k,q in targets.items()),
           "R48 live goal binding")
    def recall(q,o):return gate.prev.recall(index,extension,layer,memory,memory,q,o,gate.base.CURRENT)
    result={k:recall(q,observations[k]) for k,q in sorted(requests.items())}
    earlier={k:recall(q,global_obs[k]) for k,q in sorted(global_qs.items())}
    v.need(result==prior["decisions"] and earlier==prior["earlier_decisions"] and
           decisions["raw"]["polarity"]=="negative" and earlier["raw"]["polarity"]=="negative","R48 decision drift")
    # Audit the admitted candidate graph before regenerating any application.
    recipes=gate.recipe_refs(memory,layer,decisions,result)
    body0,check0,refs0=gate.derived.consumer(qs,decisions)
    body,check,refs=gate.prev.consumer(memory,requests,observations,result)
    expected_recipes={**refs0,**refs}
    v.need(refs==prior["transport_refs"] and body0+body==prior["fresh_application"]["mcp_source"],"R48 exact source drift")
    historical_graph=gate.audit_graph(hist,recipes,expected_recipes)
    controls=gate.controls(hist,recipes,historical_graph["observed_edges"])
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    log=r23.run_lean([],out/"ApplyR49.lean",body0+body+check0+check+v.suffix(sorted(expected)))
    v.need(r29.parse(log,gate.derived.MARK)=={k:o["goal_expr"] for k,o in obs.items()} and
           r29.parse(log,gate.prev.MARK)=={k:o["goal_expr"] for k,o in observations.items()},"exact goal drift")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need(by==hist,"R48 full kernel audit drift")
    live=gate.audit_graph(by,recipes,expected_recipes)
    v.need(live==historical_graph and gate.controls(by,recipes,live["observed_edges"])==controls and
           len(audit)==41 and r29.observe_scope()==scope,"graph evidence drift")
    graph=gate.base.portable.seal({**live,"source_head":gate.base.CURRENT,
        "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"parent_transport_key":memory["key"],
        "r48_direct_digest":gate.DIRECT,"r48_mcp_digest":gate.MCP,"controls":controls,
        "semantic_search_complete":False})
    v.save(out/NEW,graph)
    d={"status":"R49_DIRECT_CONTEXTUAL_DEPENDENCY_AUDIT","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r48_direct_digest":gate.DIRECT,
       "r48_mcp_digest":gate.MCP,"capsule_manifest":manifest,"joint_capsule_manifest":joint,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"extension_key":extension["key"],
       "derived_layer_key":layer["key"],"transport_layer_key":memory["key"],"graph_key":graph["key"],
       "node_count":graph["node_count"],"observed_edge_count":graph["observed_edge_count"],
       "recipe_edge_count":graph["recipe_edge_count"],"frontier_constant_count":graph["frontier_constant_count"],
       "shared_node_count":len(graph["shared_nodes"]),"selected_root_count":len(graph["selected_roots"]),
       "controls":controls,"acyclic_observed_graph":True,"historical_hold_retained":True,"raw_negative_retained":True,
       "root_trials":0,"capsule_rebuilds":0,"provider_calls":0,"exact_kernel_type":True,
       "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body0+body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R49_DIRECT",json.dumps({k:d[k] for k in ("graph_key","node_count","observed_edge_count",
        "recipe_edge_count","frontier_constant_count","shared_node_count","selected_root_count","controls",
        "acyclic_observed_graph","root_trials","capsule_rebuilds")}|{"direct_digest":old.digest(d),"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual dependency audit","version":"1"}})
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
    result={"status":"R49_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R49_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R49_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R49_INDEPENDENT_CONTEXTUAL_DEPENDENCY_AUDIT_GREEN","source_head":d["source_head"],
        "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        **{k:d[k] for k in ("capsule_layer_key","dispatch_layer_key","extension_key","derived_layer_key","transport_layer_key",
        "graph_key","node_count","observed_edge_count","recipe_edge_count","frontier_constant_count","shared_node_count",
        "selected_root_count","controls","acyclic_observed_graph","historical_hold_retained","raw_negative_retained",
        "root_trials","capsule_rebuilds","provider_calls","exact_kernel_type","all_repository_dependencies_observed",
        "semantic_search_complete","proof_authority")},
        "parent_bytes_preserved":True,"graph_bytes_equal":True,"raw_type_and_proof_equal":True,
        "mcp_audits":len(rows),"unobserved_module_count":695}
    v.save(out/"independent.json",result)
    print("KUUOS_R49_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r48-local","r48-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
