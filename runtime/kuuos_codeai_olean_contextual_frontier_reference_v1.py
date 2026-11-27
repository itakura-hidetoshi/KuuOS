"""R51: certify exact reference witnesses for observed frontier theorems.

Keep the original Lean type, all universe parameters, and source proof
identity. A checked generic reference is not a license to instantiate it
in an arbitrary context. Non-theorem observations remain observations.
"""
from __future__ import annotations
import json
from collections import Counter
from runtime import kuuos_codeai_olean_contextual_frontier_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
derived=prev.derived
DIRECT="6598631d11730e17bc934b36fd63d762d4978f8e91bed84c6bb6291c1991287b"
MCP="7fe07564ee606c037d337bdd7bc6fc552afa1b0901c37e98b3a9b1255980fedd"
FRONTIER="7f60dbaaf5e7e2ea67194f16492716d228807db2bbfad04ffb62dccd2c8190a6"
MANIFEST=prev.MANIFEST
MARK="KUUOS_R51_REFERENCE "
NS="KuuOSR51Frontier"

def admit(d,mp,ind,index,extension,layer,memory,mem,graph,frontier):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R50_DIRECT_CONTEXTUAL_FRONTIER" or mp["status"]!="R50_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R50_INDEPENDENT_CONTEXTUAL_FRONTIER_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        frontier["key"]!=FRONTIER or base.portable.seal(frontier)["key"]!=FRONTIER or
        graph["key"]!=prev.GRAPH or base.portable.seal(graph)["key"]!=graph["key"] or
        memory["key"]!=prev.prev.LAYER or base.portable.seal(memory)["key"]!=memory["key"] or
        layer["key"]!=prev.prev.prev.PARENT or base.portable.seal(layer)["key"]!=layer["key"] or
        extension["key"]!=derived.PARENT or base.portable.seal(extension)["key"]!=extension["key"] or
        index["key"]!=derived.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        frontier["parent_graph_key"]!=graph["key"] or graph["parent_transport_key"]!=memory["key"] or
        memory["parent_derived_key"]!=layer["key"] or memory["parent_extension_key"]!=extension["key"] or
        memory["parent_dispatch_key"]!=index["key"] or layer["parent_extension_key"]!=extension["key"] or
        layer["parent_dispatch_key"]!=index["key"] or index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["frontier_key"]!=FRONTIER or x["graph_key"]!=graph["key"] or
            x["transport_layer_key"]!=memory["key"] or x["derived_layer_key"]!=layer["key"] or
            x["extension_key"]!=extension["key"] or x["dispatch_layer_key"]!=index["key"] or
            x["capsule_layer_key"]!=mem["key"] or x["capsule_manifest"]!=dispatch.prev.MANIFEST or
            x["joint_capsule_manifest"]!=MANIFEST or x["requested_count"]!=64 or x["resolved_count"]!=64 or
            x["unresolved_count"]!=0 or x["kind_counts"]!={"constructor":7,"definition":32,"inductive":5,"theorem":20} or
            x["value_body_count"]!=52 or x["next_type_frontier_count"]!=52 or x["next_value_frontier_count"]!=88 or
            x["axiom_boundary_count"]!=0 or x["expanded_depth"]!=1 or x["parent_graph_preserved"] is not True or
            x["historical_hold_retained"] is not True or x["raw_negative_retained"] is not True or
            x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["all_repository_dependencies_observed"] is not False or
            x["semantic_search_complete"] is not False or x["proof_authority"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["frontier_bytes_equal"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=41 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R50 receipt binding")
    rows={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(rows)!=41 or len(ma)!=41 or set(rows)!=set(ma) or any(
        rows[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in rows):
        raise ValueError("R50 audit binding")
    prev.recheck(rows,graph)
    return rows

def select_one(x):
    if x["status"]!="OBSERVED" or x["kind"]!="theorem":return "HOLD_NOT_THEOREM"
    if not x["has_value"] or not x["value_expr"]:return "HOLD_NO_PROOF_BODY"
    if x["unsafe"] or x["partial"]:return "HOLD_UNSAFE_OR_PARTIAL"
    if x["admission"]!="HOLD_OBSERVATION_ONLY" or set(x["axioms"])-typed.STANDARD:
        return "HOLD_AXIOM_BOUNDARY"
    return "EXACT_REFERENCE_REQUIRED"

def select(frontier,head):
    if head!=base.CURRENT or frontier["key"]!=FRONTIER or base.portable.seal(frontier)["key"]!=FRONTIER:
        raise ValueError("HOLD_FRONTIER_SCOPE")
    decisions={n:select_one(x) for n,x in sorted(frontier["observations"].items())}
    candidates={}
    for i,n in enumerate(n for n,s in decisions.items() if s=="EXACT_REFERENCE_REQUIRED"):
        x=frontier["observations"][n];a=NS+".w"+str(i)
        candidates[n]={"alias":a,"source_name":n,"source_origin":x["origin"],
            "source_observation_digest":old.digest(x),"source_type_expr":x["type_expr"],
            "source_value_expr":x["value_expr"],"universe_parameters":x["universe_parameters"],
            "axioms":x["axioms"],"requires_typed_application":True,"proof_authority":False}
    if len(candidates)!=20 or Counter(decisions.values())!={"EXACT_REFERENCE_REQUIRED":20,"HOLD_NOT_THEOREM":44}:
        raise ValueError("HOLD_REFERENCE_INVENTORY")
    return candidates,decisions

def aliases(roots,candidates):
    """Construct checked declarations from the actual kernel Name and type."""
    roots_expr=", ".join(chr(96)*2+typed.name(n) for n in roots)
    want=", ".join("("+json.dumps(n,ensure_ascii=False)+", "+chr(96)*2+c["alias"]+")" for n,c in candidates.items())
    # Alias names are not yet declared. Build their Names explicitly rather
    # than using name quotation that resolves constants during elaboration.
    want=", ".join("("+json.dumps(n,ensure_ascii=False)+", Name.str (Name.str Name.anonymous "+
                   json.dumps(NS)+") "+json.dumps(c["alias"].rsplit(".",1)[1])+")" for n,c in candidates.items())
    return r'''open Lean
set_option maxHeartbeats 4000000 in
set_option Elab.async false in
run_cmd do
  let env ← getEnv
  let roots : Array Name := #[ROOTS]
  let wanted : Array (String × Name) := #[WANTED]
  let mut names : Array Name := #[]
  for root in roots do
    let some ci := env.find? root | throwError "missing parent"
    let some proof := ci.value? (allowOpaque := true) | throwError "missing parent body"
    for dep in proof.getUsedConstants do
      if !names.contains dep then
        names := names.push dep
  let mut rows : Array Json := #[]
  for (printed, alias) in wanted do
    let matches := names.filter (fun n => n.toString == printed)
    unless matches.size == 1 do throwError "ambiguous frontier name"
    let n := matches[0]!
    let some ci := env.find? n | throwError "missing frontier theorem"
    unless ci.isTheorem && !ci.isUnsafe && !ci.isPartial do throwError "not a safe theorem"
    let some original := ci.value? (allowOpaque := true) | throwError "missing proof value"
    if ci.type.hasMVar || ci.type.hasFVar || ci.type.hasLooseBVars ||
       original.hasMVar || original.hasFVar || original.hasLooseBVars then
      throwError "open declaration"
    let proof := mkConst n (ci.levelParams.map Level.param)
    Lean.Elab.Command.liftCoreM <| Lean.addDecl (.thmDecl {
      name := alias, levelParams := ci.levelParams, type := ci.type, value := proof })
    let after ← getEnv
    let some wi := after.find? alias | throwError "missing reference witness"
    let some value := wi.value? (allowOpaque := true) | throwError "missing reference value"
    unless wi.isTheorem && wi.type.equal ci.type && wi.levelParams == ci.levelParams &&
       value.equal proof do throwError "exact reference mismatch"
    let ax ← Lean.collectAxioms alias
    rows := rows.push (Json.mkObj [("source",toJson n.toString),("alias",toJson alias.toString),
      ("source_name_repr",toJson (reprStr n)),("source_type_expr",toJson (reprStr ci.type)),
      ("source_value_expr",toJson (reprStr original)),("alias_type_expr",toJson (reprStr wi.type)),
      ("alias_value_expr",toJson (reprStr value)),("universes",toJson (ci.levelParams.map Name.toString)),
      ("axioms",toJson (ax.map Name.toString)),("exact_reference",toJson true)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R51_REFERENCE " ++ (toJson rows).compress)
'''.replace("ROOTS",roots_expr).replace("WANTED",want)

def check_references(candidates,frontier,rows,audit):
    if set(rows)!=set(candidates):raise ValueError("HOLD_REFERENCE_INVENTORY")
    records={}
    for n,c in sorted(candidates.items()):
        x=rows[n];f=frontier["observations"][n];a=audit[c["alias"]]
        if (x["source"]!=n or x["alias"]!=c["alias"] or x["source_name_repr"]!=f["name_repr"] or
            x["source_type_expr"]!=c["source_type_expr"] or x["alias_type_expr"]!=c["source_type_expr"] or
            a["type_expr_repr"]!=c["source_type_expr"] or x["universes"]!=c["universe_parameters"] or
            a["universe_parameters"]!=c["universe_parameters"]):
            raise ValueError("HOLD_REFERENCE_TYPE_DRIFT")
        if x["source_value_expr"]!=c["source_value_expr"] or not x["exact_reference"] or n not in a["proof_constants"]:
            raise ValueError("HOLD_REFERENCE_PROOF_DRIFT")
        if sorted(set(x["axioms"]))!=c["axioms"] or a["axioms"]!=c["axioms"]:
            raise ValueError("HOLD_REFERENCE_AXIOM_DRIFT")
        records[n]={**c,"alias_observation":a,"exact_reference_observation":x,
            "status":"DIRECT_REFERENCE_CHECKED","application_authority":False}
    return records

def controls(frontier,candidates,rows,audit):
    import copy
    out={}
    def reject(label,fn):
        try:fn()
        except ValueError as e:out[label]=str(e)
        else:raise ValueError("invalid reference admitted "+label)
    reject("old_head",lambda:select(frontier,old.HEAD))
    n=next(iter(sorted(rows)));bad=copy.deepcopy(rows);bad[n]["alias_type_expr"]="fabricated"
    reject("wrong_type",lambda:check_references(candidates,frontier,bad,audit))
    bad=copy.deepcopy(rows);bad[n]["source_value_expr"]="fabricated"
    reject("wrong_proof",lambda:check_references(candidates,frontier,bad,audit))
    bad=copy.deepcopy(rows);bad.pop(n)
    reject("missing_reference",lambda:check_references(candidates,frontier,bad,audit))
    if out!={"old_head":"HOLD_FRONTIER_SCOPE","wrong_type":"HOLD_REFERENCE_TYPE_DRIFT",
             "wrong_proof":"HOLD_REFERENCE_PROOF_DRIFT","missing_reference":"HOLD_REFERENCE_INVENTORY"}:
        raise ValueError("reference control drift")
    return out
