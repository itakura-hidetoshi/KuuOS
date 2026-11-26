"""Whole-source obstruction discovery, not a semantic no-go oracle.

Additive to the existing positive/prior-proof gates. All named source
previews are inspected; no top-k truncation of the obstruction inventory.
Negation in a binder, a source-path hint or an inequality is NOT evidence
that the target is impossible. Exact certified routes stay separate.
"""
from __future__ import annotations
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
import json
import re
import unicodedata

from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest,git_blob
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import load_packets
from runtime.kuuos_codeai_prior_proof_kernel_research_gate_v0_5 import (
    build_kernel_memory_research_synthesis,
)
from runtime import kuuos_codeai_no_go_memory_v1 as selected
from runtime import kuuos_codeai_certified_no_go_recall_v1 as certified

# These patterns are deliberately broad retrieval hints, not a parser for
# Lean propositions. In particular "False"/"Not" in a premise is preserved.
TYPE_HINT = re.compile(r"¬|≠|(?<![\w.])(?:Not|False|IsEmpty|NoConfusion)(?![\w])|→\s*False|<\s*0\b",re.UNICODE)
NAME_HINT = re.compile(r"(?:^|[_.])(?:no|not|ne|non|false)(?:[_.]|$)|no(?:go|exact|faithful|descent|recovery|filler|unit|class|next|left|right|strict|source)|not(?:injective|surjective|admissible|equiv|compatible|faithful|global|empty|nonempty)|non(?:injective|surjective|faithful|reflection|erasing)|obstruction|impossib|counterexample|refut|contradict|collision|distinct|incompatible|cannot",re.I)
PATH_HINT = re.compile(r"nogo|obstruction|nonreflection|impossibility|noexact|nodescent|nofaithful|counterexample|nonfaithfulness",re.I)
INDEX=Path(__file__).resolve().parents[1]/"memoryos/research_prior_proof_subject_index_v0_2.json"

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKC",s).casefold() if c.isalnum())

def family(path):
    if path.startswith("formal/KUOS/Architecture/"):
        return "KUOS/Architecture"
    if path.startswith("formal/Kuu/F112/"):
        return "Kuu/F112"
    if path.startswith("formal/KUOS/"):
        return "KUOS/other"
    if path.startswith("formal/Kuu/"):
        return "Kuu/other"
    return "other"

def hold(reason,**extra):
    return {"status":"HOLD_OBSTRUCTION_REVIEW","issues":[reason],
            "synthesis":None,"candidate_generation_allowed":False,
            "proof_authority":False,"novelty_certified":False,
            "semantic_search_complete":False,**extra}

