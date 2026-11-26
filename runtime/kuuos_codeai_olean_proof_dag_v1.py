"""R21: reuse a certified closed terminal in a proof DAG.
No new search is needed for an admitted R20 route. Only repeated nullary,
universe-closed theorem constants with audited exact types may be shared.
The final kernel proof must contain one explicit local binding and all uses.
"""
from __future__ import annotations
from collections import Counter
import re
from runtime import kuuos_codeai_olean_root_discovery_v1_r2 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R21_DAG "
HELPER=r'''
open Lean Meta
namespace KuuOSR21
def countConst (n : Name) : Expr → Nat
  | .const m _ => if n == m then 1 else 0
  | .app f a => countConst n f + countConst n a
  | .lam _ t b _ => countConst n t + countConst n b
  | .forallE _ t b _ => countConst n t + countConst n b
  | .letE _ t v b _ => countConst n t + countConst n v + countConst n b
  | .mdata _ e => countConst n e
  | .proj _ _ e => countConst n e
  | _ => 0

def countBound (d : Nat) : Expr → Nat
  | .bvar k => if k == d then 1 else 0
  | .app f a => countBound d f + countBound d a
  | .lam _ t b _ => countBound d t + countBound (d+1) b
  | .forallE _ t b _ => countBound d t + countBound (d+1) b
  | .letE _ t v b _ => countBound d t + countBound d v + countBound (d+1) b
  | .mdata _ e => countBound d e
  | .proj _ _ e => countBound d e
  | _ => 0

def sharedBindings (n : Name) : Expr → List Nat
  | .app f a => sharedBindings n f ++ sharedBindings n a
  | .lam _ t b _ => sharedBindings n t ++ sharedBindings n b
  | .forallE _ t b _ => sharedBindings n t ++ sharedBindings n b
  | .letE _ t v b _ =>
    (if v.isConstOf n then [countBound 0 b] else []) ++
      sharedBindings n t ++ sharedBindings n v ++ sharedBindings n b
  | .mdata _ e => sharedBindings n e
  | .proj _ _ e => sharedBindings n e
  | _ => []
end KuuOSR21
'''

def plan(q, inv, prior, case):
    prev.validate(q)
    if (old.digest(inv)!=prior["inventory_digest"] or prior["source_head"]!=old.HEAD or
        prior["source_tree"]!=old.TREE or prior["scope_digest"]!=old.SCOPE):
        raise ValueError("R20 proof scope or inventory changed")
    if q!=prior["requests"].get(case) or q["case_id"]!=case:
        return {"status":"HOLD_REQUEST_CONTEXT_CHANGED","shared":[]}
    a=prior["applications"].get(case)
    if a is None:
        return {"status":"HOLD_NO_ADMITTED_ROUTE","shared":[]}
    route=a["route"]
    if (route!=prior["results"][case]["chosen"]["route"] or
        not a["application"]["exact_kernel_type_match"] or
        a["target_expr_repr"]!=a["application"]["target_expr_repr"] or
        a["request"]["target"]!=q["target"]):
        raise ValueError("R20 application provenance")
    counts=Counter(x["rule"] for x in route if x["arity"]==0)
    selected={p["name"]:p for ps in inv["selected"].values() for p in ps}
    observed={x["name"]:x for x in prior["fresh_application"]["observations"]}
    shared=[]
    for name,uses in sorted(counts.items()):
        if uses<2:continue
        p=selected[name]
        key=p["module"]+"::"+name
        m=prior["materials"].get(key)
        o=observed.get(name)
        if not m or not o:continue
        if (p["binder_count"]!=0 or p["universe_parameters"] or
            o["universe_parameters"] or o["type_expr_sha256"]!=m["type_expr_sha256"] or
            set(o["axioms"])-typed.STANDARD or name not in a["source_refs"]):
            continue
        item={"module":p["module"],"name":name,"type_expr_sha256":m["type_expr_sha256"],
              "source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
              "request_digest":q["request_digest"],"uses":uses}
        shared.append({**item,"key":old.digest(item)})
    return {"status":"DAG_CANDIDATE" if shared else "HOLD_NO_SHARED_CLOSED_LEAF",
            "request_digest":q["request_digest"],"route":route,"shared":shared,
            "proof_authority":False}

