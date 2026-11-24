"""Exact-tree-bound repository-wide lexical Lean declaration recall.

This is a read-only retrieval and review aid, not a Lean environment export.
It does not certify types, proof dependencies, novelty, or execution authority.
The caller must freshly observe the actual commit/tree association via GitHub.
"""
from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
from pathlib import Path
import os
import re
import stat
import unicodedata
from typing import Any

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import (
    ROOTS, SHA, DUPLICATE, RELATIONS, digest, git_blob,
)
from scripts.check_kuuos_lean_mcp_fullsource_v1 import (
    DECL, get_pins, imports_of,
)
from scripts.kuuos_sandbox_lean_cycle_v1 import Hold, without_comments_strings

REPOSITORY = "itakura-hidetoshi/KuuOS"
PIN_FILES = ("lean-toolchain", "lake-manifest.json", "lakefile.toml")
SCOPES = {"canonical_main", "pr_test_merge", "research_head", "fixture"}
SCHEMA = "kuuos.codeai.prior_proof_library_index.v0.3"


def tree_hash(entries: list[dict]) -> str:
    """Git tree object hash, including path names, modes and object IDs.

    Git sorts directory names as if followed by a slash. Root observation
    entries are independently bound to the supplied observed root tree hash.
    """
    seen = set()
    rows = []
    for item in entries:
        name, mode, sha = item["path"], item["mode"], item["sha"]
        mode = "40000" if mode == "040000" else mode
        if (not isinstance(name, str) or name in ("", ".", "..")
                or "/" in name or "\x00" in name or name in seen
                or mode not in {"40000", "100644", "100755", "120000", "160000"}
                or not isinstance(sha, str) or not SHA.fullmatch(sha)):
            raise ValueError("invalid Git tree entry: " + repr(name))
        seen.add(name)
        raw_name = os.fsencode(name)
        rows.append((raw_name + (b"/" if mode == "40000" else b""),
                     mode.encode() + b" " + raw_name + b"\0" + bytes.fromhex(sha)))
    body = b"".join(v for _, v in sorted(rows))
    return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()


def _outline(path: str, blob: str, raw: bytes) -> dict:
    """Reuse existing source-repair lexer and declaration extractor.

    Signatures are bounded source previews, not elaborated Lean types.
    Anonymous declarations, macros, some attributes and generated constants
    are outside this lexical index. A source parser gap is retained.
    """
    module = ".".join(Path(path).parts[1:]).removesuffix(".lean")
    item = {"path": path, "blob": blob, "module_path_lexical": module,
            "imports": [], "declarations": [], "axiom_queries_lexical": [],
            "parse_status": "LEXICAL_ONLY"}
    try:
        original = raw.decode("utf-8")
        masked = without_comments_strings(original)
    except (UnicodeError, Hold) as exc:
        item["parse_status"] = "NO_DATA"
        item["parse_issue"] = str(exc)
        return item
    lines = masked.split("\n")
    raw_lines = original.split("\n")
    if len(lines) != len(raw_lines):
        item["parse_status"] = "NO_DATA"
        item["parse_issue"] = "line mapping changed during comment/string masking"
        return item
    imps = set(imports_of(masked))
    for line in lines:
        m = re.match(r"^[ \t]*(?:(?:public|private)[ \t]+)?import[ \t]+(.+)$", line)
        if m:
            imps.update(m.group(1).split())
        a = re.match(r"^[ \t]*#print[ \t]+axioms[ \t]+(\S+)", line)
        if a:
            item["axiom_queries_lexical"].append(a.group(1))
    item["imports"] = sorted(imps)
    starts = [(i, m) for i, line in enumerate(lines) if (m := DECL.match(line))]
    for j, (start, m) in enumerate(starts):
        stop = starts[j+1][0] if j+1 < len(starts) else len(lines)
        kind, name = m.group(1), m.group(2)
        # Only a source preview, including original whitespace and exact line
        # location. A := in a binder may end the preview before the full type.
        parts = []
        boundary = False
        for k in range(start, min(stop, start+150)):
            line = lines[k]
            end = re.search(r":=|\bwhere[ \t]*$", line)
            if end:
                parts.append(raw_lines[k][:end.start()])
                boundary = True
                break
            parts.append(raw_lines[k])
        preview = "\n".join(parts)
        signature_digest = hashlib.sha256(preview.encode()).hexdigest()
        identity = {"path": path, "source_blob": blob, "line": start+1,
                    "name_lexical": name, "signature_digest": signature_digest}
        item["declarations"].append({
            **identity, "id": digest(identity), "kind": kind,
            "signature_preview": preview, "lexical_block_end_line": stop,
            "signature_boundary_seen": boundary,
        })
    return item


