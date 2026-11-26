"""Project independently checked, exact closed-target applications.

This research-only boundary cannot authenticate its own receipts, infer
semantic completeness, or authorize a provider. A caller must admit the
actual run and artifact lineage separately. A failed or partial application
is never a mathematical refutation.
"""
from __future__ import annotations
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest

MODULE="KUOS.WORLD.KuuOSRepositoryAlignmentNormalFormV0_80"
NS="KuuOSOleanR9"
STANDARD={"propext","Classical.choice","Quot.sound"}
CASES={
    "reflexive":{"target":"(7 : Nat) < 7","polarity":"negative",
                 "source":MODULE+".strict_descent_is_not_reflexive","premises":[]},
    "forward":{"target":"(3 : Nat) < 7","polarity":"positive",
               "source":MODULE+".valid_step_strictly_decreases",
               "premises":[NS+".forward_valid"]},
    "reverse":{"target":"(7 : Nat) < 3","polarity":"negative",
               "source":MODULE+".opposite_strict_steps_are_impossible",
               "premises":[NS+".forward_witness"]},
}
SOURCE_NAMES=sorted({x["source"] for x in CASES.values()})
AUDIT_NAMES=sorted(SOURCE_NAMES+[NS+".forward_valid"]+
                   [NS+"."+k+"_witness" for k in CASES])

def hold(reason,**kw):
    return {"status":"HOLD_TYPED_APPLICABILITY_REVIEW","issues":[reason],**kw,
            "candidate_generation_allowed":False,"proof_authority":False,
            "execution_authority":False,"semantic_search_complete":False}

def project(direct,independent,mcp):
    try:
        if (direct!=independent or direct["status"]!="DIRECT_EXACT_TYPED_APPLICATIONS"
                or mcp["status"]!="REAL_LEAN_MCP_R9_GREEN"
                or mcp["direct_digest"]!=digest(direct)
                or direct["proof_authority"] is not False
                or direct["unobserved_module_count"]!=695
                or direct["source_controls"]["missing_premise_defeq"] is not False
                or direct["source_controls"]["wrong_target_defeq"] is not False):
            return hold("independent_or_typed_control_evidence_missing")
        rows={r["name"]:r for r in direct["observations"]}
        audits={r["name"]:r for r in mcp["observations"]}
        types={r["name"]:r for r in direct["materialized_sources"]}
        if (set(rows)!=set(AUDIT_NAMES) or len(rows)!=len(direct["observations"])
                or set(audits)!=set(rows) or len(audits)!=len(mcp["observations"])
                or set(types)!=set(SOURCE_NAMES) or set(direct["applications"])!=set(CASES)):
            return hold("application_or_audit_inventory_mismatch")
        for name,r in rows.items():
            if (set(r["axioms"])-STANDARD or r["axioms"]!=audits[name]["axioms"]
                    or not r["type_expr_sha256"]):
                return hold("axiom_or_type_audit_mismatch:"+name)
        for name,t in types.items():
            if t["type_expr_sha256"]!=rows[name]["type_expr_sha256"]:
                return hold("source_materialization_changed:"+name)
        routes={}
        for k,case in CASES.items():
            a=direct["applications"][k];name=NS+"."+k+"_witness";row=rows[name]
            target=NS+"."+k+"_target"
            if (a["target_id"]!=k or a["target_name"]!=target or a["witness_name"]!=name
                    or a["polarity"]!=case["polarity"] or a["exact_kernel_type_match"] is not True
                    or a["witness_type_repr"]!=row["type_expr_repr"]
                    or not a["target_expr_repr"] or target not in row["type_constants"]
                    or (case["polarity"]=="negative")!=("Not" in row["type_constants"])
                    or not set([case["source"]]+case["premises"])<=set(row["proof_constants"])):
                return hold("typed_application_mismatch:"+k)
            routes[k]={"status":"REFUTED_EXACT_TARGET" if case["polarity"]=="negative" else "REUSE_EXISTING",
                       "target":case["target"],"target_expr_digest":digest(a["target_expr_repr"]),
                       "source_witness":case["source"],"source_type_sha256":types[case["source"]]["type_expr_sha256"],
                       "application_witness":name,"application_type_sha256":row["type_expr_sha256"],
                       "premise_witnesses":[{"name":p,"type_sha256":rows[p]["type_expr_sha256"]}
                                            for p in case["premises"]],
                       "axioms":row["axioms"],"candidate_generation_allowed":False}
        return {"status":"INDEPENDENT_EXACT_TYPED_ROUTES_OBSERVED","source_head":direct["source_head"],
                "source_tree":direct["source_tree"],"scope_digest":direct["scope_digest"],
                "direct_digest":digest(direct),"mcp_digest":digest(mcp),
                "r7_receipt_digest":direct["r7_receipt_digest"],
                "r8_direct_digest":direct["r8_direct_digest"],"unobserved_module_count":695,
                "routes":routes,"candidate_generation_allowed":False,"proof_authority":False,
                "execution_authority":False,"semantic_search_complete":False}
    except (KeyError,TypeError,ValueError,AttributeError):
        return hold("malformed_typed_application_receipt")

def make_request(context,target_id):
    r=context["routes"][target_id]
    result={"schema":"kuuos.codeai.exact-typed-route-request.v1","context_digest":digest(context),
            "source_head":context["source_head"],"scope_digest":context["scope_digest"],
            "target_id":target_id,"target":r["target"],"target_expr_digest":r["target_expr_digest"],
            "premise_witnesses":r["premise_witnesses"]}
    result["request_digest"]=digest(result)
    return result

def pre_provider(context,expected_context_digest,request):
    """Only exact previously checked targets; external admission is required."""
    try:
        if (context["status"]!="INDEPENDENT_EXACT_TYPED_ROUTES_OBSERVED"
                or digest(context)!=expected_context_digest
                or context["proof_authority"] is not False
                or context["semantic_search_complete"] is not False):
            return hold("unadmitted_or_changed_route_context")
        key=request["target_id"]
        if key not in context["routes"] or request!=make_request(context,key):
            return hold("target_or_premise_mismatch")
        return {**context["routes"][key],"request_digest":request["request_digest"],
                "context_digest":expected_context_digest,"candidate_generation_allowed":False,
                "proof_authority":False,"execution_authority":False,"semantic_search_complete":False,
                "synthesis":None}
    except (KeyError,TypeError,ValueError,AttributeError):
        return hold("malformed_or_unknown_target")