def build_obstruction_inventory(root:Path,observation:Mapping,catalog=None):
    """Inspect all named previews in the actual materialized proof tree.

    A supplied catalog is for the *same internal batch* only. External
    admission always rebuilds it rather than trusting a caller's inventory.
    """
    if observation.get("scope")!="canonical_main":
        raise ValueError("canonical source observation required")
    if catalog is None:
        catalog=build_catalog(root,observation)
    if (catalog["source_head_as_observed_by_caller"]!=observation["source_head"]
            or catalog["source_tree"]!=observation["source_tree"]
            or catalog["observation_scope"]!="canonical_main"
            or digest({k:v for k,v in catalog.items() if k!="catalog_digest"})!=catalog["catalog_digest"]):
        raise ValueError("unbound source catalog")
    # The historical v0.4/v0.5 kernel observations are immutable. If
    # their formal scope changes, keep their old provenance, never call a
    # stale observation a current match.
    parent,frontier=load_packets(root)
    packets=(parent,frontier)
    known={}
    for packet in packets:
        for row in packet["observations"]:
            known[row["lexical_id"]]=(packet,row)
    rows=[]
    parsed=0
    for f in catalog["files"]:
        path=f["path"]
        path_hint=bool(PATH_HINT.search(path))
        for d in f["declarations"]:
            parsed+=1
            hints=[]
            if TYPE_HINT.search(d["signature_preview"]):
                hints.append("negative_or_empty_type_preview")
            if NAME_HINT.search(d["name_lexical"]):
                hints.append("name_hint")
            if path_hint:
                hints.append("obstruction_module_hint")
            if not d["signature_boundary_seen"]:
                hints.append("incomplete_signature_preview")
            prior=known.get(d["id"])
            if prior:
                packet,row=prior
                # A kernel observation can contain negative syntax in a
                # premise or nested connective; retain it, don't classify.
                if TYPE_HINT.search(row["type_pretty"]):
                    hints.append("historical_kernel_type_hint")
            if not hints:
                continue
            item={**d,"family":family(path),"module":f["module_path_lexical"],
                  "source_imports":f["imports"],"hints":hints,
                  "status":"LEXICAL_REVIEW_REQUIRED",
                  "negative_conclusion_certified":False,
                  "applicability_certified":False}
            if prior:
                packet,row=prior
                exact=(packet["source_subtrees"]==catalog["source_subtrees"]
                       and packet["pins"]==catalog["pins"]
                       and row["blob"]==d["source_blob"]
                       and row["signature_preview_digest"]==d["signature_digest"])
                item["historical_kernel_observation"]={
                    "status":"EXACT_SCOPE_MATCH" if exact else "HOLD_REOBSERVE_KERNEL",
                    "historical_source_head":packet["source_head"],
                    "historical_source_tree":packet["source_tree"],
                    "historical_run":packet["provenance"]["run_id"],
                    "name":row["name"],"type_pretty":row["type_pretty"],
                    "type_expr_sha256":row["type_expr_sha256"],"axioms":row["axioms"]}
            rows.append(item)
    if parsed!=catalog["named_declaration_preview_count"]:
        raise ValueError("named declaration inventory mismatch")
    rows.sort(key=lambda x:(x["path"],x["line"],x["id"]))
    if len({x["id"] for x in rows})!=len(rows):
        raise ValueError("duplicate obstruction identity")
    gaps=[{"path":f["path"],"blob":f["blob"],"issue":f.get("parse_issue")}
          for f in catalog["files"] if f["parse_status"]=="NO_DATA"]
    result={"schema":"kuuos.codeai.whole-library-obstruction-inventory.v1",
            "source_head":observation["source_head"],"source_tree":observation["source_tree"],
            "catalog_digest":catalog["catalog_digest"],"source_subtrees":catalog["source_subtrees"],
            "pins":catalog["pins"],"named_previews_scanned":parsed,
            "lean_source_files_scanned":catalog["lean_source_file_count"],
            "hint_count":len(rows),"family_counts":dict(sorted(Counter(x["family"] for x in rows).items())),
            "hint_kind_counts":dict(sorted(Counter(h for row in rows for h in row["hints"]).items())),
            "hints":rows,"parse_gaps":gaps,"omitted_hint_count":0,
            "semantic_search_complete":False,"kernel_type_inventory_complete":False,
            "proof_authority":False,"novelty_certified":False}
    result["inventory_digest"]=digest(result)
    return result

def _terms(query,terms,target,index):
    # Bind to both ordinary prior-proof query and target. Supplement
    # recognized subjects with every direct alias and anchor declaration.
    # No caller-controlled negative-only filter or top-k removal.
    if not isinstance(query,str) or not query.strip() or not isinstance(target,str) or not target.strip():
        raise ValueError("nonempty query and target required")
    if not isinstance(terms,list) or not all(isinstance(t,str) for t in terms):
        raise ValueError("invalid prior-proof query terms")
    keys={norm(t) for t in terms}
    keys.update(norm(t) for t in re.findall(r"[^\W_]+",query+" "+target,flags=re.UNICODE))
    topic_text=norm(query+" "+target)
    topics={t["id"]:t for t in index["topics"]}
    direct=sorted(t for t,v in topics.items() if any(norm(a) in topic_text for a in v["aliases"]))
    # One-hop subject neighbors are a source-retrieval hint, not a semantic
    # equivalence between research questions.
    expanded=sorted(set(direct)|{v for t in direct for v in topics[t]["neighbors"]})
    anchors=[]
    for t in expanded:
        for a in topics[t]["anchors"]:
            anchors.append({"topic":t,"path":a["path"],"blob":a["blob"]})
        for alias in topics[t]["aliases"]:
            # Include direct subject synonyms; neighbors' exact anchor
            # modules are retained without adding every generic word.
            if t in direct:
                keys.add(norm(alias))
    # Tiny Lean tokens are overly broad lexical hints; retain the entire
    # global inventory even when a subject has no useful token.
    return sorted(k for k in keys if len(k)>=3),direct,expanded,anchors

