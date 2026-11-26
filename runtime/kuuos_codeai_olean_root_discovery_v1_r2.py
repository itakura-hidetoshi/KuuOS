"""R20: root discovery from an admitted global structural inventory.
The request has no theorem name. A closed seven-argument context is explicit;
only a root with two or three closed residual propositions is eligible in this
conditional-derivation mode. Closed roots are deferred, not disproved.
"""
from __future__ import annotations
import copy
import json
import re
from runtime import kuuos_codeai_olean_global_multi_premise_gluing_v1 as prev
from runtime import kuuos_codeai_olean_multi_premise_gluing_v1_r2 as base
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

poly=base.poly
LEC=base.LEC
MARK="KUUOS_R20_R2_ROOT_DISCOVERY "
HELPER=r'''
open Lean Meta KuuOSR16 KuuOSR17 KuuOSR18
namespace KuuOSR20
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000

def prefixTrial (n : Name) (ctxArgs : Array Expr) (goal : Expr) :
    MetaM KuuOSR16.Trial := withNewMCtxDepth do
  let info ← getConstInfo n
  let us := info.levelParams.length
  unless info.isTheorem && KuuOSR16.closed goal &&
      ctxArgs.all (fun e => KuuOSR16.closed e && !e.hasLevelMVar) do
    return ⟨"HOLD_INVALID_INPUT", 0, us, 0, #[]⟩
  let c ← mkConstWithFreshMVarLevels n
  let (args, _, _) ← forallMetaTelescope (← inferType c)
  unless args.size ≥ ctxArgs.size do
    return ⟨"HOLD_ROOT_PREFIX_ARITY", args.size, us, 0, #[]⟩
  for i in [:ctxArgs.size] do
    let a := args[i]!
    let p := ctxArgs[i]!
    unless ← isDefEq (← inferType a) (← inferType p) do
      return ⟨"HOLD_ROOT_PREFIX_TYPE", args.size, us, i, #[]⟩
    unless ← isDefEq a p do
      return ⟨"HOLD_ROOT_PREFIX_VALUE", args.size, us, i, #[]⟩
  let specialized ← instantiateMVars (mkAppN c (args.extract 0 ctxArgs.size))
  unless KuuOSR16.closed specialized && !specialized.hasLevelMVar do
    return ⟨"HOLD_ROOT_PREFIX_OPEN", args.size, us, ctxArgs.size, #[]⟩
  KuuOSR18.rootTrial specialized goal

def safePrefix (n : Name) (ctxArgs : Array Expr) (goal : Expr) :
    MetaM KuuOSR16.Trial := do
  try prefixTrial n ctxArgs goal
  catch _ => pure ⟨"HOLD_ROOT_COMPARISON_FAILURE", 0, 0, 0, #[]⟩

def discover (pools : Array (String × Array Name))
    (bound : Array (Name × Expr)) (closedRecall : Array Name)
    (ctxArgs : Array Expr) (goal : Expr) : MetaM Json := do
  let head := if goal.getAppFn.isConst then goal.getAppFn.constName!.toString else ""
  let rootNames := ((pools.find? (fun p => p.1 == head)).map Prod.snd).getD #[]
  let (neg, cache, negTrace, _) ← KuuOSR18.negative pools goal #[]
  let mut rootTrials : Array Json := #[]
  let mut successes : Array Json := #[]
  let mut chosen : Option KuuOSR18.Route := none
  let mut chosenTrial : Option Json := none
  for n in rootNames do
    let trial ← safePrefix n ctxArgs goal
    let eligible := trial.status == "MATCH_RESIDUAL" &&
      trial.residual.size ≥ 2 && trial.residual.size ≤ 3
    rootTrials := rootTrials.push (Json.mkObj [
      ("rule", toJson n.toString), ("trial", KuuOSR16.trialJson n trial),
      ("eligible", toJson eligible)])
    if eligible && neg.isNone then
      let first ← KuuOSR18.glueRoot pools bound closedRecall 3 n goal trial cache
      let replay ← KuuOSR18.glueRoot pools bound closedRecall 3 n goal trial first.entries
      let child := trial.residual[0]!
      let cycle ← KuuOSR18.walk pools bound #[] 3 #[child] child first.entries
      let budget ← KuuOSR18.walk pools bound #[] 0 #[] child first.entries
      successes := successes.push (Json.mkObj [
        ("rule", toJson n.toString), ("primary", KuuOSR16.trialJson n trial),
        ("first", KuuOSR18.resultJson first), ("replay", KuuOSR18.resultJson replay),
        ("cycle", KuuOSR18.resultJson cycle), ("budget", KuuOSR18.resultJson budget)])
      if chosen.isNone && first.route.isSome then
        chosen := first.route
        chosenTrial := some (KuuOSR16.trialJson n trial)
  pure (Json.mkObj [
    ("goal_expr", toJson (reprStr goal)), ("root_head", toJson head),
    ("root_trials", toJson rootTrials), ("branches", toJson successes),
    ("chosen", KuuOSR18.resultJson ⟨chosen, #[], #[], 0⟩),
    ("chosen_primary", toJson chosenTrial),
    ("exact_target_negative_candidate", toJson (neg.map Name.toString)),
    ("negative_trace", toJson negTrace)])
end KuuOSR20
'''

def make_request(case,target,args,context_modules):
    if not isinstance(case,str) or not typed.CASE.fullmatch(case):
        raise ValueError("case id")
    if not isinstance(args,list) or len(args)!=7:
        raise ValueError("explicit seven-argument source context required")
    budget=[256];typed.term(target,budget=budget)
    for x in args:typed.term(x,budget=budget)
    if not isinstance(context_modules,list) or len(context_modules)>8 or len(set(context_modules))!=len(context_modules):
        raise ValueError("module context")
    for m in context_modules:typed.name(m)
    q={"schema":"kuuos.codeai.root-discovery-request.v1","case_id":case,
       "target":target,"context_args":args,"context_modules":context_modules,
       "source_head":old.HEAD,"scope_digest":old.SCOPE,"mode":"MULTI_PREMISE_ONLY"}
    return {**q,"request_digest":old.digest(q)}

