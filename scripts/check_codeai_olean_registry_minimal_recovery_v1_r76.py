#!/usr/bin/env python3
"""R76: least checked recovery batch over exact compiled predecessor chain."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_recovery_v1_r75 as r75
transport=r75.transport
r74=r75.r74
r73=r74.r73
r72=r73.r72
r71=r72.r71
r70=r71.r70
r69=r70.r69
from check_codeai_no_go_memory_v1_r2 import normalize
r68=r69.r68
r67=r69.r67
r66=r69.r66
r65=r69.r65
r64=r69.r64
r63=r69.r63
v=r69.v
old=r69.old
ROOT=r69.ROOT
load=r69.load
RUN=46137870754
HEAD="9fd9c44d42e0f92f6ff56e1f50acad35a2ac6886"
DIRECT="48b2af053f08233da6354c8d9e7b539d4cec5e96da535a7e4308698c0c24957d"
MCP="eb9fba38f4698d6a7fb92f8534c4bed13d96c5ccb99866da84fbf5f20d060a2b"
KEY="3617f6c209d122d5b2499a27d05fcd3808a40821de9cdc2aba99fd21a6db924e"
PARENT_DIAGNOSTICS="9c019f84a3a46479293809f0ff1031811c7b74c24f22330a5d8793547a0699cc"
PARENT_REPLAY="d212c3295102059938ed640858c6cb1e937256e23ec02f69021c86e5d997c0d2"
PARENT_MANIFEST="72267a67f260cf9c21119d852ea65301b75e06f235ce211d1ab438c8773bc933"
PARENT_OLEAN="57dd980679db8423c38db77d68af400b7cbdbf118b00e471750272c68184bfa4"
SCOPE=r69.SCOPE
BRIDGE=r69.BRIDGE
EXTENSION="e8bed0fde1244c49b7194db383a8516418ee2950adaa5ff5233997b5672d626d"
ARTS=((15259794856,"codeai-olean-r76-r2-local-46137870754-1","sha256:0527df172eb78a5d85caf4d9639f5cec6aef61084686c5dffbc52324a5c3b505"),
      (15261111220,"codeai-olean-r76-r2-independent-46137870754-1","sha256:fdf015349bf4410a6b085d69357469025cb7d062c93775d4a38831f631482101"))
FILES=r75.FILES+(r75.NEW,)
NEW="registry-minimal-recovery-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_registry_minimal_recovery_v1.lean"
NS="KuuOSR76."
sha=r63.r62.r23.sha
digest=old.digest
MODULE="MinimalRecoveryR76"
IMPORT_MODULE="artifacts.«olean-r76».MinimalRecoveryR76"
IMPORT_DIR=Path("artifacts")/"olean-r76"
SOURCE=MODULE+".lean"
VIEW="McpCapsuleApplication.lean"
VIEW_TEXT="import "+IMPORT_MODULE+"\n"
CAP="audit-capsule"
MANIFEST="r76-audit-capsule.json"
REPLAY="r76-imported-replay.json"
PARENT_CAP="parent-r75-audit-capsule"
BASE_CAP=r75.PARENT_CAP
PARENT_FOLDER="parent-r75-receipts"
FIELDS=transport.FIELDS
STANDARD={"Classical.choice","Quot.sound","propext"}
HIST_RAW=tuple("parent-r"+str(i)+"-raw-replay.json" for i in range(62,76))
GENERAL=("compatibility_check_iff","consistency_check_iff","minimal_batch_mem","minimal_batch_ready",
         "minimal_batch_supplies","checked_plan_some_iff","checked_plan_admits","recovering_batch_contains_minimal",
         "checked_plan_minimal","extension_conditions","checked_plan_exists_iff_extension",
         "checked_plan_none_iff_no_extension","checked_plan_path_recovers","checked_plan_conflict_hold",
         "checked_plan_inconsistent_hold")
REFS={
 "minimal_batch_mem":["List.mem_dedup","KuuOSR75.missing_binding_iff"],
 "minimal_batch_ready":[NS+"minimal_batch_mem","List.nodup_dedup","List.Nodup.map_on"],
 "minimal_batch_supplies":[NS+"minimal_batch_mem"],
 "checked_plan_some_iff":[NS+"compatibility_check_iff",NS+"consistency_check_iff"],
 "checked_plan_admits":[NS+"checked_plan_some_iff","KuuOSR74.checked_batch_exists",
    NS+"minimal_batch_ready","KuuOSR75.requirements_after_batch_iff",NS+"minimal_batch_supplies"],
 "recovering_batch_contains_minimal":[NS+"minimal_batch_mem","KuuOSR75.requirements_after_batch_iff"],
 "checked_plan_minimal":[NS+"checked_plan_some_iff",NS+"recovering_batch_contains_minimal"],
 "extension_conditions":["KuuOSR71.registered_binding_unique"],
 "checked_plan_exists_iff_extension":[NS+"checked_plan_admits","KuuOSR73.checked_batch_extends",NS+"extension_conditions",NS+"checked_plan_some_iff"],
 "checked_plan_none_iff_no_extension":[NS+"checked_plan_exists_iff_extension"],
 "checked_plan_path_recovers":[NS+"checked_plan_admits","KuuOSR72.recovery_iff_of_tagged","KuuOSR75.required_bindings_iff"],
 "checked_plan_conflict_hold":[NS+"checked_plan_none_iff_no_extension","KuuOSR75.conflicting_requirement_no_extension"],
 "checked_plan_inconsistent_hold":[NS+"checked_plan_none_iff_no_extension","KuuOSR75.inconsistent_requirements_no_registry"],
}

def copy_tree_equal(left,right,target):
    a=sorted(str(x.relative_to(left)) for x in left.rglob("*") if x.is_file())
    b=sorted(str(x.relative_to(right)) for x in right.rglob("*") if x.is_file())
    v.need(bool(a) and a==b,"R76 complete parent directory inventory "+str(target))
    for name in a:
        r63.copy_equal(left/name,right/name,target/name)

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R75 R2 run")
    for jid,steps in ((140957113907,["Verify R75 R2 registry recovery obligations","Actual Lean MCP R75 R2 new declarations and exact prior receipt reuse"]),
                      (140958630449,["Independently verify R75 R2 registry recovery obligations"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),
               "R75 R2 job completion")
    for aid,name,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==name and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R75 R2 artifact")
    local,other=a.r75_local,a.r75_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and digest(d)==DIRECT and digest(mp)==MCP and
           mp["status"]=="R75_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R75_INDEPENDENT_RECOVERY_OBLIGATIONS_GREEN" and ind["direct_digest"]==DIRECT and
           ind["mcp_digest"]==MCP and ind["mcp_audits"]==344 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","recovery_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal","compiled_file_bytes_equal",
                                "imported_replay_equal")) and
           d["parent_source_recompiled"] is False and ind["parent_source_recompiled"] is False and
           ind["independent_delta_compilation_count"]==1 and d["delta_compilation_count"]==1,
           "R75 R2 certified exact receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==344 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R75 actual audit inventory")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r75.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_readiness_path_key"]==load(out/r74.NEW)["key"] and len(record["recovery_paths"])==2 and
           record["historical_scope_digest"]==d["historical_scope_digest"]==SCOPE==digest(scope) and
           record["script_bridge_digest"]==d["script_bridge_digest"]==BRIDGE==digest(bridge) and
           record["r69_additive_observation_digest"]==d["r69_additive_observation_digest"]==EXTENSION==digest(extension) and
           record["historical_research_only"] and record["future_additions_observation_only"] and
           d["deletion_basis_only_no_inverse_retained"] and d["net_history_collision_retained"] and
           d["original_patch_history_retained"] and d["empty_inventory_hold_count"]==5 and
           d["minimal_batch_constructor_proved"] is False and
           {n:digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R75 exact record scope")
    v.need(all(d.get(k) is False and record.get(k) is False for k in
           ("proof_authority","action_authority","release_authorized","active_policy_changed",
            "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed",
            "python_general_correctness_proved","live_main_admission","current_main_certification_transferred",
            "registry_updated","batch_applied_to_live_registry","automatic_registration_authority",
            "automatic_recovery_authority","registry_authentication_proved","identity_authentication_proved",
            "unknown_registration_is_refutation","registration_correctness_implied_by_readiness","execution_history_order_independent")),
           "R75 no authority or completeness transfer")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"R76 base capsule manifest")
        copy_tree_equal(local/folder,other/folder,out/folder)
        v.need(sha((out/folder/(manifest["module"]+".lean")).read_bytes())==manifest["source_sha256"],"R76 base capsule source")
        tool.install(out/folder,manifest)
    receipts=out/PARENT_FOLDER;receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","recovery-application.lean","recovery-computation.lean","recovery-computation.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                 r75.SOURCE,r75.VIEW,r75.MANIFEST,r75.REPLAY,"CapsuleObservation.lean",
                 "formal-source-r1.lean","recovery-computation-r1.lean","RegistryRecoveryR75-r1.lean","RegistryRecoveryR75-r1.log",
                 "r75-r2-repair.json",*r75.HIST_RAW):
        r63.copy_equal(local/name,other/name,receipts/name)
    repair=load(receipts/"r75-r2-repair.json")
    v.need(repair["status"]=="R75_R2_RESERVED_TOKEN_AND_EXPLICIT_DIRECT_REFERENCES" and
           repair["all_source_propositions_unchanged"] and repair["all_17_raw_types_equal"] and
           repair["unchanged_full_proof_expressions"]==15 and repair["axiom_sets_not_increased"] and
           repair["direct_dependency_requirements_unchanged"] and repair["r2_direct_digest"]==DIRECT and
           repair["r2_source_sha256"]==record["delta_source_sha256"] and repair["parent_source_recompiled"] is False,
           "R75 R2 repair evidence")
    v.need(load(receipts/"historical-scope.json")==scope and load(receipts/"script-bridge.json")==bridge and
           load(receipts/"script-observation-bridge-r69.json")==extension and
           sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           sha((receipts/"recovery-application.lean").read_bytes())==record["application_source_sha256"] and
           sha((receipts/"recovery-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"recovery-computation.json")==record["recovery_paths"] and
           (receipts/r75.SOURCE).read_bytes()==d["fresh_application"]["mcp_source"].encode(),"R75 R2 source lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R76 parent observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
        for name in (r75.SOURCE.replace(".lean",".log"),"CapsuleObservation.log"):
            shutil.copyfile(src/name,receipts/(label+"-"+name))
    # Preserve both compiled ancestors, not just the latest delta.
    m1,r1=r75.check_capsule(local,d);m2,r2=r75.check_capsule(other,d)
    v.need(m1==m2 and digest(m1)==PARENT_MANIFEST and r1==r2 and digest(r1)==PARENT_REPLAY and
           m1["files"]==[{"name":"RegistryRecoveryR75.olean","sha256":PARENT_OLEAN,"bytes":236464}],
           "R75 independently reproduced delta")
    copy_tree_equal(local/BASE_CAP,other/BASE_CAP,out/BASE_CAP)
    v.need(transport.capsule_files(out/BASE_CAP)==[{"name":"RecoveryDualityR62.olean","sha256":r75.PARENT_OLEAN,"bytes":5972832}],
           "R76 exact independently certified base module")
    transport.install(out/BASE_CAP,transport.capsule_files(out/BASE_CAP))
    copy_tree_equal(local/r75.CAP,other/r75.CAP,out/PARENT_CAP)
    r75.install_module(out/PARENT_CAP,m1["files"])
    r75.installed_matches(m1["files"])
    v.need(mp["parent_mcp_digest"]==r75.MCP and mp["reused_audit_count"]==327 and mp["new_audit_count"]==17 and
           mp["fresh_full_source_diagnostics"] and len(mp["audit_origins"])==344 and ind["mcp_reused_audits"]==327 and
           ind["mcp_new_audits"]==17 and mp["diagnostic_coverage_digest"]==ind["diagnostic_coverage_digest"]==PARENT_DIAGNOSTICS and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==PARENT_MANIFEST and
           mp["imported_replay_digest"]==PARENT_REPLAY and
           mp["diagnostic_source_scope"]=="new_delta_module_with_certified_parent_import","R75 actual transport receipt")
    coverage=r75.verify_complete_diagnostics(local,d,mp)
    v.need(digest(coverage)==PARENT_DIAGNOSTICS,"R75 full-source severity coverage")
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json";raw=load(local/name);val=v.structured(raw);origin=mp["audit_origins"][j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha((local/name).read_bytes()),
               "R75 exact per-declaration MCP receipt")
        shutil.copyfile(local/name,receipts/name)
    for i in range(54,75):
        folder="parent-r"+str(i)+"-receipts"
        copy_tree_equal(local/folder,other/folder,out/folder)
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),
                    (67,r67.NEW),(68,r68.NEW),(69,r69.NEW),(70,r70.NEW),(71,r71.NEW),(72,r72.NEW),(73,r73.NEW),(74,r74.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],
               "R75 exact historical raw record")
    return d,mp,ind,record

def observer(out,names):
    result=r75.observer(out,names)
    v.need(result.count("KUUOS_R75_RAW ")==1,"R76 observer marker boundary")
    return result.replace("KUUOS_R75_RAW ","KUUOS_R76_RAW ")

def raw_audit(log,by,names):
    marker="KUUOS_R76_RAW "
    rows=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    raw={x["name"]:x for x in rows}
    v.need(len(rows)==len(raw)==len(names) and set(raw)==set(names),"R76 exact raw inventory")
    for n,x in raw.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and
               "sorryAx" not in x["proof_expr"] and "sorryAx" not in x["type_expr"] and
               sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
               set(x["axioms"])<=STANDARD,"R76 exact raw theorem "+n)
    return raw
def minimal_sources(ledger,parent,patch_record):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=patch_record["patches"];by_digest={old.digest(p):p for p in patches}
    v.need(len(rows)==7 and len(patches)==2 and len(parent["recovery_paths"])==2 and len(ledger["empty_inventory_holds"])==5,"R76 inventory")
    idx={"global_boundary":2,"global_default":3,"global_probes":6}
    def fs(case):return {tuple(x) for x in rows[case]["encoded_cuts"]}
    def basis(case):return "((KuuOSR63.cuts_"+str(idx[case])+".map List.toFinset).toFinset)"
    def key(pair):return "("+json.dumps(pair[0])+", "+json.dumps(pair[1])+")"
    def literal(xs):return "(("+json.dumps([list(x) for x in sorted(xs)])+" : List (List Nat)).map List.toFinset).toFinset"
    def step(sk,tk,s,t,R,N):
        return "({ sourceKey := "+sk+", targetKey := "+tk+", patch := { source := "+basis(s)+", target := "+basis(t)+", retired := "+literal(R)+", introduced := "+literal(N)+" } } : KuuOSR70.TaggedStep (String × String) Nat)"
    bindings={}
    for p in patches:
        for c,r in ((p["source_case"],p["source_request_id"]),(p["target_case"],p["target_request_id"])):
            k=(p["context_id"],r)
            v.need(c in idx and (k not in bindings or bindings[k]==c),"R76 unique binding")
            bindings[k]=c
    v.need(len(bindings)==3 and set(bindings.values())==set(idx),"R76 three original bindings")
    original=[{"key":list(k),"case":c,"basis_digest":old.digest([list(x) for x in sorted(fs(c))])} for k,c in sorted(bindings.items())]
    src=["namespace KuuOSR76"];compute=["namespace KuuOSR76"];items=[];refs={}
    reg="KuuOSR71.observedRegistry"
    for i,path in enumerate(parent["recovery_paths"]):
        pairs=[tuple(k) for k in path["ordered_context_request_keys"]];nodes=path["ordered_cases"];edges=path["ordered_parent_patch_refs"]
        v.need(path["index"]==i and path["original_registry"]==original and path["original_registry_unchanged"] and
               path["lean_computation"]["correct_recovers"] and path["lean_computation"]["wrong_ready_path_hold"] and
               len(pairs)==len(nodes)==len(edges)+1 and len(edges)==(3 if i==0 else 4) and
               all(bindings.get(k)==c for k,c in zip(pairs,nodes)),"R75 exact registry and path")
        keys=[key(k) for k in pairs];literals=[]
        for j,e in enumerate(edges):
            p=by_digest[e["digest"]];s,t=p["source_case"],p["target_case"];sid,tid=p["source_request_id"],p["target_request_id"]
            R={tuple(x) for x in p["retired"]};N={tuple(x) for x in p["introduced"]}
            v.need(e["direction"] in ("forward","rollback"),"R76 direction")
            if e["direction"]=="rollback":s,t,sid,tid,R,N=t,s,tid,sid,N,R
            v.need((s,t)==tuple(nodes[j:j+2]) and ((p["context_id"],sid),(p["context_id"],tid))==tuple(pairs[j:j+2]) and
                   (sid,tid)==(e["source_request_id"],e["target_request_id"]) and R==fs(s)-fs(t) and N==fs(t)-fs(s),"R76 exact patch")
            literals.append(step(keys[j],keys[j+1],s,t,R,N))
        f,h,m=basis(nodes[0]),basis(nodes[-1]),basis(nodes[1]);R,N=fs(nodes[0])-fs(nodes[-1]),fs(nodes[-1])-fs(nodes[0])
        v.need(R=={tuple(x) for x in path["retired"]} and N=={tuple(x) for x in path["introduced"]},"R75 net identity")
        v.need(pairs[0]!=pairs[1] and fs(nodes[0])!=fs(nodes[1]),"R76 nontrivial missing controls")
        walk="(KuuOSR70.taggedWalk ("+keys[0]+", "+f+") ["+", ".join("("+k+", "+basis(c)+")" for k,c in zip(keys[1:],nodes[1:]))+"])"
        args=keys[0]+" "+keys[-1]+" "+f+" "+h+" "+walk
        delta="("+f+" \\ "+h+", "+h+" \\ "+f+")"
        requirement="(KuuOSR75.RequiredBindings "+args+")"
        name="actual_minimal_plan_recovers_"+str(i);least="actual_minimal_plan_necessary_"+str(i)
        src += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                "theorem "+name,
                "  (reg : (String × String) → Option (KuuOSR69.Basis Nat))",
                "  (bs : List ((String × String) × KuuOSR69.Basis Nat))",
                "  (hp : checkedRecoveryPlan reg "+requirement+" = some bs) :",
                "  ∃ next, KuuOSR73.checkedBatch reg bs = some next ∧",
                "    KuuOSR71.checkedRegisteredPath next "+args+" = some "+delta+" :=",
                "  checked_plan_path_recovers reg bs "+args+" "+delta+" hp",
                "    (KuuOSR71.checked_registered_projection "+reg+" "+args+" "+delta+" KuuOSR71.actual_registered_path_"+str(i)+")",
                "set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                "theorem "+least,
                "  (reg next : (String × String) → Option (KuuOSR69.Basis Nat))",
                "  (candidate bs : List ((String × String) × KuuOSR69.Basis Nat))",
                "  (hp : checkedRecoveryPlan reg "+requirement+" = some candidate)",
                "  (hb : KuuOSR73.checkedBatch reg bs = some next)",
                "  (hr : KuuOSR71.checkedRegisteredPath next "+args+" = some "+delta+") :",
                "  ∀ b ∈ candidate, b ∈ bs :=",
                "  checked_plan_minimal reg next "+requirement+" candidate bs hp hb",
                "    ((KuuOSR75.required_bindings_iff next "+args+").mpr",
                "      ((KuuOSR71.checked_registered_iff next "+args+" "+delta+").mp hr).1)"]
        refs[NS+name]=[NS+"checked_plan_path_recovers","KuuOSR71.checked_registered_projection","KuuOSR71.actual_registered_path_"+str(i)]
        refs[NS+least]=[NS+"checked_plan_minimal","KuuOSR75.required_bindings_iff","KuuOSR71.checked_registered_iff"]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let h := "+h,"  let m := "+m,
                    "  let path : List (KuuOSR70.TaggedStep (String × String) Nat) := ["+", ".join(literals)+"]",
                    "  let firstKey := "+keys[0],"  let lastKey := "+keys[-1],"  let middleKey := "+keys[1],
                    "  let reg := "+reg,"  let r := "+literal(R),"  let n := "+literal(N),
                    "  let req := KuuOSR75.RequiredBindings firstKey lastKey f h path",
                    "  let missing := fun k : String × String => if k = firstKey ∨ k = middleKey then none else reg k",
                    "  let oneMissing := fun k : String × String => if k = firstKey then none else reg k",
                    "  let absent : (String × String) → Option (KuuOSR69.Basis Nat) := fun _ => none",
                    "  let restore := [(firstKey,f),(middleKey,m)]",
                    "  let conflict := KuuOSR72.setBinding reg firstKey m",
                    "  let plan := checkedRecoveryPlan missing req",
                    "  let replay := fun next => KuuOSR71.checkedRegisteredPath next firstKey lastKey f h path",
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("steps", Lean.toJson path.length),',
                    '    ("requirements_occurrences", Lean.toJson req.length),',
                    '    ("baseline_empty", Lean.toJson (decide (checkedRecoveryPlan reg req = some []))),',
                    '    ("generated_exact", Lean.toJson (decide (plan.map List.toFinset = some restore.toFinset))),',
                    '    ("generated_two", Lean.toJson (decide (plan.map List.length = some 2))),',
                    '    ("generated_ready", Lean.toJson (decide (plan.map (KuuOSR74.batchReadyCheck missing) = some true))),',
                    '    ("generated_recovers", Lean.toJson (decide ((plan.bind (KuuOSR73.checkedBatch missing)).map replay = some (some (r,n))))),',
                    '    ("conflict_hold", Lean.toJson ((checkedRecoveryPlan conflict req).isNone)),',
                    '    ("inconsistent_hold", Lean.toJson ((checkedRecoveryPlan absent ((firstKey,m)::req)).isNone)),',
                    '    ("repeated_requirements_same_set", Lean.toJson (decide ((checkedRecoveryPlan missing (req ++ req)).map List.toFinset = plan.map List.toFinset))),',
                    '    ("one_missing_exact", Lean.toJson (decide (checkedRecoveryPlan oneMissing req = some [(firstKey,f)]))),',
                    '    ("all_missing_three", Lean.toJson (decide ((checkedRecoveryPlan absent req).map List.length = some 3))),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R76_COMPUTE " ++ payload.compress)']
        req_occ=[{"key":list(pairs[0]),"case":nodes[0]},{"key":list(pairs[-1]),"case":nodes[-1]}]+[
            x for j in range(len(edges)) for x in ({"key":list(pairs[j]),"case":nodes[j]},{"key":list(pairs[j+1]),"case":nodes[j+1]})]
        missing_occ=[{"key":list(pairs[j]),"case":nodes[j]} for j in (0,1)]
        v.need(req_occ==path["required_bindings_occurrences"] and missing_occ==path["counterfactual_missing_bindings"],
               "R76 R75 exact occurrence history")
        items.append({"index":i,"parent_recovery_path_digest":digest(path),"original_registry":original,
            "required_bindings_occurrences":req_occ,"counterfactual_missing_bindings":missing_occ,
            "ordered_context_request_keys":[list(k) for k in pairs],"ordered_cases":nodes,"ordered_parent_patch_refs":edges,
            "retired":path["retired"],"introduced":path["introduced"],"theorems":[NS+name,NS+least],
            "path_history_retained":True,"counterfactual_only":True,"original_registry_unchanged":True,
            "action_authority":False,"registry_authentication_proved":False,"candidate_minimality":"inclusion_of_bindings"})
    for line in compute:
        if line.lstrip().startswith('("'):
            v.need(line.count("(")==line.count(")"),"R76 generated JSON field parentheses "+line[:120])
    return "\n".join(src+["end KuuOSR76",""]),"\n".join(compute+["end KuuOSR76",""]),items,refs

def module_files(folder):
    f=folder/(MODULE+".olean")
    paths=(f,Path(str(f)+".server"),Path(str(f)+".private"))
    present=[p.is_file() and not p.is_symlink() for p in paths]
    v.need(present[0] and present[1]==present[2] and
           {p.name for p in folder.iterdir()}=={p.name for p,ok in zip(paths,present) if ok},
           "R76 complete isolated module parts")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p,ok in zip(paths,present) if ok]

def install_module(folder,files):
    v.need(module_files(folder)==files,"R76 module identity")
    dest=ROOT/".lake/build/lib/lean"/IMPORT_DIR
    dest.mkdir(parents=True,exist_ok=True)
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"R76 module destination collision")
    for item in files:
        p=dest/item["name"]
        with p.open("xb") as f:f.write((folder/item["name"]).read_bytes())
        v.need(sha(p.read_bytes())==item["sha256"],"R76 installed module identity")

def installed_matches(files):
    r75.installed_matches([{"name":"RegistryRecoveryR75.olean","sha256":PARENT_OLEAN,"bytes":236464}])
    for item in files:
        p=ROOT/".lake/build/lib/lean"/IMPORT_DIR/item["name"]
        v.need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==item["sha256"],"R76 installed module drift")

def expected_raw(out):
    result={}
    for name in HIST_RAW:
        x=load(out/name)
        v.need(not set(x).intersection(result),"R76 duplicate historical proof")
        result.update(x)
    v.need(len(result)==245,"R76 prior full proof count")
    return result

def canonical_raw(x):
    return {**x,"axioms":sorted(set(x["axioms"]))}

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope)
    extension=r69.additive_bridge(scope,bridge)
    v.need(digest(extension)==EXTENSION,"R76 historical bridge")
    before=r69.observe_live_r3(scope)
    for name,value in (("historical-scope.json",scope),("script-bridge.json",bridge),("script-observation-bridge-r69.json",extension)):
        v.save(out/name,value)
    pd,pm,pi,parent=admit(a,out,scope,bridge,extension)
    # Retain every full historical proof record independently of the new module.
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW),
                    (68,r68.NEW),(69,r69.NEW),(70,r70.NEW),(71,r71.NEW),(72,r72.NEW),(73,r73.NEW),(74,r74.NEW),(75,r75.NEW)):
        row=load(out/layer)["raw_theorems"]
        if i<75:v.need(row==load(out/PARENT_FOLDER/("parent-r"+str(i)+"-raw-replay.json")),"R76 old raw lineage")
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),row)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=minimal_sources(load(out/r63.NEW),parent,load(out/r67.NEW))
    for name,s in (("formal-source.lean",formal),("minimal-application.lean",app),("minimal-computation.lean",compute)):
        (out/name).write_text(s,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(n for item in items for n in item["theorems"])
    v.need(len(names)==len(set(names))==19,"R76 new theorem inventory")
    expected={NS+n:REFS.get(n,[]) for n in GENERAL};expected.update(refs)
    # Compile ONLY the delta. The certified parent is an immutable import.
    source=r75.VIEW_TEXT+"\n"+formal+"\n"+app+"\n"+compute+"\n"+observer(out,sorted(names))+v.suffix(sorted(names))
    cap=out/CAP;cap.mkdir()
    p=out/SOURCE
    log=r63.r62.r23.run_lean(["--root="+str(ROOT),"-o",str(cap/(MODULE+".olean"))],p,source)
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(names)])
    newraw=raw_audit(log,{x["name"]:x for x in audit},names)
    mark="KUUOS_R76_COMPUTE "
    computations=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(len(computations)==2 and [x["index"] for x in computations]==[0,1],"R76 computation inventory")
    for item,x in zip(items,computations):
        v.need(all(x[k] is True for k in ("baseline_empty","generated_exact","generated_two","generated_ready","generated_recovers",
                    "conflict_hold","inconsistent_hold","repeated_requirements_same_set","one_missing_exact","all_missing_three")) and
               x["requirements_occurrences"]==len(item["required_bindings_occurrences"])==2+2*x["steps"] and
               x["steps"]==len(item["ordered_parent_patch_refs"]) and x["net_retired"]==len(item["retired"]) and
               x["net_introduced"]==len(item["introduced"]),"R76 actual obligation controls")
        item["lean_computation"]=x
    v.save(out/"minimal-computation.json",items)
    files=module_files(cap);install_module(cap,files)
    prior_rows=pd["fresh_application"]["observations"]
    all_rows=sorted(prior_rows+audit,key=lambda x:x["name"])
    v.need(len(all_rows)==len({x["name"] for x in all_rows})==363,"R76 accumulated declaration inventory")
    all_names=[x["name"] for x in all_rows]
    all_raw=expected_raw(out);v.need(set(all_raw).isdisjoint(newraw),"R76 no old proof replacement");all_raw.update(newraw)
    v.need(len(all_raw)==264,"R76 complete proof inventory")
    # Independently observe the imported proof graph; no parent elaboration.
    imported_source=VIEW_TEXT+"\n"+observer(out,sorted(all_raw))+v.suffix(all_names)
    ilog=r63.r62.r23.run_lean([],out/"CapsuleObservation.lean",imported_source)
    observed=v.read_direct(ilog,[{"name":x["name"],"expected_direct_refs":x["expected_direct_refs"]} for x in all_rows])
    v.need(len(observed)==363 and [x["name"] for x in observed]==all_names,"R76 all imported names")
    for arow,brow in zip(observed,all_rows):
        v.need(all(arow[k]==brow[k] for k in FIELDS),"R76 imported kernel difference "+brow["name"])
    iraw=raw_audit(ilog,{x["name"]:x for x in observed},all_raw)
    v.need({n:canonical_raw(x) for n,x in iraw.items()}=={n:canonical_raw(x) for n,x in all_raw.items()},
           "R76 full imported proof equality without expression normalization")
    replay={"observations":[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in observed],
            "raw_proof_digests":{n:digest(canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay)
    (out/VIEW).write_text(VIEW_TEXT,encoding="utf-8")
    manifest={"schema":"kuuos.codeai.r76.incremental-compiled-proof.v1","module":IMPORT_MODULE,
              "module_path":str(IMPORT_DIR/(MODULE+".olean")),"files":files,
              "parent_module":r75.IMPORT_MODULE,"parent_olean_sha256":PARENT_OLEAN,
              "parent_independent_run":RUN,"parent_imported_replay_digest":PARENT_REPLAY,
              "source_sha256":sha(p.read_bytes()),"view_sha256":sha((out/VIEW).read_bytes()),
              "imported_replay_digest":digest(replay),"imported_audits":363,"imported_complete_proofs":264,
              "parent_source_recompiled":False,"delta_compilation_count":1,"proof_authority":False,"action_authority":False}
    v.save(out/MANIFEST,manifest)
    after=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,before,after)
    v.save(out/"main-observations.json",{"before":before,"after":after})
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved","registry_authentication_proved",
      "unknown_registration_is_refutation","registry_updated","automatic_registration_authority","batch_applied_to_live_registry",
      "registration_correctness_implied_by_readiness","execution_history_order_independent","automatic_recovery_authority")}
    boundary.update({"minimal_batch_constructor_proved":True,"candidate_inclusion_minimality_proved":True,"conflict_no_extension_proved":True})
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,
        "future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.registry-minimal-recovery.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_recovery_path_key":KEY,"r75_direct_digest":DIRECT,"r75_mcp_digest":MCP,"r75_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
        "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "formal_source_sha256":sha(formal.encode()),"application_source_sha256":sha(app.encode()),
        "computation_source_sha256":sha(compute.encode()),"delta_source_sha256":manifest["source_sha256"],
        "minimal_recovery_paths":items,"empty_inventory_holds":parent["empty_inventory_holds"],
        "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
        "raw_theorems":newraw,"formal_observations":{x["name"]:x for x in audit},**boundary})
    v.save(out/NEW,record)
    result={"status":"R76_DIRECT_MINIMAL_RECOVERY","source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,
        "scope_digest":old.SCOPE,"parent_recovery_path_key":KEY,"minimal_recovery_path_key":record["key"],
        "r75_direct_digest":DIRECT,"r75_mcp_digest":MCP,"r75_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "capsule_manifest":pd["capsule_manifest"],"joint_capsule_manifest":pd["joint_capsule_manifest"],
        "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
        "audit_capsule_digest":digest(manifest),"imported_replay_digest":digest(replay),
        "general_theorems":15,"actual_minimal_recovery_theorems":4,"actual_path_count":2,"empty_inventory_hold_count":5,
        "actual_computations":computations,"formal_source_sha256":record["formal_source_sha256"],
        "application_source_sha256":record["application_source_sha256"],"computation_source_sha256":record["computation_source_sha256"],
        "delta_source_sha256":manifest["source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in newraw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:digest(x) for n,x in newraw.items()},"parent_source_recompiled":False,
        "delta_compilation_count":1,"parent_raw_replay_bytewise_equal":True,"imported_complete_proofs":264,
        "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
        "capsule_rebuilds":0,"active_dispatches":0,"new_root_discovery_trials":0,**boundary,
        "fresh_application":{"observations":all_rows,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R76_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest","raw_theorem_digests")}|
        {"direct_digest":digest(result),"audits":len(all_rows)},sort_keys=True),flush=True)
    print("KUUOS_R76_COMPILED",json.dumps(manifest,sort_keys=True),flush=True)
    return result

def check_capsule(out,d):
    m=load(out/MANIFEST);r=load(out/REPLAY)
    v.need(m["schema"]=="kuuos.codeai.r76.incremental-compiled-proof.v1" and m["module"]==IMPORT_MODULE and
           m["module_path"]==str(IMPORT_DIR/(MODULE+".olean")) and m["files"]==module_files(out/CAP) and
           m["parent_olean_sha256"]==PARENT_OLEAN and m["parent_module"]==r75.IMPORT_MODULE and
           m["parent_imported_replay_digest"]==PARENT_REPLAY and m["parent_independent_run"]==RUN and
           m["source_sha256"]==sha((out/SOURCE).read_bytes())==d["delta_source_sha256"] and
           (out/SOURCE).read_bytes()==d["fresh_application"]["mcp_source"].encode() and
           (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m["view_sha256"]==sha((out/VIEW).read_bytes()) and
           digest(m)==d["audit_capsule_digest"] and digest(r)==m["imported_replay_digest"]==d["imported_replay_digest"] and
           m["imported_audits"]==363 and m["imported_complete_proofs"]==264 and
           m["parent_source_recompiled"] is False and m["delta_compilation_count"]==1 and
           m["proof_authority"] is False and m["action_authority"] is False,"R76 exact incremental manifest")
    v.need(r["observations"]==[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in d["fresh_application"]["observations"]],
           "R76 exact imported replay metadata")
    raw=expected_raw(out);raw.update(load(out/NEW)["raw_theorems"])
    v.need(len(raw)==264 and r["raw_proof_digests"]=={n:digest(canonical_raw(x)) for n,x in raw.items()},
           "R76 exact imported complete proof digests")
    return m,r


# R76: exact same full source, separate complete error and warning reports.
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
    v.need(p.read_bytes()==load(out/"direct.json")["fresh_application"]["mcp_source"].encode(),"R76 exact direct receipt source")
    entries=[]
    for severity,name in DIAG_FILES:
        args={"file_path":rel,"timeout_s":DIAG_TIMEOUT,"severity":severity}
        raw=v.call_tool(client,"lean_diagnostic_messages",args)
        v.save(out/name,raw)
        # Never treat a timeout or filtered error/warning as success.
        diag=v.structured(raw)
        print("KUUOS_R76_DIAGNOSTIC",json.dumps({"severity":severity,"success":diag.get("success"),
             "partial":diag.get("partial"),"timed_out":diag.get("timed_out"),
             "still_elaborating_lines":diag.get("still_elaborating_lines"),
             "item_count":len(diag.get("items",[])),
             "failed_dependencies":diag.get("failed_dependencies")},sort_keys=True),flush=True)
        v.need(complete_diagnostic(raw),"R76 incomplete or non-clean full-source "+severity+" diagnostic")
        entries.append({"severity":severity,"file":name,"request":args,
                        "raw_sha256":sha((out/name).read_bytes())})
    manifest={"schema":"kuuos.codeai.r76.complete-severity-diagnostics.v1",
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
           manifest["schema"]=="kuuos.codeai.r76.complete-severity-diagnostics.v1" and
           manifest["mcp_version"]==v.EXPECTED_SERVER_VERSION and
           manifest["pinned_diagnostics_api_blob"]==DIAG_API_BLOB and
           manifest["pinned_diagnostics_processor_blob"]==DIAG_PROCESS_BLOB and
           manifest["timeout_s_per_call"]==DIAG_TIMEOUT and manifest["client_timeout_s"]==DIAG_CLIENT_TIMEOUT and
           all(manifest[k] is True for k in ("full_source","no_line_or_declaration_filter","all_error_and_warning_severities",
                                            "info_and_hint_not_transferred")) and
           len(manifest["receipts"])==2,"R76 complete diagnostic scope and exact source")
    for entry,(severity,name) in zip(manifest["receipts"],DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r76/MinimalRecoveryR76.lean",
                                  "timeout_s":DIAG_TIMEOUT,"severity":severity} and
               entry["raw_sha256"]==sha((first/name).read_bytes()) and complete_diagnostic(load(first/name)),
               "R76 actual complete full-source diagnostic "+severity)
    return manifest



def mcp(out):
    d=load(out/"direct.json");manifest,replay=check_capsule(out,d)
    installed_matches(manifest["files"])
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==DIRECT and digest(pm)==MCP and pm["direct_digest"]==DIRECT and
           pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R76 certified parent MCP")
    parent_rows={r["name"]:(j,r) for j,r in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==344 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R76 distinct audit inventory")
    p=out/SOURCE
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp"]
    version=v.server_version(cmd,ROOT)
    client=transport.new_client("KuuOS R76 delta source diagnostics")
    try:
        coverage=run_complete_diagnostics(client,str(p.relative_to(ROOT)),out,p)
    finally:
        client.close()
    client=transport.new_client("KuuOS R76 compiled delta axiom audits")
    rows=[];origins=[];rel=str((out/VIEW).relative_to(ROOT))
    try:
        for j,row in enumerate(d["fresh_application"]["observations"]):
            name=row["name"];dest=out/f"mcp-verify-{j}.json"
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(prior==row and d["parent_raw_replay_bytewise_equal"],"R76 exact prior row")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,dest);raw=load(dest)
                origin={"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140957113907,
                        "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":sha(dest.read_bytes())}
            else:
                v.need(name in d["new_theorem_names"],"R76 new audit identity")
                installed_matches(manifest["files"])
                args={"file_path":rel,"theorem_name":name,"scan_source":False}
                print("KUUOS_R76_VERIFY_START",json.dumps(args,sort_keys=True),flush=True)
                raw=client.request("tools/call",{"name":"lean_verify","arguments":args})
                v.save(dest,raw)
                v.need(raw["result"]["isError"] is False,"R76 actual lean_verify failed "+name)
                origin={"name":name,"mode":"fresh_actual_mcp","receipt_sha256":sha(dest.read_bytes()),
                        "request":args,"audit_capsule_digest":digest(manifest),"audit_view_sha256":manifest["view_sha256"]}
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R76 actual MCP audit "+name)
            rows.append({"name":name,"axioms":ax});origins.append(origin)
    finally:
        client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==344 and fresh==19 and len(rows)==363,"R76 exact MCP count")
    installed_matches(manifest["files"])
    result={"status":"R76_REAL_MCP_GREEN","direct_digest":digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_source_scope":"new_delta_module_with_certified_parent_import",
            "diagnostic_coverage_digest":digest(coverage),"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version,
            "audit_transport":"incremental_compiled_import_exact_replay","audit_capsule_digest":digest(manifest),
            "audit_view_sha256":manifest["view_sha256"],"imported_replay_digest":digest(replay)}
    v.save(out/"mcp.json",result)
    print("KUUOS_R76_MCP",json.dumps({"mcp_digest":digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True,
          "audit_transport":result["audit_transport"],"diagnostic_scope":result["diagnostic_source_scope"]},sort_keys=True),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    current,replay=check_capsule(out,d);prior,first_replay=check_capsule(first,a)
    v.need(a==d and prior==current and replay==first_replay and mp["status"]=="R76_REAL_MCP_GREEN" and
           mp["direct_digest"]==digest(d) and mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==344 and
           mp["new_audit_count"]==19 and mp["fresh_full_source_diagnostics"] is True and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==digest(prior) and
           mp["audit_view_sha256"]==prior["view_sha256"] and mp["imported_replay_digest"]==digest(replay) and
           mp["diagnostic_source_scope"]=="new_delta_module_with_certified_parent_import","R76 independent receipt and exact compiled replay")
    coverage=verify_complete_diagnostics(first,d,mp)
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(first/name,out/name)
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(origins)==len(rows)==363,"R76 independent MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        p=first/f"mcp-verify-{j}.json";raw=load(p);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha(p.read_bytes()),
               "R76 actual MCP receipt")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140957113907 and
                   pd["fresh_application"]["observations"][k]==row and origin["prior_origin"]==pm["audit_origins"][k] and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==p.read_bytes(),"R76 reused receipt identity")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"] and
                   origin["request"]=={"file_path":"artifacts/olean-r76/"+VIEW,"theorem_name":row["name"],"scan_source":False} and
                   origin["audit_capsule_digest"]==digest(prior) and origin["audit_view_sha256"]==prior["view_sha256"],
                   "R76 fresh compiled audit identity")
            fresh+=1
    v.need(reused==344 and fresh==19,"R76 independent counts")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        ob=load(folder/"main-observations.json");r69.observation_pair_valid(scope,ob["before"],ob["after"])
    for name in FILES+(NEW,"direct.json","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                       "formal-source.lean","minimal-application.lean","minimal-computation.lean","minimal-computation.json",
                       SOURCE,VIEW,MANIFEST,REPLAY,"CapsuleObservation.lean",*HIST_RAW):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"R76 independent exact bytes "+name)
    for folder in (CAP,PARENT_CAP,BASE_CAP,"capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,76))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"R76 parent and compiled bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R76_INDEPENDENT_MINIMAL_RECOVERY_GREEN","direct_digest":digest(d),
        "mcp_digest":digest(mp),"mcp_audits":363,"mcp_new_audits":19,"mcp_reused_audits":344,
        "fresh_full_source_mcp_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
        "diagnostic_source_scope":"new_delta_module_with_certified_parent_import","diagnostic_coverage_digest":digest(coverage),
        "minimal_recovery_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"compiled_file_bytes_equal":True,
        "imported_replay_equal":True,"parent_source_recompiled":False,"independent_delta_compilation_count":1,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R76_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r75-local","r75-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out==ROOT/"artifacts/olean-r76","R76 exact isolated module path")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
