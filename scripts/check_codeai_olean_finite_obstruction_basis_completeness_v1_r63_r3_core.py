#!/usr/bin/env python3
"""R63: finite minimal transversal completeness and exact R60 ledger replay."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_contextual_recovery_duality_v1_r62_r2 as r62
from check_codeai_no_go_memory_v1_r2 import normalize
v=r62.v
old=r62.old
ROOT=r62.ROOT
load=r62.load
RUN=45992685030
HEAD="a230f9ded4e877b64605fa7b185c05ad4f020399"
DIRECT="915cf3d800335ad04dc2e8833a88379633f1ad5a5e4c48b6f8d2f26ecd52ee30"
MCP="b4ddf5bba3b361f5743353490eddf1379197e5b3e346a8a87420e8b34da81a95"
KEY="03c426c78c080391f459feaa4d0aa3e24ef7e4fb83aadb04eaa531f91d78bb6a"
ARTS=((15194892749,"codeai-olean-r62-r2-local-45992685030-1","sha256:28aef313a3744e5ea1bc7162a727777c3395640e78ee76f9a5f93babfdfe0a7c"),
      (15195705381,"codeai-olean-r62-r2-independent-45992685030-1","sha256:eb95dd94375dd73ccc2a14fd33fb98cc1b8ab184867eaff98da65c0481e9ae42"))
FILES=r62.FILES+(r62.NEW,)
NEW="finite-obstruction-basis-completeness-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_finite_obstruction_basis_completeness_v1.lean"
GENERAL=("exists_minimal_subset","finite_witness_cut","exists_minimal_cut",
         "finite_basis_complete","minimal_cut_card_le","finite_recovery_duality",
         "two_minimal_form","mem_pair_cut","listed_iff","one_cuts_complete",
         "two_cuts_complete","single_family_basis","double_family_basis")
NS="KuuOSR63."
REFS={
 "exists_minimal_cut":[NS+"finite_witness_cut",NS+"exists_minimal_subset"],
 "finite_basis_complete":[NS+"exists_minimal_cut"],
 "minimal_cut_card_le":[NS+"finite_witness_cut"],
 "finite_recovery_duality":["KuuOSR62.family_recovery_iff_break_complete_basis",NS+"finite_basis_complete"],
 "two_minimal_form":["KuuOSR62.two_blocked_iff_basis"],
 "one_cuts_complete":[NS+"listed_iff"],
 "two_cuts_complete":[NS+"listed_iff","KuuOSR62.two_blocked_iff_basis",NS+"mem_pair_cut"],
 "single_family_basis":[NS+"one_cuts_complete"],
 "double_family_basis":[NS+"two_cuts_complete"],
}

def copy_equal(a,b,dest):
    raw=a.read_bytes()
    v.need(raw==b.read_bytes(),"parent byte drift "+str(a))
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw)

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R62 R2 run")
    for jid,steps in ((140484231097,["Verify R62 R2 contextual recovery duality","Actual Lean MCP R62 R2 formal recovery duality audit"]),
                      (140488462739,["Independently verify R62 R2 contextual recovery duality"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R62 R2 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R62 R2 artifact")
    local=a.r62_local;other=a.r62_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R62_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R62_INDEPENDENT_CONTEXTUAL_RECOVERY_DUALITY_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and
           ind["mcp_audits"]==110 and ind["parent_bytes_preserved"] and ind["raw_new_proofs_equal"],"R62 R2 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==110 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R62 R2 audit")
    for name in FILES:
        copy_equal(local/name,other/name,out/name)
    record=load(out/r62.NEW)
    v.need(record["key"]==KEY and r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_obstruction_key"]==load(out/r62.r60.NEW)["key"] and
           record["parent_recovery_key"]==load(out/r62.r61.NEW)["key"],"R62 R2 key")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R62 R2 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R62 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r62.r39 if folder=="capsule" else r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r62-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","finite-table.lean","finite-table-r1.lean"):
        copy_equal(local/name,other/name,receipts/name)
    v.need(r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r62.r23.sha((receipts/"finite-table.lean").read_bytes())==record["finite_source_sha256"] and
           r62.r23.sha((receipts/"finite-table-r1.lean").read_bytes())==record["r1_finite_source_sha256"],"R62 formal/table source")
    for i in range(54,62):
        folder="parent-r"+str(i)+"-receipts"
        for name in ("direct.json","mcp.json","independent.json"):
            copy_equal(local/folder/name,other/folder/name,out/folder/name)
    return d,mp,ind,record

def lean_list(xs):
    return "["+", ".join(map(str,xs))+"]"

def ledger(obs,paths,budget):
    rp=paths["projection"]["route_paths"]
    groups=obs["groups"]
    v.need(len(groups)==12,"R60 context inventory")
    ids=sorted({n for ps in rp.values() for n in ps})
    enc={n:i for i,n in enumerate(ids)}
    records=[];hold=[];names=[];refs={}
    source=["namespace KuuOSR63"]
    for j,(case,g) in enumerate(sorted(groups.items())):
        ns=g["budget_eligible"]
        v.need(ns==budget["decisions"][case]["eligible"],"R60 route context drift")
        if not ns:
            v.need(not g["cuts"] and not g["complete_for_recorded_routes_only"],"empty inventory cannot certify")
            hold.append(case);continue
        v.need(len(ns) in (1,2) and g["complete_for_recorded_routes_only"],"R60 finite scope")
        deps=[sorted(enc[n] for n in rp[route]) for route in ns]
        a=deps[0]; b=deps[1] if len(ns)==2 else []
        v.need(all(deps),"empty dependency inventory")
        actual={}
        for cut in g["cuts"]:
            xs=tuple(sorted(enc[n] for n in cut["denied"]))
            v.need(xs not in actual,"duplicate R60 cut")
            actual[xs]=cut
            for route,ds in zip(ns,deps):
                hits=set(xs)&set(ds)
                v.need(hits and set(cut["path_digests"][route])=={ids[k] for k in hits} and
                    all(cut["path_digests"][route][ids[k]]==old.digest(rp[route][ids[k]]) for k in hits),"R60 path binding")
            v.need(not any(all((set(xs)-{k})&set(ds) for ds in deps) for k in xs),"R60 cut minimality")
        if len(ns)==1:
            order=[(x,) for x in a]
        else:
            A=set(a);B=set(b)
            order=[(x,) for x in a if x in B]+[tuple(sorted((x,y))) for x in a if x not in B for y in b if y not in A]
        v.need(len(order)==len(set(order)) and set(order)==set(actual),"R60 ledger exact enumeration")
        label=str(j)
        aN="routeA_"+label;bN="routeB_"+label;cN="cuts_"+label
        eq="ledger_eq_"+label;bs="observed_basis_"+label;rec="observed_recovery_"+label
        source.append("def "+aN+" : List Nat := "+lean_list(a))
        if len(ns)==2:source.append("def "+bN+" : List Nat := "+lean_list(b))
        # Each encoded cut is read from the immutable R60 record, not substituted
        # with a synthetic expected cut. Reordering only fixes presentation.
        recorded=[tuple(sorted(enc[n] for n in actual[x]["denied"])) for x in order]
        source.append("def "+cN+" : List (List Nat) := ["+", ".join(lean_list(x) for x in recorded)+"]")
        enum="oneCuts "+aN if len(ns)==1 else "twoCuts "+aN+" "+bN
        dep="SingleDeps "+aN if len(ns)==1 else "DoubleDeps "+aN+" "+bN
        hbase="single_family_basis "+aN if len(ns)==1 else "double_family_basis "+aN+" "+bN
        source += ["set_option maxRecDepth 16384 in","set_option maxHeartbeats 12000000 in",
                   "theorem "+eq+" : "+cN+" = "+enum+" := by","  rfl",
                   "theorem "+bs+" (U : Nat → Prop) :",
                   "    (∀ i, KuuOSR62.Hits U ("+dep+" i)) ↔",
                   "      ∃ C, ListedBasis "+cN+" C ∧ KuuOSR62.Included C U := by",
                   "  rw ["+eq+"]","  exact "+hbase+" U",
                   "theorem "+rec+" (D R : Nat → Prop) :",
                   "    (∃ i, KuuOSR62.Eligible (KuuOSR62.Residual D R) ("+dep+" i)) ↔",
                   "      ∀ C, ListedBasis "+cN+" C → KuuOSR62.Included C D → KuuOSR62.Hits R C :=",
                   "  KuuOSR62.family_recovery_iff_break_complete_basis ("+dep+") (ListedBasis "+cN+") D R "+bs]
        names += [NS+eq,NS+bs,NS+rec]
        refs[NS+bs]=[NS+eq,NS+hbase.split()[0]]
        refs[NS+rec]=[NS+bs,"KuuOSR62.family_recovery_iff_break_complete_basis"]
        records.append({"case":case,"route_names":ns,"route_dependencies":deps,
            "r60_cut_digests":[old.digest(actual[x]) for x in order],"encoded_cuts":[list(x) for x in recorded],
            "ledger_theorem":NS+eq,"basis_theorem":NS+bs,"recovery_theorem":NS+rec,
            "complete_for_recorded_routes_only":True,"proof_authority":False,"action_authority":False})
    v.need(len(records)==7 and len(hold)==5 and sum(len(x["encoded_cuts"]) for x in records)==1856,"R60 complete ledger inventory")
    return ids,records,hold,names,refs,"\n".join(source+["end KuuOSR63",""])

def raw_observer(names):
    template=r62.gate.raw_observer()
    old_names=", ".join(chr(96)*2+n for n in r62.gate.NAMES)
    new_names=", ".join(chr(96)*2+n for n in names)
    v.need(template.count(old_names)==1,"raw observer boundary")
    return template.replace(old_names,new_names).replace("R62","R63").replace("KuuOSR63.","KuuOSR63.")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R63_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R63_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R63 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R63 raw proof")
    return result

def direct(a,out):
    scope=r62.r29.observe_scope()
    d,mp,ind,parent=admit(a,out)
    obs=load(out/r62.r60.NEW);paths=load(out/r62.r59.NEW);budget=load(out/r62.r56.NEW)
    ids,records,hold,concrete,refs,table=ledger(obs,paths,budget)
    formal=FORMAL.read_text(encoding="utf-8")
    names=tuple(NS+n for n in GENERAL)+tuple(concrete)
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    (out/"finite-ledger.lean").write_text(table,encoding="utf-8")
    source=d["fresh_application"]["mcp_source"]+"\n"+formal+"\n"+table+"\n"+raw_observer(names)
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({NS+n:REFS.get(n,[]) for n in GENERAL})
    expected.update({n:refs.get(n,[]) for n in concrete})
    # Preserve the certified parent module/file identity for raw replay.
    # The parent prefix is unchanged. Only new declarations follow it.
    p=ROOT/"artifacts"/"olean-r62"/"RecoveryDualityR62.lean"
    p.parent.mkdir(parents=True,exist_ok=False)
    try:log=r62.r23.run_lean([],p,source+v.suffix(sorted(expected)))
    except ValueError:
        if p.with_suffix(".log").is_file():
            lines=p.with_suffix(".log").read_text(encoding="utf-8").splitlines()
            for i,line in enumerate(lines):
                if len(line)<5000 and ("error:" in line or "error(" in line or "warning:" in line):
                    print("\n".join(z[:6000] for z in lines[i:i+10])[:24000],flush=True)
        raise
    finally:
        for path in (p,p.with_suffix(".log")):
            if path.is_file():
                shutil.copyfile(path,out/path.name)
    audit=v.read_direct(log,[{"name":n,"expected_direct_refs":expected[n]} for n in sorted(expected)])
    by={x["name"]:x for x in audit}
    v.need({n:by[n] for n in hist}==hist,"R62 full audit drift")
    previous_raw=r62.gate.raw_audit(log,by)
    expected_raw=parent["raw_theorems"]
    # Never normalize or ignore proof-expression differences.
    v.save(out/"parent-r62-raw-replay.json",previous_raw)
    if previous_raw!=expected_raw:
        differences=[]
        for n in sorted(set(previous_raw)|set(expected_raw)):
            before=expected_raw.get(n,{})
            after=previous_raw.get(n,{})
            for k in sorted(set(before)|set(after)):
                x,y=before.get(k),after.get(k)
                if x==y:continue
                xs,ys=str(x),str(y)
                i=next((i for i,(u,w) in enumerate(zip(xs,ys)) if u!=w),min(len(xs),len(ys)))
                differences.append({"name":n,"field":k,"offset":i,
                    "before":xs[max(0,i-120):i+240],"after":ys[max(0,i-120):i+240],
                    "before_digest":old.digest(x),"after_digest":old.digest(y)})
        v.save(out/"parent-r62-raw-differences.json",differences)
        print("KUUOS_R63_R3_RAW_DRIFT",json.dumps(differences,ensure_ascii=False)[:24000],flush=True)
    v.need(previous_raw==expected_raw,"R62 raw type/proof/axiom drift")
    raw=raw_audit(log,by,names)
    v.need(len(audit)==110+len(names) and r62.r29.observe_scope()==scope,"R63 scope")
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved","policy_is_refutation")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True})
    record=r62.gate.base.portable.seal({"schema":"kuuos.codeai.finite-obstruction-basis-completeness.v1",
        "source_head":r62.gate.base.CURRENT,"source_tree":r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_duality_key":KEY,"parent_obstruction_key":obs["key"],"r62_direct_digest":DIRECT,"r62_mcp_digest":MCP,
        "formal_source_sha256":r62.r23.sha(formal.encode()),"ledger_source_sha256":r62.r23.sha(table.encode()),
        "dependency_id_map":ids,"contexts":records,"empty_inventory_holds":hold,"raw_theorems":raw,
        "formal_observations":{n:by[n] for n in names},**boundary})
    v.save(out/NEW,record)
    result={"status":"R63_DIRECT_FINITE_OBSTRUCTION_BASIS_COMPLETENESS",
        "source_head":r62.gate.base.CURRENT,"source_tree":r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_duality_key":KEY,"basis_key":record["key"],"r62_direct_digest":DIRECT,"r62_mcp_digest":MCP,
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"concrete_theorems":len(concrete),"certified_context_count":len(records),
        "empty_inventory_hold_count":len(hold),"ledger_cut_count":sum(len(x["encoded_cuts"]) for x in records),
        "formal_source_sha256":record["formal_source_sha256"],"ledger_source_sha256":record["ledger_source_sha256"],
        "new_theorem_names":list(names),"new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,**boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R63_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS finite obstruction basis completeness","version":"1"}})
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
    result={"status":"R63_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R63_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R63_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R63 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R63 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R63 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R63 MCP evidence")
    for name in FILES+(NEW,"formal-source.lean","finite-ledger.lean"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R63 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,63))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R63_INDEPENDENT_FINITE_OBSTRUCTION_BASIS_COMPLETENESS_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "basis_bytes_equal":True,"raw_new_proofs_equal":True,"parent_bytes_preserved":True,
        "raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R63_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r62-local","r62-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
