"""R54: compare certified R53 routes without rediscovering them.

Five admitted routes are replayed with their original rule, mode, and fact
pool. Proof values and exact goals must match. Rankings are optional
preferences, never proof admission, refutation, or action authority.
"""
from __future__ import annotations
import copy
import json
from runtime import kuuos_codeai_olean_contextual_rule_selection_v1_r2 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
derived=prev.derived
DIRECT="17f266ae7304d41954030e72d2f1d108325fd9bcfc19951de557746cbace2533"
MCP="44d056931857e37595e27f86b5e11ea5ac260a293cba6357fae2e5503b38ffd9"
SELECTION="4eb723ce2a53debbe3745c379ea158a0618227995acb213f87c4b92d3c8bbdc5"
MANIFEST=prev.MANIFEST
MARK="KUUOS_R54_REPLAY "
COUNTS={"rawCompat":0,"rawGlobal":0,"rawNoGlobal":1,"shadowCompat":2,"shadowGlobal":2}
POLICIES={
    "compact":("proof_nodes","boundary_count","observed_dependency_count"),
    "bounded_dependencies":("boundary_count","observed_dependency_count","proof_nodes"),
    "historical_probe_cost":("historical_probes","proof_nodes","boundary_count")}

def admit(d,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference,application,selection):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R53_DIRECT_CONTEXTUAL_RULE_SELECTION" or mp["status"]!="R53_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R53_INDEPENDENT_CONTEXTUAL_RULE_SELECTION_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP):
        raise ValueError("R53 receipt binding")
    chain=((selection,SELECTION),(application,prev.APPLICATION),
        (reference,prev.prev.REFERENCE),(frontier,prev.prev.prev.FRONTIER),
        (graph,prev.prev.prev.prev.GRAPH),(memory,prev.prev.prev.prev.prev.LAYER),
        (layer,prev.prev.prev.prev.prev.prev.PARENT),(extension,derived.PARENT),
        (index,derived.parent.PARENT),(mem,dispatch.LAYER))
    if any(x["key"]!=k or base.portable.seal(x)["key"]!=k for x,k in chain):
        raise ValueError("R53 immutable layer binding")
    if (selection["parent_application_key"]!=application["key"] or
        application["parent_reference_key"]!=reference["key"] or
        reference["parent_frontier_key"]!=frontier["key"] or reference["parent_graph_key"]!=graph["key"] or
        frontier["parent_graph_key"]!=graph["key"] or graph["parent_transport_key"]!=memory["key"] or
        memory["parent_derived_key"]!=layer["key"] or memory["parent_extension_key"]!=extension["key"] or
        memory["parent_dispatch_key"]!=index["key"] or layer["parent_extension_key"]!=extension["key"] or
        layer["parent_dispatch_key"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"]):
        raise ValueError("R53 lineage drift")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "selection_key":SELECTION,"application_key":application["key"],"reference_key":reference["key"],
        "frontier_key":frontier["key"],"graph_key":graph["key"],"transport_layer_key":memory["key"],
        "derived_layer_key":layer["key"],"extension_key":extension["key"],"dispatch_layer_key":index["key"],
        "capsule_layer_key":mem["key"],"capsule_manifest":dispatch.prev.MANIFEST,"joint_capsule_manifest":MANIFEST,
        "rule_candidates":23,"fact_candidates":11,"goal_count":5,"rule_trials":345,"premise_probes":511,
        "checked_routes":5,"positive_routes":4,"negative_routes":1,"route_counts":COUNTS,
        "raw_positive_hold":True,"historical_hold_retained":True,"raw_negative_retained":True,
        "capsule_rebuilds":0,"provider_calls":0,"root_search_complete":False,
        "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False}
    if any(x[k]!=v for x in (d,ind) for k,v in fixed.items()):
        raise ValueError("R53 scope binding")
    if (not ind["parent_bytes_preserved"] or not ind["selection_bytes_equal"] or
        not ind["raw_type_and_proof_equal"] or ind["mcp_audits"]!=69 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R53 independent evidence")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=69 or len(ma)!=69 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R53 audit binding")
    earlier={n:x for n,x in hist.items() if n not in selection["witnesses"]}
    if len(earlier)!=64 or any(hist[n]!=x for n,x in selection["witnesses"].items()):
        raise ValueError("R53 witness identity")
    candidates,decisions=prev.prev.prev.select(frontier,base.CURRENT)
    if decisions!=reference["selection_decisions"] or set(reference["records"])!=set(candidates):
        raise ValueError("R51 inventory")
    for n,c in candidates.items():
        row=reference["records"][n]
        if any(row[k]!=v for k,v in c.items()) or row["alias_observation"]!=hist[c["alias"]]:
            raise ValueError("R51 identity")
    refs,routes,decisions=prev.project(candidates,earlier,application,selection["observations"])
    if (refs!=selection["application_refs"] or routes!=selection["routes"] or decisions!=selection["decisions"] or
        prev.controls(candidates,earlier,application,selection["observations"])!=selection["controls"] or
        selection["controls"]!=d["controls"]):
        raise ValueError("R53 selection drift")
    for n,x in routes.items():
        if (hist[n]["type_expr_repr"]!=selection["observations"][x["goal"]]["goal_expr"] or
            hist[n]["universe_parameters"] or set(refs[n])-set(hist[n]["proof_constants"]) or
            hist[n]["axioms"]!=sorted(set(x["axioms"]))):
            raise ValueError("R53 route binding")
    return hist,candidates,earlier

METRIC=r'''
open Lean
namespace KuuOSR54Metric
def nodes : Expr → Nat
  | .app f a => 1 + nodes f + nodes a
  | .lam _ t b _ => 1 + nodes t + nodes b
  | .forallE _ t b _ => 1 + nodes t + nodes b
  | .letE _ t v b _ => 1 + nodes t + nodes v + nodes b
  | .mdata _ e => 1 + nodes e
  | .proj _ _ e => 1 + nodes e
  | _ => 1
end KuuOSR54Metric
'''

def replay(source,candidates,earlier,selection):
    original="\n"+prev.observer(candidates,earlier)
    if not source.endswith(original):raise ValueError("HOLD_R53_SOURCE_BOUNDARY")
    parent=source[:-len(original)]
    _,facts=prev.pool(candidates,earlier)
    tick=chr(96)*2
    commands=[prev.HELPER,METRIC]
    for n,row in sorted(selection["routes"].items()):
        label=row["goal"];short=n.rsplit(".",1)[1]
        commands.append(r'''open Lean
set_option maxHeartbeats 12000000 in
set_option Elab.async false in
run_cmd do
  let r54Env ← getEnv
  let some r54Target := r54Env.find? __R54_TARGET__ | throwError "missing target"
  let some r54Goal := r54Target.value? (allowOpaque := true) | throwError "missing goal body"
  let r54Facts : Array Name := #[__R54_FACTS__]
  let r54Trial ← Lean.Elab.Command.liftTermElabM do
    KuuOSR53Search.safeTrial __R54_RULE__ __R54_MODE__ r54Goal r54Facts
  let some r54Proof := r54Trial.proof | throwError "admitted route replay failed"
  unless r54Trial.status == "MATCH_RULE" && KuuOSR53Search.closedExpr r54Proof do
    throwError "admitted route not closed"
  let r54Name := Name.str (Name.mkSimple "KuuOSR53Selected") __R54_SHORT__
  Lean.Elab.Command.liftCoreM <| Lean.addDecl (.thmDecl {
    name := r54Name, levelParams := [], type := r54Goal, value := r54Proof })
  let r54After ← getEnv
  let some r54Info := r54After.find? r54Name | throwError "missing replay witness"
  let some r54Body := r54Info.value? (allowOpaque := true) | throwError "missing replay proof"
  unless r54Info.isTheorem && r54Info.type.equal r54Goal && r54Body.equal r54Proof do
    throwError "replay identity"
  let r54Ax ← Lean.collectAxioms r54Name
  let r54Payload := Json.mkObj [
    ("name",toJson r54Name.toString),("goal_expr",toJson (reprStr r54Goal)),
    ("proof_expr",toJson (reprStr r54Body)),("proof_nodes",toJson (KuuOSR54Metric.nodes r54Body)),
    ("premises",toJson (r54Trial.premises.map Name.toString)),("probes",toJson r54Trial.probes),
    ("axioms",toJson (r54Ax.map Name.toString)),
    ("proof_constants",toJson (r54Body.getUsedConstants.map Name.toString))]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R54_REPLAY " ++ r54Payload.compress)
'''.replace("__R54_TARGET__",tick+prev.prev.NS+"."+label+"Target")
   .replace("__R54_FACTS__",", ".join(tick+f for f in facts))
   .replace("__R54_RULE__",tick+row["rule"])
   .replace("__R54_MODE__",json.dumps(row["mode"]))
   .replace("__R54_SHORT__",json.dumps(short)))
    return parent+"\n"+"\n".join(commands)

def project(selection,hist,frontier,observations):
    routes=selection["routes"]
    if set(observations)!=set(routes) or len(routes)!=5:raise ValueError("HOLD_ROUTE_INVENTORY")
    # Keep type and value references separate. Traverse only observed value
    # edges, retaining a boundary for every reference not in this inventory.
    edges={n:set(x["proof_constants"]) for n,x in hist.items()}
    for n,x in frontier["observations"].items():
        if x["status"]=="OBSERVED" and n not in edges:
            edges[n]=set(x["value_constants"])
    def closure(n):
        seen=set();boundary=set();pending=list(edges[n])
        while pending:
            k=pending.pop()
            if k==n:raise ValueError("HOLD_ROUTE_CYCLE")
            if k in seen or k in boundary:continue
            if k not in edges:boundary.add(k);continue
            seen.add(k);pending.extend(edges[k])
        return sorted(seen),sorted(boundary)
    records={}
    for n,r in sorted(routes.items()):
        x=observations[n];h=hist[n]
        if x["name"]!=n or x["goal_expr"]!=h["type_expr_repr"] or x["goal_expr"]!=selection["observations"][r["goal"]]["goal_expr"]:
            raise ValueError("HOLD_ROUTE_CONTEXT")
        if (x["proof_expr"]!=r["proof_expr"] or x["premises"]!=r["premises"] or
            x["probes"]!=r["probes"] or sorted(set(x["axioms"]))!=h["axioms"] or
            sorted(set(x["proof_constants"]))!=h["proof_constants"]):
            raise ValueError("HOLD_ROUTE_PROOF_DRIFT")
        if type(x["proof_nodes"]) is not int or x["proof_nodes"]<=0:
            raise ValueError("HOLD_ROUTE_METRIC")
        observed,boundary=closure(n)
        records[n]={"goal":r["goal"],"rule":r["rule"],"mode":r["mode"],"premises":r["premises"],
            "historical_route_digest":old.digest(r),"proof_digest":old.digest(x["proof_expr"]),
            "goal_expr":x["goal_expr"],"proof_nodes":x["proof_nodes"],"historical_probes":r["probes"],
            "direct_constants":h["proof_constants"],"observed_dependencies":observed,
            "unobserved_boundary":boundary,"observed_dependency_count":len(observed),
            "boundary_count":len(boundary),"axioms":h["axioms"],"proof_authority":False}
    groups={}
    for goal,ds in sorted(selection["decisions"].items()):
        ns=sorted(ds["witnesses"])
        if len(ns)!=COUNTS[goal] or any(records[n]["goal"]!=goal for n in ns):
            raise ValueError("HOLD_ROUTE_CONTEXT")
        if not ns:
            groups[goal]={"status":ds["status"],"routes":[],"preferences":{}}
            continue
        common=sorted(set.intersection(*(set(records[n]["observed_dependencies"]) for n in ns)))
        boundary_common=sorted(set.intersection(*(set(records[n]["unobserved_boundary"]) for n in ns)))
        preferences={}
        for policy,fields in POLICIES.items():
            scores={n:[records[n][k] for k in fields] for n in ns}
            best=min(scores.values())
            preferences[policy]={"criteria":list(fields),"scores":scores,"preferred":sorted(n for n in ns if scores[n]==best),
                "all_routes_retained":True,"proof_authority":False}
        groups[goal]={"status":ds["status"],"routes":ns,"common_observed_dependencies":common,
            "common_unobserved_boundary":boundary_common,
            "route_specific_observed":{n:sorted(set(records[n]["observed_dependencies"])-set(common)) for n in ns},
            "preferences":preferences}
    return {"records":records,"groups":groups,"metrics":"structural_proxy_not_wall_clock",
        "bounded_value_graph":True,"all_routes_retained":True,"mathematical_independence_claimed":False,
        "proof_authority":False,"semantic_search_complete":False}

def controls(selection,hist,frontier,rows):
    out={}
    def reject(k,bad):
        try:project(selection,hist,frontier,bad)
        except ValueError as e:out[k]=str(e)
        else:raise ValueError("invalid metric accepted "+k)
    n=next(iter(sorted(rows)))
    bad=copy.deepcopy(rows);bad.pop(n);reject("missing_route",bad)
    bad=copy.deepcopy(rows);bad[n]["goal_expr"]="wrong_context";reject("wrong_context",bad)
    bad=copy.deepcopy(rows);bad[n]["proof_expr"]="changed";reject("proof_drift",bad)
    bad=copy.deepcopy(rows);bad[n]["proof_nodes"]=0;reject("invalid_metric",bad)
    if out!={"missing_route":"HOLD_ROUTE_INVENTORY","wrong_context":"HOLD_ROUTE_CONTEXT",
        "proof_drift":"HOLD_ROUTE_PROOF_DRIFT","invalid_metric":"HOLD_ROUTE_METRIC"}:
        raise ValueError("route comparison control drift")
    return out
