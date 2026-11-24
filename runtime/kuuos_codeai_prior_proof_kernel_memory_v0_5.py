"""Additive v0.5 combined, version-bound historical kernel recall.

Both source packets remain immutable and independently bound to their own
observations. An actual source catalog is rebuilt before research admission.
No semantic novelty, proof, full dependency, execution or merge authority.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from collections.abc import Mapping

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import (
    load_packet, PACKET_DIGEST as V04_DIGEST, ENVIRONMENT_BLOBS, STANDARD)

V05_PATH = "memoryos/research_prior_proof_kernel_observation_v0_5.json"
V05_DIGEST = "23336f58b6613514063df5f1aad4e433fd9f98a461b2fae4152fd296054620ac"
PACKET_DIGESTS = {"v0.4": V04_DIGEST, "v0.5": V05_DIGEST}
COMBINED_DIGEST = digest(PACKET_DIGESTS)


def verify_packets(parent: Mapping, frontier: Mapping) -> None:
    if digest(parent) != V04_DIGEST or digest(frontier) != V05_DIGEST:
        raise ValueError("NO_DATA: historical packet digest drift")
    if frontier["parent_packet_digest"] != V04_DIGEST:
        raise ValueError("NO_DATA: parent packet binding mismatch")
    for k in ("source_subtrees", "pins", "lakefile_blob", "canonical_direct_options"):
        if parent[k] != frontier[k]:
            raise ValueError("NO_DATA: incompatible historical source scope " + k)
    rows = parent["observations"] + frontier["observations"]
    if (len(parent["observations"]) != 3 or len(frontier["observations"]) != 10
            or len({r["name"] for r in rows}) != 13
            or len({r["lexical_id"] for r in rows}) != 13
            or len({(r["path"], r["name"].rsplit(".", 1)[-1]) for r in rows}) != 13):
        raise ValueError("NO_DATA: combined identity collision or inventory drift")
    refs = {n for r in parent["observations"] for n in r["expected_direct_refs"]}
    observed = {r["name"] for r in frontier["observations"]
                if r["frontier_role"] == "recorded_direct_reference"}
    if refs != observed or len(refs) != 4:
        raise ValueError("NO_DATA: prior recorded frontier incomplete")
    for p in (parent, frontier):
        if p["proof_authority"] is not False or p["novelty_certified"] is not False:
            raise ValueError("HOLD: unexpected packet authority")
        for r in p["observations"]:
            if set(r["axioms"]) - STANDARD or not set(r["expected_direct_refs"]).issubset(r["proof_constants"]):
                raise ValueError("HOLD: invalid recorded proof references")


def load_packets(root: Path):
    parent = load_packet(root)
    p = root / V05_PATH
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError("NO_DATA: missing frontier packet")
    frontier = json.loads(p.read_text(encoding="utf-8"))
    verify_packets(parent, frontier)
    return parent, frontier


def join_kernel_memory(root: Path, observation: Mapping, catalog: Mapping,
                       lexical: Mapping, parent: Mapping, frontier: Mapping) -> dict:
    verify_packets(parent, frontier)
    if (catalog["source_head_as_observed_by_caller"] != observation["source_head"]
            or catalog["source_tree"] != observation["source_tree"]
            or lexical["catalog_digest"] != catalog["catalog_digest"]
            or lexical["source_head_as_observed_by_caller"] != observation["source_head"]
            or lexical["source_tree"] != observation["source_tree"]
            or digest({k: v for k, v in lexical.items() if k != "receipt_digest"}) != lexical["receipt_digest"]):
        raise ValueError("NO_DATA: stale or unbound catalog / lexical receipt")
    issues = []
    if catalog["source_subtrees"] != parent["source_subtrees"]:
        issues.append("formal_or_lean_dependency_scope_changed")
    if catalog["pins"] != parent["pins"]:
        issues.append("toolchain_or_mathlib_pin_changed")
    entries = {r["path"]: r["sha"] for r in observation["root_entries"]}
    for path, expected in ENVIRONMENT_BLOBS.items():
        if expected is not None and entries.get(path) != expected:
            issues.append("environment_blob_changed:" + path)
    known = {}
    for version, packet in (("v0.4", parent), ("v0.5", frontier)):
        for row in packet["observations"]:
            known[(row["path"], row["name"].rsplit(".", 1)[-1])] = (version, packet, row)
    enriched, stale, unknown = [], [], []
    seen = set()
    for hit in lexical["hits"]:
        i = hit["id"]
        if i in seen:
            raise ValueError("NO_DATA: duplicate lexical hit")
        seen.add(i)
        item = known.get((hit["path"], hit["name_lexical"]))
        if item is None:
            unknown.append(i)
            continue
        version, packet, row = item
        local = root / hit["path"]
        safe = local.is_file() and not local.is_symlink() and local.resolve().is_relative_to(root.resolve())
        raw = local.read_bytes() if safe else b""
        provenance = {"historical_packet_version": version,
                      "historical_packet_digest": PACKET_DIGESTS[version],
                      "historical_source_head": packet["source_head"],
                      "historical_source_tree": packet["source_tree"],
                      "historical_run_id": packet["provenance"]["run_id"]}
        if (issues or not safe or hit["kind"] != "theorem" or row["lexical_id"] != i
                or row["blob"] != hit["source_blob"] or row["line"] != hit["line"]
                or row["signature_preview_digest"] != hit["signature_digest"]
                or git_blob(raw) != row["blob"]
                or hashlib.sha256(raw).hexdigest() != row["original_source_sha256"]):
            stale.append({"lexical_id": i, "historical_name": row["name"],
                          **provenance, "status": "HOLD_REOBSERVE_KERNEL"})
            continue
        enriched.append({"lexical_id": i, **provenance,
                         "status": "HISTORICAL_KERNEL_OBSERVATION_SOURCE_SCOPE_MATCH",
                         "observation": dict(row)})
    result = {
        "schema": "kuuos.codeai.kernel_memory_recall.v0.5",
        "source_head": observation["source_head"], "source_tree": observation["source_tree"],
        "observation_scope": observation["scope"], "catalog_digest": catalog["catalog_digest"],
        "lexical_receipt": dict(lexical), "historical_packet_digest": COMBINED_DIGEST,
        "historical_packet_digests": dict(PACKET_DIGESTS),
        "matched_observations": enriched, "stale_observations": stale,
        "without_kernel_observation": unknown, "scope_issues": issues,
        "status": ("HOLD_REOBSERVE_KERNEL" if issues or stale else
                   "HOLD_LEXICAL_RECALL" if lexical["status"] != "REVIEW_REQUIRED" else
                   "REVIEW_REQUIRED" if enriched else "NO_DATA_KERNEL_LEXICAL_REVIEW_ONLY"),
        "proof_authority": False, "novelty_certified": False,
        "full_transitive_proof_dependencies_verified": False,
    }
    result["receipt_digest"] = digest(result)
    return result


def recall_kernel_memory(root: Path, observation: Mapping, query: str, *,
                         terms=None, mode="all", limit=100) -> dict:
    parent, frontier = load_packets(root)
    catalog = build_catalog(root, observation)
    lexical = search_catalog(catalog, query, terms=terms, mode=mode, limit=limit)
    return join_kernel_memory(root, observation, catalog, lexical, parent, frontier)
