"""R50: one-hop typed observation of the R49 proof-reference frontier.

Actual Lean Names are recovered from the certified parent proof bodies, not
guessed from printed strings. Structural declarations without expression
values and unresolved constants are retained separately. This is observation,
not theorem admission, transitive closure, or action authority.
"""
from __future__ import annotations
import json
from collections import Counter
from runtime import kuuos_codeai_olean_contextual_dependency_audit_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
dispatch=prev.dispatch
derived=prev.derived
DIRECT="7ae14357634fe96f60e0d2d634cc2448a4a047a4fa32fc6b33b62fe15bfb4233"
MCP="4106bb395f8197cc057668e16166aa19d5aeb4408cd9bf53f1ff50a73aefbd60"
GRAPH="203d8b56eb8979fda0c86a51f7a9d98b7e824727051025d945581670f385b72d"
MANIFEST=prev.MANIFEST
MARK="KUUOS_R50_FRONTIER "
KINDS={"axiom","definition","theorem","opaque","quotient","inductive","constructor","recursor"}
VALUE_KINDS={"definition","theorem","opaque"}

def admit(d,mp,ind,index,extension,layer,memory,mem,graph):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R49_DIRECT_CONTEXTUAL_DEPENDENCY_AUDIT" or mp["status"]!="R49_REAL_MCP_GREEN" or
        mp["direct_digest"]!=DIRECT or ind["status"]!="R49_INDEPENDENT_CONTEXTUAL_DEPENDENCY_AUDIT_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        graph["key"]!=GRAPH or base.portable.seal(graph)["key"]!=GRAPH or
        memory["key"]!=prev.LAYER or base.portable.seal(memory)["key"]!=memory["key"] or
        layer["key"]!=prev.prev.PARENT or base.portable.seal(layer)["key"]!=layer["key"] or
        extension["key"]!=derived.PARENT or base.portable.seal(extension)["key"]!=extension["key"] or
        index["key"]!=derived.parent.PARENT or base.portable.seal(index)["key"]!=index["key"] or
        mem["key"]!=dispatch.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        graph["parent_transport_key"]!=memory["key"] or memory["parent_derived_key"]!=layer["key"] or
        memory["parent_extension_key"]!=extension["key"] or memory["parent_dispatch_key"]!=index["key"] or
        layer["parent_extension_key"]!=extension["key"] or layer["parent_dispatch_key"]!=index["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE or x["graph_key"]!=GRAPH or
            x["transport_layer_key"]!=memory["key"] or x["derived_layer_key"]!=layer["key"] or
            x["extension_key"]!=extension["key"] or x["dispatch_layer_key"]!=index["key"] or
            x["capsule_layer_key"]!=mem["key"] or x["capsule_manifest"]!=dispatch.prev.MANIFEST or
            x["joint_capsule_manifest"]!=MANIFEST or x["node_count"]!=41 or
            x["observed_edge_count"]!=72 or x["recipe_edge_count"]!=36 or
            x["frontier_constant_count"]!=64 or x["selected_root_count"]!=3 or x["shared_node_count"]!=7 or
            x["acyclic_observed_graph"] is not True or x["historical_hold_retained"] is not True or
            x["raw_negative_retained"] is not True or x["exact_kernel_type"] is not True or
            x["root_trials"]!=0 or x["capsule_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["all_repository_dependencies_observed"] is not False or
            x["semantic_search_complete"] is not False or x["proof_authority"] is not False for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["graph_bytes_equal"] is not True or
        ind["raw_type_and_proof_equal"] is not True or ind["mcp_audits"]!=41 or
        ind["unobserved_module_count"]!=695 or d["controls"]!=ind["controls"]):
        raise ValueError("R49 receipt binding")
    rows={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(rows)!=41 or len(ma)!=41 or set(rows)!=set(ma) or any(
        rows[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in rows):
        raise ValueError("R49 audit binding")
    recheck(rows,graph)
    return rows

def recheck(rows,graph):
    refs=graph["recipe_edges"]
    live=prev.audit_graph(rows,refs,refs)
    if any(graph[k]!=v for k,v in live.items()) or prev.controls(rows,refs,live["observed_edges"])!=graph["controls"]:
        raise ValueError("R49 graph drift")
    return live

def names(graph):
    return sorted({n for ns in graph["unobserved_frontier"].values() for n in ns})

def observer(roots,wanted):
    """Recover actual Names via proof references; no parsing of printed names."""
    roots_expr=", ".join(chr(96)*2+typed.name(n) for n in roots)
    wanted_expr=", ".join(json.dumps(n,ensure_ascii=False) for n in wanted)
    return r'''open Lean
set_option maxHeartbeats 4000000 in
run_cmd do
  let env ← getEnv
  let roots : Array Name := #[ROOTS]
  let wanted : Array String := #[WANTED]
  let mut seen : Array Name := #[]
  for root in roots do
    let some ci := env.find? root | throwError "missing audited root"
    let some proof := ci.value? (allowOpaque := true) | throwError "missing audited body"
    for dep in proof.getUsedConstants do
      if wanted.contains dep.toString && !seen.contains dep then
        seen := seen.push dep
  let mut rows : Array Json := #[]
  for n in seen do
    match env.find? n with
    | none =>
      rows := rows.push (Json.mkObj [("name",toJson n.toString),("name_repr",toJson (reprStr n)),
        ("status",toJson "NO_ENV_DECLARATION")])
    | some ci =>
      let kind : String := match ci with
        | .axiomInfo _ => "axiom"
        | .defnInfo _ => "definition"
        | .thmInfo _ => "theorem"
        | .opaqueInfo _ => "opaque"
        | .quotInfo _ => "quotient"
        | .inductInfo _ => "inductive"
        | .ctorInfo _ => "constructor"
        | .recInfo _ => "recursor"
      let val := ci.value? (allowOpaque := true)
      let refs : Array String := match val with
        | some e => e.getUsedConstants.map Name.toString
        | none => #[]
      let origin : String := match env.getModuleIdxFor? n with
        | some i => env.allImportedModuleNames[i]!.toString
        | none => "CURRENT_REPLAY"
      let ax ← Lean.collectAxioms n
      rows := rows.push (Json.mkObj [
        ("name",toJson n.toString),("name_repr",toJson (reprStr n)),
        ("status",toJson "OBSERVED"),("kind",toJson kind),("origin",toJson origin),
        ("type_expr",toJson (reprStr ci.type)),
        ("type_constants",toJson (ci.type.getUsedConstants.map Name.toString)),
        ("universe_parameters",toJson (ci.levelParams.map Name.toString)),
        ("has_value",toJson val.isSome),("value_expr",toJson (val.map reprStr)),
        ("value_constants",toJson refs),("axioms",toJson (ax.map Name.toString)),
        ("unsafe",toJson ci.isUnsafe),("partial",toJson ci.isPartial)])
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R50_FRONTIER " ++ (toJson rows).compress)
'''.replace("ROOTS",roots_expr).replace("WANTED",wanted_expr)

def project(graph,parents,rows):
    wanted=names(graph)
    if len(wanted)!=64 or len(rows)!=64 or set(rows)!=set(wanted):
        raise ValueError("HOLD_FRONTIER_INVENTORY")
    observed={};unresolved=[]
    for n in wanted:
        x=rows[n]
        if x["name"]!=n or not x["name_repr"]:raise ValueError("HOLD_FRONTIER_NAME")
        users=sorted(k for k,ns in graph["unobserved_frontier"].items() if n in ns)
        if not users or any(n not in parents[k]["proof_constants"] for k in users):
            raise ValueError("HOLD_FRONTIER_EDGE")
        if x["status"]=="NO_ENV_DECLARATION":
            unresolved.append(n)
            observed[n]={**x,"referenced_by":users,"admission":"HOLD_UNRESOLVED"}
            continue
        if (x["status"]!="OBSERVED" or x["kind"] not in KINDS or not x["type_expr"] or not x["origin"] or
            x["has_value"]!=(x["value_expr"] is not None) or
            x["has_value"]!=(x["kind"] in VALUE_KINDS) or
            (not x["has_value"] and x["value_constants"])):
            raise ValueError("HOLD_FRONTIER_KIND")
        for key in ("type_constants","value_constants","axioms"):
            if not isinstance(x[key],list) or not all(isinstance(z,str) and z for z in x[key]):
                raise ValueError("HOLD_FRONTIER_SHAPE")
        # Observe only. A theorem body is not an admitted application.
        y={**x,"referenced_by":users,"admission":"HOLD_OBSERVATION_ONLY"}
        for key in ("type_constants","value_constants","axioms"):
            y[key]=sorted(set(x[key]))
        if set(y["axioms"])-typed.STANDARD or any(not set(y["axioms"])<=set(parents[k]["axioms"]) for k in users):
            y["admission"]="HOLD_AXIOM_BOUNDARY"
        observed[n]=y
    found={n for n,x in observed.items() if x["status"]=="OBSERVED"}
    universe=set(parents)|found
    next_value=sorted({v for n in found for v in observed[n]["value_constants"] if v not in universe})
    next_type=sorted({v for n in found for v in observed[n]["type_constants"] if v not in universe})
    kinds=dict(sorted(Counter(observed[n]["kind"] for n in found).items()))
    return {"schema":"kuuos.codeai.one-hop-frontier-observation.v1","parent_graph_key":GRAPH,
        "observations":observed,"kind_counts":kinds,"requested_count":len(wanted),"resolved_count":len(found),
        "unresolved":unresolved,"value_body_count":sum(observed[n]["has_value"] for n in found),
        "next_value_frontier":next_value,"next_type_frontier":next_type,
        "axiom_boundary_count":sum(x["admission"]=="HOLD_AXIOM_BOUNDARY" for x in observed.values()),
        "observed_parent_nodes":len(parents),"expanded_depth":1,"parent_graph_preserved":True,
        "all_repository_dependencies_observed":False,"semantic_search_complete":False,"proof_authority":False}

def controls(graph,parents,rows):
    import copy
    results={}
    def reject(k,g,r):
        try:project(g,parents,r)
        except ValueError as e:results[k]=str(e)
        else:raise ValueError("invalid frontier accepted "+k)
    bad=copy.deepcopy(rows);n=next(iter(sorted(bad)));bad.pop(n)
    reject("omitted_boundary",graph,bad)
    bad=copy.deepcopy(rows);bad[n]["name"]="KuuOSR50.Fabricated"
    reject("wrong_name",graph,bad)
    bad=copy.deepcopy(rows);found=next(k for k,x in sorted(bad.items()) if x["status"]=="OBSERVED")
    bad[found]["kind"]="fabricated_theorem"
    reject("wrong_kind",graph,bad)
    if results!={"omitted_boundary":"HOLD_FRONTIER_INVENTORY","wrong_name":"HOLD_FRONTIER_NAME","wrong_kind":"HOLD_FRONTIER_KIND"}:
        raise ValueError("frontier control drift")
    return results
