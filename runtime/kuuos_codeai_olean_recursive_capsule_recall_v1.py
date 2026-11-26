"""R26: recall an admitted exact capsule or negative witness at each closed
residual in the R20/R18 AND-OR search. No-match continues the bounded search.
The new hook is a candidate selector; all successful routes must be checked
by Lean and audited independently. No root/global authority is inferred."""
from __future__ import annotations
from runtime import kuuos_codeai_olean_root_discovery_v1_r2 as root
from runtime import kuuos_codeai_olean_capsule_typed_lookup_v1 as lookup
from runtime import kuuos_codeai_olean_general_application_v1 as typed

MARK="KUUOS_R26_BRANCHES "

def hook(inv):
    p,n=inv["candidates"]
    if p["polarity"]!="positive" or n["polarity"]!="negative":
        raise ValueError("inventory polarity")
    tick=chr(96)*2
    return r'''
  if KuuOSR16.closed goal && !goal.hasLevelMVar then
    let p ← getConstInfo POS
    let n ← getConstInfo NEG
    let (yes, no) ← withNewMCtxDepth do
      let a ← withNewMCtxDepth <| isDefEq p.type goal
      let b ← withNewMCtxDepth <| isDefEq n.type (mkApp (mkConst NOT) goal)
      pure (a,b)
    if yes && no then
      return ⟨none, entries, #[KuuOSR17.holdRow "HOLD_CONFLICTING_CAPSULES" goal], 0⟩
    if no then
      return ⟨none, entries, #[Json.mkObj [
        ("status", toJson "HOLD_ROUTE_EXACT_NEGATIVE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson n.name.toString)]], 0⟩
    if yes then
      return ⟨some [(p.name, 0)], entries, #[Json.mkObj [
        ("status", toJson "CAPSULE_EXACT_LEAF_CANDIDATE"),
        ("goal_expr", toJson (reprStr goal)), ("rule", toJson p.name.toString),
        ("structural_equal", toJson (p.type.equal goal))]], 0⟩
'''.replace("POS",tick+typed.name(p["name"])).replace("NEG",tick+typed.name(n["name"])).replace("NOT",tick+"Not")

def helpers(inv):
    marker="  if ancestors.any (fun e => e.equal goal) then"
    s=root.base.HELPER
    if s.count(marker)!=1:raise ValueError("R18 walk boundary")
    return s.replace(marker,hook(inv)+marker,1)

def render(q,inv,capsules):
    root.validate(q)
    s=root.render(q,inv)
    marker=root.base.HELPER
    if s.count(marker)!=1:raise ValueError("R20 helper boundary")
    mods={typed.name(x["module"]) for x in capsules["candidates"]}
    imports="".join("import "+m+"\n" for m in sorted(mods) if "import "+m+"\n" not in s)
    return imports+s.replace(marker,helpers(capsules),1)

def fixture(qs,inv):
    # Separate logical OR control. The leaves are the actual R25 C60-derived
    # propositions, while the two root rules are ordinary logical controls.
    t=lambda k:typed.term(qs[k]["target"])
    p,n=inv["candidates"]
    imports="".join("import "+m+"\n" for m in sorted({p["module"],n["module"]}))
    pre=imports+"\n"+root.poly.HELPER+"\n"+root.base.prev.HELPER+"\n"+helpers(inv)
    pre+="\nnamespace KuuOSR26Fixture\nset_option autoImplicit false\nset_option maxHeartbeats 16000000\n"
    pre+=r'''
theorem leftRule (a b c d : Prop) (ha : a) (hb : b) : (a ∧ b) ∨ (c ∧ d) :=
  Or.inl ⟨ha,hb⟩
theorem rightRule (a b c d : Prop) (hc : c) (hd : d) : (a ∧ b) ∨ (c ∧ d) :=
  Or.inr ⟨hc,hd⟩
'''
    pre+="def goal : Prop := ("+t("negative_defeq")+" ∧ "+t("exact_new")+") ∨ ("+t("defeq_new")+" ∧ "+t("exact_new")+")\n"
    pre+="def unknown : Prop := "+t("wrong_atlas")+"\nend KuuOSR26Fixture\n"
    tick=chr(96)*2
    pre+=r'''
open Lean Meta
run_cmd do
  let env ← getEnv
  let some g := env.find? TICKKuuOSR26Fixture.goal | throwError "missing goal"
  let some goal := g.value? (allowOpaque := true) | throwError "missing goal body"
  let some u := env.find? TICKKuuOSR26Fixture.unknown | throwError "missing unknown"
  let some unknown := u.value? (allowOpaque := true) | throwError "missing unknown body"
  let payload ← Lean.Elab.Command.liftTermElabM do
    let left := TICKKuuOSR26Fixture.leftRule
    let right := TICKKuuOSR26Fixture.rightRule
    let l ← KuuOSR16.safeSpecialize left goal
    let r ← KuuOSR16.safeSpecialize right goal
    unless l.status == "MATCH_RESIDUAL" && r.status == "MATCH_RESIDUAL" &&
        l.residual.size == 2 && r.residual.size == 2 do
      throwError "unexpected OR control residuals"
    let a ← KuuOSR18.glueRoot #[] #[] #[] 3 left goal l #[]
    let b ← KuuOSR18.glueRoot #[] #[] #[] 3 right goal r a.entries
    let h ← KuuOSR18.walk #[] #[] #[] 3 #[] unknown #[]
    pure (Json.mkObj [
      ("left_trial", KuuOSR16.trialJson left l),
      ("right_trial", KuuOSR16.trialJson right r),
      ("left", KuuOSR18.resultJson a), ("right", KuuOSR18.resultJson b),
      ("unknown", KuuOSR18.resultJson h)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R26_BRANCHES " ++ payload.compress)
'''.replace("TICK",tick)
    return pre

def fixture_application(qs,inv):
    # Compile the alternative root and the exact negative premise separately;
    # the negative theorem never appears in the positive route.
    t=lambda k:typed.term(qs[k]["target"])
    p,n=inv["candidates"]
    a,b,c,d=(t(k) for k in ("negative_defeq","exact_new","defeq_new","exact_new"))
    body="namespace KuuOSR26Proof\nset_option autoImplicit false\n"
    body+="theorem alternative : ("+a+" ∧ "+b+") ∨ ("+c+" ∧ "+d+") := Or.inr ⟨@"+p["name"]+", @"+p["name"]+"⟩\n"
    body+="theorem negativeLeaf : Not ("+a+") := @"+n["name"]+"\n"
    body+="theorem exactLeaf : "+b+" := @"+p["name"]+"\n"
    body+="theorem defeqLeaf : "+c+" := @"+p["name"]+"\nend KuuOSR26Proof\n"
    return body
