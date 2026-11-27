"""R62: bind general Lean obstruction/recovery laws and finite R61 cases.

The Lean laws concern an explicitly supplied family of dependencies. The
finite replay is a closed truth table generated from certified observations,
not a proof that those observations exhaust the repository or that the
Python implementation is universally correct.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path
from runtime import kuuos_codeai_olean_contextual_recovery_v1 as prev
base=prev.base
old=prev.old
comparison_gate=prev.comparison_gate
DIRECT="cc55f768d886673ffce24115054355c0335594a51c7c25c5666266890521b601"
MCP="53c94a2a0a017da933687d9ca950f0a16ed7e29791836e560ffe049ea26544f6"
KEY="5abe3577dd9854c2b190e727a9219484751ead421254b4ea16b0026d009bf4d2"
NS="KuuOSR62."
FORMAL_NAMES=(
    "eligible_iff_not_hits","residual_eligible_iff","two_blocked_iff_basis",
    "two_recovery_iff_break_basis","family_recovery_iff_break_complete_basis",
    "locked_common_dependency_blocks_recovery","minimal_release_is_route_intersection",
    "exists_valid_release_iff_unlocked_route","minimal_route_intersection_is_minimal_release")
TABLE_NAMES=("observed_recovery_duality_table","observed_minimal_release_table")
NAMES=tuple(NS+n for n in FORMAL_NAMES+TABLE_NAMES)
REFS={NS+n:[NS+x for x in rs] for n,rs in {
    "two_recovery_iff_break_basis":["eligible_iff_not_hits","residual_eligible_iff","two_blocked_iff_basis"],
    "family_recovery_iff_break_complete_basis":["eligible_iff_not_hits"],
    "minimal_release_is_route_intersection":["residual_eligible_iff"],
    "exists_valid_release_iff_unlocked_route":["residual_eligible_iff"],
    "minimal_route_intersection_is_minimal_release":["residual_eligible_iff"]}.items()}
MARK="KUUOS_R62_RAW "

def admit(d,mp,ind,comp,sel,pref,budget,av,edges,paths,obs,recovery):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or mp["direct_digest"]!=DIRECT or
        d["status"]!="R61_DIRECT_CONTEXTUAL_RECOVERY" or mp["status"]!="R61_REAL_MCP_GREEN" or
        ind["status"]!="R61_INDEPENDENT_CONTEXTUAL_RECOVERY_GREEN" or ind["direct_digest"]!=DIRECT or
        ind["mcp_digest"]!=MCP or not prev.valid(obs,paths,edges,av,budget,pref,comp,sel) or
        recovery.get("key")!=KEY or base.portable.seal(recovery)["key"]!=KEY or
        recovery["parent_obstruction_key"]!=obs["key"] or recovery["parent_paths_key"]!=paths["key"] or
        recovery["retained_records"]!=pref["retained_records"] or recovery["retained_groups"]!=pref["retained_groups"]):
        raise ValueError("HOLD_R61_BINDING")
    fixed={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
        "recovery_key":KEY,"parent_obstruction_key":prev.KEY,"request_count":19,"diagnostic_witnesses":2,
        "active_dispatches":0,"historical_cases_replayed":13,"enumerated_subsets":32,"candidate_count":11,
        "approval_holds":9,"locked_holds":3,"retained_routes":5,"all_routes_retained":True,
        "raw_positive_hold":True,"raw_negative_retained":True,"historical_hold_retained":True,
        "proof_authority":False,"action_authority":False,"complete_transitive_closure":False,
        "policy_is_refutation":False,"new_root_discovery_trials":0,"capsule_rebuilds":0,
        "active_policy_changed":False,"release_authorized":False,"external_approval_required":True}
    if any(x.get(k)!=v for x in (d,ind) for k,v in fixed.items()) or any(ind.get(k) is not True for k in
        ("parent_bytes_preserved","recovery_bytes_equal","raw_type_and_proof_equal")) or ind["mcp_audits"]!=99:
        raise ValueError("HOLD_R61_SCOPE")
    if any(recovery.get(k)!=fixed[k] for k in ("active_policy_changed","release_authorized",
        "external_approval_required","proof_authority","action_authority","complete_transitive_closure","policy_is_refutation")):
        raise ValueError("HOLD_R61_AUTHORITY")
    rows=d["fresh_application"]["observations"];hist={x["name"]:x for x in rows}
    if len(rows)!=99 or len(hist)!=99 or [{"name":x["name"],"axioms":x["axioms"]} for x in rows]!=mp["audits"]:
        raise ValueError("HOLD_R61_AUDIT")
    if len(recovery["diagnostic_witnesses"])!=2 or any(hist[n]!=x["observation"] or x["active_dispatch"] is not False
        for n,x in recovery["diagnostic_witnesses"].items()):
        raise ValueError("HOLD_R61_DIAGNOSTIC")
    return hist

def atom(b):return "True" if b else "False"
def fold(xs,op,empty):
    return "("+(" "+op+" ").join(xs)+")" if xs else empty
def conjunction(xs):return fold(xs,"∧","True")
def disjunction(xs):return fold(xs,"∨","False")

def truth_table(recovery,obs,paths,budget):
    rp=paths["projection"]["route_paths"]
    records=[];duality=[];minimality=[]
    for label,d in sorted(recovery["decisions"].items()):
        count=d["enumerated_subsets"]
        if count==0:
            if d["candidates"]:raise ValueError("HOLD_EMPTY_TABLE")
            continue
        q=d["request"];D=set(q["denied"]);L=set(q["locked"])
        if not L<=D or d["active_policy_changed"] or d["release_authorized"]:
            raise ValueError("HOLD_TABLE_AUTHORITY")
        ns=budget["decisions"][q["case"]]["eligible"]
        if not ns:raise ValueError("HOLD_TABLE_SCOPE")
        hits={n:sorted(D&set(rp[n])) for n in ns}
        cuts=[c["denied"] for c in obs["groups"][q["case"]]["cuts"] if set(c["denied"])<=D]
        if not cuts or any(not v for v in hits.values()):raise ValueError("HOLD_TABLE_ORIGINAL")
        def route_formula(R):
            return disjunction([conjunction([atom(k in R) for k in hits[n]]) for n in sorted(ns)])
        def basis_formula(R):
            return conjunction([disjunction([atom(k in R) for k in c]) for c in cuts])
        def rec(R):return any(set(hits[n])<=R for n in ns)
        domain=sorted(D-L);candidate_sets={tuple(x["release"]) for x in d["candidates"]};found=set()
        seen=0
        for size in range(len(domain)+1):
            for xs in combinations(domain,size):
                R=set(xs);seen+=1
                restore=rec(R);by_basis=all(R&set(c) for c in cuts)
                is_min=restore and not any(rec(R-{k}) for k in R)
                if restore!=by_basis or is_min!=(xs in candidate_sets):
                    raise ValueError("HOLD_TABLE_DUALITY")
                if is_min:found.add(xs)
                f=route_formula(R);g=basis_formula(R)
                h=conjunction([f]+["(¬ "+route_formula(R-{k})+")" for k in sorted(R)])
                duality.append("(("+f+" ↔ "+atom(restore)+") ∧ ("+g+" ↔ "+atom(restore)+"))")
                minimality.append("("+h+" ↔ "+atom(is_min)+")")
                records.append({"label":label,"request_id":d["request_id"],"denied":sorted(D),"locked":sorted(L),
                    "release":list(xs),"denied_dependencies_by_route":hits,"contained_cuts":cuts,
                    "restores":restore,"inclusion_minimal":is_min,"route_formula":f,"basis_formula":g,
                    "minimality_formula":h,"action_authority":False})
        if seen!=count or found!=candidate_sets:raise ValueError("HOLD_TABLE_COUNT")
    if len(records)!=32 or sum(x["inclusion_minimal"] for x in records)!=11:
        raise ValueError("HOLD_TABLE_INVENTORY")
    code="\nnamespace KuuOSR62\n"
    for n,formulas in zip(TABLE_NAMES,(duality,minimality)):
        code+="set_option maxRecDepth 4096 in\nset_option maxHeartbeats 12000000 in\n"
        code+="theorem "+n+" :\n  "+" ∧\n  ".join(formulas)+" := by\n  decide\n\n"
    return records,code+"end KuuOSR62\n"

def raw_observer():
    names=", ".join(chr(96)*2+n for n in NAMES)
    return r'''open Lean
set_option maxHeartbeats 12000000 in
run_cmd do
  let env ← getEnv
  let ns : Array Name := #[__NAMES__]
  for n in ns do
    let some info := env.find? n | throwError "R62 theorem missing"
    unless info.isTheorem do throwError "R62 not a theorem"
    let some proof := info.value? (allowOpaque := true) | throwError "R62 proof unavailable"
    let ax ← Lean.collectAxioms n
    let payload := Lean.Json.mkObj [
      ("name", Lean.toJson n.toString),
      ("type_expr", Lean.toJson (reprStr info.type)),
      ("proof_expr", Lean.toJson (reprStr proof)),
      ("axioms", Lean.toJson (ax.map Name.toString)),
      ("universe_parameters", Lean.toJson (info.levelParams.map Name.toString))]
    Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R62_RAW " ++ payload.compress)
'''.replace("__NAMES__",names)

def raw_audit(log,by):
    rows=[json.loads(x[len(MARK):]) for x in log.splitlines() if x.startswith(MARK)]
    result={x["name"]:x for x in rows}
    if len(rows)!=len(NAMES) or set(result)!=set(NAMES):
        raise ValueError("HOLD_R62_RAW_INVENTORY")
    for n,x in result.items():
        if (x["type_expr"]!=by[n]["type_expr_repr"] or not x["proof_expr"] or "sorryAx" in x["proof_expr"] or
            sorted(set(x["axioms"]))!=by[n]["axioms"] or x["universe_parameters"]!=by[n]["universe_parameters"] or
            set(x["axioms"])-{"propext","Classical.choice","Quot.sound"}):
            raise ValueError("HOLD_R62_RAW_PROOF")
    return result
