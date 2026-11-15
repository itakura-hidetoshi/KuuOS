#!/usr/bin/env python3
"""Admission only: verify exact v1.106 CodeAI -> direct Lean -> real Lean MCP evidence.
This does not certify the independently built source or authorize merge.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import urllib.request

REPO = "itakura-hidetoshi/KuuOS"
RUN = 43691061761
SOURCE_HEAD = "eb10c49d0842133fc3b87be3e8a87ff5b582067a"
SELECTED = "round4b-typed-val-simp"
PROOF_BLOB = "99ca499c470ba7b190623ed9e90e3f8d2dfb8058"
V105_BLOB = "d6a8a8e2136c1a5601fa01c02f5f478fdd827520"
PROOF = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106.lean"
V105 = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105.lean"
WORKFLOW = ".github/workflows/kuuos-v1106-codeai-label-table-round4b-v1.yml"

def require(ok, msg):
    if not ok:
        raise RuntimeError("v1.106 NO_AUTHORITY: " + msg)

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def sole_json(root, name):
    files = list(root.rglob(name))
    require(len(files) == 1, "unique " + name + " evidence")
    return json.loads(files[0].read_text(encoding="utf-8"))

def main():
    root = Path(os.environ["GITHUB_WORKSPACE"])
    ev = Path(os.environ["EVIDENCE_DIR"])
    token = os.environ["GITHUB_TOKEN"]
    require(bool(token), "Github token for exact producer-run reobservation")
    req = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + "/actions/runs/" + str(RUN),
        headers={"Accept": "application/vnd.github+json",
                 "Authorization": "Bearer " + token,
                 "User-Agent": "KuuOS-v1106-source-bound-independence"})
    with urllib.request.urlopen(req, timeout=45) as response:
        run = json.load(response)
    require(run.get("id") == RUN and run.get("head_sha") == SOURCE_HEAD
            and run.get("path") == WORKFLOW and run.get("status") == "completed"
            and run.get("conclusion") == "success", "immutable producer run")
    portfolio = sole_json(ev, "portfolio.json")
    mcp = sole_json(ev, "receipt.json")
    rows = portfolio.get("candidates")
    require(portfolio.get("source_head") == SOURCE_HEAD
            and portfolio.get("candidate_count") == 5
            and isinstance(rows, list) and len(rows) == 5
            and portfolio.get("source_restored") is True
            and portfolio.get("git_write_performed") is False
            and portfolio.get("independent_ci_certified") is False,
            "5 immutable source-bound CodeAI candidates")
    direct = [r for r in rows if r.get("status") == "SUCCESS"
              and r.get("error_count") == 0 and r.get("exit_code") == 0
              and r.get("olean_exists") is True and r.get("errors") == []]
    require(len(direct) == 1 and direct[0].get("variant") == SELECTED
            and direct[0].get("candidate_blob") == PROOF_BLOB,
            "pinned direct Lean successful candidate")
    require(mcp.get("source_head") == SOURCE_HEAD
            and mcp.get("candidate_count") == 5
            and mcp.get("direct_lean_green") == [SELECTED]
            and mcp.get("selected") == SELECTED
            and mcp.get("selected_blob") == PROOF_BLOB
            and mcp.get("mcp_success") is True
            and mcp.get("mcp_errors") == 0
            and mcp.get("second_direct_exit") == 0
            and mcp.get("second_direct_success") is True
            and mcp.get("source_restored") is True
            and mcp.get("git_write_performed") is False
            and mcp.get("independent_ci_certified") is False
            and mcp.get("status") == "LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
            "independent real Lean MCP and second direct Lean")
    source_paths = list(ev.rglob("candidate.lean"))
    require(len(source_paths) == 1, "one exact real-MCP candidate.lean")
    source = source_paths[0].read_bytes()
    promoted = (root / PROOF).read_bytes()
    require(source == promoted and blob(source) == PROOF_BLOB,
            "GitHub promoted Lean bytes exactly match successful MCP candidate")
    require(blob((root / V105).read_bytes()) == V105_BLOB,
            "certified prerequisite v1.105 source unchanged")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(promoted.decode("utf-8")),
            "no sorry/new axioms/admissions")
    require((root / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.30.0-rc2",
            "fixed Lean version")
    manifest = json.loads((root / "lake-manifest.json").read_text())
    pins = [p for p in manifest.get("packages", []) if p.get("name") == "mathlib"]
    require(len(pins) == 1 and pins[0].get("rev") ==
            "5450b53e5ddc75d46418fabb605edbf36bd0beb6", "fixed mathlib pin")
    record = {
        "source_head": SOURCE_HEAD, "producer_run": RUN,
        "promoted_head": os.environ["PROMOTED_HEAD"],
        "proof_blob": PROOF_BLOB, "direct_lean_success": True,
        "real_lean_mcp_success": True, "second_direct_lean_success": True,
        "status": "STAGES_1_2_3_VERIFIED_STAGE4_CAN_START",
        "independent_ci_certified": False, "merge_authority": False}
    out = Path("/tmp/kuuos-v1106-independent/admission.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print("KUUOS_V1106_STAGE123_SOURCE_ADMISSION " + json.dumps(record, sort_keys=True))

if __name__ == "__main__":
    main()
