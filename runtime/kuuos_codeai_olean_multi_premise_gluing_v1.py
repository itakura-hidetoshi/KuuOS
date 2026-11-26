"""R18 bounded AND-OR premise search. Only closed residual Props are admitted.
A route is not a proof. Negative candidates block a route provisionally;
only independently kernel-checked exact negative witnesses certify refutation.
"""
from __future__ import annotations
import json
import sqlite3
from runtime import kuuos_codeai_olean_global_recursive_premise_v1 as prev
from runtime import kuuos_codeai_olean_polymorphic_premise_v1 as poly
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R18_SEARCH "
FUEL=3
LIMIT=24
LEC="Kuu.LivingEngi."
MODULES=[LEC+"ScopedGluing",LEC+"NativeF55CechSourceGluingObstruction",LEC+"SourceAwareOverlapDescentCriterion"]
HEADS=[LEC+x for x in ("Compatible","HasGlobal","Covers","OverlapFiberFaithful")]
NEG=[LEC+x for x in ("nativeF55_twoChart_not_overlapFiberFaithful","nativeF55_twoChart_raw_incompatible","nativeF55_twoChart_raw_no_global")]
HELPER=r'''
open Lean Meta KuuOSR16 KuuOSR17
namespace KuuOSR18
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

-- Same closed-residual discipline as R16, but with an explicitly bound
-- observer and source atlas. Never invent non-Prop arguments.
def rootTrial (c goal : Expr) : MetaM KuuOSR16.Trial := withNewMCtxDepth do
  let (args, _, conclusion) ← forallMetaTelescope (← inferType c)
  unless KuuOSR16.closed goal && (← isDefEq conclusion goal) do
    return ⟨"HOLD_ROOT_TYPE", args.size, 0, 0, #[]⟩
  let mut residual : Array Expr := #[]
  let mut inferred := 0
  for a in args do
    let a ← instantiateMVars a
    if KuuOSR16.closed a then
      inferred := inferred + 1
    else
      unless a.isMVar do
        return ⟨"HOLD_OPEN_ARGUMENT", args.size, 0, inferred, #[]⟩
      let ty ← instantiateMVars (← inferType a)
      unless KuuOSR16.closed ty && !ty.hasLevelMVar && (← isProp ty) do
        return ⟨"HOLD_DEPENDENT_RESIDUAL", args.size, 0, inferred, #[]⟩
      residual := residual.push ty
  let proof ← instantiateMVars (mkAppN c args)
  if proof.hasLevelMVar || proof.hasFVar || proof.hasLooseBVars then
    return ⟨"HOLD_OPEN_UNIVERSE_OR_CONTEXT", args.size, 0, inferred, #[]⟩
  unless ← isDefEq (← inferType proof) goal do
    return ⟨"HOLD_SPECIALIZED_TYPE", args.size, 0, inferred, #[]⟩
  return ⟨if residual.isEmpty then "MATCH_COMPLETE" else "MATCH_RESIDUAL",
    args.size, 0, inferred, residual⟩

abbrev Route := List (Name × Nat)
structure Result where
  route : Option Route
  entries : Array KuuOSR17.CacheEntry
  trace : Array Json
  hits : Nat

def negative (pools : Array (String × Array Name)) (goal : Expr)
    (entries : Array KuuOSR17.CacheEntry) :
    MetaM (Option Name × Array KuuOSR17.CacheEntry × Array Json × Nat) := do
  let some (_, rules) := pools.find? (fun p => p.1 == "Not") |
    return (none, entries, #[], 0)
  let mut cache := entries
  let mut trace : Array Json := #[]
  let mut hits := 0
  let neg := mkApp (mkConst (Name.mkSimple "Not")) goal
  for n in rules do
    let (t, next, hit) ← KuuOSR17.lookupTrial cache n neg
    cache := next
    if hit then hits := hits + 1
    trace := trace.push (Json.mkObj [
      ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.toString),
      ("status", toJson (if t.status == "MATCH_COMPLETE" then
        "HOLD_PENDING_EXACT_NEGATIVE_AUDIT" else "HOLD_NEGATIVE_TRIAL")),
      ("trial", KuuOSR16.trialJson n t)])
    if t.status == "MATCH_COMPLETE" then
      return (some n, cache, trace, hits)
  return (none, cache, trace, hits)

def walk (pools : Array (String × Array Name)) (fuel : Nat)
    (ancestors : Array Expr) (goal : Expr)
    (entries : Array KuuOSR17.CacheEntry) : MetaM Result := do
  if ancestors.any (fun e => e.equal goal) then
    return ⟨none, entries, #[KuuOSR17.holdRow "HOLD_EXACT_CYCLE" goal], 0⟩
  match fuel with
  | 0 => return ⟨none, entries, #[KuuOSR17.holdRow "HOLD_DEPTH_BUDGET" goal], 0⟩
  | remaining + 1 =>
    let (neg, initial, negTrace, negHits) ← negative pools goal entries
    if neg.isSome then
      return ⟨none, initial, negTrace, negHits⟩
    let head := if goal.getAppFn.isConst then goal.getAppFn.constName!.toString else ""
    let some (_, rules) := pools.find? (fun p => p.1 == head) |
      return ⟨none, initial, negTrace.push (KuuOSR17.holdRow "HOLD_UNRANKED_HEAD" goal), negHits⟩
    let mut cache := initial
    let mut trace := negTrace
    let mut hits := negHits
    for n in rules do
      let (trial, next, hit) ← KuuOSR17.lookupTrial cache n goal
      cache := next
      if hit then hits := hits + 1
      trace := trace.push (Json.mkObj [
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.toString),
        ("trial", KuuOSR16.trialJson n trial), ("cache_hit", toJson hit)])
      if trial.status == "MATCH_COMPLETE" then
        return ⟨some [(n, 0)], cache, trace, hits⟩
      if trial.status == "MATCH_RESIDUAL" && trial.residual.size > 0 &&
          trial.residual.size ≤ 3 then
        let mut route : Route := [(n, trial.residual.size)]
        let mut allFound := true
        for childGoal in trial.residual do
          let child ← walk pools remaining (ancestors.push goal) childGoal cache
          cache := child.entries
          trace := trace ++ child.trace
          hits := hits + child.hits
          if let some r := child.route then
            route := route ++ r
          else
            allFound := false
        if allFound then
          return ⟨some route, cache, trace, hits⟩
        trace := trace.push (KuuOSR17.holdRow "HOLD_AND_BRANCH_INCOMPLETE" goal)
    return ⟨none, cache, trace, hits⟩
termination_by fuel

def glueRoot (pools : Array (String × Array Name)) (fuel : Nat)
    (root : Name) (goal : Expr) (trial : KuuOSR16.Trial)
    (entries : Array KuuOSR17.CacheEntry) : MetaM Result := do
  let mut route : Route := [(root, trial.residual.size)]
  let mut cache := entries
  let mut trace : Array Json := #[]
  let mut hits := 0
  let mut allFound := trial.status == "MATCH_RESIDUAL" && trial.residual.size ≥ 2 &&
    trial.residual.size ≤ 3
  for childGoal in trial.residual do
    let child ← walk pools fuel #[goal] childGoal cache
    cache := child.entries
    trace := trace ++ child.trace
    hits := hits + child.hits
    if let some r := child.route then
      route := route ++ r
    else
      allFound := false
  return ⟨if allFound then some route else none, cache, trace, hits⟩

def resultJson (s : Result) : Json :=
  Json.mkObj [("route", toJson (s.route.map (List.map (fun p =>
      Json.mkObj [("rule", toJson p.1.toString), ("arity", toJson p.2)])))),
    ("trace", toJson s.trace), ("cache_entries", toJson s.entries.size),
    ("cache_hits", toJson s.hits)]
end KuuOSR18
'''

