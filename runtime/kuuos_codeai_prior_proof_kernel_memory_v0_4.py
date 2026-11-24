"""Read-only, version-bound memory of independently observed existing Lean declarations.

The durable packet is a projection of the two exact v0.4 runner artifacts.
No authority, proof equivalence, novelty, or complete dependency claim.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from collections.abc import Mapping

from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog

PACKET_PATH = "memoryos/research_prior_proof_kernel_observation_v0_4.json"
PACKET_DIGEST = "bfcf9fde9a27fea2e1bad35c44cf46544ae92f42bf54bed7db3f267327b1d271"
ENVIRONMENT_BLOBS = {
    "lean-toolchain": None,
    "lake-manifest.json": "4b795033645fd37e42e67014abc3e0d5925a227c",
    "lakefile.toml": "947bac41f9535a7ba2ef03a93081cdfbc1b946f7",
}
FIELDS = ("name","path","blob","line","module","lexical_id","signature_preview_digest",
          "original_source_sha256","type_pretty","type_expr_sha256","universe_parameters",
          "type_constants","proof_constants","axioms","expected_direct_refs")
STANDARD = {"Classical.choice","propext","Quot.sound"}


def load_packet(root: Path) -> dict:
    p = root / PACKET_PATH
    if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError("NO_DATA: unavailable historical packet")
    packet = json.loads(p.read_text())
    if digest(packet) != PACKET_DIGEST:
        raise ValueError("NO_DATA: historical packet digest drift")
    return packet


def verify_runner_receipts(packet: Mapping, first: Mapping, fresh: Mapping,
                           mcp: Mapping, independent: Mapping) -> None:
    """Reproduce the exact committed projection from archived actual receipts."""
    if digest(packet) != PACKET_DIGEST:
        raise ValueError("historical packet digest mismatch")
    prov = packet["provenance"]
    expected = (prov["direct_receipt_digest"],prov["independent_direct_receipt_digest"],
                prov["mcp_receipt_digest"],prov["independent_receipt_digest"])
    if tuple(map(digest,(first,fresh,mcp,independent))) != expected:
        raise ValueError("NO_DATA: historical runner receipt digest mismatch")
    if first != fresh or first["status"] != "DIRECT_SOURCE_LOCAL_OBSERVATION_GREEN":
        raise ValueError("NO_DATA: original direct observations disagree")
    if mcp["status"] != "REAL_LEAN_MCP_RECALL_GREEN" or mcp["mcp_version"] != prov["mcp_version"]:
        raise ValueError("NO_DATA: actual Lean MCP not green")
    if independent["status"] != "INDEPENDENT_SELECTED_OBSERVATIONS_AGREE":
        raise ValueError("NO_DATA: independent observation not green")
    for record in (first,fresh,mcp,independent):
        for k in ("source_head","source_tree"):
            if record[k] != packet[k]:
                raise ValueError("historical source binding mismatch: "+k)
    if (mcp["direct_receipt_digest"] != expected[0]
        or independent["first_direct_digest"] != expected[0]
        or independent["fresh_direct_digest"] != expected[1]
        or independent["first_mcp_digest"] != expected[2]):
        raise ValueError("historical receipt cross-binding mismatch")
    for k in ("source_subtrees","pins","lakefile_blob","canonical_direct_options",
              "catalog_digest","plan_digest"):
        if first[k] != packet[k]:
            raise ValueError("historical environment binding mismatch: "+k)
    rows = [{k:r[k] for k in FIELDS} for r in first["observations"]]
    if rows != packet["observations"] or independent["selected_count"] != len(rows):
        raise ValueError("historical projection differs from actual observations")
    mrows = {r["name"]:r for r in mcp["observations"]}
    if len(mrows) != len(rows) or len(mcp["observations"]) != len(rows):
        raise ValueError("historical MCP inventory mismatch")
    for r in rows:
        if (hashlib.sha256(next(x["type_expr_repr"] for x in first["observations"]
                               if x["name"]==r["name"]).encode()).hexdigest()!=r["type_expr_sha256"]
            or set(r["axioms"])-STANDARD or
            not set(r["expected_direct_refs"]).issubset(r["proof_constants"])):
            raise ValueError("invalid historical type/proof observation")
        m=mrows[r["name"]]
        if (m["source_blob"]!=r["blob"] or m["type_expr_sha256_from_direct"]!=r["type_expr_sha256"]
                or m["axioms"]!=r["axioms"]):
            raise ValueError("historical MCP row differs")


def join_kernel_memory(root: Path, observation: Mapping, catalog: Mapping,
                       lexical: Mapping, packet: Mapping) -> dict:
    """Join existing exact v0.3 hits to selected historical kernel observations.

    Caller uses recall_kernel_memory to rebuild catalog against fresh GitHub
    observed tree. This pure join is not an authentication service.
    """
    if digest(packet)!=PACKET_DIGEST:
        raise ValueError("NO_DATA: historical packet digest drift")
    if (catalog["source_head_as_observed_by_caller"]!=observation["source_head"]
            or catalog["source_tree"]!=observation["source_tree"]
            or lexical["catalog_digest"]!=catalog["catalog_digest"]):
        raise ValueError("NO_DATA: stale catalog / recall")
    issues=[]
    if catalog["source_subtrees"]!=packet["source_subtrees"]:
        issues.append("formal_or_lean_dependency_scope_changed")
    if catalog["pins"]!=packet["pins"]:
        issues.append("toolchain_or_mathlib_pin_changed")
    entries={r["path"]:r["sha"] for r in observation["root_entries"]}
    for path,sha in ENVIRONMENT_BLOBS.items():
        if sha is not None and entries.get(path)!=sha:
            issues.append("environment_blob_changed:"+path)
    known={(r["path"],r["name"].rsplit(".",1)[-1]):r for r in packet["observations"]}
    enriched=[]
    stale=[]
    unknown=[]
    for hit in lexical["hits"]:
        row=known.get((hit["path"],hit["name_lexical"]))
        if row is None:
            unknown.append(hit["id"])
            continue
        raw=(root/hit["path"]).read_bytes()
        if (issues or row["lexical_id"]!=hit["id"] or row["blob"]!=hit["source_blob"]
                or row["line"]!=hit["line"] or row["signature_preview_digest"]!=hit["signature_digest"]
                or git_blob(raw)!=row["blob"]
                or hashlib.sha256(raw).hexdigest()!=row["original_source_sha256"]):
            stale.append({"lexical_id":hit["id"],"historical_name":row["name"],
                          "historical_source_head":packet["source_head"],
                          "status":"HOLD_REOBSERVE_KERNEL"})
            continue
        enriched.append({"lexical_id":hit["id"],"status":"HISTORICAL_KERNEL_OBSERVATION_SOURCE_SCOPE_MATCH",
                         "historical_source_head":packet["source_head"],
                         "historical_run_id":packet["provenance"]["run_id"],
                         "observation":dict(row)})
    result={"schema":"kuuos.codeai.kernel_memory_recall.v0.4",
            "source_head":observation["source_head"],"source_tree":observation["source_tree"],
            "observation_scope":observation["scope"],"catalog_digest":catalog["catalog_digest"],
            "lexical_receipt":dict(lexical),"historical_packet_digest":PACKET_DIGEST,
            "matched_observations":enriched,"stale_observations":stale,
            "without_kernel_observation":unknown,"scope_issues":issues,
            "status":("HOLD_REOBSERVE_KERNEL" if stale else
                      "HOLD_LEXICAL_RECALL" if lexical["status"]!="REVIEW_REQUIRED" else
                      "REVIEW_REQUIRED" if enriched else "NO_DATA_KERNEL_LEXICAL_REVIEW_ONLY"),
            "proof_authority":False,"novelty_certified":False,
            "full_transitive_proof_dependencies_verified":False}
    result["receipt_digest"]=digest(result)
    return result


def recall_kernel_memory(root: Path, observation: Mapping, query: str, *,
                         terms=None, mode="all", limit=100) -> dict:
    packet=load_packet(root)
    catalog=build_catalog(root,observation)
    lexical=search_catalog(catalog,query,terms=terms,mode=mode,limit=limit)
    return join_kernel_memory(root,observation,catalog,lexical,packet)
