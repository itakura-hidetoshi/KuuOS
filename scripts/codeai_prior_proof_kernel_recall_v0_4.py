#!/usr/bin/env python3
"""Read-only selected kernel recall: exact source, actual Lean, real MCP."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import git_blob, digest
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import (
    MCPClient, PROTOCOL_VERSION, EXPECTED_SERVER_VERSION, DISABLED_DURING_PROBE,
    call_tool, server_version, tool_map)
from scripts.check_kuuos_lean_mcp_parent_pr3522_v155_v1 import structured

STANDARD={"propext","Classical.choice","Quot.sound"}
PREFIX="KUUOS_RECALL_KERNEL "
BASE_TREES={"formal":"facf2c867536127e655fefd379e4224ea98a8c4b",
            "lean":"e96df2a7e90a22bdfbea790e46bef4bad4d3eede"}
LEC="Kuu.LivingEngi."
QI="KUOS.Architecture.WuxingCyclicPaths."
PLANS=[
    {"path":"formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean",
     "blob":"c3c989eff7b430faa5350d1300b4a17f531da757",
     "module":"Kuu.LivingEngi.SourceAwareOverlapDescentCriterion",
     "query":"source aware overlap descent",
     "names":{
         LEC+"sourceGlobal_iff_shadowGlobal_and_overlapFaithful":[
             LEC+"sourceGlobal_implies_shadowGlobal",LEC+"sourceGlobal_implies_overlapFaithful",
             LEC+"shadowGlobal_and_overlapFaithful_implies_sourceGlobal"],
         LEC+"no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal":[
             LEC+"sourceGlobal_implies_overlapFaithful",
             LEC+"shadowGlobal_and_overlapFaithful_implies_sourceGlobal"]}},
    {"path":"formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean",
     "blob":"836a0cccc0263e33d652da6b9391e4d5c07cb368",
     "module":"KUOS.Architecture.QiWuxingNativeC60GaugeV3_4",
     "query":"c60 gauge slot injective",
     "names":{QI+"nativeC60GaugeSlot_injective":[QI+"nativeC60GaugeSlot_index"]}}
]

# The actual Lake compiler options of the frozen original public library.
# Direct "lake env lean" does not inherit its module-setup leanOptions.
# Reproduce precisely the existing canonical policy, never introduce a new
# linter exemption or relax kernel / warning / sorry checks in the scratch run.
LAKEFILE_BLOB="947bac41f9535a7ba2ef03a93081cdfbc1b946f7"
CANONICAL_LEAN_OPTIONS={
    "warningAsError": True,
    "linter.unnecessarySimpa": False,
    "linter.unusedVariables": False,
    "linter.unusedSectionVars": False,
    "weak.linter.unreachableTactic": False,
    "weak.linter.unnecessarySeqFocus": False,
    "weak.linter.unusedTactic": False,
    "weak.linter.unusedSimpArgs": False,
}

def canonical_direct_options(raw):
    if git_blob(raw)!=LAKEFILE_BLOB:
        raise ValueError("NO_DATA: canonical Lake config blob drift")
    config=tomllib.loads(raw.decode("utf-8"))
    libraries=[x for x in config["lean_lib"] if x["name"]=="KuuOSFormal"]
    if len(libraries)!=1 or libraries[0].get("leanOptions")!=CANONICAL_LEAN_OPTIONS:
        raise ValueError("NO_DATA: canonical library options differ")
    return ["-D"+k+"="+str(v).lower() for k,v in sorted(CANONICAL_LEAN_OPTIONS.items())]+["-Dweak.sorryAsError=true"]

def save(p,obj):
    p.write_text(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def sha(b):
    return hashlib.sha256(b).hexdigest()

def plan(root):
    obs=github_observation(os.environ["GITHUB_SHA"],"research_head")
    catalog=build_catalog(root,obs)
    if catalog["source_subtrees"]!=BASE_TREES:
        raise ValueError("NO_DATA: exact canonical source subtrees changed")
    files={f["path"]:f for f in catalog["files"]}
    selected=[]
    for p in PLANS:
        f=files[p["path"]]
        if f["blob"]!=p["blob"] or f["module_path_lexical"]!=p["module"]:
            raise ValueError("NO_DATA: selected source blob/module changed")
        q=search_catalog(catalog,p["query"],limit=500)
        if q["status"]!="REVIEW_REQUIRED":
            raise ValueError("NO_DATA: incomplete lexical retrieval "+p["query"])
        for name,refs in p["names"].items():
            hits=[x for x in q["hits"] if x["path"]==p["path"] and
                  x["name_lexical"]==name.rsplit(".",1)[-1] and x["kind"]=="theorem"]
            if len(hits)!=1:
                raise ValueError("NO_DATA: recalled declaration not unique "+name)
            hit=hits[0]
            selected.append({"name":name,"path":p["path"],"blob":p["blob"],"module":p["module"],
                             "line":hit["line"],"lexical_id":hit["id"],
                             "lexical_receipt_digest":q["receipt_digest"],
                             "signature_preview_digest":hit["signature_digest"],
                             "expected_direct_refs":refs})
    return catalog,selected

def suffix(names):
    lines=["","","open Lean","set_option pp.universes true","set_option pp.explicit true",
           "set_option pp.fullNames true","set_option maxHeartbeats 4000000",""]
    for name in names:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*",name):
            raise ValueError("invalid fixed name")
        lines += [
            "#check @"+name,
            # Axiom identities are Lean Names, not pretty-printed Const expressions.
            # Preserve detailed universe printing for the type, but not for the
            # independently printed axiom inventory.
            "set_option pp.universes false in", "#print axioms "+name,"run_cmd do",
            "  let n := "+chr(96)*2+name,
            "  let env ← getEnv",
            '  let some info := env.find? n | throwError "constant not found"',
            '  unless info.isTheorem do throwError "not a theorem"',
            '  let some value := info.value? (allowOpaque := true) | throwError "proof value unavailable"',
            '  if info.type.hasMVar || value.hasMVar then throwError "unresolved metavariable"',
            '  if info.type.hasFVar || value.hasFVar then throwError "free local variable"',
            "  let ty ← Lean.Elab.Command.liftTermElabM do",
            "    return (← Lean.Meta.ppExpr info.type).pretty",
            "  let ax ← Lean.collectAxioms n",
            "  let payload := Lean.Json.mkObj [",
            '    ("name", Lean.toJson n.toString),',
            '    ("type_pretty", Lean.toJson ty),',
            '    ("type_expr_repr", Lean.toJson (reprStr info.type)),',
            '    ("universe_parameters", Lean.toJson (info.levelParams.map Name.toString)),',
            '    ("type_constants", Lean.toJson (info.type.getUsedConstants.map Name.toString)),',
            '    ("proof_constants", Lean.toJson (value.getUsedConstants.map Name.toString)),',
            '    ("axioms", Lean.toJson (ax.map Name.toString))]',
            '  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_RECALL_KERNEL " ++ payload.compress)',""]
    return "\n".join(lines)+"\n"

def read_direct(log,selected):
    if "sorryAx" in log or re.search(r"(?im)(?:\berror:|\bwarning:|PANIC at |Lean panicked)",log):
        raise ValueError("HOLD: direct Lean diagnostics")
    rows=[json.loads(s[len(PREFIX):]) for s in log.splitlines() if s.startswith(PREFIX)]
    expected={r["name"]:r for r in selected}
    if len(rows)!=len(expected) or {r.get("name") for r in rows}!=set(expected):
        raise ValueError("NO_DATA: missing, duplicate or unexpected kernel observation")
    printed={}
    for name,raw in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log,re.S):
        printed.setdefault(name,[]).append({s.strip() for s in raw.split(",") if s.strip()})
    for name in re.findall(r"'([^']+)' does not depend on any axioms",log):
        printed.setdefault(name,[]).append(set())
    result=[]
    for row in rows:
        entry=expected[row["name"]]
        for k in ("type_pretty","type_expr_repr"):
            if not isinstance(row.get(k),str) or not row[k].strip():
                raise ValueError("NO_DATA: missing type "+k)
        for k in ("universe_parameters","type_constants","proof_constants","axioms"):
            if not isinstance(row.get(k),list) or not all(isinstance(x,str) and x for x in row[k]):
                raise ValueError("NO_DATA: malformed inventory "+k)
            if k!="universe_parameters":
                row[k]=sorted(set(row[k]))
        if not row["type_constants"] or not row["proof_constants"]:
            raise ValueError("NO_DATA: empty expression reference list")
        if set(row["axioms"])-STANDARD:
            raise ValueError("HOLD: unexpected axiom")
        if not set(entry["expected_direct_refs"]).issubset(row["proof_constants"]):
            raise ValueError("NO_DATA: expected source proof dependency absent")
        reports=printed.get(row["name"],[])+printed.get(row["name"].rsplit(".",1)[-1],[])
        if not reports or any(r!=set(row["axioms"]) for r in reports):
            raise ValueError("NO_DATA: source-local axiom reports disagree: "+
                             row["name"]+"; printed="+repr([sorted(r) for r in reports])+
                             "; kernel="+repr(row["axioms"]))
        result.append({**entry,**row,"type_expr_sha256":sha(row["type_expr_repr"].encode()),
                       "proof_body_observed":True,"direct_expression_constants_only":True})
    return sorted(result,key=lambda x:x["name"])

def direct(root,out):
    cat,selected=plan(root)
    ver=subprocess.run(["lake","env","lean","--version"],cwd=root,check=True,
                       capture_output=True,text=True,timeout=30).stdout
    if "4.30.0-rc2" not in ver:
        raise ValueError("Lean executable pin mismatch")
    save(out/"selection.json",selected)
    options=canonical_direct_options((root/"lakefile.toml").read_bytes())
    save(out/"canonical-direct-options.json",{"lakefile_blob":LAKEFILE_BLOB,"argv":options})
    print("KUUOS_DIRECT_CANONICAL_OPTIONS",json.dumps(options),flush=True)
    results=[]
    for i,p in enumerate(PLANS):
        raw=(root/p["path"]).read_bytes()
        if git_blob(raw)!=p["blob"]:
            raise ValueError("source changed")
        appended=raw+suffix(list(p["names"])).encode()
        local=out/("LocalRecall_"+str(i)+".lean")
        with local.open("xb") as f:
            f.write(appended)
        try:
            result=subprocess.run(["lake","env","lean",*options,str(local.relative_to(root))],
                                  cwd=root,text=True,capture_output=True,timeout=900)
        except subprocess.TimeoutExpired as e:
            def txt(x): return x.decode("utf-8","replace") if isinstance(x,bytes) else x or ""
            (out/("direct-"+str(i)+".log")).write_text(txt(e.stdout)+"\n"+txt(e.stderr)+"\nTIMEOUT\n")
            raise
        log=result.stdout+"\n"+result.stderr
        (out/("direct-"+str(i)+".log")).write_text(log)
        if result.returncode:
            print(log[-16000:],flush=True)
            raise ValueError("direct Lean exit "+str(result.returncode))
        try:
            rows=read_direct(log,[r for r in selected if r["path"]==p["path"]])
        except ValueError:
            print(log[-16000:],flush=True)
            raise
        print("KUUOS_DIRECT_MODULE",p["module"],"exit=0",json.dumps([
            {"name":row["name"],"type_constants":len(row["type_constants"]),
             "proof_constants":len(row["proof_constants"]),"axioms":row["axioms"]} for row in rows]),flush=True)
        for row in rows:
            row.update(original_source_sha256=sha(raw),scratch_source_sha256=sha(appended),
                       compiler_log_sha256=sha(log.encode()))
        results.extend(rows)
        if (root/p["path"]).read_bytes()!=raw:
            raise ValueError("original source mutated")
    fresh,_=plan(root)
    if fresh["catalog_digest"]!=cat["catalog_digest"]:
        raise ValueError("catalog changed during observation")
    receipt={"schema":"kuuos.prior-proof-kernel-recall.v0.4",
             "source_head":os.environ["GITHUB_SHA"],"source_tree":cat["source_tree"],
             "source_subtrees":cat["source_subtrees"],"catalog_digest":cat["catalog_digest"],
             "pins":cat["pins"],"plan_digest":digest(selected),
             "lakefile_blob":LAKEFILE_BLOB,"canonical_direct_options":options,
             "observations":sorted(results,key=lambda x:x["name"]),
             "status":"DIRECT_SOURCE_LOCAL_OBSERVATION_GREEN",
             "original_sources_unchanged":True,"independent_runner_verified":False,
             "novelty_certified":False,"proof_authority":False,
             "full_transitive_proof_dependencies_verified":False}
    save(out/"direct.json",receipt)
    print("KUUOS_KERNEL_DIRECT",json.dumps({
        "source_head":receipt["source_head"],"observed":len(results),
        "results":[{"name":x["name"],"type_constants":len(x["type_constants"]),
                    "proof_constants":len(x["proof_constants"]),"axioms":x["axioms"]} for x in results]}),flush=True)

def mcp(root,out):
    d=json.loads((out/"direct.json").read_text())
    cat,selected=plan(root)
    if d["status"]!="DIRECT_SOURCE_LOCAL_OBSERVATION_GREEN" or d["source_head"]!=os.environ["GITHUB_SHA"] or d["catalog_digest"]!=cat["catalog_digest"] or d["plan_digest"]!=digest(selected):
        raise ValueError("NO_DATA: unbound direct receipt")
    dr={x["name"]:x for x in d["observations"]}
    command=["uvx","--from",f"lean-lsp-mcp=={EXPECTED_SERVER_VERSION}","lean-lsp-mcp","--transport","stdio"]
    ver=server_version(command[:-2],root)
    client=MCPClient(command,cwd=root,env={"LEAN_PROJECT_PATH":str(root),
        "LEAN_LOG_LEVEL":"NONE","LEAN_MCP_DISABLED_TOOLS":DISABLED_DURING_PROBE,
        "LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    rows=[]
    try:
        init=client.request("initialize",{"protocolVersion":PROTOCOL_VERSION,"capabilities":{},
                            "clientInfo":{"name":"KuuOS prior-proof recall","version":"0.4"}})
        client.notify("notifications/initialized")
        tools=tool_map(client.request("tools/list"))
        if not {"lean_hover_info","lean_diagnostic_messages","lean_verify"}.issubset(tools):
            raise ValueError("NO_DATA: real MCP tools missing")
        for i,p in enumerate(PLANS):
            f=out/("ImportedRecall_"+str(i)+".lean")
            names=list(p["names"])
            source="import "+p["module"]+"\n\n"+"\n".join("#check @"+n for n in names)+"\n"
            with f.open("x") as stream:
                stream.write(source)
            rel=str(f.relative_to(root))
            raw=call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
            save(out/("mcp-diagnostics-"+str(i)+".json"),raw)
            diag=structured(raw)
            if (diag.get("success") is not True or diag.get("partial") is not False
                or diag.get("timed_out") is not False or diag.get("failed_dependencies")!=[]
                or not isinstance(diag.get("items"),list)
                or any(x.get("severity") in ("error","warning") for x in diag["items"])):
                raise ValueError("NO_DATA: actual MCP diagnostics incomplete or failed")
            for j,name in enumerate(names):
                col=len("#check @")+len(name)-len(name.rsplit(".",1)[-1])+1
                hr=call_tool(client,"lean_hover_info",{"file_path":rel,"line":3+j,"column":col})
                vr=call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":name,"scan_source":False})
                save(out/f"mcp-hover-{i}-{j}.json",hr)
                save(out/f"mcp-verify-{i}-{j}.json",vr)
                hover,verify=structured(hr),structured(vr)
                info=hover.get("info")
                if not isinstance(info,str) or name.rsplit(".",1)[-1] not in info or not isinstance(hover.get("diagnostics"),list) or any(x.get("severity") in ("error","warning") for x in hover["diagnostics"]):
                    raise ValueError("NO_DATA: actual MCP hover not bound to theorem")
                ax=verify.get("axioms")
                if not isinstance(ax,list) or not all(isinstance(x,str) for x in ax) or sorted(set(ax))!=dr[name]["axioms"] or verify.get("warnings")!=[]:
                    raise ValueError("HOLD: actual MCP axiom report differs")
                rows.append({"name":name,"hover_type_and_docs":info,"axioms":sorted(set(ax)),
                             "source_blob":p["blob"],"type_expr_sha256_from_direct":dr[name]["type_expr_sha256"],
                             "probe_source_sha256":sha(source.encode())})
    finally:
        client.close()
    if len(rows)!=len(selected):
        raise ValueError("NO_DATA: incomplete MCP inventory")
    receipt={"schema":"kuuos.prior-proof-real-lean-mcp.v0.4","source_head":d["source_head"],
             "source_tree":d["source_tree"],"catalog_digest":d["catalog_digest"],"plan_digest":d["plan_digest"],
             "direct_receipt_digest":digest(d),"mcp_version":EXPECTED_SERVER_VERSION,
             "mcp_version_output":ver,"server_info":init.get("result",{}).get("serverInfo"),
             "status":"REAL_LEAN_MCP_RECALL_GREEN","observations":sorted(rows,key=lambda x:x["name"]),
             "independent_runner_verified":False,"novelty_certified":False,"proof_authority":False}
    save(out/"mcp.json",receipt)
    print("KUUOS_KERNEL_REAL_MCP",json.dumps({"observed":len(rows),"status":receipt["status"]}),flush=True)

def independent(out,first):
    old=json.loads((first/"direct.json").read_text())
    new=json.loads((out/"direct.json").read_text())
    m=json.loads((first/"mcp.json").read_text())
    for k in ("source_head","source_tree","catalog_digest","plan_digest","pins","source_subtrees",
              "lakefile_blob","canonical_direct_options"):
        if old[k]!=new[k]: raise ValueError("independent source mismatch: "+k)
    if m["status"]!="REAL_LEAN_MCP_RECALL_GREEN" or m["direct_receipt_digest"]!=digest(old) or m["source_head"]!=old["source_head"]:
        raise ValueError("NO_DATA: first MCP receipt unbound")
    keys=("name","path","blob","line","lexical_id","type_expr_sha256","universe_parameters",
          "type_constants","proof_constants","axioms","original_source_sha256","scratch_source_sha256")
    if len(old["observations"])!=len(new["observations"]):
        raise ValueError("independent observation count mismatch")
    for x,y in zip(old["observations"],new["observations"]):
        for k in keys:
            if x[k]!=y[k]: raise ValueError("independent observation mismatch "+x["name"]+":"+k)
    if {x["name"] for x in m["observations"]}!={x["name"] for x in new["observations"]}:
        raise ValueError("independent MCP scope mismatch")
    receipt={"schema":"kuuos.prior-proof-independent-recall.v0.4",
             "status":"INDEPENDENT_SELECTED_OBSERVATIONS_AGREE","source_head":new["source_head"],
             "source_tree":new["source_tree"],"first_direct_digest":digest(old),
             "fresh_direct_digest":digest(new),"first_mcp_digest":digest(m),
             "selected_count":len(new["observations"]),"proof_authority":False,
             "novelty_certified":False,"full_transitive_proof_dependencies_verified":False}
    save(out/"independent.json",receipt)
    print("KUUOS_KERNEL_INDEPENDENT",json.dumps(receipt),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--phase",choices=("direct","mcp","independent"),required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args(); out=a.out.resolve()
    if not out.is_relative_to(ROOT/"artifacts"):
        raise ValueError("pilot outputs must stay in isolated artifacts")
    out.mkdir(parents=True,exist_ok=True)
    if a.phase=="direct": direct(ROOT,out)
    elif a.phase=="mcp": mcp(ROOT,out)
    else:
        if a.first is None: p.error("--first required")
        direct(ROOT,out)
        independent(out,a.first.resolve())
    return 0

if __name__=="__main__":
    raise SystemExit(main())
