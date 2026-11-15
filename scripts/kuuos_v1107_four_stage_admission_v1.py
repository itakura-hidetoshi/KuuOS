#!/usr/bin/env python3
"""Verify source-bound v1.107 CodeAI -> pinned direct Lean -> real MCP receipts.

Only enables a separate exact-source independent Strict Lean build. MemoryOS
and producer-run success cannot attest a theorem or authorize merging.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import urllib.request

REPO = "itakura-hidetoshi/KuuOS"
PRODUCER_RUN = 43693040574
PRODUCER_HEAD = "b31ea108ea3889e4557876ffe96b2888ccf51c36"
PRODUCER_WORKFLOW = ".github/workflows/kuuos-v1107-codeai-visible-face-table-v1.yml"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107.lean"
PRIOR = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106.lean"
PRIOR_BLOB = "99ca499c470ba7b190623ed9e90e3f8d2dfb8058"
SELECTED = "round1-exact"
CANDIDATE_BLOB = "37c3e75c5d74c74b8d125983c9cd257f9757995a"

def require(ok, reason):
    if not ok:
        raise RuntimeError("KuuOS v1.107 NO_AUTHORITY: " + reason)

def blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def load_one_json(folder: Path, name: str) -> dict:
    paths=list(folder.rglob(name))
    require(len(paths)==1,"one immutable "+name)
    return json.loads(paths[0].read_text(encoding="utf-8"))

def main():
    root=Path(os.environ["GITHUB_WORKSPACE"])
    evidence=Path(os.environ["EVIDENCE_DIR"])
    token=os.environ.get("GITHUB_TOKEN")
    require(bool(token), "read-access token for producer run")
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{PRODUCER_RUN}",
        headers={"Accept":"application/vnd.github+json",
                 "Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-v1107-exact-source-admission"})
    with urllib.request.urlopen(req,timeout=45) as response:
        run=json.load(response)
    require(run.get("id")==PRODUCER_RUN
            and run.get("head_sha")==PRODUCER_HEAD
            and run.get("path")==PRODUCER_WORKFLOW
            and run.get("status")=="completed"
            and run.get("conclusion")=="success",
            "exact separate source-bound completed producer run")
    portfolio=load_one_json(evidence,"portfolio.json")
    mcp=load_one_json(evidence,"receipt.json")
    rows=portfolio.get("candidates")
    require(portfolio.get("source_head")==PRODUCER_HEAD
            and portfolio.get("imported_v1103_blob")==PRIOR_BLOB
            and portfolio.get("candidate_count")==5
            and isinstance(rows,list) and len(rows)==5
            and portfolio.get("source_restored") is True
            and portfolio.get("git_write_performed") is False
            and portfolio.get("independent_ci_certified") is False,
            "CodeAI portfolio source and authority restrictions")
    successful=[r for r in rows if isinstance(r,dict)
                and r.get("exit_code")==0 and r.get("olean_exists") is True
                and r.get("status")=="SUCCESS"
                and r.get("error_count")==0 and r.get("errors")==[]]
    require(len(successful)==4
            and any(r.get("variant")==SELECTED
                    and r.get("candidate_blob")==CANDIDATE_BLOB for r in successful),
            "exact direct Lean candidate; 4 successes and 1 failure retained")
    require(mcp.get("source_head")==PRODUCER_HEAD
            and mcp.get("candidate_count")==5
            and set(mcp.get("direct_lean_green",[]))==
                {r["variant"] for r in successful}
            and mcp.get("selected")==SELECTED
            and mcp.get("selected_blob")==CANDIDATE_BLOB
            and mcp.get("mcp_success") is True
            and mcp.get("mcp_errors")==0
            and mcp.get("second_direct_exit")==0
            and mcp.get("second_direct_success") is True
            and mcp.get("source_restored") is True
            and mcp.get("git_write_performed") is False
            and mcp.get("independent_ci_certified") is False
            and mcp.get("status")==
                "LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
            "real MCP, direct Lean and source restored")
    paths=list(evidence.rglob("candidate.lean"))
    require(len(paths)==1, "one selected MCP source")
    selected=paths[0].read_bytes()
    promoted=(root/TARGET).read_bytes()
    require(blob(promoted)==CANDIDATE_BLOB and promoted==selected,
            "same Git blob/codeAI/MCP/source bytes")
    require(blob((root/PRIOR).read_bytes())==PRIOR_BLOB,
            "unchanged independently certified prior v1.106")
    require(promoted.decode().startswith(
        "import KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106\n"),
        "same strict predecessor import")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(promoted.decode("utf-8")),
            "no sorry, new axioms or forbidden code")
    require((root/"lean-toolchain").read_text().strip() ==
            "leanprover/lean4:v4.30.0-rc2", "fixed Lean")
    m=json.loads((root/"lake-manifest.json").read_text())
    matches=[x for x in m.get("packages",[]) if x.get("name")=="mathlib"]
    require(len(matches)==1 and matches[0].get("rev")==
            "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
            "fixed mathlib source")
    receipt={"status":"STAGES_1_2_3_VERIFIED_INDEPENDENT_STRICT_LEAN_CAN_BEGIN",
             "producer_run":PRODUCER_RUN, "producer_head":PRODUCER_HEAD,
             "promoted_head":os.environ["PROMOTED_HEAD"],
             "exact_candidate_blob":CANDIDATE_BLOB,
             "direct_lean_green":len(successful),
             "real_mcp_success":True, "second_direct_success":True,
             "independent_ci_certified":False, "merge_authority":False}
    dest=Path("/tmp/kuuos-v1107-independent/admission.json")
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1107_STAGE123_SOURCE_ADMISSION "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    main()
