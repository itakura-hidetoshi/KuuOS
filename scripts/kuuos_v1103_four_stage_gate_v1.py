#!/usr/bin/env python3
"""Validate v1.103 immutable CodeAI -> direct Lean -> real MCP precommit lineage.

Read-only, fail-closed. This never certifies independent CI or grants merge authority.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

REPO="itakura-hidetoshi/KuuOS"
SOURCE_HEAD="2ee48e0e55509ec30f955dae2274a2e5b5dd4aa1"
SOURCE_TREE="34026cc3341b57711c301ef775c46f47afd3119c"
SOURCE_BLOB="04de7e72813e0e28c9d4e499b68876f081b3bdba"
CANDIDATE_BLOB="ff2e6a09e2c064a23207ee1323bc14182c86d7cd"
PRODUCER_RUN=43683314843
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
SELECTED="round2-congr-rw"

def require(value, why):
    if not value:
        raise RuntimeError("NO_AUTHORITY: "+why)

def sha_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def one(root, filename):
    matches=list(root.rglob(filename))
    require(len(matches)==1,"unique artifact "+filename)
    return json.loads(matches[0].read_text())

def authentic_source_run():
    token=os.getenv("GITHUB_TOKEN","")
    require(token,"GitHub Actions read authorization")
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{PRODUCER_RUN}",
        headers={"Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-v1103-ordered-proof-gate",
                 "Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(req,timeout=40) as resp:
        run=json.load(resp)
    require(run.get("id")==PRODUCER_RUN and
            run.get("head_sha")==SOURCE_HEAD and
            run.get("status")=="completed" and
            run.get("conclusion")=="success" and
            run.get("path")==".github/workflows/kuuos-v1103-codeai-round2-v1.yml",
            "producer completed/SUCCESS exact source and workflow")
    return run

def main():
    evidence=Path(os.environ["EVIDENCE_ROOT"])
    root=Path(os.environ["GITHUB_WORKSPACE"])
    head=os.environ["PROMOTED_HEAD"]
    require(re.fullmatch("[0-9a-f]{40}",head),"promoted GitHub HEAD")
    authentic_source_run()
    portfolio=one(evidence,"portfolio_receipt.json")
    mcp=one(evidence,"receipt.json")
    require(portfolio.get("head")==SOURCE_HEAD and
            portfolio.get("source_tree")==SOURCE_TREE and
            portfolio.get("original_blob")==SOURCE_BLOB,
            "original CodeAI source lineage")
    require(portfolio.get("source_restored") is True and
            portfolio.get("git_written") is False and
            portfolio.get("independent_ci_certified") is False,
            "CodeAI source restoration and authority")
    require(re.fullmatch("[0-9a-f]{64}",portfolio.get("portfolio_receipt","")),
            "source-bound CodeAI portfolio digest")
    rows=portfolio.get("candidates")
    require(isinstance(rows,list) and len(rows)==6,"six CodeAI proposals")
    names=[r.get("variant") for r in rows]
    require(len(set(names))==6 and SELECTED in names,"unique candidate names")
    for item in rows:
        require(re.fullmatch("[0-9a-f]{40}",str(item.get("candidate_blob",""))) and
                re.fullmatch("[0-9a-f]{64}",str(item.get("candidate_receipt",""))),
                "per-candidate CodeAI content and receipt identity")
    passed={r["variant"] for r in rows
            if r.get("status")=="SUCCESS" and r.get("exit_code")==0
            and r.get("olean_exists") is True and
            r.get("error_count")==0 and r.get("errors")==[]}
    selected=next(r for r in rows if r["variant"]==SELECTED)
    require(SELECTED in passed and selected["candidate_blob"]==CANDIDATE_BLOB,
            "selected direct Lean green on exact proof blob")
    require(mcp.get("source_head")==SOURCE_HEAD and
            mcp.get("original_blob")==SOURCE_BLOB and
            mcp.get("selected")==SELECTED and
            set(mcp.get("strict_direct_green",[]))==passed,
            "real MCP must select a direct-Lean green candidate only")
    require(mcp.get("mcp_success") is True and mcp.get("mcp_errors")==0,
            "actual MCP diagnostics incomplete/red")
    for key in ("lean_goal_183","lean_goal_198",
                "lean_multi_attempt_183","lean_multi_attempt_198",
                "mcp_diagnostic_sha256","second_direct_log_sha256"):
        require(re.fullmatch("[0-9a-f]{64}",str(mcp.get(key,""))),
                "missing actual MCP proof state / second direct receipt "+key)
    require(mcp.get("second_direct_green") is True and
            mcp.get("second_direct_exit")==0 and
            mcp.get("source_restored") is True and
            mcp.get("git_mutation") is False and
            mcp.get("independent_ci_certified") is False and
            mcp.get("status")=="LOCAL_MCP_AND_SECOND_DIRECT_GREEN_CI_NOT_CERTIFIED",
            "MCP green plus restoration, not independent CI")
    require(sha_blob((root/TARGET).read_bytes())==CANDIDATE_BLOB,
            "promoted exact source blob mismatch")
    require((root/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2",
            "Lean compiler pin")
    manifest=json.loads((root/"lake-manifest.json").read_text())
    deps=[p for p in manifest.get("packages",[]) if p.get("name")=="mathlib"]
    require(len(deps)==1 and deps[0].get("rev")==
            "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
            "mathlib pin")
    record={"status":"STAGES_1_2_3_VERIFIED_READY_FOR_INDEPENDENT_CI",
            "codeai_source_head":SOURCE_HEAD,
            "codeai_run":PRODUCER_RUN,"promoted_head":head,
            "candidate_count":6,"direct_green_count":len(passed),
            "mcp_zero_errors":True,"second_direct_lean_success":True,
            "selected_blob":CANDIDATE_BLOB,
            "stage4_independent_ci_certified":False,
            "merge_authority":False}
    out=Path(os.environ["ADMISSION_RECEIPT_PATH"])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1103_FOUR_STAGE_ADMISSION "+json.dumps(record,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
