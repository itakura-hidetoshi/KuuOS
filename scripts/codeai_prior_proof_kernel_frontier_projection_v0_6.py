#!/usr/bin/env python3
"""Project only exact archived v0.6 receipts into a read-only candidate packet.

The v0.4 and v0.5 historical packets are immutable. This candidate does not authorize
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
    FIELDS, STANDARD, ENVIRONMENT_BLOBS)
from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import (
    load_packets, PACKET_DIGESTS, V05_DIGEST)
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import build_catalog, search_catalog
from scripts.codeai_prior_proof_library_index_v0_3 import github_observation
from scripts.codeai_prior_proof_kernel_frontier_v0_6 import (
    PLANS, validate_frontier, EXTERNAL_RECORDED_REFS, CANONICAL_BASE)

HEAD = "8afa360f0eee06a8bc648e2957c9e4b9b4af7117"
TREE = "ee52f0a2805c012aae05fea0e20624f1e9ea00e3"
RUN = 45539451502
ATTEMPT = 1
JOBS = {
    138954083259: [
        "Direct source-local Lean types, proof constants and axiom observations",
        "Actual Lean MCP hover, diagnostics and verify only after direct green"],
    138956949097: ["Independently re-elaborate and compare source-local observations"]}
ARTIFACTS = {
    "local": (14989101416, "075e27dfd6867ba3505619fb5529a38b408559374deb3dd6dcde82dea481b6a7"),
    "independent": (14989630413, "cd49a4c0f9d6ca8200d11ce9b4cc7882fd305a39bf7e056a61abc6b06830aff0")}
DIRECT_DIGEST = "a21faff25607d162cdf7bb4f900a5c733784e2dc3b7af077b0b3c2519463ccf1"
MCP_DIGEST = "1e87bd3c24016437efe2b20536c5c49d8fc0c81bf6a29ea443f6ed0db3a4c070"
EXTRA_FIELDS = ("prior_packet_digest", "prior_packet_digests", "frontier_role")


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
    print("KUUOS_V06_ARCHIVE_BINDING_GREEN", flush=True)


def project(parent, previous, first, fresh, mcp, independent):
    frontier = validate_frontier(parent, previous)
    require(first["prior_packet_digests"] == PACKET_DIGESTS
            and first["canonical_starting_head"] == CANONICAL_BASE
            and first["external_recorded_refs"] == sorted(EXTERNAL_RECORDED_REFS),
            "recorded frontier or historical packet binding drift")
    require(digest(first) == DIRECT_DIGEST and digest(fresh) == DIRECT_DIGEST
            and first == fresh, "direct receipt digest mismatch")
    require(digest(mcp) == MCP_DIGEST, "MCP receipt digest mismatch")
    require(first["schema"] == "kuuos.prior-proof-kernel-recall.v0.6"
            and first["status"] == "DIRECT_SOURCE_LOCAL_OBSERVATION_GREEN"
            and first["original_sources_unchanged"] is True, "direct receipt scope")
    require(mcp["schema"] == "kuuos.prior-proof-real-lean-mcp.v0.6"
            and mcp["status"] == "REAL_LEAN_MCP_RECALL_GREEN"
            and mcp["mcp_version"] == "0.30.0", "MCP receipt scope")
    require(independent["schema"] == "kuuos.prior-proof-independent-recall.v0.6"
            and independent["status"] == "INDEPENDENT_SELECTED_OBSERVATIONS_AGREE"
            and independent["selected_count"] == 8, "independent receipt scope")
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
        require(first[k] == parent[k] == previous[k], "environment drift " + k)
    for k in ("catalog_digest", "plan_digest"):
        require(first[k] == mcp[k], "MCP selection drift " + k)
    expected = {name: (p, refs) for p in PLANS for name, refs in p["names"].items()}
    rows = first["observations"]
    mr = {r["name"]: r for r in mcp["observations"]}
    require(len(rows) == len(mcp["observations"]) == len(mr) == len(expected) == 8
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
        require(row["prior_packet_digest"] == V05_DIGEST
                and row["prior_packet_digests"] == PACKET_DIGESTS
                and name in frontier and row["frontier_role"] == "recorded_direct_reference",
                "frontier binding " + name)
        m = mr[name]
        require(m["source_blob"] == row["blob"]
                and m["type_expr_sha256_from_direct"] == row["type_expr_sha256"]
                and m["axioms"] == row["axioms"], "MCP row mismatch " + name)
        selected.append({k: row[k] for k in FIELDS + EXTRA_FIELDS})
    return {
        "schema": "kuuos.prior-proof-kernel-memory.v0.6",
        "source_head": HEAD, "source_tree": TREE,
        **{k: first[k] for k in ("source_subtrees", "pins", "lakefile_blob",
                "canonical_direct_options", "catalog_digest", "plan_digest")},
        "parent_packet_digest": V05_DIGEST,
        "prior_packet_digests": dict(PACKET_DIGESTS),
        "canonical_starting_head": CANONICAL_BASE,
        "external_recorded_refs": sorted(EXTERNAL_RECORDED_REFS),
        "provenance": {"run_id": RUN, "run_attempt": ATTEMPT,
            "sandbox_job": 138954083259, "independent_job": 138956949097,
            **{kind + "_artifact_id": v[0] for kind, v in ARTIFACTS.items()},
            **{kind + "_artifact_sha256": v[1] for kind, v in ARTIFACTS.items()},
            "direct_receipt_digest": DIRECT_DIGEST,
            "independent_direct_receipt_digest": DIRECT_DIGEST,
            "mcp_receipt_digest": MCP_DIGEST,
            "independent_receipt_digest": digest(independent), "mcp_version": "0.30.0"},
        "observations": selected, "proof_authority": False,
        "novelty_certified": False, "full_transitive_proof_dependencies_verified": False}


def current_scope(root, parent, previous, packet):
    obs = github_observation(os.environ["GITHUB_SHA"], "research_head")
    catalog = build_catalog(root, obs)
    require(catalog["source_subtrees"] == packet["source_subtrees"]
            and catalog["pins"] == packet["pins"], "current source scope drift")
    entries = {r["path"]: r["sha"] for r in obs["root_entries"]}
    require(entries.get("lakefile.toml") == packet["lakefile_blob"]
            and entries.get("lake-manifest.json") == "4b795033645fd37e42e67014abc3e0d5925a227c",
            "current Lake configuration drift")
    rows = parent["observations"] + previous["observations"] + packet["observations"]
    require(len(rows) == len({r["name"] for r in rows}) == len({r["lexical_id"] for r in rows}) == 21,
            "combined inventory mismatch")
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
    print("KUUOS_V06_COMBINED_SOURCE_SCOPE_GREEN", json.dumps({
        "head": obs["source_head"], "tree": obs["source_tree"],
        "historical_v04": 3, "historical_v05": 10, "historical_v06": 8, "scope_matches": 21,
        "proof_authority": False}), flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--first", type=Path, required=True)
    p.add_argument("--fresh", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    observe_archives()
    parent, previous = load_packets(ROOT)
    read = lambda f: json.loads(f.read_text())
    first, fresh, mcp, independent = (
        read(args.first/"direct.json"), read(args.fresh/"direct.json"),
        read(args.first/"mcp.json"), read(args.fresh/"independent.json"))
    packet = project(parent, previous, first, fresh, mcp, independent)
    current_scope(ROOT, parent, previous, packet)
    # Negative regressions on actual retrieved observations.
    import copy
    for index, field, value in ((0, "status", "failure"), (1, "source_head", "0"*40),
            (2, "direct_receipt_digest", "0"*64), (3, "selected_count", 7)):
        tampered = copy.deepcopy([first, fresh, mcp, independent])
        tampered[index][field] = value
        try:
            project(parent, previous, *tampered)
        except ValueError:
            pass
        else:
            raise ValueError("tampered receipt unexpectedly admitted")
    for p in (parent, previous):
        bad = copy.deepcopy(p)
        bad["observations"][0]["expected_direct_refs"] = []
        try:
            project(bad if p is parent else parent, bad if p is previous else previous,
                    first, fresh, mcp, independent)
        except ValueError:
            pass
        else:
            raise ValueError("tampered historical packet unexpectedly admitted")
    print("KUUOS_V06_NEGATIVE_REPLAY_GREEN 6/6", flush=True)
    out = args.out.resolve()
    require(out.is_relative_to(ROOT/"artifacts"), "output outside artifacts")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        f.write(json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True)+"\n")
    print("KUUOS_V06_PACKET_DIGEST " + digest(packet), flush=True)
    print("KUUOS_V06_PACKET_JSON_BEGIN", flush=True)
    print(out.read_text(), end="", flush=True)
    print("KUUOS_V06_PACKET_JSON_END", flush=True)


if __name__ == "__main__":
    main()
