"""R10 versioned research synthesis entry, before the provider boundary.

Only historical exact closed targets are admitted. No lookup miss, caller
assertion, or failed proof authorizes synthesis. Residual generation must
later pass the original research gates AND a separately admitted authority.
This module does not authenticate GitHub: the caller must independently
observe canonical source and admit the fixed run/artifact lineage.
"""
from __future__ import annotations

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from runtime.kuuos_codeai_olean_exact_materialization_preflight_v1 import prepare
from runtime import kuuos_codeai_olean_typed_route_preflight_v1 as typed

HEAD="e1d754e8e0fc9382001a2e698751aa11d4272b84"
TREE="bdf2e81fc2cf702481b80e7079e59b1b47836013"
SCOPE="2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b"
R7="b47968f3f9983c2c938b6d268d0ee718679936c20748bc21b83c665f8121af54"
R8="08acb4b9a67329f6433daeb655691a9850b9c4f2ea0acaad739185864ff8e109"
R9_DIRECT="3a1559f587f1dc85573b285fc8c6dd0d341d406d3fa31716d98af32d022b1cb1"
R9_MCP="457aded4cae8c6b3d9d1d7b76f7cd585970dd5597e317fd264d409e1cba1206b"
R9_CONTEXT="c3ffa5968be2b9549d520f01150c0d8d53f38126c39d222e3d9f1b086255cf48"

def hold(reason, **evidence):
    return {"status":"HOLD_TYPED_APPLICABILITY_REVIEW", "issues":[reason],
            **evidence, "synthesis":None, "provider_calls":0,
            "candidate_generation_allowed":False, "proof_authority":False,
            "execution_authority":False, "merge_authority":False,
            "semantic_search_complete":False, "novelty_certified":False}

def admitted_context(index_receipt, direct, independent, mcp, routes, replay):
    """Fixed historical content binding. Not issuer authentication."""
    if (digest(index_receipt)!=R7 or digest(direct)!=R9_DIRECT
            or independent!=direct or digest(mcp)!=R9_MCP
            or digest(routes)!=R9_CONTEXT
            or direct["source_head"]!=HEAD or direct["source_tree"]!=TREE
            or direct["scope_digest"]!=SCOPE or direct["r7_receipt_digest"]!=R7
            or direct["r8_direct_digest"]!=R8
            or replay["status"]!="INDEPENDENT_OLEAN_R9_GREEN"
            or replay["direct_digest"]!=R9_DIRECT or replay["mcp_digest"]!=R9_MCP
            or replay["context_digest"]!=R9_CONTEXT
            or replay["unobserved_module_count"]!=695
            or replay["hold_controls"]!=8 or replay["provider_calls"]!=0):
        raise ValueError("historical receipt binding mismatch")
    fresh=typed.project(direct,independent,mcp)
    if fresh!=routes or digest(fresh)!=R9_CONTEXT:
        raise ValueError("typed context projection changed")
    return fresh

def build_olean_bound_research_synthesis(
        *, db, index_receipt, direct, independent, mcp, routes, replay,
        observation, target, target_request=None, terms=None, selections=None,
        provider_adapters=(), **legacy_synthesis_arguments):
    """Versioned entry for mathematical research, not ordinary code repair.

    Accept the provider input shape but do not invoke a provider for exact
    reuse/refutation or unresolved cases. There is deliberately no residual
    generation lease in R10; legacy arguments cannot override this boundary.
    """
    try:
        if (observation["repository"]!="itakura-hidetoshi/KuuOS"
                or observation["scope"]!="canonical_main"
                or observation["source_head"]!=HEAD or observation["source_tree"]!=TREE):
            return hold("canonical_source_changed")
        if not isinstance(target,str) or not target.strip():
            return hold("explicit_formal_target_required")
        context=admitted_context(index_receipt,direct,independent,mcp,routes,replay)
        if target_request is None:
            plan=prepare(db,index_receipt,R7,HEAD,terms or [],target,selections or [])
            return hold("residual_typed_review_and_separate_generation_authority_required",
                        search_plan=plan)
        # Reproduce the exact historical search plan without recompiling.
        plan=prepare(db,index_receipt,R7,HEAD,typed.SOURCE_NAMES,
                     "Exact closed strict descent applicability review",
                     [{"module":typed.MODULE,"name":n} for n in typed.SOURCE_NAMES])
        if (plan["status"]!="HOLD_TYPED_APPLICABILITY_REVIEW"
                or plan["preflight_digest"]!=direct["preflight_digest"]
                or len(plan["search"]["unobserved_modules"])!=695
                or plan["search"]["omitted_matches"]!=0):
            return hold("index_preflight_changed",search_plan=plan)
        materials={r["name"]:r for r in direct["materialized_sources"]}
        if set(materials)!=set(typed.SOURCE_NAMES):
            return hold("materialization_inventory_changed",search_plan=plan)
        for req in plan["requests"]:
            row=materials[req["name"]]
            if (row["module"]!=req["module"] or row["request_digest"]!=req["request_digest"]
                    or row["artifact_binding_digest"]!=digest(req["binding"])):
                return hold("materialization_request_changed",search_plan=plan)
        if not isinstance(target_request,dict) or target_request.get("target")!=target:
            return hold("target_binding_mismatch",search_plan=plan)
        result=typed.pre_provider(context,R9_CONTEXT,target_request)
        if result["status"] not in ("REUSE_EXISTING","REFUTED_EXACT_TARGET"):
            return hold("exact_typed_route_unavailable",search_plan=plan,typed_review=result)
        return {**result,"search_plan":plan,"materialized_sources":list(materials.values()),
                "provider_calls":0,"merge_authority":False,"novelty_certified":False,
                "source_tree":TREE,"historical_r9_context_digest":R9_CONTEXT}
    except (KeyError,TypeError,ValueError,AttributeError,OSError):
        return hold("invalid_or_unadmitted_evidence")
