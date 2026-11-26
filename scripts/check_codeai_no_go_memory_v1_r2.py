#!/usr/bin/env python3
"""R2: retain R1 direct evidence; normalize only observed standard universe
annotations, not arbitrary names. Actual MCP verifies the exact declaration
prefix under explicit pp.universes=false. Independent CI repeats direct Lean.
No proof changes or lowered acceptance conditions.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import tempfile
import zipfile

import check_codeai_no_go_memory_v1 as v
from runtime import kuuos_codeai_no_go_memory_v1 as n

ROOT=v.ROOT
RUN=45739271670
HEAD="1928158206e06431751123e5b52ebcb02fbc8c6c"
ART=15080457601
ART_SHA="b14862b4ac55e4af1a39e04dd18ef553faea575486397b8c0d88a6bfc5789104"
DIRECT="84feb3de775f8cf8f49183936cf231ab7f31f933d4b40b31bf52f1980ff11305"
FIRST="Kuu.LivingEngi.nativeF55_constant_twoChart_refined_global"
STANDARD={"Classical.choice","Quot.sound","propext"}
# The exact two suffix forms actually observed in the failed MCP artifact.
OBSERVED_UNIVERSE_DISPLAY={"Classical.choice.{u}":"Classical.choice",
                           "Quot.sound.{u}":"Quot.sound"}

def normalize(values):
    v.need(isinstance(values,list) and all(isinstance(a,str) for a in values),
           "MCP axiom inventory not a list of names")
    out=[]
    for a in values:
        name=OBSERVED_UNIVERSE_DISPLAY.get(a,a)
        v.need(name in STANDARD,"unrecognized axiom name/display: "+a)
        out.append(name)
    v.need(len(out)==len(set(out)),"ambiguous duplicate axiom representation")
    return sorted(out)

def regressions():
    v.need(normalize(["propext","Classical.choice.{u}","Quot.sound.{u}"])==sorted(STANDARD),
           "observed universe-display regression failed")
    for bad in (["sorryAx"],["Other.Classical.choice.{u}"],
                ["Classical.choice.{v}"],["propext.{u}"],
                ["Classical.choice","Classical.choice.{u}"]):
        try:
            normalize(bad)
        except ValueError:
            continue
        raise ValueError("invalid axiom representation accepted: "+repr(bad))

def archived(head,out):
    """Only reuse direct observations of the identical canonical source/probe.
    The failed overall workflow is not promoted to independent certification.
    """
    run=v.cache.api(f"actions/runs/{RUN}")
    v.need(run["head_sha"]==HEAD and run["status"]=="completed"
           and run["conclusion"]=="failure" and run["run_attempt"]==1,
           "historical run identity mismatch")
    jobs=v.cache.api(f"actions/runs/{RUN}/jobs?per_page=100")
    j=next(j for j in jobs["jobs"] if j["id"]==139639998161)
    v.need(j["status"]=="completed" and j["conclusion"]=="failure"
           and any(s["name"]=="Recall negative and positive evidence, verify exact typed targets"
                   and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"])
           and any(s["name"]=="Actual Lean MCP diagnostics and verification"
                   and s["conclusion"]=="failure" for s in j["steps"]),
           "historical direct/MCP boundary mismatch")
    art=v.cache.api(f"actions/artifacts/{ART}")
    v.need(art["id"]==ART and art["size_in_bytes"]==33011
           and art["digest"]=="sha256:"+ART_SHA and art["expired"] is False
           and art["workflow_run"]["id"]==RUN and art["workflow_run"]["head_sha"]==HEAD
           and art["workflow_run"]["repository_id"]==v.cache.REPO_ID
           and art["workflow_run"]["head_repository_id"]==v.cache.REPO_ID,
           "historical artifact metadata mismatch")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"r1.zip"
        v.cache.download_zip({"artifact_id":ART,"artifact_size":33011,"artifact_digest":ART_SHA},p)
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            v.need(len(names)==len(set(names)) and len(names)<40,"archive inventory")
            rows={}
            for name in ("direct.json","recall.json","Probe.lean","Probe.log",
                         "WrongScope.lean","WrongScope.log","mcp-verify-0.json","mcp-diagnostics.json"):
                i=z.getinfo(name)
                v.need(not i.is_dir() and 0<i.file_size<10_000_000,"invalid archive member")
                rows[name]=z.read(i)
    d=json.loads(rows["direct.json"]); r=json.loads(rows["recall.json"])
    raw=json.loads(rows["mcp-verify-0.json"])
    q=v.structured(raw)
    v.need(v.digest(d)==DIRECT and d["source_head"]==head and d["source_tree"]==v.TREE
           and d["scope_digest"]==v.SCOPE and d["recall_digest"]==r["receipt_digest"]
           and d["status"]=="DIRECT_TYPED_NO_GO_GREEN" and r==v.recall(head)
           and rows["Probe.lean"]==v.render()[0].encode()
           and v.sha(rows["Probe.lean"])==d["probe_sha256"],
           "archived direct evidence does not bind current source")
    row=d["observations"][0]
    v.need(row["name"]==FIRST and row["axioms"]==sorted(STANDARD)
           and q["warnings"]==[] and set(q["axioms"])=={"propext","Classical.choice.{u}","Quot.sound.{u}"}
           and normalize(q["axioms"])==row["axioms"],"archived mismatch not the observed display difference")
    for name in ("direct.json","recall.json","Probe.lean","Probe.log","WrongScope.lean","WrongScope.log"):
        (out/name).write_bytes(rows[name])
    v.save(out/"r1-mcp-display-diagnosis.json",{"run_id":RUN,"head":HEAD,"artifact_id":ART,
        "direct_digest":DIRECT,"name":FIRST,"expected_axioms":row["axioms"],
        "raw_mcp_response":raw,"normalized_axioms":normalize(q["axioms"]),
        "original_run_not_independently_certified":True})
    print("KUUOS_NOGO_R1_DIRECT_REUSED",json.dumps({"direct_digest":DIRECT,
        "raw_axioms":q["axioms"],"normalized_axioms":normalize(q["axioms"]),
        "historical_run":RUN,"new_direct_execution":False},sort_keys=True),flush=True)

def mcp(head,out):
    regressions()
    d=json.loads((out/"direct.json").read_text())
    r=json.loads((out/"recall.json").read_text())
    src=(out/"Probe.lean").read_text(encoding="utf-8")
    v.need(d["source_head"]==head and d["recall_digest"]==r["receipt_digest"]
           and r==v.recall(head) and v.sha(src.encode())==d["probe_sha256"]
           and src==v.render()[0] and v.digest(d)==DIRECT,"unbound direct evidence")
    # Same definitions and witness bodies. Only remove the observation
    # metaprogram tail, and explicitly select name-only axiom printing.
    boundary="end "+n.NS+"\n\nopen Lean\n"
    v.need(src.count(boundary)==1,"probe declaration boundary mismatch")
    prefix,tail=src.split(boundary)
    declarations=prefix+"end "+n.NS+"\n"
    source=declarations+"\nset_option pp.universes false\n"+"\n".join(
        "#check @"+row["name"] for row in d["observations"])+"\n"
    f=out/"McpProbe.lean"
    f.write_text(source,encoding="utf-8")
    v.need(src.startswith(declarations) and source.startswith(declarations),"witness prefix changed")
    # Directly elaborate the exact small MCP source as well; reject
    # errors, warnings and new axioms, without modifying the declarations.
    code,log=v.compile_source(f,source)
    v.need(code==0 and not v.re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked|sorryAx)",log),
           "MCP declaration-prefix direct Lean failed")
    command=["uvx","--from",f"lean-lsp-mcp=={v.EXPECTED_SERVER_VERSION}","lean-lsp-mcp","--transport","stdio"]
    ver=v.server_version(command[:-2],ROOT)
    client=v.MCPClient(command,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),
        "LEAN_LOG_LEVEL":"NONE","LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
            "clientInfo":{"name":"KuuOS no-go exact-name audit","version":"1.2"}})
        client.notify("notifications/initialized")
        tools=v.tool_map(client.request("tools/list"))
        v.need({"lean_diagnostic_messages","lean_verify"}.issubset(tools),"real MCP tools unavailable")
        rel=str(f.relative_to(ROOT))
        raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        v.save(out/"mcp-diagnostics.json",raw)
        diag=v.structured(raw)
        v.need(diag.get("success") is True and diag.get("partial") is False and diag.get("timed_out") is False
               and diag.get("failed_dependencies")==[] and isinstance(diag.get("items"),list)
               and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
               "real MCP diagnostics incomplete")
        for i,row in enumerate(d["observations"]):
            raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
            v.save(out/f"mcp-verify-{i}.json",raw)
            result=v.structured(raw)
            print("KUUOS_NOGO_MCP_AUDIT",json.dumps({"name":row["name"],"expected":row["axioms"],
                 "raw_axioms":result.get("axioms"),"warnings":result.get("warnings")},ensure_ascii=False),flush=True)
            v.need(result.get("warnings")==[] and normalize(result.get("axioms"))==row["axioms"],
                   "real MCP axiom mismatch: "+row["name"])
            rows.append({"name":row["name"],"axioms":row["axioms"],"raw_axioms":result["axioms"]})
    finally:
        client.close()
    receipt={"status":"REAL_LEAN_MCP_NO_GO_GREEN","direct_digest":v.digest(d),
        "mcp_version":v.EXPECTED_SERVER_VERSION,"version_output":ver,"observations":rows,
        "mcp_probe_sha256":v.sha(source.encode()),"declaration_prefix_sha256":v.sha(declarations.encode()),
        "normalization_policy":"only two observed standard universe annotations",
        "raw_responses_preserved":True}
    v.save(out/"mcp.json",receipt)
    print("KUUOS_NO_GO_REAL_MCP",json.dumps({"observed":len(rows),"direct_digest":v.digest(d),
        "mcp_digest":v.digest(receipt)},sort_keys=True),flush=True)

def independent(head,out,first):
    current=v.direct(head,out)
    prior=json.loads((first/"direct.json").read_text())
    mp=json.loads((first/"mcp.json").read_text())
    r=json.loads((out/"recall.json").read_text())
    v.need(v.digest(current)==DIRECT and prior==current
           and json.loads((first/"recall.json").read_text())==r,
           "independent direct observations differ")
    v.need(mp["direct_digest"]==DIRECT and mp["raw_responses_preserved"] is True,
           "MCP receipt unbound")
    routes=n.observe_selected_routes(r,prior,current,mp)
    v.need(routes["status"]=="INDEPENDENT_SELECTED_NO_GO_ROUTES_OBSERVED",repr(routes))
    v.need(sum(x["status"]=="REFUTED_EXACT_TARGET" for x in routes["routes"].values())==3
           and sum(x["status"]=="REUSE_EXISTING" for x in routes["routes"].values())==3
           and not routes["candidate_generation_allowed"],"route mismatch")
    v.need(n.observe_selected_routes(r,prior,dict(current,source_head="0"*40),mp)["status"]=="HOLD_NO_GO_REVIEW",
           "wrong scope promoted")
    v.save(out/"routes.json",routes)
    receipt={"status":"INDEPENDENT_NO_GO_GREEN","direct_digest":v.digest(current),
             "mcp_digest":v.digest(mp),"route_digest":v.digest(routes),
             "routes":{k:x["status"] for k,x in routes["routes"].items()},
             "conditional_without_hbad":"HOLD_NO_GO_REVIEW","provider_calls":0,
             "historical_direct_reused_in_sandbox":True,"independent_direct_recomputed":True,
             "semantic_search_complete":False,"proof_authority":False,"novelty_certified":False}
    v.save(out/"independent.json",receipt)
    print("KUUOS_NO_GO_INDEPENDENT",json.dumps(receipt,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--head",required=True)
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="direct": archived(a.head,out)
    elif a.phase=="mcp": mcp(a.head,out)
    else:
        v.need(a.first is not None,"first runner evidence required")
        independent(a.head,out,a.first)

if __name__=="__main__":
    main()
