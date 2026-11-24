#!/usr/bin/env python3
"""Project only exact archived v0.5 receipts into a read-only candidate packet.

The v0.4 historical packet is immutable. This candidate does not authorize
learning, proof adoption, execution, novelty, or any Git mutation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import (
    load_packet, PACKET_DIGEST, FIELDS, STANDARD)
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.codeai_prior_proof_kernel_frontier_v0_5 import PLANS, validate_frontier

HEAD = "1d40637574fb2cd2ba81a9a746172b937239e521"
TREE = "29277c9422d46c215796c05b1ab0efd163824610"
RUN = 45502007330
ATTEMPT = 1
JOBS = {
    138827428008: [
        "Direct source-local Lean types, proof constants and axiom observations",
        "Actual Lean MCP hover, diagnostics and verify only after direct green"],
    138830376315: ["Independently re-elaborate and compare source-local observations"]}
ARTIFACTS = {
    "local": (14971820820, "798990f8b88bfaacaad36a38b0515e0c43362452828976d3dd42e31c3c50b415"),
    "independent": (14971601477, "0c580fafe1d7981980a82367163eba97bb5c8454b2a343207dcfbc9eee84ee0a")}
DIRECT_DIGEST = "aa932ca177604c6e63b19504192c62f7ceb53dceea0b85bba361aa3d23bd8610"
MCP_DIGEST = "9f3fbbd46f4b04a1b0fe901a438e998263115105685a92421e54d9a48b2c5143"
EXTRA_FIELDS = ("prior_packet_digest", "frontier_role")


def require(condition, issue):
    if not condition:
        raise ValueError("HOLD: " + issue)


def observe_archives():
    def get(path):
        req = urllib.request.Request(
            "https://api.github.com/repos/itakura-hidetoshi/KuuOS/" + path,
            headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                     "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.load(resp)
    r = get("actions/runs/" + str(RUN))
    require((r["status"], r["conclusion"], r["head_sha"], r["run_attempt"])
            == ("completed", "success", HEAD, ATTEMPT), "original workflow not exact-green")
    jobs = get("actions/runs/" + str(RUN) + "/jobs?per_page=100")
    require(jobs["total_count"] == 2, "job inventory mismatch")
    actual = {j["id"]: j for j in jobs["jobs"]}
    require(set(actual) == set(JOBS), "job identities differ")
    for jid, names in JOBS.items():
        j = actual[jid]
        require((j["status"], j["conclusion"], j["head_sha"])
                == ("completed", "success", HEAD), "job not exact-green")
        steps = {s["name"]: s for s in j["steps"]}
        for name in names:
            require((steps[name]["status"], steps[name]["conclusion"])
                    == ("completed", "success"), "required step not green")
    for kind, (aid, sha) in ARTIFACTS.items():
        a = get("actions/artifacts/" + str(aid))
        require(not a["expired"] and a["digest"] == "sha256:" + sha,
                "missing or changed archive " + kind)
        require(a["name"] == "prior-proof-kernel-" + kind + "-" + str(RUN) + "-1"
                and a["workflow_run"]["id"] == RUN
                and a["workflow_run"]["head_sha"] == HEAD, "archive source mismatch")
    print("KUUOS_V05_ARCHIVE_BINDING_GREEN", flush=True)


def project(parent, first, fresh, mcp, independent):
    frontier = validate_frontier(parent)
    require(digest(parent) == PACKET_DIGEST, "parent packet drift")
    require(digest(first) == DIRECT_DIGEST and digest(fresh) == DIRECT_DIGEST
            and first == fresh, "direct receipt digest mismatch")
    require(digest(mcp) == MCP_DIGEST, "MCP receipt digest mismatch")
    require(first["schema"] == "kuuos.prior-proof-kernel-recall.v0.5"
            and first["status"] == "DIRECT_SOURCE_LOCAL_OBSERVATION_GREEN"
            and first["original_sources_unchanged"] is True, "direct receipt scope")
    require(mcp["schema"] == "kuuos.prior-proof-real-lean-mcp.v0.5"
            and mcp["status"] == "REAL_LEAN_MCP_RECALL_GREEN"
            and mcp["mcp_version"] == "0.30.0", "MCP receipt scope")
    require(independent["schema"] == "kuuos.prior-proof-independent-recall.v0.5"
            and independent["status"] == "INDEPENDENT_SELECTED_OBSERVATIONS_AGREE"
            and independent["selected_count"] == 10, "independent receipt scope")
    for record in (first, fresh, mcp, independent):
        require((record["source_head"], record["source_tree"]) == (HEAD, TREE),
                "historical source identity mismatch")
        require(record["proof_authority"] is False and record["novelty_certified"] is False,
                "unexpected authority promotion")
    require(mcp["direct_receipt_digest"] == DIRECT_DIGEST
            and independent["first_direct_digest"] == DIRECT_DIGEST
            and independent["fresh_direct_digest"] == DIRECT_DIGEST
            and independent["first_mcp_digest"] == MCP_DIGEST, "receipt cross-binding mismatch")
    for k in ("source_subtrees", "pins", "lakefile_blob", "canonical_direct_options"):
        require(first[k] == parent[k], "environment drift " + k)
    for k in ("catalog_digest", "plan_digest"):
        require(first[k] == mcp[k], "MCP selection drift " + k)
    expected = {name: (p, refs) for p in PLANS for name, refs in p["names"].items()}
    rows = first["observations"]
    mr = {r["name"]: r for r in mcp["observations"]}
    require(len(rows) == len(mcp["observations"]) == len(mr) == len(expected) == 10
            and {r["name"] for r in rows} == set(mr) == set(expected), "inventory mismatch")
    selected = []
    for row in rows:
        name = row["name"]
        p, refs = expected[name]
        require((row["path"], row["blob"], row["module"]) ==
                (p["path"], p["blob"], p["module"]), "row source mismatch " + name)
        require(row["expected_direct_refs"] == refs
                and set(refs).issubset(row["proof_constants"])
                and not (set(row["axioms"]) - STANDARD)
                and row["proof_body_observed"] is True
                and row["direct_expression_constants_only"] is True, "proof scope " + name)
        require(hashlib.sha256(row["type_expr_repr"].encode()).hexdigest()
                == row["type_expr_sha256"], "type digest mismatch " + name)
        require(row["prior_packet_digest"] == PACKET_DIGEST
                and row["frontier_role"] == ("recorded_direct_reference" if name in frontier
                                           else "selected_related_existing_theorem"), "frontier binding " + name)
        m = mr[name]
        require(m["source_blob"] == row["blob"]
                and m["type_expr_sha256_from_direct"] == row["type_expr_sha256"]
                and m["axioms"] == row["axioms"], "MCP row mismatch " + name)
        selected.append({k: row[k] for k in FIELDS + EXTRA_FIELDS})
    return {
        "schema": "kuuos.prior-proof-kernel-memory.v0.5",
        "source_head": HEAD, "source_tree": TREE,
        **{k: first[k] for k in ("source_subtrees", "pins", "lakefile_blob",
                "canonical_direct_options", "catalog_digest", "plan_digest")},
        "parent_packet_digest": PACKET_DIGEST,
        "provenance": {"run_id": RUN, "run_attempt": ATTEMPT,
            "sandbox_job": 138827428008, "independent_job": 138830376315,
            **{kind + "_artifact_id": v[0] for kind, v in ARTIFACTS.items()},
            **{kind + "_artifact_sha256": v[1] for kind, v in ARTIFACTS.items()},
            "direct_receipt_digest": DIRECT_DIGEST,
            "independent_direct_receipt_digest": DIRECT_DIGEST,
            "mcp_receipt_digest": MCP_DIGEST,
            "independent_receipt_digest": digest(independent), "mcp_version": "0.30.0"},
        "observations": selected, "proof_authority": False,
        "novelty_certified": False, "full_transitive_proof_dependencies_verified": False}


def current_scope(root, parent, packet):
    obs = github_observation(os.environ["GITHUB_SHA"], "research_head")
    catalog = build_catalog(root, obs)
    require(catalog["source_subtrees"] == packet["source_subtrees"]
            and catalog["pins"] == packet["pins"], "current source scope drift")
    entries = {r["path"]: r["sha"] for r in obs["root_entries"]}
    require(entries.get("lakefile.toml") == packet["lakefile_blob"]
            and entries.get("lake-manifest.json") == "4b795033645fd37e42e67014abc3e0d5925a227c",
            "current Lake configuration drift")
    rows = parent["observations"] + packet["observations"]
    require(len(rows) == len({r["name"] for r in rows}) == 13, "combined inventory mismatch")
    files = {f["path"]: f for f in catalog["files"]}
    for row in rows:
        f = files[row["path"]]
        raw = (root / row["path"]).read_bytes()
        require(f["blob"] == row["blob"] == git_blob(raw)
                and f["module_path_lexical"] == row["module"]
                and hashlib.sha256(raw).hexdigest() == row["original_source_sha256"],
                "current source mismatch " + row["name"])
        matches = [d for d in f["declarations"] if d["id"] == row["lexical_id"]]
        require(len(matches) == 1, "missing lexical identity")
        d = matches[0]
        require(d["name_lexical"] == row["name"].rsplit(".", 1)[-1]
                and d["kind"] == "theorem" and d["line"] == row["line"]
                and d["signature_digest"] == row["signature_preview_digest"], "lexical source drift")
    print("KUUOS_V05_COMBINED_SOURCE_SCOPE_GREEN", json.dumps({
        "head": obs["source_head"], "tree": obs["source_tree"],
        "historical_v04": 3, "historical_v05": 10, "scope_matches": 13,
        "proof_authority": False}), flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--first", type=Path, required=True)
    p.add_argument("--fresh", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    observe_archives()
    parent = load_packet(ROOT)
    read = lambda f: json.loads(f.read_text())
    first, fresh, mcp, independent = (
        read(args.first/"direct.json"), read(args.fresh/"direct.json"),
        read(args.first/"mcp.json"), read(args.fresh/"independent.json"))
    packet = project(parent, first, fresh, mcp, independent)
    current_scope(ROOT, parent, packet)
    # Negative regressions on actual retrieved observations.
    import copy
    for index, field, value in ((0, "status", "failure"), (1, "source_head", "0"*40),
            (2, "direct_receipt_digest", "0"*64), (3, "selected_count", 9)):
        tampered = copy.deepcopy([first, fresh, mcp, independent])
        tampered[index][field] = value
        try:
            project(parent, *tampered)
        except ValueError:
            pass
        else:
            raise ValueError("tampered receipt unexpectedly admitted")
    print("KUUOS_V05_NEGATIVE_REPLAY_GREEN 4/4", flush=True)
    out = args.out.resolve()
    require(out.is_relative_to(ROOT/"artifacts"), "output outside artifacts")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        f.write(json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True)+"\n")
    print("KUUOS_V05_PACKET_DIGEST " + digest(packet), flush=True)
    print("KUUOS_V05_PACKET_JSON_BEGIN", flush=True)
    print(out.read_text(), end="", flush=True)
    print("KUUOS_V05_PACKET_JSON_END", flush=True)


if __name__ == "__main__":
    main()
