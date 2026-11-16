#!/usr/bin/env python3
"""v1.112 stage-123 source admission; only separate strict CI may certify stage 4."""
from __future__ import annotations
import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

REPO = "itakura-hidetoshi/KuuOS"
PRODUCER_RUN = 43759371015
PRODUCER_HEAD = "a781fca41db15fb0d29c8a071ad67a253f36031d"
PRODUCER_TREE = "52c9ff0ab3406a920a30e3448c2be2f4160b0cf6"
WORKFLOW = ".github/workflows/kuuos-v1112-codeai-all-dimensions-round2-v1.yml"
SOURCE = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112.lean"
PREDECESSOR = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111.lean"
PRED_BLOB = "35dc6ddf9bcd6ecd4f7141674e75055c306dbfe9"
BLOB = "c9977fe0144e922da23eddde1d6eba2ec2f51e65"
SHA256 = "f789e97421d3e17197eb289b559e1dc176c286d689099602c17303685a7bc3ea"
SELECTED = "round2-fin-cases-simp-all"
MEMORY = "memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v1112_round2_v1.json"
BASE = "validation/kuuos-v1111-rlp-exact-source-20261115"
BASE_SHA = "66bd3e71739f8a841d7d2723ab45a1475fd276ca"
BRANCH = "research/kuuos-typeA-all-dimensions-v112-20261116"
RESULTS = {
    "round2-fin-cases-simp-all": (BLOB, "SUCCESS", 0),
    "round2-fin-cases-nonempty": ("5eb045f086104ce3ec2baaa3f3f8e74522c705a5", "SUCCESS", 0),
    "round2-fin-cases-low-simpa": ("9adc7b7ab3da29d9dbd689e32efcedb222b43461", "SUCCESS", 0),
    "round2-explicit-bounds": ("e5dd59c28af9160ebafcc38c4d238664692ac97c", "FAILURE", 2),
}

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V1112_NO_AUTHORITY: " + message)

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def load_one(directory: Path, name: str) -> dict:
    files = list(directory.rglob(name))
    require(len(files) == 1, "unique evidence: " + name)
    return json.loads(files[0].read_text(encoding="utf-8"))

def github(path: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    require(bool(token), "missing GitHub read token")
    req = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + "/" + path,
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "KuuOS-v1112-exact-source-independent"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)

