"""R59: exact bounded dependency-path witnesses for contextual withdrawal.
Witnesses certify reachability in the observed graph, not a Lean theorem of
necessity, full transitive closure, or an authorization to use a proof.
"""
from __future__ import annotations
from collections import deque
import copy
from runtime import kuuos_codeai_olean_contextual_dependency_edges_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
render=prev.render
DIRECT="4e30ddb66a4549ec66c4b45455526bb246fe2771e24880951ca8e5deb8403175"
MCP="b1779a05a3cc8791a6b3682a53dfce143bc6817b10689bee00388b84964cf283"
KEY="6196ef47162454369927c0a654d18889f135d27183249553fa56818e2003b5a0"

def valid(edges,av,budget,pref,comp,sel):
    return (edges.get("key")==KEY and base.portable.seal(edges)["key"]==KEY and
        prev.valid(av,budget,pref,comp,sel) and edges["parent_availability_key"]==av["key"] and
        edges["parent_budget_key"]==budget["key"] and edges["retained_records"]==pref["retained_records"] and
        edges["retained_groups"]==pref["retained_groups"] and edges["proof_authority"] is False and
        edges["action_authority"] is False and edges["complete_transitive_closure"] is False)

def admit(d,mp,ind,comp,sel,pref,budget,av,edges):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R58_DIRECT_CONTEXTUAL_DEPENDENCY_EDGES" or mp["status"]!="R58_REAL_MCP_GREEN" or
        ind["status"]!="R58_INDEPENDENT_CONTEXTUAL_DEPENDENCY_EDGES_GREEN" or ind["direct_digest"]!=DIRECT or
        ind["mcp_digest"]!=MCP or not valid(edges,av,budget,pref,comp,sel)):
        raise ValueError("HOLD_R58_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "edges_key":KEY,"parent_availability_key":prev.KEY,"request_count":9,"typed_dispatches":3,
        "choices_changed":1,"expanded_dependency_holds":1,"expanded_distinct_names":145,
        "distinct_next_names":129,"retained_routes":5,"all_routes_retained":True,
        "raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "proof_authority":False,"action_authority":False,"complete_transitive_closure":False,
        "full_body_serialized":False,"policy_is_refutation":False,"new_root_discovery_trials":0,"capsule_rebuilds":0}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","edges_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=92:
        raise ValueError("HOLD_R58_SCOPE")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=92 or len(hist)!=92 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R58_AUDIT")
    if len(edges["dispatches"])!=3 or any(hist[n]!=x["observation"] for n,x in edges["dispatches"].items()):
        raise ValueError("HOLD_R58_DISPATCH")
    return hist

def adjacency(route,comp,expanded,hist):
    r=expanded["routes"][route]
    graph={}
    def put(n,types,values):
        graph[n]=sorted({("type",x) for x in types}|{("value",x) for x in values})
    put(route,hist[route]["type_constants"],comp["records"][route]["direct_constants"])
    for n in r["historical"]:
        row=expanded["nodes"][n]
        put(n,row["type_constants"],row["value_constants"])
    return graph

def paths(route,graph):
    found={route:[]};q=deque([route])
    while q:
        n=q.popleft()
        for kind,t in graph.get(n,[]):
            if t not in found:
                found[t]=found[n]+[{"from":n,"edge":kind,"to":t}]
                q.append(t)
    found.pop(route)
    return found

def check_path(route,target,path,graph):
    if not isinstance(path,list) or not path:raise ValueError("HOLD_PATH_EMPTY")
    here=route;seen={here}
    for step in path:
        if not isinstance(step,dict) or set(step)!={"from","edge","to"} or step["from"]!=here:
            raise ValueError("HOLD_PATH_CHAIN")
        nxt=step["to"]
        if not isinstance(nxt,str) or step["edge"] not in ("type","value") or (step["edge"],nxt) not in graph.get(here,[]):
            raise ValueError("HOLD_PATH_EDGE")
        if nxt in seen:raise ValueError("HOLD_PATH_CYCLE")
        seen.add(nxt);here=nxt
    if here!=target:raise ValueError("HOLD_PATH_TARGET")
    if len(path)!=len(paths(route,graph)[target]):raise ValueError("HOLD_PATH_NOT_SHORTEST")
    return True

