"""R58: append one-hop type/value edges of the finite R57 inventory.

Type references are not silently merged into the historical R54 cost metric.
Operational eligibility is tightened using both newly observed edge sets.
No assertion of full transitive closure, proof independence or authority.
"""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_dependency_availability_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
render=prev.render
DIRECT="5958b743c8f42ec4496d287be2d66591235e236b3a1e6948020f617336763500"
MCP="86e3458d018e6b0218491a9f4f290f97a1daa8b4727790e5ec4d990b3f7d3285"
KEY="8b216cdda83b1e150d855ed72d826cfc427a4356524c19e22fe0ef9aeac007b3"
MARK="KUUOS_R58_EDGES "

def valid(av,budget,pref,comp,sel):
    return (av.get("key")==KEY and base.portable.seal(av)["key"]==KEY and
        prev.valid(budget,pref,comp,sel) and av["parent_budget_key"]==budget["key"] and
        av["parent_preference_key"]==pref["key"] and av["retained_records"]==pref["retained_records"] and
        av["retained_groups"]==pref["retained_groups"] and av["proof_authority"] is False and
        av["action_authority"] is False and av["boundary_body_audited"] is False)

def admit(d,mp,ind,comp,sel,pref,budget,av):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R57_DIRECT_CONTEXTUAL_DEPENDENCY_AVAILABILITY" or mp["status"]!="R57_REAL_MCP_GREEN" or
        ind["status"]!="R57_INDEPENDENT_CONTEXTUAL_DEPENDENCY_AVAILABILITY_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or not valid(av,budget,pref,comp,sel)):
        raise ValueError("HOLD_R57_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "availability_key":KEY,"parent_budget_key":prev.KEY,"request_count":9,"typed_dispatches":4,
        "policy_holds":3,"budget_holds":1,"search_holds":1,"fallbacks":1,"retained_routes":5,
        "distinct_present_names":145,"all_routes_retained":True,"raw_positive_hold":True,
        "raw_negative_retained":True,"historical_hold_retained":True,"proof_authority":False,
        "action_authority":False,"boundary_body_audited":False,"policy_is_refutation":False,
        "new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","availability_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=89:
        raise ValueError("HOLD_R57_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=89 or len(hist)!=89 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R57_AUDIT")
    if len(av["dispatches"])!=4 or any(hist[n]!=x["observation"] for n,x in av["dispatches"].items()):
        raise ValueError("HOLD_R57_DISPATCH")
    return hist

def observer(comp):
    lines=[]
    for route,row in sorted(comp["records"].items()):
        known=row["observed_dependencies"]
        limit=len(known)+len(row["unobserved_boundary"])
        lines.append(r'''open Lean
set_option maxHeartbeats 12000000 in
set_option Elab.async false in
run_cmd do
  let env ← getEnv
  let root : Name := __ROOT__
  let known : Array String := #[__KNOWN__]
  let some ci := env.find? root | throwError "R58 root missing"
  let some proof := ci.value? (allowOpaque := true) | throwError "R58 proof missing"
  let mut pending : Array Name := #[]
  for dep in proof.getUsedConstants do
    if !pending.contains dep then pending := pending.push dep
  let mut rows : Array Json := #[]
  for i in [:__LIMIT__] do
    if i < pending.size then
      let n := pending[i]!
      let some info := env.find? n | throwError "R58 parent dependency missing"
      let val := info.value? (allowOpaque := true)
      let refs : Array Name := match val with
        | some e => e.getUsedConstants
        | none => #[]
      let tys := info.type.getUsedConstants
      if known.contains n.toString then
        for dep in refs do
          if !pending.contains dep then pending := pending.push dep
      let kind : String := match info with
        | .axiomInfo _ => "axiom"
        | .defnInfo _ => "definition"
        | .thmInfo _ => "theorem"
        | .opaqueInfo _ => "opaque"
        | .quotInfo _ => "quotient"
        | .inductInfo _ => "inductive"
        | .ctorInfo _ => "constructor"
        | .recInfo _ => "recursor"
      let origin : String := match env.getModuleIdxFor? n with
        | some j => env.allImportedModuleNames[j]!.toString
        | none => "CURRENT_REPLAY"
      let missingVal := refs.filter fun k => (env.find? k).isNone
      let missingTy := tys.filter fun k => (env.find? k).isNone
      rows := rows.push (Json.mkObj [("name",toJson n.toString),
        ("kind",toJson kind),("origin",toJson origin),("has_value",toJson val.isSome),
        ("type_constants",toJson (tys.map Name.toString)),
        ("value_constants",toJson (refs.map Name.toString)),
        ("missing_type",toJson (missingTy.map Name.toString)),
        ("missing_value",toJson (missingVal.map Name.toString))])
  unless rows.size == pending.size do throwError "R58 inventory exceeded"
  let payload := Json.mkObj [("route",toJson root.toString),
    ("root_type_constants",toJson (ci.type.getUsedConstants.map Name.toString)),
    ("rows",toJson rows)]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R58_EDGES " ++ payload.compress)
'''.replace("__ROOT__",chr(96)*2+route).replace("__KNOWN__",", ".join(json.dumps(n,ensure_ascii=False) for n in known)).replace("__LIMIT__",str(limit)))
    return "\n".join(lines)

KINDS={"axiom","definition","theorem","opaque","quotient","inductive","constructor","recursor"}
VALUE_KINDS={"definition","theorem","opaque"}

def project(comp,hist,av,observations):
    if set(observations)!=set(comp["records"]):raise ValueError("HOLD_EDGE_INVENTORY")
    common={};routes={}
    for route,rec in sorted(comp["records"].items()):
        ob=observations[route];prior=av["availability"][route]
        if ob["route"]!=route or sorted(set(ob["root_type_constants"]))!=hist[route]["type_constants"]:
            raise ValueError("HOLD_ROOT_TYPE")
        rows={x["name"]:x for x in ob["rows"]}
        if len(rows)!=len(ob["rows"]) or set(rows)!=set(prior["present"]) or prior["missing"]:
            raise ValueError("HOLD_EDGE_INVENTORY")
        old_edges={x["name"]:x for x in av["environment_observations"][route]["rows"]}
        for n,x in rows.items():
            if (x["kind"] not in KINDS or not x["origin"] or type(x["has_value"]) is not bool or
                x["has_value"]!=(x["kind"] in VALUE_KINDS) or (not x["has_value"] and x["value_constants"])):
                raise ValueError("HOLD_EDGE_KIND")
            for k in ("type_constants","value_constants","missing_type","missing_value"):
                if not isinstance(x[k],list) or not all(isinstance(z,str) and z for z in x[k]):
                    raise ValueError("HOLD_EDGE_SHAPE")
            if not set(x["missing_type"])<=set(x["type_constants"]) or not set(x["missing_value"])<=set(x["value_constants"]):
                raise ValueError("HOLD_EDGE_MISSING")
            if n in prior["known"] and set(x["value_constants"])!=set(old_edges[n]["value_constants"]):
                raise ValueError("HOLD_PARENT_EDGE")
            y={**x,**{k:sorted(set(x[k])) for k in ("type_constants","value_constants","missing_type","missing_value")}}
            if n in common and common[n]!=y:raise ValueError("HOLD_SHARED_EDGE")
            common[n]=y
        before=set(rows)
        val={k for x in rows.values() for k in x["value_constants"]}
        typ=set(ob["root_type_constants"])|{k for x in rows.values() for k in x["type_constants"]}
        missing={k for x in rows.values() for t in ("missing_type","missing_value") for k in x[t]}
        routes[route]={"historical":sorted(before),"value_frontier":sorted(val-before),
            "type_frontier":sorted(typ-before),"observed_references":sorted(before|val|typ),
            "new_references":sorted((val|typ)-before),"missing_references":sorted(missing),
            "expanded_names":sorted(before),"complete_transitive_closure":False}
    if len(common)!=145:raise ValueError("HOLD_EDGE_UNION")
    return {"nodes":common,"routes":routes,"expanded_distinct_names":len(common),
        "distinct_next_names":len({n for r in routes.values() for n in r["new_references"]}),
        "complete_transitive_closure":False,"type_and_value_edges_separate":True,
        "full_body_serialized":False}

def plan(av,budget,pref,comp,sel,expanded):
    ds={};selected={}
    for label,prior in sorted(av["decisions"].items()):
        q=prior["request"];b=budget["decisions"][q["case"]];ns=prior["all_routes"]
        if b["request_id"]!=prior["parent_request_id"] or set(ns)!=set(b["all_routes"]):
            raise ValueError("HOLD_R58_LINEAGE")
        denied=set(q["denied"])
        blocked={n:sorted(denied&set(expanded["routes"][n]["observed_references"])) for n in ns}
        missing={n:expanded["routes"][n]["missing_references"] for n in ns if expanded["routes"][n]["missing_references"]}
        eligible=sorted(n for n in prior["eligible"] if not blocked[n] and n not in missing)
        if not set(eligible)<=set(prior["eligible"]):raise ValueError("HOLD_R58_RELAXATION")
        decision={"parent_decision":label,"parent_request_id":prior["request_id"],
            "request":copy.deepcopy(q),"all_routes":list(ns),"old_eligible":prior["eligible"],"eligible":eligible,
            "old_preferred":prior["preferred"],"preferred":[],"policy_excluded":{n:x for n,x in blocked.items() if x},
            "missing_references":missing,"newly_excluded":sorted(set(prior["eligible"])-set(eligible)),
            "parent_status":prior["status"],"parent_polarity":prior["parent_polarity"],
            "status":prior["status"],"proof_authority":False,"action_authority":False,"policy_is_refutation":False}
        if eligible:
            br=b["request"]["base_request"]
            parents=[x for x in pref["decisions"] if x["request"]==br]
            if len(parents)!=1:raise ValueError("HOLD_R58_PREF_LINEAGE")
            scores=parents[0]["scores"];best=min(scores[n] for n in eligible)
            wins=sorted(n for n in eligible if scores[n]==best)
            decision.update({"preferred":wins,"status":"PREFERRED_EXPANDED_ROUTE"})
            goal=br["goal"]
            for i,n in enumerate(wins):
                selected["KuuOSR58Expanded."+label+"_"+str(i)]={"route":n,"goal":goal,
                    "goal_expr":sel["observations"][goal]["goal_expr"],"request_id":old.digest(q)}
        elif prior["eligible"]:
            decision["status"]="HOLD_EXPANDED_DEPENDENCY"
        decision["choice_changed"]=decision["preferred"]!=prior["preferred"]
        ds[label]=decision
    if len(ds)!=9 or not selected or not all(ds[n]["preferred"] for n in ("global_default","negative_default")):
        raise ValueError("HOLD_R58_COVERAGE")
    return ds,selected

def controls(comp,hist,av,observations,expanded,ds):
    out={}
    for label,mut,status in (
        ("missing_row",lambda x,r:x[r]["rows"].pop(),"HOLD_EDGE_INVENTORY"),
        ("root_type_drift",lambda x,r:x[r]["root_type_constants"].append("KuuOSR58.Fabricated"),"HOLD_ROOT_TYPE"),
        ("kind_drift",lambda x,r:x[r]["rows"][0].update(kind="fabricated"),"HOLD_EDGE_KIND")):
        x=copy.deepcopy(observations);route=next(iter(sorted(x)));mut(x,route)
        try:project(comp,hist,av,x)
        except ValueError as e:
            if str(e)!=status:raise
            out[label]=status
        else:raise ValueError("invalid edge record accepted "+label)
    x=copy.deepcopy(observations);route=next(iter(sorted(x)))
    known=set(av["availability"][route]["known"])
    row=next(z for z in x[route]["rows"] if z["name"] in known and z["has_value"])
    row["value_constants"].append("KuuOSR58.Fabricated")
    try:project(comp,hist,av,x)
    except ValueError as e:
        if str(e)!="HOLD_PARENT_EDGE":raise
        out["parent_edge_drift"]=str(e)
    else:raise ValueError("parent edge drift accepted")
    if not all(set(x["eligible"])<=set(x["old_eligible"]) for x in ds.values()):
        raise ValueError("expanded eligibility relaxed")
    out["monotone_eligibility"]="NO_PREVIOUSLY_EXCLUDED_ROUTE_REINTRODUCED"
    if not all(set(x["historical"])<=set(x["observed_references"]) for x in expanded["routes"].values()):
        raise ValueError("historical edge inventory lost")
    out["historical_inventory"]="ALL_PREVIOUS_NAMES_RETAINED"
    return out