def main() -> None:
    root = Path(os.environ["GITHUB_WORKSPACE"])
    evidence = Path(os.environ["EVIDENCE_DIR"])
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr = event.get("pull_request") or {}
    head, base = pr.get("head") or {}, pr.get("base") or {}
    promoted_head = os.environ["PROMOTED_HEAD"]
    require((event.get("repository") or {}).get("full_name") == REPO
            and event.get("number") == 3557 and pr.get("draft") is True
            and head.get("ref") == BRANCH and base.get("ref") == BASE
            and base.get("sha") == BASE_SHA and head.get("sha") == promoted_head,
            "wrong PR/base/checkout event")
    require(re.fullmatch(r"[0-9a-f]{40}", promoted_head) is not None, "bad promoted HEAD")
    actual_pr = github("pulls/3557")
    require(actual_pr.get("head", {}).get("sha") == promoted_head
            and actual_pr.get("base", {}).get("sha") == BASE_SHA,
            "source HEAD changed during independent validation")
    producer = github("actions/runs/" + str(PRODUCER_RUN))
    require(producer.get("id") == PRODUCER_RUN
            and producer.get("head_sha") == PRODUCER_HEAD
            and producer.get("path") == WORKFLOW
            and producer.get("status") == "completed"
            and producer.get("conclusion") == "success",
            "producer is not an exact successful source-bound experiment")
    commit = github("git/commits/" + PRODUCER_HEAD)
    require(commit.get("sha") == PRODUCER_HEAD
            and (commit.get("tree") or {}).get("sha") == PRODUCER_TREE,
            "source-bound producer tree changed")
    current = github("git/commits/" + promoted_head)
    require(current.get("sha") == promoted_head
            and re.fullmatch(r"[0-9a-f]{40}", (current.get("tree") or {}).get("sha", "")),
            "promoted source tree invalid")
    portfolio = load_one(evidence, "portfolio.json")
    mcp = load_one(evidence, "receipt.json")
    require(portfolio.get("source_head") == PRODUCER_HEAD
            and portfolio.get("source_tree") == PRODUCER_TREE
            and portfolio.get("imported_v1103_blob") == PRED_BLOB
            and portfolio.get("candidate_count") == 4
            and portfolio.get("source_restored") is True
            and portfolio.get("git_write_performed") is False
            and portfolio.get("independent_ci_certified") is False,
            "CodeAI producer provenance/source restoration")
    rows = portfolio.get("candidates")
    require(isinstance(rows, list) and len(rows) == 4
            and {x.get("variant") for x in rows} == set(RESULTS),
            "exact four candidate portfolio")
    for row in rows:
        blob, status, err_count = RESULTS[row["variant"]]
        require(row.get("candidate_blob") == blob and row.get("status") == status
                and row.get("error_count") == err_count
                and row.get("exit_code") == (0 if err_count == 0 else 1)
                and row.get("olean_exists") is (err_count == 0)
                and isinstance(row.get("errors"), list)
                and len(row["errors"]) == err_count,
                "observed candidate status changed: " + row["variant"])
    failure = next(x for x in rows if x["variant"] == "round2-explicit-bounds")
    require(all("omega could not prove the goal" in s for s in failure["errors"]),
            "failure diagnostics must be observed, never causalized")
    require(mcp.get("source_head") == PRODUCER_HEAD
            and mcp.get("candidate_count") == 4
            and set(mcp.get("direct_lean_green", [])) == set(RESULTS) - {"round2-explicit-bounds"}
            and mcp.get("selected") == SELECTED and mcp.get("selected_blob") == BLOB
            and mcp.get("mcp_success") is True and mcp.get("mcp_errors") == 0
            and mcp.get("second_direct_success") is True
            and mcp.get("second_direct_exit") == 0
            and mcp.get("source_restored") is True
            and mcp.get("git_write_performed") is False
            and mcp.get("independent_ci_certified") is False
            and mcp.get("status") == "LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
            "actual selected direct Lean/MCP/second direct evidence")
    candidates = list(evidence.rglob("candidate.lean"))
    require(len(candidates) == 1, "unique actual real MCP selected proof")
    promoted = (root / SOURCE).read_bytes()
    require(promoted == candidates[0].read_bytes() and git_blob(promoted) == BLOB
            and hashlib.sha256(promoted).hexdigest() == SHA256,
            "byte-identical generated candidate, real MCP artifact, GitHub source")
    require(git_blob((root / PREDECESSOR).read_bytes()) == PRED_BLOB,
            "pinned v1.111 source altered")
    require(promoted.decode("utf-8").startswith(
            "import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111\n"),
            "wrong imported predecessor")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(promoted.decode("utf-8")),
            "forbidden proof weakening, axioms or sorry")
    from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed
    from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory
    recorded = read_observation_seed(root / MEMORY)
    all_cases = read_observation_directory(root / "memoryos/external/github/2026/11")
    require(len(recorded) == 4 and len(all_cases) >= 48
            and len({x["id"] for x in all_cases}) == len(all_cases),
            "append-only MemoryOS four unique round2 observations")
    for x in recorded:
        require(x["source_head"] == PRODUCER_HEAD and x["source_tree"] == PRODUCER_TREE
                and x["imported_blob"] == PRED_BLOB and x["producer_run"] == PRODUCER_RUN
                and x["candidate_blob"] == RESULTS[x["variant"]][0]
                and x["outcome"] == ("DIRECT_LEAN_FAILURE" if x["variant"] == "round2-explicit-bounds" else "DIRECT_LEAN_SUCCESS")
                and x["causal_status"] == "UNVERIFIED_HYPOTHESIS"
                and x["independent_run"] is None,
                "memory is only experiment evidence, no proof authority")
    require((root / "lean-toolchain").read_text().strip() ==
            "leanprover/lean4:v4.30.0-rc2", "Lean pin changed")
    manifest = json.loads((root / "lake-manifest.json").read_text())
    pins = [p.get("rev") for p in manifest.get("packages", [])
            if p.get("name") == "mathlib"]
    require(pins == ["5450b53e5ddc75d46418fabb605edbf36bd0beb6"],
            "mathlib pin changed")
    out = Path("/tmp/kuuos-v1112-independent")
    out.mkdir(parents=True, exist_ok=True)
    receipt = {"stage": "CODEAI_DIRECT_AND_REAL_MCP_ADMITTED_ONLY",
               "producer_run": PRODUCER_RUN, "producer_head": PRODUCER_HEAD,
               "producer_tree": PRODUCER_TREE, "promoted_head": promoted_head,
               "promoted_tree": current["tree"]["sha"],
               "selected_blob": BLOB, "MemoryOS_added": len(recorded),
               "direct_green": 3, "real_mcp_success": True,
               "second_direct_success": True, "independent_ci_certified": False,
               "merge_authority": False}
    (out / "admission.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print("KUUOS_V1112_STAGE123_ADMISSION", json.dumps(receipt, sort_keys=True))

if __name__ == "__main__":
    main()
