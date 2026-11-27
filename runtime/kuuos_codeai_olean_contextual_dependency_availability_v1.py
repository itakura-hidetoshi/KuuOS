"""R57: bounded kernel dependency availability and contextual exclusion.
Only value edges in the certified R54 graph are expanded. Boundary presence
does not imply that boundary bodies or their descendants have been audited.
Policy denial is not actual missing data or mathematical refutation.
"""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_budget_selection_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
render=prev.render
DIRECT="9ddf74e241598beb5d11f4e503784369e867a04a218bd8a94fc9658bb0e87af9"
MCP="9ee5785fbbc7f21052d2a017030e03baa84e470eb5992c07194d661ced6f8901"
KEY="075f57dd9a50c64b187aac17801722fe03145bbf5de775053e986ee822f970c6"
MARK="KUUOS_R57_ENV "

def valid(budget,pref,comp,sel):
    return (budget.get("key")==KEY and base.portable.seal(budget)["key"]==KEY and
        prev.valid(pref,comp,sel) and budget["parent_preference_key"]==pref["key"] and
        budget["parent_comparison_key"]==comp["key"] and
        budget["retained_records"]==pref["retained_records"] and budget["retained_groups"]==pref["retained_groups"] and
        budget["proof_authority"] is False and budget["action_authority"] is False and budget["budget_is_refutation"] is False)

