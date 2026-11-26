"""R22: common non-nullary subtree of two admitted R20 routes.
Structural equality proposes a subtree only. Closed specialized proof type,
actual kernel binding and uses must be checked. No root search, no provider.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_proof_dag_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old

MARK="KUUOS_R22_SHARED_SUBPROOF "
HELPER=prev.HELPER+r'''
open Lean Meta KuuOSR21
namespace KuuOSR22
def bindings (n : Name) : Expr → List (Expr × Expr × Nat)
  | .app f a => bindings n f ++ bindings n a
  | .lam _ t b _ => bindings n t ++ bindings n b
  | .forallE _ t b _ => bindings n t ++ bindings n b
  | .letE _ t v b _ =>
    (if v.getAppFn.isConstOf n then [(t, v, KuuOSR21.countBound 0 b)] else []) ++
      bindings n t ++ bindings n v ++ bindings n b
  | .mdata _ e => bindings n e
  | .proj _ _ e => bindings n e
  | _ => []

def closed (e : Expr) : Bool :=
  !e.hasMVar && !e.hasFVar && !e.hasLooseBVars && !e.hasLevelMVar
end KuuOSR22
'''

def tree(route):
    pos=0
    def parse(depth):
        nonlocal pos
        if pos>=len(route) or depth>4:raise ValueError("route bounds")
        row=route[pos];pos+=1
        n=typed.name(row["rule"]);a=row["arity"]
        if type(a) is not int or not 0<=a<=3:raise ValueError("arity")
        return (n,tuple(parse(depth+1) for _ in range(a)))
    root=parse(0)
    if pos!=len(route):raise ValueError("trailing route")
    return root

def nodes(t):
    return [t]+[n for c in t[1] for n in nodes(c)]

def plan(inv, r20, r21):
    if old.digest(inv)!=r20["inventory_digest"] or any(
        h["source_head"]!=old.HEAD or h["source_tree"]!=old.TREE or h["scope_digest"]!=old.SCOPE
        for h in (r20,r21)):
        raise ValueError("scope/inventory drift")
    if r21["r20_direct_digest"]!=old.digest(r20) or r21["plan"]["route"]!=r20["applications"][r21["case"]]["route"]:
        raise ValueError("R21 route lineage")
    cases=sorted(r20["applications"])
    if len(cases)!=2:raise ValueError("bounded two-route fixture")
    trees={}
    for k in cases:
        q=r20["requests"][k];prev.prev.validate(q)
        a=r20["applications"][k]
        if (a["route"]!=r20["results"][k]["chosen"]["route"] or
            a["request"]["target"]!=q["target"] or
            a["application"]["exact_kernel_type_match"] is not True or
            a["target_expr_repr"]!=a["application"]["target_expr_repr"]):
            raise ValueError("admitted route changed")
        trees[k]=tree(a["route"])
    left,right=cases
    common={n for n in nodes(trees[left]) if n[1]} & {n for n in nodes(trees[right]) if n[1]}
    if not common:return {"status":"HOLD_NO_COMMON_SUBTREE"}
    candidate=sorted(common,key=lambda n:(-len(nodes(n)),repr(n)))[0]
    if any(nodes(trees[k]).count(candidate)!=1 for k in cases):
        return {"status":"HOLD_AMBIGUOUS_SUBTREE_OCCURRENCE"}
    indexed={p["name"]:p for ps in inv["selected"].values() for p in ps}
    source_nodes=[]
    for name in sorted({n[0] for n in nodes(candidate)}):
        item=indexed[name];key=item["module"]+"::"+name
        mat=r20["materials"][key]
        if mat["name"]!=name or mat["module"]!=item["module"]:
            raise ValueError("source material changed")
        source_nodes.append({"module":item["module"],"name":name,
                             "type_expr_sha256":mat["type_expr_sha256"]})
    return {"status":"SPECIALIZED_SUBTREE_CANDIDATE","cases":cases,
            "shared_root":candidate[0],"shared_tree":candidate,
            "shared_tree_nodes":len(nodes(candidate)),"uses":2,"sources":source_nodes,
            "request_digests":{k:r20["requests"][k]["request_digest"] for k in cases},
            "r20_direct_digest":old.digest(r20),"r21_direct_digest":old.digest(r21),
            "source_head":old.HEAD,"source_tree":old.TREE,"scope_digest":old.SCOPE,
            "proof_authority":False}

def application(inv,r20,r21,shared_goal,wrong_goal):
    p=plan(inv,r20,r21)
    if p["status"]!="SPECIALIZED_SUBTREE_CANDIDATE":raise ValueError(p["status"])
    shared=p["shared_tree"];name=typed.name(p["shared_root"])
    typed.term(shared_goal);typed.term(wrong_goal)
    q={k:r20["requests"][k] for k in p["cases"]}
    target={"apply":[{"const":"And"}]+[q[k]["target"] for k in p["cases"]]}
    req=typed.make_request("r22_joint_specialized",q[p["cases"][0]]["context_modules"][0],
                           "And.intro",target,[],"positive")
    def render_node(t,indent,depth,args,replace):
        if replace and t==shared:return ["exact shared0"]
        n,children=t
        term=prev.prev.base.bound_term(n,args) if args and (depth==0 or n in prev.prev.base.BOUND_RULES) else "@"+n
        lines=["apply "+term]
        for child in children:
            rows=render_node(child,indent+2,depth+1,args,replace)
            lines+=[" "*indent+"· "+rows[0]]+rows[1:]
        return lines
    # The common node is not one of either request's roots. Its actual
    # specialized type is supplied explicitly and checked in both uses.
    if any(tree(r20["applications"][k]["route"])==shared for k in p["cases"]):
        raise ValueError("root sharing not supported")
    shared_lines=render_node(shared,4,1,[],False)
    replacement="theorem witness : target :=\n  let shared0 : "+typed.term(shared_goal)+" := by\n    "
    replacement+="\n".join(shared_lines)+"\n  by\n    change "+typed.term(target)+"\n    apply @And.intro"
    for k in p["cases"]:
        rows=render_node(tree(r20["applications"][k]["route"]),6,0,q[k]["context_args"],True)
        replacement+="\n    · "+rows[0]
        if len(rows)>1:replacement+="\n"+"\n".join(rows[1:])
    marker="theorem witness : target := @And.intro"
    def transform(s):
        if s.count(marker)!=1:raise ValueError("witness boundary")
        return s.replace(marker,replacement,1)
    src,mcp=transform(typed.render(req)),transform(typed.declarations(req))
    _,w=typed.names(req);tick=chr(96)*2
    audit=[HELPER,"","def KuuOSR22.expectedType : Prop := "+typed.term(shared_goal),
        "def KuuOSR22.wrongType : Prop := "+typed.term(wrong_goal),
        "open Lean Meta KuuOSR22","run_cmd do","  let env ← getEnv",
        "  let some wi := env.find? "+tick+w+' | throwError "missing witness"',
        '  let some body := wi.value? (allowOpaque := true) | throwError "missing witness body"',
        "  let some ei := env.find? "+tick+"KuuOSR22.expectedType"+' | throwError "missing expected type"',
        "  let some bi := env.find? "+tick+"KuuOSR22.wrongType"+' | throwError "missing wrong type"',
        '  let some expected := ei.value? (allowOpaque := true) | throwError "missing expected body"',
        '  let some wrong := bi.value? (allowOpaque := true) | throwError "missing wrong body"',
        "  let n := "+tick+name,
        "  let found := KuuOSR22.bindings n body",
        '  unless found.length == 1 do throwError "expected one specialized binding"',
        '  let some (ty, value, uses) := found.head? | throwError "missing binding"',
        '  unless KuuOSR22.closed ty && KuuOSR22.closed value do throwError "open specialized subproof"',
        "  let (sameTy, badTy, inferredTy) ← Lean.Elab.Command.liftTermElabM do",
        "    let a ← withNewMCtxDepth <| isDefEq ty expected",
        "    let b ← withNewMCtxDepth <| isDefEq ty wrong",
        "    let c ← withNewMCtxDepth <| isDefEq (← inferType value) ty",
        "    pure (a, b, c)",
        "  let occurrences := KuuOSR21.countConst n body",
        '  unless sameTy && !badTy && inferredTy && uses == 2 && occurrences == 1 do',
        '    throwError m!"shared specialization mismatch: same={sameTy}, wrong={badTy}, inferred={inferredTy}, uses={uses}, occurrences={occurrences}"',
        '  let payload := Json.mkObj [("source", toJson n.toString),',
        '    ("specialized_type", toJson (reprStr ty)), ("specialized_proof", toJson (reprStr value)),',
        '    ("proof_constant_occurrences", toJson occurrences), ("shared_binding_uses", toJson uses),',
        '    ("same_type_defeq", toJson sameTy), ("wrong_type_defeq", toJson badTy),',
        '    ("inferred_type_defeq", toJson inferredTy), ("proof_expr", toJson (reprStr body))]',
        '  Lean.Elab.Command.liftIO <| IO.println ("'+MARK+'" ++ payload.compress)',""]
    return req,p,src+"\n"+"\n".join(audit),mcp