def application(q,inv,prior,case,wrong):
    p=plan(q,inv,prior,case)
    if p["status"]!="DAG_CANDIDATE" or len(p["shared"])!=1:
        raise ValueError("bounded shared-leaf fixture")
    leaf=p["shared"][0];name=typed.name(leaf["name"])
    prev.validate(wrong)
    req,src,mcp=prev.application(q,inv,p["route"],"r21_"+case)
    marker="theorem witness : target := by\n"
    end="\nend "+typed.NS+"."+req["case_id"]
    pattern=r"(?m)(^ *·? *)apply @"+re.escape(name)+r"$"
    def transform(s):
        if s.count(marker)!=1:raise ValueError("witness boundary")
        begin,tail=s.split(marker,1)
        if tail.count(end)!=1:raise ValueError("end boundary")
        body,after=tail.split(end,1)
        body,n=re.subn(pattern,lambda m:m.group(1)+"exact shared0",body)
        if n!=leaf["uses"]:raise ValueError("unexpected leaf occurrence count")
        body="\n".join("  "+line for line in body.splitlines())
        return (begin+"theorem witness : target :=\n  let shared0 := @"+name+
                "\n  by\n"+body+end+after)
    src,mcp=transform(src),transform(mcp)
    target,witness=typed.names(req)
    wrong_name="KuuOSR21.wrongTarget"
    tick=chr(96)*2
    audit=[HELPER,"","def "+wrong_name+" : Prop := "+typed.term(wrong["target"]),
        "open Lean Meta KuuOSR21","run_cmd do","  let env ← getEnv",
        "  let some w := env.find? "+tick+witness+' | throwError "missing witness"',
        '  let some body := w.value? (allowOpaque := true) | throwError "missing proof body"',
        "  let some s := env.find? "+tick+name+' | throwError "missing shared source"',
        "  let some gt := env.find? "+tick+target+' | throwError "missing target"',
        "  let some bad := env.find? "+tick+wrong_name+' | throwError "missing wrong target"',
        '  let some goodGoal := gt.value? (allowOpaque := true) | throwError "missing target body"',
        '  let some badGoal := bad.value? (allowOpaque := true) | throwError "missing wrong body"',
        '  unless s.isTheorem && s.levelParams.isEmpty && !s.type.hasMVar && !s.type.hasFVar && !s.type.hasLooseBVars do',
        '    throwError "shared source is not a closed monomorphic theorem"',
        "  let n := "+tick+name,
        "  let occurrences := countConst n body",
        "  let uses := sharedBindings n body",
        "  let (sameTarget, wrongTarget) ← Lean.Elab.Command.liftTermElabM do",
        "    let a ← withNewMCtxDepth <| isDefEq s.type goodGoal",
        "    let b ← withNewMCtxDepth <| isDefEq s.type badGoal",
        "    pure (a, b)",
        '  unless sameTarget && !wrongTarget && occurrences == 1 && uses == ['+str(leaf["uses"])+'] do',
        '    throwError m!"shared proof binding not verified: occurrences={occurrences}, uses={uses}, same={sameTarget}, wrong={wrongTarget}"',
        '  let payload := Json.mkObj [("source", toJson n.toString), ("source_type", toJson (reprStr s.type)),',
        '    ("proof_constant_occurrences", toJson occurrences), ("shared_binding_uses", toJson uses),',
        '    ("same_target_defeq", toJson sameTarget), ("wrong_target_defeq", toJson wrongTarget),',
        '    ("wrong_target_expr", toJson (reprStr badGoal)), ("proof_expr", toJson (reprStr body))]',
        '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return req,p,src+"\n"+"\n".join(audit),mcp