def project(edges,av,budget,comp,hist,expanded):
    if expanded!=edges["expanded"]:raise ValueError("HOLD_R58_EXPANDED_DRIFT")
    route_paths={};graphs={}
    for route,r in sorted(expanded["routes"].items()):
        g=adjacency(route,comp,expanded,hist);graphs[route]=g
        ps=paths(route,g)
        if set(ps)!=set(r["observed_references"])-{route}:
            raise ValueError("HOLD_PATH_INVENTORY")
        for n,p in ps.items():check_path(route,n,p,g)
        route_paths[route]=ps
    explanations={}
    for label,d in sorted(edges["decisions"].items()):
        prior=av["decisions"][label]
        q=d["request"]
        if q!=prior["request"] or d["parent_request_id"]!=prior["request_id"] or d["all_routes"]!=prior["all_routes"]:
            raise ValueError("HOLD_PATH_LINEAGE")
        denied=set(q["denied"]);blocked={}
        for route in d["all_routes"]:
            ps=route_paths[route]
            hits=sorted(denied&set(ps))
            if hits:blocked[route]={n:ps[n] for n in hits}
        if {n:sorted(v) for n,v in blocked.items()}!=d["policy_excluded"]:
            raise ValueError("HOLD_PATH_POLICY_MISMATCH")
        new={r:{n:p for n,p in hits.items() if n not in av["availability"][r]["present"]}
             for r,hits in blocked.items()}
        new={r:hits for r,hits in new.items() if hits}
        explanations[label]={"request":copy.deepcopy(q),"parent_status":prior["status"],"status":d["status"],
            "old_preferred":d["old_preferred"],"preferred":d["preferred"],"all_routes":d["all_routes"],
            "blocked_paths":blocked,"new_boundary_paths":new,"newly_excluded":d["newly_excluded"],
            "parent_polarity":d["parent_polarity"],"proof_authority":False,"action_authority":False,
            "policy_is_refutation":False}
    a="KuuOSR53Selected.shadowGlobal_1";b="KuuOSR53Selected.shadowGlobal_9"
    w=explanations["deny_preferred"]
    if (w["status"]!="HOLD_EXPANDED_DEPENDENCY" or w["preferred"] or w["newly_excluded"]!=[a] or
        "And" not in w["new_boundary_paths"].get(a,{}) or
        set(w["blocked_paths"])!={a,b} or any("And" not in w["blocked_paths"][n] for n in (a,b))):
        raise ValueError("HOLD_WITHDRAWAL_WITNESS")
    return {"route_paths":route_paths,"explanations":explanations,
        "path_count":sum(len(v) for v in route_paths.values()),
        "blocked_path_count":sum(len(h) for x in explanations.values() for h in x["blocked_paths"].values()),
        "new_path_count":sum(len(h) for x in explanations.values() for h in x["new_boundary_paths"].values()),
        "withdrawal_paths":w["blocked_paths"],"complete_transitive_closure":False,
        "shortest_paths_in_observed_graph_only":True,"proof_authority":False}

def plan(edges,budget,sel,projection):
    selected={}
    for label,d in sorted(edges["decisions"].items()):
        ex=projection["explanations"][label]
        if ex["preferred"]!=d["preferred"] or ex["status"]!=d["status"]:raise ValueError("HOLD_EXPLANATION_DRIFT")
        goal=budget["decisions"][d["request"]["case"]]["request"]["base_request"]["goal"]
        for i,n in enumerate(d["preferred"]):
            selected["KuuOSR59Path."+label+"_"+str(i)]={"route":n,"goal":goal,
                "goal_expr":sel["observations"][goal]["goal_expr"],"request_id":old.digest(d["request"])}
    if len(selected)!=3:raise ValueError("HOLD_R59_DISPATCH_COUNT")
    return selected

def controls(edges,av,budget,comp,hist,expanded,projection):
    route="KuuOSR53Selected.shadowGlobal_1";target="And"
    g=adjacency(route,comp,expanded,hist);p=projection["route_paths"][route][target]
    out={}
    cases=[("empty",[],"HOLD_PATH_EMPTY"),
           ("wrong_start",[{**p[0],"from":"KuuOSR59.Fabricated"}]+p[1:],"HOLD_PATH_CHAIN"),
           ("fabricated_edge",[{**p[0],"to":"KuuOSR59.Fabricated"}]+p[1:],"HOLD_PATH_EDGE"),
           ("wrong_kind",[{**p[0],"edge":"unknown"}]+p[1:],"HOLD_PATH_EDGE")]
    for label,bad,status in cases:
        try:check_path(route,target,bad,g)
        except ValueError as e:
            if str(e)!=status:raise
            out[label]=status
        else:raise ValueError("invalid path accepted "+label)
    try:check_path(route,"KuuOSR59.Fabricated",p,g)
    except ValueError as e:
        if str(e)!="HOLD_PATH_TARGET":raise
        out["wrong_target"]=str(e)
    else:raise ValueError("wrong target accepted")
    bad=copy.deepcopy(expanded);bad["routes"][route]["observed_references"].append("KuuOSR59.Fabricated")
    try:project(edges,av,budget,comp,hist,bad)
    except ValueError as e:
        if str(e)!="HOLD_R58_EXPANDED_DRIFT":raise
        out["unobserved_reference"]=str(e)
    else:raise ValueError("unobserved reference accepted")
    return out
