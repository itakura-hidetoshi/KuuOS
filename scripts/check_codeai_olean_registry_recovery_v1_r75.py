#!/usr/bin/env python3
"""R75: exact path recovery obligations over independently certified compiled parent."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_registry_batch_readiness_v1_r74_r4 as transport
r74=transport.r1
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
RUN=46134807070
HEAD="f700937e91752276d0e00f867896bdf61778fbdf"
DIRECT="52c2f717f36e56d6d2350a3597fc0d5feeb29833d3e28ad233fbb01642be0783"
MCP="0c69419cafa65b563ea187b99cc79d205c2b6d0a9a39987e09e6750e1722de75"
KEY="2b300673b9dfb37e177b6a5233459ac57f3bf9cd23bebea4205abab13da852e5"
PARENT_DIAGNOSTICS="f33f56722763c4baf6768078f6fcf197e267ba5f294ec0b02c700ae2343af93c"
PARENT_REPLAY="7b1f5735cca6d1ad44c2b1eee0c300b854a6937bf2b1e74f4daace9b7cbb5544"
PARENT_LOCAL_CAP="1c0f4091cb7191005f0d16a88717dbc9a399ff1c04d8f9f267060c66850ae255"
PARENT_INDEPENDENT_CAP="abe5edb670a7170508302d98b6fa84739b10a90cca31045ff810a577bec7bdfc"
PARENT_OLEAN="e787df4d03a8b02efefb49c9d8e7f23aefeb0773c7072e270a53c8fdf68eb6ec"
SCOPE=r69.SCOPE
BRIDGE=r69.BRIDGE
EXTENSION="e8bed0fde1244c49b7194db383a8516418ee2950adaa5ff5233997b5672d626d"
ARTS=((15259782064,"codeai-olean-r74-r4-local-46134807070-1","sha256:a889e324c73d961ed720b435af1973ae4588cded35c4df2d7d9479964fee392e"),
      (15259103518,"codeai-olean-r74-r4-independent-46134807070-1","sha256:c6e64e4e775c109219183b5e5eb573fba189350e77f976aa98bddf86dc78c588"))
FILES=r74.FILES+(r74.NEW,)
NEW="registry-recovery-obligations-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_registry_recovery_v1.lean"
NS="KuuOSR75."
sha=r63.r62.r23.sha
digest=old.digest
MODULE="RegistryRecoveryR75"
IMPORT_MODULE="artifacts.«olean-r75».RegistryRecoveryR75"
IMPORT_DIR=Path("artifacts")/"olean-r75"
SOURCE=MODULE+".lean"
VIEW="McpCapsuleApplication.lean"
VIEW_TEXT="import "+IMPORT_MODULE+"\n"
CAP="audit-capsule"
MANIFEST="r75-audit-capsule.json"
REPLAY="r75-imported-replay.json"
PARENT_CAP="parent-audit-capsule"
PARENT_FOLDER="parent-r74-receipts"
FIELDS=transport.FIELDS
STANDARD={"Classical.choice","Quot.sound","propext"}
HIST_RAW=tuple("parent-r"+str(i)+"-raw-replay.json" for i in range(62,75))
GENERAL=("covers_cons","step_requirements_iff","required_bindings_iff","supply_check_iff",
         "binding_after_batch_iff","requirements_after_batch_iff","checked_batch_recovery_iff",
         "missing_binding_iff","missing_required_in_recovery","exact_missing_recovers",
         "conflicting_requirement_no_extension","inconsistent_requirements_no_registry","conflicting_path_hold")
REFS={
 "step_requirements_iff":[NS+"covers_cons"],
 "required_bindings_iff":[NS+"covers_cons",NS+"step_requirements_iff"],
 "binding_after_batch_iff":["KuuOSR73.checked_batch_contains","KuuOSR74.checked_batch_frame","KuuOSR73.checked_batch_extends"],
 "requirements_after_batch_iff":[NS+"binding_after_batch_iff"],
 "checked_batch_recovery_iff":["KuuOSR72.recovery_iff_of_tagged",NS+"required_bindings_iff",NS+"requirements_after_batch_iff"],
 "missing_required_in_recovery":[NS+"missing_binding_iff",NS+"required_bindings_iff","KuuOSR71.checked_registered_iff",NS+"binding_after_batch_iff"],
 "exact_missing_recovers":[NS+"checked_batch_recovery_iff",NS+"missing_binding_iff"],
 "conflicting_requirement_no_extension":["KuuOSR71.registered_binding_unique"],
 "inconsistent_requirements_no_registry":["KuuOSR71.registered_binding_unique"],
 "conflicting_path_hold":[NS+"conflicting_requirement_no_extension",NS+"required_bindings_iff","KuuOSR71.checked_registered_iff"],
}

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R74 R4 run")
    for jid,steps in ((140947604835,["Verify R74 R4 registry batch readiness","Actual Lean MCP R74 R4 new declarations and exact prior receipt reuse"]),
                      (140950075523,["Independently verify R74 R4 registry batch readiness"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R74 R4 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R74 R4 artifact")
    local=a.r74_local;other=a.r74_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R74_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R74_INDEPENDENT_REGISTRY_BATCH_READINESS_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==327 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","readiness_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R74 R4 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==327 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R74 R4 actual MCP audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r74.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_batch_path_key"]==load(out/r73.NEW)["key"],"R74 R4 key")
    v.need(record["historical_research_only"] and record["future_additions_observation_only"] and
           record["live_main_admission"] is False and record["current_main_certification_transferred"] is False and
           d["historical_scope_digest"]==record["historical_scope_digest"]==SCOPE==old.digest(scope) and
           d["script_bridge_digest"]==BRIDGE==old.digest(bridge) and
           d["r69_additive_observation_digest"]==record["r69_additive_observation_digest"]==EXTENSION==old.digest(extension) and
           d["deletion_basis_only_no_inverse_retained"] and d["net_history_collision_retained"] and
           d["original_patch_history_retained"] and len(record["readiness_paths"])==2 and d["registration_correctness_implied_by_readiness"] is False and d["execution_history_order_independent"] is False and d["batch_applied_to_live_registry"] is False and d["registry_updated"] is False and d["automatic_registration_authority"] is False and d["registry_authentication_proved"] is False and d["unknown_registration_is_refutation"] is False and d["identity_authentication_proved"] is False and d["empty_inventory_hold_count"]==5,"R71 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R71 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R71 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/PARENT_FOLDER;receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other),("McpApplication.lean",local)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","readiness-application.lean","readiness-computation.lean","readiness-computation.json",
                 "historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                 "CapsuleObservation.lean","CapsuleObservation.log","RecoveryDualityR62.lean","RecoveryDualityR62.log",
                 "McpCapsuleApplication.lean",transport.REPLAY,transport.REPAIR,transport.ROOT_REPAIR,transport.OBSERVER_REPAIR,
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,74))):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(load(receipts/"script-observation-bridge-r69.json")==extension and
           load(receipts/"script-bridge.json")==bridge and load(receipts/"historical-scope.json")==scope and
           sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           sha((receipts/"readiness-application.lean").read_bytes())==record["application_source_sha256"] and
           sha((receipts/"readiness-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"readiness-computation.json")==record["readiness_paths"] and
           (receipts/"McpApplication.lean").read_bytes()==d["fresh_application"]["mcp_source"].encode(),
           "R74 exact source lineage")
    m1,replay1=transport.check_capsule(local,d);m2,replay2=transport.check_capsule(other,d)
    tr=load(other/"r74-r4-independent-transport.json")
    v.need(digest(m1)==PARENT_LOCAL_CAP and digest(m2)==PARENT_INDEPENDENT_CAP and
           replay1==replay2 and digest(replay1)==PARENT_REPLAY and
           tr["status"]=="R74_R4_INDEPENDENT_AUDIT_TRANSPORT_GREEN" and
           tr["direct_digest"]==DIRECT and tr["mcp_digest"]==MCP and
           tr["sandbox_audit_capsule_digest"]==PARENT_LOCAL_CAP and tr["independent_audit_capsule_digest"]==PARENT_INDEPENDENT_CAP and
           tr["compiled_file_bytes_equal"] and tr["imported_replay_equal"] and tr["imported_replay_digest"]==PARENT_REPLAY and
           tr["imported_audits"]==327 and tr["imported_complete_proofs"]==228 and
           tr["sandbox_reused_r3_compilation"] and tr["independent_fresh_compilation"] and tr["observer_name_array_exact"] and
           tr["new_actual_mcp_audits"]==14 and tr["prior_mcp_audits_reused"]==313 and
           m1["files"]==m2["files"]==[{"name":"RecoveryDualityR62.olean","sha256":PARENT_OLEAN,"bytes":5972832}],
           "R74 independently reproduced compiled transport")
    for item in m1["files"]:
        r63.copy_equal(local/transport.CAP/item["name"],other/transport.CAP/item["name"],out/PARENT_CAP/item["name"])
    transport.install(out/PARENT_CAP,m1["files"])
    for label,src in (("sandbox",local),("independent",other)):
        for name in (transport.CAP_MANIFEST,transport.OBSERVER_ORIGIN):
            shutil.copyfile(src/name,receipts/(label+"-"+name))
    shutil.copyfile(other/"r74-r4-independent-transport.json",receipts/"r74-r4-independent-transport.json")
    for src in sorted((local/"r74-r1-mcp-history").iterdir()):
        if src.is_file():r63.copy_equal(src,other/"r74-r1-mcp-history"/src.name,receipts/"r74-r1-mcp-history"/src.name)
    v.need(mp["parent_mcp_digest"]==r74.MCP and mp["reused_audit_count"]==313 and mp["new_audit_count"]==14 and
           mp["fresh_full_source_diagnostics"] is True and len(mp["audit_origins"])==327 and
           ind["mcp_reused_audits"]==313 and ind["mcp_new_audits"]==14 and
           mp["diagnostic_coverage_digest"]==ind["diagnostic_coverage_digest"]==PARENT_DIAGNOSTICS and
           mp["audit_transport"]=="compiled_import_exact_replay" and mp["audit_capsule_digest"]==PARENT_LOCAL_CAP and
           mp["imported_replay_digest"]==PARENT_REPLAY,"R74 exact MCP and transport lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R69 live observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    coverage=r74.verify_complete_diagnostics(local,d,mp)
    v.need(old.digest(coverage)==PARENT_DIAGNOSTICS,"R71 complete severity coverage")
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json"
        raw=load(local/name);val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==mp["audit_origins"][j]["name"] and
               mp["audit_origins"][j]["receipt_sha256"]==r63.r62.r23.sha((local/name).read_bytes()),"R71 actual MCP per-declaration evidence")
        shutil.copyfile(local/name,receipts/name)
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW),(68,r68.NEW),(69,r69.NEW),(70,r70.NEW),(71,r71.NEW),(72,r72.NEW),(73,r73.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R69 ancestor raw lineage")
    for i in range(54,74):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record


def observer(out,names):
    # Use the certified corrected template but interpolate names only after
    # all namespace choices. No string-wide namespace replacement.
    p=out/PARENT_FOLDER/"CapsuleObservation.lean"
    v.need(sha(p.read_bytes())=="fd6804417aad4e00589e397e076b633baa33fdb3ea9e8834fbd10c3160908e46",
           "R75 exact R74 observer template")
    template=p.read_text(encoding="utf-8")
    cut="\n\nopen Lean\nset_option pp.universes true"
    v.need(template.count(cut)==1 and template.startswith(transport.VIEW_TEXT),"R75 observer template boundary")
    block=template[len(transport.VIEW_TEXT):template.index(cut)]
    prefix="  let ns : Array Name := #["
    lines=block.splitlines(keepends=True)
    at=[i for i,l in enumerate(lines) if l.startswith(prefix)]
    v.need(len(at)==1 and len(names)==len(set(names)) and
           all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*",n) for n in names),"R75 exact theorem inventory")
    lines[at[0]]=prefix+", ".join(chr(96)*2+n for n in names)+"]\n"
    result="".join(lines)
    v.need(result.count("KUUOS_R74_RAW ")==1,"R75 observer marker")
    return result.replace("KUUOS_R74_RAW ","KUUOS_R75_RAW ")+"\n"

def raw_audit(log,by,names):
    marker="KUUOS_R75_RAW "
    rows=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    raw={x["name"]:x for x in rows}
    v.need(len(rows)==len(raw)==len(names) and set(raw)==set(names),"R75 exact raw inventory")
    for n,x in raw.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and
               "sorryAx" not in x["proof_expr"] and "sorryAx" not in x["type_expr"] and
               sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
               set(x["axioms"])<=STANDARD,"R75 exact raw theorem "+n)
    return raw

def recovery_sources(ledger,parent,patch_record):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=patch_record["patches"];by_digest={old.digest(p):p for p in patches}
    v.need(len(rows)==7 and len(patches)==2 and len(parent["readiness_paths"])==2 and len(ledger["empty_inventory_holds"])==5,"R75 inventory")
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
            v.need(c in idx and (k not in bindings or bindings[k]==c),"R75 unique binding")
            bindings[k]=c
    v.need(len(bindings)==3 and set(bindings.values())==set(idx),"R75 three original bindings")
    original=[{"key":list(k),"case":c,"basis_digest":old.digest([list(x) for x in sorted(fs(c))])} for k,c in sorted(bindings.items())]
    src=["namespace KuuOSR75"];compute=["namespace KuuOSR75"];items=[];refs={}
    reg="KuuOSR71.observedRegistry"
    for i,path in enumerate(parent["readiness_paths"]):
        pairs=[tuple(k) for k in path["ordered_context_request_keys"]];nodes=path["ordered_cases"];edges=path["ordered_parent_patch_refs"]
        v.need(path["index"]==i and path["original_registry"]==original and path["original_registry_unchanged"] and
               path["lean_computation"]["old_path_preserved"] and path["lean_computation"]["wrong_ready_but_path_hold"] and
               len(pairs)==len(nodes)==len(edges)+1 and len(edges)==(3 if i==0 else 4) and
               all(bindings.get(k)==c for k,c in zip(pairs,nodes)),"R74 exact registry and path")
        keys=[key(k) for k in pairs];literals=[]
        for j,e in enumerate(edges):
            p=by_digest[e["digest"]];s,t=p["source_case"],p["target_case"];sid,tid=p["source_request_id"],p["target_request_id"]
            R={tuple(x) for x in p["retired"]};N={tuple(x) for x in p["introduced"]}
            v.need(e["direction"] in ("forward","rollback"),"R75 direction")
            if e["direction"]=="rollback":s,t,sid,tid,R,N=t,s,tid,sid,N,R
            v.need((s,t)==tuple(nodes[j:j+2]) and ((p["context_id"],sid),(p["context_id"],tid))==tuple(pairs[j:j+2]) and
                   (sid,tid)==(e["source_request_id"],e["target_request_id"]) and R==fs(s)-fs(t) and N==fs(t)-fs(s),"R75 exact patch")
            literals.append(step(keys[j],keys[j+1],s,t,R,N))
        f,h,m=basis(nodes[0]),basis(nodes[-1]),basis(nodes[1]);R,N=fs(nodes[0])-fs(nodes[-1]),fs(nodes[-1])-fs(nodes[0])
        v.need(R=={tuple(x) for x in path["retired"]} and N=={tuple(x) for x in path["introduced"]},"R74 net identity")
        v.need(pairs[0]!=pairs[1] and fs(nodes[0])!=fs(nodes[1]),"R75 nontrivial missing controls")
        walk="(KuuOSR70.taggedWalk ("+keys[0]+", "+f+") ["+", ".join("("+k+", "+basis(c)+")" for k,c in zip(keys[1:],nodes[1:]))+"])"
        args=keys[0]+" "+keys[-1]+" "+f+" "+h+" "+walk
        delta="("+f+" \\ "+h+", "+h+" \\ "+f+")"
        requirement="(RequiredBindings "+args+")"
        name="actual_original_requirements_"+str(i);rec="actual_recovery_condition_"+str(i)
        src += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                "theorem "+name+" : CoversBindings "+reg+" "+requirement+" :=",
                "  (required_bindings_iff "+reg+" "+args+").mpr",
                "    ((KuuOSR71.checked_registered_iff "+reg+" "+args+" "+delta+").mp KuuOSR71.actual_registered_path_"+str(i)+").1",
                "set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                "theorem "+rec,
                "  (reg next : (String × String) → Option (KuuOSR69.Basis Nat))",
                "  (bs : List ((String × String) × KuuOSR69.Basis Nat))",
                "  (hb : KuuOSR73.checkedBatch reg bs = some next) :",
                "  KuuOSR71.checkedRegisteredPath next "+args+" = some "+delta+" ↔ Supplies reg bs "+requirement+" :=",
                "  checked_batch_recovery_iff reg next bs "+args+" "+delta+" hb",
                "    (KuuOSR71.checked_registered_projection "+reg+" "+args+" "+delta+" KuuOSR71.actual_registered_path_"+str(i)+")"]
        refs[NS+name]=[NS+"required_bindings_iff","KuuOSR71.checked_registered_iff","KuuOSR71.actual_registered_path_"+str(i)]
        refs[NS+rec]=[NS+"checked_batch_recovery_iff","KuuOSR71.checked_registered_projection","KuuOSR71.actual_registered_path_"+str(i)]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let h := "+h,"  let m := "+m,
                    "  let path : List (KuuOSR70.TaggedStep (String × String) Nat) := ["+", ".join(literals)+"]",
                    "  let firstKey := "+keys[0],"  let lastKey := "+keys[-1],"  let middleKey := "+keys[1],
                    "  let reg := "+reg,"  let r := "+literal(R),"  let n := "+literal(N),
                    "  let req := RequiredBindings firstKey lastKey f h path",
                    "  let missing := fun k : String × String => if k = firstKey ∨ k = middleKey then none else reg k",
                    "  let restore := [(firstKey,f),(middleKey,m)]","  let partial := [(firstKey,f)]",
                    "  let wrong := [(firstKey,f),(middleKey,f)]",
                    "  let conflict := KuuOSR72.setBinding reg firstKey m",
                    "  let replay := fun next => KuuOSR71.checkedRegisteredPath next firstKey lastKey f h path",
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("steps", Lean.toJson path.length),',
                    '    ("requirements_occurrences", Lean.toJson req.length),',
                    '    ("baseline_covered", Lean.toJson (supplyCheck reg [] req)),',
                    '    ("missing_exact", Lean.toJson (decide ((missingBindings missing req).toFinset = restore.toFinset))),',
                    '    ("correct_supply", Lean.toJson (supplyCheck missing restore req)),',
                    '    ("partial_unsupplied", Lean.toJson (!supplyCheck missing partial req)),',
                    '    ("wrong_unsupplied", Lean.toJson (!supplyCheck missing wrong req)),',
                    '    ("correct_recovers", Lean.toJson (decide ((KuuOSR73.checkedBatch missing restore).map replay = some (some (r,n))))),',
                    '    ("partial_hold", Lean.toJson (decide ((KuuOSR73.checkedBatch missing partial).map replay = some none))),',
                    '    ("wrong_ready_path_hold", Lean.toJson (KuuOSR74.batchReadyCheck missing wrong && decide ((KuuOSR73.checkedBatch missing wrong).map replay = some none))),',
                    '    ("conflict_unsupplied", Lean.toJson (!supplyCheck conflict [] req)),',
                    '    ("conflict_existing_batch_hold", Lean.toJson ((KuuOSR73.checkedBatch conflict [(firstKey,f)]).isNone)),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R75_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"parent_readiness_path_digest":digest(path),"original_registry":original,
            "required_bindings_occurrences":[{"key":list(pairs[0]),"case":nodes[0]},{"key":list(pairs[-1]),"case":nodes[-1]}]+
                [x for j in range(len(edges)) for x in ({"key":list(pairs[j]),"case":nodes[j]},{"key":list(pairs[j+1]),"case":nodes[j+1]})],
            "counterfactual_missing_bindings":[{"key":list(pairs[j]),"case":nodes[j]} for j in (0,1)],
            "ordered_context_request_keys":[list(k) for k in pairs],"ordered_cases":nodes,"ordered_parent_patch_refs":edges,
            "retired":path["retired"],"introduced":path["introduced"],"theorems":[NS+name,NS+rec],
            "path_history_retained":True,"counterfactual_only":True,"original_registry_unchanged":True,
            "action_authority":False,"registry_authentication_proved":False})
    for line in compute:
        if line.lstrip().startswith('("'):
            v.need(line.count("(")==line.count(")"),"R75 generated JSON field parentheses "+line[:120])
    return "\n".join(src+["end KuuOSR75",""]),"\n".join(compute+["end KuuOSR75",""]),items,refs


def module_files(folder):
    f=folder/(MODULE+".olean")
    paths=(f,Path(str(f)+".server"),Path(str(f)+".private"))
    present=[p.is_file() and not p.is_symlink() for p in paths]
    v.need(present[0] and present[1]==present[2] and
           {p.name for p in folder.iterdir()}=={p.name for p,ok in zip(paths,present) if ok},
           "R75 complete isolated module parts")
    return [{"name":p.name,"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size} for p,ok in zip(paths,present) if ok]

def install_module(folder,files):
    v.need(module_files(folder)==files,"R75 module identity")
    dest=ROOT/".lake/build/lib/lean"/IMPORT_DIR
    dest.mkdir(parents=True,exist_ok=True)
    for suffix in (".olean",".olean.server",".olean.private"):
        v.need(not (dest/(MODULE+suffix)).exists(),"R75 module destination collision")
    for item in files:
        p=dest/item["name"]
        with p.open("xb") as f:f.write((folder/item["name"]).read_bytes())
        v.need(sha(p.read_bytes())==item["sha256"],"R75 installed module identity")

def installed_matches(files):
    transport.installed_matches([{"name":"RecoveryDualityR62.olean","sha256":PARENT_OLEAN,"bytes":5972832}])
    for item in files:
        p=ROOT/".lake/build/lib/lean"/IMPORT_DIR/item["name"]
        v.need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==item["sha256"],"R75 installed module drift")

def expected_raw(out):
    result={}
    for name in HIST_RAW:
        x=load(out/name)
        v.need(not set(x).intersection(result),"R75 duplicate historical proof")
        result.update(x)
    v.need(len(result)==228,"R75 prior full proof count")
    return result

def canonical_raw(x):
    return {**x,"axioms":sorted(set(x["axioms"]))}

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope)
    extension=r69.additive_bridge(scope,bridge)
    v.need(digest(extension)==EXTENSION,"R75 historical bridge")
    before=r69.observe_live_r3(scope)
    for name,value in (("historical-scope.json",scope),("script-bridge.json",bridge),("script-observation-bridge-r69.json",extension)):
        v.save(out/name,value)
    pd,pm,pi,parent=admit(a,out,scope,bridge,extension)
    # Retain every full historical proof record independently of the new module.
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW),
                    (68,r68.NEW),(69,r69.NEW),(70,r70.NEW),(71,r71.NEW),(72,r72.NEW),(73,r73.NEW),(74,r74.NEW)):
        row=load(out/layer)["raw_theorems"]
        if i<74:v.need(row==load(out/PARENT_FOLDER/("parent-r"+str(i)+"-raw-replay.json")),"R75 old raw lineage")
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),row)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=recovery_sources(load(out/r63.NEW),parent,load(out/r67.NEW))
    for name,s in (("formal-source.lean",formal),("recovery-application.lean",app),("recovery-computation.lean",compute)):
        (out/name).write_text(s,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(n for item in items for n in item["theorems"])
    v.need(len(names)==len(set(names))==17,"R75 new theorem inventory")
    expected={NS+n:REFS.get(n,[]) for n in GENERAL};expected.update(refs)
    # Compile ONLY the delta. The certified parent is an immutable import.
    source=transport.VIEW_TEXT+"\n"+formal+"\n"+app+"\n"+compute+"\n"+observer(out,sorted(names))+v.suffix(sorted(names))
    cap=out/CAP;cap.mkdir()
    p=out/SOURCE
    log=r63.r62.r23.run_lean(["--root="+str(ROOT),"-o",str(cap/(MODULE+".olean"))],p,source)
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(names)])
    newraw=raw_audit(log,{x["name"]:x for x in audit},names)
    mark="KUUOS_R75_COMPUTE "
    computations=[json.loads(l[len(mark):]) for l in log.splitlines() if l.startswith(mark)]
    v.need(len(computations)==2 and [x["index"] for x in computations]==[0,1],"R75 computation inventory")
    for item,x in zip(items,computations):
        v.need(all(x[k] is True for k in ("baseline_covered","missing_exact","correct_supply","partial_unsupplied",
                    "wrong_unsupplied","correct_recovers","partial_hold","wrong_ready_path_hold",
                    "conflict_unsupplied","conflict_existing_batch_hold")) and
               x["requirements_occurrences"]==len(item["required_bindings_occurrences"])==2+2*x["steps"] and
               x["steps"]==len(item["ordered_parent_patch_refs"]) and x["net_retired"]==len(item["retired"]) and
               x["net_introduced"]==len(item["introduced"]),"R75 actual obligation controls")
        item["lean_computation"]=x
    v.save(out/"recovery-computation.json",items)
    files=module_files(cap);install_module(cap,files)
    prior_rows=pd["fresh_application"]["observations"]
    all_rows=sorted(prior_rows+audit,key=lambda x:x["name"])
    v.need(len(all_rows)==len({x["name"] for x in all_rows})==344,"R75 accumulated declaration inventory")
    all_names=[x["name"] for x in all_rows]
    all_raw=expected_raw(out);v.need(set(all_raw).isdisjoint(newraw),"R75 no old proof replacement");all_raw.update(newraw)
    v.need(len(all_raw)==245,"R75 complete proof inventory")
    # Independently observe the imported proof graph; no parent elaboration.
    imported_source=VIEW_TEXT+"\n"+observer(out,sorted(all_raw))+v.suffix(all_names)
    ilog=r63.r62.r23.run_lean([],out/"CapsuleObservation.lean",imported_source)
    observed=v.read_direct(ilog,[{"name":x["name"],"expected_direct_refs":x["expected_direct_refs"]} for x in all_rows])
    v.need(len(observed)==344 and [x["name"] for x in observed]==all_names,"R75 all imported names")
    for arow,brow in zip(observed,all_rows):
        v.need(all(arow[k]==brow[k] for k in FIELDS),"R75 imported kernel difference "+brow["name"])
    iraw=raw_audit(ilog,{x["name"]:x for x in observed},all_raw)
    v.need({n:canonical_raw(x) for n,x in iraw.items()}=={n:canonical_raw(x) for n,x in all_raw.items()},
           "R75 full imported proof equality without expression normalization")
    replay={"observations":[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in observed],
            "raw_proof_digests":{n:digest(canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay)
    (out/VIEW).write_text(VIEW_TEXT,encoding="utf-8")
    manifest={"schema":"kuuos.codeai.r75.incremental-compiled-proof.v1","module":IMPORT_MODULE,
              "module_path":str(IMPORT_DIR/(MODULE+".olean")),"files":files,
              "parent_module":transport.IMPORT_MODULE,"parent_olean_sha256":PARENT_OLEAN,
              "parent_independent_run":RUN,"parent_imported_replay_digest":PARENT_REPLAY,
              "source_sha256":sha(p.read_bytes()),"view_sha256":sha((out/VIEW).read_bytes()),
              "imported_replay_digest":digest(replay),"imported_audits":344,"imported_complete_proofs":245,
              "parent_source_recompiled":False,"delta_compilation_count":1,"proof_authority":False,"action_authority":False}
    v.save(out/MANIFEST,manifest)
    after=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,before,after)
    v.save(out/"main-observations.json",{"before":before,"after":after})
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved","registry_authentication_proved",
      "unknown_registration_is_refutation","registry_updated","automatic_registration_authority","batch_applied_to_live_registry",
      "registration_correctness_implied_by_readiness","execution_history_order_independent","automatic_recovery_authority","minimal_batch_constructor_proved")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,
        "future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.registry-recovery-obligations.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_readiness_path_key":KEY,"r74_direct_digest":DIRECT,"r74_mcp_digest":MCP,"r74_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
        "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "formal_source_sha256":sha(formal.encode()),"application_source_sha256":sha(app.encode()),
        "computation_source_sha256":sha(compute.encode()),"delta_source_sha256":manifest["source_sha256"],
        "recovery_paths":items,"empty_inventory_holds":parent["empty_inventory_holds"],
        "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
        "raw_theorems":newraw,"formal_observations":{x["name"]:x for x in audit},**boundary})
    v.save(out/NEW,record)
    result={"status":"R75_DIRECT_RECOVERY_OBLIGATIONS","source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,
        "scope_digest":old.SCOPE,"parent_readiness_path_key":KEY,"recovery_path_key":record["key"],
        "r74_direct_digest":DIRECT,"r74_mcp_digest":MCP,"r74_diagnostic_coverage_digest":PARENT_DIAGNOSTICS,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "capsule_manifest":pd["capsule_manifest"],"joint_capsule_manifest":pd["joint_capsule_manifest"],
        "parent_olean_sha256":PARENT_OLEAN,"parent_imported_replay_digest":PARENT_REPLAY,
        "audit_capsule_digest":digest(manifest),"imported_replay_digest":digest(replay),
        "general_theorems":13,"actual_recovery_theorems":4,"actual_path_count":2,"empty_inventory_hold_count":5,
        "actual_computations":computations,"formal_source_sha256":record["formal_source_sha256"],
        "application_source_sha256":record["application_source_sha256"],"computation_source_sha256":record["computation_source_sha256"],
        "delta_source_sha256":manifest["source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in newraw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:digest(x) for n,x in newraw.items()},"parent_source_recompiled":False,
        "delta_compilation_count":1,"parent_raw_replay_bytewise_equal":True,"imported_complete_proofs":245,
        "deletion_basis_only_no_inverse_retained":True,"net_history_collision_retained":True,"original_patch_history_retained":True,
        "capsule_rebuilds":0,"active_dispatches":0,"new_root_discovery_trials":0,**boundary,
        "fresh_application":{"observations":all_rows,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R75_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest","raw_theorem_digests")}|
        {"direct_digest":digest(result),"audits":len(all_rows)},sort_keys=True),flush=True)
    print("KUUOS_R75_COMPILED",json.dumps(manifest,sort_keys=True),flush=True)
    return result

def check_capsule(out,d):
    m=load(out/MANIFEST);r=load(out/REPLAY)
    v.need(m["schema"]=="kuuos.codeai.r75.incremental-compiled-proof.v1" and m["module"]==IMPORT_MODULE and
           m["module_path"]==str(IMPORT_DIR/(MODULE+".olean")) and m["files"]==module_files(out/CAP) and
           m["parent_olean_sha256"]==PARENT_OLEAN and m["parent_module"]==transport.IMPORT_MODULE and
           m["parent_imported_replay_digest"]==PARENT_REPLAY and m["parent_independent_run"]==RUN and
           m["source_sha256"]==sha((out/SOURCE).read_bytes())==d["delta_source_sha256"] and
           (out/SOURCE).read_bytes()==d["fresh_application"]["mcp_source"].encode() and
           (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m["view_sha256"]==sha((out/VIEW).read_bytes()) and
           digest(m)==d["audit_capsule_digest"] and digest(r)==m["imported_replay_digest"]==d["imported_replay_digest"] and
           m["imported_audits"]==344 and m["imported_complete_proofs"]==245 and
           m["parent_source_recompiled"] is False and m["delta_compilation_count"]==1 and
           m["proof_authority"] is False and m["action_authority"] is False,"R75 exact incremental manifest")
    v.need(r["observations"]==[{"name":x["name"],**{k:x[k] for k in FIELDS}} for x in d["fresh_application"]["observations"]],
           "R75 exact imported replay metadata")
    raw=expected_raw(out);raw.update(load(out/NEW)["raw_theorems"])
    v.need(len(raw)==245 and r["raw_proof_digests"]=={n:digest(canonical_raw(x)) for n,x in raw.items()},
           "R75 exact imported complete proof digests")
    return m,r


# R75: exact same full source, separate complete error and warning reports.
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
    v.need(p.read_bytes()==load(out/"direct.json")["fresh_application"]["mcp_source"].encode(),"R75 exact direct receipt source")
    entries=[]
    for severity,name in DIAG_FILES:
        args={"file_path":rel,"timeout_s":DIAG_TIMEOUT,"severity":severity}
        raw=v.call_tool(client,"lean_diagnostic_messages",args)
        v.save(out/name,raw)
        # Never treat a timeout or filtered error/warning as success.
        diag=v.structured(raw)
        print("KUUOS_R75_DIAGNOSTIC",json.dumps({"severity":severity,"success":diag.get("success"),
             "partial":diag.get("partial"),"timed_out":diag.get("timed_out"),
             "still_elaborating_lines":diag.get("still_elaborating_lines"),
             "item_count":len(diag.get("items",[])),
             "failed_dependencies":diag.get("failed_dependencies")},sort_keys=True),flush=True)
        v.need(complete_diagnostic(raw),"R75 incomplete or non-clean full-source "+severity+" diagnostic")
        entries.append({"severity":severity,"file":name,"request":args,
                        "raw_sha256":sha((out/name).read_bytes())})
    manifest={"schema":"kuuos.codeai.r75.complete-severity-diagnostics.v1",
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
           manifest["schema"]=="kuuos.codeai.r75.complete-severity-diagnostics.v1" and
           manifest["mcp_version"]==v.EXPECTED_SERVER_VERSION and
           manifest["pinned_diagnostics_api_blob"]==DIAG_API_BLOB and
           manifest["pinned_diagnostics_processor_blob"]==DIAG_PROCESS_BLOB and
           manifest["timeout_s_per_call"]==DIAG_TIMEOUT and manifest["client_timeout_s"]==DIAG_CLIENT_TIMEOUT and
           all(manifest[k] is True for k in ("full_source","no_line_or_declaration_filter","all_error_and_warning_severities",
                                            "info_and_hint_not_transferred")) and
           len(manifest["receipts"])==2,"R75 complete diagnostic scope and exact source")
    for entry,(severity,name) in zip(manifest["receipts"],DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r75/RegistryRecoveryR75.lean",
                                  "timeout_s":DIAG_TIMEOUT,"severity":severity} and
               entry["raw_sha256"]==sha((first/name).read_bytes()) and complete_diagnostic(load(first/name)),
               "R75 actual complete full-source diagnostic "+severity)
    return manifest



def mcp(out):
    d=load(out/"direct.json");manifest,replay=check_capsule(out,d)
    installed_matches(manifest["files"])
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(digest(pd)==DIRECT and digest(pm)==MCP and pm["direct_digest"]==DIRECT and
           pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R75 certified parent MCP")
    parent_rows={r["name"]:(j,r) for j,r in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==327 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R75 distinct audit inventory")
    p=out/SOURCE
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp"]
    version=v.server_version(cmd,ROOT)
    client=transport.new_client("KuuOS R75 delta source diagnostics")
    try:
        coverage=run_complete_diagnostics(client,str(p.relative_to(ROOT)),out,p)
    finally:
        client.close()
    client=transport.new_client("KuuOS R75 compiled delta axiom audits")
    rows=[];origins=[];rel=str((out/VIEW).relative_to(ROOT))
    try:
        for j,row in enumerate(d["fresh_application"]["observations"]):
            name=row["name"];dest=out/f"mcp-verify-{j}.json"
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(prior==row and d["parent_raw_replay_bytewise_equal"],"R75 exact prior row")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,dest);raw=load(dest)
                origin={"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140947604835,
                        "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":sha(dest.read_bytes())}
            else:
                v.need(name in d["new_theorem_names"],"R75 new audit identity")
                installed_matches(manifest["files"])
                args={"file_path":rel,"theorem_name":name,"scan_source":False}
                print("KUUOS_R75_VERIFY_START",json.dumps(args,sort_keys=True),flush=True)
                raw=client.request("tools/call",{"name":"lean_verify","arguments":args})
                v.save(dest,raw)
                v.need(raw["result"]["isError"] is False,"R75 actual lean_verify failed "+name)
                origin={"name":name,"mode":"fresh_actual_mcp","receipt_sha256":sha(dest.read_bytes()),
                        "request":args,"audit_capsule_digest":digest(manifest),"audit_view_sha256":manifest["view_sha256"]}
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R75 actual MCP audit "+name)
            rows.append({"name":name,"axioms":ax});origins.append(origin)
    finally:
        client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==327 and fresh==17 and len(rows)==344,"R75 exact MCP count")
    installed_matches(manifest["files"])
    result={"status":"R75_REAL_MCP_GREEN","direct_digest":digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_source_scope":"new_delta_module_with_certified_parent_import",
            "diagnostic_coverage_digest":digest(coverage),"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version,
            "audit_transport":"incremental_compiled_import_exact_replay","audit_capsule_digest":digest(manifest),
            "audit_view_sha256":manifest["view_sha256"],"imported_replay_digest":digest(replay)}
    v.save(out/"mcp.json",result)
    print("KUUOS_R75_MCP",json.dumps({"mcp_digest":digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True,
          "audit_transport":result["audit_transport"],"diagnostic_scope":result["diagnostic_source_scope"]},sort_keys=True),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    current,replay=check_capsule(out,d);prior,first_replay=check_capsule(first,a)
    v.need(a==d and prior==current and replay==first_replay and mp["status"]=="R75_REAL_MCP_GREEN" and
           mp["direct_digest"]==digest(d) and mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==327 and
           mp["new_audit_count"]==17 and mp["fresh_full_source_diagnostics"] is True and
           mp["audit_transport"]=="incremental_compiled_import_exact_replay" and mp["audit_capsule_digest"]==digest(prior) and
           mp["audit_view_sha256"]==prior["view_sha256"] and mp["imported_replay_digest"]==digest(replay) and
           mp["diagnostic_source_scope"]=="new_delta_module_with_certified_parent_import","R75 independent receipt and exact compiled replay")
    coverage=verify_complete_diagnostics(first,d,mp)
    for name in ("mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(first/name,out/name)
    parent=out/PARENT_FOLDER;pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(origins)==len(rows)==344,"R75 independent MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        p=first/f"mcp-verify-{j}.json";raw=load(p);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==origin["name"] and origin["receipt_sha256"]==sha(p.read_bytes()),
               "R75 actual MCP receipt")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140947604835 and
                   pd["fresh_application"]["observations"][k]==row and origin["prior_origin"]==pm["audit_origins"][k] and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==p.read_bytes(),"R75 reused receipt identity")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"] and
                   origin["request"]=={"file_path":"artifacts/olean-r75/"+VIEW,"theorem_name":row["name"],"scan_source":False} and
                   origin["audit_capsule_digest"]==digest(prior) and origin["audit_view_sha256"]==prior["view_sha256"],
                   "R75 fresh compiled audit identity")
            fresh+=1
    v.need(reused==327 and fresh==17,"R75 independent counts")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        ob=load(folder/"main-observations.json");r69.observation_pair_valid(scope,ob["before"],ob["after"])
    for name in FILES+(NEW,"direct.json","historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                       "formal-source.lean","recovery-application.lean","recovery-computation.lean","recovery-computation.json",
                       SOURCE,VIEW,MANIFEST,REPLAY,"CapsuleObservation.lean",*HIST_RAW):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"R75 independent exact bytes "+name)
    for folder in (CAP,PARENT_CAP,"capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,75))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"R75 parent and compiled bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R75_INDEPENDENT_RECOVERY_OBLIGATIONS_GREEN","direct_digest":digest(d),
        "mcp_digest":digest(mp),"mcp_audits":344,"mcp_new_audits":17,"mcp_reused_audits":327,
        "fresh_full_source_mcp_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
        "diagnostic_source_scope":"new_delta_module_with_certified_parent_import","diagnostic_coverage_digest":digest(coverage),
        "recovery_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"compiled_file_bytes_equal":True,
        "imported_replay_equal":True,"parent_source_recompiled":False,"independent_delta_compilation_count":1,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R75_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r74-local","r74-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out==ROOT/"artifacts/olean-r75","R75 exact isolated module path")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
