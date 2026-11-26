"""Separate exact no-go observations from compiler failure/deduplication.

Selected F55 two-chart frontier. Lexical retrieval is never a complete
semantic obstruction search. A negative theorem is reusable mathematical
evidence, not a failed candidate. An unknown or conditional-only target
must HOLD, not become a refutation or a generation authorization.
"""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
import re

from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import load_packets

PREFIX = "Kuu.LivingEngi."
MODULE = "Kuu.LivingEngi.SourceAwareOverlapDescentCriterion"
SOURCE = "formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean"
NATIVE = "formal/Kuu/LivingEngi/NativeF55CechSourceGluingObstruction.lean"
BLOBS = {SOURCE:"c3c989eff7b430faa5350d1300b4a17f531da757",
         NATIVE:"eed8c043b0ffad67572a2938329b8f1feeaf583a"}
SUBJECT = "native-f55-two-chart-source-descent"
TERMS = ["nativeF55TwoChart", "no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal",
         "no_source_promotion_of_refuted_overlapFaithfulness",
         "sourceGlobal_iff_shadowGlobal_and_overlapFaithful"]
ANCHORS = {
    "nativeF55_twoChart_raw_no_global": (NATIVE,"negative"),
    "nativeF55_twoChart_raw_incompatible": (NATIVE,"negative"),
    "nativeF55_twoChart_no_exact_source_preserving_replacement": (NATIVE,"negative"),
    "nativeF55_twoChart_shadow_glues_not_raw": (NATIVE,"mixed"),
    "nativeF55_twoChart_raw_global_not_admissible": (NATIVE,"conditional_negative"),
    "nativeF55_twoChart_trace_no_global": (NATIVE,"negative"),
    "nativeF55_twoChart_not_overlapFiberFaithful": (SOURCE,"negative"),
    "nativeF55_twoChart_refined_no_global": (SOURCE,"negative"),
    "no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal": (SOURCE,"conditional_criterion"),
    "no_source_promotion_of_refuted_overlapFaithfulness": (SOURCE,"conditional_negative"),
    "sourceGlobal_iff_shadowGlobal_and_overlapFaithful": (SOURCE,"conditional_criterion"),
    "nativeF55_twoChart_shadow_global": (NATIVE,"positive_control"),
    "nativeF55_twoChart_constant_raw_global": (NATIVE,"positive_control"),
    "nativeF55_constant_twoChart_refined_global": (SOURCE,"positive_control"),
    "nativeF55_twoChart_constant_raw_changed": (NATIVE,"source_change"),
}
# Explicit closed propositions only. Conditions for general mathematical
# questions remain outside this small selected observation.
CASES = {
    "original_raw": ("HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartRaw",
                     "nativeF55_twoChart_raw_no_global","negative"),
    "shadow": ("HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartShadow",
               "nativeF55_twoChart_shadow_global","positive"),
    "alternative_raw": ("HasGlobal northNativeF55TwoChartCover northNativeF55TwoChartConstantRaw",
                        "nativeF55_twoChart_constant_raw_global","positive"),
    "original_faithfulness": ("OverlapFiberFaithful northNativeF55TwoChartCover northNativeF55Observe northNativeF55TwoChartRaw",
                              "nativeF55_twoChart_not_overlapFiberFaithful","negative"),
    "original_refined": ("HasGlobal northNativeF55TwoChartCover (shadowSections northNativeF55TwoChartCover (sourceAwareReadout northNativeF55Observe) northNativeF55TwoChartRaw)",
                         "nativeF55_twoChart_refined_no_global","negative"),
    "alternative_refined": ("HasGlobal northNativeF55TwoChartCover (shadowSections northNativeF55TwoChartCover (sourceAwareReadout northNativeF55Observe) northNativeF55TwoChartConstantRaw)",
                            "nativeF55_constant_twoChart_refined_global","positive"),
}
NS = "KuuOSNoGoProbe"
STANDARD = {"propext","Classical.choice","Quot.sound"}

def _hold(reason, **extra):
    return {"status":"HOLD_NO_GO_REVIEW","issues":[reason],
            "candidate_generation_allowed":False,"proof_authority":False,
            "novelty_certified":False,"execution_authority":False,
            "merge_authority":False,**extra}

