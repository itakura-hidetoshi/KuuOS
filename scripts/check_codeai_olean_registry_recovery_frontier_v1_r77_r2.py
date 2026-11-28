#!/usr/bin/env python3
"""R77 finite recovery frontier, exact compiled R76 predecessor."""
from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_minimal_recovery_v1_r76_r2 as r76
r75=r76.r75
r69=r76.r69
r66=r76.r66
r68=r76.r68
r63=r76.r63
v=r76.v
old=r76.old
transport=r76.transport
ROOT=r76.ROOT
load=r76.load
sha=r76.sha
digest=r76.digest
normalize=r76.normalize
RUN=46140784873
HEAD="2a0b829a7bf9eb3f5e2f2db1e14ff80deca2e971"
DIRECT="3ed6180b4907a3fd73f2617ddf20ccf95e0fc838321135019c2cf5bac36a0b24"
MCP="025e478a00f555dafce8509c5ab7507e0066187c42e7457b49ab94a17f6cdcdd"
KEY="8ca9d65034e8156d89b788ce41e69fefd4da05a4b1f90c1a71367030fbf070e1"
PARENT_DIAGNOSTICS="2057684a275553a301f29bd5fea9b918a4bcb889c5ec7ade38dfc2e7e1ee9311"
PARENT_MANIFEST="24312703f21cf8130ae60d847122432bcc300156929349ae838c56e7ab7924ac"
PARENT_REPLAY="c82f7f7e88e554b4a352132c59c65694db564d137a5ff6c118f76ebe7d9992b6"
PARENT_OLEAN="8aaedad338fd420887df8bd3166a64af3bc0e165ee78f16abd1b7ffb58a10af2"
PARENT_FILES=[{"name":"MinimalRecoveryR76.olean","sha256":PARENT_OLEAN,"bytes":227592}]
SCOPE=r76.SCOPE
BRIDGE=r76.BRIDGE
EXTENSION=r76.EXTENSION
ARTS=[[15261793490,"codeai-olean-r76-r2-independent-46140784873-1","sha256:f764237fc0ac89bc9f054cfe4e6dc0e5ce59e1031720931b4eb4083310180eee"],[15261388291,"codeai-olean-r76-r2-local-46140784873-1","sha256:81a492675aac97a88c02c6a2b611c221be59f5f13c156cd65c7b80bfea643021"]]
FILES=r76.FILES+(r76.NEW,)
NEW="registry-recovery-frontier-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_registry_recovery_frontier_v1_r2.lean"
NS="KuuOSR77."
MODULE="RecoveryFrontierR77"
IMPORT_DIR=Path("artifacts")/"olean-r77"
IMPORT_MODULE="artifacts.«olean-r77».RecoveryFrontierR77"
SOURCE=MODULE+".lean"
VIEW="McpCapsuleApplication.lean"
VIEW_TEXT="import "+IMPORT_MODULE+"\n"
CAP="audit-capsule"
MANIFEST="r77-audit-capsule.json"
REPLAY="r77-imported-replay.json"
PARENT_CAP="parent-r76-audit-capsule"
R75_CAP=r76.PARENT_CAP
BASE_CAP=r76.BASE_CAP
PARENT_FOLDER="parent-r76-receipts"
HIST_RAW=tuple("parent-r"+str(i)+"-raw-replay.json" for i in range(62,77))
FIELDS=r76.FIELDS
STANDARD=r76.STANDARD
GENERAL=("frontier_mem_iff","frontier_sound","frontier_equal_survives","frontier_covers",
         "frontier_antichain","frontier_exists_iff","checked_candidates_mem_iff",
         "checked_frontier_admits","checked_frontier_covers","checked_frontier_empty_iff")