def admit(d,mp,ind,comp,sel,pref,budget):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R56_DIRECT_CONTEXTUAL_BUDGET_SELECTION" or mp["status"]!="R56_REAL_MCP_GREEN" or
        ind["status"]!="R56_INDEPENDENT_CONTEXTUAL_BUDGET_SELECTION_GREEN" or ind["direct_digest"]!=DIRECT or
        ind["mcp_digest"]!=MCP or not valid(budget,pref,comp,sel)):
        raise ValueError("HOLD_R56_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "budget_key":KEY,"parent_preference_key":prev.KEY,"request_count":12,"typed_dispatches":7,
        "budget_holds":3,"search_holds":2,"fallbacks":3,"retained_routes":5,"all_routes_retained":True,
        "raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "proof_authority":False,"action_authority":False,"budget_is_refutation":False,
        "new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","budget_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=85:
        raise ValueError("HOLD_R56_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=85 or len(hist)!=85 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R56_AUDIT")
    if len(budget["dispatches"])!=7 or any(hist[n]!=x["observation"] for n,x in budget["dispatches"].items()):
        raise ValueError("HOLD_R56_DISPATCH")
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
  let some ci := env.find? root | throwError "R57 root missing"
  let some proof := ci.value? (allowOpaque := true) | throwError "R57 proof missing"
  let mut pending : Array Name := #[]
  for dep in proof.getUsedConstants do
    if !pending.contains dep then pending := pending.push dep
  let mut rows : Array Json := #[]
  for i in [:__LIMIT__] do
    if i < pending.size then
      let n := pending[i]!
      let expand := known.contains n.toString
      match env.find? n with
      | none =>
        rows := rows.push (Json.mkObj [("name",toJson n.toString),("present",toJson false),
          ("expanded",toJson false),("value_constants",toJson (#[] : Array String))])
      | some info =>
        let refs : Array Name := if expand then
          match info.value? (allowOpaque := true) with
          | some e => e.getUsedConstants
          | none => #[]
        else #[]
        for dep in refs do
          if !pending.contains dep then pending := pending.push dep
        rows := rows.push (Json.mkObj [("name",toJson n.toString),("present",toJson true),
          ("expanded",toJson expand),("value_constants",toJson (refs.map Name.toString))])
  unless rows.size == pending.size do throwError "R57 dependency inventory exceeded"
  let payload := Json.mkObj [("route",toJson root.toString),
    ("direct_constants",toJson (proof.getUsedConstants.map Name.toString)),("rows",toJson rows)]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R57_ENV " ++ payload.compress)
'''.replace("__ROOT__",chr(96)*2+route).replace("__KNOWN__",", ".join(json.dumps(n,ensure_ascii=False) for n in known)).replace("__LIMIT__",str(limit)))
    return "\n".join(lines)

def project(comp,hist,frontier,observations):
    if set(observations)!=set(comp["records"]):raise ValueError("HOLD_ENV_INVENTORY")
    edges={n:set(x["proof_constants"]) for n,x in hist.items()}
    edges.update({n:set(x["value_constants"]) for n,x in frontier["observations"].items()
        if x["status"]=="OBSERVED" and n not in edges})
    out={}
    for route,record in sorted(comp["records"].items()):
        ob=observations[route]
        if ob["route"]!=route or sorted(set(ob["direct_constants"]))!=record["direct_constants"]:
            raise ValueError("HOLD_ENV_ROOT")
        rows={x["name"]:x for x in ob["rows"]}
        known=set(record["observed_dependencies"]);boundary=set(record["unobserved_boundary"])
        if len(rows)!=len(ob["rows"]) or set(rows)!=known|boundary or known&boundary:
            raise ValueError("HOLD_ENV_INVENTORY")
        for n,x in rows.items():
            if type(x["present"]) is not bool or type(x["expanded"]) is not bool:
                raise ValueError("HOLD_ENV_SHAPE")
            if x["present"] and n in known:
                if not x["expanded"] or set(x["value_constants"])!=edges[n]:
                    raise ValueError("HOLD_ENV_EDGE")
            elif x["expanded"] or x["value_constants"]:
                raise ValueError("HOLD_ENV_BOUNDARY")
        out[route]={"known":sorted(known),"boundary":sorted(boundary),
            "present":sorted(n for n,x in rows.items() if x["present"]),
            "missing":sorted(n for n,x in rows.items() if not x["present"]),
            "expanded":sorted(n for n,x in rows.items() if x["expanded"]),
            "boundary_body_audited":False}
    return out

def choose(budget,pref,comp,sel,availability,q):
    def hold(status):
        return {"status":status,"preferred":[],"proof_authority":False,"action_authority":False}
    if not valid(budget,pref,comp,sel):return hold("HOLD_PARENT_MEMORY")
    if set(q)!={"budget_key","case","denied"}:return hold("HOLD_REQUEST_SHAPE")
    if q["budget_key"]!=KEY:return hold("HOLD_PARENT_KEY")
    if not isinstance(q["case"],str) or q["case"] not in budget["decisions"]:return hold("HOLD_UNKNOWN_CONTEXT")
    denied=q["denied"]
    inventory={n for r in comp["records"].values() for n in r["observed_dependencies"]+r["unobserved_boundary"]}
    if not isinstance(denied,list) or not all(isinstance(n,str) for n in denied) or sorted(set(denied))!=denied:
        return hold("HOLD_DENIAL_SHAPE")
    if set(denied)-inventory:return hold("HOLD_UNKNOWN_DEPENDENCY")
    p=budget["decisions"][q["case"]];ns=p["all_routes"];eligible0=p["eligible"]
    if set(availability)!=set(comp["records"]):return hold("HOLD_ENV_INVENTORY")
    missing={n:availability[n]["missing"] for n in ns if availability[n]["missing"]}
    blocked={n:sorted(set(denied)&(set(availability[n]["known"])|set(availability[n]["boundary"]))) for n in ns}
    eligible=sorted(n for n in eligible0 if n not in missing and not blocked[n])
    result={"request":copy.deepcopy(q),"request_id":old.digest(q),"parent_request_id":p["request_id"],
        "context_id":p["context_id"],"parent_status":p["status"],"parent_polarity":p["parent_polarity"],
        "all_routes":list(ns),"budget_eligible":list(eligible0),"eligible":eligible,
        "missing_environment":missing,"policy_excluded":{n:xs for n,xs in blocked.items() if xs},
        "preferred":[],"parent_preferred":p["preferred"],"fallback":False,"raw_negative_retained":True,
        "policy_is_refutation":False,"proof_authority":False,"action_authority":False}
    if not eligible0:return {**result,"status":p["status"]}
    if not eligible:return {**result,"status":"HOLD_ENV_OR_POLICY"}
    b=p["request"]["base_request"]
    parent=[x for x in pref["decisions"] if x["request"]==b]
    if len(parent)!=1:raise ValueError("R57 preference lineage")
    scores=parent[0]["scores"];best=min(scores[n] for n in eligible)
    winners=sorted(n for n in eligible if scores[n]==best)
    return {**result,"status":"PREFERRED_AVAILABLE_ROUTE","preferred":winners,
        "fallback":not bool(set(winners)&set(p["preferred"]))}

def plan(budget,pref,comp,sel,availability):
    records=comp["records"];a="KuuOSR53Selected.shadowGlobal_1";b="KuuOSR53Selected.shadowGlobal_9"
    neg="KuuOSR53Selected.rawNoGlobal_12"
    def deps(n):return set(records[n]["observed_dependencies"]+records[n]["unobserved_boundary"])
    only_a=sorted(deps(a)-deps(b));only_b=sorted(deps(b)-deps(a));shared=sorted(deps(a)&deps(b))
    if not only_a or not only_b or not shared or any(x["missing"] for x in availability.values()):
        raise ValueError("HOLD_R57_AVAILABILITY_OR_DISTINCTION")
    cases=(("global_default","global_default",[],b),("deny_preferred","global_default",[only_b[0]],a),
        ("deny_alternative","global_default",[only_a[0]],b),("deny_shared","global_default",[shared[0]],"HOLD_ENV_OR_POLICY"),
        ("deny_after_budget","global_boundary",[only_a[0]],"HOLD_ENV_OR_POLICY"),
        ("budget_unchanged","global_joint",[],"HOLD_ROUTE_BUDGET"),
        ("negative_default","negative_allowed",[],neg),
        ("negative_denied","negative_allowed",[sorted(deps(neg))[0]],"HOLD_ENV_OR_POLICY"),
        ("raw_search","raw_global",[],"HOLD_NO_RULE_ROUTE"))
    ds={};selected={}
    for label,case,denied,expected in cases:
        q={"budget_key":KEY,"case":case,"denied":denied}
        x=choose(budget,pref,comp,sel,availability,q);ds[label]=x
        if expected.startswith("HOLD_"):
            if x["status"]!=expected or x["preferred"]:raise ValueError("R57 hold "+label)
        else:
            if x["status"]!="PREFERRED_AVAILABLE_ROUTE" or x["preferred"]!=[expected]:raise ValueError("R57 route "+label)
            goal=budget["decisions"][case]["request"]["base_request"]["goal"]
            selected["KuuOSR57Availability."+label]={"route":expected,"goal":goal,
                "goal_expr":sel["observations"][goal]["goal_expr"],"request_id":x["request_id"]}
    if len(selected)!=4 or sum(x["fallback"] for x in ds.values())!=1:raise ValueError("R57 coverage")
    return ds,selected

def controls(budget,pref,comp,sel,availability,hist,frontier,obs):
    out={}
    q={"budget_key":KEY,"case":"global_default","denied":[]}
    for label,bad,status in (
        ("wrong_key",{**q,"budget_key":"0"*64},"HOLD_PARENT_KEY"),
        ("wrong_case",{**q,"case":"unknown"},"HOLD_UNKNOWN_CONTEXT"),
        ("unknown_dep",{**q,"denied":["KuuOSR57.Fabricated"]},"HOLD_UNKNOWN_DEPENDENCY"),
        ("bad_shape",{**q,"denied":"not a list"},"HOLD_DENIAL_SHAPE"),
        ("extra_route",{**q,"route":"unknown"},"HOLD_REQUEST_SHAPE")):
        x=choose(budget,pref,comp,sel,availability,bad)
        if x["status"]!=status or x["preferred"] or x["proof_authority"] or x["action_authority"]:raise ValueError(label)
        out[label]=status
    bad=copy.deepcopy(budget);bad["decisions"].pop("global_default")
    if choose(base.portable.seal(bad),pref,comp,sel,availability,q)["status"]!="HOLD_PARENT_MEMORY":raise ValueError("memory drift")
    out["resealed_memory"]="HOLD_PARENT_MEMORY"
    # Simulated missing environment is explicitly a test, not observed absence.
    bad=copy.deepcopy(availability);n="KuuOSR53Selected.shadowGlobal_9";dep=bad[n]["present"].pop()
    bad[n]["missing"]=[dep]
    x=choose(budget,pref,comp,sel,bad,q)
    if x["preferred"]!=["KuuOSR53Selected.shadowGlobal_1"] or not x["fallback"]:raise ValueError("missing simulation")
    out["simulated_missing"]="FALLBACK_ONLY_TEST"
    bad=copy.deepcopy(obs);route=next(iter(sorted(bad)));bad[route]["rows"].pop()
    try:project(comp,hist,frontier,bad)
    except ValueError as e:
        if str(e)!="HOLD_ENV_INVENTORY":raise
        out["missing_row"]=str(e)
    else:raise ValueError("missing row accepted")
    bad=copy.deepcopy(obs);row=next(x for x in bad[route]["rows"] if x["expanded"])
    row["value_constants"].append("KuuOSR57.Fabricated")
    try:project(comp,hist,frontier,bad)
    except ValueError as e:
        if str(e)!="HOLD_ENV_EDGE":raise
        out["fabricated_edge"]=str(e)
    else:raise ValueError("fabricated edge accepted")
    return out