def _walk(directory: Path, rel: str, files: list, counts: dict) -> str:
    entries = []
    for child in directory.iterdir():
        name = child.name
        subpath = rel + "/" + name
        st = child.lstat()
        if stat.S_ISLNK(st.st_mode):
            # Match Git object bytes but do not read any linked target.
            sha = git_blob(os.fsencode(os.readlink(child)))
            mode = "120000"
            counts["blobs"] += 1
            if child.suffix == ".lean":
                files.append({"path": subpath, "blob": sha,
                              "module_path_lexical": ".".join(Path(subpath).parts[1:]).removesuffix(".lean"),
                              "imports": [], "declarations": [], "axiom_queries_lexical": [],
                              "parse_status": "NO_DATA", "parse_issue": "symlink not followed"})
        elif stat.S_ISDIR(st.st_mode):
            mode = "40000"
            sha = _walk(child, subpath, files, counts)
        elif stat.S_ISREG(st.st_mode):
            mode = "100755" if st.st_mode & stat.S_IXUSR else "100644"
            raw = child.read_bytes()
            sha = git_blob(raw)
            counts["blobs"] += 1
            if child.suffix == ".lean":
                files.append(_outline(subpath, sha, raw))
        else:
            raise ValueError("unsupported source tree object: " + subpath)
        entries.append({"path": name, "mode": mode, "sha": sha})
    return tree_hash(entries)


def build_catalog(root: Path, observation: Mapping) -> dict:
    """Rebuild from materialized source; reject missing, extra or changed files.

    The commit/tree association is an external observation, not self-certified
    by hashing the local directories. No Git/gh CLI or network is used here.
    """
    root = root.resolve()
    head, expected_tree = observation["source_head"], observation["source_tree"]
    if (observation["repository"] != REPOSITORY
            or observation["scope"] not in SCOPES
            or not isinstance(head, str) or not SHA.fullmatch(head)
            or not isinstance(expected_tree, str) or not SHA.fullmatch(expected_tree)
            or observation.get("truncated") is not False):
        raise ValueError("NO_DATA: invalid exact source observation")
    entries = observation["root_entries"]
    if not isinstance(entries, list) or tree_hash(entries) != expected_tree:
        raise ValueError("NO_DATA: root tree observation mismatch")
    expected = {x["path"]: x for x in entries}
    pins = get_pins(root)
    for name in PIN_FILES:
        p = root / name
        if (name not in expected or p.is_symlink() or not p.is_file()
                or expected[name]["mode"] not in {"100644", "100755"}
                or git_blob(p.read_bytes()) != expected[name]["sha"]):
            raise ValueError("NO_DATA: pinned source file mismatch: " + name)
    files = []
    counts = {"blobs": 0}
    source_trees = {}
    for name in ROOTS:
        path = root / name
        if (name not in expected or expected[name]["mode"] not in {"040000", "40000"}
                or path.is_symlink() or not path.is_dir()):
            raise ValueError("NO_DATA: missing source root: " + name)
        actual = _walk(path, name, files, counts)
        if actual != expected[name]["sha"]:
            raise ValueError("NO_DATA: materialized source tree differs: " + name)
        source_trees[name] = actual
    files.sort(key=lambda f: f["path"])
    if not files:
        raise ValueError("NO_DATA: empty Lean source catalog")
    catalog = {"schema": SCHEMA, "repository": REPOSITORY,
               "source_head_as_observed_by_caller": head, "source_tree": expected_tree,
               "observation_scope": observation["scope"],
               "source_subtrees": source_trees, "pins": pins,
               "source_blob_count": counts["blobs"],
               "lean_source_file_count": len(files),
               "named_declaration_preview_count": sum(len(f["declarations"]) for f in files),
               "parse_gap_count": sum(f["parse_status"] == "NO_DATA" for f in files),
               "files": files, "proof_authority": False, "novelty_certified": False,
               "coverage": "verified formal/ and lean/ Git subtrees; lexical named declaration previews only"}
    catalog["catalog_digest"] = digest(catalog)
    return catalog


