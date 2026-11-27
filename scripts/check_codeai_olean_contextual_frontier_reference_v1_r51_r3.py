#!/usr/bin/env python3
"""R51: exact universe-preserving reference witnesses for R50 theorems."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_frontier_v1_r50 as r50
from runtime import kuuos_codeai_olean_contextual_frontier_reference_v1_r3 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r49=r50.r49
r48=r50.r48
r46=r50.r46
r45=r50.r45
r29=r50.r29
r23=r50.r23
r39=r50.r39
v=r50.v
ROOT=r50.ROOT
load=r50.load
FILES=r50.FILES+(r50.NEW,)
NEW="frontier-exact-reference-v1.json"
RUN=45964595427
HEAD="a1bcd15554d696e05c0b30f408227fec1f9d15db"
ARTS=((15181653795,"codeai-olean-r50-local-45964595427-1","sha256:855a35902d6122c60c8cc35fff724817968c2be908a16da21fda32c934ebe3fc"),
      (15181274976,"codeai-olean-r50-independent-45964595427-1","sha256:b2b9dcad44cd5fbf52380a4088a5b23c36a5f59ae22b1ababec84286d7d2ec8d"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R50 run")
    for jid,steps in ((140390147867,["Verify R50 contextual frontier observation","Actual Lean MCP R50 parent theorem audit"]),
                      (140391566547,["Independently verify R50 contextual frontier observation"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R50 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R50 artifact")
    d=load(a.r50_local/"direct.json");mp=load(a.r50_local/"mcp.json");ind=load(a.r50_independent/"independent.json")
    v.need(d==load(a.r50_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R50 evidence")
    for name in FILES:
        raw=(a.r50_local/name).read_bytes()
        v.need(raw==(a.r50_independent/name).read_bytes(),"R50 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r50_local/"capsule";other=a.r50_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR51",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR51Independent",names) and
           {n:old.digest(raw[n]) for n in names}==mem["raw_digests"],"full raw proof identity")
    saved=out/"capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in manifest["files"]]:
        (saved/n).write_bytes((local/n).read_bytes())
    r39.install(saved,manifest)
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    memory=load(out/r48.NEW);graph=load(out/r49.NEW)
    frontier=load(out/r50.NEW)
    hist=gate.admit(prior,mp,ind,index,extension,layer,memory,mem,graph,frontier)
    joint=load(out/r45.NEW);a0=a.r50_local/"joint-capsule";b0=a.r50_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR51",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR51Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    body=prior["fresh_application"]["mcp_source"]
    wanted=gate.prev.names(graph)
    chunks=[wanted[i:i+16] for i in range(0,len(wanted),16)]
    observation="\n".join(gate.prev.observer(sorted(hist),part) for part in chunks)
    candidates,decisions=gate.select(frontier,gate.base.CURRENT)
    entries=list(candidates.items())
    aliases="\n".join(gate.aliases(sorted(hist),dict(entries[i:i+5])) for i in range(0,len(entries),5))
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({c["alias"]:[n] for n,c in candidates.items()})
    source=body+"\n"+aliases
    path=out/"ReferenceR51.lean"
    try:
        log=r23.run_lean([],path,body+"\n"+observation+"\n"+aliases+v.suffix(sorted(expected)))
    except ValueError:
        # Preserve the first actual diagnostics, not just the tail of huge Expr logs.
        if path.with_suffix(".log").is_file():
            lines=path.with_suffix(".log").read_text(encoding="utf-8").splitlines()
            print("\n".join(x for x in lines if len(x)<5000 and
                            ("error:" in x or "error(" in x or "warning:" in x))[:12000],flush=True)
        raise
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"parent kernel drift")
    gate.prev.recheck(hist,graph)
    batches=[json.loads(s[len(gate.prev.MARK):]) for s in log.splitlines() if s.startswith(gate.prev.MARK)]
    v.need(len(batches)==len(chunks) and all(sorted(x["name"] for x in batch)==part for batch,part in zip(batches,chunks)),
           "frontier inventory")
    rows={x["name"]:x for batch in batches for x in batch}
    live=gate.prev.project(graph,hist,rows)
    v.need(all(frontier[k]==x for k,x in live.items()),"R50 full observation drift")
    batches=[json.loads(s[len(gate.MARK):]) for s in log.splitlines() if s.startswith(gate.MARK)]
    references={x["source"]:x for batch in batches for x in batch}
    v.need(len(batches)==4 and sum(map(len,batches))==20 and len(references)==20,"reference inventory")
    records=gate.check_references(candidates,frontier,references,by)
    controls=gate.controls(frontier,candidates,references,by)
    layer_record=gate.base.portable.seal({"schema":"kuuos.codeai.frontier-exact-reference.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_frontier_key":frontier["key"],"parent_graph_key":graph["key"],"r50_direct_digest":gate.DIRECT,
        "r50_mcp_digest":gate.MCP,"records":records,"selection_decisions":decisions,"controls":controls,
        "semantic_search_complete":False,"proof_authority":False})
    v.save(out/NEW,layer_record)
    v.need(len(audit)==61 and r29.observe_scope()==scope,"audit scope")
    d={"status":"R51_DIRECT_CONTEXTUAL_FRONTIER_REFERENCE","source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,
       "scope_digest":old.SCOPE,"r50_direct_digest":gate.DIRECT,"r50_mcp_digest":gate.MCP,
       "capsule_manifest":manifest,"joint_capsule_manifest":joint,"capsule_layer_key":mem["key"],
       "dispatch_layer_key":index["key"],"extension_key":extension["key"],"derived_layer_key":layer["key"],
       "transport_layer_key":memory["key"],"graph_key":graph["key"],"frontier_key":frontier["key"],
       "reference_key":layer_record["key"],"theorem_references":len(records),"non_theorem_holds":44,
       "polymorphic_references":sum(bool(c["universe_parameters"]) for c in candidates.values()),
       "monomorphic_references":sum(not c["universe_parameters"] for c in candidates.values()),
       "exact_type_and_universes":True,"source_proof_identity":True,"application_authority":False,
       "controls":controls,"root_trials":0,"capsule_rebuilds":0,"provider_calls":0,
       "historical_hold_retained":True,"raw_negative_retained":True,"all_repository_dependencies_observed":False,
       "semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",d)
    print("KUUOS_R51_DIRECT",json.dumps({k:d[k] for k in ("reference_key","theorem_references","non_theorem_holds",
        "polymorphic_references","monomorphic_references","exact_type_and_universes","source_proof_identity","controls",
        "root_trials","capsule_rebuilds")}|{"direct_digest":old.digest(d),"audits":len(audit)},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual frontier references","version":"1"}})
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
    result={"status":"R51_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R51_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R51_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    result={"status":"R51_INDEPENDENT_CONTEXTUAL_FRONTIER_REFERENCE_GREEN","source_head":d["source_head"],
        "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),"mcp_digest":old.digest(mp),
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        **{k:d[k] for k in ("capsule_layer_key","dispatch_layer_key","extension_key","derived_layer_key","transport_layer_key",
        "graph_key","frontier_key","reference_key","theorem_references","non_theorem_holds","polymorphic_references",
        "monomorphic_references","exact_type_and_universes","source_proof_identity","application_authority",
        "controls","root_trials","capsule_rebuilds","provider_calls","historical_hold_retained","raw_negative_retained",
        "all_repository_dependencies_observed","semantic_search_complete","proof_authority")},
        "parent_bytes_preserved":True,"reference_bytes_equal":True,"raw_type_and_proof_equal":True,
        "mcp_audits":len(rows),"unobserved_module_count":695}
    v.save(out/"independent.json",result)
    print("KUUOS_R51_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r50-local","r50-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