ACTUAL=("actual_frontier_covers","actual_frontier_admits")
REFS={"frontier_sound":[NS+"frontier_mem_iff"],
      "frontier_equal_survives":[NS+"frontier_mem_iff"],
      "frontier_covers":[NS+"frontier_mem_iff","Nat.find_spec","Finset.card_lt_card"],
      "frontier_antichain":[NS+"frontier_mem_iff",NS+"frontier_sound"],
      "frontier_exists_iff":[NS+"frontier_sound",NS+"frontier_covers"],
      "checked_frontier_admits":[NS+"frontier_sound",NS+"checked_candidates_mem_iff","KuuOSR76.checked_plan_admits"],
      "checked_frontier_covers":[NS+"frontier_covers"],
      "checked_frontier_empty_iff":[NS+"checked_frontier_covers",NS+"checked_frontier_admits",NS+"checked_candidates_mem_iff","KuuOSR76.checked_plan_exists_iff_extension","KuuOSR73.checked_batch_extends"],
      "actual_frontier_covers":[NS+"checked_frontier_covers"],
      "actual_frontier_admits":[NS+"checked_frontier_admits"]}

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R76 R2 run")
    for jid,steps in ((140966006564,["Verify R76 registry minimal recovery","Actual Lean MCP R76 new declarations and exact prior receipt reuse"]),
                      (140967535344,["Independently verify R76 registry minimal recovery"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R76 R2 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R76 R2 artifact")
    local,other=a.r76_local,a.r76_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and digest(d)==DIRECT and digest(mp)==MCP and
           mp["status"]=="R76_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R76_INDEPENDENT_MINIMAL_RECOVERY_GREEN" and ind["direct_digest"]==DIRECT and
           ind["mcp_digest"]==MCP and ind["mcp_audits"]==363 and
           all(ind[k] is True for k in ("parent_bytes_preserved","raw_new_proofs_equal","minimal_recovery_bytes_equal",
                  "actual_computation_bytes_equal","raw_type_and_proof_equal","compiled_file_bytes_equal","imported_replay_equal")) and
           d["parent_source_recompiled"] is False and ind["parent_source_recompiled"] is False and
           d["delta_compilation_count"]==ind["independent_delta_compilation_count"]==1,"R76 exact certified receipts")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==363 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R76 exact declaration inventory")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r76.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           len(record["minimal_recovery_paths"])==2 and len(record["empty_inventory_holds"])==5 and
           record["historical_scope_digest"]==d["historical_scope_digest"]==SCOPE==digest(scope) and
           record["script_bridge_digest"]==d["script_bridge_digest"]==BRIDGE==digest(bridge) and
           record["r69_additive_observation_digest"]==d["r69_additive_observation_digest"]==EXTENSION==digest(extension) and
           all(record[k] is True for k in ("minimal_batch_constructor_proved","candidate_inclusion_minimality_proved","conflict_no_extension_proved")) and
           {n:digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R76 exact record")
    v.need(all(d.get(k) is False and record.get(k) is False for k in
           ("proof_authority","action_authority","release_authorized","active_policy_changed",
            "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed",
            "python_general_correctness_proved","live_main_admission","current_main_certification_transferred",
            "registry_updated","batch_applied_to_live_registry","automatic_registration_authority",
            "automatic_recovery_authority","registry_authentication_proved","identity_authentication_proved",
            "unknown_registration_is_refutation","registration_correctness_implied_by_readiness","execution_history_order_independent")),
           "R76 authority and completeness boundary")
    receipts=out/PARENT_FOLDER;receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","minimal-application.lean","minimal-computation.lean","minimal-computation.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                 r76.SOURCE,r76.VIEW,r76.MANIFEST,r76.REPLAY,"CapsuleObservation.lean",*r76.HIST_RAW):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(load(receipts/"historical-scope.json")==scope and load(receipts/"script-bridge.json")==bridge and
           load(receipts/"script-observation-bridge-r69.json")==extension and
           sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           sha((receipts/"minimal-application.lean").read_bytes())==record["application_source_sha256"] and
           sha((receipts/"minimal-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"minimal-computation.json")==record["minimal_recovery_paths"],"R76 exact source lineage")
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
    for folder in (BASE_CAP,R75_CAP):
        r76.copy_tree_equal(local/folder,other/folder,out/folder)
    v.need(transport.capsule_files(out/BASE_CAP)==[{"name":"RecoveryDualityR62.olean","sha256":r75.PARENT_OLEAN,"bytes":5972832}],"R77 base compiled identity")
    transport.install(out/BASE_CAP,transport.capsule_files(out/BASE_CAP))
    r75files=[{"name":"RegistryRecoveryR75.olean","sha256":r76.PARENT_OLEAN,"bytes":236464}]
    v.need(r75.module_files(out/R75_CAP)==r75files,"R77 R75 compiled identity")
    r75.install_module(out/R75_CAP,r75files)
    m1,replay1=r76.check_capsule(local,d);m2,replay2=r76.check_capsule(other,d)
    v.need(m1==m2 and digest(m1)==PARENT_MANIFEST and replay1==replay2 and digest(replay1)==PARENT_REPLAY and
           m1["files"]==PARENT_FILES,"R76 exact independently reproduced delta")
    r76.copy_tree_equal(local/r76.CAP,other/r76.CAP,out/PARENT_CAP)
    r76.install_module(out/PARENT_CAP,PARENT_FILES);r76.installed_matches(PARENT_FILES)
    coverage=r76.verify_complete_diagnostics(local,d,mp)
    v.need(digest(coverage)==PARENT_DIAGNOSTICS==ind["diagnostic_coverage_digest"] and
           mp["reused_audit_count"]==344 and mp["new_audit_count"]==19 and len(mp["audit_origins"])==363 and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==PARENT_MANIFEST and
           mp["imported_replay_digest"]==PARENT_REPLAY and mp["fresh_full_source_diagnostics"] is True,"R76 actual MCP receipt")
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json";raw=load(local/name);val=v.structured(raw);origin=mp["audit_origins"][j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha((local/name).read_bytes()),"R76 exact MCP row")
        shutil.copyfile(local/name,receipts/name)
    for i in range(54,76):
        folder="parent-r"+str(i)+"-receipts"
        r76.copy_tree_equal(local/folder,other/folder,out/folder)
    for name in r76.HIST_RAW:
        r63.copy_equal(local/name,other/name,out/name)
    v.save(out/"parent-r76-raw-replay.json",record["raw_theorems"])
    return d,mp,ind,record

def actual_sources(record):
    paths=record["minimal_recovery_paths"]
    idx={"global_boundary":2,"global_default":3,"global_probes":6}
    def key(k):
        return "("+json.dumps(k[0])+", "+json.dumps(k[1])+")"
    def basis(case):
        return "((KuuOSR63.cuts_"+str(idx[case])+".map List.toFinset).toFinset)"
    def binding(b):
        return "("+key(b["key"])+", "+basis(b["case"])+")"
    registry=paths[0]["original_registry"]
    actual_set={(tuple(x["key"]),x["case"]) for x in registry}
    v.need(len(registry)==len(actual_set)==3 and len(paths)==2,"R77 exact parent route inventory")
    rows=[]
    for i,p in enumerate(paths):
        req=p["required_bindings_occurrences"]
        v.need(p["index"]==i and p["original_registry"]==registry and p["path_history_retained"] is True and
               p["counterfactual_only"] is True and p["original_registry_unchanged"] is True and
               {(tuple(x["key"]),x["case"]) for x in req}==actual_set and
               p["lean_computation"]["all_missing_three"] is True,"R77 parent requirement identities")
        rows.append("("+str(i)+", ["+", ".join(binding(x) for x in req)+"])")
    ty="List ((String × String) × KuuOSR69.Basis Nat)"
    app="\n".join([
        "namespace KuuOSR77",
        "def actualRoutes : List (Nat × "+ty+") := ["+", ".join(rows)+"]",
        "theorem actual_frontier_covers",
        "    (reg : (String × String) → Option (KuuOSR69.Basis Nat)) (p : Nat × "+ty+")",
        "    (hp : p ∈ checkedCandidates reg actualRoutes) :",
        "    ∃ q ∈ checkedFrontier reg actualRoutes, q.2.toFinset ⊆ p.2.toFinset :=",
        "  checked_frontier_covers reg actualRoutes p hp",
        "theorem actual_frontier_admits",
        "    (reg : (String × String) → Option (KuuOSR69.Basis Nat)) (p : Nat × "+ty+")",
        "    (hp : p ∈ checkedFrontier reg actualRoutes) :",
        "    ∃ r ∈ actualRoutes, r.1 = p.1 ∧ ∃ next, KuuOSR73.checkedBatch reg p.2 = some next ∧ KuuOSR75.CoversBindings next r.2 :=",
        "  checked_frontier_admits reg actualRoutes p hp",
        "end KuuOSR77",""])
    missing=paths[0]["counterfactual_missing_bindings"]
    v.need(len(missing)==2 and missing[0]["key"]!=missing[1]["key"] and missing[0]["case"]!=missing[1]["case"],"R77 nontrivial controls")
    k0,k1=key(missing[0]["key"]),key(missing[1]["key"])
    restore="["+", ".join(binding(x) for x in missing)+"]"
    compute="\n".join([
        "namespace KuuOSR77","set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
        "  let reg := KuuOSR71.observedRegistry",
        "  let k0 := "+k0,"  let k1 := "+k1,
        "  let missing := fun k : String × String => if k = k0 ∨ k = k1 then none else reg k",
        "  let one := fun k : String × String => if k = k0 then none else reg k",
        "  let absent : (String × String) → Option (KuuOSR69.Basis Nat) := fun _ => none",
        "  let conflict := KuuOSR72.setBinding reg k0 "+basis(missing[1]["case"]),
        "  let restore : "+ty+" := "+restore,
        "  let base := checkedFrontier reg actualRoutes",
        "  let two := checkedFrontier missing actualRoutes",
        "  let single := checkedFrontier one actualRoutes",
        "  let allPlans := checkedFrontier absent actualRoutes",
        "  let bad := checkedFrontier conflict actualRoutes",
        "  let synthetic : List (Nat × List Nat) := [(0,[0,1]),(1,[0]),(2,[2]),(3,[0,0])]",
        "  let payload := Lean.Json.mkObj [",
        '    ("baseline_ids", Lean.toJson (decide (base.map Prod.fst = [0,1]))),',
        '    ("baseline_empty", Lean.toJson (base.all (fun p => p.2.isEmpty))),',
        '    ("two_missing_ids", Lean.toJson (decide (two.map Prod.fst = [0,1]))),',
        '    ("two_missing_exact", Lean.toJson (decide (two.map (fun p => p.2.toFinset) = [restore.toFinset,restore.toFinset]))),',
        '    ("single_missing_ids", Lean.toJson (decide (single.map Prod.fst = [0,1]))),',
        '    ("single_missing_count", Lean.toJson (decide (single.map (fun p => p.2.length) = [1,1]))),',
        '    ("all_missing_ids", Lean.toJson (decide (allPlans.map Prod.fst = [0,1]))),',
        '    ("all_missing_count", Lean.toJson (decide (allPlans.map (fun p => p.2.length) = [3,3]))),',
        '    ("conflict_no_candidate", Lean.toJson bad.isEmpty),',
        '    ("strict_and_incomparable_and_equal", Lean.toJson (decide ((frontier synthetic).map Prod.fst = [1,2,3]))),',
        '    ("empty_dominates", Lean.toJson (decide ((frontier (synthetic ++ [(4,[])])).map Prod.fst = [4])))]',
        '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R77_COMPUTE " ++ payload.compress)',
        "end KuuOSR77",""])
    return app,compute

def module_files(folder):
    f=folder/(MODULE+".olean")
    paths=(f,Path(str(f)+".server"),Path(str(f)+".private"))
    present=[p.is_file() and not p.is_symlink() for p in paths]
    v.need(present[0] and present[1]==present[2] and
           {p.name for p in folder.iterdir()}=={p.name for p,ok in zip(paths,present) if ok},
           "R77 complete isolated module parts")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p,ok in zip(paths,present) if ok]

def install_module(folder,files):
    v.need(module_files(folder)==files,"R77 module identity")
    dest=ROOT/".lake/build/lib/lean"/IMPORT_DIR
    dest.mkdir(parents=True,exist_ok=True)
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"R77 module destination collision")
    for item in files:
        p=dest/item["name"]
        with p.open("xb") as f:f.write((folder/item["name"]).read_bytes())
        v.need(sha(p.read_bytes())==item["sha256"],"R77 installed module identity")

def installed_matches(files):
    r76.installed_matches(PARENT_FILES)
    for item in files:
        p=ROOT/".lake/build/lib/lean"/IMPORT_DIR/item["name"]
        v.need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==item["sha256"],"R77 installed module drift")

def expected_raw(out):
    result={}
    for name in HIST_RAW:
        x=load(out/name)
        v.need(not set(x).intersection(result),"R77 duplicate historical proof")
        result.update(x)
    v.need(len(result)==264,"R77 prior full proof count")
    return result

def canonical_raw(x):
    return {**x,"axioms":sorted(set(x["axioms"]))}

def run_lean_with_diagnostics(args,path,source):
    try:
        return r63.r62.r23.run_lean(args,path,source)
    except Exception:
        log=path.with_suffix(".log")
        if log.is_file():
            import re
            lines=log.read_text(encoding="utf-8").splitlines()
            hits=[i for i,x in enumerate(lines) if re.search(r"(?:\berror:|\bwarning:|PANIC at |Lean panicked)",x,re.I) and not x.startswith(("KUUOS_","@"))]
            print("R77_R2_RETAINED_DIAGNOSTIC_COUNT",len(hits),flush=True)
            for i in hits:
                for line in lines[i:min(i+30,len(lines))]:
                    if line.startswith(("KUUOS_","@")): break
                    print(line,flush=True)
        raise

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope);extension=r69.additive_bridge(scope,bridge)
    v.need(digest(extension)==EXTENSION,"R77 historical bridge")
    before=r69.observe_live_r3(scope)
    for name,value in (("historical-scope.json",scope),("script-bridge.json",bridge),("script-observation-bridge-r69.json",extension)):
        v.save(out/name,value)
    pd,pm,pi,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding="utf-8");app,compute=actual_sources(parent)
    for name,s in (("formal-source.lean",formal),("frontier-application.lean",app),("frontier-computation.lean",compute)):
        (out/name).write_text(s,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL+ACTUAL)
    v.need(len(names)==len(set(names))==12,"R77 new theorem inventory")
    expected={NS+n:REFS.get(n,[]) for n in GENERAL+ACTUAL}
    source=r76.VIEW_TEXT+"\n"+formal+"\n"+app+"\n"+compute+"\n"+r76.observer(out,sorted(names))+v.suffix(sorted(names))
    cap=out/CAP;cap.mkdir();p=out/SOURCE
    log=run_lean_with_diagnostics(["--root="+str(ROOT),"-o",str(cap/(MODULE+".olean"))],p,source)
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(names)])
    newraw=r76.raw_audit(log,{x["name"]:x for x in audit},names)
    marker="KUUOS_R77_COMPUTE "
    computations=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    v.need(len(computations)==1 and set(computations[0])=={"baseline_ids","baseline_empty","two_missing_ids","two_missing_exact",
           "single_missing_ids","single_missing_count","all_missing_ids","all_missing_count","conflict_no_candidate",
           "strict_and_incomparable_and_equal","empty_dominates"} and all(x is True for x in computations[0].values()),"R77 actual and synthetic controls")
    v.save(out/"frontier-computation.json",computations)
    files=module_files(cap);install_module(cap,files)
    prior_rows=pd["fresh_application"]["observations"]
    all_rows=sorted(prior_rows+audit,key=lambda x:x["name"])
    v.need(len(all_rows)==len({x["name"] for x in all_rows})==375,"R77 accumulated declarations")
    all_names=[x["name"] for x in all_rows]
    all_raw=expected_raw(out);v.need(set(all_raw).isdisjoint(newraw),"R77 no old proof replacement");all_raw.update(newraw)
    v.need(len(all_raw)==276,"R77 complete proof inventory")
    imported_source=VIEW_TEXT+"\n"+r76.observer(out,sorted(all_raw))+v.suffix(all_names)
    ilog=run_lean_with_diagnostics([],out/"CapsuleObservation.lean",imported_source)
    observed=v.read_direct(ilog,[{"name":x["name"],"expected_direct_refs":x["expected_direct_refs"]} for x in all_rows])
    v.need(len(observed)==375 and [x["name"] for x in observed]==all_names,"R77 all imported names")
    for arow,brow in zip(observed,all_rows):
        v.need(all(arow[k]==brow[k] for k in FIELDS),"R77 imported kernel difference "+brow["name"])
    iraw=r76.raw_audit(ilog,{x["name"]:x for x in observed},all_raw)
    v.need({n:canonical_raw(x) for n,x in iraw.items()}=={n:canonical_raw(x) for n,x in all_raw.items()},"R77 full imported proof equality")
    replay={"observations":[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in observed],
            "raw_proof_digests":{n:digest(canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay);(out/VIEW).write_text(VIEW_TEXT,encoding="utf-8")
    manifest={"schema":"kuuos.codeai.r77.incremental-compiled-proof.v1","module":IMPORT_MODULE,
              "module_path":str(IMPORT_DIR/(MODULE+".olean")),"files":files,
              "parent_module":r76.IMPORT_MODULE,"parent_olean_sha256":PARENT_OLEAN,
              "parent_independent_run":RUN,"parent_imported_replay_digest":PARENT_REPLAY,
              "source_sha256":sha(p.read_bytes()),"view_sha256":sha((out/VIEW).read_bytes()),
              "imported_replay_digest":digest(replay),"imported_audits":375,"imported_complete_proofs":276,
              "parent_source_recompiled":False,"delta_compilation_count":1,"proof_authority":False,"action_authority":False}
    v.save(out/MANIFEST,manifest)
    after=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,before,after)
    v.save(out/"main-observations.json",{"before":before,"after":after})
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved","registry_authentication_proved",
      "unknown_registration_is_refutation","registry_updated","automatic_registration_authority","batch_applied_to_live_registry",
      "registration_correctness_implied_by_readiness","execution_history_order_independent","automatic_recovery_authority",
      "cross_route_replacement_proved","search_of_unlisted_routes_complete")}
    boundary.update({"minimal_batch_constructor_proved":True,"candidate_inclusion_minimality_proved":True,"conflict_no_extension_proved":True,
      "finite_frontier_coverage_proved":True,"equal_binding_set_distinct_route_retained":True,
      "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
      "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,"future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.registry-recovery-frontier.v1",
      "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
      "parent_minimal_recovery_path_key":KEY,"r76_direct_digest":DIRECT,"r76_mcp_digest":MCP,"r76_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
      "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
      "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
      "formal_source_sha256":sha(formal.encode()),"application_source_sha256":sha(app.encode()),
      "computation_source_sha256":sha(compute.encode()),"delta_source_sha256":manifest["source_sha256"],
      "original_routes":parent["minimal_recovery_paths"],"actual_computations":computations,
      "empty_inventory_holds":parent["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
      "net_history_collision_retained":True,"original_patch_history_retained":True,
      "raw_theorems":newraw,"formal_observations":{x["name"]:x for x in audit},**boundary})
    v.save(out/NEW,record)
    result={"status":"R77_DIRECT_RECOVERY_FRONTIER","source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
      "parent_minimal_recovery_path_key":KEY,"recovery_frontier_key":record["key"],"r76_direct_digest":DIRECT,"r76_mcp_digest":MCP,
      "r76_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,"historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,
      "r69_additive_observation_digest":EXTENSION,"capsule_manifest":pd["capsule_manifest"],"joint_capsule_manifest":pd["joint_capsule_manifest"],
      "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,"audit_capsule_digest":digest(manifest),
      "imported_replay_digest":digest(replay),"general_theorems":10,"actual_frontier_theorems":2,"actual_path_count":2,
      "empty_inventory_hold_count":5,"actual_computations":computations,"formal_source_sha256":record["formal_source_sha256"],
      "application_source_sha256":record["application_source_sha256"],"computation_source_sha256":record["computation_source_sha256"],
      "delta_source_sha256":manifest["source_sha256"],"new_theorem_names":list(names),
      "new_theorem_axioms":sorted({ax for x in newraw.values() for ax in x["axioms"]}),"raw_theorem_digests":{n:digest(x) for n,x in newraw.items()},
      "parent_source_recompiled":False,"delta_compilation_count":1,"parent_raw_replay_bytewise_equal":True,"imported_complete_proofs":276,
      "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
      "capsule_rebuilds":0,"active_dispatches":0,"new_root_discovery_trials":0,**boundary,
      "fresh_application":{"observations":all_rows,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R77_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest","raw_theorem_digests")}|
        {"direct_digest":digest(result),"audits":len(all_rows)},sort_keys=True),flush=True)
    print("KUUOS_R77_COMPILED",json.dumps(manifest,sort_keys=True),flush=True)
    return result

def check_capsule(out,d):
    m=load(out/MANIFEST);r=load(out/REPLAY)
    v.need(m["schema"]=="kuuos.codeai.r77.incremental-compiled-proof.v1" and m["module"]==IMPORT_MODULE and
           m["module_path"]==str(IMPORT_DIR/(MODULE+".olean")) and m["files"]==module_files(out/CAP) and
           m["parent_olean_sha256"]==PARENT_OLEAN and m["parent_module"]==r76.IMPORT_MODULE and
           m["parent_imported_replay_digest"]==PARENT_REPLAY and m["parent_independent_run"]==RUN and
           m["source_sha256"]==sha((out/SOURCE).read_bytes())==d["delta_source_sha256"] and
           (out/SOURCE).read_bytes()==d["fresh_application"]["mcp_source"].encode() and
           (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m["view_sha256"]==sha((out/VIEW).read_bytes()) and
           digest(m)==d["audit_capsule_digest"] and digest(r)==m["imported_replay_digest"]==d["imported_replay_digest"] and
           m["imported_audits"]==375 and m["imported_complete_proofs"]==276 and
           m["parent_source_recompiled"] is False and m["delta_compilation_count"]==1 and
           m["proof_authority"] is False and m["action_authority"] is False,"R77 exact incremental manifest")
    v.need(r["observations"]==[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in d["fresh_application"]["observations"]],
           "R77 exact imported replay metadata")
    raw=expected_raw(out);raw.update(load(out/NEW)["raw_theorems"])
    v.need(len(raw)==276 and r["raw_proof_digests"]=={n:digest(canonical_raw(x)) for n,x in raw.items()},
           "R77 exact imported complete proof digests")
    return m,r


# R77: exact same full source, separate complete error and warning reports.
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
    v.need(p.read_bytes()==load(out/"direct.json")["fresh_application"]["mcp_source"].encode(),"R77 exact direct receipt source")
    entries=[]
    for severity,name in DIAG_FILES:
        args={"file_path":rel,"timeout_s":DIAG_TIMEOUT,"severity":severity}
        raw=v.call_tool(client,"lean_diagnostic_messages",args)
        v.save(out/name,raw)
        # Never treat a timeout or filtered error/warning as success.
        diag=v.structured(raw)
        print("KUUOS_R77_DIAGNOSTIC",json.dumps({"severity":severity,"success":diag.get("success"),
             "partial":diag.get("partial"),"timed_out":diag.get("timed_out"),
             "still_elaborating_lines":diag.get("still_elaborating_lines"),
             "item_count":len(diag.get("items",[])),
             "failed_dependencies":diag.get("failed_dependencies")},sort_keys=True),flush=True)
        v.need(complete_diagnostic(raw),"R77 incomplete or non-clean full-source "+severity+" diagnostic")
        entries.append({"severity":severity,"file":name,"request":args,
                        "raw_sha256":sha((out/name).read_bytes())})
    manifest={"schema":"kuuos.codeai.r77.complete-severity-diagnostics.v1",
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
           manifest["schema"]=="kuuos.codeai.r77.complete-severity-diagnostics.v1" and
           manifest["mcp_version"]==v.EXPECTED_SERVER_VERSION and
           manifest["pinned_diagnostics_api_blob"]==DIAG_API_BLOB and
           manifest["pinned_diagnostics_processor_blob"]==DIAG_PROCESS_BLOB and
           manifest["timeout_s_per_call"]==DIAG_TIMEOUT and manifest["client_timeout_s"]==DIAG_CLIENT_TIMEOUT and
           all(manifest[k] is True for k in ("full_source","no_line_or_declaration_filter","all_error_and_warning_severities",
                                            "info_and_hint_not_transferred")) and
           len(manifest["receipts"])==2,"R77 complete diagnostic scope and exact source")
    for entry,(severity,name) in zip(manifest["receipts"],DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r77/RecoveryFrontierR77.lean",
                                  "timeout_s":DIAG_TIMEOUT,"severity":severity} and
               entry["raw_sha256"]==sha((first/name).read_bytes()) and complete_diagnostic(load(first/name)),
               "R77 actual complete full-source diagnostic "+severity)
    return manifest



def mcp(out):
    d=load(out/"direct.json");manifest,replay=check_capsule(out,d)
    installed_matches(manifest["files"])
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==DIRECT and digest(pm)==MCP and pm["direct_digest"]==DIRECT and
           pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R77 certified parent MCP")
    parent_rows={r["name"]:(j,r) for j,r in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==363 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R77 distinct audit inventory")
    p=out/SOURCE
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp"]
    version=v.server_version(cmd,ROOT)
    client=transport.new_client("KuuOS R77 delta source diagnostics")
    try:
        coverage=run_complete_diagnostics(client,str(p.relative_to(ROOT)),out,p)
    finally:
        client.close()
    client=transport.new_client("KuuOS R77 compiled delta axiom audits")
    rows=[];origins=[];rel=str((out/VIEW).relative_to(ROOT))
    try:
        for j,row in enumerate(d["fresh_application"]["observations"]):
            name=row["name"];dest=out/f"mcp-verify-{j}.json"
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(prior==row and d["parent_raw_replay_bytewise_equal"],"R77 exact prior row")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,dest);raw=load(dest)
                origin={"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140966006564,
                        "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":sha(dest.read_bytes())}
            else:
                v.need(name in d["new_theorem_names"],"R77 new audit identity")
                installed_matches(manifest["files"])
                args={"file_path":rel,"theorem_name":name,"scan_source":False}
                print("KUUOS_R77_VERIFY_START",json.dumps(args,sort_keys=True),flush=True)
                raw=client.request("tools/call",{"name":"lean_verify","arguments":args})
                v.save(dest,raw)
                v.need(raw["result"]["isError"] is False,"R77 actual lean_verify failed "+name)
                origin={"name":name,"mode":"fresh_actual_mcp","receipt_sha256":sha(dest.read_bytes()),
                        "request":args,"audit_capsule_digest":digest(manifest),"audit_view_sha256":manifest["view_sha256"]}
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R77 actual MCP audit "+name)
            rows.append({"name":name,"axioms":ax});origins.append(origin)
    finally:
        client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==363 and fresh==12 and len(rows)==375,"R77 exact MCP count")
    installed_matches(manifest["files"])
    result={"status":"R77_REAL_MCP_GREEN","direct_digest":digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_source_scope":"new_delta_module_with_certified_parent_import",
            "diagnostic_coverage_digest":digest(coverage),"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version,
            "audit_transport":"incremental_compiled_import_exact_replay","audit_capsule_digest":digest(manifest),
            "audit_view_sha256":manifest["view_sha256"],"imported_replay_digest":digest(replay)}
    v.save(out/"mcp.json",result)
    print("KUUOS_R77_MCP",json.dumps({"mcp_digest":digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True,
          "audit_transport":result["audit_transport"],"diagnostic_scope":result["diagnostic_source_scope"]},sort_keys=True),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    current,replay=check_capsule(out,d);prior,first_replay=check_capsule(first,a)
    v.need(a==d and prior==current and replay==first_replay and mp["status"]=="R77_REAL_MCP_GREEN" and
           mp["direct_digest"]==digest(d) and mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==363 and
           mp["new_audit_count"]==12 and mp["fresh_full_source_diagnostics"] is True and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==digest(prior) and
           mp["audit_view_sha256"]==prior["view_sha256"] and mp["imported_replay_digest"]==digest(replay) and
           mp["diagnostic_source_scope"]=="new_delta_module_with_certified_parent_import","R77 independent receipt and exact compiled replay")
    coverage=verify_complete_diagnostics(first,d,mp)
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(first/name,out/name)
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(origins)==len(rows)==375,"R77 independent MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        p=first/f"mcp-verify-{j}.json";raw=load(p);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha(p.read_bytes()),
               "R77 actual MCP receipt")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140966006564 and
                   pd["fresh_application"]["observations"][k]==row and origin["prior_origin"]==pm["audit_origins"][k] and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==p.read_bytes(),"R77 reused receipt identity")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"] and
                   origin["request"]=={"file_path":"artifacts/olean-r77/"+VIEW,"theorem_name":row["name"],"scan_source":False} and
                   origin["audit_capsule_digest"]==digest(prior) and origin["audit_view_sha256"]==prior["view_sha256"],
                   "R77 fresh compiled audit identity")
            fresh+=1
    v.need(reused==363 and fresh==12,"R77 independent counts")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        ob=load(folder/"main-observations.json");r69.observation_pair_valid(scope,ob["before"],ob["after"])
    for name in FILES+(NEW,"direct.json","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                       "formal-source.lean","frontier-application.lean","frontier-computation.lean","frontier-computation.json",
                       SOURCE,VIEW,MANIFEST,REPLAY,"CapsuleObservation.lean",*HIST_RAW):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"R77 independent exact bytes "+name)
    for folder in (CAP,PARENT_CAP,R75_CAP,BASE_CAP,"capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,77))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"R77 parent and compiled bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R77_INDEPENDENT_RECOVERY_FRONTIER_GREEN","direct_digest":digest(d),
        "mcp_digest":digest(mp),"mcp_audits":375,"mcp_new_audits":12,"mcp_reused_audits":363,
        "fresh_full_source_mcp_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
        "diagnostic_source_scope":"new_delta_module_with_certified_parent_import","diagnostic_coverage_digest":digest(coverage),
        "recovery_frontier_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"compiled_file_bytes_equal":True,
        "imported_replay_equal":True,"parent_source_recompiled":False,"independent_delta_compilation_count":1,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R77_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r76-local","r76-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out==ROOT/"artifacts/olean-r77","R77 exact isolated module path")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
