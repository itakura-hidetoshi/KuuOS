#!/usr/bin/env python3
"""R70: exact context/request keyed path admission with reused old MCP receipts."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_checked_basis_path_v1_r69_r3_core as r69
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
RUN=46106329503
HEAD="11ccb9c9a9d11d94366c20527dbb2e030c811fdc"
DIRECT="ae92d3e8db3999d0a4077a1b9f6016861d3fc8f9ff5e33bdb82dbfe3c3a59dda"
MCP="b6959a7f8bb030c87aa17f3a996111e4f31dc99b5c9504e911273763505a22c9"
KEY="4f6b4b0c48bb26278302d5e0fd9ce182a139dd58633861d524ccf77d3461947d"
SCOPE=r69.SCOPE
BRIDGE=r69.BRIDGE
EXTENSION="e8bed0fde1244c49b7194db383a8516418ee2950adaa5ff5233997b5672d626d"
ARTS=((15248645864,"codeai-olean-r69-r3-local-46106329503-1","sha256:7460212e064a823d14966f855881365539560bd11303fc1241f3d3105c92beb1"),
      (15248293305,"codeai-olean-r69-r3-independent-46106329503-1","sha256:fd93cfe398a956cf042a85536fef8e05fbe9b8ba31788fd5928997b7682cc164"))
FILES=r69.FILES+(r69.NEW,)
NEW="context-keyed-basis-path-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_context_keyed_basis_path_v1.lean"
NS="KuuOSR70."
GENERAL=("key_check_iff","checked_tagged_iff","checked_tagged_exact","checked_tagged_projection",
         "checked_tagged_reject_keys","checked_tagged_reject_source","equal_basis_wrong_key","keys_append_valid",
         "checked_tagged_append","tagged_walk_valid","tagged_walk_exact","checked_tagged_replay")
REFS={
 "checked_tagged_iff":[NS+"key_check_iff","KuuOSR69.checked_path_iff"],
 "checked_tagged_exact":[NS+"checked_tagged_iff"],
 "checked_tagged_projection":[NS+"checked_tagged_iff","KuuOSR69.checked_path_iff"],
 "checked_tagged_reject_keys":[NS+"key_check_iff"],
 "checked_tagged_reject_source":[NS+"checked_tagged_reject_keys"],
 "equal_basis_wrong_key":["KuuOSR69.checked_path_exact",NS+"checked_tagged_reject_keys"],
 "checked_tagged_append":[NS+"checked_tagged_iff",NS+"keys_append_valid",NS+"checked_tagged_exact",
                           "KuuOSR69.path_append_valid","KuuOSR68.compose_diff_exact"],
 "tagged_walk_valid":["KuuOSR67.checked_bound_exact"],
 "tagged_walk_exact":[NS+"checked_tagged_exact",NS+"tagged_walk_valid"],
 "checked_tagged_replay":[NS+"checked_tagged_projection","KuuOSR69.checked_path_replay"],
}

def admit(a,out,scope,bridge,extension):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R69 R3 run")
    for jid,steps in ((140859797615,["Verify R69 R3 checked basis path","Actual Lean MCP R69 R3 checked basis path audit"]),
                      (140865152624,["Independently verify R69 R3 checked basis path"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R69 R3 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R69 R3 artifact")
    local=a.r69_local;other=a.r69_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R69_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R69_INDEPENDENT_CHECKED_BASIS_PATH_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==247 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","path_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R69 R3 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==247 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R69 R3 actual MCP audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r69.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_chain_key"]==load(out/r68.NEW)["key"],"R69 R3 key")
    v.need(record["historical_research_only"] and record["future_additions_observation_only"] and
           record["live_main_admission"] is False and record["current_main_certification_transferred"] is False and
           d["historical_scope_digest"]==record["historical_scope_digest"]==SCOPE==old.digest(scope) and
           d["script_bridge_digest"]==BRIDGE==old.digest(bridge) and
           d["r69_additive_observation_digest"]==record["r69_additive_observation_digest"]==EXTENSION==old.digest(extension) and
           d["deletion_basis_only_no_inverse_retained"] and d["net_history_collision_certified"] and
           d["original_patch_history_retained"] and len(record["paths"])==2 and d["empty_inventory_hold_count"]==5,"R69 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R69 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R69 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r69-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other),("McpApplication.lean",local)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","path-application.lean","path-computation.lean","path-computation.json",
                 "path-computation-r1.lean","r69-r2-repair.json","r69-r3-repair.json","historical-scope.json",
                 "script-bridge.json","script-observation-bridge-r69.json",
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,69))):
        r63.copy_equal(local/name,other/name,receipts/name)
    repair=load(receipts/"r69-r3-repair.json")
    v.need(repair["r1_all_raw_proofs_equal"] and repair["r1_formal_and_application_unchanged"] and
           repair["r2_artifact_count"]==0 and repair["qualified_calls"]==4 and
           repair["additive_observation_digest"]==EXTENSION and repair["original_script_bridge_digest"]==BRIDGE and
           load(receipts/"script-observation-bridge-r69.json")==extension and
           load(receipts/"script-bridge.json")==bridge and load(receipts/"historical-scope.json")==scope,
           "R69 explicit repair lineage")
    v.need(r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"path-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"path-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"path-computation.json")==record["paths"] and
           (receipts/"McpApplication.lean").read_text(encoding="utf-8")==d["fresh_application"]["mcp_source"],"R69 exact source and path lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R69 live observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    diag_raw=load(local/"mcp-diagnostics.json");diag=v.structured(diag_raw)
    v.need(diag_raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False and
           diag["timed_out"] is False and diag["failed_dependencies"]==[] and
           not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R69 actual MCP diagnostics")
    shutil.copyfile(local/"mcp-diagnostics.json",receipts/"mcp-diagnostics.json")
    for j,row in enumerate(rows):
        name=f"mcp-verify-{j}.json"
        raw=load(local/name);val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
               normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
               row["name"]==mp["audits"][j]["name"],"R69 actual MCP per-declaration evidence")
        shutil.copyfile(local/name,receipts/name)
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW),(68,r68.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R69 ancestor raw lineage")
    for i in range(54,69):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r69.raw_observer(names).replace("KUUOS_R69_RAW ","KUUOS_R70_RAW ").replace("R69 theorem","R70 theorem").replace("R69 not a theorem","R70 not a theorem").replace("R69 proof unavailable","R70 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R70_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R70_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R70 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R70 raw proof")
    return result

def keyed_sources(ledger,parent,patch_record):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=patch_record["patches"]
    v.need(len(rows)==7 and len(patches)==2 and len(parent["paths"])==2 and len(ledger["empty_inventory_holds"])==5,"R70 scope")
    by_digest={old.digest(x):x for x in patches}
    v.need(len(by_digest)==2,"R70 patch identities")
    indices={"global_boundary":2,"global_default":3,"global_probes":6}
    def basis(case):return "((KuuOSR63.cuts_"+str(indices[case])+".map List.toFinset).toFinset)"
    def fs(case):return {tuple(x) for x in rows[case]["encoded_cuts"]}
    def literal(xs):return "(("+json.dumps([list(x) for x in sorted(xs)])+" : List (List Nat)).map List.toFinset).toFinset"
    def key(c,r):return "("+json.dumps(c)+", "+json.dumps(r)+")"
    def state(k,case):return "("+k+", "+basis(case)+")"
    def step(sk,tk,s,t,R,N):
        return "({ sourceKey := "+sk+", targetKey := "+tk+", patch := { source := "+basis(s)+", target := "+basis(t)+", retired := "+literal(R)+", introduced := "+literal(N)+" } } : TaggedStep (String × String) Nat)"
    src=["namespace KuuOSR70"]
    compute=["namespace KuuOSR70"]
    items=[];refs={}
    for i,path in enumerate(parent["paths"]):
        nodes=path["ordered_cases"];ids=path["ordered_request_ids"];ctx=path["context_id"]
        edges=path["ordered_parent_patch_refs"]
        v.need(path["index"]==i and path["path_history_retained"] and path["lean_computation"]["recorded_path_exact"] and
               len(nodes)==len(ids)==len(edges)+1 and len(edges)==(3 if i==0 else 4) and
               all(isinstance(z,str) and len(z)==64 and all(c in "0123456789abcdef" for c in z) for z in [ctx,*ids]),"R69 recorded key inventory")
        keys=[key(ctx,z) for z in ids]
        data=[];literals=[]
        for j,e in enumerate(edges):
            p=by_digest[e["digest"]]
            s,t=p["source_case"],p["target_case"];sid,tid=p["source_request_id"],p["target_request_id"]
            R={tuple(x) for x in p["retired"]};N={tuple(x) for x in p["introduced"]}
            v.need(e["direction"] in ("forward","rollback"),"R70 direction")
            if e["direction"]=="rollback":s,t,sid,tid,R,N=t,s,tid,sid,N,R
            v.need(p["context_id"]==ctx and (s,t)==tuple(nodes[j:j+2]) and (sid,tid)==tuple(ids[j:j+2]) and
                   (sid,tid)==(e["source_request_id"],e["target_request_id"]) and R==fs(s)-fs(t) and N==fs(t)-fs(s),
                   "R70 exact context/request and patch binding")
            data.append((s,t,R,N));literals.append(step(keys[j],keys[j+1],s,t,R,N))
        f,h=basis(nodes[0]),basis(nodes[-1]);R,N=fs(nodes[0])-fs(nodes[-1]),fs(nodes[-1])-fs(nodes[0])
        v.need(R=={tuple(x) for x in path["retired"]} and N=={tuple(x) for x in path["introduced"]},"R69 net identity")
        start=state(keys[0],nodes[0]);ends="["+", ".join(state(k,c) for k,c in zip(keys[1:],nodes[1:]))+"]"
        name="actual_tagged_path_"+str(i)
        src += ["theorem "+name+" :",
                "  checkedTaggedPath "+keys[0]+" "+keys[-1]+" "+f+" "+h+" (taggedWalk "+start+" "+ends+") =",
                "    some ("+f+" \\ "+h+", "+h+" \\ "+f+") :=",
                "  tagged_walk_exact "+start+" "+ends]
        refs[NS+name]=[NS+"tagged_walk_exact"]
        s,t,r,n=data[1]
        wrong_middle=list(literals);wrong_middle[1]=step(keys[0],keys[2],s,t,r,n)
        s,t,r,n=data[0]
        bad_context=list(literals);bad_context[0]=step(key("UNADMITTED_CONTEXT",ids[0]),keys[1],s,t,r,n)
        wrong_end=keys[1] if keys[0]==keys[-1] else keys[0]
        v.need(keys[0]!=keys[1] and wrong_end!=keys[-1],"R70 distinct key controls")
        alias="actual_equal_basis_wrong_key_"+str(i)
        src += ["theorem "+alias+" :",
                "  KuuOSR69.checkedPath "+f+" "+f+" [] = some ((∅ : KuuOSR69.Basis Nat), (∅ : KuuOSR69.Basis Nat)) ∧",
                "    checkedTaggedPath "+keys[0]+" "+keys[1]+" "+f+" "+f+" [] = none :=",
                "  equal_basis_wrong_key "+keys[0]+" "+keys[1]+" "+f+" (by decide)"]
        refs[NS+alias]=[NS+"equal_basis_wrong_key"]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let h := "+h,
                    "  let path : List (TaggedStep (String × String) Nat) := ["+", ".join(literals)+"]",
                    "  let badMiddle : List (TaggedStep (String × String) Nat) := ["+", ".join(wrong_middle)+"]",
                    "  let badContext : List (TaggedStep (String × String) Nat) := ["+", ".join(bad_context)+"]",
                    "  let r := "+literal(R),"  let n := "+literal(N),
                    "  let firstKey := "+keys[0],"  let lastKey := "+keys[-1],
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("steps", Lean.toJson path.length),',
                    '    ("recorded_tagged_exact", Lean.toJson (decide (checkedTaggedPath firstKey lastKey f h path = some (r,n)))),',
                    '    ("canonical_tagged_exact", Lean.toJson (decide (checkedTaggedPath firstKey lastKey f h (taggedWalk '+start+' '+ends+') = some (r,n)))),',
                    '    ("wrong_middle_key_hold", Lean.toJson (decide (checkedTaggedPath firstKey lastKey f h badMiddle = none))),',
                    '    ("wrong_context_hold", Lean.toJson (decide (checkedTaggedPath firstKey lastKey f h badContext = none))),',
                    '    ("wrong_end_key_hold", Lean.toJson (decide (checkedTaggedPath firstKey '+wrong_end+' f h path = none))),',
                    '    ("unkeyed_middle_still_accepts", Lean.toJson (decide (KuuOSR69.checkedPath f h (badMiddle.map TaggedStep.patch) = some (r,n)))),',
                    '    ("unkeyed_context_still_accepts", Lean.toJson (decide (KuuOSR69.checkedPath f h (badContext.map TaggedStep.patch) = some (r,n)))),',
                    '    ("equal_basis_alias_hold", Lean.toJson (decide (checkedTaggedPath firstKey '+keys[1]+' f f [] = none))),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R70_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"parent_path_digest":old.digest(path),"context_id":ctx,
                      "ordered_context_request_keys":[[ctx,z] for z in ids],"ordered_cases":nodes,
                      "ordered_parent_patch_refs":edges,"retired":path["retired"],"introduced":path["introduced"],
                      "theorems":[NS+name,NS+alias],"path_history_retained":True,
                      "counterfactual_only":True,"action_authority":False})
    return "\n".join(src+["end KuuOSR70",""]),"\n".join(compute+["end KuuOSR70",""]),items,refs

def direct(a,out):
    scope=r66.observe_historical_scope();bridge=r68.script_bridge(scope)
    extension=r69.additive_bridge(scope,bridge)
    v.need(old.digest(extension)==EXTENSION,"R70 exact parent observation bridge")
    start_main=r69.observe_live_r3(scope)
    v.save(out/"historical-scope.json",scope);v.save(out/"script-bridge.json",bridge)
    v.save(out/"script-observation-bridge-r69.json",extension)
    v.save(out/"main-observations.json",{"before":start_main})
    d,mp,ind,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=keyed_sources(load(out/r63.NEW),parent,load(out/r67.NEW))
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"keyed-application.lean").write_text(app,encoding="utf-8")
    (out/"keyed-computation.lean").write_text(compute,encoding="utf-8")
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
    v.need(not missing,"R70 missing direct reference "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R69 full audit drift")
    for i,layer,checker in ((69,r69.NEW,r69.raw_audit),(68,r68.NEW,r68.raw_audit),(67,r67.NEW,r67.raw_audit),
                            (66,r66.NEW,r66.raw_audit),(65,r65.NEW,r65.raw_audit),(64,r64.NEW,r64.raw_audit),(63,r63.NEW,r63.raw_audit)):
        previous=checker(log,by,tuple(load(out/("parent-r"+str(i)+"-receipts")/"direct.json")["new_theorem_names"]))
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),previous)
        v.need(previous==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous62==load(out/r63.r62.NEW)["raw_theorems"],"R62 raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R70_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"R70 computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("recorded_tagged_exact","canonical_tagged_exact","wrong_middle_key_hold",
                  "wrong_context_hold","wrong_end_key_hold","unkeyed_middle_still_accepts","unkeyed_context_still_accepts",
                  "equal_basis_alias_hold")) and x["steps"]==len(item["ordered_parent_patch_refs"]) and
               x["net_retired"]==len(item["retired"]) and x["net_introduced"]==len(item["introduced"]),
               "R70 exact tagged paths and identity controls")
        item["lean_computation"]=x
    v.need(len(audit)==247+len(names)==263 and r66.observe_historical_scope()==scope and
           r68.script_bridge(scope)==bridge and r69.additive_bridge(scope,bridge)==extension,"R70 scope")
    end_main=r69.observe_live_r3(scope);r69.observation_pair_valid(scope,start_main,end_main)
    v.save(out/"main-observations.json",{"before":start_main,"after":end_main})
    v.save(out/"keyed-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred","identity_authentication_proved")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True,
        "future_additions_observation_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.context-keyed-basis-path.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_path_key":KEY,"r69_direct_digest":DIRECT,"r69_mcp_digest":MCP,"historical_scope_digest":SCOPE,
        "script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),"application_source_sha256":r63.r62.r23.sha(app.encode()),
        "computation_source_sha256":r63.r62.r23.sha(compute.encode()),"keyed_paths":items,
        "empty_inventory_holds":parent["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_retained":True,"original_patch_history_retained":True,
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R70_DIRECT_CONTEXT_KEYED_BASIS_PATH",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_path_key":KEY,"keyed_path_key":record["key"],"r69_direct_digest":DIRECT,"r69_mcp_digest":MCP,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"r69_additive_observation_digest":EXTENSION,
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_keyed_theorems":len(names)-len(GENERAL),"actual_path_count":len(items),
        "empty_inventory_hold_count":5,"actual_computations":computations,"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_retained":True,"original_patch_history_retained":True,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],"new_theorem_names":list(names),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R70_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
        {"direct_digest":old.digest(result),"audits":len(audit)},sort_keys=True),flush=True)
    return result

def mcp(out):
    d=load(out/"direct.json");x=d["fresh_application"]
    parent=out/"parent-r69-receipts";pd=load(parent/"direct.json");pm=load(parent/"mcp.json")
    v.need(old.digest(pd)==DIRECT and old.digest(pm)==MCP and pm["direct_digest"]==DIRECT,"R70 reuse parent receipt")
    parent_rows={row["name"]:(j,row) for j,row in enumerate(pd["fresh_application"]["observations"])}
    v.need(len(parent_rows)==247 and set(parent_rows).isdisjoint(d["new_theorem_names"]),"R70 distinct MCP inventory")
    p=out/"McpApplication.lean";p.write_text(x["mcp_source"],encoding="utf-8")
    rel=str(p.relative_to(ROOT))
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    v.need(pm["mcp_version"]==v.EXPECTED_SERVER_VERSION,"R70 exact MCP version")
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
        "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[];origins=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                                     "clientInfo":{"name":"KuuOS context keyed basis path","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),"MCP tools")
        raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        v.save(out/"mcp-diagnostics.json",raw);diag=v.structured(raw)
        v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
               and diag["timed_out"] is False and diag["failed_dependencies"]==[] and
               not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R70 fresh full-source MCP diagnostics")
        for j,row in enumerate(x["observations"]):
            name=row["name"]
            if name in parent_rows:
                k,prior=parent_rows[name]
                v.need(row==prior and d["parent_raw_replay_bytewise_equal"],"R70 identical prior direct observation")
                src=parent/f"mcp-verify-{k}.json";shutil.copyfile(src,out/f"mcp-verify-{j}.json")
                raw=load(src)
                origins.append({"name":name,"mode":"exact_reused","origin_run":RUN,"origin_job":140859797615,
                                "parent_audit_index":k,"receipt_sha256":r63.r62.r23.sha(src.read_bytes())})
            else:
                v.need(name in d["new_theorem_names"],"R70 new audit identity")
                raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":name,"scan_source":False})
                v.save(out/f"mcp-verify-{j}.json",raw)
                origins.append({"name":name,"mode":"fresh_actual_mcp",
                                "receipt_sha256":r63.r62.r23.sha((out/f"mcp-verify-{j}.json").read_bytes())})
            val=v.structured(raw);ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],"R70 MCP axiom audit")
            rows.append({"name":name,"axioms":ax})
    finally:client.close()
    reused=sum(x["mode"]=="exact_reused" for x in origins);fresh=len(origins)-reused
    v.need(reused==247 and fresh==16 and len(rows)==263,"R70 new and reused MCP counts")
    result={"status":"R70_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,"audit_origins":origins,
            "parent_mcp_digest":MCP,"reused_audit_count":reused,"new_audit_count":fresh,
            "fresh_full_source_diagnostics":True,"mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R70_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows),
          "new_actual_mcp_audits":fresh,"reused_actual_mcp_audits":reused,"fresh_full_source_diagnostics":True}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R70_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d) and
           mp["parent_mcp_digest"]==MCP and mp["reused_audit_count"]==247 and mp["new_audit_count"]==16 and
           mp["fresh_full_source_diagnostics"] is True,"independent R70 receipt")
    diag_raw=load(first/"mcp-diagnostics.json");diag=v.structured(diag_raw)
    v.need(diag_raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
        and diag["timed_out"] is False and diag["failed_dependencies"]==[] and
        not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R70 MCP diagnostics")
    parent=out/"parent-r69-receipts";pd=load(parent/"direct.json")
    rows=d["fresh_application"]["observations"];origins=mp["audit_origins"]
    v.need(len(mp["audits"])==len(rows)==len(origins)==263,"R70 MCP inventory")
    reused=0;fresh=0
    for j,row in enumerate(rows):
        path=first/f"mcp-verify-{j}.json";raw=load(path);val=v.structured(raw);origin=origins[j]
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"]==origin["name"] and
            origin["receipt_sha256"]==r63.r62.r23.sha(path.read_bytes()),"R70 MCP evidence")
        if origin["mode"]=="exact_reused":
            k=origin["parent_audit_index"]
            v.need(origin["origin_run"]==RUN and origin["origin_job"]==140859797615 and
                   pd["fresh_application"]["observations"][k]==row and
                   (parent/f"mcp-verify-{k}.json").read_bytes()==path.read_bytes(),"R70 exact historical MCP bytes")
            reused+=1
        else:
            v.need(origin["mode"]=="fresh_actual_mcp" and row["name"] in d["new_theorem_names"],"R70 new MCP receipt")
            fresh+=1
    v.need(reused==247 and fresh==16,"R70 independent exact reuse count")
    scope=load(out/"historical-scope.json")
    for folder in (out,first):
        obs=load(folder/"main-observations.json")
        v.need(set(obs)=={"before","after"},"R70 observation inventory")
        r69.observation_pair_valid(scope,obs["before"],obs["after"])
    for name in FILES+(NEW,"historical-scope.json","script-bridge.json","script-observation-bridge-r69.json",
                      "formal-source.lean","keyed-application.lean","keyed-computation.lean","keyed-computation.json",
                      *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,70))):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R70 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,70))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R70_INDEPENDENT_CONTEXT_KEYED_BASIS_PATH_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),"mcp_new_audits":fresh,
        "mcp_reused_audits":reused,"fresh_full_source_mcp_diagnostics":True,
        "keyed_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R70_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r69-local","r69-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
