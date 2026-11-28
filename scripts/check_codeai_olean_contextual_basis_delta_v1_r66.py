#!/usr/bin/env python3
"""R66: exact basis deltas from immutable R65/R63 and context-bound route inventories."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_incremental_transversal_ledger_v1_r65 as r65
from check_codeai_no_go_memory_v1_r2 import normalize
r64=r65.r64
r63=r65.r63
v=r65.v
old=r65.old
ROOT=r65.ROOT
load=r65.load
RUN=46085479636
HEAD="e2ed7b755578270b81b4872a2554024778cd63be"
DIRECT="27332d914ae0fb2765f2eef06ba33bff74a25e3c61a4e7e047dd484044ab9535"
MCP="c2cec597bf1ec077712d49e00d5dfea47b0d798f576a36a6f41f1193c16a54ff"
KEY="5ee09096e6183f6e6b4e036c37e4d3568fad996f7b00d8107225dac200a8a284"
ARTS=((15239676722,"codeai-olean-r65-r2-local-46085479636-1","sha256:1bbbe230b117640de7ef7bc8444a56e782f1b426cc7ad3de2d93c3653b28fcf8"),
      (15239513817,"codeai-olean-r65-r2-independent-46085479636-1","sha256:09f332acf53893a703b1ddc3fac7d7a135abb901d94db6a09adbea2721e6600f"))
FILES=r65.FILES+(r65.NEW,)
NEW="contextual-basis-delta-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_contextual_basis_delta_v1.lean"
NS="KuuOSR66."
GENERAL=("update_eq","retained_iff_hits","retained_eq_filter","retired_iff_misses",
         "new_cut_origin","reconstruct_new","reconstruct_old","basis_congr_membership","swap_basis",
         "deletion_collision","deletion_distinct","deletion_no_inverse")
REFS={
    "retained_iff_hits":["KuuOSR65.incremental_exact"],
    "retained_eq_filter":[NS+"retained_iff_hits"],
    "retired_iff_misses":[NS+"retained_iff_hits"],
    "new_cut_origin":["KuuOSR64.mem_reduced_iff"],
    "basis_congr_membership":["KuuOSR65.incremental_exact"],
    "swap_basis":[NS+"basis_congr_membership"],
    "deletion_no_inverse":[NS+"deletion_collision",NS+"deletion_distinct"],
}

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R65 R2 run")
    for jid,steps in ((140793950663,["Verify R65 R2 incremental transversal ledger","Actual Lean MCP R65 R2 incremental transversal ledger audit"]),
                      (140800675504,["Independently verify R65 R2 incremental transversal ledger"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R65 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R65 R2 artifact")
    local=a.r65_local;other=a.r65_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R65_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R65_INDEPENDENT_INCREMENTAL_TRANSVERSAL_LEDGER_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==182 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","incremental_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R65 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==182 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R65 R2 audit")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r65.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_enumerator_key"]==load(out/r64.NEW)["key"] and record["parent_basis_key"]==load(out/r63.NEW)["key"],"R65 R2 key")
    v.need(d["actual_cut_count"]==1856 and d["actual_context_count"]==7 and d["empty_inventory_hold_count"]==5 and
           d["r60_ledger_recomputed_by_general_enumerator"] and d["parent_raw_replay_bytewise_equal"],"R65 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R65 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R65 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r65-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","formal-source-r1.lean","r65-r2-repair.json","ledger-application.lean",
                 "ledger-computation.lean","ledger-computation.json","parent-r64-raw-replay.json",
                 "parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"ledger-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"ledger-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"r65-r2-repair.json")["r1_all_propositions_unchanged"] is True and
           load(receipts/"ledger-computation.json")==record["contexts"],"R65 source and actual ledger lineage")
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R65 parent raw lineage")
    for i in range(54,65):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r65.raw_observer(names).replace("KUUOS_R65_RAW ","KUUOS_R66_RAW ").replace("R65 theorem","R66 theorem").replace("R65 not a theorem","R66 not a theorem").replace("R65 proof unavailable","R66 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R66_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R66_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R66 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R66 raw proof")
    return result

def delta_sources(ledger,incremental,budget):
    rows={x["case"]:x for x in ledger["contexts"]}
    parent={x["case"]:x for x in incremental["contexts"]}
    decisions=budget["decisions"]
    v.need(len(rows)==len(parent)==7 and len(ledger["empty_inventory_holds"])==5,"actual context scope")
    src=["namespace KuuOSR66","open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65"]
    compute=["namespace KuuOSR66","open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65"]
    items=[];refs={}
    target=rows["global_default"];td=decisions["global_default"]
    v.need(target["route_names"]==["KuuOSR53Selected.shadowGlobal_1","KuuOSR53Selected.shadowGlobal_9"] and
           target["route_names"]==td["eligible"] and parent["global_default"]["index"]==3,"target inventory")
    target_cuts={tuple(x) for x in target["encoded_cuts"]}
    v.need(len(target_cuts)==268 and len(target["route_dependencies"])==2,"target basis")
    def literal(cuts):
        return "((" + json.dumps([list(x) for x in sorted(cuts)])+" : List (List Nat)).map List.toFinset).toFinset"
    for i,case in enumerate(("global_boundary","global_probes")):
        row=rows[case];bd=decisions[case]
        v.need(bd["context_id"]==td["context_id"] and bd["request"]["base_request"]==td["request"]["base_request"] and
               bd["all_routes"]==td["all_routes"] and row["route_names"]==bd["eligible"] and
               row["route_names"]==[target["route_names"][i]],"typed common context and route identity")
        v.need(row["route_dependencies"]==[target["route_dependencies"][i]] and
               parent[case]["index"]==(2 if i==0 else 6),"exact route dependency identity")
        index=parent[case]["index"]
        a="KuuOSR63.routeA_"+str(index)+".toFinset"
        added=("KuuOSR63.routeB_3" if i==0 else "KuuOSR63.routeA_3")+".toFinset"
        oldcuts="((KuuOSR63.cuts_"+str(index)+".map List.toFinset).toFinset)"
        newcuts="((KuuOSR63.cuts_3.map List.toFinset).toFinset)"
        name="actual_update_"+str(i)
        src += ["theorem "+name+" :", "    updateBasis ("+added+") "+oldcuts+" = "+newcuts+" := by",
                "  calc",
                "    _ = updateBasis ("+added+") (incrementalBasis ["+a+"]) :=",
                "      congrArg (updateBasis ("+added+")) KuuOSR65.actual_ledger_"+str(index)+".symm",
                "    _ = incrementalBasis ["+added+", "+a+"] := update_eq ("+added+") ["+a+"]"]
        if i==0:
            src += ["    _ = incrementalBasis ["+a+", "+added+"] := swap_basis ("+added+") ("+a+")"]
        src += ["    _ = "+newcuts+" := KuuOSR65.actual_ledger_3"]
        refs[NS+name]=[NS+"update_eq","KuuOSR65.actual_ledger_"+str(index),"KuuOSR65.actual_ledger_3"]+([NS+"swap_basis"] if i==0 else [])
        old_cuts={tuple(x) for x in row["encoded_cuts"]}
        retained=old_cuts&target_cuts;retired=old_cuts-target_cuts;introduced=target_cuts-old_cuts
        v.need((len(retained),len(retired),len(introduced))==((260,1,8) if i==0 else (260,8,8)),"actual delta sizes")
        # Independently evaluate actual Lean structures against explicit immutable
        # ledger differences, not just counts. Reverse deletion uses retained route data.
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let old := "+oldcuts,
                    "  let target := "+newcuts,
                    "  let updated := updateBasis ("+added+") old",
                    "  let retained := old ∩ updated",
                    "  let retired := old \\ updated",
                    "  let introduced := updated \\ old",
                    "  let expectedRetained := "+literal(retained),
                    "  let expectedRetired := "+literal(retired),
                    "  let expectedIntroduced := "+literal(introduced),
                    "  let restored := incrementalBasis ["+a+"]",
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("exact", Lean.toJson (decide (updated = target))),',
                    '    ("retained_exact", Lean.toJson (decide (retained = expectedRetained))),',
                    '    ("retired_exact", Lean.toJson (decide (retired = expectedRetired))),',
                    '    ("introduced_exact", Lean.toJson (decide (introduced = expectedIntroduced))),',
                    '    ("reverse_recomputed_exact", Lean.toJson (decide (restored = old))),',
                    '    ("retained", Lean.toJson retained.card),',
                    '    ("retired", Lean.toJson retired.card),',
                    '    ("introduced", Lean.toJson introduced.card),',
                    '    ("update_candidates", Lean.toJson (extendCuts ('+added+') old).card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R66_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"source_case":case,"target_case":"global_default","context_id":bd["context_id"],
                      "source_request_id":bd["request_id"],"target_request_id":td["request_id"],
                      "source_routes":row["route_names"],"added_route":target["route_names"][1-i],
                      "source_basis_count":len(old_cuts),"target_basis_count":len(target_cuts),
                      "retained":[list(x) for x in sorted(retained)],"retired":[list(x) for x in sorted(retired)],
                      "introduced":[list(x) for x in sorted(introduced)],"theorem":NS+name,
                      "transition_kind":"counterfactual replay of recorded contexts","active_policy_changed":False,
                      "reverse_recomputed_from_retained_route_inventory":True})
    return "\n".join(src+["end KuuOSR66",""]),"\n".join(compute+["end KuuOSR66",""]),items,refs

def direct(a,out):
    scope=r63.r62.r29.observe_scope()
    d,mp,ind,parent=admit(a,out)
    ledger=load(out/r63.NEW)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=delta_sources(ledger,parent,load(out/"contextual-budget-selection-v1.json"))
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"delta-application.lean").write_text(app,encoding="utf-8")
    (out/"delta-computation.lean").write_text(compute,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(x["theorem"] for x in items)
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
    kernel_rows=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    missing={x["name"]:sorted(set(expected[x["name"]])-set(x["proof_constants"])) for x in kernel_rows
             if x["name"] in expected and set(expected[x["name"]])-set(x["proof_constants"])}
    v.need(not missing,"R66 required direct reference missing "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R65 full audit drift")
    previous65=r65.raw_audit(log,by,tuple(d["new_theorem_names"]))
    previous64=r64.raw_audit(log,by,tuple(load(out/"parent-r64-receipts"/"direct.json")["new_theorem_names"]))
    previous63=r63.raw_audit(log,by,tuple(load(out/"parent-r63-receipts"/"direct.json")["new_theorem_names"]))
    previous62=r63.r62.gate.raw_audit(log,by)
    for i,raw,layer in ((65,previous65,r65.NEW),(64,previous64,r64.NEW),(63,previous63,r63.NEW),(62,previous62,r63.r62.NEW)):
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),raw)
        v.need(raw==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R66_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"delta computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("exact","retained_exact","retired_exact","introduced_exact","reverse_recomputed_exact")) and
               all(x[k]==len(item[k]) for k in ("retained","retired","introduced")),"actual delta equality")
        item["lean_computation"]=x
    v.need(len(audit)==182+len(names) and r63.r62.r29.observe_scope()==scope,"R66 scope")
    v.save(out/"delta-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved","policy_is_refutation")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.contextual-basis-delta.v1",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_incremental_key":KEY,"parent_basis_key":ledger["key"],"r65_direct_digest":DIRECT,"r65_mcp_digest":MCP,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),
        "application_source_sha256":r63.r62.r23.sha(app.encode()),"computation_source_sha256":r63.r62.r23.sha(compute.encode()),
        "context_transitions":items,"empty_inventory_holds":ledger["empty_inventory_holds"],
        "route_deletion_basis_only_inverse_disproved":True,"route_removal_requires_sufficient_retained_information":True,
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R66_DIRECT_CONTEXTUAL_BASIS_DELTA",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_incremental_key":KEY,"delta_key":record["key"],"r65_direct_digest":DIRECT,"r65_mcp_digest":MCP,
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_delta_theorems":len(items),"actual_delta_count":2,"empty_inventory_hold_count":5,
        "actual_computations":computations,"route_deletion_basis_only_inverse_disproved":True,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R66_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS contextual basis delta","version":"1"}})
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
    result={"status":"R66_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R66_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R66_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R66 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R66 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R66 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R66 MCP evidence")
    for name in FILES+(NEW,"formal-source.lean","delta-application.lean","delta-computation.lean","delta-computation.json",
                      "parent-r65-raw-replay.json","parent-r64-raw-replay.json","parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R66 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,66))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R66_INDEPENDENT_CONTEXTUAL_BASIS_DELTA_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "delta_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,"parent_bytes_preserved":True,
        "raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R66_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r65-local","r65-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
