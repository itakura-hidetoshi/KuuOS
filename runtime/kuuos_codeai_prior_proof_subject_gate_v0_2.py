"""Research subject recall v0.2: cross-family prior-proof anchors, not a novelty oracle."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unicodedata
from collections.abc import Mapping
from typing import Any

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import (
    scan, assess, digest, git_blob, DUPLICATE, RELATIONS,
)
from runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1 import (
    build_research_structured_edit_synthesis,
)

INDEX = Path(__file__).resolve().parents[1] / "memoryos/research_prior_proof_subject_index_v0_2.json"


def _normalized(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKC", s).casefold() if c.isalnum())


def recall_subject(root: Path, source_head: str, query: str) -> dict[str, Any]:
    """Accept ordinary Japanese/English topic text without remembered theorem names.

    The index is a curated retrieval aid, not a complete semantic search.
    Source blob drift is an explicit re-observation obligation, not retirement
    of an older theorem. A new HEAD alone does not invalidate these hints.
    """
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in index["topics"]}
    q = _normalized(query)
    direct = sorted(t for t, entry in topics.items()
                    if any(_normalized(a) in q for a in entry["aliases"]))
    selected = sorted(set(direct) | {n for t in direct for n in topics[t]["neighbors"]})
    anchors = []
    issues = []
    for t in selected:
        for a in topics[t]["anchors"]:
            path = root / a["path"]
            try:
                if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                    raise OSError("missing or unsafe source")
                raw = path.read_bytes()
                blob = git_blob(raw)
                lines = raw.decode("utf-8").splitlines()
            except (OSError, UnicodeError):
                issues.append("anchor_source_unavailable:" + a["path"])
                continue
            if blob != a["blob"]:
                issues.append("anchor_blob_changed_reobserve:" + a["path"])
            for name in a["declarations"]:
                pattern = re.compile(r"^\s*(?:noncomputable\s+)?(?:theorem|def|abbrev|lemma|structure|inductive)\s+"
                                     + re.escape(name) + r"(?:\s|[:({]|$)")
                found = [i for i, line in enumerate(lines, 1) if pattern.match(line)]
                if len(found) != 1:
                    issues.append("anchor_declaration_not_unique:" + a["path"] + ":" + name)
                    continue
                n = found[0]
                anchors.append({"topic": t, "path": a["path"], "blob": blob,
                                "declaration": name, "line": n,
                                "declaration_line": lines[n-1], "scope_hint": a["scope"],
                                "anchor_blob_matches": blob == a["blob"]})
    # All anchors trigger the original broad lexical source scan, including
    # consumers, not only their own files. No keyword hit is a proof.
    terms = sorted({a["declaration"] for a in anchors})
    lexical = None
    if len(terms) >= 2:
        lexical = scan(root, source_head, terms)
    if not direct:
        issues.append("NO_DATA: unindexed_subject_requires_cross_family_research")
    if lexical is None:
        issues.append("NO_DATA: insufficient_anchored_declarations")
    receipt = {
        "schema": "kuuos.research.subject_recall.v0.2",
        "source_head_as_observed_by_caller": source_head,
        "query": query, "index_digest": digest(index),
        "direct_topics": direct, "expanded_topics": selected, "anchors": anchors,
        "lexical_receipt": lexical, "issues": issues,
        "status": "HOLD_REOBSERVATION" if issues else "REVIEW_REQUIRED",
        "proof_authority": False, "novelty_certified": False, "merge_authority": False,
        "coverage": "curated subject index plus literal source retrieval, not complete semantic search",
    }
    receipt["receipt_digest"] = digest(receipt)
    return receipt


def assess_subject(root: Path, source_head: str, receipt: dict[str, Any],
                   review: dict[str, Any]) -> dict[str, Any]:
    """Require declaration-level disposition in addition to v0.1 file review."""
    fresh = recall_subject(root, source_head, receipt["query"])
    issues = list(fresh["issues"])
    if fresh != receipt or review.get("subject_receipt_digest") != fresh["receipt_digest"]:
        issues.append("stale_or_unbound_subject_receipt")
    expected = {(a["path"], a["declaration"]): a for a in fresh["anchors"]}
    seen = set()
    duplicate = False
    comparisons = review.get("anchor_comparisons", [])
    if not isinstance(comparisons, list):
        comparisons = []
        issues.append("invalid_anchor_comparisons")
    for item in comparisons:
        if not isinstance(item, Mapping):
            issues.append("invalid_anchor_comparison")
            continue
        path, name = item.get("path"), item.get("declaration")
        if not isinstance(path, str) or not isinstance(name, str):
            issues.append("invalid_anchor_key")
            continue
        key = (path, name)
        if key not in expected or key in seen:
            issues.append("unknown_or_duplicate_anchor:" + repr(key))
            continue
        seen.add(key)
        a = expected[key]
        relation = item.get("relation")
        if (item.get("blob") != a["blob"] or item.get("line") != a["line"]
                or not isinstance(relation, str) or relation not in RELATIONS
                or any(not isinstance(item.get(k), str) or not item[k].strip()
                       for k in ("reason", "assumptions_comparison", "conclusion_comparison"))):
            issues.append("invalid_anchor_review:" + name)
            continue
        if relation == "unresolved":
            issues.append("unresolved_anchor:" + name)
        duplicate |= relation in DUPLICATE
    if seen != set(expected):
        issues.append("unreviewed_prior_declarations")
    legacy = None
    if fresh["lexical_receipt"] is not None:
        legacy = assess(root, source_head, fresh["lexical_receipt"], review)
        if legacy["issues"]:
            issues.extend(legacy["issues"])
    status = "HOLD_RESEARCH_RECALL"
    if not issues and legacy is not None:
        if duplicate and review.get("request") == "new":
            status = "HOLD_DUPLICATE_REUSE_REQUIRED"
        else:
            status = legacy["status"]
    return {"status": status, "issues": issues, "subject_receipt_digest": fresh["receipt_digest"],
            "legacy_review": legacy, "review_assertions_only": True,
            "candidate_generation_hint": status in ("BRIDGE_PROPOSAL_ONLY_NOT_NOVELTY",
                                                       "REVIEWED_DELTA_PROPOSAL_ONLY"),
            "proof_authority": False, "novelty_certified": False,
            "execution_authority": False, "merge_authority": False}


def build_subject_research_synthesis(*, root: Path, source_head: str,
                                     subject_receipt: dict[str, Any],
                                     mathematical_review: dict[str, Any],
                                     **kwargs: Any) -> dict[str, Any]:
    """Subject preflight, then v0.1's existing source/context/provider boundary."""
    try:
        review = assess_subject(root, source_head, subject_receipt, mathematical_review)
        if not review["candidate_generation_hint"]:
            return {"status": "HOLD_RESEARCH_RECALL", "subject_review": review, "synthesis": None}
        # The entire anchored source (including named obstructions) must reach
        # the real provider context, not merely a claimed declaration name.
        files = kwargs.get("repository_files")
        required = {a["path"] for a in subject_receipt["anchors"]}
        if not isinstance(files, Mapping) or not required.issubset(files):
            return {"status": "HOLD_RESEARCH_RECALL", "subject_review": review,
                    "issues": ["missing_anchored_source_context"], "synthesis": None}
        downstream = build_research_structured_edit_synthesis(
            root=root, source_head=source_head,
            recall_receipt=subject_receipt["lexical_receipt"],
            mathematical_review=mathematical_review, **kwargs)
        return {"status": downstream["status"], "subject_review": review,
                "downstream": downstream, "synthesis": downstream["synthesis"]}
    except (ValueError, TypeError, KeyError, OSError, AttributeError) as exc:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": [type(exc).__name__], "synthesis": None}
