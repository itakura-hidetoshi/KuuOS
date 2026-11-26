"""R16 bounded universe/argument specialization and two-step premise search.

A successful unification is not a proof receipt. Open non-Prop arguments,
dependent residuals, mismatches and resource failures remain HOLD.
Only explicitly audited final closed applications may be admitted.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
import json
import sqlite3

MARK="KUUOS_R16_SPECIALIZE "
HELPER=r'''
open Lean Meta
namespace KuuOSR16
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

structure Trial where
  status : String
  binders : Nat
  universes : Nat
  inferred : Nat
  residual : Array Expr

def closed (e : Expr) : Bool :=
  !e.hasMVar && !e.hasFVar && !e.hasLooseBVars

def specialize (n : Name) (goal : Expr) : MetaM Trial := withNewMCtxDepth do
  let info ← getConstInfo n
  let us := info.levelParams.length
  unless info.isTheorem && closed goal do
    return ⟨"HOLD_INVALID_INPUT", 0, us, 0, #[]⟩
  let c ← mkConstWithFreshMVarLevels n
  let (args, _, conclusion) ← forallMetaTelescope (← inferType c)
  let size := args.size
  unless ← isDefEq conclusion goal do
    return ⟨"HOLD_NOT_DEFEQ", size, us, 0, #[]⟩
  let mut inferred := 0
  let mut residual : Array Expr := #[]
  for a in args do
    let a ← instantiateMVars a
    if closed a then
      inferred := inferred + 1
    else
      unless a.isMVar do
        return ⟨"HOLD_OPEN_ARGUMENT", size, us, inferred, #[]⟩
      let ty ← instantiateMVars (← inferType a)
      unless closed ty do
        return ⟨"HOLD_DEPENDENT_RESIDUAL", size, us, inferred, #[]⟩
      unless ← isProp ty do
        return ⟨"HOLD_OPEN_NONPROP", size, us, inferred, #[]⟩
      residual := residual.push ty
  let proof ← instantiateMVars (mkAppN c args)
  if proof.hasLevelMVar || proof.hasFVar || proof.hasLooseBVars then
    return ⟨"HOLD_OPEN_UNIVERSE_OR_CONTEXT", size, us, inferred, #[]⟩
  unless ← isDefEq (← inferType proof) goal do
    return ⟨"HOLD_SPECIALIZED_TYPE", size, us, inferred, #[]⟩
  if residual.isEmpty then
    unless closed proof do
      return ⟨"HOLD_OPEN_PROOF", size, us, inferred, #[]⟩
    return ⟨"MATCH_COMPLETE", size, us, inferred, #[]⟩
  return ⟨"MATCH_RESIDUAL", size, us, inferred, residual⟩

def trialJson (n : Name) (t : Trial) : Json :=
  Json.mkObj [
    ("name", toJson n.toString), ("status", toJson t.status),
    ("binders", toJson t.binders), ("universe_parameters", toJson t.universes),
    ("inferred", toJson t.inferred),
    ("residuals", toJson (t.residual.map reprStr)),
    ("heads", toJson (t.residual.map fun e =>
      if e.getAppFn.isConst then e.getAppFn.constName!.toString else ""))]

def safeSpecialize (n : Name) (goal : Expr) : MetaM Trial := do
  try specialize n goal
  catch _ => pure ⟨"HOLD_COMPARISON_FAILURE", 0, 0, 0, #[]⟩
end KuuOSR16
'''

def make_query(case,module,source,target,polarity,context_modules,secondary_modules):
    req=typed.make_request(case,module,source,target,[],polarity)
    for ms in (context_modules,secondary_modules):
        if not isinstance(ms,list) or len(ms)>8 or len(ms)!=len(set(ms)):
            raise ValueError("module scope")
        for m in ms:typed.name(m)
    q={"request":req,"context_modules":context_modules,"secondary_modules":secondary_modules}
    return {**q,"query_digest":old.digest(q)}

def validate(q):
    req=q["request"];typed.validate(req)
    if q!=make_query(req["case_id"],req["module"],req["source"],req["target"],
                     req["polarity"],q["context_modules"],q["secondary_modules"]):
        raise ValueError("query changed")

def candidates(db,q,head):
    validate(q)
    # Caller has already admitted and hashed R7 using its existing gate.
    con=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        rows=[json.loads(x[0]) for x in con.execute(
              "SELECT row_json FROM theorem_types ORDER BY module,name")]
    finally:con.close()
    if len(rows)!=47705:raise ValueError("index inventory")
    eligible=[];excluded=[]
    for x in rows:
        if x["module"] not in q["secondary_modules"]:continue
        row={"module":x["module"],"name":x["name"],"row_digest":old.digest(x),
             "binder_count":x["binder_count"],"universe_parameters":x["universe_parameters"]}
        if not (x["binder_count"] or x["universe_parameters"]):
            excluded.append({**row,"reason":"CLOSED_MONOMORPHIC"});continue
        if x["conclusion_head"]!=head or x["binder_count"]>32:
            excluded.append({**row,"reason":"DEFERRED_BY_HEAD_OR_BINDER_BUDGET"});continue
        try:typed.name(x["name"])
        except ValueError:
            excluded.append({**row,"reason":"UNSUPPORTED_IDENTIFIER"});continue
        eligible.append(row)
    if len(eligible)>8:raise ValueError("bounded candidate scope exceeded")
    return {"query_digest":q["query_digest"],"selected":eligible,"deferred":excluded,
            "index_rows":len(rows),"semantic_search_complete":False,"proof_authority":False}

def render(q,secondary=(),leaves=()):
    validate(q);req=q["request"];typed.validate(req)
    mods=sorted(set([req["module"]]+q["context_modules"]+
                    [p["module"] for p in list(secondary)+list(leaves)]))
    for m in mods:typed.name(m)
    for p in list(secondary)+list(leaves):typed.name(p["name"])
    ns="KuuOSR16."+req["case_id"]
    target=typed.term(req["target"])
    if req["polarity"]=="negative":target="Not ("+target+")"
    tick=chr(96)*2
    names=lambda ps:", ".join(tick+p["name"] for p in ps)
    out=["import "+m for m in mods]+["",HELPER,"namespace "+ns,
         "set_option autoImplicit false","set_option maxRecDepth 8192","set_option maxHeartbeats 4000000",
         "def goal : Prop := "+target,"end "+ns,"","open Lean Meta KuuOSR16",
         "run_cmd do","  let env ← getEnv",
         "  let some info := env.find? "+tick+ns+".goal"+' | throwError "missing goal"',
         '  let some goal := info.value? (allowOpaque := true) | throwError "missing goal body"',
         '  unless closed goal do throwError "open goal"',
         "  let payload ← Lean.Elab.Command.liftTermElabM do",
         "    let primaryName := "+tick+req["source"],
         "    let primary ← safeSpecialize primaryName goal",
         "    let mut branches : Array Json := #[]",
         '    if primary.status == "MATCH_RESIDUAL" && primary.residual.size == 1 then',
         "      let secondNames : Array Name := #["+names(secondary)+"]",
         "      let leafNames : Array Name := #["+names(leaves)+"]",
         "      for secondName in secondNames do",
         "        let second ← safeSpecialize secondName primary.residual[0]!",
         "        let mut leafRows : Array Json := #[]",
         '        if second.status == "MATCH_RESIDUAL" && second.residual.size == 1 then',
         "          for leafName in leafNames do",
         "            let leaf ← safeSpecialize leafName second.residual[0]!",
         "            leafRows := leafRows.push (trialJson leafName leaf)",
         '        branches := branches.push (Json.mkObj [("secondary", trialJson secondName second),',
         '          ("leaves", toJson leafRows)])',
         '    pure (Json.mkObj [("goal_expr", toJson (reprStr goal)),',
         '      ("primary", trialJson primaryName primary), ("branches", toJson branches)])',
         '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return "\n".join(out)

def application(q,secondary,leaf,case):
    validate(q);r=q["request"]
    req=typed.make_request(case,r["module"],r["source"],r["target"],[],r["polarity"])
    for p in (secondary,leaf):typed.name(p["module"]);typed.name(p["name"])
    mods=sorted(set([r["module"]]+q["context_modules"]+[secondary["module"],leaf["module"]]))
    prefix="import "+r["module"]+"\n"
    ty="target" if r["polarity"]=="positive" else "Not target"
    marker="theorem witness : "+ty+" := @"+r["source"]
    change=typed.term(r["target"])
    if r["polarity"]=="negative":change="Not ("+change+")"
    replacement="theorem witness : "+ty+" := by\n  change "+change+"\n  apply @"+r["source"]+"\n  apply @"+secondary["name"]+"\n  exact @"+leaf["name"]
    def transform(s):
        if not s.startswith(prefix) or s.count(marker)!=1:
            raise ValueError("application renderer boundary changed")
        return "".join("import "+m+"\n" for m in mods)+s[len(prefix):].replace(marker,replacement)
    return req,transform(typed.render(req)),transform(typed.declarations(req))
