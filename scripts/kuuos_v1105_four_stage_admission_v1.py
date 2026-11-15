#!/usr/bin/env python3
"""Source-bound gate for v1.105 CodeAI -> direct pinned Lean -> real Lean MCP.

The result is only authorization to START independent exact-source CI.
It never claims an independent Lean proof or merge authority.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

REPO="itakura-hidetoshi/KuuOS"
CODEAI_HEAD="b28157aea549e833044da7f8fa7987157df874d8"
CODEAI_TREE="979bf78dbd8d4f5fc46a51cbd0c2524f22a6da1b"
CODEAI_RUN=43687986358
PREVIOUS_BLOB="6c4c3a2243796aa19d494c685b1b52796feeb2dd"
PROMOTED_BLOB="d6a8a8e2136c1a5601fa01c02f5f478fdd827520"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105.lean"
SELECTED="round3-four-index-refl"

def check(condition: bool, message: str):
    if not condition:
        raise RuntimeError("v1.105 NO_AUTHORITY: "+message)

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def load_exact(base: Path, name: str) -> dict:
    matched=list(base.rglob(name))
    check(len(matched)==1,"one artifact "+name)
    return json.loads(matched[0].read_text())

def run_observation():
    token=os.environ["GITHUB_TOKEN"]
    check(bool(token),"GitHub authentication")
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{CODEAI_RUN}",
        headers={"Accept":"application/vnd.github+json",
                 "Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-v1105-source-ordered-gate"})
    with urllib.request.urlopen(req,timeout=45) as resp:
        row=json.load(resp)
    check(row.get("id")==CODEAI_RUN and row.get("head_sha")==CODEAI_HEAD
          and row.get("path")==".github/workflows/kuuos-v1105-codeai-visible-face-round3-v1.yml"
          and row.get("status")=="completed"
          and row.get("conclusion")=="success",
          "source-bound completed CodeAI+MCP producer run")

def main():
    evidence=Path(os.environ["EVIDENCE_DIR"])
    root=Path(os.environ["GITHUB_WORKSPACE"])
    promoted_head=os.environ["PROMOTED_HEAD"]
    check(re.fullmatch(r"[0-9a-f]{40}",promoted_head) is not None,
          "promoted immutable GitHub head")
    run_observation()
    portfolio=load_exact(evidence,"portfolio.json")
    mcp=load_exact(evidence,"receipt.json")
    check(portfolio.get("source_head")==CODEAI_HEAD
          and portfolio.get("source_tree")==CODEAI_TREE
          and portfolio.get("imported_v1103_blob")==PREVIOUS_BLOB
          and portfolio.get("source_restored") is True
          and portfolio.get("independent_ci_certified") is False
          and portfolio.get("git_write_performed") is False,
          "CodeAI exact source/closure/authority")
    rows=portfolio.get("candidates")
    check(portfolio.get("candidate_count")==3 and
          isinstance(rows,list) and len(rows)==3,
          "three CodeAI candidates required")
    check(re.fullmatch(r"[0-9a-f]{64}",str(portfolio.get("codeai_receipt","")))
          is not None,"sealed CodeAI portfolio identity")
    for r in rows:
        check(re.fullmatch(r"[0-9a-f]{64}",str(r.get("codeai_receipt","")))
              is not None and
              re.fullmatch(r"[0-9a-f]{40}",str(r.get("candidate_blob","")))
              is not None,"CodeAI candidate immutable record")
    direct_green=[r for r in rows if r.get("status")=="SUCCESS"
                  and r.get("exit_code")==0
                  and r.get("olean_exists") is True
                  and r.get("error_count")==0 and r.get("errors")==[]]
    check(len(direct_green)==3
          and any(r["variant"]==SELECTED
                  and r["candidate_blob"]==PROMOTED_BLOB
                  for r in direct_green),
          "selected proof must have pinned direct Lean SUCCESS and olean")
    check(mcp.get("source_head")==CODEAI_HEAD
          and mcp.get("candidate_count")==3
          and set(mcp.get("direct_lean_green",[]))=={r["variant"] for r in direct_green}
          and mcp.get("selected")==SELECTED
          and mcp.get("selected_blob")==PROMOTED_BLOB
          and mcp.get("mcp_success") is True
          and mcp.get("mcp_errors")==0
          and mcp.get("second_direct_exit")==0
          and mcp.get("second_direct_success") is True
          and mcp.get("source_restored") is True
          and mcp.get("git_write_performed") is False
          and mcp.get("independent_ci_certified") is False
          and mcp.get("status")=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
          "real Lean MCP, independent second direct Lean, and source restoration")
    expected=next((e for e in evidence.rglob("candidate.lean")
                  if e.is_file()),None)
    check(expected is not None and blob_sha(expected.read_bytes())==PROMOTED_BLOB,
          "real MCP selected source bytes unavailable")
    current=(root/TARGET).read_bytes()
    check(blob_sha(current)==PROMOTED_BLOB and current==expected.read_bytes(),
          "promoted source must equal CodeAI/MCP exact selected bytes")
    check((root/"lean-toolchain").read_text().strip()
          =="leanprover/lean4:v4.30.0-rc2","pinned Lean toolchain")
    manifest=json.loads((root/"lake-manifest.json").read_text())
    matches=[p for p in manifest["packages"] if p.get("name")=="mathlib"]
    check(len(matches)==1 and matches[0].get("rev")
          =="5450b53e5ddc75d46418fabb605edbf36bd0beb6",
          "fixed mathlib revision")
    receipt={
        "status":"STAGES_1_2_3_VERIFIED_STAGE4_CAN_START",
        "codeai_source_head":CODEAI_HEAD,
        "codeai_run":CODEAI_RUN,
        "promoted_source_head":promoted_head,
        "proof_blob":PROMOTED_BLOB,
        "direct_lean_green":1,
        "real_mcp_zero_errors":True,
        "second_direct_lean_green":True,
        "independent_ci_certified":False,
        "merge_authority":False,
    }
    out=Path(os.environ["OUTPUT_RECEIPT"])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1104_FOUR_STAGE_ADMISSION "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    main()