def _norm(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKC", value).casefold() if c.isalnum())


def search_catalog(catalog: Mapping, query: str, *, terms: list[str] | None = None,
                   mode: str = "all", limit: int = 100) -> dict:
    """Deterministic lexical concept retrieval across every indexed source file.

    No ranking score, absence of hits, or bounded page establishes novelty.
    """
    if not isinstance(query, str) or not query.strip() or len(query) > 4000:
        raise ValueError("NO_DATA: research query required")
    if mode not in ("all", "any") or type(limit) is not int or not 1 <= limit <= 500:
        raise ValueError("invalid search policy")
    if terms is None:
        terms = re.findall(r"[^\W_]+", query, flags=re.UNICODE)
    if not isinstance(terms, list) or not all(isinstance(x, str) for x in terms):
        raise ValueError("invalid search terms")
    keys = sorted({_norm(x) for x in terms if len(_norm(x)) >= 2})
    if not keys or len(keys) > 20:
        raise ValueError("NO_DATA: require 1..20 meaningful lexical search terms")
    hits = []
    modules: dict[str, list[str]] = {}
    files = {f["path"]: f for f in catalog["files"]}
    for f in catalog["files"]:
        modules.setdefault(f["module_path_lexical"], []).append(f["path"])
        p = _norm(f["path"])
        for d in f["declarations"]:
            name = _norm(d["name_lexical"])
            signature = _norm(d["signature_preview"])
            matched = [k for k in keys if k in name or k in signature or k in p]
            if not matched or (mode == "all" and len(matched) != len(keys)):
                continue
            score = sum(5*(k in name) + 3*(k in signature) + (k in p) for k in matched)
            hits.append({**d, "matched_terms": matched, "lexical_score": score})
    hits.sort(key=lambda d: (-d["lexical_score"], d["path"], d["line"], d["id"]))
    selected = hits[:limit]
    paths = sorted({d["path"] for d in selected})
    dependencies = []
    for p in paths:
        f = files[p]
        dependencies.append({
            "path": p, "source_blob": f["blob"],
            "imports": [{"module": m, "local_source_candidates": sorted(modules.get(m, []))}
                        for m in f["imports"]],
            "axiom_queries_lexical": f["axiom_queries_lexical"],
        })
    gaps = [{"path": f["path"], "blob": f["blob"], "issue": f.get("parse_issue")}
            for f in catalog["files"] if f["parse_status"] == "NO_DATA"]
    status = ("HOLD_NO_DATA" if not hits else "HOLD_TRUNCATED" if len(hits) > limit
              else "REVIEW_REQUIRED")
    receipt = {"schema": "kuuos.codeai.library_recall.v0.3",
               "source_head_as_observed_by_caller": catalog["source_head_as_observed_by_caller"],
               "source_tree": catalog["source_tree"], "catalog_digest": catalog["catalog_digest"],
               "query": query, "terms": keys, "mode": mode, "limit": limit,
               "total_hits": len(hits), "omitted_hits": max(0, len(hits)-limit),
               "hits": selected, "source_import_candidates": dependencies,
               "parse_gaps": gaps, "status": status, "proof_authority": False,
               "novelty_certified": False, "semantic_search_complete": False,
               "proof_dependency_graph_verified": False}
    receipt["receipt_digest"] = digest(receipt)
    return receipt


def assess_library(root: Path, observation: Mapping, receipt: Mapping,
                   review: Mapping) -> dict:
    """Rebuild rather than trusting a caller's catalog/digest alone.

    Full retrieved-declaration and parse-gap disposition is needed for a
    research hint, not proof. The prior v0.1/v0.2 gates remain required.
    """
    fresh = search_catalog(build_catalog(root, observation), receipt["query"],
                           terms=receipt["terms"], mode=receipt["mode"], limit=receipt["limit"])
    issues = []
    if observation["scope"] != "canonical_main":
        issues.append("noncanonical_observation_scope")
    if fresh != receipt or review.get("library_receipt_digest") != fresh["receipt_digest"]:
        issues.append("stale_or_unbound_library_recall")
    if fresh["status"] != "REVIEW_REQUIRED":
        issues.append(fresh["status"])
    expected = {d["id"]: d for d in fresh["hits"]}
    seen = set()
    duplicate = False
    rows = review.get("library_comparisons")
    if not isinstance(rows, list):
        rows = []
        issues.append("missing_library_comparisons")
    for item in rows:
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            issues.append("invalid_library_comparison")
            continue
        identity = item["id"]
        d = expected.get(identity)
        if d is None or identity in seen:
            issues.append("unknown_or_duplicate_library_declaration")
            continue
        seen.add(identity)
        relation = item.get("relation")
        if (item.get("source_blob") != d["source_blob"]
                or item.get("signature_digest") != d["signature_digest"]
                or not isinstance(relation, str) or relation not in RELATIONS
                or any(not isinstance(item.get(k), str) or not item[k].strip()
                       for k in ("reason", "assumptions_comparison", "conclusion_comparison"))):
            issues.append("invalid_library_declaration_review:" + identity)
        elif relation == "unresolved":
            issues.append("unresolved_library_declaration:" + identity)
        else:
            duplicate |= relation in DUPLICATE
    if seen != set(expected):
        issues.append("unreviewed_library_declarations")
    gaps = {(g["path"], g["blob"]) for g in fresh["parse_gaps"]}
    gap_seen = set()
    gap_rows = review.get("parse_gap_reviews", [])
    if not isinstance(gap_rows, list):
        gap_rows = []
        issues.append("invalid_parse_gap_reviews")
    for item in gap_rows:
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str) or not isinstance(item.get("blob"), str):
            issues.append("invalid_parse_gap_review")
            continue
        key = item["path"], item["blob"]
        if (key not in gaps or key in gap_seen or item.get("disposition") not in ("reviewed_irrelevant", "reviewed_source")
                or not isinstance(item.get("reason"), str) or not item["reason"].strip()):
            issues.append("unresolved_parse_gap:" + item["path"])
        else:
            gap_seen.add(key)
    if gap_seen != gaps:
        issues.append("unreviewed_parse_gaps")
    request = review.get("request")
    status = "HOLD_RESEARCH_RECALL"
    if not issues:
        if duplicate and request == "new":
            status = "HOLD_DUPLICATE_REUSE_REQUIRED"
        elif duplicate and request == "reuse":
            status = "REUSE_EXISTING"
        elif request in ("bridge", "new"):
            status = "LIBRARY_REVIEW_HINT_ONLY"
        else:
            issues.append("unsupported_research_request")
    return {"status": status, "issues": issues,
            "library_receipt_digest": fresh["receipt_digest"],
            "candidate_generation_hint": status == "LIBRARY_REVIEW_HINT_ONLY",
            "review_assertions_only": True, "proof_authority": False,
            "novelty_certified": False, "execution_authority": False, "merge_authority": False}