def inventory(db, historical, receipt):
    # R7 admission and digest verification are performed by the existing
    # caller; reuse R17's authenticated inventory rather than rerun R17.
    if old.digest(historical)!=receipt["inventory_digest"]:
        raise ValueError("R17 inventory drift")
    if historical["source_head"]!=old.HEAD or historical["scope_digest"]!=old.SCOPE:
        raise ValueError("R17 scope drift")
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        rows=[json.loads(x[0]) for x in con.execute(
            "SELECT row_json FROM theorem_types WHERE module IN (?,?,?) ORDER BY module,name",MODULES)]
    finally:con.close()
    pools={h:[] for h in HEADS+["Not"]};deferred=[]
    for x in rows:
        h="Not" if x["name"] in NEG else x["conclusion_head"]
        if h not in pools or x["binder_count"]>32:
            deferred.append(x["name"]);continue
        typed.name(x["module"]);typed.name(x["name"])
        pools[h].append({"module":x["module"],"name":x["name"],"row_digest":old.digest(x),
                         "binder_count":x["binder_count"],"universe_parameters":x["universe_parameters"]})
    for h,rs in pools.items():
        rs.sort(key=lambda x:(x["name"] not in NEG,x["binder_count"],x["module"],x["name"]))
        deferred.extend(x["name"] for x in rs[LIMIT:]);pools[h]=rs[:LIMIT]
    if not set(NEG)<= {x["name"] for x in pools["Not"]}:raise ValueError("indexed negative hints missing")
    return {"source_head":old.HEAD,"scope_digest":old.SCOPE,"selected":pools,
            "r17_inventory_digest":old.digest(historical),"index_rows":47705,
            "scoped_rows":len(rows),"deferred":deferred,"semantic_search_complete":False,
            "proof_authority":False}

