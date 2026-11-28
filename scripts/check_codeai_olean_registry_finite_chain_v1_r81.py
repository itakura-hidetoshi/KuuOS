#!/usr/bin/env python3
"""R81: finite registry extension chain with immutable R80 proof delta."""
from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_composable_frontier_v1_r80_r2 as r80
r79=r80.r79
r78=r80.r78
r77=r80.r77
r76=r80.r76
r75=r80.r75
r69=r80.r69
r66=r80.r66
r68=r80.r68
r63=r80.r63
v=r80.v
old=r80.old
transport=r80.transport
ROOT=r80.ROOT
load=r80.load
sha=r80.sha
digest=r80.digest
normalize=r80.normalize
RUN=46149569390
HEAD="d6b8f71c275387995c4f501d6f7dd416379639ae"
DIRECT="055ae7afa150002d346e2f95c106d112015c1b817fcee36d2bc86bd801fc0ac0"
MCP="c6047e9d64f42e2e7a5e188d268cc04656a4fbab31f4b3cef9721103217f9777"
KEY="fd916d85c0fb24d9a4b118a998f4fe7e0288b15e8dae4705fb05d9acc7a4ae59"
PARENT_DIAGNOSTICS="bf7df9174b8346486c860cf448e5e2d074b90a5839de069b59dd3d63613d7410"
PARENT_MANIFEST="a7be856d972878d940de3c9b6c75beeb96d5857b428cfbdc4804b1f4cf09b290"
PARENT_REPLAY="895fba0f0c1062b3b1433d6df781996aba028da64502f2dc4db26a8609821652"
PARENT_OLEAN="3d1cd5d88e9f118e3f10cc2a9e98ec5c75f0491f558da7fa2ba6d7bb49cbc0e4"
PARENT_FILES=[{"name":"ComposableFrontierR80.olean","sha256":PARENT_OLEAN,"bytes":130224}]
SCOPE=r80.SCOPE
BRIDGE=r80.BRIDGE
EXTENSION=r80.EXTENSION
ARTS=[[15265252918,"codeai-olean-r80-r2-independent-46149569390-1","sha256:1eac9f451f698255c80cd8f453214e94e89c936df708ab05438ff45c9e3626eb"],[15264943717,"codeai-olean-r80-r2-local-46149569390-1","sha256:f9f8d916c2eb442803cf14b77541333adfe0234dbd44e861307ee28a0a3cb11c"]]
FILES=r80.FILES+(r80.NEW,)
NEW="registry-finite-chain-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_registry_finite_chain_v1.lean"
NS="KuuOSR81."
MODULE="FiniteChainR81"
IMPORT_DIR=Path("artifacts")/"olean-r81"
IMPORT_MODULE="artifacts.«olean-r81».FiniteChainR81"
SOURCE=MODULE+".lean"
VIEW="McpCapsuleApplication.lean"
VIEW_TEXT="import "+IMPORT_MODULE+"\n"
CAP="audit-capsule"
MANIFEST="r81-audit-capsule.json"
REPLAY="r81-imported-replay.json"
PARENT_CAP="parent-r80-audit-capsule"
R79_CAP=r80.PARENT_CAP
R78_CAP=r80.R78_CAP
R77_CAP=r80.R77_CAP
R76_CAP=r80.R76_CAP
R75_CAP=r80.R75_CAP
BASE_CAP=r80.BASE_CAP
PARENT_FOLDER="parent-r80-receipts"
HIST_RAW=tuple("parent-r"+str(i)+"-raw-replay.json" for i in range(62,81))
FIELDS=r80.FIELDS
STANDARD=r80.STANDARD
GENERAL=("chain_end_extends","chain_end_append","refresh_chain_append","refresh_chain_exact",
         "refresh_chain_one_shot","refresh_chain_frontier_exact")
