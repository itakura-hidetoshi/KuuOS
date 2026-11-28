#!/usr/bin/env python3
"""R67: reversible set patches over the exact certified R66 deltas."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_basis_delta_v1_r66_r2 as r66
from check_codeai_no_go_memory_v1_r2 import normalize
r65=r66.r65
r64=r66.r64
r63=r66.r63
v=r66.v
old=r66.old
ROOT=r66.ROOT
load=r66.load
RUN=46092659167
HEAD="d1f42f431f536706cb86c0d302ef07da7f158843"
DIRECT="2d9cd7e7da39ea68149745b1610ba5aa00c14e3ecf4a907e277a7912ebcf8456"
MCP="759d5778bd2e085e114fa0bdc4d5d72697cd79d8ac9b383b8cbd9dbf8a0d5121"
KEY="ec850ea209298ed38364835e1506201cd4ed585ffe217dc4e3223789dc06428b"
SCOPE="45681a82fd054aca0713e77a1b650b77d04627d3c0f984a71fd46d156e3f236c"
ARTS=((15242966885,"codeai-olean-r66-r2-local-46092659167-1","sha256:16963ba0fc3fb07ff9ab8089827f9f29cb79ae8513afb970c98770d8b48be5da"),
      (15243146539,"codeai-olean-r66-r2-independent-46092659167-1","sha256:a5e5e8f8f4fbbf669e22ff29f483a4e94b3b60fbee1c7f3f1cce4ae99903de73"))
FILES=r66.FILES+(r66.NEW,)
NEW="reversible-basis-patch-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_reversible_basis_patch_v1.lean"
NS="KuuOSR67."
GENERAL=("patch_retired","patch_introduced","reverse_valid","actual_patch_valid","keep_eq_inter",
         "apply_diff_exact","rollback_exact","patch_unique","checked_diff_exact","checked_roundtrip",
         "checked_reject_missing","checked_reject_overlap","checked_bound_exact","checked_bound_reject_wrong")
REFS={
 "reverse_valid":[NS+"patch_retired"],
 "apply_diff_exact":[NS+"keep_eq_inter","KuuOSR66.reconstruct_new"],
 "rollback_exact":[NS+"patch_introduced",NS+"patch_retired",NS+"apply_diff_exact"],
 "patch_unique":[NS+"patch_retired",NS+"patch_introduced"],
 "checked_diff_exact":[NS+"actual_patch_valid",NS+"apply_diff_exact"],
 "checked_roundtrip":[NS+"reverse_valid",NS+"rollback_exact"],
 "checked_bound_exact":[NS+"actual_patch_valid",NS+"apply_diff_exact"],
}

def admit(a,out,scope):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R66 R2 run")
    for jid,steps in ((140816901724,["Verify R66 R2 contextual basis delta","Actual Lean MCP R66 R2 contextual basis delta audit"]),
                      (140823854687,["Independently verify R66 R2 contextual basis delta"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R66 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R66 R2 artifact")
    local=a.r66_local;other=a.r66_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R66_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R66_INDEPENDENT_CONTEXTUAL_BASIS_DELTA_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==196 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","delta_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R66 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==196 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R66 R2 audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r66.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_incremental_key"]==load(out/r65.NEW)["key"],"R66 R2 key")
    v.need(record["historical_research_only"] and record["live_main_admission"] is False and
           record["current_main_certification_transferred"] is False and d["historical_scope_digest"]==SCOPE==old.digest(scope) and
           record["historical_scope_digest"]==SCOPE and d["route_deletion_basis_only_inverse_disproved"] and
           len(record["context_transitions"])==2 and d["empty_inventory_hold_count"]==5,"R66 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R66 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R66 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r66-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","delta-application.lean","delta-computation.lean","delta-computation.json",
                 "historical-scope.json","parent-r65-raw-replay.json","parent-r64-raw-replay.json",
                 "parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(load(receipts/"historical-scope.json")==scope and
           r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"delta-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"delta-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"delta-computation.json")==record["context_transitions"],"R66 source and delta lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["current_main_certification_transferred"] is False and x["live_main_admission"] is False for x in obs.values()),"R66 live observation")
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R66 ancestor raw lineage")
    for i in range(54,66):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r66.raw_observer(names).replace("KUUOS_R66_RAW ","KUUOS_R67_RAW ").replace("R66 theorem","R67 theorem").replace("R66 not a theorem","R67 not a theorem").replace("R66 proof unavailable","R67 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R67_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R67_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R67 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R67 raw proof")
    return result

def patch_sources(ledger,parent):
    rows={x["case"]:x for x in ledger["contexts"]}
    v.need(len(rows)==7 and len(ledger["empty_inventory_holds"])==5,"R63 scope")
    src=["namespace KuuOSR67","open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65 KuuOSR66"]
    compute=["namespace KuuOSR67","open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65 KuuOSR66"]
    items=[];refs={}
    def literal(cuts):
        return "(("+json.dumps(cuts)+" : List (List Nat)).map List.toFinset).toFinset"
    for i,t in enumerate(parent["context_transitions"]):
        v.need(t["index"]==i and t["target_case"]=="global_default" and
               t["source_case"]==("global_boundary" if i==0 else "global_probes") and
               t["theorem"]=="KuuOSR66.actual_update_"+str(i) and t["lean_computation"]["exact"],"R66 transition identity")
        F={tuple(x) for x in rows[t["source_case"]]["encoded_cuts"]}
        G={tuple(x) for x in rows[t["target_case"]]["encoded_cuts"]}
        v.need({tuple(x) for x in t["retained"]}==F&G and {tuple(x) for x in t["retired"]}==F-G and
               {tuple(x) for x in t["introduced"]}==G-F and len(F)==t["source_basis_count"] and
               len(G)==t["target_basis_count"],"R66 exact delta values")
        index=2 if i==0 else 6
        oldcuts="((KuuOSR63.cuts_"+str(index)+".map List.toFinset).toFinset)"
        newcuts="((KuuOSR63.cuts_3.map List.toFinset).toFinset)"
        added=("KuuOSR63.routeB_3" if i==0 else "KuuOSR63.routeA_3")+".toFinset"
        updated="(updateBasis ("+added+") "+oldcuts+")"
        origin="KuuOSR66.actual_update_"+str(i)
        fwd="actual_forward_"+str(i);back="actual_rollback_"+str(i)
        src += ["theorem "+fwd+" :",
                "    checkedPatch "+oldcuts+" ("+oldcuts+" \\ "+updated+") ("+updated+" \\ "+oldcuts+") = some "+newcuts+" :=",
                "  (checked_diff_exact "+oldcuts+" "+updated+").trans (congrArg some "+origin+")",
                "theorem "+back+" :",
                "    checkedPatch "+newcuts+" ("+updated+" \\ "+oldcuts+") ("+oldcuts+" \\ "+updated+") = some "+oldcuts+" :=",
                "  (congrArg (fun H => checkedPatch H ("+updated+" \\ "+oldcuts+") ("+oldcuts+" \\ "+updated+")) "+origin+".symm).trans",
                "    (checked_diff_exact "+updated+" "+oldcuts+")"]
        refs[NS+fwd]=[NS+"checked_diff_exact",origin]
        refs[NS+back]=[NS+"checked_diff_exact",origin]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let old := "+oldcuts,"  let target := "+newcuts,
                    "  let removed := "+literal(t["retired"]),
                    "  let added := "+literal(t["introduced"]),
                    "  let retained := "+literal(t["retained"]),
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("forward_exact", Lean.toJson (decide (checkedPatch old removed added = some target))),',
                    '    ("rollback_exact", Lean.toJson (decide (checkedPatch target added removed = some old))),',
                    '    ("bound_forward_exact", Lean.toJson (decide (checkedBoundPatch old target removed added = some target))),',
                    '    ("bound_rollback_exact", Lean.toJson (decide (checkedBoundPatch target old added removed = some old))),',
                    '    ("missing_retired_hold", Lean.toJson (decide (checkedPatch old (removed ∪ added) added = none))),',
                    '    ("duplicate_introduction_hold", Lean.toJson (decide (checkedPatch old removed (added ∪ retained) = none))),',
                    '    ("wrong_endpoint_hold", Lean.toJson (decide (checkedBoundPatch old old removed added = none))),',
                    '    ("removed", Lean.toJson removed.card),',
                    '    ("introduced", Lean.toJson added.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R67_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"source_case":t["source_case"],"target_case":t["target_case"],
                      "parent_transition_digest":old.digest(t),"context_id":t["context_id"],
                      "source_request_id":t["source_request_id"],"target_request_id":t["target_request_id"],
                      "source_routes":t["source_routes"],"added_route":t["added_route"],
                      "retired":t["retired"],"introduced":t["introduced"],
                      "forward_theorem":NS+fwd,"rollback_theorem":NS+back,
                      "counterfactual_only":True,"active_policy_changed":False,"action_authority":False})
    return "\n".join(src+["end KuuOSR67",""]),"\n".join(compute+["end KuuOSR67",""]),items,refs

def direct(a,out):
    scope=r66.observe_historical_scope()
    start_main=r66.observe_live_main(scope)
    v.save(out/"historical-scope.json",scope)
    v.save(out/"main-observations.json",{"before":start_main})
    d,mp,ind,parent=admit(a,out,scope)
    ledger=load(out/r63.NEW)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=patch_sources(ledger,parent)
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"patch-application.lean").write_text(app,encoding="utf-8")
    (out/"patch-computation.lean").write_text(compute,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(n for x in items for n in (x["forward_theorem"],x["rollback_theorem"]))
    source=d["fresh_application"]["mcp_source"]+"\n"+formal+"\n"+app+"\n"+raw_observer(names)
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({NS+n:REFS.get(n,[]) for n in GENERAL});expected.update(refs)
    p=ROOT/"artifacts"/"olean-r62"/"RecoveryDualityR62.lean"
    p.parent.mkdir(parents=True,exist_ok=False)
    try:
        log=r63.r62.r23.run_lean([],p,source+"\n"+compute+v.suffix(sorted(expected)))
    except ValueError:
        if p.with_suffix(".log").is_file():
            lines=p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
            for i,line in enumerate(lines):
                if len(line)<5000 and ("error:" in line or "error(" in line or "warning:" in line):
                    print("\n".join(z[:6000] for z in lines[i:i+12])[:30000],flush=True)
        raise
    finally:
        for path in (p,p.with_suffix(".log")):
            if path.is_file():shutil.copyfile(path,out/path.name)
    marker="KUUOS_RECALL_KERNEL "
    kernel=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    missing={x["name"]:sorted(set(expected[x["name"]])-set(x["proof_constants"])) for x in kernel
             if x["name"] in expected and set(expected[x["name"]])-set(x["proof_constants"])}
    v.need(not missing,"R67 missing direct reference "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R66 full audit drift")
    for i,layer,checker in ((66,r66.NEW,r66.raw_audit),(65,r65.NEW,r65.raw_audit),
                            (64,r64.NEW,r64.raw_audit),(63,r63.NEW,r63.raw_audit)):
        previous=checker(log,by,tuple(load(out/("parent-r"+str(i)+"-receipts")/"direct.json")["new_theorem_names"]))
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),previous)
        v.need(previous==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous62==load(out/r63.r62.NEW)["raw_theorems"],"R62 raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R67_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"patch computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("forward_exact","rollback_exact","bound_forward_exact","bound_rollback_exact",
               "missing_retired_hold","duplicate_introduction_hold","wrong_endpoint_hold")) and
               x["removed"]==len(item["retired"]) and x["introduced"]==len(item["introduced"]),"patch exactness and negative controls")
        item["lean_computation"]=x
    v.need(len(audit)==196+len(names) and r66.observe_historical_scope()==scope,"R67 scope")
    end_main=r66.observe_live_main(scope)
    v.need(v.cache.ancestor(v.cache.api,start_main["head"],end_main["head"]),"R67 live main rewound")
    v.save(out/"main-observations.json",{"before":start_main,"after":end_main})
    v.save(out/"patch-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.reversible-basis-patch.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_delta_key":KEY,"r66_direct_digest":DIRECT,"r66_mcp_digest":MCP,"historical_scope_digest":SCOPE,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),"application_source_sha256":r63.r62.r23.sha(app.encode()),
        "computation_source_sha256":r63.r62.r23.sha(compute.encode()),"patches":items,
        "empty_inventory_holds":ledger["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R67_DIRECT_REVERSIBLE_BASIS_PATCH",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_delta_key":KEY,"patch_key":record["key"],"r66_direct_digest":DIRECT,"r66_mcp_digest":MCP,
        "historical_scope_digest":SCOPE,"capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_patch_theorems":len(names)-len(GENERAL),"actual_patch_count":len(items),
        "empty_inventory_hold_count":5,"actual_computations":computations,"deletion_basis_only_no_inverse_retained":True,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R67_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
        {"direct_digest":old.digest(result),"audits":len(audit)},sort_keys=True),flush=True)
    return result

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
                                     "clientInfo":{"name":"KuuOS reversible basis patch","version":"1"}})
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
    result={"status":"R67_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R67_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R67_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R67 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R67 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R67 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R67 MCP evidence")
    for folder in (out,first):
        obs=load(folder/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["current_main_certification_transferred"] is False and x["live_main_admission"] is False for x in obs.values()),"R67 live observations")
    for name in FILES+(NEW,"historical-scope.json","formal-source.lean","patch-application.lean","patch-computation.lean",
                      "patch-computation.json",*("parent-r"+str(i)+"-raw-replay.json" for i in range(62,67))):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R67 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,67))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R67_INDEPENDENT_REVERSIBLE_BASIS_PATCH_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "patch_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R67_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r66-local","r66-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
