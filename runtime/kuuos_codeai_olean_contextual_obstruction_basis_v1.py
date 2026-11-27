"""R60: finite operational obstruction bases from certified dependency paths.

A hitting set blocks the recorded budget-eligible routes under a denial
policy. It never refutes the underlying proposition or unobserved routes.
Empty route inventories are HOLD, not a vacuous obstruction certificate.
"""
from __future__ import annotations
from itertools import combinations
import copy
from runtime import kuuos_codeai_olean_contextual_dependency_paths_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
render=prev.render
DIRECT="64dd8fb1a22d00950967acab1d4f3249421d89aaf23374838c21c54edc1e925e"
MCP="76bb6001600ed5e7be42ffb943f16f9e96ab4bcc5515e335a92b7ca653a5bfdb"
KEY="7ac4bd5667134d2df62f23b6b879c053921d885356771843f4dc1dffb621f294"

def valid(paths,edges,av,budget,pref,comp,sel):
    return (paths.get("key")==KEY and base.portable.seal(paths)["key"]==KEY and
        prev.valid(edges,av,budget,pref,comp,sel) and paths["parent_edges_key"]==edges["key"] and
        paths["parent_availability_key"]==av["key"] and paths["retained_records"]==pref["retained_records"] and
        paths["retained_groups"]==pref["retained_groups"] and paths["proof_authority"] is False and
        paths["action_authority"] is False and paths["complete_transitive_closure"] is False)