def query_obstructions(inventory,catalog,query,terms,target):
    if (inventory["catalog_digest"]!=catalog["catalog_digest"]
            or digest({k:v for k,v in inventory.items() if k!="inventory_digest"})!=inventory["inventory_digest"]):
        raise ValueError("unbound obstruction inventory")
    index=json.loads(INDEX.read_text(encoding="utf-8"))
    keys,direct,expanded,anchors=_terms(query,terms,target,index)
    files={f["path"]:f for f in catalog["files"]}
    changed=[a for a in anchors if a["path"] not in files or files[a["path"]]["blob"]!=a["blob"]]
    anchor_paths={a["path"] for a in anchors}
    rows=[]
    for d in inventory["hints"]:
        hay=norm(d["name_lexical"]+" "+d["signature_preview"]+" "+d["path"])
        matched=[k for k in keys if k in hay]
        if matched or d["path"] in anchor_paths:
            rows.append({"id":d["id"],"path":d["path"],"source_blob":d["source_blob"],
                         "signature_digest":d["signature_digest"],"hints":d["hints"],
                         "matched_terms":matched,"curated_anchor_module":d["path"] in anchor_paths})
    result={"schema":"kuuos.codeai.obstruction-subject-recall.v1",
            "source_head":inventory["source_head"],"source_tree":inventory["source_tree"],
            "inventory_digest":inventory["inventory_digest"],"catalog_digest":inventory["catalog_digest"],
            "subject_index_digest":digest(index),"query":query,"target":target,"terms":terms,
            "expanded_terms":keys,"direct_topics":direct,"expanded_topics":expanded,
            "anchor_scope_issues":changed,"matches":rows,"match_count":len(rows),
            "global_hint_count":inventory["hint_count"],
            "outside_query_count":inventory["hint_count"]-len(rows),"omitted_matches":0,
            "parse_gaps":inventory["parse_gaps"],
            "status":"HOLD_REOBSERVE" if changed or inventory["parse_gaps"] else
                     "REVIEW_REQUIRED" if rows else "HOLD_NO_DATA",
            "semantic_search_complete":False,"proof_authority":False,"novelty_certified":False}
    result["receipt_digest"]=digest(result)
    return result

def recall_obstructions(root,observation,query,terms,target):
    catalog=build_catalog(root,observation)
    inventory=build_obstruction_inventory(root,observation,catalog)
    return query_obstructions(inventory,catalog,query,terms,target)

