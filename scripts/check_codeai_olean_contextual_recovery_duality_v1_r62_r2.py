#!/usr/bin/env python3
"""R62: formal obstruction/recovery duality and finite recovery truth tables."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_recovery_v1_r61 as r61
r60=r61.r60
r59=r60.r59
r58=r59.r58
r57=r58.r57
r56=r57.r56
r55=r56.r55
r54=r55.r54
from runtime import kuuos_codeai_olean_contextual_recovery_duality_v1_r2 as gate
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
FILES=r61.FILES+(r61.NEW,)
NEW="contextual-recovery-duality-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_contextual_recovery_duality_v1.lean"
RUN=45989637883
HEAD="a98303dadbfa10eb77dfff164267a2c60494456b"
ARTS=((15192919460,"codeai-olean-r61-local-45989637883-1","sha256:f27f44154b3e661c245fbc5d9230fe396ae66e60c46d139036ca9113242a0c76"),
      (15193946150,"codeai-olean-r61-independent-45989637883-1","sha256:db762ff4e74fbdbfcdffc66dad083b477a1d17179b73ba4a5763d382b5e50623"))

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R61 run")
    for jid,steps in ((140473902140,["Verify R61 contextual recovery","Actual Lean MCP R61 typed recovery diagnostic audit"]),
                      (140477607000,["Independently verify R61 contextual recovery"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R61 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R61 artifact")
    d=load(a.r61_local/"direct.json");mp=load(a.r61_local/"mcp.json");ind=load(a.r61_independent/"independent.json")
    v.need(d==load(a.r61_independent/"direct.json") and old.digest(d)==gate.DIRECT and old.digest(mp)==gate.MCP,"R61 evidence")
    for name in FILES:
        raw=(a.r61_local/name).read_bytes()
        v.need(raw==(a.r61_independent/name).read_bytes(),"R61 immutable bytes "+name)
        (out/name).write_bytes(raw)
    return d,mp,ind

def direct(a,out):
    scope=r29.observe_scope()
    prior,mp,ind=admit(a,out)
    mem=load(out/"composite-capsule-layer-v1.json");index=load(out/"capsule-dispatch-layer-v1.json")
    manifest=load(out/"capsule-manifest.json")
    v.need(manifest==gate.comparison_gate.dispatch.prev.MANIFEST==prior["capsule_manifest"]==ind["capsule_manifest"],"manifest")
    names=sorted(mem["raw_digests"]);local=a.r61_local/"capsule";other=a.r61_independent/"capsule"
    v.need(r39.capsule_files(local)==r39.capsule_files(other)==manifest["files"],"capsule bytes")
    source=gate.comparison_gate.dispatch.MODULE+".lean"
    v.need((local/source).read_bytes()==(other/source).read_bytes() and
           r23.sha((local/source).read_bytes())==manifest["source_sha256"],"source binding")
    raw=r39.raw_read(local,out,"RawParentR62",names)
    v.need(raw==r39.raw_read(other,out,"RawParentR62Independent",names) and
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
    av=load(out/r57.NEW)
    edges=load(out/r58.NEW)
    paths=load(out/r59.NEW)
    obstruction=load(out/r60.NEW)
    recovery=load(out/r61.NEW)
    hist=gate.admit(prior,mp,ind,comparison,selection,pref,budget,av,edges,paths,obstruction,recovery)
    joint=load(out/r45.NEW);a0=a.r61_local/"joint-capsule";b0=a.r61_independent/"joint-capsule"
    v.need(joint==gate.comparison_gate.MANIFEST==prior["joint_capsule_manifest"]==ind["joint_capsule_manifest"] and
           r45.capsule_files(a0)==r45.capsule_files(b0)==joint["files"],"joint capsule manifest")
    source=gate.comparison_gate.derived.prev.MODULE+".lean"
    v.need((a0/source).read_bytes()==(b0/source).read_bytes() and
           r23.sha((a0/source).read_bytes())==joint["source_sha256"],"joint source identity")
    names=sorted(n for n in hist if n.startswith(("KuuOSR44Replay.","KuuOSR44Joint.")) or
                 n=="KuuOSOleanR12.r44_alt_recall.witness")
    v.need(len(names)==15,"joint theorem inventory")
    raw=r45.raw_read(a0,out,"RawJointR62",names)
    v.need(raw==r45.raw_read(b0,out,"RawJointR62Independent",names) and
           all(raw[n]["type_expr"]==hist[n]["type_expr_repr"] for n in names),"joint full raw identity")
    for record in layer["records"]:
        for route in record["routes"]:
            v.need(old.digest(raw[route["joint_root"]])==route["joint_raw_digest"],"joint route proof drift")
    saved=out/"joint-capsule";saved.mkdir()
    for n in [source]+[x["name"] for x in joint["files"]]:
        (saved/n).write_bytes((a0/n).read_bytes())
    r45.install(saved,joint)

    # Preserve original receipts separately; the new receipts cannot overwrite them.
    receipts=out/"parent-r61-receipts";receipts.mkdir()
    for name,src in (("direct.json",a.r61_local),("mcp.json",a.r61_local),("independent.json",a.r61_independent)):
        (receipts/name).write_bytes((src/name).read_bytes())
    ancestors={}
    for i in range(54,61):
        folder="parent-r"+str(i)+"-receipts";ancestor=out/folder;ancestor.mkdir()
        for name in ("direct.json","mcp.json","independent.json"):
            raw=(a.r61_local/folder/name).read_bytes()
            v.need(raw==(a.r61_independent/folder/name).read_bytes(),"ancestor receipt byte drift")
            (ancestor/name).write_bytes(raw)
        ancestors[i]=[load(ancestor/name) for name in ("direct.json","mcp.json","independent.json")]
    g61=gate.prev;g60=g61.prev;g59=g60.prev;g58=g59.prev;g57=g58.prev;g56=g57.prev;g55=g56.prev
    parent_hist=g55.require_parent(*ancestors[54],comparison,selection)
    hs=[parent_hist,g56.admit(*ancestors[55],comparison,selection,pref),
        g57.admit(*ancestors[56],comparison,selection,pref,budget),
        g58.admit(*ancestors[57],comparison,selection,pref,budget,av),
        g59.admit(*ancestors[58],comparison,selection,pref,budget,av,edges),
        g60.admit(*ancestors[59],comparison,selection,pref,budget,av,edges,paths),
        g61.admit(*ancestors[60],comparison,selection,pref,budget,av,edges,paths,obstruction)]
    v.need(all(hist[n]==x for h in hs for n,x in h.items()),"ancestor identity")
    edge_obs=edges["edge_observations"]
    expanded=g58.project(comparison,parent_hist,av,edge_obs)
    projection=g59.project(edges,av,budget,comparison,parent_hist,expanded)
    groups=g60.project(paths,budget,projection,expanded)
    v.need(groups==obstruction["groups"],"R60 basis drift")
    previous,_=g60.plan(paths,edges,av,budget,pref,selection,groups)
    v.need(previous==obstruction["decisions"],"R60 decision drift")
    decisions,selected=g61.plan(obstruction,paths,budget,pref,selection)
    v.need(decisions==recovery["decisions"] and
           g61.controls(obstruction,paths,budget,pref,decisions)==recovery["controls"],"R61 recovery drift")
    v.need(set(selected)==set(recovery["diagnostic_witnesses"]),"R61 diagnostic inventory")
    table,table_code=gate.truth_table(recovery,obstruction,paths,budget)
    original_table,original_code=gate.r1.truth_table(recovery,obstruction,paths,budget)
    v.need(table==original_table and table_code.replace(" := by\n  simp\n\n"," := by\n  decide\n\n")==original_code,"R62 all propositions unchanged")
    formal=FORMAL.read_text(encoding="utf-8")
    v.need(all("theorem "+n in formal for n in gate.FORMAL_NAMES),"R62 theorem inventory")
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"finite-table.lean").write_text(table_code,encoding="utf-8")
    (out/"finite-table-r1.lean").write_text(original_code,encoding="utf-8")
    prefix=prior["fresh_application"]["mcp_source"]
    source=prefix+"\n"+formal+"\n"+table_code+"\n"+gate.raw_observer()
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({n:gate.REFS.get(n,[]) for n in gate.NAMES})
    p=out/"RecoveryDualityR62.lean"
    try:log=r23.run_lean([],p,source+v.suffix(sorted(expected)))
    except ValueError:
        if p.with_suffix(".log").is_file():
            lines=p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
            for i,line in enumerate(lines):
                if len(line)<5000 and ("error:" in line or "error(" in line or "warning:" in line):
                    print("\n".join(z[:6000] for z in lines[i:i+5])[:16000],flush=True)
        raise
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R61 complete audit drift")
    rows=[json.loads(x[len(gate.comparison_gate.MARK):]) for x in log.splitlines() if x.startswith(gate.comparison_gate.MARK)]
    observations={x["name"]:x for x in rows}
    v.need(len(rows)==5 and observations==comparison["replay_observations"],"R54 exact replay proof drift")
    replay_env=[json.loads(x[len(g57.MARK):]) for x in log.splitlines() if x.startswith(g57.MARK)]
    env_obs={x["route"]:x for x in replay_env}
    v.need(len(replay_env)==5 and env_obs==av["environment_observations"],"R57 environment replay drift")
    v.need(g57.project(comparison,parent_hist,frontier,env_obs)==av["availability"],"R57 availability drift")
    replay_edges=[json.loads(x[len(g58.MARK):]) for x in log.splitlines() if x.startswith(g58.MARK)]
    actual_edges={x["route"]:x for x in replay_edges}
    v.need(len(replay_edges)==5 and actual_edges==edge_obs,"R58 edge replay drift")
    fresh_expanded=g58.project(comparison,parent_hist,av,actual_edges)
    fresh_projection=g59.project(edges,av,budget,comparison,parent_hist,fresh_expanded)
    v.need(fresh_projection==projection,"R59 path witness replay drift")
    v.need(g60.project(paths,budget,fresh_projection,fresh_expanded)==groups,"R60 basis replay drift")
    v.need(g61.plan(obstruction,paths,budget,pref,selection)==(decisions,selected),"R61 recovery replay drift")
    projected=gate.comparison_gate.project(selection,parent_hist,frontier,observations)
    v.need(all(comparison[k]==x for k,x in projected.items()),"R54 preference projection drift")
    raw=gate.raw_audit(log,by)
    v.need(len(audit)==99+len(gate.NAMES) and r29.observe_scope()==scope,"R62 audit scope")
    used=sorted({ax for x in raw.values() for ax in x["axioms"]})
    record=gate.base.portable.seal({"schema":"kuuos.codeai.contextual-recovery-duality.v1",
        "source_head":gate.base.CURRENT,"source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_recovery_key":recovery["key"],"parent_obstruction_key":obstruction["key"],
        "r61_direct_digest":gate.DIRECT,"r61_mcp_digest":gate.MCP,
        "formal_source_sha256":r23.sha(formal.encode()),"finite_source_sha256":r23.sha(table_code.encode()),
        "r1_finite_source_sha256":r23.sha(original_code.encode()),"r1_all_propositions_unchanged":True,
        "formal_observations":{n:by[n] for n in gate.NAMES},"raw_theorems":raw,"finite_table":table,
        "retained_records":pref["retained_records"],"retained_groups":pref["retained_groups"],
        "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "active_policy_changed":False,"release_authorized":False,"external_approval_required":True,
        "complete_transitive_closure":False,"policy_is_refutation":False,"proof_authority":False,
        "action_authority":False,"semantic_search_complete":False,"python_general_correctness_proved":False})
    v.save(out/NEW,record)
    d={"status":"R62_DIRECT_CONTEXTUAL_RECOVERY_DUALITY","source_head":gate.base.CURRENT,
        "source_tree":gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,"parent_recovery_key":recovery["key"],
        "r61_direct_digest":gate.DIRECT,"r61_mcp_digest":gate.MCP,"duality_key":record["key"],
        "capsule_manifest":manifest,"joint_capsule_manifest":joint,"request_count":len(decisions),
        "general_theorems":len(gate.FORMAL_NAMES),"finite_table_theorems":len(gate.TABLE_NAMES),
        "finite_table_rows":len(table),"finite_minimal_candidates":sum(x["inclusion_minimal"] for x in table),
        "formal_source_sha256":record["formal_source_sha256"],"finite_source_sha256":record["finite_source_sha256"],
        "r1_finite_source_sha256":record["r1_finite_source_sha256"],"r1_all_propositions_unchanged":True,
        "new_theorem_names":list(gate.NAMES),"new_theorem_axioms":used,"raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},
        "active_dispatches":0,"retained_routes":len(pref["retained_records"]),
        "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "new_root_discovery_trials":0,"parent_replayed_routes":len(rows),"parent_replay_premise_probes":sum(x["probes"] for x in rows),
        "capsule_rebuilds":0,"complete_transitive_closure":False,"policy_is_refutation":False,
        "active_policy_changed":False,"release_authorized":False,"external_approval_required":True,
        "proof_authority":False,"action_authority":False,"semantic_search_complete":False,"all_repository_dependencies_observed":False,
        "python_general_correctness_proved":False,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",d)
    print("KUUOS_R62_DIRECT",json.dumps({k:x for k,x in d.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS contextual recovery duality","version":"1"}})
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
    result={"status":"R62_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R62_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R62_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent receipt")
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
    for name in FILES+(NEW,"formal-source.lean","finite-table.lean","finite-table-r1.lean"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent ledger bytes")
    v.need(r39.capsule_files(out/"capsule")==r39.capsule_files(first/"capsule")==d["capsule_manifest"]["files"],"independent retained capsule bytes")
    v.need(r45.capsule_files(out/"joint-capsule")==r45.capsule_files(first/"joint-capsule")==d["joint_capsule_manifest"]["files"],
           "joint capsule bytes")

    for folder in ("parent-r54-receipts","parent-r55-receipts","parent-r56-receipts","parent-r57-receipts","parent-r58-receipts","parent-r59-receipts","parent-r60-receipts","parent-r61-receipts"):
        for name in ("direct.json","mcp.json","independent.json"):
            v.need((out/folder/name).read_bytes()==(first/folder/name).read_bytes(),"ancestor receipt byte drift")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R62_INDEPENDENT_CONTEXTUAL_RECOVERY_DUALITY_GREEN","direct_digest":old.digest(d),
                   "mcp_digest":old.digest(mp),"mcp_audits":len(rows),"duality_bytes_equal":True,"raw_new_proofs_equal":True,
                   "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R62_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r61-local","r61-independent","first"):
        p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":main()
