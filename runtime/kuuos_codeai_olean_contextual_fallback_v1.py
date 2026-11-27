"""R34: context-gated recall OR bounded indexed closed-source discovery.
R33's context memory is immutable. Only an aligned genuine memory miss may
enter discovery. Known context mismatch does not enter search. Exact
closed theorem comparison covers the current registry and the selected
index's relevant zero-binder positive/negative pool. Deferred candidates
and missing modules remain explicit. No search failure is a refutation."""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_memory_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
root=prev.root
portable=prev.portable
base=prev.base
ext=prev.ext
CURRENT=prev.CURRENT
CURRENT_TREE=prev.CURRENT_TREE
VIEW=prev.VIEW
DIRECT="48853e429089998fd609a6a53ff8288246cf2e3b47ed8f928a99be80971fb0da"
MCP="78b5833f1dd5d446ea4eaf0cab5689e59b39bffa15cca9d980f42dd0e33a6ec5"
KEY="2507a9afd1fd86ef46c9b8600e43886cc744cda640d7b651aaad7cbd9f9d6110"
LEC=prev.prev.LEC
MARK="KUUOS_R34_FALLBACK "

def requests(d):
    qs={k:root.make_request("r34_"+k,q["target"],q["context_args"],q["context_modules"])
        for k,q in sorted(d["requests"].items())}
    a=qs["new_original_compat"]["context_args"]
    c=prev.prev.c;ap=prev.prev.ap
    shadow=c(LEC+"northNativeF55TwoChartShadow")
    ctx=[a[0],a[1],a[3],a[3],a[4],ap("id",a[3]),shadow]
    t=ap(LEC+"HasGlobal",ctx[0],ctx[1],ctx[2],ctx[4],ctx[6])
    qs["new_shadow_global"]=root.make_request("r34_new_shadow_global",t,ctx,qs["new_original_compat"]["context_modules"])
    return qs

def inventory(q,memory,inv):
    root.validate(q)
    if q["target"]!=prev.prev.context_target(q):raise ValueError("unaligned fallback request")
    h=q["target"]["apply"][0]["const"]
    if h not in inv["selected"]:raise ValueError("unranked head")
    candidates={}
    for c in memory["registry"]["candidates"]:
        candidates[c["name"]]={"name":c["name"],"module":c["module"],
            "polarity":c["polarity"],"origin":"context_registry","type_sha256":c["type_sha256"]}
    if len(candidates)!=10:raise ValueError("registry inventory")
    deferred=[]
    for head,pol in ((h,"positive"),("Not","negative")):
        for p in inv["selected"][head]:
            n=p["name"];m=p["module"]
            if head=="Not" and h not in p["negative_head_matches"]:continue
            if p["binder_count"]!=0:
                deferred.append({"name":n,"module":m,"reason":"NONZERO_BINDER_DEFERRED"});continue
            if n in candidates:
                if candidates[n]["module"]!=m or candidates[n]["polarity"]!=pol:
                    raise ValueError("indexed candidate identity conflict")
                continue
            candidates[n]={"name":n,"module":m,"polarity":pol,"origin":"bounded_index","row_digest":p["row_digest"]}
    xs=sorted(candidates.values(),key=lambda c:(c["origin"]!="context_registry",c["module"],c["name"]))
    for x in xs:typed.name(x["name"]);typed.name(x["module"])
    return {"target_head":h,"candidates":xs,"deferred":sorted(deferred,key=lambda x:x["name"]),
            "selected_index_digest":old.digest(inv),"context_memory_key":memory["key"],
            "unobserved_module_count":len(inv["unobserved_modules"]),
            "semantic_search_complete":False,"proof_authority":False}

