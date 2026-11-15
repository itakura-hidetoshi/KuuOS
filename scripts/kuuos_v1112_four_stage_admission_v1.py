#!/usr/bin/env python3
"""v1.112 stage-123 admission; exact code provenance is NOT independent proof.

Verifies the real source-bound CodeAI candidate portfolio, fixed direct Lean,
real Lean MCP and second direct Lean before a separate clean Lean CI.
"""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
import urllib.request

REPO="itakura-hidetoshi/KuuOS"
PRODUCER_RUN=43712327972
PRODUCER_HEAD="df85701cdabb757d8831f50b1134a42222114980"
PRODUCER_WORKFLOW=".github/workflows/kuuos-v1112-codeai-all-typeA-rlp-v1.yml"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111.lean"
PRIOR_BLOB="35dc6ddf9bcd6ecd4f7141674e75055c306dbfe9"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112.lean"
SELECTED="round1-fin-cases"
BLOB="9934de88791e6ffc4c085e14ca1736168d17c93b"

def require(ok, detail):
    if not ok:
        raise RuntimeError("v1.112 NO_AUTHORITY: "+detail)
def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def load_one(root,name):
    found=list(root.rglob(name))
    require(len(found)==1,"unique immutable "+name)
    return json.loads(found[0].read_text(encoding="utf-8"))

def main():
    root=Path(os.environ["GITHUB_WORKSPACE"])
    evidence=Path(os.environ["EVIDENCE_DIR"])
    token=os.environ.get("GITHUB_TOKEN")
    require(bool(token),"GitHub producer run read token")
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{PRODUCER_RUN}",
        headers={"Accept":"application/vnd.github+json",
                 "Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-v1112-exact-source-audit"})
    with urllib.request.urlopen(req,timeout=45) as response:
        run=json.load(response)
    require(run.get("id")==PRODUCER_RUN
            and run.get("head_sha")==PRODUCER_HEAD
            and run.get("path")==PRODUCER_WORKFLOW
            and run.get("status")=="completed"
            and run.get("conclusion")=="success",
            "completed source-bound producer run, not itself a Lean certificate")
    portfolio=load_one(evidence,"portfolio.json")
    mcp=load_one(evidence,"receipt.json")
    rows=portfolio.get("candidates")
    require(portfolio.get("source_head")==PRODUCER_HEAD
            and portfolio.get("imported_v1103_blob")==PRIOR_BLOB
            and portfolio.get("candidate_count")==3
            and isinstance(rows,list) and len(rows)==5
            and portfolio.get("source_restored") is True
            and portfolio.get("git_write_performed") is False
            and portfolio.get("independent_ci_certified") is False,
            "CodeAI source, pins and non-authoritative producer scope")
    green=[r for r in rows if isinstance(r,dict)
           and r.get("status")=="SUCCESS" and r.get("exit_code")==0
           and r.get("olean_exists") is True and r.get("error_count")==0
           and r.get("errors")==[]]
    require(len(green)==1
            and any(r.get("variant")==SELECTED and r.get("candidate_blob")==BLOB
                    for r in green),
            "one independently direct Lean green candidate and selected blob")
    require(mcp.get("source_head")==PRODUCER_HEAD
            and mcp.get("candidate_count")==3
            and set(mcp.get("direct_lean_green",[]))==
                {r["variant"] for r in green}
            and mcp.get("selected")==SELECTED and mcp.get("selected_blob")==BLOB
            and mcp.get("mcp_success") is True
            and mcp.get("mcp_errors")==0
            and mcp.get("second_direct_exit")==0
            and mcp.get("second_direct_success") is True
            and mcp.get("source_restored") is True
            and mcp.get("git_write_performed") is False
            and mcp.get("independent_ci_certified") is False
            and mcp.get("status")=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
            "selected real Lean MCP and verified second direct Lean")
    source=list(evidence.rglob("candidate.lean"))
    require(len(source)==1,"unique real MCP selected proof")
    expected=source[0].read_bytes()
    promoted=(root/TARGET).read_bytes()
    require(promoted==expected and blob(promoted)==BLOB,
            "byte-identical CodeAI, direct Lean, MCP and promoted GitHub proof")
    require(blob((root/PRIOR).read_bytes())==PRIOR_BLOB,
            "exact v1.111 independently certified predecessor source")
    require(promoted.decode("utf-8").startswith(
        "import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111\n"),
        "invariant exact predecessor import")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(promoted.decode("utf-8")),
            "forbid sorry, new axiom and source weakening")
    require((root/"lean-toolchain").read_text().strip()==
            "leanprover/lean4:v4.30.0-rc2","fixed toolchain")
    manifest=json.loads((root/"lake-manifest.json").read_text())
    mathlib=[p.get("rev") for p in manifest.get("packages",[])
             if p.get("name")=="mathlib"]
    require(mathlib==["5450b53e5ddc75d46418fabb605edbf36bd0beb6"],
            "fixed mathlib source")
    receipt={"status":"STAGES_1_2_3_VERIFIED_STAGE4_CAN_BEGIN",
             "producer_run":PRODUCER_RUN,"producer_head":PRODUCER_HEAD,
             "promoted_head":os.environ["PROMOTED_HEAD"],
             "selected_blob":BLOB,"direct_lean_green":len(green),
             "real_mcp_success":True,"second_direct_success":True,
             "independent_ci_certified":False,"merge_authority":False}
    out=Path("/tmp/kuuos-v1112-independent/admission.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1112_STAGE123_ADMISSION "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    main()