def build_library_research_synthesis(*, root: Path, observation: Mapping,
                                     library_receipt: Mapping, mathematical_review: Mapping,
                                     recall_receipt: dict, subject_receipt: dict | None = None,
                                     **kwargs: Any) -> dict:
    """Whole-source review before the existing subject/lexical provider gate.

    Generic software repair and historical replay are not reclassified here.
    """
    from runtime.kuuos_codeai_prior_proof_subject_gate_v0_2 import (
        build_subject_research_synthesis,
    )
    from runtime.kuuos_codeai_research_structured_edit_synthesis_v0_1 import (
        build_research_structured_edit_synthesis,
    )
    try:
        result = assess_library(root, observation, library_receipt, mathematical_review)
        if not result["candidate_generation_hint"]:
            return {"status": "HOLD_RESEARCH_RECALL", "library_review": result, "synthesis": None}
        head = observation["source_head"]
        required = {d["path"] for d in library_receipt["hits"]
                    if any(c["id"] == d["id"] and c["relation"] != "irrelevant"
                           for c in mathematical_review["library_comparisons"])}
        required.update(g["path"] for g in mathematical_review.get("parse_gap_reviews", [])
                        if g["disposition"] == "reviewed_source")
        files = kwargs.get("repository_files")
        if not isinstance(files, Mapping) or not required.issubset(files):
            return {"status": "HOLD_RESEARCH_RECALL", "issues": ["missing_library_source_context"],
                    "library_review": result, "synthesis": None}
        # A recognized curated subject must still use the stricter existing
        # per-anchor gate; a broader new topic needs v0.1 exact source review.
        index = json.loads((root / "memoryos/research_prior_proof_subject_index_v0_2.json").read_text())
        query = library_receipt["query"]
        # Consider the target too, so renaming the retrieval query is not a
        # way to omit known anchor review.
        target = str(mathematical_review.get("target", ""))
        recognized = any(_norm(alias) in _norm(query + " " + target)
                         for topic in index["topics"] for alias in topic["aliases"])
        if recognized and subject_receipt is None:
            return {"status": "HOLD_RESEARCH_RECALL", "issues": ["missing_existing_subject_review"],
                    "library_review": result, "synthesis": None}
        if subject_receipt is not None:
            if subject_receipt.get("query") != query or (recognized and not subject_receipt.get("direct_topics")):
                return {"status": "HOLD_RESEARCH_RECALL", "issues": ["unbound_existing_subject_review"],
                        "library_review": result, "synthesis": None}
            downstream = build_subject_research_synthesis(
                root=root, source_head=head, subject_receipt=subject_receipt,
                mathematical_review=mathematical_review, **kwargs)
        else:
            downstream = build_research_structured_edit_synthesis(
                root=root, source_head=head, recall_receipt=recall_receipt,
                mathematical_review=mathematical_review, **kwargs)
        return {"status": downstream["status"], "library_review": result,
                "downstream": downstream, "synthesis": downstream["synthesis"]}
    except (ValueError, TypeError, KeyError, OSError, AttributeError, RuntimeError) as exc:
        return {"status": "HOLD_RESEARCH_RECALL", "issues": [type(exc).__name__, str(exc)],
                "synthesis": None}
