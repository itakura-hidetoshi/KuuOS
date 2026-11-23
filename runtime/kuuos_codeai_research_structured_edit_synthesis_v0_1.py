"""Prior-proof gate as the research-specific entry to the original CodeAI kernel.

Not a new authority or replacement for ordinary CodeAI software repair.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import assess, digest
from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    build_codeai_autonomous_structured_edit_synthesis,
)


def build_research_structured_edit_synthesis(
    *, root: Path, source_head: str, recall_receipt: dict[str, Any],
    mathematical_review: dict[str, Any], source_observation_receipt: Any,
    repository_files: Any, synthesis_request: Any, provider_adapters: Any,
    synthesis_policy: Any, candidate_policy: Any,
) -> dict[str, Any]:
    """Only a reviewed bridge/delta can reach the original provider kernel.

    The exact reviewed target/delta and complete relevant source text must be
    in the bound synthesis context. The gate cannot certify semantic novelty.
    """
    issues = []
    try:
        review = assess(root, source_head, recall_receipt, mathematical_review)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": [type(exc).__name__],
                "recall_review": None, "synthesis": None}
    if not review["candidate_generation_hint"]:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": [review["status"]],
                "recall_review": review, "synthesis": None}
    if (not isinstance(source_observation_receipt, Mapping) or
        source_observation_receipt.get("source_commit_sha") != source_head or
        source_observation_receipt.get("source_branch") != "main" or
        source_observation_receipt.get("repository_full_name") != "itakura-hidetoshi/KuuOS"):
        issues.append("research_source_observation_mismatch")
    if (not isinstance(synthesis_request, Mapping) or
        mathematical_review.get("synthesis_request_binding") != digest(dict(synthesis_request))):
        issues.append("research_synthesis_request_unbound")
    else:
        intent = synthesis_request.get("intent_text")
        required = [mathematical_review["target"], mathematical_review["assumptions"],
                    mathematical_review["delta"]]
        if mathematical_review["request"] == "bridge":
            required.append(mathematical_review["consumer"])
        if not isinstance(intent, str) or not all(t in intent for t in required):
            issues.append("reviewed_target_or_delta_not_in_synthesis_intent")
    if not isinstance(repository_files, Mapping):
        issues.append("research_source_context_missing")
    else:
        required_paths = {c["path"] for c in mathematical_review["comparisons"]
                          if c["relation"] != "irrelevant"}
        if not required_paths.issubset(repository_files):
            issues.append("reviewed_prior_source_not_in_provider_context")
        for path, content in repository_files.items():
            if not isinstance(path, str) or not isinstance(content, str):
                issues.append("invalid_research_context")
                continue
            local = root / path
            try:
                if (Path(path).is_absolute() or ".." in Path(path).parts or
                    not local.resolve().is_relative_to(root.resolve()) or
                    local.is_symlink() or local.read_bytes() != content.encode("utf-8")):
                    issues.append("provider_context_source_mismatch:" + path)
            except OSError:
                issues.append("provider_context_source_unavailable:" + path)
    if issues:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": issues,
                "recall_review": review, "synthesis": None}
    synthesis = build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=source_observation_receipt,
        repository_files=repository_files, synthesis_request=synthesis_request,
        provider_adapters=provider_adapters, synthesis_policy=synthesis_policy,
        candidate_policy=candidate_policy,
    )
    return {"status": "FORWARDED_TO_ORIGINAL_CODEAI", "issues": [],
            "recall_review": review, "synthesis": synthesis}
