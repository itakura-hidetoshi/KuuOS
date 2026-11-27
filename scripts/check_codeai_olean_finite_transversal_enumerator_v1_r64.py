#!/usr/bin/env python3
"""R64: executable arbitrary finite-route transversal enumeration."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import check_codeai_olean_finite_obstruction_basis_completeness_v1_r63_r3_core as r63
from check_codeai_no_go_memory_v1_r2 import normalize
v=r63.v
old=r63.old
ROOT=r63.ROOT
load=r63.load
RUN=45997331298
HEAD="fd48f5cdf661baad9438a7ad1d261948661826df"
DIRECT="94c5ef3799fdb5d576443c4aeed59dc592eec61ed2107f341fa9a288b1a45b17"
MCP="42091bd416c65a6e52261b5e9c2a29333567fcc907955682adb0ba8353a464e0"
KEY="574081d407fe4ef90e397e0341cd9d8b9d6e50170e341e871005300be666d265"
ARTS=((15196879277,"codeai-olean-r63-r3-local-45997331298-1","sha256:fc1be618debd046cd31851d322ab05183a196661c96c4749e00c493232025df7"),
      (15197014607,"codeai-olean-r63-r3-independent-45997331298-1","sha256:3d5cd7a044e32fc705860c9292c34a63ea78fc4114ee0ada8da7a89d223c2979"))
FILES=r63.FILES+(r63.NEW,)
NEW="finite-transversal-enumerator-v1.json"
FORMAL=Path(__file__).resolve().parent/"lean_probes"/"codeai_finite_transversal_enumerator_v1.lean"
NS="KuuOSR64."
GENERAL=("witness_sound","witness_complete","witness_card_le","mem_reduced_iff","mem_finite_basis",
         "enumerator_complete","basis_antichain","enumerated_cut_card_le","private_route_witness",
         "complete_certificate","enumerated_recovery_duality","two_route_enumeration_exact",
         "operational_empty_routes_hold","operational_empty_dependency_hold")
TESTS=("triangle_basis_exact","four_route_basis_exact","empty_math_family","empty_math_dependency")
NAMES=tuple(NS+n for n in GENERAL+TESTS)
REFS={
 "mem_finite_basis":[NS+"witness_sound",NS+"witness_complete",NS+"mem_reduced_iff"],
 "enumerator_complete":[NS+"witness_complete",NS+"witness_sound",NS+"mem_finite_basis","KuuOSR63.exists_minimal_subset"],
 "basis_antichain":[NS+"mem_finite_basis"],
 "enumerated_cut_card_le":[NS+"mem_reduced_iff",NS+"witness_card_le"],
 "private_route_witness":[NS+"mem_finite_basis"],
 "complete_certificate":[NS+"enumerator_complete",NS+"mem_finite_basis"],
 "enumerated_recovery_duality":["KuuOSR62.family_recovery_iff_break_complete_basis",NS+"complete_certificate"],
 "two_route_enumeration_exact":["KuuOSR63.two_minimal_form",NS+"mem_finite_basis"],
}

def admit(a,out):
    run=v.cache.api("actions/runs/"+str(RUN))
    v.need(run["head_sha"]==HEAD and run["run_attempt"]==1 and run["status"]=="completed" and run["conclusion"]=="success","R63 R3 run")
    for jid,steps in ((140499905603,["Verify R63 R3 finite obstruction basis completeness","Actual Lean MCP R63 R3 finite obstruction basis audit"]),
                      (140508863320,["Independently verify R63 R3 finite obstruction basis completeness"])):
        j=v.cache.api("actions/jobs/"+str(jid))
        v.need(j["run_id"]==RUN and j["head_sha"]==HEAD and j["status"]=="completed" and j["conclusion"]=="success" and
               all(any(s["name"]==n and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"]) for n in steps),"R63 R3 jobs")
    for aid,n,dig in ARTS:
        x=v.cache.api("actions/artifacts/"+str(aid))
        v.need(x["id"]==aid and x["name"]==n and x["digest"]==dig and not x["expired"] and
               x["workflow_run"]["id"]==RUN and x["workflow_run"]["head_sha"]==HEAD,"R63 R3 artifact")
    local=a.r63_local;other=a.r63_independent
    d=load(local/"direct.json");mp=load(local/"mcp.json");ind=load(other/"independent.json")
    v.need(d==load(other/"direct.json") and old.digest(d)==DIRECT and old.digest(mp)==MCP and
           mp["status"]=="R63_REAL_MCP_GREEN" and mp["direct_digest"]==DIRECT and
           ind["status"]=="R63_INDEPENDENT_FINITE_OBSTRUCTION_BASIS_COMPLETENESS_GREEN" and
           ind["direct_digest"]==DIRECT and ind["mcp_digest"]==MCP and ind["mcp_audits"]==144 and
           all(ind[k] for k in ("parent_bytes_preserved","raw_new_proofs_equal","basis_bytes_equal","raw_type_and_proof_equal")),"R63 R3 receipt")
    rows=d["fresh_application"]["observations"]
    v.need(len(rows)==144 and [{"name":x["name"],"axioms":x["axioms"]} for x in rows]==mp["audits"],"R63 R3 audit")
    for name in FILES:
        r63.copy_equal(local/name,other/name,out/name)
    record=load(out/r63.NEW)
    v.need(record["key"]==KEY and r63.r62.gate.base.portable.seal(record)["key"]==KEY and
           record["parent_duality_key"]==load(out/r63.r62.NEW)["key"] and
           record["parent_obstruction_key"]==load(out/r63.r62.r60.NEW)["key"],"R63 R3 key")
    v.need(d["certified_context_count"]==7 and d["empty_inventory_hold_count"]==5 and d["ledger_cut_count"]==1856 and
           len(record["contexts"])==7 and len(record["empty_inventory_holds"])==5 and
           sum(len(x["encoded_cuts"]) for x in record["contexts"])==1856,"R63 ledger scope")
    v.need(all(d.get(k) is False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
        "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved")),
        "R63 authority")
    v.need({n:old.digest(x) for n,x in record["raw_theorems"].items()}==d["raw_theorem_digests"],"R63 raw digests")
    for folder in ("capsule","joint-capsule"):
        manifest=d["capsule_manifest" if folder=="capsule" else "joint_capsule_manifest"]
        tool=r63.r62.r39 if folder=="capsule" else r63.r62.r45
        v.need(tool.capsule_files(local/folder)==tool.capsule_files(other/folder)==manifest["files"],"parent capsule manifest")
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
        source=manifest["module"]+".lean"
        v.need(r63.r62.r23.sha((out/folder/source).read_bytes())==manifest["source_sha256"],"parent capsule source")
        tool.install(out/folder,manifest)
    receipts=out/"parent-r63-receipts";receipts.mkdir()
    for name,src in (("direct.json",local),("mcp.json",local),("independent.json",other)):
        shutil.copyfile(src/name,receipts/name)
    for name in ("formal-source.lean","finite-ledger.lean","formal-source-r1.lean","r63-r2-repair.json",
                 "r63-r3-repair.json","parent-r62-raw-replay.json"):
        r63.copy_equal(local/name,other/name,receipts/name)
    v.need(r63.r62.r23.sha((receipts/"formal-source.lean").read_bytes())==record["formal_source_sha256"] and
           r63.r62.r23.sha((receipts/"finite-ledger.lean").read_bytes())==record["ledger_source_sha256"] and
           load(receipts/"r63-r3-repair.json")["parent_raw_replay_bytewise_equal"] is True and
           load(receipts/"parent-r62-raw-replay.json")==load(out/r63.r62.NEW)["raw_theorems"],"R63 source and raw lineage")
    for i in range(54,63):
        folder="parent-r"+str(i)+"-receipts"
        # R62 receipts include the three immutable Lean source files.
        for src in sorted((local/folder).iterdir()):
            if src.is_file():r63.copy_equal(src,other/folder/src.name,out/folder/src.name)
    return d,mp,ind,record

def raw_observer(names):
    return r63.raw_observer(names).replace("KUUOS_R63_RAW ","KUUOS_R64_RAW ").replace("R63 theorem","R64 theorem").replace("R63 not a theorem","R64 not a theorem").replace("R63 proof unavailable","R64 proof unavailable")

def raw_audit(log,by,names):
    rows=[json.loads(x[len("KUUOS_R64_RAW "):]) for x in log.splitlines() if x.startswith("KUUOS_R64_RAW ")]
    result={x["name"]:x for x in rows}
    v.need(len(rows)==len(names) and set(result)==set(names),"R64 raw inventory")
    for n,x in result.items():
        v.need(x["type_expr"]==by[n]["type_expr_repr"] and bool(x["proof_expr"]) and "sorryAx" not in x["proof_expr"] and
            sorted(set(x["axioms"]))==by[n]["axioms"] and x["universe_parameters"]==by[n]["universe_parameters"] and
            not set(x["axioms"])-{"propext","Classical.choice","Quot.sound"},"R64 raw proof")
    return result

def direct(a,out):
    scope=r63.r62.r29.observe_scope()
    d,mp,ind,parent=admit(a,out)
    formal=FORMAL.read_text(encoding="utf-8")
    (out/"formal-source.lean").write_text(formal,encoding="utf-8")
    source=d["fresh_application"]["mcp_source"]+"\n"+formal+"\n"+raw_observer(NAMES)
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    expected={n:x["expected_direct_refs"] for n,x in hist.items()}
    expected.update({NS+n:REFS.get(n,[]) for n in GENERAL+TESTS})
    p=ROOT/"artifacts"/"olean-r62"/"RecoveryDualityR62.lean"
    p.parent.mkdir(parents=True,exist_ok=False)
    try:
        log=r63.r62.r23.run_lean([],p,source+v.suffix(sorted(expected)))
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
    v.need({n:by[n] for n in hist}==hist,"R63 full audit drift")
    previous63=r63.raw_audit(log,by,tuple(d["new_theorem_names"]))
    previous62=r63.r62.gate.raw_audit(log,by)
    v.save(out/"parent-r63-raw-replay.json",previous63)
    v.save(out/"parent-r62-raw-replay.json",previous62)
    v.need(previous63==parent["raw_theorems"] and previous62==load(out/r63.r62.NEW)["raw_theorems"],"parent exact raw type/proof/axiom drift")
    raw=raw_audit(log,by,NAMES)
    v.need(len(audit)==144+len(NAMES) and r63.r62.r29.observe_scope()==scope,"R64 scope")
    boundary={k:False for k in ("proof_authority","action_authority","release_authorized","active_policy_changed",
      "semantic_search_complete","complete_transitive_closure","all_repository_dependencies_observed","python_general_correctness_proved","policy_is_refutation")}
    boundary.update({"all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"external_approval_required":True})
    record=r63.r62.gate.base.portable.seal({"schema":"kuuos.codeai.finite-transversal-enumerator.v1",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_basis_key":KEY,"r63_direct_digest":DIRECT,"r63_mcp_digest":MCP,
        "formal_source_sha256":r63.r62.r23.sha(formal.encode()),
        "algorithm":"witness-product, deduplication, inclusion-minimal reduction",
        "domain":"explicit finite route inventory with finite dependency sets",
        "global_semantic_search_claim":False,"r60_ledger_recomputed_by_general_enumerator":False,
        "general_theorems":list(GENERAL),"executable_tests":list(TESTS),
        "raw_theorems":raw,"formal_observations":{n:by[n] for n in NAMES},**boundary})
    v.save(out/NEW,record)
    result={"status":"R64_DIRECT_FINITE_TRANSVERSAL_ENUMERATOR",
        "source_head":r63.r62.gate.base.CURRENT,"source_tree":r63.r62.gate.base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "parent_basis_key":KEY,"enumerator_key":record["key"],"r63_direct_digest":DIRECT,"r63_mcp_digest":MCP,
        "capsule_manifest":d["capsule_manifest"],"joint_capsule_manifest":d["joint_capsule_manifest"],
        "general_theorems":len(GENERAL),"executable_tests":len(TESTS),
        "formal_source_sha256":record["formal_source_sha256"],"new_theorem_names":list(NAMES),
        "new_theorem_axioms":sorted({ax for x in raw.values() for ax in x["axioms"]}),
        "raw_theorem_digests":{n:old.digest(x) for n,x in raw.items()},"capsule_rebuilds":0,"active_dispatches":0,
        "new_root_discovery_trials":0,"parent_raw_replay_bytewise_equal":True,"r60_ledger_recomputed_by_general_enumerator":False,
        **boundary,"fresh_application":{"observations":audit,"mcp_source":source}}
    v.save(out/"direct.json",result)
    print("KUUOS_R64_DIRECT",json.dumps({k:x for k,x in result.items() if k not in ("fresh_application","capsule_manifest","joint_capsule_manifest")}|
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
                                     "clientInfo":{"name":"KuuOS finite transversal enumerator","version":"1"}})
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
    result={"status":"R64_REAL_MCP_GREEN","direct_digest":old.digest(d),"audits":rows,
            "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":version}
    v.save(out/"mcp.json",result)
    print("KUUOS_R64_MCP",json.dumps({"mcp_digest":old.digest(result),"audited":len(rows)}),flush=True)

def independent(d,first,out):
    a=load(first/"direct.json");mp=load(first/"mcp.json")
    v.need(a==d and mp["status"]=="R64_REAL_MCP_GREEN" and mp["direct_digest"]==old.digest(d),"independent R64 receipt")
    diag=v.structured(load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
        and diag["failed_dependencies"]==[] and not any(z.get("severity") in ("error","warning") for z in diag["items"]),"R64 MCP diagnostics")
    rows=d["fresh_application"]["observations"]
    v.need(len(mp["audits"])==len(rows),"R64 MCP inventory")
    for j,row in enumerate(rows):
        raw=load(first/f"mcp-verify-{j}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[] and
            normalize(val["axioms"])==row["axioms"]==mp["audits"][j]["axioms"] and
            row["name"]==mp["audits"][j]["name"],"R64 MCP evidence")
    for name in FILES+(NEW,"formal-source.lean","parent-r63-raw-replay.json","parent-r62-raw-replay.json"):
        v.need((out/name).read_bytes()==(first/name).read_bytes(),"independent R64 ledger bytes "+name)
    for folder in ("capsule","joint-capsule",*("parent-r"+str(i)+"-receipts" for i in range(54,64))):
        for path in (out/folder).rglob("*"):
            if path.is_file():v.need(path.read_bytes()==(first/path.relative_to(out)).read_bytes(),"independent parent bytes")
    result={k:x for k,x in d.items() if k!="fresh_application"}
    result.update({"status":"R64_INDEPENDENT_FINITE_TRANSVERSAL_ENUMERATOR_GREEN",
        "direct_digest":old.digest(d),"mcp_digest":old.digest(mp),"mcp_audits":len(rows),
        "enumerator_bytes_equal":True,"raw_new_proofs_equal":True,"parent_bytes_preserved":True,
        "raw_type_and_proof_equal":True,"unobserved_module_count":695})
    v.save(out/"independent.json",result)
    print("KUUOS_R64_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    for x in ("r63-local","r63-independent","first"):p.add_argument("--"+x,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output")
    if a.phase=="mcp":mcp(out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a,out)
    if a.phase=="independent":independent(d,a.first,out)
if __name__=="__main__":main()
