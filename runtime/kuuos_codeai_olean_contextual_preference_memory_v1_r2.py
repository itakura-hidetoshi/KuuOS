"""R55: context-bound preference requests, never proof or action authority."""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_route_comparison_v1 as prev
old=prev.old
base=prev.base
DIRECT="ed70d580e2acfe1053f68261deaa65904d03ccd543efabdfee20096f35e7537b"
MCP="042d9c0d00e191d86fa4467b7877ac8c27d4ba7020d907d8cb1ebb35a71a96ad"
COMPARISON="dbb0cbfcc0672e4785544c297f5d1d03e3e96db639a95a8570dc983c50267d80"
GOALS=tuple(sorted(prev.COUNTS))
POLICIES=prev.POLICIES

def require_parent(d,mp,ind,comparison,selection):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R54_DIRECT_CONTEXTUAL_ROUTE_COMPARISON" or
        mp["status"]!="R54_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R54_INDEPENDENT_CONTEXTUAL_ROUTE_COMPARISON_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP):
        raise ValueError("HOLD_PARENT_RECEIPTS")
    if (comparison["key"]!=COMPARISON or base.portable.seal(comparison)["key"]!=COMPARISON or
        selection["key"]!=prev.SELECTION or base.portable.seal(selection)["key"]!=prev.SELECTION or
        comparison["parent_selection_key"]!=selection["key"]):
        raise ValueError("HOLD_PARENT_MEMORY")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
           "comparison_key":COMPARISON,"selection_key":prev.SELECTION,"replayed_routes":5,
           "route_counts":prev.COUNTS,"raw_positive_hold":True,"historical_hold_retained":True,
           "raw_negative_retained":True,"all_routes_retained":True,"proof_authority":False,
           "new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()):
        raise ValueError("HOLD_PARENT_SCOPE")
    if any(ind.get(k) is not True for k in ("parent_bytes_preserved","comparison_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=69:
        raise ValueError("HOLD_PARENT_INDEPENDENT")
    rows=d["fresh_application"]["observations"]
    if len(rows)!=69 or len(mp["audits"])!=69 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_PARENT_AUDIT")
    if set(comparison["records"])!=set(selection["routes"]) or set(comparison["groups"])!=set(GOALS):
        raise ValueError("HOLD_PARENT_INVENTORY")
    return {x["name"]:x for x in rows}

def request(selection,goal,policy):
    return {"goal":goal,"goal_expr":selection["observations"][goal]["goal_expr"],
            "source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
            "parent_key":COMPARISON,"selection_key":prev.SELECTION,"policy":policy}

def choose(comparison,selection,q):
    """A preference only. All ties and all nonselected routes survive."""
    def hold(reason):
        return {"status":reason,"preferred":[],"proof_authority":False,"action_authority":False}
    if (comparison.get("key")!=COMPARISON or base.portable.seal(comparison)["key"]!=COMPARISON or
        selection.get("key")!=prev.SELECTION or base.portable.seal(selection)["key"]!=prev.SELECTION):
        return hold("HOLD_PARENT_MEMORY")
    if q.get("goal") not in GOALS:
        return hold("HOLD_UNKNOWN_CONTEXT")
    if q.get("policy") not in POLICIES:
        return hold("HOLD_UNKNOWN_POLICY")
    expected=request(selection,q["goal"],q["policy"])
    if set(q)!=set(expected):
        return hold("HOLD_REQUEST_SHAPE")
    for k in ("source_head","source_tree","scope_digest"):
        if q[k]!=expected[k]:return hold("HOLD_SOURCE_SCOPE")
    for k in ("parent_key","selection_key"):
        if q[k]!=expected[k]:return hold("HOLD_PARENT_KEY")
    if q["goal_expr"]!=expected["goal_expr"]:
        return hold("HOLD_GOAL_TYPE")
    group=comparison["groups"][q["goal"]]
    names=group["routes"]
    result={"request":copy.deepcopy(q),"all_routes":list(names),"preferred":[],
            "unselected":list(names),"proof_authority":False,"action_authority":False,
            "context_id":old.digest({k:v for k,v in q.items() if k!="policy"}),
            "request_id":old.digest(q),"search_complete":False}
    if not names:
        return {**result,"status":"HOLD_NO_RULE_ROUTE","polarity":"unresolved_positive_search"}
    fields=POLICIES[q["policy"]]
    scores={n:[comparison["records"][n][k] for k in fields] for n in names}
    winners=sorted(n for n in names if scores[n]==min(scores.values()))
    recorded=group["preferences"][q["policy"]]
    if (recorded["criteria"]!=list(fields) or recorded["scores"]!=scores or recorded["preferred"]!=winners or
        recorded["proof_authority"] is not False):
        return hold("HOLD_PREFERENCE_DRIFT")
    return {**result,"status":"PREFERRED_CHECKED_ROUTE","polarity":"negative" if q["goal"]=="rawNoGlobal" else "positive",
            "preferred":winners,"unselected":sorted(set(names)-set(winners)),"criteria":list(fields),"scores":scores}

def controls(comparison,selection):
    q=request(selection,"shadowGlobal","compact")
    cases={
        "old_head":({**q,"source_head":"0"*40},"HOLD_SOURCE_SCOPE"),
        "wrong_scope":({**q,"scope_digest":"0"*64},"HOLD_SOURCE_SCOPE"),
        "wrong_key":({**q,"parent_key":"0"*64},"HOLD_PARENT_KEY"),
        "wrong_context":({**q,"goal":"rawGlobal"},"HOLD_GOAL_TYPE"),
        "wrong_type":({**q,"goal_expr":"wrong"},"HOLD_GOAL_TYPE"),
        "unknown_raw":({**q,"goal":"otherRaw"},"HOLD_UNKNOWN_CONTEXT"),
        "unknown_policy":({**q,"policy":"guess"},"HOLD_UNKNOWN_POLICY"),
        "unadmitted_route":({**q,"route":"unknown"},"HOLD_REQUEST_SHAPE")}
    out={}
    for k,(bad,status) in cases.items():
        x=choose(comparison,selection,bad)
        if x["status"]!=status or x["preferred"] or x["proof_authority"] or x["action_authority"]:
            raise ValueError("preference control "+k)
        out[k]=status
    bad=copy.deepcopy(comparison);bad["records"].pop(next(iter(bad["records"])))
    bad=base.portable.seal(bad)
    x=choose(bad,selection,q)
    if x["status"]!="HOLD_PARENT_MEMORY":raise ValueError("mutated memory accepted")
    out["resealed_memory"]="HOLD_PARENT_MEMORY"
    return out

def plan(comparison,selection):
    decisions=[choose(comparison,selection,request(selection,g,p)) for g in GOALS for p in sorted(POLICIES)]
    if len(decisions)!=15 or sum(x["status"]=="PREFERRED_CHECKED_ROUTE" for x in decisions)!=9:
        raise ValueError("HOLD_PREFERENCE_INVENTORY")
    if sum(x["polarity"]=="negative" for x in decisions)!=3 or sum(x["status"]=="HOLD_NO_RULE_ROUTE" for x in decisions)!=6:
        raise ValueError("HOLD_PREFERENCE_POLARITY")
    selected={}
    for x in decisions:
        for i,n in enumerate(x["preferred"]):
            q=x["request"];name="KuuOSR55Preference."+q["goal"]+"_"+q["policy"]+"_"+str(i)
            selected[name]={"route":n,"goal":q["goal"],"goal_expr":q["goal_expr"],"request_id":x["request_id"]}
    if len(selected)!=9 or len({x["route"] for x in selected.values()})!=4:
        raise ValueError("HOLD_PREFERENCE_COVERAGE")
    return decisions,selected

def render(source,selected):
    tick=chr(96)*2
    lines=[source,"","open Lean"]
    for name,x in sorted(selected.items()):
        lines+=["set_option Elab.async false in","run_cmd do","  let env55 ← getEnv",
            "  let some route55 := env55.find? "+tick+x["route"]+" | throwError \"missing admitted route\"",
            "  let some target55 := env55.find? "+tick+prev.prev.prev.NS+"."+x["goal"]+"Target | throwError \"missing exact target\"",
            "  let some goal55 := target55.value? (allowOpaque := true) | throwError \"missing target body\"",
            "  unless route55.isTheorem && route55.levelParams.isEmpty && route55.type.equal goal55 do",
            "    throwError \"R55 exact type mismatch\"",
            "  let name55 := Name.str (Name.mkSimple "+json.dumps(name.rsplit(".",1)[0])+") "+json.dumps(name.rsplit(".",1)[1]),
            "  Lean.Elab.Command.liftCoreM <| Lean.addDecl (.thmDecl {",
            "    name := name55, levelParams := [], type := goal55, value := mkConst "+tick+x["route"]+" })",
            "  let some info55 := (← getEnv).find? name55 | throwError \"missing generated preference\"",
            "  let some body55 := info55.value? (allowOpaque := true) | throwError \"missing generated proof\"",
            "  unless info55.isTheorem && info55.type.equal goal55 && body55.equal (mkConst "+tick+x["route"]+") do",
            "    throwError \"generated preference proof drift\"",
            ""]
    return "\n".join(lines)
