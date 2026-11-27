#!/usr/bin/env python3
"""R65: certified incremental transversal computation over the R60 ledger."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_finite_transversal_enumerator_v1_r64 as r64
from check_codeai_no_go_memory_v1_r2 import normalize
r63=r64.r63
v=r64.v
old=r64.old
ROOT=r64.ROOT
load=r64.load
RUN=46078923504
HEAD="1e4d75f099767002d17ac32f68eb0d052eb13add"
DIRECT="520946aac7ae14e0e933d0e4a144f095e9d1a9ca07eff3494a9746efe03d929f"
MCP="412297c7cbae59332ab87418c2e2557078064099ef74e3a9fdcce33ffd66e58e"
KEY="084447b2d623f1c458e5b31b2137d19e83b3a87c77efcecf9b55b7d004067647"
ARTS=((15237107282,"codeai-olean-r64-r2-local-46078923504-1","sha256:779ba8a89be4817c109e0ad82c7c5f9b600b0745e5bbe6a2bb2454cb63802d59"),
      (15237321889,"codeai-olean-r64-r2-independent-46078923504-1","sha256:62966ef51b62286362b9efe51a3f8fdd2cf89aa979fd92ef9cf4ecdacea633e4"))
FILES=r64.FILES+(r64.NEW,)
NEW="incremental-transversal-ledger-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_incremental_transversal_ledger_v1.lean"
NS="KuuOSR65."
GENERAL=("extend_sound","extend_complete","reduce_exact","incremental_eq_reference",
         "incremental_exact","incremental_recovery_duality","operational_equivalence",
         "singleton_basis_form","pair_list_to_finset","one_list_reference","two_list_reference",
         "incremental_triangle","incremental_four_routes")
REFS={
 "extend_sound":["KuuOSR64.mem_finite_basis"],
 "extend_complete":["KuuOSR64.enumerator_complete"],
 "reduce_exact":["KuuOSR64.mem_reduced_iff"],
 "incremental_eq_reference":[NS+"reduce_exact",NS+"extend_sound",NS+"extend_complete","KuuOSR64.mem_finite_basis"],
 "incremental_exact":[NS+"incremental_eq_reference","KuuOSR64.mem_finite_basis"],
 "incremental_recovery_duality":[NS+"incremental_eq_reference","KuuOSR64.enumerated_recovery_duality"],
 "operational_equivalence":[NS+"incremental_eq_reference"],
 "singleton_basis_form":["KuuOSR64.mem_finite_basis"],
 "pair_list_to_finset":["KuuOSR63.mem_pair_cut"],
 "one_list_reference":[NS+"incremental_eq_reference",NS+"singleton_basis_form"],
 "two_list_reference":[NS+"incremental_eq_reference","KuuOSR64.two_route_enumeration_exact",NS+"pair_list_to_finset"],
 "incremental_triangle":[NS+"incremental_eq_reference","KuuOSR64.triangle_basis_exact"],
 "incremental_four_routes":[NS+"incremental_eq_reference","KuuOSR64.four_route_basis_exact"],
}

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R64 R2 run")
    for jid,steps in ((140773083206,["Verify R64 R2 finite transversal enumerator","Actual Lean MCP R64 R2 finite transversal enumerator audit"]),
                      (140779202774,["Independently verify R64 R2 finite transversal enumerator"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R64 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R64 R2 artifact")
    local=a.r64_local;other=a.r64_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R64_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R64_INDEPENDENT_FINITE_TRANSVERSAL_ENUMERATOR_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==162 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","enumerator_bytes_equal","raw_type_and_proof_equal")),"R64 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==162 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R64 R2 audit")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r64.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_basis_key"]==load(out/r63.NEW)["key"] and
           record["parent_basis_key"]==r64.KEY,"R64 R2 key")
    v.need(d["general_theorems"]==14 and d["executable_tests"]==4 and
           d["parent_raw_replay_bytewise_equal"] and not d["r60_ledger_recomputed_by_general_enumerator"],"R64 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R64 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R64 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r64-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","formal-source-r1.lean","r64-r2-repair.json",
                 "parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           load(receipts/"r64-r2-repair.json")["r1_all_propositions_unchanged"] is True and
           load(receipts/"parent-r63-raw-replay.json")==load(out/r63.NEW)["raw_theorems"] and
           load(receipts/"parent-r62-raw-replay.json")==load(out/r63.r62.NEW)["raw_theorems"],"R64 source and raw lineage")
    for i in range(54,64):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r64.raw_observer(names).replace("KUUOS_R64_RAW ","KUUOS_R65_RAW ").replace("R64 theorem","R65 theorem").replace("R64 not a theorem","R65 not a theorem").replace("R64 proof unavailable","R65 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R65_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R65_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R65 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R65 raw proof")
    return result

def ledger_source(parent):
    rows=parent["contexts"]
    v.need(len(rows)==7 and len(parent["empty_inventory_holds"])==5 and
           sum(len(x["encoded_cuts"]) for x in rows)==1856,"R63 actual ledger scope")
    src=["namespace KuuOSR65"]
    compute=["namespace KuuOSR65"]
    items=[];refs={}
    for row in rows:
        label=row["ledger_theorem"].rsplit("_",1)[-1]
        v.need(label.isdigit() and row["ledger_theorem"]=="KuuOSR63.ledger_eq_"+label,"R63 ledger theorem name")
        a="KuuOSR63.routeA_"+label
        b="KuuOSR63.routeB_"+label
        cut="KuuOSR63.cuts_"+label
        deps=row["route_dependencies"]
        v.need(len(deps) in (1,2) and all(deps),"R63 route scope")
        v.need(len(row["route_names"])==len(deps) and len(row["encoded_cuts"])==len(row["r60_cut_digests"]),"R63 actual row identity")
        route_list="["+a+".toFinset"+(", "+b+".toFinset" if len(deps)==2 else "")+"]"
        expected="(("+cut+".map List.toFinset).toFinset)"
        n="actual_ledger_"+label
        reference=("one_list_reference "+a) if len(deps)==1 else ("two_list_reference "+a+" "+b)
        src += ["theorem "+n+" :",
                "    incrementalBasis ("+route_list+") = "+expected+" := by",
                "  rw ["+row["ledger_theorem"]+"]",
                "  exact "+reference]
        refs[NS+n]=[row["ledger_theorem"],NS+reference.split()[0]]
        # IO evaluation is an independent executable observation. It is not
        # a proof oracle and contributes no new axiom to the theorem above.
        compute += ["set_option maxRecDepth 16384 in",
                    "set_option maxHeartbeats 12000000 in",
                    "run_cmd do",
                    "  let rs : List (Finset Nat) := "+route_list,
                    "  let observed := incrementalBasis rs",
                    "  let expected := "+expected,
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+label+' : Nat)),',
                    '    ("exact", Lean.toJson (decide (observed = expected))),',
                    '    ("observed", Lean.toJson observed.card),',
                    '    ("expected", Lean.toJson expected.card),',
                    '    ("stage_candidates", Lean.toJson (stageCandidateCounts rs))]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R65_COMPUTE " ++ payload.compress)']
        items.append({"index":int(label),"case":row["case"],"route_count":len(deps),
                      "route_sizes":[len(x) for x in deps],"expected_cuts":len(row["encoded_cuts"]),
                      "theorem":NS+n,"parent_ledger_theorem":row["ledger_theorem"],
                      "parent_cut_digests":row["r60_cut_digests"]})
    return "\n".join(src+["end KuuOSR65",""]), "\n".join(compute+["end KuuOSR65",""]), items, refs

def direct(a,out):
    scope=r63.r62.r29.observe_scope()
    d,mp,ind,parent=admit(a,out)
    ledger=load(out/r63.NEW)
    ledger_formal,compute,items,refs=ledger_source(ledger)
    formal=FORMAL.read_text(encoding="utf-8")
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"ledger-application.lean").write_text(ledger_formal,encoding="utf-8")
    (out/"ledger-computation.lean").write_text(compute,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(x["theorem"] for x in items)
    source=d["fresh_application"]["mcp_source"]+"\n"+formal+"\n"+ledger_formal+"\n"+raw_observer(names)
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({NS+n:REFS.get(n,[]) for n in GENERAL})
    expected.update(refs)
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
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R64 full audit drift")
    previous64=r64.raw_audit(log,by,tuple(d["new_theorem_names"]))
    previous63=r63.raw_audit(log,by,tuple(load(out/"parent-r63-receipts"/"direct.json")["new_theorem_names"]))
    previous62=r63.r62.gate.raw_audit(log,by)
    for i,raw in ((64,previous64),(63,previous63),(62,previous62)):v.save(out/("parent-r"+str(i)+"-raw-replay.json"),raw)
    v.need(previous64==parent["raw_theorems"] and previous63==ledger["raw_theorems"] and
           previous62==load(out/r63.r62.NEW)["raw_theorems"],"parent exact raw type/proof/axiom drift")
    raw=raw_audit(log,by,names)
    marker="KUUOS_R65_COMPUTE "
    computations=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==7 and set(by_index)=={x["index"] for x in items},"actual computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(x["exact"] is True and x["expected"]==x["observed"]==item["expected_cuts"] and
               len(x["stage_candidates"])==item["route_count"],"actual exact ledger recomputation")
        item["lean_computation"]=x
    v.need(sum(x["observed"] for x in computations)==1856,"actual computation total")
    v.need(len(audit)==162+len(names) and r63.r62.r29.observe_scope()==scope,"R65 scope")
    v.save(out/"ledger-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved","policy_is_refutation")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.incremental-transversal-ledger.v1",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_enumerator_key":KEY,"parent_basis_key":ledger["key"],"r64_direct_digest":DIRECT,"r64_mcp_digest":MCP,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),
        "application_source_sha256":r63.r62.r23.sha(ledger_formal.encode()),"computation_source_sha256":r63.r62.r23.sha(compute.encode()),
        "algorithm":"incremental extension of antichain; retain already hitting candidates; reduce at every step",
        "contexts":items,"empty_inventory_holds":ledger["empty_inventory_holds"],
        "r60_ledger_recomputed_by_general_enumerator":True,"raw_theorems":raw,
        "formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R65_DIRECT_INCREMENTAL_TRANSVERSAL_LEDGER",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_enumerator_key":KEY,"parent_basis_key":ledger["key"],"incremental_key":record["key"],
        "r64_direct_digest":DIRECT,"r64_mcp_digest":MCP,"capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_ledger_theorems":len(items),"actual_context_count":7,"empty_inventory_hold_count":5,
        "actual_cut_count":1856,"actual_computations":computations,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,"r60_ledger_recomputed_by_general_enumerator":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R65_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS incremental transversal ledger","version":"1"}})
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
    result={"status":"R65_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R65_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R65_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R65 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R65 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R65 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R65 MCP evidence")
    for name in FILES+(NEW,"formal-source.lean","ledger-application.lean","ledger-computation.lean","ledger-computation.json",
                      "parent-r64-raw-replay.json","parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R65 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,65))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R65_INDEPENDENT_INCREMENTAL_TRANSVERSAL_LEDGER_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "incremental_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,"parent_bytes_preserved":True,
        "raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R65_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r64-local","r64-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
