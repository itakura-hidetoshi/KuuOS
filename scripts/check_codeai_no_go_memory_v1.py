#!/usr/bin/env python3
"""Existing no-go and positive controls, direct pinned Lean then real MCP.

No public theorem additions, no candidate provider calls, no compiler-error
as refutation. Exact closed-proposition types are checked in Lean itself.
Separate runner repeats the typed applications before route projection.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path.cwd().resolve()
INSTALL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(INSTALL))
from runtime import kuuos_codeai_no_go_memory_v1 as n
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.codeai_prior_proof_kernel_recall_v0_4 import canonical_direct_options, suffix, read_direct, sha, save
from scripts import ci_verified_lean_project_cache_v1 as cache
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, EXPECTED_SERVER_VERSION, DISABLED_DURING_PROBE,
    call_tool, tool_map, server_version)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

MAIN="e1d754e8e0fc9382001a2e698751aa11d4272b84"
TREE="bdf2e81fc2cf702481b80e7079e59b1b47836013"
SCOPE="2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b"
MARK="KUUOS_EXACT_NOGO_TARGET "

def need(ok,reason):
    if not ok:
        raise ValueError(reason)

def recall(head):
    need(head==MAIN,"pilot exact canonical head changed")
    obs=github_observation(head,"canonical_main")
    scope=cache.local_scope(ROOT,head)
    need(obs["source_tree"]==TREE and scope==cache.remote_scope(cache.api,head)
         and digest(scope)==SCOPE,"proof scope mismatch")
    result=n.recall_no_go_frontier(ROOT,obs,n.SUBJECT)
    need(result["status"]=="REVIEW_REQUIRED","no-go retrieval held: "+repr(result.get("issues")))
    need({a["name"] for a in result["anchors"]}=={n.PREFIX+k for k in n.ANCHORS},
         "anchored inventory incomplete")
    # The ordinary search and the curated obstruction anchors are BOTH
    # retained; lexical hits not independently reviewed are not discarded.
    need(result["semantic_search_complete"] is False and result["unreviewed_hits_retained"],
         "retrieval authority escalated")
    return result

def render():
    lines=["import "+n.MODULE,"","namespace "+n.NS,"open Kuu.LivingEngi",
           "set_option autoImplicit false",""]
    for key,(prop,witness,polarity) in n.CASES.items():
        ty=("¬ " if polarity=="negative" else "")+key+"_target"
        lines+=["def "+key+"_target : Prop := "+prop,
                "theorem "+key+"_witness : "+ty+" := "+witness,""]
    lines+=["theorem original_raw_via_criterion : ¬ original_raw_target :=",
            "  (no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal",
            "    northNativeF55TwoChartCover northNativeF55Observe northNativeF55TwoChartRaw",
            "    nativeF55_twoChart_cover nativeF55_twoChart_shadow_global).2",
            "    nativeF55_twoChart_not_overlapFiberFaithful","",
            "end "+n.NS,"","open Lean",""]
    for key,(_,_,polarity) in n.CASES.items():
        target=n.NS+"."+key+"_target"; witness=n.NS+"."+key+"_witness"
        quote=chr(96)*2
        expected=("mkApp (mkConst "+quote+"Not) (mkConst "+quote+target+")"
                  if polarity=="negative" else "mkConst "+quote+target)
        lines+=["run_cmd do","  let env ← getEnv",
                "  let some t := env.find? "+quote+target+' | throwError "missing target"',
                "  let some w := env.find? "+quote+witness+' | throwError "missing witness"',
                '  let some v := t.value? (allowOpaque := true) | throwError "missing target body"',
                "  let expected := "+expected,
                '  unless w.isTheorem && w.type == expected do throwError "exact witness type mismatch"',
                '  if v.hasMVar || v.hasFVar then throwError "unresolved target"',
                "  let payload := Lean.Json.mkObj [",
                '    ("target_id", Lean.toJson "'+key+'"),',
                '    ("target_name", Lean.toJson "'+target+'"),',
                '    ("witness_name", Lean.toJson "'+witness+'"),',
                '    ("polarity", Lean.toJson "'+polarity+'"),',
                '    ("target_expr_repr", Lean.toJson (reprStr v)),',
                '    ("witness_type_repr", Lean.toJson (reprStr w.type)),',
                '    ("exact_kernel_type_match", Lean.toJson true)]',
                '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    names=[n.PREFIX+k for k in sorted(n.ANCHORS)]
    names += [n.NS+"."+k+"_witness" for k in n.CASES]+[n.NS+".original_raw_via_criterion"]
    return "\n".join(lines)+"\n"+suffix(names),names

def compile_source(path,source):
    path.write_text(source,encoding="utf-8")
    opts=canonical_direct_options((ROOT/"lakefile.toml").read_bytes())
    p=subprocess.run(["lake","env","lean",*opts,str(path.relative_to(ROOT))],
                     cwd=ROOT,capture_output=True,text=True,timeout=600)
    log=p.stdout+"\n"+p.stderr
    path.with_suffix(".log").write_text(log,encoding="utf-8")
    return p.returncode,log

def direct(head,out):
    r=recall(head)
    save(out/"recall.json",r)
    source,names=render()
    selected=[{"name":a["name"],"path":a["path"],"blob":a["source_blob"],
               "observation_kind":a["observation_kind"],"expected_direct_refs":[]}
              for a in r["anchors"]]
    selected += [{"name":n.NS+"."+key+"_witness","expected_direct_refs":[n.PREFIX+witness],
                  "observation_kind":"typed_application"}
                 for key,(_,witness,_) in n.CASES.items()]
    selected += [{"name":n.NS+".original_raw_via_criterion","observation_kind":"conditional_application",
                  "expected_direct_refs":[n.PREFIX+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal",
                                          n.PREFIX+"nativeF55_twoChart_not_overlapFiberFaithful",
                                          n.PREFIX+"nativeF55_twoChart_cover",
                                          n.PREFIX+"nativeF55_twoChart_shadow_global"]}]
    code,log=compile_source(out/"Probe.lean",source)
    if code:
        print(log[-20000:],flush=True)
        raise ValueError("direct typed witness Lean failed")
    rows=read_direct(log,selected)
    matches=[json.loads(s[len(MARK):]) for s in log.splitlines() if s.startswith(MARK)]
    need(len(matches)==len(n.CASES) and {a["target_id"] for a in matches}==set(n.CASES),
         "typed target inventory missing")
    apps={a["target_id"]:a for a in matches}
    # Observe that the historical negative theorem and conditional type are
    # really present. The conditional criterion alone cannot refute P.
    parent,_=n.load_packets(ROOT)
    original=next(x for x in parent["observations"] if x["name"]==n.PREFIX+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal")
    row=next(x for x in rows if x["name"]==original["name"])
    need(row["type_expr_sha256"]==original["type_expr_sha256"] and row["axioms"]==original["axioms"],
         "historical conditional criterion changed")
    # Deliberate new negative test: exact no-go must NOT be transported to
    # the alternative atlas. The resulting compiler error is not a no-go.
    wrong="import "+n.MODULE+"\nopen Kuu.LivingEngi\nexample : ¬ HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartConstantRaw := nativeF55_twoChart_raw_no_global\n"
    rc,err=compile_source(out/"WrongScope.lean",wrong)
    need(rc!=0 and "error:" in err and "type mismatch" in err.lower(),
         "wrong-scope witness unexpectedly accepted")
    print("KUUOS_NO_GO_WRONG_SCOPE_REJECTED",rc,flush=True)
    for key,(prop,_,_) in n.CASES.items():
        pre=n.target_preflight(r,key,prop)
        need(pre["status"]=="HOLD_NO_GO_REVIEW" and not pre["candidate_generation_allowed"],
             "unindependently-verified witness promoted")
    unknown=n.target_preflight(r,"conditional_without_hbad","HasGlobal U s")
    need(unknown["status"]=="HOLD_NO_GO_REVIEW" and not unknown["candidate_generation_allowed"],
         "missing hypothesis treated as refutation or permission")
    changed=n.target_preflight(r,"original_raw",n.CASES["alternative_raw"][0])
    need(changed["status"]=="HOLD_NO_GO_REVIEW","different target accepted")
    current={"schema":"kuuos.codeai.selected-no-go-application.v1","status":"DIRECT_TYPED_NO_GO_GREEN",
             "source_head":head,"source_tree":r["source_tree"],"recall_digest":r["receipt_digest"],
             "scope_digest":SCOPE,"probe_sha256":sha(source.encode()),"observations":rows,
             "applications":apps,"wrong_scope_lean_exit":rc,
             "wrong_scope_diagnostic_only":True,"conditional_without_hbad":"HOLD_NO_GO_REVIEW",
             "historical_conditional_type_sha256":row["type_expr_sha256"],
             "provider_calls":0,"public_source_changed":False,"proof_authority":False,
             "novelty_certified":False}
    save(out/"direct.json",current)
    need(recall(head)["receipt_digest"]==r["receipt_digest"],"source recall drift")
    print("KUUOS_NO_GO_DIRECT_GREEN",json.dumps({"direct_digest":digest(current),
        "source_head":head,"anchors":len(r["anchors"]),"lexical_hits":r["lexical_receipt"]["total_hits"],
        "negative_hints":len(r["lexical_negative_hint_ids"]),"parse_gaps":len(r["lexical_receipt"]["parse_gaps"]),
        "typed_applications":len(apps),"observed_declarations":len(rows),
        "axioms":sorted({a for x in rows for a in x["axioms"]}),
        "wrong_scope_rejected":True,"conditional_without_hbad":"HOLD","provider_calls":0,
        "semantic_search_complete":False},sort_keys=True),flush=True)
    return current

def mcp(head,out):
    d=json.loads((out/"direct.json").read_text())
    r=json.loads((out/"recall.json").read_text())
    need(d["source_head"]==head and d["recall_digest"]==r["receipt_digest"]
         and r==recall(head) and sha((out/"Probe.lean").read_bytes())==d["probe_sha256"],
         "unbound direct evidence")
    command=["uvx","--from",f"lean-lsp-mcp=={EXPECTED_SERVER_VERSION}","lean-lsp-mcp","--transport","stdio"]
    ver=server_version(command[:-2],ROOT)
    client=MCPClient(command,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),
        "LEAN_LOG_LEVEL":"NONE","LEAN_MCP_DISABLED_TOOLS":DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[]
    try:
        client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"KuuOS selected no-go recall","version":"1"}})
        client.notify("notifications/initialized")
        tools=tool_map(client.request("tools/list"))
        need({"lean_diagnostic_messages","lean_verify"}.issubset(tools),"real MCP tools unavailable")
        rel=str((out/"Probe.lean").relative_to(ROOT))
        raw=call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        save(out/"mcp-diagnostics.json",raw)
        diag=structured(raw)
        need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
             and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
             and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
             "real MCP diagnostics incomplete")
        for i,row in enumerate(d["observations"]):
            raw=call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
            save(out/f"mcp-verify-{i}.json",raw)
            v=structured(raw)
            need(isinstance(v.get("axioms"),list) and sorted(set(v["axioms"]))==row["axioms"]
                 and v.get("warnings")==[],"real MCP axiom mismatch: "+row["name"])
            rows.append({"name":row["name"],"axioms":row["axioms"]})
    finally:
        client.close()
    receipt={"status":"REAL_LEAN_MCP_NO_GO_GREEN","direct_digest":digest(d),
             "mcp_version":EXPECTED_SERVER_VERSION,"version_output":ver,"observations":rows}
    save(out/"mcp.json",receipt)
    print("KUUOS_NO_GO_REAL_MCP",json.dumps({"observed":len(rows),"direct_digest":digest(d),
        "mcp_digest":digest(receipt)},sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="mcp":
        mcp(a.head,out)
        return
    current=direct(a.head,out)
    if a.phase=="independent":
        need(a.first is not None,"first runner evidence required")
        prior=json.loads((a.first/"direct.json").read_text())
        mp=json.loads((a.first/"mcp.json").read_text())
        r=json.loads((out/"recall.json").read_text())
        need(json.loads((a.first/"recall.json").read_text())==r and prior==current,
             "independent typed evidence differs")
        routes=n.observe_selected_routes(r,prior,current,mp)
        need(routes["status"]=="INDEPENDENT_SELECTED_NO_GO_ROUTES_OBSERVED",repr(routes))
        need(sum(v["status"]=="REFUTED_EXACT_TARGET" for v in routes["routes"].values())==3
             and sum(v["status"]=="REUSE_EXISTING" for v in routes["routes"].values())==3
             and not routes["candidate_generation_allowed"],"positive/negative routing mismatch")
        stale=n.observe_selected_routes(r,prior,dict(current,source_head="0"*40),mp)
        need(stale["status"]=="HOLD_NO_GO_REVIEW","wrong independent evidence promoted")
        save(out/"routes.json",routes)
        receipt={"status":"INDEPENDENT_NO_GO_GREEN","direct_digest":digest(current),
                 "mcp_digest":digest(mp),"route_digest":digest(routes),
                 "routes":{k:v["status"] for k,v in routes["routes"].items()},
                 "conditional_without_hbad":"HOLD_NO_GO_REVIEW","provider_calls":0,
                 "semantic_search_complete":False,"proof_authority":False,"novelty_certified":False}
        save(out/"independent.json",receipt)
        print("KUUOS_NO_GO_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

if __name__=="__main__":
    main()
