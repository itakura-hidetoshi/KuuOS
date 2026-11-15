#!/usr/bin/env python3
"""v1.108 independent source admission only; does not itself certify a theorem."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
import urllib.request

REPO="itakura-hidetoshi/KuuOS"
PRODUCER_RUN=43694200399
PRODUCER_HEAD="6f364c895cb7dbd6eec2a9c7c2c2c0e6405addd3"
WORKFLOW=".github/workflows/kuuos-v1108-codeai-four-implies-five-v1.yml"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108.lean"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107.lean"
PRIOR_BLOB="37c3e75c5d74c74b8d125983c9cd257f9757995a"
SELECTED="omega-bounds"
PROOF_BLOB="6071b265507c1798c8a61ce87a0a828713c97c63"

def require(condition,detail):
    if not condition:
        raise RuntimeError("v1.108 NO_AUTHORITY: "+detail)

def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def one_json(folder,name):
    files=list(Path(folder).rglob(name))
    require(len(files)==1,"unique producer "+name)
    return json.loads(files[0].read_text(encoding="utf-8"))

def main():
    root=Path(os.environ["GITHUB_WORKSPACE"])
    evidence=Path(os.environ["EVIDENCE_DIR"])
    token=os.environ.get("GITHUB_TOKEN")
    require(bool(token),"GitHub source/run read token")
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{PRODUCER_RUN}",
        headers={"Accept":"application/vnd.github+json",
                 "Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-v1108-exact-source-audit"})
    with urllib.request.urlopen(req,timeout=45) as response:
        run=json.load(response)
    require(run.get("head_sha")==PRODUCER_HEAD
            and run.get("id")==PRODUCER_RUN
            and run.get("path")==WORKFLOW
            and run.get("status")=="completed"
            and run.get("conclusion")=="success",
            "exact immutable producer run")
    portfolio=one_json(evidence,"portfolio.json")
    mcp=one_json(evidence,"receipt.json")
    rows=portfolio.get("candidates")
    require(portfolio.get("source_head")==PRODUCER_HEAD
            and portfolio.get("imported_v1103_blob")==PRIOR_BLOB
            and portfolio.get("candidate_count")==3
            and isinstance(rows,list) and len(rows)==3
            and portfolio.get("source_restored") is True
            and portfolio.get("git_write_performed") is False
            and portfolio.get("independent_ci_certified") is False,
            "non-authoritative, source-bound CodeAI portfolio")
    green=[r for r in rows if isinstance(r,dict)
           and r.get("status")=="SUCCESS" and r.get("exit_code")==0
           and r.get("olean_exists") is True and r.get("error_count")==0
           and r.get("errors")==[]]
    require(len(green)==3
            and any(r["variant"]==SELECTED and r["candidate_blob"]==PROOF_BLOB for r in green),
            "pinned direct Lean source and exact selected blob")
    require(mcp.get("source_head")==PRODUCER_HEAD
            and mcp.get("candidate_count")==3
            and set(mcp.get("direct_lean_green",[]))==
                {r["variant"] for r in green}
            and mcp.get("selected")==SELECTED
            and mcp.get("selected_blob")==PROOF_BLOB
            and mcp.get("mcp_success") is True and mcp.get("mcp_errors")==0
            and mcp.get("second_direct_exit")==0
            and mcp.get("second_direct_success") is True
            and mcp.get("source_restored") is True
            and mcp.get("git_write_performed") is False
            and mcp.get("independent_ci_certified") is False
            and mcp.get("status")=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI",
            "real Lean MCP and independent second pinned direct Lean")
    files=list(evidence.rglob("candidate.lean"))
    require(len(files)==1,"exact selected MCP candidate source")
    selected=files[0].read_bytes()
    promoted=(root/TARGET).read_bytes()
    require(promoted==selected and blob(promoted)==PROOF_BLOB,
            "promoted bytes must equal independently verified exact candidate")
    require(blob((root/PRIOR).read_bytes())==PRIOR_BLOB,
            "unchanged exact v1.107 independent certificate source")
    require(promoted.decode().startswith(
        "import KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107\n"),
        "valid preceding import")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(promoted.decode()),
            "no axiom/sorry/forbidden code")
    require((root/"lean-toolchain").read_text().strip() ==
            "leanprover/lean4:v4.30.0-rc2","Lean toolchain pin")
    m=json.loads((root/"lake-manifest.json").read_text())
    rev=[x["rev"] for x in m.get("packages",[]) if x.get("name")=="mathlib"]
    require(rev==["5450b53e5ddc75d46418fabb605edbf36bd0beb6"],
            "exact mathlib pin")
    receipt={"status":"STAGES_1_2_3_VERIFIED_STAGE4_CAN_BEGIN",
             "producer_run":PRODUCER_RUN,"producer_head":PRODUCER_HEAD,
             "promoted_head":os.environ["PROMOTED_HEAD"],
             "selected_blob":PROOF_BLOB,"direct_lean_green":3,
             "real_lean_mcp_success":True,"second_direct_success":True,
             "independent_ci_certified":False,"merge_authority":False}
    dest=Path("/tmp/kuuos-v1108-independent/admission.json")
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1108_STAGE123_ADMISSION "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    main()
