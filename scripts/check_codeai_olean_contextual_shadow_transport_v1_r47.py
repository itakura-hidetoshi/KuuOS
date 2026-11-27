#!/usr/bin/env python3
"""R47: infer previously unregistered shadow goals through checked equality."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_derived_compatibility_v1_r46 as r46
from runtime import kuuos_codeai_olean_contextual_shadow_transport_v1 as gate
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from check_codeai_no_go_memory_v1_r2 import normalize
r45=r46.r45
r29=r46.r29
r23=r46.r23
r39=r46.r39
v=r46.v
ROOT=r46.ROOT
load=r46.load
FILES=r46.FILES+(r46.NEW,)
RUN=45958830120
HEAD="6d4df328cb783b9d99ca940b0f81f2ee3babb300"
ARTS=((15179986698,"codeai-olean-r46-local-45958830120-1","sha256:085d849831c4b211753a7f0a37f31f4aa8edb5bb6c1b90bad88efe31254f1aa4"),
      (15179804689,"codeai-olean-r46-independent-45958830120-1","sha256:e391a54a7e265927d1c45e243279a161be63bc842c917d24f94ba590a1146ad8"))
def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R46 run")
    for jid,steps in ((140371559830,["Verify R46 contextual derived compatibility","Actual Lean MCP R46 compatibility audit"]),
                      (140373367573,["Independently verify R46 contextual derived compatibility"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R46 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R46 artifact")
    d=load(a.r46_local/"direct.json");mp=load(a.r46_local/"mcp.json");ind=load(a.r46_independent/"independent.json")
    v.need(d==load(a.r46_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R46 evidence")
    for name in FILES:
        raw=(a.r46_local/name).read_bytes()
        v.need(raw==(a.r46_independent/name).read_bytes(),"R46 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r46_local/"capsule";other=a.r46_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR47",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR47Independent",names) and
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
    global_obs=r29.parse(r23.run_lean([],out/"ObserveR47.lean",dispatch.observe(global_qs)),"KUUOS_R41_CONTEXT ")
    extension=load(out/r45.r44.r43.EXT);layer=load(out/r46.NEW)
    qs=gate.prev.prev.requests(global_qs)
    def observe(label,q):
        controls={n:global_qs[n] for n in ("shadow","raw","alternate")}
        batch={**controls,label:q}
        row=r29.parse(r23.run_lean([],out/("ObserveR47_"+label+".lean"),dispatch.observe(batch)),"KUUOS_R41_CONTEXT ")
        v.need(set(row)==set(batch) and all(row[n]==global_obs[n] for n in controls),"canonical control drift")
        return row[label]
    obs={k:observe("compat_"+k,q) for k,q in sorted(qs.items())}
    decisions,hist=gate.admit(prior,mp,ind,index,extension,layer,mem,qs,obs,global_qs,global_obs)
    joint=load(out/r45.NEW);a0=a.r46_local/"joint-capsule";b0=a.r46_independent/"joint-capsule"
    v.need(joint==gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.prev.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR47",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR47Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)
    targets=gate.requests(qs["shadow"])
    observations={k:observe("transport_"+k,q) for k,q in sorted(targets.items())}
    p=gate.plan(index,extension,layer,qs["shadow"],obs["shadow"],targets,observations)
    controls={}
    def reject(label,q,o,ts,os):
        try:gate.plan(index,extension,layer,q,o,ts,os)
        except ValueError as e:controls[label]=str(e)
        else:raise ValueError("unlawful transport "+label)
    reject("raw_source",qs["raw"],obs["raw"],targets,observations)
    reject("alternate_raw_source",qs["alternate"],obs["alternate"],targets,observations)
    reject("raw_destination",qs["shadow"],obs["shadow"],
           {"compat":qs["alternate"],"global":global_qs["alternate"]},observations)
    bad=copy.deepcopy(observations);bad["compat"]["aligned"]=False
    reject("unaligned_target",qs["shadow"],obs["shadow"],targets,bad)
    v.need(controls=={"raw_source":"HOLD_SHADOW_TRANSPORT_SOURCE",
        "alternate_raw_source":"HOLD_SHADOW_TRANSPORT_SOURCE",
        "raw_destination":"HOLD_SHADOW_TRANSPORT_CONTEXT",
        "unaligned_target":"HOLD_SHADOW_TRANSPORT_CONTEXT"},"transport controls")
    # Reapply the nine remembered compatibility recipes, never rebuild a capsule.
    body0,check0,refs0=gate.prev.consumer(qs,decisions)
    v.need(refs0==prior["compatibility_refs"],"parent recipe drift")
    body,check,refs=gate.consumer(p)
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update(refs)
    log=r23.run_lean([],out/"ApplyR47.lean",body0+body+check0+check+v.suffix(sorted(expected)))
    v.need(r29.parse(log,gate.prev.MARK)=={k:o["goal_expr"] for k,o in obs.items()} and
           r29.parse(log,gate.MARK)=={k:o["goal_expr"] for k,o in observations.items()},"transport exact goal")
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    for n,x in hist.items():
        v.need(all(by[n][f]==x[f] for f in ("type_expr_repr","type_expr_sha256","type_constants",
               "proof_constants","axioms","universe_parameters")),"parent proof drift "+n)
    for n,rs in refs.items():
        v.need(set(rs)<=set(by[n]["proof_constants"]) and
               set(by[n]["axioms"])<={a for r in rs for a in by[r]["axioms"]},"transport dependency "+n)
    v.need(len(audit)==41 and all(set(x["axioms"])<=typed.STANDARD for x in audit) and
           r29.observe_scope()==scope,"audit scope")
    d={"status":"R47_DIRECT_CONTEXTUAL_SHADOW_TRANSPORT","source_head":gate.base.CURRENT,
       "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"r46_direct_digest":gate.DIRECT,
       "r46_mcp_digest":gate.MCP,"capsule_manifest":manifest,"joint_capsule_manifest":joint,
       "capsule_layer_key":mem["key"],"dispatch_layer_key":index["key"],"extension_key":extension["key"],
       "derived_layer_key":layer["key"],"transport_plan":p,"transport_refs":refs,
       "compatibility_witnesses":3,"global_witnesses":3,"new_targets":2,"controls":controls,
       "historical_hold_retained":True,"raw_negative_retained":True,"root_trials":0,"capsule_rebuilds":0,
       "reapplied_compatibility_recipes":9,"provider_calls":0,"exact_kernel_type":True,
       "semantic_search_complete":False,"proof_authority":False,
       "fresh_application":{"observations":audit,"mcp_source":body0+body}}
    v.save(out/"direct.json",d)
    print("KUUOS_R47_DIRECT",json.dumps({"direct_digest":old.digest(d),"derived_layer_key":layer["key"],
          "new_targets":2,"compatibility_witnesses":3,"global_witnesses":3,"root_trials":0,
          "capsule_rebuilds":0,"audits":len(audit),"controls":controls},sort_keys=True),flush=True)
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
                                     "clientInfo":{"name":"KuuOS contextual shadow transport","version":"1"}})
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
    result={"status":"R47_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R47_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R47_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES:
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    v.need(r45.capsule_files(out/"joint-capsule")==r45.capsule_files(first/"joint-capsule")==d["joint_capsule_manifest"]["files"],
           "joint capsule bytes")
    result={"status":"R47_INDEPENDENT_CONTEXTUAL_SHADOW_TRANSPORT_GREEN","source_head":d["source_head"],
            "source_tree":d["source_tree"],"scope_digest":d["scope_digest"],"direct_digest":old.digest(d),
            "mcp_digest":old.digest(mp),"capsule_layer_key":d["capsule_layer_key"],
            "dispatch_layer_key":d["dispatch_layer_key"],"extension_key":d["extension_key"],
            "derived_layer_key":d["derived_layer_key"],"capsule_manifest":d["capsule_manifest"],
            "joint_capsule_manifest":d["joint_capsule_manifest"],"new_targets":2,
            "compatibility_witnesses":3,"global_witnesses":3,"transport_refs":d["transport_refs"],
            "historical_hold_retained":True,"raw_negative_retained":True,"exact_kernel_type":True,
            "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"root_trials":0,
            "capsule_rebuilds":0,"reapplied_compatibility_recipes":9,"provider_calls":0,
            "controls":d["controls"],"mcp_audits":len(rows),"unobserved_module_count":695,
            "semantic_search_complete":False,"proof_authority":False}
    v.save(out/"independent.json",result)
    print("KUUOS_R47_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r46-local","r46-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