def admit(d,mp,ind,comp,sel,pref,budget,av,edges,paths):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R59_DIRECT_CONTEXTUAL_DEPENDENCY_PATHS" or mp["status"]!="R59_REAL_MCP_GREEN" or
        ind["status"]!="R59_INDEPENDENT_CONTEXTUAL_DEPENDENCY_PATHS_GREEN" or ind["direct_digest"]!=DIRECT or
        ind["mcp_digest"]!=MCP or not valid(paths,edges,av,budget,pref,comp,sel)):
        raise ValueError("HOLD_R59_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "paths_key":KEY,"parent_edges_key":prev.KEY,"request_count":9,"typed_dispatches":3,
        "path_count":1322,"blocked_path_count":7,"new_path_count":1,"retained_routes":5,"all_routes_retained":True,
        "raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,"proof_authority":False,
        "action_authority":False,"complete_transitive_closure":False,"policy_is_refutation":False,
        "shortest_paths_in_observed_graph_only":True,"new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","paths_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=95:
        raise ValueError("HOLD_R59_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=95 or len(hist)!=95 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R59_AUDIT")
    if len(paths["dispatches"])!=3 or any(hist[n]!=x["observation"] for n,x in paths["dispatches"].items()):
        raise ValueError("HOLD_R59_DISPATCH")
    return hist

def hits(deps,cut):
    return bool(deps) and all(set(cut)&v for v in deps.values())

def minimal(deps):
    # At most two routes occur in this exact parent inventory.
    # Every inclusion-minimal hitting set has size at most the route count:
    # each member must uniquely hit some route, and those routes are distinct.
    if not deps:return [],0
    ns=sorted(deps)
    if len(ns)>2 or any(not x for x in deps.values()):
        raise ValueError("HOLD_BASIS_SCOPE")
    common=set.intersection(*deps.values())
    cuts={(n,) for n in common}
    if len(ns)==2:
        a,b=(deps[n] for n in ns)
        cuts|={tuple(sorted((x,y))) for x in a-b for y in b-a}
    # Independently enumerate every singleton and, for two routes, every pair.
    domain=sorted(set.union(*deps.values()));brute=set();trials=0
    for size in range(1,len(ns)+1):
        for cut in combinations(domain,size):
            trials+=1
            if hits(deps,cut) and not any(hits(deps,cut[:i]+cut[i+1:]) for i in range(size)):
                brute.add(cut)
    if cuts!=brute:raise ValueError("HOLD_BASIS_ENUMERATION")
    return sorted(cuts,key=lambda x:(len(x),x)),trials

def check_cut(deps,cut):
    if not isinstance(cut,list) or not cut or not all(isinstance(n,str) for n in cut) or cut!=sorted(set(cut)):
        raise ValueError("HOLD_CUT_SHAPE")
    if not hits(deps,cut):raise ValueError("HOLD_CUT_INCOMPLETE")
    if any(hits(deps,cut[:i]+cut[i+1:]) for i in range(len(cut))):
        raise ValueError("HOLD_CUT_NOT_MINIMAL")

def project(paths,budget,projection,expanded):
    if projection!=paths["projection"]:raise ValueError("HOLD_PATH_PROJECTION_DRIFT")
    rp=projection["route_paths"]
    if any(expanded["routes"][n]["missing_references"] for n in rp):
        raise ValueError("HOLD_ENV_MISSING")
    groups={}
    for case,b in sorted(budget["decisions"].items()):
        ns=b["eligible"];deps={n:set(rp[n]) for n in ns}
        cuts,trials=minimal(deps)
        records=[]
        for cut in cuts:
            check_cut(deps,list(cut))
            # Link each blocked route to all relevant certified paths.
            evidence={n:{k:old.digest(rp[n][k]) for k in cut if k in deps[n]} for n in ns}
            records.append({"denied":list(cut),"path_digests":evidence})
        groups[case]={"parent_request_id":b["request_id"],"context_id":b["context_id"],
            "all_routes":b["all_routes"],"budget_eligible":ns,"parent_status":b["status"],
            "parent_polarity":b["parent_polarity"],"cuts":records,"enumerated_candidates":trials,
            "singleton_count":sum(len(x)==1 for x in cuts),"pair_count":sum(len(x)==2 for x in cuts),
            "status":"FINITE_POLICY_BASIS" if ns else b["status"],
            "complete_for_recorded_routes_only":bool(ns),"proof_authority":False,"action_authority":False}
    return groups

def choose(paths,budget,pref,groups,q):
    def hold(status):
        return {"status":status,"preferred":[],"proof_authority":False,"action_authority":False}
    if paths.get("key")!=KEY or base.portable.seal(paths)["key"]!=KEY or budget.get("key")!=prev.prev.prev.KEY or base.portable.seal(budget)["key"]!=budget["key"] or pref.get("key")!=prev.prev.prev.prev.KEY or base.portable.seal(pref)["key"]!=pref["key"]:
        return hold("HOLD_PARENT_MEMORY")
    if set(q)!={"paths_key","case","denied"}:return hold("HOLD_REQUEST_SHAPE")
    if q["paths_key"]!=KEY:return hold("HOLD_PARENT_KEY")
    case=q["case"]
    if not isinstance(case,str) or case not in groups:return hold("HOLD_UNKNOWN_CONTEXT")
    denied=q["denied"]
    if not isinstance(denied,list) or not all(isinstance(n,str) for n in denied) or denied!=sorted(set(denied)):
        return hold("HOLD_DENIAL_SHAPE")
    rp=paths["projection"]["route_paths"]
    if set(denied)-{n for ps in rp.values() for n in ps}:return hold("HOLD_UNKNOWN_DEPENDENCY")
    b=budget["decisions"][case];g=groups[case];ns=b["eligible"]
    if g["parent_request_id"]!=b["request_id"] or g["budget_eligible"]!=ns:
        return hold("HOLD_BASIS_LINEAGE")
    blocked={n:{k:rp[n][k] for k in denied if k in rp[n]} for n in ns}
    eligible=sorted(n for n in ns if not blocked[n])
    contained=[x["denied"] for x in g["cuts"] if set(x["denied"])<=set(denied)]
    result={"request":copy.deepcopy(q),"request_id":old.digest(q),"parent_request_id":b["request_id"],
        "context_id":b["context_id"],"all_routes":b["all_routes"],"budget_eligible":ns,"eligible":eligible,
        "blocked_paths":{n:x for n,x in blocked.items() if x},"contained_minimal_cuts":contained,
        "preferred":[],"parent_polarity":b["parent_polarity"],"proof_authority":False,"action_authority":False,
        "policy_is_refutation":False,"raw_negative_retained":True}
    if not ns:return {**result,"status":b["status"]}
    if bool(contained)!=(not bool(eligible)):raise ValueError("HOLD_BASIS_DECISION_DRIFT")
    if not eligible:return {**result,"status":"HOLD_ALL_RECORDED_ROUTES_BLOCKED"}
    parents=[x for x in pref["decisions"] if x["request"]==b["request"]["base_request"]]
    if len(parents)!=1:raise ValueError("HOLD_PREF_LINEAGE")
    scores=parents[0]["scores"];best=min(scores[n] for n in eligible)
    return {**result,"status":"PREFERRED_POLICY_ROUTE","preferred":sorted(n for n in eligible if scores[n]==best)}

def plan(paths,edges,av,budget,pref,sel,groups):
    rp=paths["projection"]["route_paths"]
    a="KuuOSR53Selected.shadowGlobal_1";b="KuuOSR53Selected.shadowGlobal_9"
    left=sorted(set(rp[a])-set(rp[b]));right=sorted(set(rp[b])-set(rp[a]))
    if not left or not right:raise ValueError("HOLD_EXCLUSIVE_DEPENDENCIES")
    ds={};selected={}
    # Historical requests are replayed at the expanded R58 scope, not retroactively
    # evaluated as though R57 had observed these edges.
    for label,d in sorted(edges["decisions"].items()):
        q={"paths_key":KEY,"case":d["request"]["case"],"denied":d["request"]["denied"]}
        x=choose(paths,budget,pref,groups,q)
        if x["preferred"]!=d["preferred"] or x["eligible"]!=d["eligible"]:
            raise ValueError("HOLD_HISTORICAL_POLICY_DRIFT")
        ds["historical_"+label]=x
    cases=(("deny_left",[left[0]],b),("deny_right",[right[0]],a),
           ("deny_both",sorted([left[0],right[0]]),None),("deny_common",["And"],None))
    for label,denied,expected in cases:
        q={"paths_key":KEY,"case":"global_default","denied":denied}
        x=choose(paths,budget,pref,groups,q);ds[label]=x
        if expected is None:
            if x["status"]!="HOLD_ALL_RECORDED_ROUTES_BLOCKED" or x["preferred"] or denied not in x["contained_minimal_cuts"]:
                raise ValueError("HOLD_EXPECTED_CUT")
        elif x["preferred"]!=[expected] or x["status"]!="PREFERRED_POLICY_ROUTE":
            raise ValueError("HOLD_EXPECTED_ALTERNATIVE")
        else:
            selected["KuuOSR60Obstruction."+label]={"route":expected,"goal":"shadowGlobal",
                "goal_expr":sel["observations"]["shadowGlobal"]["goal_expr"],"request_id":x["request_id"]}
    if len(ds)!=13 or len(selected)!=2:raise ValueError("HOLD_CASE_INVENTORY")
    return ds,selected

def controls(paths,budget,pref,groups,ds):
    out={}
    q={"paths_key":KEY,"case":"global_default","denied":[]}
    for label,bad,status in (
        ("wrong_key",{**q,"paths_key":"0"*64},"HOLD_PARENT_KEY"),
        ("wrong_case",{**q,"case":"unknown"},"HOLD_UNKNOWN_CONTEXT"),
        ("unknown_dependency",{**q,"denied":["KuuOSR60.Fabricated"]},"HOLD_UNKNOWN_DEPENDENCY"),
        ("duplicate_denial",{**q,"denied":["And","And"]},"HOLD_DENIAL_SHAPE"),
        ("extra_route",{**q,"route":"unknown"},"HOLD_REQUEST_SHAPE")):
        x=choose(paths,budget,pref,groups,bad)
        if x["status"]!=status or x["preferred"] or x["proof_authority"] or x["action_authority"]:
            raise ValueError(label)
        out[label]=status
    bad=copy.deepcopy(paths);bad["projection"]["route_paths"].pop(next(iter(bad["projection"]["route_paths"])))
    if choose(base.portable.seal(bad),budget,pref,groups,q)["status"]!="HOLD_PARENT_MEMORY":raise ValueError("resealed paths accepted")
    out["resealed_paths"]="HOLD_PARENT_MEMORY"
    rp=paths["projection"]["route_paths"];deps={n:set(rp[n]) for n in groups["global_default"]["budget_eligible"]}
    incomplete=ds["deny_left"]["request"]["denied"]
    redundant=sorted(set(incomplete)|{"And"})
    for label,cut,status in (("incomplete_cut",incomplete,"HOLD_CUT_INCOMPLETE"),
                             ("nonminimal_cut",redundant,"HOLD_CUT_NOT_MINIMAL")):
        try:check_cut(deps,cut)
        except ValueError as e:
            if str(e)!=status:raise
            out[label]=status
        else:raise ValueError("invalid cut accepted")
    if any(groups[n]["cuts"] or groups[n]["complete_for_recorded_routes_only"] for n in ("raw_global","raw_compat","global_joint","negative_budget")):
        raise ValueError("vacuous obstruction")
    out["empty_inventory"]="HOLD_NOT_VACUOUS_REFUTATION"
    return out
