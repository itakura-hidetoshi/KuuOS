"""R11: historical proof scope transport, not a new proof or authority.

The host must provide its trusted repository metadata reader. Digest equality
alone never authenticates a caller's observation. R10 remains immutable;
the historical source/request is kept distinct from the current source.
"""
from __future__ import annotations
from runtime import kuuos_codeai_olean_research_synthesis_v1 as old
from scripts import ci_verified_lean_project_cache_v1 as cache

def observe_scope(get):
    """Read the actual canonical ref, ancestry and all existing cache inputs."""
    try:
        ref=get("git/ref/heads/main")
        if ref["ref"]!="refs/heads/main" or ref["object"]["type"]!="commit":
            return old.hold("invalid_canonical_ref")
        current=ref["object"]["sha"]
        historic=get("git/commits/"+old.HEAD)
        now=get("git/commits/"+current)
        if historic["sha"]!=old.HEAD or historic["tree"]["sha"]!=old.TREE or now["sha"]!=current:
            return old.hold("commit_identity_mismatch")
        before=cache.remote_scope(get,old.HEAD)
        after=cache.remote_scope(get,current)
        if cache.digest(before)!=old.SCOPE or after!=before:
            return old.hold("proof_scope_changed")
        if not cache.ancestor(get,old.HEAD,current):
            return old.hold("historical_source_not_ancestor")
        if get("git/ref/heads/main")!=ref:
            return old.hold("canonical_ref_moved_during_observation")
        return {"status":"SAME_PROOF_SCOPE_OBSERVED",
                "repository":cache.REPO,"canonical_branch":"main",
                "historical_source_head":old.HEAD,"historical_source_tree":old.TREE,
                "current_source_head":current,"current_source_tree":now["tree"]["sha"],
                "proof_scope":after,"scope_digest":old.SCOPE,
                "ancestor_observed":True,"proof_authority":False,
                "execution_authority":False,"semantic_search_complete":False}
    except (KeyError,TypeError,ValueError,AttributeError,OSError):
        return old.hold("scope_observation_unavailable")

def make_request(transport,target,historical_request=None,terms=None,selections=None):
    req={"schema":"kuuos.codeai.scope-bound-research-request.v1",
         "transport_digest":old.digest(transport),
         "current_source_head":transport["current_source_head"],
         "current_source_tree":transport["current_source_tree"],
         "scope_digest":transport["scope_digest"],
         "target":target,"historical_request":historical_request,
         "terms":terms if terms is not None else [],
         "selections":selections if selections is not None else []}
    return {**req,"request_digest":old.digest(req)}

def build_scope_bound_research_synthesis(*,transport,expected_transport_digest,request,
        db,index_receipt,direct,independent,mcp,routes,replay,provider_adapters=()):
    """Use only a separately admitted host observation. No provider lease."""
    try:
        if (transport["status"]!="SAME_PROOF_SCOPE_OBSERVED"
                or old.digest(transport)!=expected_transport_digest
                or transport["repository"]!=cache.REPO or transport["canonical_branch"]!="main"
                or transport["historical_source_head"]!=old.HEAD
                or transport["historical_source_tree"]!=old.TREE
                or transport["scope_digest"]!=old.SCOPE
                or cache.digest(transport["proof_scope"])!=old.SCOPE
                or transport["ancestor_observed"] is not True
                or transport["proof_authority"] is not False
                or transport["execution_authority"] is not False):
            return old.hold("unadmitted_scope_transport")
        if request!=make_request(transport,request["target"],request["historical_request"],
                                 request["terms"],request["selections"]):
            return old.hold("current_target_request_binding_mismatch")
        # R10 reads the historical proof package under its ORIGINAL source.
        # This is not an assertion that the historical ref is still current.
        historical={"repository":cache.REPO,"scope":"canonical_main",
                    "source_head":old.HEAD,"source_tree":old.TREE}
        result=old.build_olean_bound_research_synthesis(
            db=db,index_receipt=index_receipt,direct=direct,independent=independent,
            mcp=mcp,routes=routes,replay=replay,observation=historical,
            target=request["target"],target_request=request["historical_request"],
            terms=request["terms"],selections=request["selections"],provider_adapters=provider_adapters)
        return {"status":result["status"],"historical_result":result,
                "transport_digest":expected_transport_digest,"request_digest":request["request_digest"],
                "historical_source_head":old.HEAD,"historical_source_tree":old.TREE,
                "current_source_head":transport["current_source_head"],
                "current_source_tree":transport["current_source_tree"],"scope_digest":old.SCOPE,
                "candidate_generation_allowed":False,"provider_calls":0,"synthesis":None,
                "proof_authority":False,"execution_authority":False,"merge_authority":False,
                "semantic_search_complete":False,"novelty_certified":False}
    except (KeyError,TypeError,ValueError,AttributeError,OSError):
        return old.hold("invalid_scope_bound_request")
