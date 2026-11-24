"""Prior-proof recall and research-delta admission, not a Lean proof or novelty oracle.

The caller must obtain the canonical GitHub SHA via MCP and materialize that exact
source. This module checks the actual source inventory, not Git refs or CI status.
No model memory, file name, search miss, digest or review is proof authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

TOOLCHAIN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
ROOTS = ("formal", "lean")
DUPLICATE = {"equivalent", "specialization", "direct_derivation"}
RELATIONS = DUPLICATE | {"prerequisite", "obstruction", "distinct", "irrelevant", "unresolved"}
SHA = re.compile(r"[0-9a-f]{40}")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def scan(root: Path, source_head: str, terms: list[str]) -> dict[str, Any]:
    if not SHA.fullmatch(source_head):
        raise ValueError("NO_DATA: missing exact observed GitHub source head")
    if (root / "lean-toolchain").read_text().strip() != TOOLCHAIN:
        raise ValueError("toolchain drift")
    manifest = json.loads((root / "lake-manifest.json").read_text())
    if [p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"] != [MATHLIB]:
        raise ValueError("mathlib drift")
    terms = sorted(set(t.strip().casefold() for t in terms if t.strip()))
    if len(terms) < 2:
        raise ValueError("require at least two distinct recall terms: symbols and concepts")
    inventory = []
    hits = []
    term_counts = {t: 0 for t in terms}
    for dirname in ROOTS:
        directory = root / dirname
        if not directory.is_dir() or directory.is_symlink():
            raise ValueError("NO_DATA: missing or unsafe source root: " + dirname)
        for file in sorted(directory.rglob("*.lean")):
            if file.is_symlink() or not file.is_file():
                raise ValueError("NO_DATA: unsafe source file: " + str(file))
            path = file.relative_to(root).as_posix()
            data = file.read_bytes()
            blob = git_blob(data)
            inventory.append([path, blob])
            matches = []
            for n, line in enumerate(data.decode("utf-8").splitlines(), 1):
                folded = line.casefold()
                found = [t for t in terms if t in folded]
                if found:
                    matches.append({"line": n, "text": line, "terms": found})
                    for t in found:
                        term_counts[t] += 1
            if matches:
                hits.append({"path": path, "blob": blob, "matches": matches})
    if not inventory:
        raise ValueError("NO_DATA: empty source corpus")
    receipt = {
        "schema": "kuuos.codeai.prior_proof_recall.v0.1",
        "source_head_as_observed_by_caller": source_head,
        "source_roots": list(ROOTS),
        "source_file_count": len(inventory),
        "inventory_digest": digest(inventory),
        "lean": TOOLCHAIN,
        "mathlib": MATHLIB,
        "terms": terms,
        "term_counts": term_counts,
        "hits": hits,
        "scope": "literal Lean source retrieval; not a complete semantic theorem search",
        "status": "REVIEW_REQUIRED" if hits else "HOLD_NO_DATA",
        "proof_authority": False,
        "novelty_certified": False,
        "merge_authority": False,
    }
    receipt["receipt_digest"] = digest(receipt)
    return receipt


def assess(root: Path, source_head: str, receipt: dict[str, Any],
           review: dict[str, Any]) -> dict[str, Any]:
    """Fail closed on stale evidence; never autonomously certify mathematical novelty.

    Each hit file must be dispositioned by the reviewing agent on the exact
    source. A review supplies a human/agent assertion, not a proof certificate.
    The proposed target is one proposition (not a bundle of different claims).
    """
    issues = []
    status = "HOLD_UNREVIEWED"
    fresh = scan(root, source_head, receipt["terms"])
    if fresh != receipt or review.get("receipt_digest") != fresh["receipt_digest"]:
        issues.append("stale_or_unbound_recall_receipt")
    if not fresh["hits"]:
        issues.append("search_miss_is_not_novelty")
    if not isinstance(review.get("target"), str) or not review["target"].strip():
        issues.append("missing_target_statement")
    if not isinstance(review.get("assumptions"), str) or not review["assumptions"].strip():
        issues.append("missing_target_assumptions")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        issues.append("missing_review_provenance")
    observed = {h["path"]: h for h in fresh["hits"]}
    entries = review.get("comparisons", [])
    if not isinstance(entries, list):
        entries = []
        issues.append("invalid_comparisons")
    seen = set()
    duplicate = False
    unresolved = False
    for entry in entries:
        if not isinstance(entry, dict):
            issues.append("invalid_comparison")
            continue
        path = entry.get("path")
        if not isinstance(path, str) or path not in observed or path in seen:
            issues.append("unknown_or_duplicate_comparison_path")
            continue
        seen.add(path)
        h = observed[path]
        relation = entry.get("relation")
        if (entry.get("blob") != h["blob"] or
            entry.get("line") not in {m["line"] for m in h["matches"]} or
            not isinstance(entry.get("declaration"), str) or not entry["declaration"].strip() or
            not isinstance(entry.get("reason"), str) or not entry["reason"].strip() or
            not isinstance(relation, str) or relation not in RELATIONS):
            issues.append("invalid_source_comparison:" + path)
            continue
        duplicate |= relation in DUPLICATE
        unresolved |= relation == "unresolved"
    if seen != set(observed):
        issues.append("unreviewed_source_hits")
    if unresolved:
        issues.append("unresolved_mathematical_comparison")
    requested = review.get("request")
    if requested not in ("reuse", "bridge", "new"):
        issues.append("invalid_research_request")
    if not issues:
        if duplicate and requested == "new":
            status = "HOLD_DUPLICATE_REUSE_REQUIRED"
        elif requested == "reuse" and duplicate:
            status = "REUSE_EXISTING"
        elif requested == "bridge":
            if isinstance(review.get("consumer"), str) and review["consumer"].strip() and isinstance(review.get("delta"), str) and review["delta"].strip():
                status = "BRIDGE_PROPOSAL_ONLY_NOT_NOVELTY"
            else:
                issues.append("missing_typed_bridge_consumer_or_delta")
        elif requested == "new" and not duplicate:
            if isinstance(review.get("delta"), str) and review["delta"].strip():
                status = "REVIEWED_DELTA_PROPOSAL_ONLY"
            else:
                issues.append("missing_unproved_delta")
        else:
            issues.append("no_supported_reuse_relation")
    if issues:
        status = "HOLD_UNREVIEWED"
    result = {
        "schema": "kuuos.codeai.prior_proof_review.v0.1",
        "source_head_as_observed_by_caller": source_head,
        "recall_digest": fresh["receipt_digest"],
        "review_digest": digest(review),
        "status": status,
        "issues": issues,
        "review_assertions_only": True,
        "candidate_generation_hint": status in ("BRIDGE_PROPOSAL_ONLY_NOT_NOVELTY",
                                                 "REVIEWED_DELTA_PROPOSAL_ONLY"),
        "proof_authority": False,
        "novelty_certified": False,
        "execution_authority": False,
        "merge_authority": False,
    }
    return result
