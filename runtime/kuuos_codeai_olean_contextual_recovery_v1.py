"""R61: counterfactual minimal release sets, with immutable active policy.

Recovery candidates are advisory only, not a policy change. Locked denials
cannot be released. A finite recovery condition never asserts authorization,
mathematical necessity, or complete dependency knowledge.
"""
from __future__ import annotations
from itertools import combinations
import copy
from runtime import kuuos_codeai_olean_contextual_obstruction_basis_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
render=prev.render
DIRECT="0112ffdbca8b1933fdd28683bc6f27cdf5ed1df45cbab16f035301eba3681231"
MCP="34d2a2e9b8d4b7a9a9344ea87427e57461f3a722c3f172ca9754334ee93d0bf3"
KEY="3178ed48c5dfb2dbe989c53c3ed75d961d530cd86efcd0f64e5c1f0d24a93928"

def valid(obs,paths,edges,av,budget,pref,comp,sel):
    return (obs.get("key")==KEY and base.portable.seal(obs)["key"]==KEY and
        prev.valid(paths,edges,av,budget,pref,comp,sel) and
        obs["parent_paths_key"]==paths["key"] and obs["parent_edges_key"]==edges["key"] and
        obs["retained_records"]==pref["retained_records"] and obs["retained_groups"]==pref["retained_groups"] and
        obs["proof_authority"] is False and obs["action_authority"] is False and
        obs["complete_transitive_closure"] is False and obs["policy_is_refutation"] is False)

