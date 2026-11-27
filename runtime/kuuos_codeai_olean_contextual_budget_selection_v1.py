"""R56: operational budget filter on certified preference memory."""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_preference_memory_v1_r2 as prev
base=prev.base
old=prev.old
comparison_gate=prev.prev
DIRECT="d0a95ca28ad4ca0940b2a180013b824a0b3d6bbd38c1522cc672fc7ec1c55f3c"
MCP="911b15bde9a535395306b37d2ec020c234fd98b75e9ef3a50e205590f0cbd14b"
KEY="08c4af69caa177d939e611a7aca14c61308ecd4c9c9a3f6207ad7498df5b5492"
METRICS=("proof_nodes","boundary_count","observed_dependency_count","historical_probes")
render=prev.render

def valid(mem,comp,sel):
    return (all(x.get("key")==k and base.portable.seal(x)["key"]==k for x,k in
                ((mem,KEY),(comp,prev.COMPARISON),(sel,comparison_gate.SELECTION))) and
            mem["parent_comparison_key"]==comp["key"] and mem["parent_selection_key"]==sel["key"] and
            mem["retained_records"]==comp["records"] and mem["retained_groups"]==comp["groups"] and
            mem["proof_authority"] is False and mem["action_authority"] is False)

def admit(d,mp,ind,comp,sel,mem):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R55_DIRECT_CONTEXTUAL_PREFERENCE_MEMORY" or mp["status"]!="R55_REAL_MCP_GREEN" or
        ind["status"]!="R55_INDEPENDENT_CONTEXTUAL_PREFERENCE_MEMORY_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or not valid(mem,comp,sel)):
        raise ValueError("HOLD_R55_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "preference_key":KEY,"parent_comparison_key":prev.COMPARISON,"request_count":15,"typed_dispatches":9,
        "retained_routes":5,"hold_requests":6,"negative_requests":3,"all_routes_retained":True,
        "raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "proof_authority":False,"action_authority":False,"new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","preference_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=78:
        raise ValueError("HOLD_R55_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=78 or len(hist)!=78 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R55_AUDIT")
    if len(mem["dispatches"])!=9 or any(hist[n]!=x["observation"] for n,x in mem["dispatches"].items()):
        raise ValueError("HOLD_R55_DISPATCH")
    return hist

def request(sel,goal,policy,caps):
    return {"base_request":prev.request(sel,goal,policy),"preference_key":KEY,"caps":dict(caps)}

def choose(mem,comp,sel,q):
    def hold(status):
        return {"status":status,"preferred":[],"proof_authority":False,"action_authority":False}
    if not valid(mem,comp,sel):return hold("HOLD_PARENT_MEMORY")
    if set(q)!={"base_request","preference_key","caps"} or not isinstance(q["base_request"],dict):
        return hold("HOLD_REQUEST_SHAPE")
    if q["preference_key"]!=KEY:return hold("HOLD_PARENT_KEY")
    b=q["base_request"]
    if b.get("goal") not in prev.GOALS:return hold("HOLD_UNKNOWN_CONTEXT")
    if not isinstance(b.get("policy"),str) or b["policy"] not in prev.POLICIES:return hold("HOLD_UNKNOWN_POLICY")
    exp=prev.request(sel,b["goal"],b["policy"])
    if set(b)!=set(exp):return hold("HOLD_REQUEST_SHAPE")
    if any(b[k]!=exp[k] for k in ("source_head","source_tree","scope_digest")):return hold("HOLD_SOURCE_SCOPE")
    if any(b[k]!=exp[k] for k in ("parent_key","selection_key")):return hold("HOLD_PARENT_KEY")
    if b["goal_expr"]!=exp["goal_expr"]:return hold("HOLD_GOAL_TYPE")
    caps=q["caps"]
    if not isinstance(caps,dict) or any(k not in METRICS or type(v) is not int or v<0 for k,v in caps.items()):
        return hold("HOLD_INVALID_BUDGET")
    prior=[x for x in mem["decisions"] if x["request"]==b]
    if len(prior)!=1:return hold("HOLD_PARENT_DECISION")
    p=prior[0];records=mem["retained_records"];ns=p["all_routes"]
    if ns!=mem["retained_groups"][b["goal"]]["routes"]:return hold("HOLD_ROUTE_INVENTORY")
    excluded={n:sorted(k for k,v in caps.items() if records[n][k]>v) for n in ns}
    eligible=sorted(n for n in ns if not excluded[n])
    result={"request":copy.deepcopy(q),"request_id":old.digest(q),"parent_request_id":p["request_id"],
        "context_id":p["context_id"],"all_routes":list(ns),"eligible":eligible,
        "excluded":{n:ks for n,ks in excluded.items() if ks},"preferred":[],"unselected":list(ns),
        "parent_preferred":p["preferred"],"parent_polarity":p["polarity"],"parent_status":p["status"],
        "raw_negative_retained":True,"proof_authority":False,"action_authority":False,
        "search_complete":False,"budget_is_refutation":False,"fallback":False}
    if not ns:return {**result,"status":"HOLD_NO_RULE_ROUTE"}
    if not eligible:return {**result,"status":"HOLD_ROUTE_BUDGET"}
    scores=p["scores"];best=min(scores[n] for n in eligible)
    winners=sorted(n for n in eligible if scores[n]==best)
    return {**result,"status":"PREFERRED_FEASIBLE_ROUTE","preferred":winners,
        "unselected":sorted(set(ns)-set(winners)),"fallback":not bool(set(winners)&set(p["preferred"]))}

CASES=(
    ("global_default","shadowGlobal","compact",{},"shadowGlobal_9"),
    ("global_boundary","shadowGlobal","compact",{"boundary_count":81},"shadowGlobal_1"),
    ("global_size","shadowGlobal","bounded_dependencies",{"proof_nodes":29},"shadowGlobal_9"),
    ("global_joint","shadowGlobal","compact",{"proof_nodes":29,"boundary_count":81},"HOLD_ROUTE_BUDGET"),
    ("global_probes","shadowGlobal","compact",{"historical_probes":4},"shadowGlobal_9"),
    ("compat_boundary","shadowCompat","compact",{"boundary_count":81},"shadowCompat_3"),
    ("compat_size","shadowCompat","compact",{"proof_nodes":12},"HOLD_ROUTE_BUDGET"),
    ("negative_allowed","rawNoGlobal","compact",{"boundary_count":82},"rawNoGlobal_12"),
    ("negative_budget","rawNoGlobal","compact",{"boundary_count":81},"HOLD_ROUTE_BUDGET"),
    ("raw_global","rawGlobal","compact",{},"HOLD_NO_RULE_ROUTE"),
    ("raw_compat","rawCompat","compact",{},"HOLD_NO_RULE_ROUTE"),
    ("global_dependencies","shadowGlobal","compact",{"observed_dependency_count":52},"shadowGlobal_1"),
)

def plan(mem,comp,sel):
    ds={};selected={}
    for label,goal,policy,caps,expected in CASES:
        x=choose(mem,comp,sel,request(sel,goal,policy,caps));ds[label]=x
        if expected.startswith("HOLD_"):
            if x["status"]!=expected or x["preferred"]:raise ValueError("budget HOLD "+label)
        else:
            name="KuuOSR53Selected."+expected
            if x["status"]!="PREFERRED_FEASIBLE_ROUTE" or x["preferred"]!=[name]:raise ValueError("budget route "+label)
            selected["KuuOSR56Budget."+label]={"route":name,"goal":goal,
                "goal_expr":x["request"]["base_request"]["goal_expr"],"request_id":x["request_id"]}
    if len(selected)!=7 or sum(x["fallback"] for x in ds.values())!=3:
        raise ValueError("budget coverage")
    return ds,selected

def controls(mem,comp,sel):
    q=request(sel,"shadowGlobal","compact",{});b=q["base_request"]
    cases={
        "wrong_head":({**q,"base_request":{**b,"source_head":"0"*40}},"HOLD_SOURCE_SCOPE"),
        "wrong_type":({**q,"base_request":{**b,"goal_expr":"wrong"}},"HOLD_GOAL_TYPE"),
        "wrong_context":({**q,"base_request":{**b,"goal":"rawGlobal"}},"HOLD_GOAL_TYPE"),
        "wrong_preference":({**q,"preference_key":"0"*64},"HOLD_PARENT_KEY"),
        "unknown_metric":({**q,"caps":{"wall_clock":1}},"HOLD_INVALID_BUDGET"),
        "negative_cap":({**q,"caps":{"proof_nodes":-1}},"HOLD_INVALID_BUDGET"),
        "bool_cap":({**q,"caps":{"proof_nodes":True}},"HOLD_INVALID_BUDGET"),
        "float_cap":({**q,"caps":{"proof_nodes":29.0}},"HOLD_INVALID_BUDGET"),
        "unadmitted_route":({**q,"route":"arbitrary"},"HOLD_REQUEST_SHAPE")}
    out={}
    for label,(bad,expected) in cases.items():
        x=choose(mem,comp,sel,bad)
        if x["status"]!=expected or x["preferred"] or x["proof_authority"] or x["action_authority"]:
            raise ValueError("budget control "+label)
        out[label]=expected
    bad=copy.deepcopy(mem);bad["retained_records"].pop(next(iter(bad["retained_records"])))
    if choose(base.portable.seal(bad),comp,sel,q)["status"]!="HOLD_PARENT_MEMORY":
        raise ValueError("resealed memory accepted")
    out["resealed_memory"]="HOLD_PARENT_MEMORY"
    sets=[set(choose(mem,comp,sel,request(sel,"shadowGlobal","compact",{"boundary_count":n}))["eligible"]) for n in (80,81,82)]
    if not sets[0]<sets[1]<sets[2]:raise ValueError("budget monotonicity")
    out["tightening"]="ELIGIBILITY_MONOTONE_ON_OBSERVED_INVENTORY"
    return out