def render(k,q,memory,plan):
    # Same file re-observes context, original registry and query Expr.
    # The caller checks this observation against the pre-search gate.
    src=prev.render({k:q},memory)
    mods=sorted({x["module"] for x in plan["candidates"]})
    src="".join("import "+m+"\n" for m in mods if "import "+m+"\n" not in src)+src
    tick=chr(96)*2
    entries=", ".join("("+tick+typed.name(x["name"])+", "+json.dumps(x["module"])+", "+
                      ("true" if x["polarity"]=="negative" else "false")+")" for x in plan["candidates"])
    src+="\nopen Lean Meta\nrun_cmd do\n  let env ← getEnv\n"
    src+="  let some qi := env.find? "+tick+'KuuOSR28Probe.q0 | throwError "missing fallback target"\n'
    src+='  let some goal := qi.value? (allowOpaque := true) | throwError "missing fallback body"\n'
    src+="  let some ei := env.find? "+tick+'KuuOSR28Probe.e0 | throwError "missing fallback context target"\n'
    src+='  let some expected := ei.value? (allowOpaque := true) | throwError "missing fallback context body"\n'
    src+='  unless goal.equal expected do throwError "unaligned fallback context"\n'
    src+="  let candidates : Array (Name × String × Bool) := #["+entries+"]\n"
    src+=r'''
  let payload ← Lean.Elab.Command.liftTermElabM do
    let mut rows : Array Json := #[]
    for (n,m,neg) in candidates do
      let some info := env.find? n | throwError "missing indexed theorem"
      let some idx := env.getModuleIdxFor? n | throwError "missing indexed origin"
      unless info.isTheorem && env.allImportedModuleNames[idx]!.toString == m do
        throwError "indexed theorem origin drift"
      let status ← if !info.levelParams.isEmpty || info.type.hasMVar || info.type.hasFVar ||
                       info.type.hasLooseBVars || info.type.hasLevelMVar then
          pure "HOLD_OPEN_SOURCE"
        else do
          let target := if neg then mkApp (mkConst NOTCONST) goal else goal
          try
            withNewMCtxDepth do
              let same ← isDefEq info.type target
              pure (if same then (if info.type.equal target then "MATCH_EXACT" else "MATCH_DEFEQ") else "HOLD_NOT_DEFEQ")
          catch _ => pure "HOLD_COMPARISON_FAILURE"
      rows := rows.push (Json.mkObj [
        ("name", toJson n.toString), ("module", toJson m),
        ("polarity", toJson (if neg then "negative" else "positive")),
        ("status", toJson status), ("type_expr", toJson (reprStr info.type))])
    pure (Json.mkObj [("goal_expr", toJson (reprStr goal)), ("comparisons", toJson rows)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R34_FALLBACK " ++ payload.compress)
'''.replace("NOTCONST",tick+"Not")
    return src

def decide(plan,obs,expected_goal,live):
    if obs["goal_expr"]!=expected_goal:raise ValueError("fallback target drift")
    xs=obs["comparisons"];by={r["name"]:r for r in xs}
    candidates=plan["candidates"]
    if len(xs)!=len(by) or set(by)!={c["name"] for c in candidates}:raise ValueError("comparison inventory")
    matches=[];failures=[];deferred=[]
    for c in candidates:
        x=by[c["name"]]
        if (x["module"],x["polarity"])!=(c["module"],c["polarity"]):raise ValueError("comparison source drift")
        if c["origin"]=="context_registry":
            if x["type_expr"]!=live[c["name"]] or portable.hash_type(x["type_expr"])!=c["type_sha256"]:
                raise ValueError("live registry type drift")
        if x["status"] in ("MATCH_EXACT","MATCH_DEFEQ"):
            matches.append({**c,"type_expr":x["type_expr"],"match_status":x["status"]})
        elif x["status"]=="HOLD_COMPARISON_FAILURE":
            failures.append(c["name"])
        elif x["status"]=="HOLD_OPEN_SOURCE":
            deferred.append(c["name"])
        elif x["status"]!="HOLD_NOT_DEFEQ":raise ValueError("unknown comparison status")
    # A failed comparison is not evidence against its candidate. In this
    # bounded selection policy, hold on failure or conflicting polarity.
    if failures or len({x["polarity"] for x in matches})>1:status="HOLD_COMPARISON_OR_CONFLICT"
    elif matches:status="INDEXED_APPLICATION_REQUIRED"
    else:status="HOLD_RECURSIVE_SEARCH_REQUIRED"
    return {"status":status,"matches":matches,"comparison_count":len(xs)-len(deferred),
            "open_deferred":deferred,"failed_comparisons":failures,
            "semantic_search_complete":False,"proof_authority":False}