def recall_no_go_frontier(root:Path, observation:Mapping, subject:str) -> dict:
    """Always retain positive, negative, mixed, conditional and unknown hits.

    The fixed subject search cannot be narrowed to a positive-only name.
    Preserve parser gaps and omissions. No search result establishes novelty
    or mathematical impossibility without an actual typed witness.
    """
    if subject != SUBJECT or observation.get("scope") != "canonical_main":
        return _hold("unsupported_subject_or_noncanonical_scope")
    catalog=build_catalog(root,observation)
    parent,_=load_packets(root)
    if catalog["source_subtrees"]!=parent["source_subtrees"] or catalog["pins"]!=parent["pins"]:
        return _hold("formal_scope_changed_reobserve")
    hits=search_catalog(catalog,subject,terms=TERMS,mode="any",limit=500)
    if hits["status"]!="REVIEW_REQUIRED":
        return _hold("lexical_retrieval_incomplete",lexical_receipt=hits)
    files={f["path"]:f for f in catalog["files"]}
    anchored=[]
    for name,(path,kind) in sorted(ANCHORS.items()):
        f=files.get(path)
        if not f or f["blob"]!=BLOBS[path] or git_blob((root/path).read_bytes())!=BLOBS[path]:
            return _hold("anchor_source_changed:"+path)
        rows=[d for d in f["declarations"] if d["name_lexical"]==name and d["kind"]=="theorem"]
        if len(rows)!=1:
            return _hold("anchor_not_unique:"+name)
        anchored.append({**rows[0],"name":PREFIX+name,"observation_kind":kind})
    # Include all lexical candidates, not only name-based guesses. Labels
    # are retrieval hints; a negation in a premise is not itself a no-go.
    lexical_negative_hints=[d["id"] for d in hits["hits"] if
        re.search(r"(?:¬|≠|→\s*False|\bNot\b|\bFalse\b|_no_|_not_|_incompatible|obstruction)",
                  d["name_lexical"]+" "+d["signature_preview"],re.I)]
    result={"schema":"kuuos.codeai.no-go-recall.v1","status":"REVIEW_REQUIRED",
            "subject":subject,"source_head":observation["source_head"],"source_tree":observation["source_tree"],
            "source_subtrees":catalog["source_subtrees"],"pins":catalog["pins"],
            "catalog_digest":catalog["catalog_digest"],"lexical_receipt":hits,"anchors":anchored,
            "lexical_negative_hint_ids":lexical_negative_hints,
            "semantic_search_complete":False,"unreviewed_hits_retained":True,
            "candidate_generation_allowed":False,"proof_authority":False,"novelty_certified":False}
    result["receipt_digest"]=digest(result)
    return result

def target_preflight(recall:Mapping, target_id:str, proposition:str) -> dict:
    """Never treat a failed compiler attempt or a conditional theorem alone
    as REFUTED. Even known exact cases require a typed application receipt.
    """
    case=CASES.get(target_id)
    if recall.get("status")!="REVIEW_REQUIRED" or case is None or proposition!=case[0]:
        return _hold("unknown_or_changed_target_scope")
    return _hold("typed_application_and_independent_evidence_required",
                 target_id=target_id,proposition=proposition,witness=PREFIX+case[1],
                 expected_polarity=case[2])

def observe_selected_routes(recall:Mapping, direct:Mapping, independent:Mapping, mcp:Mapping) -> dict:
    """Project *already independently observed* exact typed applications.

    The caller must obtain the receipt lineage from actual CI; self-sealed
    JSON is not external authentication. This projects historical evidence
    only, not a proof authority or general new-research admission.
    """
    if (recall.get("status")!="REVIEW_REQUIRED" or direct!=independent
            or direct.get("recall_digest")!=recall["receipt_digest"]
            or direct.get("source_head")!=recall["source_head"]
            or direct.get("source_tree")!=recall["source_tree"]
            or mcp.get("status")!="REAL_LEAN_MCP_NO_GO_GREEN"
            or mcp.get("direct_digest")!=digest(direct)
            or direct.get("status")!="DIRECT_TYPED_NO_GO_GREEN"):
        return _hold("independent_typed_evidence_missing_or_mismatched")
    if set(direct.get("applications",{}))!=set(CASES):
        return _hold("application_inventory_incomplete")
    obs={r["name"]:r for r in direct.get("observations",[])}
    mc={r["name"]:r for r in mcp.get("observations",[])}
    if len(obs)!=len(direct.get("observations",[])) or set(obs)!=set(mc):
        return _hold("kernel_or_mcp_inventory_mismatch")
    routes={}
    for key,(proposition,witness,polarity) in CASES.items():
        a=direct["applications"][key]
        name=NS+"."+key+"_witness"
        expected_target=NS+"."+key+"_target"
        r=obs.get(name,{})
        prior=obs.get(PREFIX+witness,{})
        if (a.get("target_id")!=key or a.get("target_name")!=expected_target
                or a.get("witness_name")!=name or a.get("polarity")!=polarity
                or not a.get("exact_kernel_type_match")
                or not a.get("target_expr_repr") or not prior
                or a.get("witness_type_repr")!=r.get("type_expr_repr")
                or expected_target not in r.get("type_constants",[])
                or PREFIX+witness not in r.get("proof_constants",[])
                or set(r.get("axioms",[]))-STANDARD
                or r.get("axioms")!=mc.get(name,{}).get("axioms")
                or (polarity=="negative") != ("Not" in r.get("type_constants",[]))):
            return _hold("typed_witness_binding_mismatch:"+key)
        routes[key]={"status":"REFUTED_EXACT_TARGET" if polarity=="negative" else "REUSE_EXISTING",
            "proposition":proposition,"target_expr_digest":digest(a["target_expr_repr"]),
            "source_witness":PREFIX+witness,"application_type_expr_sha256":r["type_expr_sha256"],
            "axioms":r["axioms"],"candidate_generation_allowed":False}
    return {"status":"INDEPENDENT_SELECTED_NO_GO_ROUTES_OBSERVED","routes":routes,
            "conditional_only":"HOLD_NO_GO_REVIEW",
            "unreviewed_new_research":"HOLD_NO_GO_REVIEW",
            "semantic_search_complete":False,"candidate_generation_allowed":False,
            "proof_authority":False,"novelty_certified":False,
            "execution_authority":False,"merge_authority":False}
