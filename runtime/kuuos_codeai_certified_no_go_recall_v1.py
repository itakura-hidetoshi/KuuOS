"""Read-only reuse of independently observed exact no-go routes.

This bounded entry point is a pre-provider gate, not a proof authority,
and never treats absence of a matched negative theorem as permission.
For unknown/new targets a separate typed obstruction review is required.
Historical artifacts are authenticated by the caller via GitHub metadata
and exact content digests; no proof or provider execution is performed here.
"""
from __future__ import annotations
from collections.abc import Mapping
from pathlib import Path
import json

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest,git_blob
from runtime import kuuos_codeai_no_go_memory_v1 as selected
from scripts.ci_verified_lean_project_cache_v1 import make_scope

LINEAGE_PATH="memoryos/codeai_selected_no_go_certified_lineage_v1.json"
LINEAGE_BLOB="17dce4346c910024f4428e5ff90a879933e77be5"
INSTALL=Path(__file__).resolve().parents[1]

def load_lineage():
    path=INSTALL/LINEAGE_PATH
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(INSTALL):
        raise ValueError("missing or unsafe selected no-go lineage")
    raw=path.read_bytes()
    if git_blob(raw)!=LINEAGE_BLOB:
        raise ValueError("immutable selected no-go lineage blob mismatch")
    p=json.loads(raw)
    if (p["schema"]!="kuuos.codeai.selected-no-go-certified-lineage.v1"
            or any(p[k] is not False for k in ("semantic_search_complete","proof_authority",
                "novelty_certified","execution_authority","merge_authority"))):
        raise ValueError("lineage authority mismatch")
    return p

def hold(reason,**extra):
    return {"status":"HOLD_NO_GO_REVIEW","issues":[reason],
            "candidate_generation_allowed":False,"synthesis":None,
            "semantic_search_complete":False,"proof_authority":False,
            "novelty_certified":False,"execution_authority":False,
            "merge_authority":False,**extra}

def validate_historical_bundle(bundle:Mapping):
    """Content binding, not external issuer authentication.

    The artifact reader must obtain completed job, step and artifact lineage
    from GitHub. The fixed expected digests prohibit swapping in self-sealed
    historical observations. Both negative and positive cases are retained.
    """
    p=load_lineage()
    if (digest(bundle["direct"])!=p["direct_digest"]
            or digest(bundle["mcp"])!=p["mcp_digest"]
            or digest(bundle["routes"])!=p["route_digest"]):
        raise ValueError("historical evidence digest mismatch")
    d=bundle["direct"]; r=bundle["recall"]; mp=bundle["mcp"]
    if (r["receipt_digest"]!=digest({k:v for k,v in r.items() if k!="receipt_digest"})
            or d["recall_digest"]!=r["receipt_digest"]
            or r["source_head"]!=p["historical_source_head"]
            or r["source_tree"]!=p["historical_source_tree"]
            or d["scope_digest"]!=p["scope_digest"]
            or r["subject"]!=p["subject"]
            or bundle["independent_direct"]!=d
            or len(d["observations"])!=p["observed_declarations"]
            or len(r["anchors"])!=p["anchors"]):
        raise ValueError("historical source or inventory mismatch")
    routes=selected.observe_selected_routes(r,d,bundle["independent_direct"],mp)
    if (routes!=bundle["routes"]
            or {k:v["status"] for k,v in routes["routes"].items()}!=p["routes"]):
        raise ValueError("historical route projection mismatch")
    return p,r,routes

