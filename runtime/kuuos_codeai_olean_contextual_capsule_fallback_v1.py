"""R42: a genuine aligned capsule miss may enter bounded canonical discovery.
Use independently admitted R20 structural inventory, not R41's control
theorem name, to enumerate closed positive and negative theorem candidates.
Capsule hits and context mismatch never enter fallback; exact Expr equality
only. Capped/deferred/unobserved material is not mathematical refutation.
"""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_capsule_dispatch_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
DIRECT="1cff1334b6cddaec6acbc81de16124c8cd446b62575488d41855cd8f23fc59cd"
MCP="f51ab7a39ffe6fbfbd210c8a678e8305da5695ec294f78c4c289f70a1279cd37"
LAYER="93973fe533915e4e97852cd709141a7c0a81b270185ec7191562f746001d1028"
MARK="KUUOS_R42_SEARCH "
NS="KuuOSR42Replay"
def admit(d,mp,ind,index,mem,qs,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R41_DIRECT_CONTEXTUAL_CAPSULE_DISPATCH" or mp["status"]!="R41_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R41_INDEPENDENT_CONTEXTUAL_CAPSULE_DISPATCH_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        d["source_head"]!=base.CURRENT or d["source_tree"]!=base.CURRENT_TREE or d["scope_digest"]!=old.SCOPE or
        ind["source_head"]!=base.CURRENT or ind["source_tree"]!=base.CURRENT_TREE or ind["scope_digest"]!=old.SCOPE or
        index["key"]!=LAYER or base.portable.seal(index)["key"]!=LAYER or
        d["dispatch_layer_key"]!=LAYER or ind["dispatch_layer_key"]!=LAYER or
        mem["key"]!=prev.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        d["capsule_layer_key"]!=mem["key"] or ind["capsule_layer_key"]!=mem["key"] or
        d["capsule_manifest"]!=prev.prev.MANIFEST or ind["capsule_manifest"]!=prev.prev.MANIFEST or
        ind["dispatch_layer_bytes_equal"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["imported_certified_capsule"] is not True or ind["parent_bytes_preserved"] is not True or
        ind["mcp_audits"]!=16 or ind["capsule_rebuilds"]!=0 or ind["root_trials"]!=0 or
        ind["positive_witnesses"]!=3 or ind["negative_witnesses"]!=3 or
        d["requests"]!=qs or d["observations"]!=obs):
        raise ValueError("R41 admission")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=16 or len(ma)!=16 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R41 audit binding")
    decisions={k:prev.dispatch(index,index,q,obs[k],base.CURRENT) for k,q in sorted(qs.items())}
    if decisions!=d["decisions"] or {k:x["status"] for k,x in decisions.items()}!=ind["decisions"]:
        raise ValueError("R41 dispatch drift")
    return decisions

def plan(index,q,obs,decision,inv):
    if index["key"]!=LAYER or base.portable.seal(index)["key"]!=LAYER:
        raise ValueError("dispatch layer drift")
    if prev.dispatch(index,index,q,obs,base.CURRENT)!=decision:
        raise ValueError("unbound dispatch receipt")
    if decision["status"]!="HOLD_CAPSULE_MISS" or not obs["aligned"]:
        return {"status":"HOLD_FALLBACK_NOT_AUTHORIZED","candidates":[]}
    base.root.validate(q)
    if q["target"]!=base.cm.prev.context_target(q):
        raise ValueError("unaligned fallback target")
    h=q["target"]["apply"][0]["const"]
    if h not in inv["selected"] or h not in inv["capped"]:
        return {"status":"HOLD_UNINDEXED_HEAD","candidates":[]}
    # Explicit module scope is the request's imports plus the canonical
    # F55 source module on which the admitted composite capsule depends.
    allowed=set(q["context_modules"])|{prev.prev.prev.prev.MODULE}
    if any(not m.startswith("Kuu.") for m in allowed):
        raise ValueError("noncanonical source module")
    cs={};deferred=0
    for pool in ("selected","capped"):
        for key,pol in ((h,"positive"),("Not","negative")):
            for x in inv[pool][key]:
                if key=="Not" and h not in x["negative_head_matches"]:continue
                if x["module"] not in allowed or x["binder_count"]!=0:
                    deferred+=1;continue
                n=x["name"]
                typed.name(n);typed.name(x["module"])
                if n in cs:raise ValueError("duplicate indexed name")
                cs[n]={"name":n,"module":x["module"],"polarity":pol,"row_digest":x["row_digest"],"pool":pool}
    return {"status":"EXACT_CLOSED_COMPARISON_REQUIRED","goal_expr":obs["goal_expr"],
            "context_exprs":obs["context_exprs"],"head":h,"allowed_modules":sorted(allowed),
            "candidates":[cs[n] for n in sorted(cs)],"deferred":deferred,
            "inventory_digest":old.digest(inv),"unobserved_module_count":len(inv["unobserved_modules"]),
            "semantic_search_complete":False,"proof_authority":False}

def render(qs,k,p):
    if p["status"]!="EXACT_CLOSED_COMPARISON_REQUIRED" or k not in qs:
        raise ValueError("unauthorized search")
    tick=chr(96)*2
    # R41 observation is repeated in the same imported environment. Its
    # named canonical controls are only type checks, not search candidates.
    src=prev.observe(qs)
    src="".join("import "+m+"\n" for m in sorted({c["module"] for c in p["candidates"]})) + src
    src+="\nopen Lean\nrun_cmd do\n  let env ← getEnv\n"
    src+="  let some gi := env.find? "+tick+"KuuOSR41Observe."+k+'Goal | throwError "missing search goal"\n'
    src+="  let some ei := env.find? "+tick+"KuuOSR41Observe."+k+'Expected | throwError "missing expected context"\n'
    src+='  let some g := gi.value? (allowOpaque := true) | throwError "missing search body"\n'
    src+='  let some e := ei.value? (allowOpaque := true) | throwError "missing expected body"\n'
    src+='  unless g.equal e do throwError "search context mismatch"\n'
    entries=", ".join("("+tick+c["name"]+", "+json.dumps(c["module"])+", "+("true" if c["polarity"]=="negative" else "false")+")" for c in p["candidates"])
    src+="  let candidates : Array (Name × String × Bool) := #["+entries+"]\n"
    src+=r'''  let mut rows : Array Json := #[]
  for (n,m,neg) in candidates do
    let some info := env.find? n | throwError "missing indexed source"
    let some idx := env.getModuleIdxFor? n | throwError "missing indexed origin"
    unless info.isTheorem && env.allImportedModuleNames[idx]!.toString == m do
      throwError "indexed source origin drift"
    let target := if neg then mkApp (mkConst NOTCONST) g else g
    let closed := info.levelParams.isEmpty && !info.type.hasMVar && !info.type.hasFVar &&
      !info.type.hasLooseBVars && !info.type.hasLevelMVar
    let status := if !closed then "HOLD_OPEN_SOURCE" else if info.type.equal target then "MATCH_EXACT" else "HOLD_NOT_EXACT"
    rows := rows.push (Json.mkObj [("name",toJson n.toString),("module",toJson m),
      ("polarity",toJson (if neg then "negative" else "positive")),("status",toJson status),
      ("type_expr",toJson (reprStr info.type))])
  let payload := Json.mkObj [("goal_expr",toJson (reprStr g)),("comparisons",toJson rows)]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R42_SEARCH " ++ payload.compress)
'''.replace("NOTCONST",tick+"Not")
    return src

def decide(p,obs):
    if p["status"]!="EXACT_CLOSED_COMPARISON_REQUIRED" or p["goal_expr"]!=obs["goal_expr"]:
        raise ValueError("search scope drift")
    rows=obs["comparisons"];by={x["name"]:x for x in rows}
    if len(rows)!=len(by) or set(by)!={x["name"] for x in p["candidates"]}:
        raise ValueError("comparison inventory")
    matches=[];opened=[]
    for c in p["candidates"]:
        x=by[c["name"]]
        if (x["module"],x["polarity"])!=(c["module"],c["polarity"]):
            raise ValueError("source drift")
        if x["status"]=="MATCH_EXACT":
            matches.append({**c,"type_expr":x["type_expr"]})
        elif x["status"]=="HOLD_OPEN_SOURCE":opened.append(c["name"])
        elif x["status"]!="HOLD_NOT_EXACT":raise ValueError("comparison status")
    status="HOLD_CONFLICT" if len({x["polarity"] for x in matches})>1 else "INDEXED_APPLICATION_REQUIRED" if matches else "HOLD_INDEX_MISS"
    return {"status":status,"matches":matches if status=="INDEXED_APPLICATION_REQUIRED" else [],
            "conflicting_matches":matches if status=="HOLD_CONFLICT" else [],"open_deferred":opened,
            "comparison_count":len(rows),"semantic_search_complete":False,"proof_authority":False}
