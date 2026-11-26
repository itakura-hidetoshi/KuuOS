#!/usr/bin/env python3
"""Actual canonical corpus regression for untruncated obstruction discovery.
No Lean recomputation, no new mathematics, and no synthetic authority.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from collections import Counter

ROOT=Path.cwd().resolve()
INSTALL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(INSTALL))
from runtime import kuuos_codeai_whole_library_obstruction_recall_v1 as m
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation

ANCHORS={
    "formal/Kuu/F112/PolygonNativeF55P92OriginalUnitNaturalityNoGo.lean":(
        "2a339e216891620cda270580ab5be428431f5b9b",
        ["nativeF55P92_original_unit_naturality_no_filler",
         "northNativeF55P92_original_unit_naturality_no_filler"]),
    "formal/Kuu/F112/PolygonNativeC60PhysicalBinarySizeNonerasingNoGo.lean":(
        "b17f5358f97fa40d01a83cc100d3989a68c7d642",
        ["nativeK5BPNonerasing_no_singleton_BG","nativeK5BPNonerasing_no_all_BG"]),
    "formal/Kuu/F112/PolygonNativeC60PhysicalParallelBoundaryNoGo.lean":(
        "45e2053cffbd89545c16e5d8c9b678f8a023803d",
        ["nativeK5BKExchange_no_sixteen_cell","nativeK5BKExchange_no_strict_iso",
         "nativeK5BKParallelNaturality_has_comparison"]),
    "formal/KUOS/Architecture/QiWuxingGK5CHP77UniformFiniteAncestorTowerObstructionV5_63.lean":(
        "5363ddaa4429219d451c6ced4cd78e84d25c5eb2",
        ["selectedRawCongruentFiniteTower_notInjective",
         "selectedRawCongruentFiniteTower_noNextDecoder",
         "selectedRawCongruentFiniteTower_noClassDecoder"]),
    "formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean":(
        "c3c989eff7b430faa5350d1300b4a17f531da757",
        ["no_sourceGlobal_iff_no_overlapFaithful_of_shadowGlobal",
         "no_source_promotion_of_refuted_overlapFaithfulness"]),
}
QUERIES={
    "f112-unit":("F112 original unit naturality",["F55","naturality","unit"],
                "original unit naturality cell existence",0),
    "c60-size":("C60 binary size nonerasing",["C60","nonerasing","whiskering"],
                "singleton whiskering equivariance with source size nonerasing",1),
    "c60-boundary":("C60 parallel boundary exchange",["parallel","boundary","exchange"],
                "strict isomorphism between exchange routes",2),
    "qi-tower":("Qi GK5 finite ancestor tower",["finite","ancestor","tower"],
                "faithful finite observation and class decoder",3),
    "source-descent":("source overlap descent",["source","overlap","descent"],
                "raw global gluing and overlap faithfulness",4),
}
def need(ok,why):
    if not ok:
        raise ValueError(why)

def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")

def run(head,out):
    obs=github_observation(head,"canonical_main")
    catalog=build_catalog(ROOT,obs)
    inv=m.build_obstruction_inventory(ROOT,obs,catalog)
    need(inv["named_previews_scanned"]==catalog["named_declaration_preview_count"]
         and inv["omitted_hint_count"]==0 and not inv["semantic_search_complete"]
         and not inv["kernel_type_inventory_complete"],"inventory boundary mismatch")
    rows={(d["path"],d["name_lexical"]):d for d in inv["hints"]}
    need(len(rows)==len(inv["hints"]),"ambiguous lexical declaration identities")
    anchor_ids={}
    for path,(blob,names) in ANCHORS.items():
        ids=[]
        for name in names:
            d=rows[(path,name)]
            need(d["source_blob"]==blob and not d["negative_conclusion_certified"]
                 and not d["applicability_certified"],"anchor evidence mismatch:"+name)
            ids.append(d["id"])
        anchor_ids[path]=ids
    save(out/"obstruction-inventory.json",inv)
    results={}
    paths=list(ANCHORS)
    for key,(query,terms,target,idx) in QUERIES.items():
        rec=m.query_obstructions(inv,catalog,query,terms,target)
        need(rec["match_count"]+rec["outside_query_count"]==inv["hint_count"]
             and rec["omitted_matches"]==0 and len(rec["matches"])==rec["match_count"],
             "query silently omitted inventory")
        need(set(anchor_ids[paths[idx]])<={d["id"] for d in rec["matches"]},
             "subject-first obstruction retrieval omitted observed anchors:"+key)
        need(rec["status"] in ("REVIEW_REQUIRED","HOLD_REOBSERVE"),"missing subject result")
        save(out/(key+".json"),rec)
        results[key]={"matches":rec["match_count"],"outside_query":rec["outside_query_count"],
                      "status":rec["status"],"receipt_digest":rec["receipt_digest"],
                      "required_anchor_hits":len(anchor_ids[paths[idx]])}
    # Unknown wording cannot become permission or refutation; no global
    # search-completeness claim is made. Existing historical witnesses stay.
    unknown=m.query_obstructions(inv,catalog,"zzzzkuuunindexednonce",["zzzzkuuunindexednonce"],
                                 "zzzzkuuunindexedtarget")
    need(unknown["status"] in ("HOLD_NO_DATA","HOLD_REOBSERVE"),"unknown query incorrectly admitted")
    # Exact actual-source tests of pre-provider boundary. The review rows
    # below are deliberate adversarial fixtures, NOT mathematical reviews.
    query,terms,target,_=QUERIES["source-descent"]
    rec=m.query_obstructions(inv,catalog,query,terms,target)
    request={"intent_text":"negative boundary test; not a research proposal"}
    review={"target":target,"obstruction_receipt_digest":rec["receipt_digest"],
            "synthesis_request_binding":digest(request),"obstruction_comparisons":[]}
    missing=m.review_obstruction_receipt(rec,review,request,{},ROOT)
    need(missing["status"]=="HOLD_OBSTRUCTION_REVIEW","empty review allowed")
    one=rec["matches"][0]
    alleged={**review,"obstruction_comparisons":[{"id":one["id"],
        "source_blob":one["source_blob"],"signature_digest":one["signature_digest"],
        "assumptions_comparison":"test fixture only","conclusion_comparison":"test fixture only",
        "reason":"adversarial claimed refutation, not proof","disposition":"applicable_refutation"}]}
    source_files={one["path"]:(ROOT/one["path"]).read_text(encoding="utf-8")}
    refused=m.review_obstruction_receipt(rec,alleged,request,source_files,ROOT)
    need(refused["status"]=="HOLD_OBSTRUCTION_REVIEW" and not refused["proof_authority"],
         "asserted refutation treated as proof")
    changed=m.review_obstruction_receipt(rec,dict(review,obstruction_receipt_digest="0"*64),request,{},ROOT)
    need(changed["status"]=="HOLD_OBSTRUCTION_REVIEW","stale receipt allowed")
    ctx=m.obstruction_context_text(review)
    req2={"intent_text":ctx}
    bound=dict(review,synthesis_request_binding=digest(req2))
    need(m.obstruction_context_text(bound)==ctx,"request digest context recursion")
    # Exercise the actual new wrapper (not merely a standalone checker)
    # with exact source inputs but omitted obstruction review. A callback
    # would raise if the older provider path were reached.
    calls=[]
    def forbidden(*a,**k):
        calls.append("provider")
        raise ValueError("provider not allowed")
    result=m.build_obstruction_reviewed_research_synthesis(
        root=ROOT,observation=obs,kernel_receipt={"lexical_receipt":{"query":query,"terms":terms}},
        mathematical_review={"target":target},recall_receipt={},
        obstruction_receipt=rec,obstruction_review=None,
        synthesis_request=request,repository_files={},provider_adapters=[forbidden])
    need(result["status"]=="HOLD_OBSTRUCTION_REVIEW" and result["synthesis"] is None and not calls,
         "missing mandatory obstruction review reached generation")
    current=github_observation(head,"canonical_main")
    need(current==obs,"canonical source changed during replay")
    receipt={"schema":"kuuos.codeai.whole-library-obstruction-recall-replay.v1",
             "head":head,"tree":obs["source_tree"],"catalog_digest":catalog["catalog_digest"],
             "inventory_digest":inv["inventory_digest"],
             "named_previews_scanned":inv["named_previews_scanned"],
             "lean_source_files_scanned":inv["lean_source_files_scanned"],
             "obstruction_hint_count":inv["hint_count"],"family_counts":inv["family_counts"],
             "hint_kind_counts":inv["hint_kind_counts"],
             "omitted_hint_count":inv["omitted_hint_count"],"parse_gap_count":len(inv["parse_gaps"]),
             "known_source_anchor_count":sum(map(len,anchor_ids.values())),
             "subject_retrievals":results,"unknown_subject_hold":True,
             "review_boundary_checks":5,"provider_calls":len(calls),"new_lean_executions":0,
             "kernel_type_inventory_complete":False,"semantic_search_complete":False,
             "proof_authority":False,"novelty_certified":False}
    save(out/"receipt.json",receipt)
    print("KUUOS_WHOLE_LIBRARY_OBSTRUCTION_GREEN",json.dumps(receipt,ensure_ascii=False,sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True);p.add_argument("--out",type=Path,required=True)
    p.add_argument("--first",type=Path)
    a=p.parse_args();out=a.out.resolve()
    need(out.is_relative_to(ROOT/"artifacts"),"isolated output required")
    out.mkdir(parents=True,exist_ok=True)
    receipt=run(a.head,out)
    if a.first:
        need(json.loads(a.first.read_text())==receipt,"independent obstruction inventory differed")
        print("KUUOS_WHOLE_LIBRARY_OBSTRUCTION_INDEPENDENT",digest(receipt),flush=True)

if __name__=="__main__":
    main()
