"""Version-bound historical kernel observations before research proposal synthesis.

This is an additive gate over v0.3/v0.2/v0.1, never a semantic novelty
oracle or mathematical authority. The original provider kernel receives
the exact historical observation context only after review.
"""
from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
from typing import Any

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_6 import recall_kernel_memory
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_library_research_synthesis
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, DUPLICATE


def kernel_context_text(receipt: Mapping) -> str:
    """Serialize the exact read-only observations into the existing provider intent."""
    context = {
        "schema": "kuuos.codeai.kernel_memory_provider_context.v0.6",
        "kernel_receipt_digest": receipt["receipt_digest"],
        "current_source_head": receipt["source_head"],
        "current_source_tree": receipt["source_tree"],
        "historical_packet_digest": receipt["historical_packet_digest"],
        "historical_packet_digests": receipt["historical_packet_digests"],
        "unobserved_recorded_reference_names": receipt["unobserved_recorded_reference_names"],
        "status": receipt["status"],
        "matched_observations": receipt["matched_observations"],
        "without_kernel_observation": receipt["without_kernel_observation"],
        "stale_observations": receipt["stale_observations"],
        "scope_issues": receipt["scope_issues"],
        "proof_authority": False,
        "novelty_certified": False,
        "full_transitive_proof_dependencies_verified": False,
    }
    return ("KuuOS historical kernel observations (read-only evidence; "
            "not a novelty or authority certificate):\n"
            + json.dumps(context, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


def assess_kernel_research(root: Path, observation: Mapping, receipt: Mapping,
                           review: Mapping, *, synthesis_request: Any,
                           repository_files: Any) -> dict:
    """Rebuild the actual current-source recall before considering generation."""
    lexical = receipt["lexical_receipt"]
    fresh = recall_kernel_memory(root, observation, lexical["query"],
                                 terms=lexical["terms"], mode=lexical["mode"],
                                 limit=lexical["limit"])
    issues = []
    if observation["scope"] != "canonical_main":
        issues.append("noncanonical_kernel_research_scope")
    if fresh != receipt or review.get("kernel_receipt_digest") != fresh["receipt_digest"]:
        issues.append("stale_or_unbound_kernel_memory")
    if fresh["status"] not in ("REVIEW_REQUIRED", "NO_DATA_KERNEL_LEXICAL_REVIEW_ONLY"):
        issues.append(fresh["status"])
    if fresh["lexical_receipt"]["status"] != "REVIEW_REQUIRED":
        issues.append("incomplete_lexical_recall")
    if fresh["stale_observations"]:
        issues.append("historical_kernel_observation_requires_reobservation")
    if review.get("library_receipt_digest") != fresh["lexical_receipt"]["receipt_digest"]:
        issues.append("unbound_underlying_library_review")
    comparisons = review.get("library_comparisons")
    if not isinstance(comparisons, list):
        comparisons = []
        issues.append("missing_underlying_library_comparisons")
    library_rows = {}
    for c in comparisons:
        if not isinstance(c, Mapping) or not isinstance(c.get("id"), str) or c["id"] in library_rows:
            issues.append("invalid_underlying_library_comparison")
            continue
        library_rows[c["id"]] = c
    expected = {r["lexical_id"]: r for r in fresh["matched_observations"]}
    rows = review.get("kernel_comparisons")
    if not isinstance(rows, list):
        rows = []
        issues.append("missing_kernel_comparisons")
    seen = set()
    duplicate = False
    for c in rows:
        if not isinstance(c, Mapping) or not isinstance(c.get("id"), str):
            issues.append("invalid_kernel_comparison")
            continue
        i = c["id"]
        r = expected.get(i)
        if r is None or i in seen:
            issues.append("unknown_or_duplicate_kernel_comparison")
            continue
        seen.add(i)
        prior = library_rows.get(i, {})
        relation = c.get("relation")
        if (c.get("observation_digest") != digest(r) or
                c.get("type_expr_sha256") != r["observation"]["type_expr_sha256"] or
                relation != prior.get("relation") or not isinstance(relation, str) or
                relation == "unresolved" or
                any(not isinstance(c.get(k), str) or not c[k].strip()
                    for k in ("type_assumptions_comparison", "type_conclusion_comparison",
                              "proof_reference_review"))):
            issues.append("unresolved_or_unbound_kernel_comparison:" + i)
            continue
        duplicate |= relation in DUPLICATE
    if seen != set(expected):
        issues.append("unreviewed_kernel_observations")
    if review.get("unobserved_kernel_hit_ids") != fresh["without_kernel_observation"]:
        issues.append("unobserved_kernel_scope_not_acknowledged")
    if not isinstance(synthesis_request, Mapping) or \
            review.get("synthesis_request_binding") != digest(dict(synthesis_request)):
        issues.append("unbound_kernel_synthesis_request")
    else:
        intent = synthesis_request.get("intent_text")
        if not isinstance(intent, str) or kernel_context_text(fresh) not in intent:
            issues.append("historical_kernel_context_missing_from_provider_intent")
    if not isinstance(repository_files, Mapping):
        issues.append("kernel_source_context_missing")
    else:
        for r in expected.values():
            path = r["observation"]["path"]
            local = root / path
            content = repository_files.get(path)
            if (not isinstance(content, str) or local.is_symlink() or
                    not local.resolve().is_relative_to(root.resolve()) or
                    local.read_bytes() != content.encode("utf-8")):
                issues.append("kernel_source_context_mismatch:" + path)
    status = "HOLD_RESEARCH_RECALL"
    if not issues:
        if duplicate and review.get("request") == "new":
            status = "HOLD_DUPLICATE_REUSE_REQUIRED"
        elif duplicate and review.get("request") == "reuse":
            status = "REUSE_EXISTING"
        elif review.get("request") in ("bridge", "new"):
            status = "KERNEL_MEMORY_REVIEW_HINT_ONLY"
        else:
            issues.append("unsupported_research_request")
    return {
        "schema": "kuuos.codeai.kernel_memory_review.v0.6",
        "status": status, "issues": issues,
        "kernel_receipt_digest": fresh["receipt_digest"],
        "matched_observation_count": len(expected),
        "unobserved_hit_count": len(fresh["without_kernel_observation"]),
        "candidate_generation_hint": status == "KERNEL_MEMORY_REVIEW_HINT_ONLY",
        "review_assertions_only": True, "proof_authority": False,
        "novelty_certified": False, "execution_authority": False, "merge_authority": False,
    }


def build_kernel_memory_research_synthesis(*, root: Path, observation: Mapping,
                                           kernel_receipt: Mapping,
                                           mathematical_review: Mapping,
                                           recall_receipt: dict,
                                           subject_receipt: dict | None = None,
                                           **kwargs: Any) -> dict:
    """Only a reviewed residual target proceeds to all the existing gates."""
    try:
        check = assess_kernel_research(root, observation, kernel_receipt, mathematical_review,
                                       synthesis_request=kwargs.get("synthesis_request"),
                                       repository_files=kwargs.get("repository_files"))
        if not check["candidate_generation_hint"]:
            return {"status": "HOLD_RESEARCH_RECALL", "kernel_review": check, "synthesis": None}
        downstream = build_library_research_synthesis(
            root=root, observation=observation,
            library_receipt=kernel_receipt["lexical_receipt"],
            mathematical_review=mathematical_review,
            recall_receipt=recall_receipt, subject_receipt=subject_receipt, **kwargs)
        return {"status": downstream["status"], "kernel_review": check,
                "downstream": downstream, "synthesis": downstream["synthesis"]}
    except (ValueError, TypeError, KeyError, OSError, AttributeError, RuntimeError) as exc:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": [type(exc).__name__, str(exc)],
                "synthesis": None}
