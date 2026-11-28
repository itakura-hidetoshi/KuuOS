#!/usr/bin/env python3
"""R71: registered key-to-basis binding with exact MCP receipt lineage."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_context_keyed_basis_path_v1_r70 as r70
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
RUN=46109656399
HEAD="4743c0a28dc452e216f3257a68350589f92bcfd3"
DIRECT="89aef2ca1b34360570985a684fb6d3bf0ad45b5adf473341ecf6f8efb27399ef"
MCP="7164e6f53805ac0f15e9980c0d7d45e550d416c3d99356ab770a9297fb1cf83c"
KEY="5b99682bf0370f3a18b495fde15446f320418318f8657604d52c1777bb35bf09"
SCOPE=r69.SCOPE
BRIDGE=r69.BRIDGE
EXTENSION="e8bed0fde1244c49b7194db383a8516418ee2950adaa5ff5233997b5672d626d"
ARTS=((15249197219,"codeai-olean-r70-r2-local-46109656399-1","sha256:be2a3ca77f731397d6f8a7437a9167d68926f9c071f5a570ff8f540f8b5e8d81"),
      (15249398295,"codeai-olean-r70-r2-independent-46109656399-1","sha256:0a720592c742e6de50d80ac00b8f4540826682e23cd55ce130ae9640db3cd8ec"))
FILES=r70.FILES+(r70.NEW,)
NEW="registered-basis-path-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_registered_basis_path_v1.lean"
NS="KuuOSR71."
GENERAL=("registry_check_iff","registered_steps_append","registered_step_mem","checked_registered_iff",
         "checked_registered_of_checks","checked_registered_projection","checked_registered_reject_source",
         "checked_registered_reject_target","checked_registered_reject_steps","registered_binding_unique",
         "checked_registered_append","checked_registered_replay","unknown_key_alias")
REFS={
 "checked_registered_iff":[NS+"registry_check_iff","KuuOSR70.checked_tagged_iff"],
 "checked_registered_projection":[NS+"checked_registered_iff","KuuOSR70.checked_tagged_iff"],
 "checked_registered_reject_steps":[NS+"registry_check_iff"],
 "checked_registered_append":[NS+"checked_registered_iff",NS+"registered_steps_append",NS+"registry_check_iff",
     NS+"checked_registered_of_checks",NS+"checked_registered_projection","KuuOSR70.checked_tagged_append"],
 "checked_registered_replay":[NS+"checked_registered_projection","KuuOSR70.checked_tagged_replay"],
 "unknown_key_alias":[NS+"checked_registered_reject_source","KuuOSR70.checked_tagged_exact"],
}

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R70 R2 run")
    for jid,steps in ((140870125180,["Verify R70 R2 context keyed basis path","Actual Lean MCP R70 R2 new declarations and exact prior receipt reuse"]),
                      (140872516879,["Independently verify R70 R2 context keyed basis path"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R70 R2 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R70 R2 artifact")
    local=a.r70_local;other=a.r70_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R70_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R70_INDEPENDENT_CONTEXT_KEYED_BASIS_PATH_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==263 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","keyed_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R70 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==263 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R70 R2 actual MCP audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r70.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_path_key"]==load(out/r69.NEW)["key"],"R70 R2 key")
    v.need(record["historical_research_only"] and record["future_additions_observation_only"] and
           record["live_main_admission"] is False and record["current_main_certification_transferred"] is False and
           d["historical_scope_digest"]==record["historical_scope_digest"]==SCOPE==old.digest(scope) and
           d["script_bridge_digest"]==BRIDGE==old.digest(bridge) and
           d["r69_additive_observation_digest"]==record["r69_additive_observation_digest"]==EXTENSION==old.digest(extension) and
           d["deletion_basis_only_no_inverse_retained"] and d["net_history_collision_retained"] and
           d["original_patch_history_retained"] and len(record["keyed_paths"])==2 and d["identity_authentication_proved"] is False and d["empty_inventory_hold_count"]==5,"R70 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R70 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R70 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r70-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other),("McpApplication.lean",local)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","formal-source-r1.lean","r70-r2-repair.json",
                 "keyed-application.lean","keyed-computation.lean","keyed-computation.json","historical-scope.json",
                 "script-bridge.json","script-observation-bridge-r69.json",
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,70))):
        r63.copy_equal(local/name,other/name,receipts/name)
    repair=load(receipts/"r70-r2-repair.json")
    v.need(repair["r1_all_propositions_unchanged"] and repair["r1_kernel_types_equal"] and
           repair["r1_prior_raw_replay_equal"] and repair["r1_actual_computations_equal"] and
           repair["r1_computation_bytes_equal"] and len(repair["r1_sorryAx_affected_declarations"])==14 and
           repair["r2_sorryAx_affected_declarations"]==[] and
           load(receipts/"script-observation-bridge-r69.json")==extension and
           load(receipts/"script-bridge.json")==bridge and load(receipts/"historical-scope.json")==scope,
           "R70 repair lineage")
    v.need(r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"keyed-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"keyed-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"keyed-computation.json")==record["keyed_paths"] and
           (receipts/"McpApplication.lean").read_text(encoding="utf-8")==d["fresh_application"]["mcp_source"],"R70 exact source lineage")
    v.need(mp["parent_mcp_digest"]==r70.MCP and mp["reused_audit_count"]==247 and mp["new_audit_count"]==16 and
           mp["fresh_full_source_diagnostics"] is True and len(mp["audit_origins"])==263 and
           ind["mcp_reused_audits"]==247 and ind["mcp_new_audits"]==16,"R70 precise MCP origin counts")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R69 live observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    diag_raw=load(local/"mcp-diagnostics.json");diag=v.structured(diag_raw)
    v.need(diag_raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False and
           diag["timed_out"] is False and diag["failed_dependencies"]==[] and
           not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R70 actual MCP diagnostics")
    shutil.copyfile(local/"mcp-diagnostics.json",receipts/"mcp-diagnostics.json")
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json"
        raw=load(local/name);val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"]==mp["audit_origins"][j]["name"] and
               mp["audit_origins"][j]["receipt_sha256"]==r63.r62.r23.sha((local/name).read_bytes()),"R70 actual MCP per-declaration evidence")
        shutil.copyfile(local/name,receipts/name)
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW),(68,r68.NEW),(69,r69.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R69 ancestor raw lineage")
    for i in range(54,70):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r70.raw_observer(names).replace("KUUOS_R70_RAW ","KUUOS_R71_RAW ").replace("R70 theorem","R71 theorem").replace("R70 not a theorem","R71 not a theorem").replace("R70 proof unavailable","R71 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R71_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R71_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R71 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R71 raw proof")
    return result

def registry_sources(ledger,parent,patch_record):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=patch_record["patches"];by_digest={old.digest(p):p for p in patches}
    v.need(len(rows)==7 and len(by_digest)==2 and len(parent["keyed_paths"])==2 and len(ledger["empty_inventory_holds"])==5,"R71 inventory")
    idx={"global_boundary":2,"global_default":3,"global_probes":6}
    def fs(case):return {tuple(x) for x in rows[case]["encoded_cuts"]}
    def basis(case):return "((KuuOSR63.cuts_"+str(idx[case])+".map List.toFinset).toFinset)"
    def key(pair):return "("+json.dumps(pair[0])+", "+json.dumps(pair[1])+")"
    def literal(xs):return "(("+json.dumps([list(x) for x in sorted(xs)])+" : List (List Nat)).map List.toFinset).toFinset"
    # Bind registry to the separately admitted R67 patch endpoint inventory
    # and R63 exact basis data; do not manufacture it from the supplied walk.
    bindings={}
    for p in patches:
        for c,r in ((p["source_case"],p["source_request_id"]),(p["target_case"],p["target_request_id"])):
            k=(p["context_id"],r)
            v.need(c in idx and (k not in bindings or bindings[k]==c),"R71 unique recorded binding")
            bindings[k]=c
    v.need(len(bindings)==3 and set(bindings.values())==set(idx),"R71 three registered endpoints")
    ordered=sorted(bindings.items())
    src=["namespace KuuOSR71","def observedRegistry (k : String × String) : Option (KuuOSR69.Basis Nat) :="]
    for k,c in ordered:src.append("  if k = "+key(k)+" then some "+basis(c)+" else")
    src.append("  none")
    compute=["namespace KuuOSR71"]
    items=[];refs={}
    def step(sk,tk,s,t,R,N):
        return "({ sourceKey := "+sk+", targetKey := "+tk+", patch := { source := "+basis(s)+", target := "+basis(t)+", retired := "+literal(R)+", introduced := "+literal(N)+" } } : KuuOSR70.TaggedStep (String × String) Nat)"
    for i,path in enumerate(parent["keyed_paths"]):
        pairs=[tuple(k) for k in path["ordered_context_request_keys"]];nodes=path["ordered_cases"];edges=path["ordered_parent_patch_refs"]
        v.need(path["index"]==i and len(pairs)==len(nodes)==len(edges)+1 and len(edges)==(3 if i==0 else 4) and
               all(bindings.get(k)==c for k,c in zip(pairs,nodes)) and path["lean_computation"]["recorded_tagged_exact"],"R70 exact registered path")
        keys=[key(k) for k in pairs];literals=[]
        for j,e in enumerate(edges):
            p=by_digest[e["digest"]]
            s,t=p["source_case"],p["target_case"];sid,tid=p["source_request_id"],p["target_request_id"]
            R={tuple(x) for x in p["retired"]};N={tuple(x) for x in p["introduced"]}
            v.need(e["direction"] in ("forward","rollback"),"R71 direction")
            if e["direction"]=="rollback":s,t,sid,tid,R,N=t,s,tid,sid,N,R
            v.need((s,t)==tuple(nodes[j:j+2]) and ((p["context_id"],sid),(p["context_id"],tid))==tuple(pairs[j:j+2]) and
                   (sid,tid)==(e["source_request_id"],e["target_request_id"]) and R==fs(s)-fs(t) and N==fs(t)-fs(s),"R71 patch binding")
            literals.append(step(keys[j],keys[j+1],s,t,R,N))
        f,h=basis(nodes[0]),basis(nodes[-1]);R,N=fs(nodes[0])-fs(nodes[-1]),fs(nodes[-1])-fs(nodes[0])
        v.need(R=={tuple(x) for x in path["retired"]} and N=={tuple(x) for x in path["introduced"]},"R70 net identity")
        start="("+keys[0]+", "+f+")"
        ends="["+", ".join("("+k+", "+basis(c)+")" for k,c in zip(keys[1:],nodes[1:]))+"]"
        walk="(KuuOSR70.taggedWalk "+start+" "+ends+")"
        name="actual_registered_path_"+str(i)
        src += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                "theorem "+name+" :",
                "  checkedRegisteredPath observedRegistry "+keys[0]+" "+keys[-1]+" "+f+" "+h+" "+walk+" =",
                "    some ("+f+" \\ "+h+", "+h+" \\ "+f+") :=",
                "  checked_registered_of_checks observedRegistry "+keys[0]+" "+keys[-1]+" "+f+" "+h+" "+walk+" _",
                "    (by decide) (by decide) (by decide) KuuOSR70.actual_tagged_path_"+str(i)]
        refs[NS+name]=[NS+"checked_registered_of_checks","KuuOSR70.actual_tagged_path_"+str(i)]
        unknown=key(("UNREGISTERED_CONTEXT",pairs[0][1]))
        v.need(("UNREGISTERED_CONTEXT",pairs[0][1]) not in bindings and pairs[1]!=pairs[0] and fs(nodes[1])!=fs(nodes[0]),"R71 nontrivial controls")
        alias="actual_unregistered_alias_"+str(i)
        src += ["theorem "+alias+" :",
                "  KuuOSR70.checkedTaggedPath "+unknown+" "+unknown+" "+f+" "+f+" [] =",
                "    some ((∅ : KuuOSR69.Basis Nat), (∅ : KuuOSR69.Basis Nat)) ∧",
                "  checkedRegisteredPath observedRegistry "+unknown+" "+unknown+" "+f+" "+f+" [] = none :=",
                "  unknown_key_alias observedRegistry "+unknown+" "+f+" (by decide)"]
        refs[NS+alias]=[NS+"unknown_key_alias"]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let h := "+h,
                    "  let path : List (KuuOSR70.TaggedStep (String × String) Nat) := ["+", ".join(literals)+"]",
                    "  let firstKey := "+keys[0],"  let lastKey := "+keys[-1],"  let middleKey := "+keys[1],
                    "  let unknownKey := "+unknown,
                    "  let missingMiddle := fun k : String × String => if k = middleKey then none else observedRegistry k",
                    "  let wrongMiddle := fun k : String × String => if k = middleKey then some f else observedRegistry k",
                    "  let missingSource := fun k : String × String => if k = firstKey then none else observedRegistry k",
                    "  let r := "+literal(R),"  let n := "+literal(N),
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("steps", Lean.toJson path.length),',
                    '    ("registered_exact", Lean.toJson (decide (checkedRegisteredPath observedRegistry firstKey lastKey f h path = some (r,n)))),',
                    '    ("canonical_registered_exact", Lean.toJson (decide (checkedRegisteredPath observedRegistry firstKey lastKey f h '+walk+' = some (r,n)))),',
                    '    ("missing_middle_hold", Lean.toJson (decide (checkedRegisteredPath missingMiddle firstKey lastKey f h path = none))),',
                    '    ("wrong_middle_basis_hold", Lean.toJson (decide (checkedRegisteredPath wrongMiddle firstKey lastKey f h path = none))),',
                    '    ("missing_source_hold", Lean.toJson (decide (checkedRegisteredPath missingSource firstKey lastKey f h path = none))),',
                    '    ("unknown_alias_hold", Lean.toJson (decide (checkedRegisteredPath observedRegistry unknownKey unknownKey f f [] = none))),',
                    '    ("unregistered_tagged_accepts", Lean.toJson (decide (KuuOSR70.checkedTaggedPath firstKey lastKey f h path = some (r,n)))),',
                    '    ("unknown_alias_tagged_accepts", Lean.toJson (decide (KuuOSR70.checkedTaggedPath unknownKey unknownKey f f [] = some ((∅ : KuuOSR69.Basis Nat), (∅ : KuuOSR69.Basis Nat)))))),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R71_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"parent_keyed_path_digest":old.digest(path),
            "registry":[{"key":list(k),"case":c,"basis_digest":old.digest([list(x) for x in sorted(fs(c))])} for k,c in ordered],
            "ordered_context_request_keys":[list(k) for k in pairs],"ordered_cases":nodes,"ordered_parent_patch_refs":edges,
            "retired":path["retired"],"introduced":path["introduced"],"theorems":[NS+name,NS+alias],
            "path_history_retained":True,"counterfactual_only":True,"action_authority":False,"registry_authentication_proved":False})
    return "\n".join(src+["end KuuOSR71",""]),"\n".join(compute+["end KuuOSR71",""]),items,refs

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope)
    extension=r69.additive_bridge(scope,bridge)
    v.need(old.digest(extension)==EXTENSION,"R71 exact parent observation bridge")
    start_main=r69.observe_live_r3(scope)
    v.save(out/"historical-scope.json",scope);v.save(out/"script-bridge.json",bridge)
    v.save(out/"script-observation-bridge-r69.json",extension)
    v.save(out/"main-observations.json",{"before":start_main})
    d,mp,ind,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=registry_sources(load(out/r63.NEW),parent,load(out/r67.NEW))
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"registry-application.lean").write_text(app,encoding="utf-8")
    (out/"registry-computation.lean").write_text(compute,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(n for x in items for n in x["theorems"])
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
            for line in p.with_suffix(".log").read_text(encoding="utf-8").splitlines():
                if line.startswith("/home/") and ("error:" in line or "error(" in line or "warning:" in line):
                    print(line[:6000],flush=True)
        raise
    finally:
        for path in (p,p.with_suffix(".log")):
            if path.is_file():shutil.copyfile(path,out/path.name)
    marker="KUUOS_RECALL_KERNEL "
    kernel=[json.loads(x[len(marker):]) for x in log.splitlines() if x.startswith(marker)]
    missing={x["name"]:sorted(set(expected[x["name"]])-set(x["proof_constants"])) for x in kernel
             if x["name"] in expected and set(expected[x["name"]])-set(x["proof_constants"])}
    v.need(not missing,"R71 missing direct reference "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R70 full audit drift")
    for i,layer,checker in ((70,r70.NEW,r70.raw_audit),(69,r69.NEW,r69.raw_audit),(68,r68.NEW,r68.raw_audit),(67,r67.NEW,r67.raw_audit),
                            (66,r66.NEW,r66.raw_audit),(65,r65.NEW,r65.raw_audit),(64,r64.NEW,r64.raw_audit),(63,r63.NEW,r63.raw_audit)):
        previous=checker(log,by,tuple(load(out/("parent-r"+str(i)+"-receipts")/"direct.json")["new_theorem_names"]))
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),previous)
        v.need(previous==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous62==load(out/r63.r62.NEW)["raw_theorems"],"R62 raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R71_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"R71 computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("registered_exact","canonical_registered_exact","missing_middle_hold",
                  "wrong_middle_basis_hold","missing_source_hold","unknown_alias_hold","unregistered_tagged_accepts",
                  "unknown_alias_tagged_accepts")) and x["steps"]==len(item["ordered_parent_patch_refs"]) and
               x["net_retired"]==len(item["retired"]) and x["net_introduced"]==len(item["introduced"]),
               "R71 exact tagged paths and identity controls")
        item["lean_computation"]=x
    v.need(len(audit)==263+len(names)==280 and r66.observe_historical_scope()==scope and
           r68.script_bridge(scope)==bridge and r69.additive_bridge(scope,bridge)==extension,"R71 scope")
    end_main=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,start_main,end_main)
    v.save(out/"main-observations.json",{"before":start_main,"after":end_main})
    v.save(out/"registry-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved","registry_authentication_proved","unknown_registration_is_refutation")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,
        "future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.context-registry-basis-path.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_keyed_path_key":KEY,"r70_direct_digest":DIRECT,"r70_mcp_digest":MCP,"historical_scope_digest":SCOPE,
        "script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),"application_source_sha256":r63.r62.r23.sha(app.encode()),
        "computation_source_sha256":r63.r62.r23.sha(compute.encode()),"registered_paths":items,
        "empty_inventory_holds":parent["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_retained":True,"original_patch_history_retained":True,
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R71_DIRECT_REGISTERED_BASIS_PATH",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_keyed_path_key":KEY,"registered_path_key":record["key"],"r70_direct_digest":DIRECT,"r70_mcp_digest":MCP,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_registered_theorems":len(names)-len(GENERAL),"actual_path_count":len(items),
        "empty_inventory_hold_count":5,"actual_computations":computations,"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_retained":True,"original_patch_history_retained":True,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R71_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
        {"direct_digest":old.digest(result),"audits":len(audit)},sort_keys=True),flush=True)
    return result


# R71 R3: exact same full source, separate complete error and warning reports.
# MCP v0.30.0 tools/diagnostics.py calls full-file client.diagnostics before
# applying the severity filter in diagnostic_utils.py. No line or declaration
# range is supplied. Partial reports are never admitted.
DIAG_TIMEOUT=600
DIAG_CLIENT_TIMEOUT=900
DIAG_API_BLOB="fc6e94a4c1798cd18e63cbb59e163eab60247954"
DIAG_PROCESS_BLOB="ebbf0588f1678b953761f470ab060757e87c9708"
DIAG_FILES=(("error","mcp-diagnostics.json"),("warning","mcp-diagnostics-warning.json"))
R2_MCP_SOURCE_SHA="09f1bc7c1d309a2e243244ce64e388000e0cf435fca03f9c2206ad5b520e1131"

def complete_diagnostic(raw):
    diag=v.structured(raw)
    return (raw["result"]["isError"] is False and diag["success"] is True and
            diag["partial"] is False and diag["timed_out"] is False and
            not diag.get("still_elaborating_lines") and diag["failed_dependencies"]==[] and diag["items"]==[])

def run_complete_diagnostics(client,rel,out,p):
    sha=r63.r62.r23.sha
    v.need(sha(p.read_bytes())==R2_MCP_SOURCE_SHA,"R71 R3 exact R2 MCP source")
    entries=[]
    for severity,name in DIAG_FILES:
        args={"file_path":rel,"timeout_s":DIAG_TIMEOUT,"severity":severity}
        raw=v.call_tool(client,"lean_diagnostic_messages",args)
        v.save(out/name,raw)
        # Never treat a timeout or filtered error/warning as success.
        diag=v.structured(raw)
        print("KUUOS_R71_R3_DIAGNOSTIC",json.dumps({"severity":severity,"success":diag.get("success"),
             "partial":diag.get("partial"),"timed_out":diag.get("timed_out"),
             "still_elaborating_lines":diag.get("still_elaborating_lines"),
             "item_count":len(diag.get("items",[])),
             "failed_dependencies":diag.get("failed_dependencies")},sort_keys=True),flush=True)
        v.need(complete_diagnostic(raw),"R71 R3 incomplete or non-clean full-source "+severity+" diagnostic")
        entries.append({"severity":severity,"file":name,"request":args,
                        "raw_sha256":sha((out/name).read_bytes())})
    manifest={"schema":"kuuos.codeai.r71.complete-severity-diagnostics.v1",
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
    source=(first/"McpApplication.lean").read_bytes()
    v.need(source==d["fresh_application"]["mcp_source"].encode() and
           sha(source)==R2_MCP_SOURCE_SHA==manifest["source_sha256"] and
           mp["diagnostic_coverage_digest"]==old.digest(manifest) and
           mp["diagnostic_scope"]=="full_source_error_and_warning" and
           manifest["schema"]=="kuuos.codeai.r71.complete-severity-diagnostics.v1" and
           manifest["mcp_version"]==v.EXPECTED_SERVER_VERSION and
           manifest["pinned_diagnostics_api_blob"]==DIAG_API_BLOB and
           manifest["pinned_diagnostics_processor_blob"]==DIAG_PROCESS_BLOB and
           manifest["timeout_s_per_call"]==DIAG_TIMEOUT and manifest["client_timeout_s"]==DIAG_CLIENT_TIMEOUT and
           all(manifest[k] is True for k in ("full_source","no_line_or_declaration_filter","all_error_and_warning_severities",
                                            "info_and_hint_not_transferred")) and
           len(manifest["receipts"])==2,"R71 R3 complete diagnostic scope and exact source")
    for entry,(severity,name) in zip(manifest["receipts"],DIAG_FILES):
        v.need(entry["severity"]==severity and entry["file"]==name and
               entry["request"]=={"file_path":"artifacts/olean-r71/McpApplication.lean",
                                  "timeout_s":DIAG_TIMEOUT,"severity":severity} and
               entry["raw_sha256"]==sha((first/name).read_bytes()) and complete_diagnostic(load(first/name)),
               "R71 R3 actual complete full-source diagnostic "+severity)
    return manifest


def mcp(out):
    d=load(out/"direct.json");x=d["fresh_application"]
    parent=out/"parent-r70-receipts";pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(old.digest(pd)==DIRECT and old.digest(pm)==MCP and pm["direct_digest"]==DIRECT,"R71 reuse parent receipt")
    parent_rows={row["name"]:(j,row) for j,row in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==263 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R71 distinct MCP inventory")
    p=out/"McpApplication.lean";p.write_text(x["mcp_source"],encoding="utf-8")
    rel=str(p.relative_to(ROOT))
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    v.need(pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R71 exact MCP version")
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=DIAG_CLIENT_TIMEOUT)
    rows=[];origins=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS registered basis path","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        coverage=run_complete_diagnostics(client,rel,out,p)
        for j,row in enumerate(x["observations"]):
            name=row["name"]
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(row==prior and d["parent_raw_replay_bytewise_equal"],"R71 identical prior direct observation")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,out/f"mcp-verify-{j}.json")
                raw=load(src)
                origins.append({"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140870125180,
                                "parent_audit_index":k,"prior_origin":pm["audit_origins"][k],"receipt_sha256":r63.r62.r23.sha(src.read_bytes())})
            else:
                v.need(name in d["new_theorem_names"],"R71 new audit identity")
                raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":name,"scan_source":False})
                v.save(out/f"mcp-verify-{j}.json",raw)
                origins.append({"name":name,"mode":"fresh_actual_mcp",
                                "receipt_sha256":r63.r62.r23.sha((out/f"mcp-verify-{j}.json").read_bytes())})
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R71 MCP axiom audit")
            rows.append({"name":name,"axioms":ax})
    finally:client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==263 and fresh==17 and len(rows)==280,"R71 new and reused MCP counts")
    result={"status":"R71_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"diagnostic_scope":"full_source_error_and_warning",
            "diagnostic_coverage_digest":old.digest(coverage),
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R71_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R71_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d) and
           mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==263 and mp["new_audit_count"]==17 and
           mp["fresh_full_source_diagnostics"] is True,"independent R71 receipt")
    coverage=verify_complete_diagnostics(first,d,mp)
    for name in ("McpApplication.lean","mcp-diagnostic-coverage.json","mcp-diagnostics.json","mcp-diagnostics-warning.json"):
        shutil.copyfile(first/name,out/name)
    parent=out/"parent-r70-receipts";pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(rows)==len(origins)==280,"R71 MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        path=first/f"mcp-verify-{j}.json";raw=load(path);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"]==origin["name"] and
            origin["receipt_sha256"]==r63.r62.r23.sha(path.read_bytes()),"R71 MCP evidence")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140870125180 and
                   pd["fresh_application"]["observations"][k]==row and origin["prior_origin"]==pm["audit_origins"][k] and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==path.read_bytes(),"R71 exact historical MCP bytes")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"],"R71 new MCP receipt")
            fresh+=1
    v.need(reused==263 and fresh==17,"R71 independent exact reuse count")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        obs=load(folder/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R71 observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
    for name in FILES+(NEW,"historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                      "formal-source.lean","registry-application.lean","registry-computation.lean","registry-computation.json",
                      *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,71))):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R71 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,71))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R71_INDEPENDENT_REGISTERED_BASIS_PATH_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),"mcp_new_audits":fresh,
        "mcp_reused_audits":reused,"fresh_full_source_mcp_diagnostics":True,
        "diagnostic_scope":"full_source_error_and_warning","diagnostic_coverage_digest":old.digest(coverage),
        "registry_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R71_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r70-local","r70-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