def root_term(q,args):
    return typed.term({"apply":[{"const":q["request"]["source"]}]+args})

def render(q,args,inv):
    s=prev.render(q,inv)
    ns="KuuOSR17."+q["request"]["case_id"]
    marker="namespace "+ns+"\n"
    s=s.replace(marker,HELPER+"\n"+marker,1)
    end="end "+ns+"\n"
    s=s.replace(end,"def primaryRule := "+root_term(q,args)+"\n"+end,1)
    cut="  let payload ← Lean.Elab.Command.liftTermElabM do\n"
    if s.count(cut)!=1:raise ValueError("render boundary")
    s=s.split(cut)[0]
    tick=chr(96)*2
    s+="  let some rootInfo := env.find? "+tick+ns+".primaryRule"+' | throwError "root missing"\n'
    s+='  let some root := rootInfo.value? (allowOpaque := true) | throwError "root body missing"\n'
    s+="  let payload ← Lean.Elab.Command.liftTermElabM do\n"
    s+="    let n := "+tick+q["request"]["source"]+"\n"
    s+='''    let primary ← KuuOSR18.rootTrial root goal
    unless primary.status == "MATCH_RESIDUAL" && primary.residual.size ≥ 2 &&
        primary.residual.size ≤ 3 do
      throwError "root did not specialize to closed multi-premise goal"
    let first ← KuuOSR18.glueRoot pools 3 n goal primary #[]
    let replay ← KuuOSR18.glueRoot pools 3 n goal primary first.entries
    let child := primary.residual[0]!
    let cycle ← KuuOSR18.walk pools 3 #[child] child first.entries
    let budget ← KuuOSR18.walk pools 0 #[] child first.entries
    let (neg, _, negTrace, _) ← KuuOSR18.negative pools goal first.entries
    pure (Json.mkObj [("goal_expr", toJson (reprStr goal)),
      ("primary", KuuOSR16.trialJson n primary),
      ("first", KuuOSR18.resultJson first), ("replay", KuuOSR18.resultJson replay),
      ("cycle", KuuOSR18.resultJson cycle), ("budget", KuuOSR18.resultJson budget),
      ("exact_target_negative_candidate", toJson (neg.map Name.toString)),
      ("negative_trace", toJson negTrace)])
'''
    s+='  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)\n'
    return s

def application(q,args,route,case):
    poly.validate(q);r=q["request"]
    req=typed.make_request(case,r["module"],r["source"],r["target"],[],r["polarity"])
    if not route or route[0]["rule"]!=r["source"]:raise ValueError("root changed")
    pos=0
    def node(indent,depth):
        nonlocal pos
        if pos>=len(route) or depth>FUEL+1:raise ValueError("route tree boundary")
        entry=route[pos];pos+=1
        name=typed.name(entry["rule"]);arity=entry["arity"]
        if type(arity) is not int or not 0<=arity<=3:raise ValueError("arity")
        term=root_term(q,args) if depth==0 and args else "@"+name
        line=("apply " if arity else "exact ")+term
        lines=[line]
        for _ in range(arity):
            child=node(indent+2,depth+1)
            lines+=[" "*indent+"· "+child[0]]+child[1:]
        return lines
    lines=node(2,0)
    if pos!=len(route):raise ValueError("trailing route")
    ty="target" if r["polarity"]=="positive" else "Not target"
    marker="theorem witness : "+ty+" := @"+r["source"]
    change=typed.term(r["target"])
    if r["polarity"]=="negative":change="Not ("+change+")"
    replacement="theorem witness : "+ty+" := by\n  change "+change+"\n  "+lines[0]+"\n"+"\n".join(lines[1:])
    def transform(s):
        if s.count(marker)!=1:raise ValueError("application renderer boundary")
        return s.replace(marker,replacement,1)
    return req,transform(typed.render(req)),transform(typed.declarations(req))
