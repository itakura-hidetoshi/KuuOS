"""R53: select a bounded root rule by actual Lean conclusion and premise types.

Use the independently admitted R51 references and three R52 parent rules.
No chosen theorem name is supplied for a target. Try direct application and
both projections of an Iff conclusion; close proof arguments using the finite
observed fact pool. Non-proof arguments must be inferred, not guessed.
Successful routes are checked declarations. Failure is HOLD, not refutation.
"""
from __future__ import annotations
import json
from runtime import kuuos_codeai_olean_contextual_frontier_application_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
derived=prev.derived
DIRECT="228084738b89db650c1871eb607f15d3119492bd76a46561362e7c86cdbf9433"
MCP="1e979bc0000c7242444a10b5b3e63dd2329627837fc52833944e0aa99217bb34"
APPLICATION="5a71f580735990223a7845a4e6ee46e645cb756d13dd6470c82e7e95fdfde371"
MANIFEST=prev.MANIFEST
NS="KuuOSR53Selected"
MARK="KUUOS_R53_RULES "
GOALS=("shadowGlobal","shadowCompat","rawNoGlobal","rawGlobal","rawCompat")
MODES=("direct","iffForward","iffBackward")
IFF=base.LEC+"compatible_iff_hasGlobal"

def admit(d,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference,application):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R52_DIRECT_CONTEXTUAL_FRONTIER_APPLICATION" or
        mp["status"]!="R52_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R52_INDEPENDENT_CONTEXTUAL_FRONTIER_APPLICATION_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        application["key"]!=APPLICATION or base.portable.seal(application)["key"]!=APPLICATION):
        raise ValueError("R52 receipt binding")
    layers=((reference,prev.REFERENCE),(frontier,prev.prev.FRONTIER),(graph,prev.prev.prev.GRAPH),
            (memory,prev.prev.prev.prev.LAYER),(layer,prev.prev.prev.prev.prev.PARENT),
            (extension,derived.PARENT),(index,derived.parent.PARENT),(mem,dispatch.LAYER))
    if any(x["key"]!=k or base.portable.seal(x)["key"]!=k for x,k in layers):
        raise ValueError("R52 immutable layer binding")
    if (application["parent_reference_key"]!=reference["key"] or
        reference["parent_frontier_key"]!=frontier["key"] or reference["parent_graph_key"]!=graph["key"] or
        frontier["parent_graph_key"]!=graph["key"] or graph["parent_transport_key"]!=memory["key"] or
        memory["parent_derived_key"]!=layer["key"] or memory["parent_extension_key"]!=extension["key"] or
        memory["parent_dispatch_key"]!=index["key"] or layer["parent_extension_key"]!=extension["key"] or
        layer["parent_dispatch_key"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"]):
        raise ValueError("R52 lineage drift")
    for x in (d,ind):
        expected={"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,"scope_digest":old.SCOPE,
            "application_key":APPLICATION,"reference_key":reference["key"],"frontier_key":frontier["key"],
            "graph_key":graph["key"],"transport_layer_key":memory["key"],"derived_layer_key":layer["key"],
            "extension_key":extension["key"],"dispatch_layer_key":index["key"],"capsule_layer_key":mem["key"],
            "capsule_manifest":dispatch.prev.MANIFEST,"joint_capsule_manifest":MANIFEST,
            "premise_trials":168,"premise_goal_count":8,"selected_premises":3,"typed_witnesses":3,
            "positive_witnesses":1,"negative_witnesses":2,"polymorphic_rule_specialized":True,
            "raw_positive_hold":True,"historical_hold_retained":True,"raw_negative_retained":True,
            "capsule_rebuilds":0,"provider_calls":0,"root_search_complete":False,
            "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False}
        if any(x[k]!=v for k,v in expected.items()):raise ValueError("R52 scope binding")
    if (ind["parent_bytes_preserved"] is not True or ind["application_bytes_equal"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=64 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R52 independent evidence")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=64 or len(ma)!=64 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R52 audit binding")
    candidates,selection=prev.prev.select(frontier,base.CURRENT)
    if selection!=reference["selection_decisions"] or set(reference["records"])!=set(candidates):
        raise ValueError("R51 reference inventory")
    for n,c in candidates.items():
        row=reference["records"][n]
        if any(row[k]!=v for k,v in c.items()) or row["alias_observation"]!=hist[c["alias"]]:
            raise ValueError("R51 reference identity")
    earlier={n:x for n,x in hist.items() if n not in application["witnesses"]}
    if len(earlier)!=61 or any(hist[n]!=x for n,x in application["witnesses"].items()):
        raise ValueError("R52 witness identity")
    decisions,chosen=prev.choose(candidates,earlier,application["observations"])
    if decisions!=application["decisions"] or chosen!=application["chosen"]:
        raise ValueError("R52 premise drift")
    parent={n:x for n,x in earlier.items() if n not in {c["alias"] for c in candidates.values()}}
    prev.prev.prev.recheck(parent,graph)
    return hist,candidates

def pool(candidates,hist):
    rules=sorted({c["alias"] for c in candidates.values()}|{prev.COVER,prev.BACK,IFF})
    if len(rules)!=23 or any(n not in hist for n in rules):raise ValueError("HOLD_RULE_INVENTORY")
    # The finite premise pool contains only existing monomorphic declarations;
    # Lean further requires a closed proposition, not an unresolved argument.
    facts=[n for n in rules if not hist[n]["universe_parameters"]]
    return rules,facts

HELPER=r'''
open Lean Meta
namespace KuuOSR53Search
structure Trial where
  status : String
  proof : Option Expr := none
  premises : Array Name := #[]
  probes : Nat := 0

def closedExpr (r53E : Expr) : Bool :=
  !r53E.hasMVar && !r53E.hasLevelMVar && !r53E.hasFVar && !r53E.hasLooseBVars

def trial (r53Rule : Name) (r53Mode : String) (r53Goal : Expr)
    (r53Facts : Array Name) : MetaM Trial := withNewMCtxDepth do
  let r53Const ← mkConstWithFreshMVarLevels r53Rule
  let (r53InitialArgs, _, r53InitialConclusion) ← forallMetaTelescope (← inferType r53Const)
  let mut r53Args := r53InitialArgs
  let mut r53Proof := mkAppN r53Const r53InitialArgs
  let mut r53Conclusion := r53InitialConclusion
  if r53Mode != "direct" then
    unless r53InitialConclusion.isAppOfArity (Name.mkSimple "Iff") 2 do
      return {status := "HOLD_NOT_IFF"}
    let r53Sides := r53InitialConclusion.getAppArgs
    let r53Left := r53Sides[0]!
    let r53Right := r53Sides[1]!
    let r53Forward := r53Mode == "iffForward"
    let r53Premise ← mkFreshExprMVar (some (if r53Forward then r53Left else r53Right))
    let r53Projection := if r53Forward then mkConst (Name.str (Name.mkSimple "Iff") "mp")
                        else mkConst (Name.str (Name.mkSimple "Iff") "mpr")
    r53Proof := mkApp (mkApp3 r53Projection r53Left r53Right r53Proof) r53Premise
    r53Args := r53Args.push r53Premise
    r53Conclusion := if r53Forward then r53Right else r53Left
  let r53Head := r53Conclusion.getAppFn
  let r53GoalHead := r53Goal.getAppFn
  if r53Head.isConst && r53GoalHead.isConst && r53Head.constName! != r53GoalHead.constName! then
    return {status := "HOLD_CONCLUSION_HEAD"}
  unless ← isDefEq r53Conclusion r53Goal do
    return {status := "HOLD_CONCLUSION_TYPE"}
  if r53Args.isEmpty then return {status := "HOLD_DIRECT_RECALL_SEPARATE"}
  let mut r53Used : Array Name := #[]
  let mut r53Probes := 0
  -- Two bounded passes. Matching a proof premise may infer previously open
  -- type/data arguments. No non-proposition argument is invented.
  for _ in [:2] do
    for r53Arg0 in r53Args do
      let r53Arg ← instantiateMVars r53Arg0
      if r53Arg.isMVar then
        let r53Ty ← instantiateMVars (← inferType r53Arg)
        if ← isProp r53Ty then
          for r53Fact in r53Facts do
            let r53FactInfo ← getConstInfo r53Fact
            if r53FactInfo.levelParams.isEmpty && closedExpr r53FactInfo.type then
              let r53Saved ← Meta.saveState
              r53Probes := r53Probes + 1
              let r53Matched ← try
                let r53TyHead := r53Ty.getAppFn
                let r53FactHead := r53FactInfo.type.getAppFn
                if r53TyHead.isConst && r53FactHead.isConst &&
                   r53TyHead.constName! != r53FactHead.constName! then pure false
                else
                  if ← isDefEq r53Ty r53FactInfo.type then
                    pure ((← instantiateMVars r53Ty).equal r53FactInfo.type)
                  else pure false
              catch _ => pure false
              if r53Matched then
                r53Arg.mvarId!.assign (mkConst r53Fact)
                r53Used := r53Used.push r53Fact
                break
              else
                r53Saved.restore
  let r53Final ← instantiateMVars r53Proof
  unless closedExpr r53Final do
    return {status := "HOLD_UNFILLED_ARGUMENT", premises := r53Used, probes := r53Probes}
  if r53Used.isEmpty then
    return {status := "HOLD_NO_PREMISE_RULE", probes := r53Probes}
  let r53FinalType ← instantiateMVars (← inferType r53Final)
  unless r53FinalType.equal r53Goal do
    return {status := "HOLD_TARGET_PRESENTATION", premises := r53Used, probes := r53Probes}
  return {status := "MATCH_RULE", proof := some r53Final, premises := r53Used, probes := r53Probes}

def safeTrial (r53Rule : Name) (r53Mode : String) (r53Goal : Expr)
    (r53Facts : Array Name) : MetaM Trial := do
  try trial r53Rule r53Mode r53Goal r53Facts
  catch _ => pure {status := "HOLD_COMPARISON_FAILURE"}
end KuuOSR53Search
'''

def observer(candidates,hist):
    rules,facts=pool(candidates,hist);tick=chr(96)*2
    entries=", ".join(tick+n for n in rules);leaves=", ".join(tick+n for n in facts)
    parts=[HELPER]
    for label in GOALS:
        parts.append(r'''open Lean
set_option maxHeartbeats 12000000 in
set_option Elab.async false in
run_cmd do
  let r53Env ← getEnv
  let some r53Target := r53Env.find? TARGET | throwError "missing goal"
  let some r53Goal := r53Target.value? (allowOpaque := true) | throwError "missing goal body"
  let r53Rules : Array Name := #[RULES]
  let r53Facts : Array Name := #[FACTS]
  let r53Modes : Array String := #["direct","iffForward","iffBackward"]
  let mut r53Rows : Array Json := #[]
  let mut r53Index : Nat := 0
  for r53Rule in r53Rules do
    for r53Mode in r53Modes do
      let r53Trial ← Lean.Elab.Command.liftTermElabM do
        KuuOSR53Search.safeTrial r53Rule r53Mode r53Goal r53Facts
      let mut r53Witness : Option String := none
      let mut r53ProofExpr : Option String := none
      let mut r53Axioms : Array String := #[]
      if let some r53Proof := r53Trial.proof then
        unless r53Trial.status == "MATCH_RULE" && KuuOSR53Search.closedExpr r53Proof do
          throwError "unclosed selected proof"
        let r53Name := Name.str (Name.mkSimple "KuuOSR53Selected") (LABEL ++ "_" ++ toString r53Index)
        Lean.Elab.Command.liftCoreM <| Lean.addDecl (.thmDecl {
          name := r53Name, levelParams := [], type := r53Goal, value := r53Proof })
        let r53After ← getEnv
        let some r53Info := r53After.find? r53Name | throwError "missing checked proof"
        let some r53Value := r53Info.value? (allowOpaque := true) | throwError "missing checked body"
        unless r53Info.isTheorem && r53Info.type.equal r53Goal && r53Value.equal r53Proof do
          throwError "selected proof identity"
        r53Witness := some r53Name.toString
        r53ProofExpr := some (reprStr r53Value)
        r53Axioms := (← Lean.collectAxioms r53Name).map Name.toString
      r53Rows := r53Rows.push (Json.mkObj [("rule",toJson r53Rule.toString),
        ("mode",toJson r53Mode),("status",toJson r53Trial.status),
        ("premises",toJson (r53Trial.premises.map Name.toString)),("probes",toJson r53Trial.probes),
        ("witness",toJson r53Witness),("proof_expr",toJson r53ProofExpr),("axioms",toJson r53Axioms)])
      r53Index := r53Index + 1
  let r53Payload := Json.mkObj [("goal",toJson LABEL),("goal_expr",toJson (reprStr r53Goal)),("trials",toJson r53Rows)]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R53_RULES " ++ r53Payload.compress)
'''.replace("TARGET",tick+prev.NS+"."+label+"Target").replace("RULES",entries).replace("FACTS",leaves).replace("LABEL",json.dumps(label)))
    return "\n".join(parts)

def project(candidates,hist,application,observations):
    rules,facts=pool(candidates,hist)
    if set(observations)!=set(GOALS):raise ValueError("HOLD_RULE_GOAL_INVENTORY")
    refs={};routes={};decisions={}
    for label in GOALS:
        ob=observations[label]
        if ob["goal"]!=label or ob["goal_expr"]!=application["observations"][label]["goal_expr"]:
            raise ValueError("HOLD_RULE_CONTEXT")
        rows=ob["trials"]
        if [(x["rule"],x["mode"]) for x in rows]!=[(n,m) for n in rules for m in MODES]:
            raise ValueError("HOLD_RULE_TRIAL_INVENTORY")
        chosen=[]
        for i,x in enumerate(rows):
            if any(n not in facts for n in x["premises"]):raise ValueError("HOLD_UNADMITTED_PREMISE")
            if x["status"]!="MATCH_RULE":
                if x["witness"] is not None or x["proof_expr"] is not None or x["axioms"]:
                    raise ValueError("HOLD_UNADMITTED_WITNESS")
                continue
            n=NS+"."+label+"_"+str(i)
            if x["witness"]!=n or not x["proof_expr"] or not x["premises"] or set(x["axioms"])-typed.STANDARD:
                raise ValueError("HOLD_RULE_WITNESS")
            deps=[x["rule"]]+x["premises"]
            if x["mode"]!="direct":deps.append("Iff.mp" if x["mode"]=="iffForward" else "Iff.mpr")
            # The Iff eliminators are kernel-checked logic operations. The
            # original rule and all proof premises must be in admitted rows.
            if not set(x["axioms"])<={a for r in [x["rule"]]+x["premises"] for a in hist[r]["axioms"]}:
                raise ValueError("HOLD_RULE_AXIOMS")
            refs[n]=sorted(set(deps));routes[n]={"goal":label,**x};chosen.append(n)
        decisions[label]={"status":"CHECKED_RULE_ROUTES" if chosen else "HOLD_NO_RULE_ROUTE","witnesses":chosen}
    if (not decisions["shadowGlobal"]["witnesses"] or not decisions["shadowCompat"]["witnesses"] or
        not decisions["rawNoGlobal"]["witnesses"] or decisions["rawGlobal"]["witnesses"] or
        decisions["rawCompat"]["witnesses"]):
        raise ValueError("HOLD_RULE_POLARITY")
    if not any(x["goal"]=="shadowGlobal" and x["mode"]=="iffForward" for x in routes.values()):
        raise ValueError("HOLD_FORWARD_RULE")
    return refs,routes,decisions

def controls(candidates,hist,application,observations):
    import copy
    out={}
    def reject(k,obs):
        try:project(candidates,hist,application,obs)
        except ValueError as e:out[k]=str(e)
        else:raise ValueError("invalid route accepted "+k)
    bad=copy.deepcopy(observations);bad["shadowGlobal"]["trials"].pop()
    reject("missing_trial",bad)
    bad=copy.deepcopy(observations);bad["rawGlobal"]["goal_expr"]=bad["shadowGlobal"]["goal_expr"]
    reject("context_swap",bad)
    bad=copy.deepcopy(observations)
    row=next(x for x in bad["shadowGlobal"]["trials"] if x["status"]=="MATCH_RULE")
    row["premises"].append("KuuOSR53.Unadmitted")
    reject("unadmitted_premise",bad)
    if out!={"missing_trial":"HOLD_RULE_TRIAL_INVENTORY","context_swap":"HOLD_RULE_CONTEXT",
             "unadmitted_premise":"HOLD_UNADMITTED_PREMISE"}:
        raise ValueError("rule control drift")
    return out