def validate(q):
    if q!=make_request(q["case_id"],q["target"],q["context_args"],q["context_modules"]):
        raise ValueError("root request binding changed")

def inventory(historical,prior):
    if old.digest(historical)!=prior["inventory_digest"] or prior["source_head"]!=old.HEAD or prior["source_tree"]!=old.TREE or prior["scope_digest"]!=old.SCOPE:
        raise ValueError("R19 inventory or proof scope drift")
    inv=copy.deepcopy(historical)
    if inv["index_rows"]!=47705 or len(inv["unobserved_modules"])!=695:
        raise ValueError("R19 coverage drift")
    obs={x["name"]:x for x in prior["fresh_application"]["observations"]}
    admitted={}
    for k,m in prior["materials"].items():
        n=m["name"]
        if k!=m["module"]+"::"+n or n not in obs or obs[n]["type_expr_sha256"]!=m["type_expr_sha256"] or set(obs[n]["axioms"])-typed.STANDARD:
            raise ValueError("R19 audited material changed")
        admitted[n]=m
    recalled=set(inv["closed_recall"])
    for h,ps in inv["selected"].items():
        if h=="Not":continue
        for p in ps:
            if p["binder_count"]==0 and p["name"] in admitted and admitted[p["name"]]["module"]==p["module"]:
                recalled.add(p["name"])
    inv["closed_recall"]=sorted(recalled)
    inv["r19_inventory_digest"]=old.digest(historical)
    return inv

def render(q,inv):
    validate(q)
    args=q["context_args"];tick=chr(96)*2
    flat=[p for ps in inv["selected"].values() for p in ps]
    mods=sorted(set(q["context_modules"]+[p["module"] for p in flat]))
    for m in mods:typed.name(m)
    for p in flat:typed.name(p["name"])
    entries=", ".join('("'+p["module"]+'", '+tick+p["name"]+')' for p in flat)
    pools=", ".join('("'+h+'", #['+", ".join(tick+p["name"] for p in ps)+'])' for h,ps in inv["selected"].items())
    for h in inv["selected"]:typed.name(h)
    ns="KuuOSR20."+q["case_id"]
    out=["import "+m for m in mods]+["",poly.HELPER,base.prev.HELPER,base.HELPER,HELPER,
        "namespace "+ns,"set_option autoImplicit false","set_option maxRecDepth 8192","set_option maxHeartbeats 16000000",
        "def goal : Prop := "+typed.term(q["target"])]
    out += ["noncomputable def ctx"+str(i)+" := "+typed.term(a) for i,a in enumerate(args)]
    bindings=base.bound_names(inv)
    out += ["def boundRule"+str(i)+" := "+base.bound_term(n,args) for i,n in enumerate(bindings)]
    out += ["end "+ns,"open Lean Meta KuuOSR20","run_cmd do","  let env ← getEnv",
        "  let some info := env.find? "+tick+ns+'.goal | throwError "missing goal"',
        '  let some goal := info.value? (allowOpaque := true) | throwError "missing goal body"',
        "  let candidates : Array (String × Name) := #["+entries+"]",
        "  for (moduleName, n) in candidates do",
        '    let some candidate := env.find? n | throwError "indexed theorem missing"',
        '    let some idx := env.getModuleIdxFor? n | throwError "indexed origin missing"',
        '    unless candidate.isTheorem && env.allImportedModuleNames[idx]!.toString == moduleName do',
        '      throwError "indexed theorem origin changed"',
        "  let pools : Array (String × Array Name) := #["+pools+"]"]
    for i in range(len(args)):
        out += ["  let some c"+str(i)+" := env.find? "+tick+ns+".ctx"+str(i)+' | throwError "missing context"',
                "  let some p"+str(i)+" := c"+str(i)+'.value? (allowOpaque := true) | throwError "missing context body"']
    out += ["  let ctxArgs : Array Expr := #["+ ", ".join("p"+str(i) for i in range(len(args)))+"]"]
    for i,n in enumerate(bindings):
        out += ["  let some b"+str(i)+" := env.find? "+tick+ns+".boundRule"+str(i)+' | throwError "bound rule missing"',
                "  let some e"+str(i)+" := b"+str(i)+'.value? (allowOpaque := true) | throwError "bound rule body missing"']
    out += ["  let bound : Array (Name × Expr) := #["+ ", ".join("("+tick+n+", e"+str(i)+")" for i,n in enumerate(bindings))+"]"]
    recall=[typed.name(n) for n in inv["closed_recall"]]
    out += ["  let closedRecall : Array Name := #["+ ", ".join(tick+n for n in recall)+"]",
            "  let payload ← Lean.Elab.Command.liftTermElabM do",
            "    KuuOSR20.discover pools bound closedRecall ctxArgs goal",
            '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return "\n".join(out)

def application(q,inv,route,case):
    validate(q)
    if not route:raise ValueError("root discovery found no route")
    n=route[0]["rule"]
    matches=[p for ps in inv["selected"].values() for p in ps if p["name"]==n]
    if len(matches)!=1 or route[0]["arity"] not in (2,3):
        raise ValueError("root candidate outside admitted pool")
    p=matches[0]
    fixed=poly.make_query(q["case_id"],p["module"],n,q["target"],"positive",q["context_modules"],[])
    return base.application(fixed,q["context_args"],route,case)
