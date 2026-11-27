"""R52: bounded exact-premise selection and typed application of R51 references.

Closed premises are matched by complete kernel Expr, not by name similarity.
The selected polymorphic gluing rule is specialized by the actual cover,
atlas, and proved premises. Unmatched propositions stay HOLD.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_contextual_frontier_reference_v1_r3 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
derived=prev.derived
DIRECT="b138aa773cb4fa2ea78c21acddf97f976ec2b9563de1b385fe1e753a16e5ba1f"
MCP="c31b73eadd266d4c5a6c31a00894e10a97cb578d9e4ae505ae9f1405067f3133"
REFERENCE="737ab0c8c783a3940a118004f8f8b6774ea2f8581e48ebca90b815f5c1e83d12"
MANIFEST=prev.MANIFEST
NS="KuuOSR52Typed"
MARK="KUUOS_R52_PREMISES "
TARGET_MARK="KUUOS_R52_TARGETS "
LEC=base.LEC
COVER=LEC+"nativeF55_twoChart_cover"
U=LEC+"northNativeF55TwoChartCover"
SHADOW=LEC+"northNativeF55TwoChartShadow"
RAW=LEC+"northNativeF55TwoChartRaw"
ALT=LEC+"northNativeF55TwoChartConstantRaw"
BACK=LEC+"global_implies_compatible"
GLUE=LEC+"glue_agrees"
COMPAT=LEC+"nativeF55_twoChart_shadow_compatible"
INCOMPAT=LEC+"nativeF55_twoChart_raw_incompatible"
JOINT=LEC+"nativeF55_twoChart_shadow_glues_not_raw"

def admit(d,mp,ind,index,extension,layer,memory,mem,graph,frontier,reference):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R51_DIRECT_CONTEXTUAL_FRONTIER_REFERENCE" or
        mp["status"]!="R51_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R51_INDEPENDENT_CONTEXTUAL_FRONTIER_REFERENCE_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        reference["key"]!=REFERENCE or base.portable.seal(reference)["key"]!=REFERENCE or
        frontier["key"]!=prev.FRONTIER or base.portable.seal(frontier)["key"]!=frontier["key"] or
        graph["key"]!=prev.prev.GRAPH or base.portable.seal(graph)["key"]!=graph["key"] or
        memory["key"]!=prev.prev.prev.LAYER or base.portable.seal(memory)["key"]!=memory["key"] or
        layer["key"]!=prev.prev.prev.prev.PARENT or base.portable.seal(layer)["key"]!=layer["key"] or
        extension["key"]!=derived.PARENT or base.portable.seal(extension)["key"]!=extension["key"] or
        index["key"]!=derived.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        reference["parent_frontier_key"]!=frontier["key"] or reference["parent_graph_key"]!=graph["key"] or
        frontier["parent_graph_key"]!=graph["key"] or graph["parent_transport_key"]!=memory["key"] or
        memory["parent_derived_key"]!=layer["key"] or memory["parent_extension_key"]!=extension["key"] or
        memory["parent_dispatch_key"]!=index["key"] or layer["parent_extension_key"]!=extension["key"] or
        layer["parent_dispatch_key"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["reference_key"]!=REFERENCE or x["frontier_key"]!=frontier["key"] or
            x["graph_key"]!=graph["key"] or x["transport_layer_key"]!=memory["key"] or
            x["derived_layer_key"]!=layer["key"] or x["extension_key"]!=extension["key"] or
            x["dispatch_layer_key"]!=index["key"] or x["capsule_layer_key"]!=mem["key"] or
            x["capsule_manifest"]!=dispatch.prev.MANIFEST or x["joint_capsule_manifest"]!=MANIFEST or
            x["theorem_references"]!=20 or x["non_theorem_holds"]!=44 or
            x["polymorphic_references"]!=10 or x["monomorphic_references"]!=10 or
            x["exact_type_and_universes"] is not True or x["source_proof_identity"] is not True or
            x["application_authority"] is not False or x["historical_hold_retained"] is not True or
            x["raw_negative_retained"] is not True or x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or
            x["provider_calls"]!=0 or x["all_repository_dependencies_observed"] is not False or
            x["semantic_search_complete"] is not False or x["proof_authority"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["reference_bytes_equal"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=61 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R51 receipt binding")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=61 or set(hist)!=set(ma) or any(hist[n]["axioms"]!=ma[n] or
        set(ma[n])-typed.STANDARD for n in hist):raise ValueError("R51 audit binding")
    candidates,decisions=prev.select(frontier,base.CURRENT)
    records=reference["records"]
    if set(records)!=set(candidates) or reference["selection_decisions"]!=decisions:
        raise ValueError("R51 reference inventory")
    for n,c in candidates.items():
        if any(records[n][k]!=v for k,v in c.items()) or records[n]["alias_observation"]!=hist[c["alias"]]:
            raise ValueError("R51 reference drift")
    parent={n:x for n,x in hist.items() if n not in {c["alias"] for c in candidates.values()}}
    prev.prev.recheck(parent,graph)
    return hist,candidates

def goals():
    return "\nnamespace "+NS+"\n"+ "\n".join([
        "def coverTarget : Prop := "+LEC+"Covers "+U,
        "def shadowCompatTarget : Prop := "+LEC+"Compatible "+U+" "+SHADOW,
        "def rawCompatTarget : Prop := "+LEC+"Compatible "+U+" "+RAW,
        "def rawIncompatTarget : Prop := Not ("+LEC+"Compatible "+U+" "+RAW+")",
        "def shadowGlobalTarget : Prop := "+LEC+"HasGlobal "+U+" "+SHADOW,
        "def rawGlobalTarget : Prop := "+LEC+"HasGlobal "+U+" "+RAW,
        "def rawNoGlobalTarget : Prop := Not ("+LEC+"HasGlobal "+U+" "+RAW+")",
        "def alternateGlobalTarget : Prop := "+LEC+"HasGlobal "+U+" "+ALT,
        "end "+NS,""])

GOALS=("cover","shadowCompat","rawCompat","rawIncompat","shadowGlobal","rawGlobal","rawNoGlobal","alternateGlobal")
def pool(candidates,hist):
    if COVER not in hist or BACK not in hist or any(n not in candidates for n in (GLUE,COMPAT,INCOMPAT,JOINT,"And.right")):
        raise ValueError("HOLD_MISSING_RULE")
    return {**{c["alias"]:n for n,c in sorted(candidates.items())},COVER:COVER}

def observer(candidates,hist):
    p=pool(candidates,hist);tick=chr(96)*2
    entries=", ".join(tick+n for n in sorted(p))
    # Small commands: no generated large dependent tactic expression.
    parts=[]
    for label in GOALS:
        parts.append(r'''open Lean
set_option maxHeartbeats 4000000 in
run_cmd do
  let r52Env ← getEnv
  let some r52Target := r52Env.find? TARGET | throwError "missing target"
  let some r52Goal := r52Target.value? (allowOpaque := true) | throwError "missing goal body"
  let r52Pool : Array Name := #[ENTRIES]
  let mut r52Rows : Array Json := #[]
  for r52Name in r52Pool do
    let some r52Info := r52Env.find? r52Name | throwError "missing certified candidate"
    unless r52Info.isTheorem do throwError "not a theorem"
    let r52Status := if !r52Info.levelParams.isEmpty then "HOLD_POLYMORPHIC_PREMISE"
      else if r52Info.type.equal r52Goal then "EXACT_CLOSED_PREMISE" else "HOLD_TYPE_MISMATCH"
    r52Rows := r52Rows.push (Json.mkObj [("name",toJson r52Name.toString),
      ("status",toJson r52Status),("type_expr",toJson (reprStr r52Info.type)),
      ("universes",toJson (r52Info.levelParams.map Name.toString))])
  let r52Payload := Json.mkObj [("goal",toJson LABEL),("goal_expr",toJson (reprStr r52Goal)),("trials",toJson r52Rows)]
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R52_PREMISES " ++ r52Payload.compress)
'''.replace("TARGET",tick+NS+"."+label+"Target").replace("ENTRIES",entries).replace("LABEL",'"'+label+'"'))
    return "\n".join(parts)

def choose(candidates,hist,observations):
    p=pool(candidates,hist)
    if set(observations)!=set(GOALS):raise ValueError("HOLD_PREMISE_INVENTORY")
    decisions={}
    for label in GOALS:
        ob=observations[label];rs=ob["trials"]
        if ob["goal"]!=label or len(rs)!=len(p) or {x["name"] for x in rs}!=set(p):
            raise ValueError("HOLD_PREMISE_INVENTORY")
        found=[]
        for x in rs:
            h=hist[x["name"]]
            if x["type_expr"]!=h["type_expr_repr"] or x["universes"]!=h["universe_parameters"]:
                raise ValueError("HOLD_PREMISE_TYPE_DRIFT")
            st=("HOLD_POLYMORPHIC_PREMISE" if x["universes"] else
                "EXACT_CLOSED_PREMISE" if x["type_expr"]==ob["goal_expr"] else "HOLD_TYPE_MISMATCH")
            if x["status"]!=st:raise ValueError("HOLD_PREMISE_OBSERVATION")
            if st=="EXACT_CLOSED_PREMISE":found.append(x["name"])
        decisions[label]={"status":"EXACT_PREMISE_REQUIRED" if found else "HOLD_NO_EXACT_PREMISE",
                          "matches":sorted(found),"goal_expr":ob["goal_expr"]}
    required={"cover":COVER,"shadowCompat":candidates[COMPAT]["alias"],"rawIncompat":candidates[INCOMPAT]["alias"]}
    for label,n in required.items():
        if n not in decisions[label]["matches"]:raise ValueError("HOLD_REQUIRED_PREMISE")
    for label in ("rawCompat","rawGlobal"):
        if decisions[label]["matches"]:raise ValueError("unexpected positive raw premise")
    # Deterministic exact match, preserve every other matched alternative.
    chosen={label:n for label,n in required.items()}
    return decisions,chosen

def consumer(candidates,chosen):
    g=candidates[GLUE]["alias"];c=chosen["cover"];s=chosen["shadowCompat"];r=chosen["rawIncompat"]
    j=candidates[JOINT]["alias"];right=candidates["And.right"]["alias"]
    body="\nnamespace "+NS+"\nset_option autoImplicit false\n"
    body+="theorem shadowViaGlue : shadowGlobalTarget := by\n"
    body+="  change "+LEC+"HasGlobal "+U+" "+SHADOW+"\n"
    body+="  exact ⟨"+LEC+"glue "+U+" "+SHADOW+" "+c+" "+s+", fun i x => "+g+" "+U+" "+SHADOW+" "+c+" "+s+" i x⟩\n"
    body+="theorem rawViaIncompat : rawNoGlobalTarget := by\n  intro h\n  exact "+r+" ("+BACK+" "+U+" "+RAW+" h)\n"
    body+="theorem rawViaJoint : rawNoGlobalTarget := "+right+" "+j+"\nend "+NS+"\n"
    refs={NS+".shadowViaGlue":[g,c,s],NS+".rawViaIncompat":[r,BACK],NS+".rawViaJoint":[right,j]}
    tick=chr(96)*2
    checks="open Lean\nrun_cmd do\n  let r52Env ← getEnv\n"
    for i,(n,t) in enumerate([(NS+".shadowViaGlue","shadowGlobal"),(NS+".rawViaIncompat","rawNoGlobal"),(NS+".rawViaJoint","rawNoGlobal")]):
        checks+="  let some r52Witness"+str(i)+" := r52Env.find? "+tick+n+' | throwError "missing typed witness"\n'
        checks+="  unless r52Witness"+str(i)+".isTheorem && r52Witness"+str(i)+".type.equal (mkConst "+tick+NS+"."+t+'Target) do throwError "typed witness drift"\n'
    checks+='  Lean.Elab.Command.liftIO <| IO.println "KUUOS_R52_TARGETS GREEN"\n'
    return body,checks,refs

def controls(candidates,hist,observations):
    import copy
    out={}
    def reject(k,o):
        try:choose(candidates,hist,o)
        except ValueError as e:out[k]=str(e)
        else:raise ValueError("invalid premise accepted "+k)
    bad=copy.deepcopy(observations);bad["cover"]["trials"].pop()
    reject("missing_trial",bad)
    bad=copy.deepcopy(observations);bad["cover"]["trials"][0]["type_expr"]="fabricated"
    reject("type_drift",bad)
    bad=copy.deepcopy(observations)
    n=candidates[COMPAT]["alias"]
    next(x for x in bad["rawCompat"]["trials"] if x["name"]==n)["status"]="EXACT_CLOSED_PREMISE"
    reject("wrong_context",bad)
    if out!={"missing_trial":"HOLD_PREMISE_INVENTORY","type_drift":"HOLD_PREMISE_TYPE_DRIFT","wrong_context":"HOLD_PREMISE_OBSERVATION"}:
        raise ValueError("premise controls")
    return out