def admit(d,mp,ind,comp,sel,pref,budget,av,edges,paths,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R60_DIRECT_CONTEXTUAL_OBSTRUCTION_BASIS" or mp["status"]!="R60_REAL_MCP_GREEN" or
        ind["status"]!="R60_INDEPENDENT_CONTEXTUAL_OBSTRUCTION_BASIS_GREEN" or ind["direct_digest"]!=DIRECT or
        ind["mcp_digest"]!=MCP or not valid(obs,paths,edges,av,budget,pref,comp,sel)):
        raise ValueError("HOLD_R60_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "obstruction_key":KEY,"parent_paths_key":prev.KEY,"request_count":13,"typed_dispatches":2,
        "basis_contexts":12,"finite_basis_contexts":7,"enumerated_candidates":37903,"minimal_cut_count":1856,
        "singleton_count":1848,"pair_count":8,"historical_policy_cases_replayed":9,"retained_routes":5,
        "all_routes_retained":True,"raw_positive_hold":True,"raw_negative_retained":True,
        "historical_hold_retained":True,"proof_authority":False,"action_authority":False,
        "complete_transitive_closure":False,"policy_is_refutation":False,"new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","obstruction_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=97:
        raise ValueError("HOLD_R60_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=97 or len(hist)!=97 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R60_AUDIT")
    if len(obs["dispatches"])!=2 or any(hist[n]!=x["observation"] for n,x in obs["dispatches"].items()):
        raise ValueError("HOLD_R60_DISPATCH")
    return hist

def minimal_sets(xs):
    return sorted({tuple(sorted(x)) for x in xs if not any(y<x for y in xs)},key=lambda x:(len(x),x))

def choose(obs,paths,budget,pref,q):
    def hold(status):
        return {"status":status,"preferred":[],"candidates":[],"proof_authority":False,"action_authority":False}
    for x,key in ((obs,KEY),(paths,prev.KEY),(budget,prev.prev.prev.prev.KEY),(pref,prev.prev.prev.prev.prev.KEY)):
        if x.get("key")!=key or base.portable.seal(x)["key"]!=key:return hold("HOLD_PARENT_MEMORY")
    if obs["parent_paths_key"]!=paths["key"]:return hold("HOLD_PARENT_MEMORY")
    if set(q)!={"obstruction_key","case","denied","locked"}:return hold("HOLD_REQUEST_SHAPE")
    if q["obstruction_key"]!=KEY:return hold("HOLD_PARENT_KEY")
    case=q["case"]
    if not isinstance(case,str) or case not in obs["groups"]:return hold("HOLD_UNKNOWN_CONTEXT")
    for field in ("denied","locked"):
        xs=q[field]
        if not isinstance(xs,list) or not all(isinstance(n,str) for n in xs) or xs!=sorted(set(xs)):
            return hold("HOLD_DENIAL_SHAPE")
    D=set(q["denied"]);L=set(q["locked"])
    if not L<=D:return hold("HOLD_LOCK_NOT_DENIED")
    if len(D)>12:return hold("HOLD_COUNTERFACTUAL_BUDGET")
    rp=paths["projection"]["route_paths"]
    if D-{n for ps in rp.values() for n in ps}:return hold("HOLD_UNKNOWN_DEPENDENCY")
    b=budget["decisions"][case];ns=b["eligible"];groups=obs["groups"]
    original=prev.choose(paths,budget,pref,groups,{"paths_key":prev.KEY,"case":case,"denied":q["denied"]})
    if original["status"] not in ("HOLD_ALL_RECORDED_ROUTES_BLOCKED","PREFERRED_POLICY_ROUTE","HOLD_ROUTE_BUDGET","HOLD_NO_RULE_ROUTE"):
        raise ValueError("HOLD_ORIGINAL_DECISION")
    result={"request":copy.deepcopy(q),"request_id":old.digest(q),"original":original,
        "status":original["status"],"preferred":original["preferred"],"candidates":[],
        "locked":sorted(L),"parent_polarity":b["parent_polarity"],"actual_denied":sorted(D),
        "active_policy_changed":False,"release_authorized":False,"external_approval_required":True,
        "proof_authority":False,"action_authority":False,"policy_is_refutation":False,
        "raw_negative_retained":True,"enumerated_subsets":0}
    if not ns:return result
    if original["eligible"]:return {**result,"status":"ALREADY_ELIGIBLE"}
    deps={n:set(rp[n]) for n in ns}
    release_sets=[D&v for v in deps.values() if not L&v]
    cuts=[set(c["denied"]) for c in groups[case]["cuts"] if set(c["denied"])<=D]
    def restores(R):
        # Dual to hitting all contained minimal obstruction cuts.
        by_route=any(not (D-R)&v for v in deps.values())
        by_basis=all(R&c for c in cuts)
        if by_route!=by_basis:raise ValueError("HOLD_RELEASE_DUALITY")
        return by_route
    brute=[];count=0;domain=sorted(D-L)
    for size in range(len(domain)+1):
        for xs in combinations(domain,size):
            R=set(xs);count+=1
            if restores(R) and not any(restores(R-{k}) for k in R):brute.append(R)
    minimal=minimal_sets(release_sets)
    if minimal!=minimal_sets(brute):raise ValueError("HOLD_RELEASE_ENUMERATION")
    candidates=[]
    for xs in minimal:
        R=set(xs)
        if not R or R&L or not R<=D or not restores(R) or any(restores(R-{k}) for k in R):
            raise ValueError("HOLD_RELEASE_MINIMALITY")
        reduced=sorted(D-R)
        after=prev.choose(paths,budget,pref,groups,{"paths_key":prev.KEY,"case":case,"denied":reduced})
        if after["status"]!="PREFERRED_POLICY_ROUTE" or not after["eligible"]:
            raise ValueError("HOLD_COUNTERFACTUAL_REPLAY")
        candidates.append({"release":list(xs),"remaining_denied":reduced,"hypothetical_eligible":after["eligible"],
            "hypothetical_preferred":after["preferred"],"broken_cuts":[sorted(c) for c in cuts if R&c],
            "path_digests":{n:{k:old.digest(rp[n][k]) for k in xs if k in rp[n]} for n in after["eligible"]},
            "external_approval_required":True,"action_authority":False,"status":"COUNTERFACTUAL_ONLY"})
    return {**result,"status":"HOLD_AWAITING_EXTERNAL_APPROVAL" if candidates else "HOLD_LOCKED_OBSTRUCTION",
        "candidates":candidates,"enumerated_subsets":count}

def plan(obs,paths,budget,pref,sel):
    ds={};selected={}
    def add(label,case,denied,locked):
        q={"obstruction_key":KEY,"case":case,"denied":sorted(denied),"locked":sorted(locked)}
        x=choose(obs,paths,budget,pref,q);ds[label]=x
        if x["active_policy_changed"] or x["release_authorized"] or x["action_authority"]:
            raise ValueError("HOLD_AUTHORITY_ESCALATION")
        return x
    for label,d in sorted(obs["decisions"].items()):
        q=d["request"];x=add("historical_"+label,q["case"],q["denied"],[])
        if x["original"]!=d:raise ValueError("HOLD_R60_POLICY_DRIFT")
    both=obs["decisions"]["deny_both"]["request"]["denied"]
    left=obs["decisions"]["deny_left"]["request"]["denied"][0]
    right=obs["decisions"]["deny_right"]["request"]["denied"][0]
    a="KuuOSR53Selected.shadowGlobal_1";b="KuuOSR53Selected.shadowGlobal_9"
    for label,denied,locked,expected in (
        ("lock_left",both,[left],[(right,)]),("lock_right",both,[right],[(left,)]),
        ("lock_both",both,both,[]),("lock_shared",["And"],["And"],[]),
        ("shared_and_both",sorted(set(both)|{"And"}),[],[tuple(sorted(["And",left])),tuple(sorted(["And",right]))]),
        ("compound_locked_shared",sorted(set(both)|{"And"}),["And"],[])):
        x=add(label,"global_default",denied,locked)
        if {tuple(c["release"]) for c in x["candidates"]}!=set(expected) or x["preferred"]:
            raise ValueError("HOLD_RELEASE_CASE "+label)
    for label,route in (("lock_left",b),("lock_right",a)):
        x=ds[label];c=x["candidates"][0]
        if c["hypothetical_preferred"]!=[route] or x["status"]!="HOLD_AWAITING_EXTERNAL_APPROVAL":
            raise ValueError("HOLD_HYPOTHETICAL_TYPE")
        # Diagnostic theorem only: this does not dispatch an active request.
        selected["KuuOSR61Recovery."+label]={"route":route,"goal":"shadowGlobal",
            "goal_expr":sel["observations"]["shadowGlobal"]["goal_expr"],"request_id":x["request_id"]}
    if len(ds)!=19 or len(selected)!=2:raise ValueError("HOLD_RECOVERY_INVENTORY")
    return ds,selected

def controls(obs,paths,budget,pref,ds):
    q=ds["lock_left"]["request"];out={}
    for label,bad,status in (
        ("wrong_key",{**q,"obstruction_key":"0"*64},"HOLD_PARENT_KEY"),
        ("unknown_case",{**q,"case":"unknown"},"HOLD_UNKNOWN_CONTEXT"),
        ("unknown_dependency",{**q,"denied":["KuuOSR61.Fabricated"],"locked":[]},"HOLD_UNKNOWN_DEPENDENCY"),
        ("locked_not_denied",{**q,"locked":["KuuOSR61.Fabricated"]},"HOLD_LOCK_NOT_DENIED"),
        ("duplicate",{**q,"denied":["And","And"],"locked":[]},"HOLD_DENIAL_SHAPE"),
        ("extra_authority",{**q,"authorized":True},"HOLD_REQUEST_SHAPE")):
        x=choose(obs,paths,budget,pref,bad)
        if x["status"]!=status or x["preferred"] or x["candidates"] or x["action_authority"]:raise ValueError(label)
        out[label]=status
    bad=copy.deepcopy(obs);bad["groups"].pop("global_default")
    if choose(base.portable.seal(bad),paths,budget,pref,q)["status"]!="HOLD_PARENT_MEMORY":raise ValueError("resealed parent accepted")
    out["resealed_parent"]="HOLD_PARENT_MEMORY"
    if any(x["active_policy_changed"] or x["release_authorized"] or
           any(c["action_authority"] for c in x["candidates"]) for x in ds.values()):
        raise ValueError("policy escalated")
    out["authority"]="COUNTERFACTUAL_ONLY"
    if any(ds["historical_historical_"+n]["candidates"] for n in ("budget_unchanged","raw_search")):
        raise ValueError("unrelated HOLD treated as release")
    out["unrelated_hold"]="NO_POLICY_RECOVERY_CLAIM"
    if any(set(c["release"])&set(x["locked"]) for x in ds.values() for c in x["candidates"]):
        raise ValueError("locked denial released")
    out["locked_denials"]="ALL_PRESERVED"
    return out
