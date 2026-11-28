#!/usr/bin/env python3
"""R69: checked arbitrary finite paths over immutable R68/R67 records."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_composable_basis_patch_v1_r68_r2 as r68
from check_codeai_no_go_memory_v1_r2 import normalize
r67=r68.r67
r66=r68.r66
r65=r68.r65
r64=r68.r64
r63=r68.r63
v=r68.v
old=r68.old
ROOT=r68.ROOT
load=r68.load
RUN=46102814147
HEAD="858e4e10c9553e2995ad497e080b879b8ecb552d"
DIRECT="d63cdbf614bdafc736bdf15c9ddeaa76d6e2292fb5e99235fcf7467382a5e1dd"
MCP="a3cae07862b69167f7b8fa54dcdc69400bca5f075a65db2a8b3876ef84231d72"
KEY="bb8ded866f5a2d6f2b66c141a8184ee5df30d46fd97c7410b28540d20707f2e3"
SCOPE=r68.SCOPE
BRIDGE="5675662bf4fb77bd1d709e354c34eee22cba1f8d742c32c3f40a4994db3c3bde"
ARTS=((15246775535,"codeai-olean-r68-r2-local-46102814147-1","sha256:5bd92e377e0c9f624b25f9f438bf9b8a5919ef83fe95cdd3ba7946d1e00ef270"),
      (15246438773,"codeai-olean-r68-r2-independent-46102814147-1","sha256:23c3e9e92f8a7d338341b236dfc8cc1f94db9629733e0ca42c563ca0c5613e2f"))
FILES=r68.FILES+(r68.NEW,)
NEW="checked-basis-path-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_checked_basis_path_v1.lean"
NS="KuuOSR69."
GENERAL=("checked_path_exact","checked_path_sound","checked_path_iff","checked_path_replay",
         "path_append_valid","checked_path_append_composes","checked_reject_source","checked_reject_step",
         "checked_reject_empty","checked_reject_tail","canonical_walk_valid","canonical_walk_exact","net_history_collision")
REFS={
 "checked_path_exact":["KuuOSR68.bound_sound","KuuOSR68.compose_valid_exact","KuuOSR67.actual_patch_valid","KuuOSR67.apply_diff_exact"],
 "checked_path_iff":[NS+"checked_path_sound",NS+"checked_path_exact"],
 "checked_path_replay":[NS+"checked_path_iff","KuuOSR67.checked_bound_exact"],
 "checked_path_append_composes":[NS+"checked_path_iff",NS+"checked_path_exact",NS+"path_append_valid","KuuOSR68.compose_diff_exact"],
 "canonical_walk_valid":["KuuOSR67.checked_bound_exact"],
 "canonical_walk_exact":[NS+"checked_path_exact",NS+"canonical_walk_valid"],
 "net_history_collision":[NS+"canonical_walk_exact"],
}

def admit(a,out,scope,bridge):
    api=v.cache.api
    run=api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R68 R2 run")
    for jid,steps in ((140848866750,["Verify R68 R2 composable basis patch","Require exact reused R68 R1 real Lean MCP evidence"]),
                      (140850145196,["Independently verify R68 R2 composable basis patch"])):
        j=api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R68 R2 jobs")
    for aid,n,dig in ARTS:
        x=api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R68 R2 artifact")
    local=a.r68_local;other=a.r68_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R68_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R68_INDEPENDENT_COMPOSABLE_BASIS_PATCH_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==231 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","chain_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R68 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==231 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R68 R1 actual MCP audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r68.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_patch_key"]==load(out/r67.NEW)["key"],"R68 R2 key")
    v.need(record["historical_research_only"] and record["live_main_admission"] is False and
           record["current_main_certification_transferred"] is False and d["historical_scope_digest"]==SCOPE==old.digest(scope) and
           record["historical_scope_digest"]==SCOPE and d["deletion_basis_only_no_inverse_retained"] and
           d["original_patch_history_retained"] and len(record["chains"])==2 and
           d["empty_inventory_hold_count"]==5,"R68 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R68 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R68 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r68-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","chain-application.lean","chain-computation.lean","chain-computation.json",
                 "historical-scope.json","script-bridge.json","r68-r2-repair.json",
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,68))):
        r63.copy_equal(local/name,other/name,receipts/name)
    repair=load(receipts/"r68-r2-repair.json")
    v.need(repair["r1_run"]==r68.R1_RUN and repair["r1_direct_digest"]==DIRECT and repair["r1_mcp_digest"]==MCP and
           repair["r1_actual_mcp_audits_reused"]==231 and repair["r2_actual_mcp_new_execution"] is False and
           repair["r1_failed_independent_kernel_and_raw_equal"] and repair["r1_failed_independent_computation_equal"] and
           repair["r1_all_formal_bytes_unchanged"] and repair["script_bridge_digest"]==BRIDGE and
           load(receipts/"script-bridge.json")==bridge and old.digest(bridge)==BRIDGE,"R68 explicit inherited execution lineage")
    v.need(load(receipts/"historical-scope.json")==scope and
           r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"chain-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"chain-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"chain-computation.json")==record["chains"],"R68 source and chain lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["scripts_tree"]==r68.NEW_SCRIPTS and x["current_main_certification_transferred"] is False and
               x["live_main_admission"] is False for x in obs.values()),"R68 live observation")
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW),(67,r67.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R68 ancestor raw lineage")
    for i in range(54,68):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r68.raw_observer(names).replace("KUUOS_R68_RAW ","KUUOS_R69_RAW ").replace("R68 theorem","R69 theorem").replace("R68 not a theorem","R69 not a theorem").replace("R68 proof unavailable","R69 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R69_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R69_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R69 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R69 raw proof")
    return result

def path_sources(ledger,parent,patch_record):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=patch_record["patches"]
    v.need(len(rows)==7 and len(patches)==2 and len(parent["chains"])==2 and len(ledger["empty_inventory_holds"])==5,"R69 scope")
    for i,t in enumerate(parent["chains"]):
        v.need(t["index"]==i and t["ordered_parent_patch_refs"]==[
            {"digest":old.digest(patches[i]),"direction":"forward"},
            {"digest":old.digest(patches[1-i]),"direction":"rollback"}] and
            t["path_history_retained"] and t["lean_computation"]["composed_exact"],"R68 chain lineage")
    src=["namespace KuuOSR69"]
    compute=["namespace KuuOSR69"]
    items=[];refs={}
    case_index={"global_boundary":2,"global_default":3,"global_probes":6}
    def fs(case):return {tuple(x) for x in rows[case]["encoded_cuts"]}
    def basis(case):return "((KuuOSR63.cuts_"+str(case_index[case])+".map List.toFinset).toFinset)"
    def literal(xs):return "(("+json.dumps([list(x) for x in sorted(xs)])+" : List (List Nat)).map List.toFinset).toFinset"
    def step_literal(source,target,R,N):
        return "({ source := "+basis(source)+", target := "+basis(target)+", retired := "+literal(R)+", introduced := "+literal(N)+" } : PatchStep Nat)"
    # Compose two certified edges and their reverses in two distinct longer
    # counterfactual walks. Preserve all occurrence order and endpoint IDs.
    for i,spec in enumerate((((0,False),(1,True),(1,False)),
                             ((1,False),(0,True),(0,False),(1,True)))):
        steps=[];nodes=[];request_ids=[];ordered=[];literals=[]
        for j,rev in spec:
            p=patches[j]
            s,t=p["source_case"],p["target_case"]
            sid,tid=p["source_request_id"],p["target_request_id"]
            R={tuple(x) for x in p["retired"]};N={tuple(x) for x in p["introduced"]}
            if rev:s,t,sid,tid,R,N=t,s,tid,sid,N,R
            v.need(R==fs(s)-fs(t) and N==fs(t)-fs(s) and p["context_id"]==patches[0]["context_id"],"exact patch difference")
            if nodes:
                v.need(nodes[-1]==s and request_ids[-1]==sid,"typed path endpoint mismatch")
            else:
                nodes.append(s);request_ids.append(sid)
            nodes.append(t);request_ids.append(tid)
            ordered.append({"digest":old.digest(p),"direction":"rollback" if rev else "forward",
                            "source_request_id":sid,"target_request_id":tid})
            steps.append((s,t,R,N))
            literals.append(step_literal(s,t,R,N))
        start,finish=nodes[0],nodes[-1]
        F,H=fs(start),fs(finish)
        R,N=F-H,H-F
        f,h=basis(start),basis(finish)
        end_list="["+", ".join(basis(x) for x in nodes[1:])+"]"
        name="actual_path_"+str(i)
        src += ["theorem "+name+" :",
                "  checkedPath "+f+" "+h+" (canonicalWalk "+f+" "+end_list+") =",
                "    some ("+f+" \\ "+h+", "+h+" \\ "+f+") :=",
                "  canonical_walk_exact "+f+" "+end_list]
        refs[NS+name]=[NS+"canonical_walk_exact"]
        names=[NS+name]
        if i==1:
            cyc="actual_nonempty_cycle_history"
            src += ["theorem "+cyc+" : (canonicalWalk "+f+" "+end_list+").length = 4 := rfl"]
            refs[NS+cyc]=[]
            names.append(NS+cyc)
        wrong_end=nodes[1] if start==finish else start
        s,t,r,n=steps[1]
        wrong_middle=list(literals);wrong_middle[1]=step_literal(start,t,r,n)
        late=list(literals);s,t,r,n=steps[-1];late[-1]=step_literal(s,t,r|n,n)
        v.need(start!=nodes[1] and wrong_end!=finish and bool(n),"nontrivial negative controls")
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let h := "+h,
                    "  let path : List (PatchStep Nat) := ["+", ".join(literals)+"]",
                    "  let badMiddle : List (PatchStep Nat) := ["+", ".join(wrong_middle)+"]",
                    "  let badLate : List (PatchStep Nat) := ["+", ".join(late)+"]",
                    "  let r := "+literal(R),"  let n := "+literal(N),
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("steps", Lean.toJson path.length),',
                    '    ("recorded_path_exact", Lean.toJson (decide (checkedPath f h path = some (r,n)))),',
                    '    ("canonical_path_exact", Lean.toJson (decide (checkedPath f h (canonicalWalk f '+end_list+') = some (r,n)))),',
                    '    ("forward_exact", Lean.toJson (decide (checkedBoundPatch f h r n = some h))),',
                    '    ("rollback_exact", Lean.toJson (decide (checkedBoundPatch h f n r = some f))),',
                    '    ("bad_middle_hold", Lean.toJson (decide (checkedPath f h badMiddle = none))),',
                    '    ("bad_late_hold", Lean.toJson (decide (checkedPath f h badLate = none))),',
                    '    ("wrong_end_hold", Lean.toJson (decide (checkedPath f '+basis(wrong_end)+' path = none))),',
                    '    ("empty_history_same_net", Lean.toJson (decide (checkedPath f f [] = checkedPath f h path))),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R69_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"source_case":start,"target_case":finish,"ordered_cases":nodes,
                      "ordered_request_ids":request_ids,"ordered_parent_patch_refs":ordered,
                      "context_id":patches[0]["context_id"],"retired":[list(x) for x in sorted(R)],
                      "introduced":[list(x) for x in sorted(N)],"theorems":names,
                      "path_history_retained":True,"counterfactual_only":True,"action_authority":False})
    return "\n".join(src+["end KuuOSR69",""]),"\n".join(compute+["end KuuOSR69",""]),items,refs

def direct(a,out):
    scope=r66.observe_historical_scope()
    bridge=r68.script_bridge(scope)
    v.need(old.digest(bridge)==BRIDGE,"R69 exact admitted scripts bridge")
    start_main=r68.observe_live_main_r2(scope)
    v.save(out/"historical-scope.json",scope);v.save(out/"script-bridge.json",bridge)
    v.save(out/"main-observations.json",{"before":start_main})
    d,mp,ind,parent=admit(a,out,scope,bridge)
    ledger=load(out/r63.NEW)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=path_sources(ledger,parent,load(out/r67.NEW))
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"path-application.lean").write_text(app,encoding="utf-8")
    (out/"path-computation.lean").write_text(compute,encoding="utf-8")
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
    v.need(not missing,"R69 missing direct reference "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R68 full audit drift")
    for i,layer,checker in ((68,r68.NEW,r68.raw_audit),(67,r67.NEW,r67.raw_audit),(66,r66.NEW,r66.raw_audit),
                            (65,r65.NEW,r65.raw_audit),(64,r64.NEW,r64.raw_audit),(63,r63.NEW,r63.raw_audit)):
        previous=checker(log,by,tuple(load(out/("parent-r"+str(i)+"-receipts")/"direct.json")["new_theorem_names"]))
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),previous)
        v.need(previous==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous62==load(out/r63.r62.NEW)["raw_theorems"],"R62 raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R69_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"R69 computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("recorded_path_exact","canonical_path_exact","forward_exact","rollback_exact",
                 "bad_middle_hold","bad_late_hold","wrong_end_hold")) and
               x["steps"]==len(item["ordered_parent_patch_refs"]) and
               x["net_retired"]==len(item["retired"]) and x["net_introduced"]==len(item["introduced"]) and
               x["empty_history_same_net"]==(item["index"]==1),"R69 exact paths and negative controls")
        item["lean_computation"]=x
    v.need(len(audit)==231+len(names)==247 and r66.observe_historical_scope()==scope and
           r68.script_bridge(scope)==bridge,"R69 scope")
    end_main=r68.observe_live_main_r2(scope)
    v.need(v.cache.ancestor(v.cache.api,start_main["head"],end_main["head"]),"R69 live main rewound")
    v.save(out/"main-observations.json",{"before":start_main,"after":end_main})
    v.save(out/"path-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.checked-basis-path.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_chain_key":KEY,"r68_direct_digest":DIRECT,"r68_mcp_digest":MCP,"historical_scope_digest":SCOPE,
        "script_bridge_digest":BRIDGE,"formal_source_sha256":r63.r62.r23.sha(formal.encode()),
        "application_source_sha256":r63.r62.r23.sha(app.encode()),"computation_source_sha256":r63.r62.r23.sha(compute.encode()),
        "paths":items,"empty_inventory_holds":ledger["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_certified":True,"original_patch_history_retained":True,
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R69_DIRECT_CHECKED_BASIS_PATH",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_chain_key":KEY,"path_key":record["key"],"r68_direct_digest":DIRECT,"r68_mcp_digest":MCP,
        "historical_scope_digest":SCOPE,"script_bridge_digest":BRIDGE,"capsule_manifest":d["capsule_manifest"],
        "joint_capsule_manifest":d["joint_capsule_manifest"],"general_theorems":len(GENERAL),
        "actual_path_theorems":len(names)-len(GENERAL),"actual_path_count":len(items),
        "empty_inventory_hold_count":5,"actual_computations":computations,"deletion_basis_only_no_inverse_retained":True,
        "net_history_collision_certified":True,"original_patch_history_retained":True,
        "formal_source_sha256":record["formal_source_sha256"],"application_source_sha256":record["application_source_sha256"],
        "computation_source_sha256":record["computation_source_sha256"],
        "new_theorem_names":list(names),"new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R69_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS checked basis path","version":"1"}})
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
    result={"status":"R69_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R69_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R69_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R69 receipt")
    diag_raw=load(first/"mcp-diagnostics.json");diag=v.structured(diag_raw)
    v.need(diag_raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
        and diag["timed_out"] is False and diag["failed_dependencies"]==[] and
        not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R69 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows)==247,"R69 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R69 MCP evidence")
    for folder in (out,first):
        obs=load(folder/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["scripts_tree"]==r68.NEW_SCRIPTS and x["current_main_certification_transferred"] is False and
               x["live_main_admission"] is False for x in obs.values()),"R69 live observations")
    for name in FILES+(NEW,"historical-scope.json","script-bridge.json","formal-source.lean","path-application.lean",
                      "path-computation.lean","path-computation.json",*("parent-r"+str(i)+"-raw-replay.json" for i in range(62,69))):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R69 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,69))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R69_INDEPENDENT_CHECKED_BASIS_PATH_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "path_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R69_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r68-local","r68-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