def review_obstruction_receipt(receipt,review,synthesis_request,repository_files,root):
    """Review every retrieved hint; no claimed applicability promotes REFUTED.

    A reviewed non-applicability is a human/model comparison assertion,
    not a Lean proof. An applicable/unresolved item requires typed evidence
    and holds. Original prior-proof gates still own residual admission.
    """
    if receipt["status"]!="REVIEW_REQUIRED":
        return hold(receipt["status"],obstruction_receipt=receipt)
    if not isinstance(review,Mapping) or not isinstance(synthesis_request,Mapping):
        return hold("missing_obstruction_review_or_request")
    if (review.get("obstruction_receipt_digest")!=receipt["receipt_digest"]
            or review.get("target")!=receipt["target"]
            or review.get("synthesis_request_binding")!=digest(dict(synthesis_request))):
        return hold("unbound_obstruction_review")
    if not isinstance(repository_files,Mapping):
        return hold("missing_source_context")
    by_id={r["id"]:r for r in receipt["matches"]}
    seen=set()
    missing_sources=set()
    verified_sources={}
    issues=[]
    comparisons=review.get("obstruction_comparisons")
    if not isinstance(comparisons,list):
        return hold("missing_obstruction_comparisons")
    for row in comparisons:
        if not isinstance(row,Mapping) or not isinstance(row.get("id"),str):
            issues.append("invalid_obstruction_comparison")
            continue
        i=row["id"]; expected=by_id.get(i)
        if expected is None or i in seen:
            issues.append("unknown_or_duplicate_obstruction:"+i);continue
        seen.add(i)
        if (row.get("source_blob")!=expected["source_blob"]
                or row.get("signature_digest")!=expected["signature_digest"]
                or any(not isinstance(row.get(k),str) or not row[k].strip()
                       for k in ("assumptions_comparison","conclusion_comparison","reason"))):
            issues.append("unbound_obstruction_comparison:"+i);continue
        disposition=row.get("disposition")
        if disposition!="reviewed_not_applicable":
            # Includes a claimed applicable refutation: require a checked
            # exact typed witness, rather than trusting this review.
            issues.append("typed_applicability_unresolved:"+i)
        path=expected["path"]
        if path not in verified_sources:
            data=repository_files.get(path)
            local=root/path
            verified_sources[path]=(isinstance(data,str) and not local.is_symlink()
                and local.resolve().is_relative_to(root.resolve())
                and git_blob(data.encode("utf-8"))==expected["source_blob"]
                and local.read_bytes()==data.encode("utf-8"))
        if not verified_sources[path]:
            missing_sources.add(path)
    if seen!=set(by_id):
        issues.append("unreviewed_obstruction_hits:"+str(len(set(by_id)-seen)))
    if missing_sources:
        issues.append("missing_obstruction_source_context:"+str(len(missing_sources)))
    # Exact selected propositions must use certified typed route recall,
    # even if a caller tries to label every hint as not applicable.
    if any(norm(receipt["target"])==norm(c[0]) for c in selected.CASES.values()):
        issues.append("selected_exact_target_requires_certified_route")
    if issues:
        return hold("obstruction_review_incomplete",review_issues=issues)
    return {"status":"OBSTRUCTION_REVIEW_HINT_ONLY","issues":[],
            "obstruction_receipt_digest":receipt["receipt_digest"],
            "review_assertions_only":True,"candidate_generation_allowed":False,
            "downstream_prior_proof_review_required":True,
            "proof_authority":False,"novelty_certified":False,"semantic_search_complete":False}

def obstruction_context_text(review):
    # Exclude the binding to the final synthesis request from the text
    # inside that request; otherwise a digest self-reference is required.
    context={k:v for k,v in review.items() if k!="synthesis_request_binding"}
    return "KuuOS obstruction review (assertions only, not proof):\n"+json.dumps(
        context,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def build_obstruction_reviewed_research_synthesis(*,root,observation,kernel_receipt,
        mathematical_review,recall_receipt,obstruction_receipt=None,obstruction_review=None,
        subject_receipt=None,**kwargs):
    """Additive pre-provider boundary for residual research.

    Not globally installed yet. The existing v0.5/v0.3/v0.2/v0.1 chain
    remains unchanged. Any missing, stale or incomplete obstruction review
    prevents forwarding. This cannot prove absence of every semantic no-go.
    """
    try:
        lex=kernel_receipt["lexical_receipt"]
        target=mathematical_review["target"]
        fresh=recall_obstructions(root,observation,lex["query"],lex["terms"],target)
        if fresh!=obstruction_receipt:
            return hold("stale_or_changed_obstruction_recall")
        check=review_obstruction_receipt(fresh,obstruction_review,kwargs.get("synthesis_request"),
                                        kwargs.get("repository_files"),root)
        if check["status"]!="OBSTRUCTION_REVIEW_HINT_ONLY":
            return {**check,"obstruction_receipt_digest":fresh["receipt_digest"]}
        # The obstruction review must be present in the same provider
        # intent that all older gates bind. Do not mutate/reseal it here.
        context=obstruction_context_text(obstruction_review)
        intent=kwargs["synthesis_request"].get("intent_text")
        if not isinstance(intent,str) or context not in intent:
            return hold("obstruction_context_missing_from_provider_intent")
        downstream=build_kernel_memory_research_synthesis(root=root,observation=observation,
            kernel_receipt=kernel_receipt,mathematical_review=mathematical_review,
            recall_receipt=recall_receipt,subject_receipt=subject_receipt,**kwargs)
        return {"status":downstream["status"],"obstruction_review":check,
                "downstream":downstream,"synthesis":downstream["synthesis"],
                "proof_authority":False,"novelty_certified":False}
    except (ValueError,TypeError,KeyError,OSError,AttributeError,RuntimeError) as exc:
        return hold(type(exc).__name__+":"+str(exc))