CONTROL=()
ACTUAL=("actual_finite_chain_exact","actual_finite_frontier_exact")
REFS={"chain_end_extends":["KuuOSR72.extends_trans"],
      "refresh_chain_exact":["KuuOSR80.refresh_set_cache_exact"],
      "refresh_chain_one_shot":[NS+"refresh_chain_exact",NS+"chain_end_extends","KuuOSR80.refresh_set_cache_exact"],
      "refresh_chain_frontier_exact":[NS+"refresh_chain_exact"],
      "actual_finite_chain_exact":[NS+"refresh_chain_exact"],
      "actual_finite_frontier_exact":[NS+"refresh_chain_frontier_exact"]}

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R80 R2 run")
    for jid,steps in ((140993032059,["Verify R80 registry composable frontier","Actual Lean MCP R80 new declarations and exact prior receipt reuse"]),
                      (140994436184,["Independently verify R80 registry composable frontier"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R80 R2 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R80 R2 artifact")
    local,other=a.r80_local,a.r80_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and digest(d)==DIRECT and digest(mp)==MCP and
           mp["status"]=="R80_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R80_INDEPENDENT_COMPOSABLE_FRONTIER_GREEN" and ind["direct_digest"]==DIRECT and
           ind["mcp_digest"]==MCP and ind["mcp_audits"]==403 and
           all(ind[k] is True for k in ("parent_bytes_preserved","raw_new_proofs_equal","composable_frontier_bytes_equal",
                  "actual_computation_bytes_equal","raw_type_and_proof_equal","compiled_file_bytes_equal","imported_replay_equal")) and
           d["parent_source_recompiled"] is False and ind["parent_source_recompiled"] is False and
           d["delta_compilation_count"]==ind["independent_delta_compilation_count"]==1,"R80 exact certified receipts")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==403 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R80 exact declaration inventory")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r80.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           len(record["original_routes"])==2 and len(record["empty_inventory_holds"])==5 and
           record["historical_scope_digest"]==d["historical_scope_digest"]==SCOPE==digest(scope) and
           record["script_bridge_digest"]==d["script_bridge_digest"]==BRIDGE==digest(bridge) and
           record["r69_additive_observation_digest"]==d["r69_additive_observation_digest"]==EXTENSION==digest(extension) and
           all(record[k] is True for k in ("minimal_batch_constructor_proved","candidate_inclusion_minimality_proved","conflict_no_extension_proved","finite_frontier_coverage_proved","equal_binding_set_distinct_route_retained","append_only_residual_exactness_proved","impossible_route_persistence_proved","old_frontier_pruning_counterexample_proved","cached_plan_set_refresh_proved","cached_inventory_order_and_ids_retained","cached_frontier_set_refresh_proved","closed_set_cache_refresh_proved","two_stage_set_cache_composition_proved","two_stage_frontier_composition_proved")) and
           {n:digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R80 exact record")
    v.need(all(d.get(k) is False and record.get(k) is False for k in
           ("proof_authority","action_authority","release_authorized","active_policy_changed",
            "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed",
            "python_general_correctness_proved","live_main_admission","current_main_certification_transferred",
            "registry_updated","batch_applied_to_live_registry","automatic_registration_authority",
            "automatic_recovery_authority","registry_authentication_proved","identity_authentication_proved",
            "unknown_registration_is_refutation","registration_correctness_implied_by_readiness","execution_history_order_independent","cross_route_replacement_proved","search_of_unlisted_routes_complete","ordered_binding_list_refresh_proved","arbitrary_cache_refresh_proved","general_r77_projection_equality_proved")),
           "R80 authority and completeness boundary")
    receipts=out/PARENT_FOLDER;receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","composable-application.lean","composable-computation.lean","composable-computation.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                 r80.SOURCE,r80.VIEW,r80.MANIFEST,r80.REPLAY,"CapsuleObservation.lean",*r80.HIST_RAW):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(load(receipts/"historical-scope.json")==scope and load(receipts/"script-bridge.json")==bridge and
           load(receipts/"script-observation-bridge-r69.json")==extension and
           sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           sha((receipts/"composable-application.lean").read_bytes())==record["application_source_sha256"] and
           sha((receipts/"composable-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"composable-computation.json")==record["actual_computations"],"R80 exact source lineage")
    for label,src in (("sandbox",local),("independent",other)):
        ob=load(src/"main-observations.json")
        r69.observation_pair_valid(scope,ob["before"],ob["after"])
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"R77 base capsule manifest")
        r76.copy_tree_equal(local/folder,other/folder,out/folder)
        v.need(sha((out/folder/(manifest["module"]+".lean")).read_bytes())==manifest["source_sha256"],"R77 base capsule source")
        tool.install(out/folder,manifest)
    for folder in (BASE_CAP,R75_CAP,R76_CAP,R77_CAP,R78_CAP,R79_CAP):
        r76.copy_tree_equal(local/folder,other/folder,out/folder)
    v.need(transport.capsule_files(out/BASE_CAP)==[{"name":"RecoveryDualityR62.olean","sha256":r75.PARENT_OLEAN,"bytes":5972832}],"R77 base compiled identity")
    transport.install(out/BASE_CAP,transport.capsule_files(out/BASE_CAP))
    r75files=[{"name":"RegistryRecoveryR75.olean","sha256":r76.PARENT_OLEAN,"bytes":236464}]
    v.need(r75.module_files(out/R75_CAP)==r75files,"R77 R75 compiled identity")
    r75.install_module(out/R75_CAP,r75files)
    v.need(r76.module_files(out/R76_CAP)==r77.PARENT_FILES,"R78 R76 compiled identity")
    r76.install_module(out/R76_CAP,r77.PARENT_FILES)
    v.need(r77.module_files(out/R77_CAP)==r78.PARENT_FILES,"R79 R77 compiled identity")
    r77.install_module(out/R77_CAP,r78.PARENT_FILES)
    v.need(r78.module_files(out/R78_CAP)==r79.PARENT_FILES,"R80 R78 compiled identity")
    r78.install_module(out/R78_CAP,r79.PARENT_FILES)
    v.need(r79.module_files(out/R79_CAP)==r80.PARENT_FILES,"R81 R79 compiled identity")
    r79.install_module(out/R79_CAP,r80.PARENT_FILES)
    m1,replay1=r80.check_capsule(local,d);m2,replay2=r80.check_capsule(other,d)
    v.need(m1==m2 and digest(m1)==PARENT_MANIFEST and replay1==replay2 and digest(replay1)==PARENT_REPLAY and
           m1["files"]==PARENT_FILES,"R80 exact independently reproduced delta")
    r76.copy_tree_equal(local/r80.CAP,other/r80.CAP,out/PARENT_CAP)
    r80.install_module(out/PARENT_CAP,PARENT_FILES);r80.installed_matches(PARENT_FILES)
    coverage=r80.verify_complete_diagnostics(local,d,mp)
    v.need(digest(coverage)==PARENT_DIAGNOSTICS==ind["diagnostic_coverage_digest"] and
           mp["reused_audit_count"]==395 and mp["new_audit_count"]==8 and len(mp["audit_origins"])==403 and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==PARENT_MANIFEST and
           mp["imported_replay_digest"]==PARENT_REPLAY and mp["fresh_full_source_diagnostics"] is True,"R80 actual MCP receipt")
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json";raw=load(local/name);val=v.structured(raw);origin=mp["audit_origins"][j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha((local/name).read_bytes()),"R80 exact MCP row")
        shutil.copyfile(local/name,receipts/name)
    for i in range(54,80):
        folder="parent-r"+str(i)+"-receipts"
        r76.copy_tree_equal(local/folder,other/folder,out/folder)
    for name in r80.HIST_RAW:
        r63.copy_equal(local/name,other/name,out/name)
    v.save(out/"parent-r80-raw-replay.json",record["raw_theorems"])
    return d,mp,ind,record

def actual_sources(record):
    paths=record["original_routes"]
    idx={"global_boundary":2,"global_default":3,"global_probes":6}
    def key(k):
        return "("+json.dumps(k[0])+ ", "+json.dumps(k[1])+")"
    def basis(case):
        return "((KuuOSR63.cuts_"+str(idx[case])+".map List.toFinset).toFinset)"
    v.need(len(paths)==2 and all(p["path_history_retained"] and p["original_registry_unchanged"] and p["counterfactual_only"] for p in paths),"R81 retained actual routes")
    missing=paths[0]["counterfactual_missing_bindings"]
    v.need(len(missing)==2 and missing[0]["key"]!=missing[1]["key"] and missing[0]["case"]!=missing[1]["case"],"R81 two actual missing bindings")
    k0,k1=key(missing[0]["key"]),key(missing[1]["key"])
    f0,f1=basis(missing[0]["case"]),basis(missing[1]["case"])
    app="\n".join([
        "namespace KuuOSR81",
        "theorem actual_finite_chain_exact",
        "    (reg : (String × String) → Option (KuuOSR69.Basis Nat))",
        "    (updates : List ((String × String) → Option (KuuOSR69.Basis Nat)))",
        "    (h : RegistryChain reg updates) :",
        "    refreshChain (KuuOSR79.setRoutePlans reg KuuOSR77.actualRoutes) updates =",
        "      KuuOSR79.setRoutePlans (chainEnd reg updates) KuuOSR77.actualRoutes :=",
        "  refresh_chain_exact reg KuuOSR77.actualRoutes updates h",
        "theorem actual_finite_frontier_exact",
        "    (reg : (String × String) → Option (KuuOSR69.Basis Nat))",
        "    (updates : List ((String × String) → Option (KuuOSR69.Basis Nat)))",
        "    (h : RegistryChain reg updates) :",
        "    KuuOSR79.setFrontier (KuuOSR79.presentPlans (refreshChain (KuuOSR79.setRoutePlans reg KuuOSR77.actualRoutes) updates)) =",
        "      KuuOSR79.freshSetFrontier (chainEnd reg updates) KuuOSR77.actualRoutes :=",
        "  refresh_chain_frontier_exact reg KuuOSR77.actualRoutes updates h",
        "end KuuOSR81",""])
    compute="\n".join([
        "namespace KuuOSR81","open KuuOSR69 KuuOSR72 KuuOSR76 KuuOSR77 KuuOSR79 KuuOSR80",
        "set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
        "  let reg := KuuOSR71.observedRegistry",
        "  let k0 := "+k0,"  let k1 := "+k1,"  let f0 := "+f0,"  let f1 := "+f1,
        "  let missing := fun k : String × String => if k = k0 ∨ k = k1 then none else reg k",
        "  let midReg := setBinding missing k0 f0",
        "  let lastReg := setBinding midReg k1 f1",
        "  let wrongReg := setBinding missing k0 f1",
        "  let wrongMore := setBinding wrongReg k1 f1",
        "  let initial := setRoutePlans missing actualRoutes",
        "  let steps := [missing,midReg,midReg,lastReg,lastReg]",
        "  let lastRows := refreshChain initial steps",
        "  let directRows := refreshSetCache lastReg initial",
        "  let freshRows := setRoutePlans lastReg actualRoutes",
        "  let chunkRows := refreshChain (refreshChain initial [missing,midReg]) [midReg,lastReg,lastReg]",
        "  let wrongRows := refreshChain initial [wrongReg,wrongMore,wrongMore]",
        "  let wrongFresh := setRoutePlans wrongMore actualRoutes",
        "  let e : Basis Nat := ∅",
        "  let g : Basis Nat := {∅}",
        "  let emptyReg : Nat → Option (Basis Nat) := fun _ => none",
        "  let routes : List (Nat × List (Nat × Basis Nat)) := [(0,[(0,e),(1,e)]),(1,[(0,e)]),(2,[(0,e),(0,g)])]",
        "  let s0 := setRoutePlans emptyReg routes",
        "  let sMidReg := setBinding emptyReg 1 e",
        "  let sLastReg := setBinding sMidReg 0 e",
        "  let sMid := refreshChain s0 [emptyReg,sMidReg,sMidReg]",
        "  let sLast := refreshChain s0 [emptyReg,sMidReg,sMidReg,sLastReg,sLastReg]",
        "  let sDirect := refreshSetCache sLastReg s0",
        "  let sFresh := setRoutePlans sLastReg routes",
        "  let nilRows := refreshChain initial []",
        "  let payload := Lean.Json.mkObj [",
        '    ("actual_nil_exact", Lean.toJson (decide (nilRows.map Prod.fst = initial.map Prod.fst) && decide (nilRows.map Prod.snd = initial.map Prod.snd))),',
        '    ("actual_chain_exact", Lean.toJson (decide (lastRows.map Prod.fst = directRows.map Prod.fst) && decide (lastRows.map Prod.snd = directRows.map Prod.snd))),',
        '    ("actual_fresh_exact", Lean.toJson (decide (lastRows.map Prod.fst = freshRows.map Prod.fst) && decide (lastRows.map Prod.snd = freshRows.map Prod.snd))),',
        '    ("actual_chunk_exact", Lean.toJson (decide (chunkRows.map Prod.fst = lastRows.map Prod.fst) && decide (chunkRows.map Prod.snd = lastRows.map Prod.snd))),',
        '    ("actual_frontier_exact", Lean.toJson (decide (setFrontier (presentPlans lastRows) = freshSetFrontier lastReg actualRoutes))),',
        '    ("actual_empty_not_none", Lean.toJson (decide (lastRows.map Prod.snd = [some ∅,some ∅]))),',
        '    ("actual_conflict_persistence", Lean.toJson (decide (wrongRows.map Prod.fst = wrongFresh.map Prod.fst) && decide (wrongRows.map Prod.snd = wrongFresh.map Prod.snd) && wrongRows.all (fun p => p.2.isNone))),',
        '    ("synthetic_ids_retained", Lean.toJson (decide (sLast.map Prod.fst = [0,1,2]))),',
        '    ("synthetic_tie_restored", Lean.toJson (decide ((setFrontier (presentPlans sMid)).map Prod.fst = [0,1]))),',
        '    ("synthetic_none_retained", Lean.toJson (decide (sLast.map Prod.snd = [some ∅,some ∅,none]))),',
        '    ("synthetic_chain_fresh", Lean.toJson (decide (sLast.map Prod.fst = sDirect.map Prod.fst) && decide (sLast.map Prod.snd = sDirect.map Prod.snd) && decide (sLast.map Prod.fst = sFresh.map Prod.fst) && decide (sLast.map Prod.snd = sFresh.map Prod.snd))),',
        '    ("synthetic_frontier_exact", Lean.toJson (decide (setFrontier (presentPlans sLast) = freshSetFrontier sLastReg routes)))]',
        '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R81_COMPUTE " ++ payload.compress)',
        "end KuuOSR81",""])
    return app,compute

def module_files(folder):
    f=folder/(MODULE+".olean")
    paths=(f,Path(str(f)+".server"),Path(str(f)+".private"))
    present=[p.is_file() and not p.is_symlink() for p in paths]
    v.need(present[0] and present[1]==present[2] and
           {p.name for p in folder.iterdir()}=={p.name for p,ok in zip(paths,present) if ok},
           "R81 complete isolated module parts")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p,ok in zip(paths,present) if ok]

def install_module(folder,files):
    v.need(module_files(folder)==files,"R81 module identity")
    dest=ROOT/".lake/build/lib/lean"/IMPORT_DIR
    dest.mkdir(parents=True,exist_ok=True)
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"R81 module destination collision")
    for item in files:
        p=dest/item["name"]
        with p.open("xb") as f:f.write((folder/item["name"]).read_bytes())
        v.need(sha(p.read_bytes())==item["sha256"],"R81 installed module identity")

def installed_matches(files):
    r80.installed_matches(PARENT_FILES)
    for item in files:
        p=ROOT/".lake/build/lib/lean"/IMPORT_DIR/item["name"]
        v.need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==item["sha256"],"R81 installed module drift")

def expected_raw(out):
    result={}
    for name in HIST_RAW:
        x=load(out/name)
        v.need(not set(x).intersection(result),"R81 duplicate historical proof")
        result.update(x)
    v.need(len(result)==304,"R81 prior full proof count")
    return result

def canonical_raw(x):
    return {**x,"axioms":sorted(set(x["axioms"]))}

def run_lean_with_diagnostics(args,path,source):
    import re
    diagnostic=re.compile(r"(?:\b(?:error|warning)(?:\([^)\r\n]*\))?:|PANIC at |Lean panicked)",re.I)
    def hits(log):
        lines=log.splitlines()
        return lines,[i for i,x in enumerate(lines) if diagnostic.search(x) and not x.startswith(("KUUOS_","@"))]
    try:
        result=r63.r62.r23.run_lean(args,path,source)
        _,bad=hits(result)
        v.need(not bad,"R81 Lean diagnostics including qualified diagnostic codes")
        return result
    except Exception:
        log=path.with_suffix(".log")
        if log.is_file():
            lines,bad=hits(log.read_text(encoding="utf-8"))
            print("R81_R2_RETAINED_DIAGNOSTIC_COUNT",len(bad),flush=True)
            for i in bad:
                for line in lines[i:min(i+30,len(lines))]:
                    if line.startswith(("KUUOS_","@")): break
                    print(line,flush=True)
            if not bad:
                print("R81_R2_RETAINED_LOG_PREFIX",flush=True)
                for line in lines[:25]:
                    if not line.startswith(("KUUOS_","@")):
                        print(line[:2000],flush=True)
        raise

def read_direct_with_dependency_diagnostics(log,selected):
    try:
        return v.read_direct(log,selected)
    except Exception:
        prefix="KUUOS_RECALL_KERNEL "
        expected={x["name"]:set(x["expected_direct_refs"]) for x in selected}
        for line in log.splitlines():
            if line.startswith(prefix):
                row=json.loads(line[len(prefix):])
                absent=sorted(expected.get(row.get("name"),set())-set(row.get("proof_constants",[])))
                if absent:
                    print("KUUOS_R81_MISSING_DIRECT_REFS",json.dumps({"name":row["name"],"missing":absent,"actual":sorted(set(row["proof_constants"]))},sort_keys=True),flush=True)
        raise

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope);extension=r69.additive_bridge(scope,bridge)
    v.need(digest(extension)==EXTENSION,"R81 historical bridge")
    before=r69.observe_live_r3(scope)
    for name,value in (("historical-scope.json",scope),("script-bridge.json",bridge),("script-observation-bridge-r69.json",extension)):
        v.save(out/name,value)
    pd,pm,pi,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding="utf-8");app,compute=actual_sources(parent)
    for name,s in (("formal-source.lean",formal),("finite-application.lean",app),("finite-computation.lean",compute)):
        (out/name).write_text(s,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL+CONTROL+ACTUAL)
    v.need(len(names)==len(set(names))==8,"R81 new theorem inventory")
    expected={NS+n:REFS.get(n,[]) for n in GENERAL+CONTROL+ACTUAL}
    source=r80.VIEW_TEXT+"\n"+formal+"\n"+app+"\n"+compute+"\n"+r76.observer(out,sorted(names))+v.suffix(sorted(names))
    cap=out/CAP;cap.mkdir();p=out/SOURCE
    log=run_lean_with_diagnostics(["--root="+str(ROOT),"-o",str(cap/(MODULE+".olean"))],p,source)
    audit=read_direct_with_dependency_diagnostics(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(names)])
    newraw=r76.raw_audit(log,{x["name"]:x for x in audit},names)
    marker="KUUOS_R81_COMPUTE "
    computations=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    v.need(len(computations)==1 and set(computations[0])=={"actual_nil_exact","actual_chain_exact","actual_fresh_exact","actual_chunk_exact","actual_frontier_exact","actual_empty_not_none","actual_conflict_persistence","synthetic_ids_retained","synthetic_tie_restored","synthetic_none_retained","synthetic_chain_fresh","synthetic_frontier_exact"} and all(x is True for x in computations[0].values()),"R81 actual and synthetic controls")
    v.save(out/"finite-computation.json",computations)
    files=module_files(cap);install_module(cap,files)
    prior_rows=pd["fresh_application"]["observations"]
    all_rows=sorted(prior_rows+audit,key=lambda x:x["name"])
    v.need(len(all_rows)==len({x["name"] for x in all_rows})==411,"R81 accumulated declarations")
    all_names=[x["name"] for x in all_rows]
    all_raw=expected_raw(out);v.need(set(all_raw).isdisjoint(newraw),"R81 no old proof replacement");all_raw.update(newraw)
    v.need(len(all_raw)==312,"R81 complete proof inventory")
    imported_source=VIEW_TEXT+"\n"+r76.observer(out,sorted(all_raw))+v.suffix(all_names)
    ilog=run_lean_with_diagnostics([],out/"CapsuleObservation.lean",imported_source)
    observed=read_direct_with_dependency_diagnostics(ilog,[{"name":x["name"],"expected_direct_refs":x["expected_direct_refs"]} for x in all_rows])
    v.need(len(observed)==411 and [x["name"] for x in observed]==all_names,"R81 all imported names")
    for arow,brow in zip(observed,all_rows):
        v.need(all(arow[k]==brow[k] for k in FIELDS),"R81 imported kernel difference "+brow["name"])
    iraw=r76.raw_audit(ilog,{x["name"]:x for x in observed},all_raw)
    v.need({n:canonical_raw(x) for n,x in iraw.items()}=={n:canonical_raw(x) for n,x in all_raw.items()},"R81 full imported proof equality")
    replay={"observations":[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in observed],
            "raw_proof_digests":{n:digest(canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay);(out/VIEW).write_text(VIEW_TEXT,encoding="utf-8")
    manifest={"schema":"kuuos.codeai.r81.incremental-compiled-proof.v1","module":IMPORT_MODULE,
              "module_path":str(IMPORT_DIR/(MODULE+".olean")),"files":files,
              "parent_module":r80.IMPORT_MODULE,"parent_olean_sha256":PARENT_OLEAN,
              "parent_independent_run":RUN,"parent_imported_replay_digest":PARENT_REPLAY,
              "source_sha256":sha(p.read_bytes()),"view_sha256":sha((out/VIEW).read_bytes()),
              "imported_replay_digest":digest(replay),"imported_audits":411,"imported_complete_proofs":312,
              "parent_source_recompiled":False,"delta_compilation_count":1,"proof_authority":False,"action_authority":False}
    v.save(out/MANIFEST,manifest)
    after=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,before,after)
    v.save(out/"main-observations.json",{"before":before,"after":after})
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved","registry_authentication_proved",
      "unknown_registration_is_refutation","registry_updated","automatic_registration_authority","batch_applied_to_live_registry",
      "registration_correctness_implied_by_readiness","execution_history_order_independent","automatic_recovery_authority",
      "cross_route_replacement_proved","search_of_unlisted_routes_complete","ordered_binding_list_refresh_proved","arbitrary_cache_refresh_proved","general_r77_projection_equality_proved")}
    boundary.update({"minimal_batch_constructor_proved":True,"candidate_inclusion_minimality_proved":True,"conflict_no_extension_proved":True,
      "finite_frontier_coverage_proved":True,"equal_binding_set_distinct_route_retained":True,
      "append_only_residual_exactness_proved":True,"impossible_route_persistence_proved":True,"old_frontier_pruning_counterexample_proved":True,
      "cached_plan_set_refresh_proved":True,"cached_inventory_order_and_ids_retained":True,"cached_frontier_set_refresh_proved":True,
      "closed_set_cache_refresh_proved":True,"two_stage_set_cache_composition_proved":True,"two_stage_frontier_composition_proved":True,
      "finite_chain_endpoint_extension_proved":True,"finite_chain_cache_exactness_proved":True,"finite_chain_chunk_composition_proved":True,"finite_chain_frontier_exactness_proved":True,
      "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
      "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,"future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.registry-finite-chain.v1",
      "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
      "parent_composable_frontier_key":KEY,"r80_direct_digest":DIRECT,"r80_mcp_digest":MCP,"r80_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
      "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
      "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
      "formal_source_sha256":sha(formal.encode()),"application_source_sha256":sha(app.encode()),
      "computation_source_sha256":sha(compute.encode()),"delta_source_sha256":manifest["source_sha256"],
      "original_routes":parent["original_routes"],"actual_computations":computations,
      "empty_inventory_holds":parent["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
      "net_history_collision_retained":True,"original_patch_history_retained":True,
      "raw_theorems":newraw,"formal_observations":{x["name"]:x for x in audit},**boundary})
    v.save(out/NEW,record)
    result={"status":"R81_DIRECT_FINITE_CHAIN","source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
      "parent_composable_frontier_key":KEY,"finite_chain_key":record["key"],"r80_direct_digest":DIRECT,"r80_mcp_digest":MCP,
      "r80_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,"historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,
      "r69_additive_observation_digest":EXTENSION,"capsule_manifest":pd["capsule_manifest"],"joint_capsule_manifest":pd["joint_capsule_manifest"],
      "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,"audit_capsule_digest":digest(manifest),
      "imported_replay_digest":digest(replay),"general_theorems":6,"actual_finite_chain_theorems":2,"actual_path_count":2,
      "empty_inventory_hold_count":5,"actual_computations":computations,"formal_source_sha256":record["formal_source_sha256"],
      "application_source_sha256":record["application_source_sha256"],"computation_source_sha256":record["computation_source_sha256"],
      "delta_source_sha256":manifest["source_sha256"],"new_theorem_names":list(names),
      "new_theorem_axioms":sorted({ax for x in newraw.values() for ax in x["axioms"]}),"raw_theorem_digests":{n:digest(x) for n,x in newraw.items()},
      "parent_source_recompiled":False,"delta_compilation_count":1,"parent_raw_replay_bytewise_equal":True,"imported_complete_proofs":312,
      "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
      "capsule_rebuilds":0,"active_dispatches":0,"new_root_discovery_trials":0,**boundary,
      "fresh_application":{"observations":all_rows,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R81_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest","raw_theorem_digests")}|
        {"direct_digest":digest(result),"audits":len(all_rows)},sort_keys=True),flush=True)
    print("KUUOS_R81_COMPILED",json.dumps(manifest,sort_keys=True),flush=True)
    return result

def check_capsule(out,d):
    m=load(out/MANIFEST);r=load(out/REPLAY)
    v.need(m["schema"]=="kuuos.codeai.r81.incremental-compiled-proof.v1" and m["module"]==IMPORT_MODULE and
           m["module_path"]==str(IMPORT_DIR/(MODULE+".olean")) and m["files"]==module_files(out/CAP) and
           m["parent_olean_sha256"]==PARENT_OLEAN and m["parent_module"]==r80.IMPORT_MODULE and
           m["parent_imported_replay_digest"]==PARENT_REPLAY and m["parent_independent_run"]==RUN and
           m["source_sha256"]==sha((out/SOURCE).read_bytes())==d["delta_source_sha256"] and
           (out/SOURCE).read_bytes()==d["fresh_application"]["mcp_source"].encode() and
           (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m["view_sha256"]==sha((out/VIEW).read_bytes()) and
           digest(m)==d["audit_capsule_digest"] and digest(r)==m["imported_replay_digest"]==d["imported_replay_digest"] and
           m["imported_audits"]==411 and m["imported_complete_proofs"]==312 and
           m["parent_source_recompiled"] is False and m["delta_compilation_count"]==1 and
           m["proof_authority"] is False and m["action_authority"] is False,"R81 exact incremental manifest")
    v.need(r["observations"]==[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in d["fresh_application"]["observations"]],
           "R81 exact imported replay metadata")
    raw=expected_raw(out);raw.update(load(out/NEW)["raw_theorems"])
    v.need(len(raw)==312 and r["raw_proof_digests"]=={n:digest(canonical_raw(x)) for n,x in raw.items()},
           "R81 exact imported complete proof digests")
    return m,r


# R81: exact same full source, separate complete error and warning reports.
# MCP v0.30.0 tools/diagnostics.py calls full-file client.diagnostics before
# applying the severity filter in diagnostic_utils.py. No line or declaration
# range is supplied. Partial reports are never admitted.
DIAG_TIMEOUT=600
DIAG_CLIENT_TIMEOUT=900
DIAG_API_BLOB="fc6e94a4c1798cd18e63cbb59e163eab60247954"
DIAG_PROCESS_BLOB="ebbf0588f1678b953761f470ab060757e87c9708"
DIAG_FILES=(("error","mcp-diagnostics.json"),("warning","mcp-diagnostics-warning.json"))

def complete_diagnostic(raw):
    diag=v.structured(raw)
    return (raw["result"]["isError"] is False and diag["success"] is True and
            diag["partial"] is False and diag["timed_out"] is False and
            not diag.get("still_elaborating_lines") and diag["failed_dependencies"]==[] and diag["items"]==[])

def run_complete_diagnostics(client,rel,out,p):
    sha=r63.r62.r23.sha
    v.need(p.read_bytes()==load(out/"direct.json")["fresh_application"]["mcp_source"].encode(),"R81 exact direct receipt source")
    entries=[]
    for severity,name in DIAG_FILES:
        args={"file_path":rel,"timeout_s":DIAG_TIMEOUT,"severity":severity}
        raw=v.call_tool(client,"lean_diagnostic_messages",args)
        v.save(out/name,raw)
        # Never treat a timeout or filtered error/warning as success.
        diag=v.structured(raw)
        print("KUUOS_R81_DIAGNOSTIC",json.dumps({"severity":severity,"success":diag.get("success"),
             "partial":diag.get("partial"),"timed_out":diag.get("timed_out"),
             "still_elaborating_lines":diag.get("still_elaborating_lines"),
             "item_count":len(diag.get("items",[])),
             "failed_dependencies":diag.get("failed_dependencies")},sort_keys=True),flush=True)
        v.need(complete_diagnostic(raw),"R81 incomplete or non-clean full-source "+severity+" diagnostic")
        entries.append({"severity":severity,"file":name,"request":args,
                        "raw_sha256":sha((out/name).read_bytes())})
    manifest={"schema":"kuuos.codeai.r81.complete-severity-diagnostics.v1",
              "source_sha256":sha(p.read_bytes()),"mcp_version":v.EXPECTED_SERVER_VERSION,
              "full_source":True,"no_line_or_declaration_filter":True,
              "all_error_and_warning_severities":True,"info_and_hint_not_transferred":True,
              "timeout_s_per_call":DIAG_TIMEOUT,"client_timeout_s":DIAG_CLIENT_TIMEOUT,
              "pinned_diagnostics_api_blob":DIAG_API_BLOB,"pinned_diagnostics_processor_blob":DIAG_PROCESS_BLOB,
              "receipts":entries}
    v.save(out/"mcp-diagnostic-coverage.json",manifest)
    return manifest

def verify_complete_diagnostics(first,d,mp):
    sha=r63.r62.r23.sha
    manifest=load(first/"mcp-diagnostic-coverage.json")
    source=(first/SOURCE).read_bytes()
    v.need(source==d["fresh_application"]["mcp_source"].encode() and
           sha(source)==manifest["source_sha256"] and
           mp["diagnostic_coverage_digest"]==old.digest(manifest) and
           mp["diagnostic_scope"]=="full_source_error_and_warning" and
           manifest["schema"]=="kuuos.codeai.r81.complete-severity-diagnostics.v1" and
           manifest["mcp_version"]==v.EXPECTED_SERVER_VERSION and
           manifest["pinned_diagnostics_api_blob"]==DIAG_API_BLOB and
           manifest["pinned_diagnostics_processor_blob"]==DIAG_PROCESS_BLOB and
           manifest["timeout_s_per_call"]==DIAG_TIMEOUT and manifest["client_timeout_s"]==DIAG_CLIENT_TIMEOUT and
           all(manifest[k] is True for k in ("full_source","no_line_or_declaration_filter","all_error_and_warning_severities",
                                            "info_and_hint_not_transferred")) and
           len(manifest["receipts"])==2,"R81 complete diagnostic scope and exact source")
    for entry,(severity,name) in zip(manifest["receipts"],DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r81/FiniteChainR81.lean",
                                  "timeout_s":DIAG_TIMEOUT,"severity":severity} and
               entry["raw_sha256"]==sha((first/name).read_bytes()) and complete_diagnostic(load(first/name)),
               "R81 actual complete full-source diagnostic "+severity)
    return manifest



def mcp(out):
    d=load(out/"direct.json");manifest,replay=check_capsule(out,d)
    installed_matches(manifest["files"])
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==DIRECT and digest(pm)==MCP and pm["direct_digest"]==DIRECT and
           pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R81 certified parent MCP")
    parent_rows={r["name"]:(j,r) for j,r in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==403 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R81 distinct audit inventory")
    p=out/SOURCE
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp"]
    version=v.server_version(cmd,ROOT)
    client=transport.new_client("KuuOS R81 delta source diagnostics")
    try:
        coverage=run_complete_diagnostics(client,str(p.relative_to(ROOT)),out,p)
    finally:
        client.close()
    client=transport.new_client("KuuOS R81 compiled delta axiom audits")
    rows=[];origins=[];rel=str((out/VIEW).relative_to(ROOT))
    try:
        for j,row in enumerate(d["fresh_application"]["observations"]):
            name=row["name"];dest=out/f"mcp-verify-{j}.json"
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(prior==row and d["parent_raw_replay_bytewise_equal"],"R81 exact prior row")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,dest);raw=load(dest)
                origin={"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140993032059,
                        "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":sha(dest.read_bytes())}
            else:
                v.need(name in d["new_theorem_names"],"R81 new audit identity")
                installed_matches(manifest["files"])
                args={"file_path":rel,"theorem_name":name,"scan_source":False}
                print("KUUOS_R81_VERIFY_START",json.dumps(args,sort_keys=True),flush=True)
                raw=client.request("tools/call",{"name":"lean_verify","arguments":args})
                v.save(dest,raw)
                v.need(raw["result"]["isError"] is False,"R81 actual lean_verify failed "+name)
                origin={"name":name,"mode":"fresh_actual_mcp","receipt_sha256":sha(dest.read_bytes()),
                        "request":args,"audit_capsule_digest":digest(manifest),"audit_view_sha256":manifest["view_sha256"]}
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R81 actual MCP audit "+name)
            rows.append({"name":name,"axioms":ax});origins.append(origin)
    finally:
        client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==403 and fresh==8 and len(rows)==411,"R81 exact MCP count")
    installed_matches(manifest["files"])
    result={"status":"R81_REAL_MCP_GREEN","direct_digest":digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_source_scope":"new_delta_module_with_certified_parent_import",
            "diagnostic_coverage_digest":digest(coverage),"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version,
            "audit_transport":"incremental_compiled_import_exact_replay","audit_capsule_digest":digest(manifest),
            "audit_view_sha256":manifest["view_sha256"],"imported_replay_digest":digest(replay)}
    v.save(out/"mcp.json",result)
    print("KUUOS_R81_MCP",json.dumps({"mcp_digest":digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True,
          "audit_transport":result["audit_transport"],"diagnostic_scope":result["diagnostic_source_scope"]},sort_keys=True),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    current,replay=check_capsule(out,d);prior,first_replay=check_capsule(first,a)
    v.need(a==d and prior==current and replay==first_replay and mp["status"]=="R81_REAL_MCP_GREEN" and
           mp["direct_digest"]==digest(d) and mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==403 and
           mp["new_audit_count"]==8 and mp["fresh_full_source_diagnostics"] is True and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==digest(prior) and
           mp["audit_view_sha256"]==prior["view_sha256"] and mp["imported_replay_digest"]==digest(replay) and
           mp["diagnostic_source_scope"]=="new_delta_module_with_certified_parent_import","R81 independent receipt and exact compiled replay")
    coverage=verify_complete_diagnostics(first,d,mp)
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(first/name,out/name)
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(origins)==len(rows)==411,"R81 independent MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        p=first/f"mcp-verify-{j}.json";raw=load(p);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha(p.read_bytes()),
               "R81 actual MCP receipt")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140993032059 and
                   pd["fresh_application"]["observations"][k]==row and origin["prior_origin"]==pm["audit_origins"][k] and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==p.read_bytes(),"R81 reused receipt identity")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"] and
                   origin["request"]=={"file_path":"artifacts/olean-r81/"+VIEW,"theorem_name":row["name"],"scan_source":False} and
                   origin["audit_capsule_digest"]==digest(prior) and origin["audit_view_sha256"]==prior["view_sha256"],
                   "R81 fresh compiled audit identity")
            fresh+=1
    v.need(reused==403 and fresh==8,"R81 independent counts")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        ob=load(folder/"main-observations.json");r69.observation_pair_valid(scope,ob["before"],ob["after"])
    for name in FILES+(NEW,"direct.json","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                       "formal-source.lean","finite-application.lean","finite-computation.lean","finite-computation.json",
                       SOURCE,VIEW,MANIFEST,REPLAY,"CapsuleObservation.lean",*HIST_RAW):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"R81 independent exact bytes "+name)
    for folder in (CAP,PARENT_CAP,R79_CAP,R78_CAP,R77_CAP,R76_CAP,R75_CAP,BASE_CAP,"capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,81))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"R81 parent and compiled bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R81_INDEPENDENT_FINITE_CHAIN_GREEN","direct_digest":digest(d),
        "mcp_digest":digest(mp),"mcp_audits":411,"mcp_new_audits":8,"mcp_reused_audits":403,
        "fresh_full_source_mcp_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
        "diagnostic_source_scope":"new_delta_module_with_certified_parent_import","diagnostic_coverage_digest":digest(coverage),
        "finite_chain_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"compiled_file_bytes_equal":True,
        "imported_replay_equal":True,"parent_source_recompiled":False,"independent_delta_compilation_count":1,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R81_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r80-local","r80-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out==ROOT/"artifacts/olean-r81","R81 exact isolated module path")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
