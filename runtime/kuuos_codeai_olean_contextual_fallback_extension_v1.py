"""R43: append a context-bound route from independently admitted R42.
No original memory or capsule bytes are replaced; hits require fresh Lean.
A missing extension record is HOLD, not a negative theorem.
"""
from __future__ import annotations
import copy
from runtime import kuuos_codeai_olean_contextual_capsule_fallback_v1 as prev
from runtime import kuuos_codeai_olean_general_application_v1 as typed
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
base=prev.base
DIRECT="d4de607ea7d30e4d18de259f428339a7dcc5850f30dd69024016e651b709fc6d"
MCP="28a883568ae2319adfe0fb86ae2ca442320ea7ec8fc4089c6fa9e7b37392dd2d"
PARENT=prev.LAYER
NS="KuuOSR43Replay"
def project(d,mp,ind,index,mem,qs,obs):
    if (old.digest(d)!=DIRECT or old.digest(mp)!=MCP or
        d["status"]!="R42_DIRECT_CONTEXTUAL_CAPSULE_FALLBACK" or
        mp["status"]!="R42_REAL_MCP_GREEN" or mp["direct_digest"]!=DIRECT or
        ind["status"]!="R42_INDEPENDENT_CONTEXTUAL_CAPSULE_FALLBACK_GREEN" or
        ind["direct_digest"]!=DIRECT or ind["mcp_digest"]!=MCP or
        any(x["source_head"]!=base.CURRENT or x["source_tree"]!=base.CURRENT_TREE or
            x["scope_digest"]!=old.SCOPE for x in (d,ind)) or
        index["key"]!=PARENT or base.portable.seal(index)["key"]!=PARENT or
        mem["key"]!=prev.prev.LAYER or base.portable.seal(mem)["key"]!=mem["key"] or
        index["parent_capsule_layer"]!=mem["key"] or
        any(x["dispatch_layer_key"]!=PARENT or x["capsule_layer_key"]!=mem["key"] or
            x["capsule_manifest"]!=prev.prev.prev.MANIFEST for x in (d,ind)) or
        ind["parent_bytes_preserved"] is not True or ind["raw_type_and_proof_equal"] is not True or
        ind["imported_certified_capsule"] is not True or ind["mcp_audits"]!=17 or
        ind["fallback_witnesses"]!=1 or ind["root_trials"]!=7 or
        any(x["capsule_rebuilds"]!=0 or x["provider_calls"]!=0 or
            x["semantic_search_complete"] is not False or x["proof_authority"] is not False
            for x in (d,ind)) or ind["unobserved_module_count"]!=695):
        raise ValueError("R42 evidence binding")
    if d["requests"]!={k:qs[k] for k in d["requests"]} or d["observations"]!={k:obs[k] for k in d["observations"]}:
        raise ValueError("live context drift")
    q=qs["alternate"];o=obs["alternate"]
    if (not o["aligned"] or q["target"]!=base.cm.prev.context_target(q) or
        prev.prev.dispatch(index,index,q,o,base.CURRENT)!=d["decisions"]["alternate"] or
        d["decisions"]["alternate"]["status"]!="HOLD_CAPSULE_MISS" or
        d["fallback"]["status"]!="INDEXED_APPLICATION_REQUIRED" or len(d["witnesses"])!=1):
        raise ValueError("not an aligned admitted fallback")
    hist={x["name"]:x for x in d["fresh_application"]["observations"]}
    ma={x["name"]:x["axioms"] for x in mp["audits"]}
    if len(hist)!=17 or len(ma)!=17 or set(hist)!=set(ma) or any(
        hist[n]["axioms"]!=ma[n] or set(ma[n])-typed.STANDARD for n in hist):
        raise ValueError("R42 audit binding")
    w,x=next(iter(d["witnesses"].items()))
    c=x["source"];r=x["request"];z=x["application"]
    typed.validate(r)
    if (d["fallback"]["matches"]!=[c] or ind["selected_sources"]!=[c["name"]] or
        r["source"]!=c["name"] or r["module"]!=c["module"] or r["arguments"]!=[] or
        r["target"]!=q["target"] or r["polarity"]!=c["polarity"] or r["polarity"]!="positive" or
        typed.names(r)[1]!=w or z["witness_name"]!=w or z["exact_kernel_type_match"] is not True or
        z["target_expr_repr"]!=o["goal_expr"] or z["witness_type_repr"]!=hist[w]["type_expr_repr"] or
        c["type_expr"]!=hist[c["name"]]["type_expr_repr"] or c["name"] not in hist[w]["proof_constants"] or
        not set(hist[w]["axioms"])<=set(hist[c["name"]]["axioms"])):
        raise ValueError("typed route drift")
    route={"source":c,"application_request":r,"historical_witness":w,
           "historical_witness_digest":old.digest(hist[w]),"source_observation":hist[c["name"]],
           "historical_application":z}
    return base.portable.seal({"schema":"kuuos.codeai.contextual-fallback-extension.v1",
        "parent_dispatch_layer":PARENT,"source_head":base.CURRENT,"source_tree":base.CURRENT_TREE,
        "scope_digest":old.SCOPE,"r42_direct_digest":DIRECT,"r42_mcp_digest":MCP,
        "records":[{"request":q,"goal_expr":o["goal_expr"],"context_exprs":o["context_exprs"],
                    "polarity":"positive","routes":[route]}],
        "semantic_search_complete":False,"proof_authority":False})

def dispatch(index,extension,trusted,q,obs,head):
    def hold(s):return {"status":s,"routes":[],"proof_authority":False}
    if (index.get("key")!=PARENT or base.portable.seal(index)["key"]!=PARENT or
        extension.get("key")!=base.portable.seal(extension)["key"]):
        return hold("HOLD_EXTENSION_INTEGRITY")
    if extension!=trusted:return hold("HOLD_UNADMITTED_EXTENSION")
    if (head!=base.CURRENT or extension["source_head"]!=head or
        extension["source_tree"]!=base.CURRENT_TREE or extension["scope_digest"]!=old.SCOPE or
        extension["parent_dispatch_layer"]!=PARENT):
        return hold("HOLD_EXTENSION_SCOPE")
    decision=prev.prev.dispatch(index,index,q,obs,head)
    if decision["status"]!="HOLD_CAPSULE_MISS":return decision
    matches=[r for r in extension["records"] if r["goal_expr"]==obs["goal_expr"] and
             r["context_exprs"]==obs["context_exprs"] and all(q[k]==r["request"][k] for k in
             ("target","context_args","context_modules","mode"))]
    if len(matches)>1:return hold("HOLD_CONFLICT")
    if not matches:
        return hold("HOLD_CONTEXT_MISMATCH" if any(r["goal_expr"]==obs["goal_expr"] for r in extension["records"])
                    else "HOLD_UNREGISTERED_TARGET")
    r=matches[0]
    return {"status":"EXACT_FALLBACK_MEMORY_APPLICATION_REQUIRED","polarity":r["polarity"],
            "routes":r["routes"],"root_trials":0,"proof_authority":False}
