#!/usr/bin/env python3
"""R68: exact composition of R67 reversible patches, preserving original path records."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_reversible_basis_patch_v1_r67 as r67
from check_codeai_no_go_memory_v1_r2 import normalize
r66=r67.r66
r65=r67.r65
r64=r67.r64
r63=r67.r63
v=r67.v
old=r67.old
ROOT=r67.ROOT
load=r67.load
RUN=46096535707
HEAD="fee1ef3c055384aec2d7221ac74a21ce5b24bc0e"
DIRECT="72f6b6eddd580b1447af244be92a256f461121385be0f9337d6d5e317a1923a5"
MCP="0fe715ba4539599393b92bc7503f3a9a8af507c21d5b58ca6a931cd894f1691c"
KEY="573c7511ff2fe6996bed70b2279883427665be343efddf936959de24d7e22757"
SCOPE=r67.SCOPE
ARTS=((15244806536,"codeai-olean-r67-r2-local-46096535707-1","sha256:db64080380a8ba17c3786e645a585ecd119283cbe98d451372caabbeb40b1e69"),
      (15244492546,"codeai-olean-r67-r2-independent-46096535707-1","sha256:585483b10fed4503edde4731c11092d421ce8074a94ae28de45bc9e595c38970"))
FILES=r67.FILES+(r67.NEW,)
NEW="composable-basis-patch-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_composable_basis_patch_v1.lean"
NS="KuuOSR68."
GENERAL=("compose_removed_exact","compose_added_exact","compose_diff_exact","compose_valid_exact",
         "bound_sound","checked_compose_exact","checked_reject_middle","checked_reject_first",
         "checked_reject_second","checked_compose_sound","checked_compose_replay",
         "compose_three_associative","checked_compose_cycle")
REFS={
 "compose_diff_exact":[NS+"compose_removed_exact",NS+"compose_added_exact"],
 "compose_valid_exact":["KuuOSR67.patch_unique",NS+"compose_diff_exact"],
 "checked_compose_exact":[NS+"bound_sound",NS+"compose_valid_exact"],
 "checked_compose_sound":[NS+"checked_compose_exact"],
 "checked_compose_replay":[NS+"checked_compose_sound","KuuOSR67.checked_bound_exact"],
 "compose_three_associative":[NS+"compose_diff_exact"],
 "checked_compose_cycle":[NS+"checked_compose_exact","KuuOSR67.checked_bound_exact"],
}

def admit(a,out,scope):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R67 R2 run")
    for jid,steps in ((140829043279,["Verify R67 R2 reversible basis patch","Actual Lean MCP R67 R2 reversible basis patch audit"]),
                      (140837339227,["Independently verify R67 R2 reversible basis patch"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R67 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R67 R2 artifact")
    local=a.r67_local;other=a.r67_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R67_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R67_INDEPENDENT_REVERSIBLE_BASIS_PATCH_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==214 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","patch_bytes_equal",
                                "actual_computation_bytes_equal","raw_type_and_proof_equal")),"R67 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==214 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R67 R2 audit")
    for name in FILES:r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r67.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_delta_key"]==load(out/r66.NEW)["key"],"R67 R2 key")
    v.need(record["historical_research_only"] and record["live_main_admission"] is False and
           record["current_main_certification_transferred"] is False and d["historical_scope_digest"]==SCOPE==old.digest(scope) and
           record["historical_scope_digest"]==SCOPE and d["deletion_basis_only_no_inverse_retained"] and
           len(record["patches"])==2 and d["empty_inventory_hold_count"]==5,"R67 scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R67 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R67 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r67-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","formal-source-r1.lean","r67-r2-repair.json","patch-application.lean",
                 "patch-computation.lean","patch-computation.json","historical-scope.json",
                 *("parent-r"+str(i)+"-raw-replay.json" for i in range(62,67))):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(load(receipts/"historical-scope.json")==scope and
           r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"patch-application.lean").read_bytes())==record["application_source_sha256"] and
           r63.r62.r23.sha((receipts/"patch-computation.lean").read_bytes())==record["computation_source_sha256"] and
           load(receipts/"patch-computation.json")==record["patches"] and
           load(receipts/"r67-r2-repair.json")["r1_all_propositions_unchanged"] is True,"R67 source and patch lineage")
    for label,src in (("sandbox",local),("independent",other)):
        obs=load(src/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["current_main_certification_transferred"] is False and x["live_main_admission"] is False for x in obs.values()),"R67 live observation")
        shutil.copyfile(src/"main-observations.json",receipts/(label+"-main-observations.json"))
    for i,layer in ((62,r63.r62.NEW),(63,r63.NEW),(64,r64.NEW),(65,r65.NEW),(66,r66.NEW)):
        v.need(load(receipts/("parent-r"+str(i)+"-raw-replay.json"))==load(out/layer)["raw_theorems"],"R67 ancestor raw lineage")
    for i in range(54,67):
        folder="parent-r"+str(i)+"-receipts"
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r67.raw_observer(names).replace("KUUOS_R67_RAW ","KUUOS_R68_RAW ").replace("R67 theorem","R68 theorem").replace("R67 not a theorem","R68 not a theorem").replace("R67 proof unavailable","R68 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R68_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R68_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R68 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R68 raw proof")
    return result

def chain_sources(ledger,parent,delta):
    rows={x["case"]:x for x in ledger["contexts"]}
    patches=parent["patches"]
    v.need(len(rows)==7 and len(patches)==2 and len(ledger["empty_inventory_holds"])==5,"R68 parent inventory")
    for i,p in enumerate(patches):
        t=delta["context_transitions"][i]
        v.need(p["index"]==i and p["parent_transition_digest"]==old.digest(t) and
               p["target_case"]=="global_default" and p["source_case"]==("global_boundary" if i==0 else "global_probes") and
               all(p[k]==t[k] for k in ("context_id","source_request_id","target_request_id","source_case","target_case",
                                         "retired","introduced","source_routes","added_route")) and
               all(p["lean_computation"][k] is True for k in ("forward_exact","rollback_exact","bound_forward_exact",
                   "bound_rollback_exact","missing_retired_hold","duplicate_introduction_hold","wrong_endpoint_hold")),
               "R67 exact parent patch")
    v.need(patches[0]["context_id"]==patches[1]["context_id"] and
           patches[0]["target_request_id"]==patches[1]["target_request_id"],"R68 typed middle context")
    src=["namespace KuuOSR68","open KuuOSR67"]
    compute=["namespace KuuOSR68","open KuuOSR67"]
    items=[];refs={}
    def fs(case):return {tuple(x) for x in rows[case]["encoded_cuts"]}
    def literal(xs):return "(("+json.dumps([list(x) for x in sorted(xs)])+" : List (List Nat)).map List.toFinset).toFinset"
    def basis(i):return "((KuuOSR63.cuts_"+str(i)+".map List.toFinset).toFinset)"
    for i in (0,1):
        a,b=patches[i],patches[1-i]
        F,G,H=fs(a["source_case"]),fs(a["target_case"]),fs(b["source_case"])
        R1,N1,R2,N2=({tuple(x) for x in q} for q in (a["retired"],a["introduced"],b["introduced"],b["retired"]))
        v.need(R1==F-G and N1==G-F and R2==G-H and N2==H-G,"R68 exact endpoints")
        R=(R1-N2)|(R2-N1);N=(N2-R1)|(N1-R2)
        v.need(R==F-H and N==H-F and len(N1&R2)==8 and not (R1&N2),"R68 net delta")
        f,g,h=basis(2 if i==0 else 6),basis(3),basis(6 if i==0 else 2)
        name="actual_chain_"+str(i)
        cyc="actual_cycle_"+str(i)
        src += ["theorem "+name+" :",
                "  checkedCompose "+f+" "+g+" "+g+" "+h,
                "    ("+f+" \\ "+g+") ("+g+" \\ "+f+") ("+g+" \\ "+h+") ("+h+" \\ "+g+")",
                "    = some ("+f+" \\ "+h+", "+h+" \\ "+f+") :=",
                "  checked_compose_exact "+f+" "+g+" "+h,
                "    ("+f+" \\ "+g+") ("+g+" \\ "+f+") ("+g+" \\ "+h+") ("+h+" \\ "+g+")",
                "    (checked_bound_exact "+f+" "+g+") (checked_bound_exact "+g+" "+h+")",
                "theorem "+cyc+" :",
                "  checkedCompose "+f+" "+g+" "+g+" "+f,
                "    ("+f+" \\ "+g+") ("+g+" \\ "+f+") ("+g+" \\ "+f+") ("+f+" \\ "+g+")",
                "    = some ((∅ : Finset (Finset Nat)), (∅ : Finset (Finset Nat))) :=",
                "  checked_compose_cycle "+f+" "+g]
        refs[NS+name]=[NS+"checked_compose_exact","KuuOSR67.checked_bound_exact"]
        refs[NS+cyc]=[NS+"checked_compose_cycle"]
        compute += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in","run_cmd do",
                    "  let f := "+f,"  let g := "+g,"  let h := "+h,
                    "  let r1 := "+literal(R1),"  let n1 := "+literal(N1),"  let r2 := "+literal(R2),"  let n2 := "+literal(N2),
                    "  let r := "+literal(R),"  let n := "+literal(N),
                    "  let payload := Lean.Json.mkObj [",
                    '    ("index", Lean.toJson ('+str(i)+' : Nat)),',
                    '    ("composed_exact", Lean.toJson (decide (checkedCompose f g g h r1 n1 r2 n2 = some (r,n)))),',
                    '    ("forward_exact", Lean.toJson (decide (checkedBoundPatch f h r n = some h))),',
                    '    ("rollback_exact", Lean.toJson (decide (checkedBoundPatch h f n r = some f))),',
                    '    ("cycle_exact", Lean.toJson (decide (checkedCompose f g g f r1 n1 n1 r1 = some ((∅ : Finset (Finset Nat)), (∅ : Finset (Finset Nat)))))),',
                    '    ("wrong_middle_hold", Lean.toJson (decide (checkedCompose f g f h r1 n1 r2 n2 = none))),',
                    '    ("bad_first_hold", Lean.toJson (decide (checkedCompose f g g h (r1 ∪ n1) n1 r2 n2 = none))),',
                    '    ("bad_second_hold", Lean.toJson (decide (checkedCompose f g g h r1 n1 (r2 ∪ n2) n2 = none))),',
                    '    ("cancelled_added_then_retired", Lean.toJson (n1 ∩ r2).card),',
                    '    ("cancelled_retired_then_added", Lean.toJson (r1 ∩ n2).card),',
                    '    ("net_retired", Lean.toJson r.card),("net_introduced", Lean.toJson n.card)]',
                    '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R68_COMPUTE " ++ payload.compress)']
        items.append({"index":i,"source_case":a["source_case"],"middle_case":a["target_case"],"target_case":b["source_case"],
                      "context_id":a["context_id"],"source_request_id":a["source_request_id"],
                      "middle_request_id":a["target_request_id"],"target_request_id":b["source_request_id"],
                      "ordered_parent_patch_refs":[{"digest":old.digest(a),"direction":"forward"},
                                                   {"digest":old.digest(b),"direction":"rollback"}],
                      "retired":[list(x) for x in sorted(R)],"introduced":[list(x) for x in sorted(N)],
                      "cancelled_added_then_retired":[list(x) for x in sorted(N1&R2)],
                      "cancelled_retired_then_added":[list(x) for x in sorted(R1&N2)],
                      "chain_theorem":NS+name,"cycle_theorem":NS+cyc,
                      "path_history_retained":True,"counterfactual_only":True,"action_authority":False})
    return "\n".join(src+["end KuuOSR68",""]),"\n".join(compute+["end KuuOSR68",""]),items,refs

def direct(a,out):
    scope=r66.observe_historical_scope()
    start_main=r66.observe_live_main(scope)
    v.save(out/"historical-scope.json",scope)
    v.save(out/"main-observations.json",{"before":start_main})
    d,mp,ind,parent=admit(a,out,scope)
    ledger=load(out/r63.NEW)
    formal=FORMAL.read_text(encoding="utf-8")
    app,compute,items,refs=chain_sources(ledger,parent,load(out/r66.NEW))
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"chain-application.lean").write_text(app,encoding="utf-8")
    (out/"chain-computation.lean").write_text(compute,encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(n for x in items for n in (x["chain_theorem"],x["cycle_theorem"]))
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
    v.need(not missing,"R68 missing direct reference "+json.dumps(missing))
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R67 full audit drift")
    for i,layer,checker in ((67,r67.NEW,r67.raw_audit),(66,r66.NEW,r66.raw_audit),(65,r65.NEW,r65.raw_audit),
                            (64,r64.NEW,r64.raw_audit),(63,r63.NEW,r63.raw_audit)):
        previous=checker(log,by,tuple(load(out/("parent-r"+str(i)+"-receipts")/"direct.json")["new_theorem_names"]))
        v.save(out/("parent-r"+str(i)+"-raw-replay.json"),previous)
        v.need(previous==load(out/layer)["raw_theorems"],"R"+str(i)+" exact raw replay drift")
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous62==load(out/r63.r62.NEW)["raw_theorems"],"R62 raw replay drift")
    raw=raw_audit(log,by,names)
    mark="KUUOS_R68_COMPUTE "
    computations=[json.loads(x[len(mark):]) for x in log.splitlines() if x.startswith(mark)]
    by_index={x["index"]:x for x in computations}
    v.need(len(computations)==len(by_index)==2 and set(by_index)=={0,1},"R68 computation inventory")
    for item in items:
        x=by_index[item["index"]]
        v.need(all(x[k] is True for k in ("composed_exact","forward_exact","rollback_exact","cycle_exact",
                 "wrong_middle_hold","bad_first_hold","bad_second_hold")) and
               x["net_retired"]==len(item["retired"]) and x["net_introduced"]==len(item["introduced"]) and
               x["cancelled_added_then_retired"]==8 and x["cancelled_retired_then_added"]==0,"R68 exact composition and controls")
        item["lean_computation"]=x
    v.need(len(audit)==214+len(names) and r66.observe_historical_scope()==scope,"R68 scope")
    end_main=r66.observe_live_main(scope)
    v.need(v.cache.ancestor(v.cache.api,start_main["head"],end_main["head"]),"R68 live main rewound")
    v.save(out/"main-observations.json",{"before":start_main,"after":end_main})
    v.save(out/"chain-computation.json",items)
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved",
      "policy_is_refutation","live_main_admission","current_main_certification_transferred")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True,"historical_research_only":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.composable-basis-patch.v1",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_patch_key":KEY,"r67_direct_digest":DIRECT,"r67_mcp_digest":MCP,"historical_scope_digest":SCOPE,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),"application_source_sha256":r63.r62.r23.sha(app.encode()),
        "computation_source_sha256":r63.r62.r23.sha(compute.encode()),"chains":items,
        "empty_inventory_holds":ledger["empty_inventory_holds"],"deletion_basis_only_no_inverse_retained":True,
        "original_patch_history_retained":True,"raw_theorems":raw,"formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R68_DIRECT_COMPOSABLE_BASIS_PATCH",
        "source_head":r66.PINNED_HEAD,"source_tree":r66.PINNED_TREE,"scope_digest":old.SCOPE,
        "parent_patch_key":KEY,"chain_key":record["key"],"r67_direct_digest":DIRECT,"r67_mcp_digest":MCP,
        "historical_scope_digest":SCOPE,"capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"actual_chain_theorems":len(names)-len(GENERAL),"actual_chain_count":len(items),
        "empty_inventory_hold_count":5,"actual_computations":computations,"deletion_basis_only_no_inverse_retained":True,
        "original_patch_history_retained":True,"formal_source_sha256":record["formal_source_sha256"],
        "application_source_sha256":record["application_source_sha256"],"computation_source_sha256":record["computation_source_sha256"],
        "new_theorem_names":list(names),"new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R68_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS composable basis patch","version":"1"}})
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
    result={"status":"R68_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R68_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R68_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R68 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R68 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R68 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R68 MCP evidence")
    for folder in (out,first):
        obs=load(folder/"main-observations.json")
        v.need(set(obs)=={"before","after"} and all(x["scope_equal"] and x["scope_digest"]==old.SCOPE and
               x["current_main_certification_transferred"] is False and x["live_main_admission"] is False for x in obs.values()),"R68 live observations")
    for name in FILES+(NEW,"historical-scope.json","formal-source.lean","chain-application.lean","chain-computation.lean",
                      "chain-computation.json",*("parent-r"+str(i)+"-raw-replay.json" for i in range(62,68))):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R68 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,68))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R68_INDEPENDENT_COMPOSABLE_BASIS_PATCH_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "chain_bytes_equal":True,"actual_computation_bytes_equal":True,"raw_new_proofs_equal":True,
        "parent_bytes_preserved":True,"raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R68_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r67-local","r67-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