def recall_certified_no_go(*,root:Path,observation:Mapping,proof_scope:Mapping,
                            bundle:Mapping,subject:str):
    """Reuse exact proof scope; keep original and current HEAD distinct.

    No lookup miss, lexical match, compiler failure, or timeout can give
    REFUTED. Broader semantics and unknown subjects remain NO_DATA.
    """
    try:
        p,historical,routes=validate_historical_bundle(bundle)
        root=root.resolve()
        if (subject!=p["subject"] or observation.get("scope")!="canonical_main"
                or observation.get("repository")!=p["repository"]):
            return hold("unsupported_subject_or_noncanonical_scope")
        if (make_scope({k:tuple(v) for k,v in proof_scope["entries"].items()})!=proof_scope
                or digest(proof_scope)!=p["scope_digest"]):
            return hold("proof_scope_changed")
        entries={e["path"]:e for e in observation["root_entries"]}
        for name,(mode,kind,blob) in proof_scope["entries"].items():
            if "/" not in name and (name not in entries or entries[name]["sha"]!=blob
                                     or entries[name]["mode"]!=mode):
                return hold("proof_root_entry_changed:"+name)
            if kind=="blob":
                path=root/name
                if (not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root)
                        or git_blob(path.read_bytes())!=blob
                        or ("100755" if path.stat().st_mode & 0o100 else "100644")!=mode):
                    return hold("proof_scope_file_changed:"+name)
        if (root/"lakefile.lean").exists():
            return hold("alternate_lake_configuration")
        fresh=selected.recall_no_go_frontier(root,observation,subject)
        if fresh["status"]!="REVIEW_REQUIRED":
            return hold("current_obstruction_recall_incomplete",current_recall=fresh)
        # Compare actual anchored inventories and all lexical hits, including
        # unknown/unreviewed and parser gaps, not just negative witnesses.
        # A metadata-only HEAD change is not a new mathematical scope.
        for k in ("subject","source_subtrees","pins","anchors","lexical_negative_hint_ids"):
            if fresh[k]!=historical[k]:
                return hold("current_obstruction_inventory_changed:"+k,current_recall=fresh)
        for k in ("hits","parse_gaps","total_hits","omitted_hits","source_import_candidates"):
            if fresh["lexical_receipt"][k]!=historical["lexical_receipt"][k]:
                return hold("current_lexical_inventory_changed:"+k,current_recall=fresh)
        context={"schema":"kuuos.codeai.certified-selected-no-go-context.v1",
                 "lineage_blob":LINEAGE_BLOB,"historical_source_head":p["historical_source_head"],
                 "historical_source_tree":p["historical_source_tree"],
                 "current_source_head":fresh["source_head"],"current_source_tree":fresh["source_tree"],
                 "current_recall_digest":fresh["receipt_digest"],"scope_digest":p["scope_digest"],
                 "direct_digest":p["direct_digest"],"mcp_digest":p["mcp_digest"],
                 "route_digest":p["route_digest"],"subject":subject,"routes":routes["routes"],
                 "conditional_without_premise":"HOLD_NO_GO_REVIEW",
                 "negative_hints":fresh["lexical_negative_hint_ids"],
                 "unreviewed_lexical_hits_retained":True,"semantic_search_complete":False,
                 "proof_authority":False,"novelty_certified":False,
                 "execution_authority":False,"merge_authority":False}
        return {"status":"SELECTED_NO_GO_CONTEXT_MATCHED","context":context,
                "context_digest":digest(context),"current_recall":fresh,
                "candidate_generation_allowed":False,"proof_authority":False}
    except (ValueError,TypeError,KeyError,OSError,AttributeError,RuntimeError) as exc:
        return hold(type(exc).__name__+":"+str(exc))

def make_target_request(context:Mapping,target_id:str):
    """Construct an exact closed-target request from the certified inventory.
    This is not a classifier of an arbitrary natural-language research goal.
    """
    row=context["routes"][target_id]
    request={"schema":"kuuos.codeai.exact-closed-target-request.v1",
             "context_digest":digest(context),"source_head":context["current_source_head"],
             "source_tree":context["current_source_tree"],"subject":context["subject"],
             "target_id":target_id,"proposition":row["proposition"],
             "target_expr_digest":row["target_expr_digest"],
             "request_kind":"review_exact_closed_target"}
    return {**request,"request_digest":digest(request)}

def pre_provider_no_go_gate(*,root:Path,observation:Mapping,proof_scope:Mapping,
        bundle:Mapping,subject:str,target_request:Mapping,repository_files:Mapping):
    """The no-go boundary runs before any provider; no bypass for no match.

    Only the selected exact propositions have certified verdicts. Unreviewed
    goals remain HOLD, so this pilot is NOT a replacement for a general
    positive/residual research synthesis entry point.
    """
    result=recall_certified_no_go(root=root,observation=observation,proof_scope=proof_scope,
                                  bundle=bundle,subject=subject)
    if result["status"]!="SELECTED_NO_GO_CONTEXT_MATCHED":
        return result
    try:
        ctx=result["context"]
        key=target_request["target_id"]
        if key not in ctx["routes"]:
            return hold("unreviewed_target",context=ctx)
        expected=make_target_request(ctx,key)
        if target_request!=expected:
            return hold("exact_target_or_request_binding_mismatch",context=ctx)
        for path in selected.BLOBS:
            if repository_files.get(path)!=(root/path).read_text(encoding="utf-8"):
                return hold("complete_source_context_missing:"+path,context=ctx)
        row=ctx["routes"][key]
        return {"status":row["status"],"target_id":key,"proposition":row["proposition"],
                "target_expr_digest":row["target_expr_digest"],"source_witness":row["source_witness"],
                "axioms":row["axioms"],"context_digest":result["context_digest"],
                "request_digest":expected["request_digest"],"issues":[],
                "candidate_generation_allowed":False,"synthesis":None,
                "semantic_search_complete":False,"proof_authority":False,
                "novelty_certified":False,"execution_authority":False,"merge_authority":False}
    except (ValueError,TypeError,KeyError,OSError,AttributeError,RuntimeError) as exc:
        return hold(type(exc).__name__+":"+str(exc))

def build_selected_no_go_research_synthesis(*,root:Path,observation:Mapping,proof_scope:Mapping,
        bundle:Mapping,subject:str,target_request:Mapping,repository_files:Mapping,**kwargs):
    """Selected pre-provider entry. All selected targets already have proof or
    refutation; all unknowns HOLD. No call to v0.5 or provider is warranted.
    Do not claim global integration or completeness. A future reviewed
    residual route must additionally pass the original v0.5/v0.3/v0.2/v0.1 gates.
    """
    return pre_provider_no_go_gate(root=root,observation=observation,proof_scope=proof_scope,
        bundle=bundle,subject=subject,target_request=target_request,repository_files=repository_files)
