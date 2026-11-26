#!/usr/bin/env python3
"""R9: selected closed WORLD alignment targets, from R7 -> R8 -> Lean/MCP.

Reuse the independently admitted R8 strict-descent type, materialize two
additional original theorem types, and verify exact applications in the
pinned elaborator. Missing premises and wrong targets remain HOLD.
No existing proof files, assumptions, public roots or provider change.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import gzip
import json
from pathlib import Path
import sqlite3
import tomllib

import check_codeai_olean_exact_materialization_v1_r8 as r8
import check_codeai_no_go_memory_v1 as prior
from check_codeai_no_go_memory_v1_r2 import normalize
from runtime import kuuos_codeai_olean_typed_route_preflight_v1 as gate
v=r8.v
r5=r8.r5
ROOT=v.ROOT
MODULE=gate.MODULE
NS=gate.NS
R8_RUN=45777202786
R8_HEAD="f639cb3bdf207ee4e5f5c6a17a16dac9e53b1784"
R8_DIRECT="08acb4b9a67329f6433daeb655691a9850b9c4f2ea0acaad739185864ff8e109"
R8_ARTIFACTS=(
 (15096303339,"codeai-olean-r8-local-45777202786-1","sha256:e8bbc41f28e3185a9679c4ffdaa75cf5c451d0838f5084608f32f73d1b2f3fde"),
 (15096533419,"codeai-olean-r8-independent-45777202786-1","sha256:01d66a0201bd627f1a0f9e098acbdf0706163f102fbe226deb79701078532657"),
)
SOURCE_BLOB="fb17427b367eb8f083a50479c28e13e1f8aa615c"
MARK="KUUOS_R9_TARGET "
CONTROL="KUUOS_R9_TYPED_CONTROL "
SOURCE=MODULE+".strict_descent_is_not_reflexive"

def historical_r8(local,independent,head):
    run=v.cache.api("actions/runs/"+str(R8_RUN))
    jobs=v.cache.api("actions/runs/"+str(R8_RUN)+"/jobs?per_page=100")
    v.need(run["head_sha"]==R8_HEAD and run["status"]=="completed" and run["conclusion"]=="success"
           and run["run_attempt"]==1 and jobs["total_count"]==2
           and {j["id"] for j in jobs["jobs"]}=={139763630320,139764345204}
           and all(j["status"]=="completed" and j["conclusion"]=="success"
                   and any(s["name"]=="Materialize exact selected theorem types and adversarial preflight controls"
                           and s["status"]=="completed" and s["conclusion"]=="success" for s in j["steps"])
                   for j in jobs["jobs"]),"R8 independent run evidence unavailable")
    for aid,name,dig in R8_ARTIFACTS:
        a=v.cache.api("actions/artifacts/"+str(aid))
        v.need(a["id"]==aid and a["name"]==name and a["digest"]==dig and not a["expired"]
               and a["workflow_run"]["id"]==R8_RUN and a["workflow_run"]["head_sha"]==R8_HEAD,
               "R8 artifact mismatch")
    first,second=r5.load(local/"direct.json"),r5.load(independent/"direct.json")
    replay=r5.load(independent/"independent.json")
    v.need(first==second and v.digest(first)==R8_DIRECT and first["source_head"]==head
           and first["scope_digest"]==v.SCOPE and first["r7_receipt_digest"]==r8.R7_RECEIPT
           and replay["status"]=="INDEPENDENT_OLEAN_R8_GREEN" and replay["direct_digest"]==R8_DIRECT,
           "R8 direct receipt changed")
    a,b=local/"exact-03",independent/"exact-03"
    x,y=r5.load(a/"receipt.json"),r5.load(b/"receipt.json")
    req=r5.load(a/"request.json")
    v.need(x==y and req==r5.load(b/"request.json") and x["name"]==SOURCE
           and x["request_digest"]==req["request_digest"] and x["module"]==MODULE
           and {k:z for k,z in x.items() if k!="row"} in first["selections"],
           "R8 strict descent materialization mismatch")
    with gzip.open(a/"kernel-types.jsonl.gz","rt",encoding="utf-8") as f:
        raw=json.loads(f.readline())
        v.need(not f.read().strip(),"extra R8 raw rows")
    v.need(raw["name"]==SOURCE and v.sha(raw["type_expr_repr"].encode())==x["type_expr_sha256"],
           "R8 complete type digest mismatch")
    return x,req

def declarations():
    return (
        "import "+MODULE+"\n\nnamespace "+NS+"\nopen "+MODULE+"\n"
        "set_option autoImplicit false\n\n"
        "def reflexive_target : Prop := (7 : Nat) < 7\n"
        "theorem reflexive_witness : ¬ reflexive_target := strict_descent_is_not_reflexive 7\n\n"
        "def forward_target : Prop := (3 : Nat) < 7\n"
        "def forwardStep : AlignmentStep := ⟨7, 3⟩\n"
        "theorem forward_valid : forwardStep.Valid := ⟨by decide⟩\n"
        "theorem forward_witness : forward_target := valid_step_strictly_decreases forwardStep forward_valid\n\n"
        "def reverse_target : Prop := (7 : Nat) < 3\n"
        "theorem reverse_witness : ¬ reverse_target :=\n"
        "  opposite_strict_steps_are_impossible (first := 7) (second := 3) forward_witness\n\n"
        "end "+NS+"\n"
    )

def render():
    lines=[declarations(),"open Lean",""]
    q=chr(96)*2
    for key,case in gate.CASES.items():
        t=NS+"."+key+"_target";w=NS+"."+key+"_witness"
        expect=("mkApp (mkConst "+q+"Not) (mkConst "+q+t+")"
                if case["polarity"]=="negative" else "mkConst "+q+t)
        lines += ["run_cmd do","  let env ← getEnv",
                  "  let some t := env.find? "+q+t+' | throwError "missing target"',
                  "  let some w := env.find? "+q+w+' | throwError "missing witness"',
                  '  let some body := t.value? (allowOpaque := true) | throwError "missing target body"',
                  "  let expected := "+expect,
                  '  unless w.isTheorem && w.type.equal expected do throwError "exact target type mismatch"',
                  '  if body.hasMVar || body.hasFVar || body.hasLooseBVars then throwError "open target"',
                  "  let payload := Lean.Json.mkObj [",
                  '    ("target_id", Lean.toJson "'+key+'"),',
                  '    ("target_name", Lean.toJson "'+t+'"),',
                  '    ("witness_name", Lean.toJson "'+w+'"),',
                  '    ("polarity", Lean.toJson "'+case["polarity"]+'"),',
                  '    ("target_expr_repr", Lean.toJson (reprStr body)),',
                  '    ("witness_type_repr", Lean.toJson (reprStr w.type)),',
                  '    ("exact_kernel_type_match", Lean.toJson true)]',
                  '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    # Inspect the actual partially applied original theorem in Lean, not a
    # compiler error. No premise -> a function, not a proof of the target.
    lines += ["run_cmd do",
              "  let (missingMatches, wrongMatches) ← Lean.Elab.Command.liftTermElabM do",
              "    let partialProof := mkApp2 (mkConst "+q+MODULE+".opposite_strict_steps_are_impossible) (mkNatLit 7) (mkNatLit 3)",
              "    let wrongProof := mkApp (mkConst "+q+SOURCE+") (mkNatLit 7)",
              "    let missingTy ← Lean.Meta.inferType partialProof",
              "    let wrongTy ← Lean.Meta.inferType wrongProof",
              "    let reverseNeg := mkApp (mkConst "+q+"Not) (mkConst "+q+NS+".reverse_target)",
              "    let forwardNeg := mkApp (mkConst "+q+"Not) (mkConst "+q+NS+".forward_target)",
              "    let a ← Lean.Meta.isDefEq missingTy reverseNeg",
              "    let b ← Lean.Meta.isDefEq wrongTy forwardNeg",
              "    pure (a, b)",
              '  if missingMatches || wrongMatches then throwError "unsafe applicability match"',
              '  let payload := Lean.Json.mkObj [("missing_premise_defeq", Lean.toJson missingMatches),',
              '    ("wrong_target_defeq", Lean.toJson wrongMatches)]',
              '  Lean.Elab.Command.liftIO <| IO.println ("'+CONTROL+'" ++ payload.compress)',""]
    return "\n".join(lines)+"\n"+v.suffix(gate.AUDIT_NAMES)

def coverage_audit(db,cat,out):
    # This source-only graph is explicitly NOT Lake's actual build graph.
    # It helps triage the 695 absent artifacts without assuming they failed.
    config=tomllib.loads((ROOT/"lakefile.toml").read_text(encoding="utf-8"))
    lib=next(x for x in config["lean_lib"] if x["name"]=="KuuOSFormal")
    roots=sorted(lib["roots"]);srcdir=lib["srcDir"]
    by_module={}
    for f in cat["files"]:
        if f["path"].startswith(srcdir+"/"):
            by_module.setdefault(f["module_path_lexical"],[]).append(f)
    reachable=set();todo=list(roots)
    while todo:
        m=todo.pop()
        if m in reachable:continue
        fs=by_module.get(m,[])
        if len(fs)!=1:continue
        reachable.add(m);todo.extend(fs[0]["imports"])
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        gaps=[json.loads(x[0]) for x in con.execute(
            "SELECT row_json FROM modules WHERE state='HOLD_MISSING_OLEAN' ORDER BY module")]
    finally:con.close()
    v.need(len(gaps)==695,"missing module inventory changed")
    rows=[]
    for x in gaps:
        m=x["module"]
        outside=all(not f["path"].startswith(srcdir+"/") for f in x["sources"])
        state=("OUTSIDE_DECLARED_SRCDIR" if outside else
               "LEXICALLY_REACHABLE_FROM_DECLARED_ROOT" if m in reachable else
               "NOT_REACHED_BY_LEXICAL_ROOT_WALK")
        rows.append({"module":m,"sources":x["sources"],"classification":state,
                     "actual_missing_reason":"NO_DATA","status":"HOLD_MISSING_OLEAN"})
    result={"source_module_count":len(cat["files"]),"missing_count":len(rows),
            "declared_source_directory":srcdir,"declared_root_count":len(roots),
            "lexical_reachable_module_count":len(reachable),
            "counts":dict(sorted(Counter(x["classification"] for x in rows).items())),
            "rows":rows,"actual_lake_build_graph_verified":False,
            "missing_artifact_cause_certified":False,"proof_authority":False}
    v.save(out/"missing-olean-coverage.json",result)
    return result

def direct(head,index,local,independent,out):
    receipt,db=r8.admit(index,head)
    obs,cat,inv=v.snapshot(head)
    sources=r5.r2.module_sources(cat)
    v.need(sources[MODULE]==[{"path":"formal/"+MODULE.replace(".","/")+".lean","blob":SOURCE_BLOB}],
           "original alignment source changed")
    archived,archived_req=historical_r8(local,independent,head)
    plan=r8.prepare(db,receipt,r8.R7_RECEIPT,head,gate.SOURCE_NAMES,
                    "Exact closed strict descent applicability review",
                    [{"module":MODULE,"name":n} for n in gate.SOURCE_NAMES])
    v.need(plan["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and len(plan["requests"])==3
           and len(plan["search"]["unobserved_modules"])==695 and plan["search"]["omitted_matches"]==0,
           "R7 preflight did not retain all search context")
    v.save(out/"search-plan.json",plan)
    env=r5.fixed_lean();materials=[]
    for i,req in enumerate(plan["requests"]):
        n=req["name"]
        if n==SOURCE:
            bound,hold=r5.bind_files(MODULE,ROOT/".lake/build/lib/lean"/(MODULE.replace(".","/")+".olean"),sources[MODULE][0])
            v.need(req==archived_req and hold is None and bound==req["binding"]
                   and v.digest(bound)==archived["artifact_binding_digest"],"R8 reused binding changed")
            result=archived
            reuse=True
        else:
            result=r8.materialize(out/f"exact-{i:02}",req,sources,env);reuse=False
        materials.append({"name":n,"module":MODULE,"type_expr_sha256":result["type_expr_sha256"],
                          "request_digest":req["request_digest"],
                          "artifact_binding_digest":result["artifact_binding_digest"],
                          "reused_r8":reuse})
    v.need(sum(x["reused_r8"] for x in materials)==1,"R8 reuse inventory")
    source=render();rc,log=prior.compile_source(out/"Probe.lean",source)
    if rc:
        print(log[-16000:],flush=True)
        raise ValueError("direct typed applicability failed")
    selected=[{"name":n,"expected_direct_refs":[]} for n in gate.SOURCE_NAMES]
    selected.append({"name":NS+".forward_valid","expected_direct_refs":[]})
    selected.extend({"name":NS+"."+k+"_witness","expected_direct_refs":[c["source"]]+c["premises"]}
                    for k,c in gate.CASES.items())
    rows=v.read_direct(log,selected);by_name={x["name"]:x for x in rows}
    v.need(all(by_name[x["name"]]["type_expr_sha256"]==x["type_expr_sha256"] for x in materials),
           "imported source type differs from exact raw olean type")
    apps=[json.loads(s[len(MARK):]) for s in log.splitlines() if s.startswith(MARK)]
    controls=[json.loads(s[len(CONTROL):]) for s in log.splitlines() if s.startswith(CONTROL)]
    v.need(len(apps)==3 and {x["target_id"] for x in apps}==set(gate.CASES)
           and controls==[{"missing_premise_defeq":False,"wrong_target_defeq":False}],
           "typed application controls incomplete")
    v.need(v.github_observation(head,"canonical_main")==obs,"source changed")
    cov=coverage_audit(db,cat,out)
    result={"status":"DIRECT_EXACT_TYPED_APPLICATIONS","source_head":head,"source_tree":obs["source_tree"],
            "scope_digest":v.SCOPE,"r7_receipt_digest":r8.R7_RECEIPT,"r8_direct_digest":R8_DIRECT,
            "preflight_digest":plan["preflight_digest"],"unobserved_module_count":695,
            "materialized_sources":materials,"probe_sha256":v.sha(source.encode()),"observations":rows,
            "applications":{x["target_id"]:x for x in apps},"source_controls":controls[0],
            "missing_coverage_digest":v.digest(cov),"proof_authority":False,"provider_calls":0}
    v.save(out/"direct.json",result)
    print("KUUOS_OLEAN_R9_DIRECT",json.dumps({"direct_digest":v.digest(result),
          "typed_applications":3,"audited_declarations":len(rows),"reused_r8":1,"new_materializations":2,
          "axioms":sorted({a for row in rows for a in row["axioms"]}),"missing_coverage_counts":cov["counts"],
          "source_controls":controls[0]},sort_keys=True),flush=True)
    return result

def mcp(head,out):
    d=r5.load(out/"direct.json")
    v.need(d["source_head"]==head and d["scope_digest"]==v.SCOPE
           and (out/"Probe.lean").read_text(encoding="utf-8")==render()
           and v.sha(render().encode())==d["probe_sha256"],"direct proof source unbound")
    source=declarations()+"\nset_option pp.universes false\n"+"\n".join("#check @"+x for x in gate.AUDIT_NAMES)+"\n"
    path=out/"McpProbe.lean";path.write_text(source,encoding="utf-8")
    cmd=["uvx","--from","lean-lsp-mcp=="+v.EXPECTED_SERVER_VERSION,"lean-lsp-mcp","--transport","stdio"]
    version=v.server_version(cmd[:-2],ROOT)
    client=v.MCPClient(cmd,cwd=ROOT,env={"LEAN_PROJECT_PATH":str(ROOT),"LEAN_LOG_LEVEL":"NONE",
             "LEAN_MCP_DISABLED_TOOLS":v.DISABLED_DURING_PROBE,"LEAN_MCP_SCRATCH_SLOTS":"1"},timeout_seconds=240)
    observations=[]
    try:
        client.request("initialize",{"protocolVersion":v.PROTOCOL_VERSION,"capabilities":{},
                       "clientInfo":{"name":"KuuOS olean typed applicability","version":"1"}})
        client.notify("notifications/initialized")
        v.need({"lean_diagnostic_messages","lean_verify"}<=set(v.tool_map(client.request("tools/list"))),
               "actual Lean MCP tools missing")
        rel=str(path.relative_to(ROOT))
        raw=v.call_tool(client,"lean_diagnostic_messages",{"file_path":rel,"timeout_s":180})
        v.save(out/"mcp-diagnostics.json",raw);diag=v.structured(raw)
        v.need(raw["result"]["isError"] is False and diag["success"] is True and diag["partial"] is False
               and diag["timed_out"] is False and diag["failed_dependencies"]==[]
               and not any(x.get("severity") in ("error","warning") for x in diag["items"]),
               "actual MCP diagnostics incomplete")
        for i,row in enumerate(d["observations"]):
            raw=v.call_tool(client,"lean_verify",{"file_path":rel,"theorem_name":row["name"],"scan_source":False})
            v.save(out/f"mcp-verify-{i}.json",raw);val=v.structured(raw)
            ax=normalize(val["axioms"])
            v.need(raw["result"]["isError"] is False and val["warnings"]==[] and ax==row["axioms"],
                   "MCP axiom mismatch:"+row["name"])
            observations.append({"name":row["name"],"axioms":ax,"raw_axioms":val["axioms"]})
    finally:client.close()
    result={"status":"REAL_LEAN_MCP_R9_GREEN","direct_digest":v.digest(d),
            "observations":observations,"mcp_version":v.EXPECTED_SERVER_VERSION,
            "version_output":version,"mcp_probe_sha256":v.sha(source.encode()),"raw_responses_preserved":True}
    v.save(out/"mcp.json",result)
    print("KUUOS_OLEAN_R9_REAL_MCP",json.dumps({"mcp_digest":v.digest(result),"audited":len(observations)},sort_keys=True),flush=True)

def independent(d,first,out):
    a=r5.load(first/"direct.json");mp=r5.load(first/"mcp.json")
    v.need(a==d,"independent direct evidence differs")
    diag=v.structured(r5.load(first/"mcp-diagnostics.json"))
    v.need(diag["success"] is True and diag["partial"] is False and diag["timed_out"] is False
           and diag["failed_dependencies"]==[] and not any(x.get("severity") in ("warning","error") for x in diag["items"]),
           "first MCP diagnostic invalid")
    for i,row in enumerate(a["observations"]):
        raw=r5.load(first/f"mcp-verify-{i}.json");val=v.structured(raw)
        v.need(raw["result"]["isError"] is False and val["warnings"]==[]
               and normalize(val["axioms"])==row["axioms"]==mp["observations"][i]["axioms"]
               and mp["observations"][i]["name"]==row["name"],"first actual MCP response mismatch")
    context=gate.project(a,d,mp)
    v.need(context["status"]=="INDEPENDENT_EXACT_TYPED_ROUTES_OBSERVED","typed route projection failed")
    context_digest=v.digest(context)
    routes={k:gate.pre_provider(context,context_digest,gate.make_request(context,k)) for k in gate.CASES}
    v.need({k:x["status"] for k,x in routes.items()}==
           {"reflexive":"REFUTED_EXACT_TARGET","forward":"REUSE_EXISTING","reverse":"REFUTED_EXACT_TARGET"},
           "exact route regression")
    req=gate.make_request(context,"reverse")
    controls={
        "missing_premise":gate.pre_provider(context,context_digest,dict(req,premise_witnesses=[])),
        "wrong_target":gate.pre_provider(context,context_digest,dict(req,target=gate.CASES["forward"]["target"])),
        "changed_expr":gate.pre_provider(context,context_digest,dict(req,target_expr_digest="0"*64)),
        "unknown_target":gate.pre_provider(context,context_digest,dict(req,target_id="unreviewed")),
        "changed_scope":gate.pre_provider(context,context_digest,dict(req,scope_digest="0"*64)),
        "wrong_receipt":gate.pre_provider(context,"0"*64,req),
        "missing_mcp":gate.project(a,d,{}),
        "changed_independent":gate.project(a,dict(d,provider_calls=1),mp)}
    v.need(all(x["status"]=="HOLD_TYPED_APPLICABILITY_REVIEW" and not x["candidate_generation_allowed"]
               for x in controls.values()),"unknown or unsupported target promoted")
    v.need(not any(x["candidate_generation_allowed"] for x in routes.values()),"unexpected provider permission")
    v.save(out/"routes.json",context);v.save(out/"route-controls.json",controls)
    result={"status":"INDEPENDENT_OLEAN_R9_GREEN","direct_digest":v.digest(d),"mcp_digest":v.digest(mp),
            "context_digest":context_digest,"routes":{k:x["status"] for k,x in routes.items()},
            "hold_controls":len(controls),"provider_calls":0,"proof_authority":False,
            "unobserved_module_count":695,"semantic_search_complete":False}
    v.save(out/"independent.json",result)
    print("KUUOS_OLEAN_R9_INDEPENDENT",json.dumps(result,sort_keys=True),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True);p.add_argument("--phase",required=True,choices=("direct","mcp","independent"))
    p.add_argument("--index",type=Path);p.add_argument("--r8-local",type=Path);p.add_argument("--r8-independent",type=Path)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    v.need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    if a.phase=="mcp":mcp(a.head,out);return
    out.mkdir(parents=True,exist_ok=False)
    d=direct(a.head,a.index,a.r8_local,a.r8_independent,out)
    if a.phase=="independent":independent(d,a.first,out)

if __name__=="__main__":
    main()
