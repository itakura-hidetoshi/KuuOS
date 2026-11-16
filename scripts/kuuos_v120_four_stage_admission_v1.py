#!/usr/bin/env python3
"""v1.120 independent exact source admission: producer SUCCESS is not proof.

The producer's four CodeAI proof candidates are evidence. We admit only the
byte-identical selected Lean source with real Lean MCP zero diagnostics and a
second successful direct Lean. A separate GitHub Actions job builds and audits
the theorem; this script cannot claim independent Lean certification.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

REPO = "itakura-hidetoshi/KuuOS"
PR_NUMBER = 3560
BASE = "validation/kuuos-v118-forward-minimal-nonlifting-on-v112-20261116"
BASE_SHA = "9632826b459f07175cc607a78db11f2349fbfc1f"
BRANCH = "validation/kuuos-v120-induced-admission-recovery-20261116"
PRODUCER_RUN = 43793277322
PRODUCER_HEAD = "9c5eb74a3c1a4d7eeea19039aa04ad5a89ff7e58"
PRODUCER_TREE = "67edb29b3f78fe5088307d71edde6a038f8bbb6d"
PRODUCER_WORKFLOW = ".github/workflows/kuuos-v120-codeai-induced-scaling-round3-v1.yml"
PROOF_PATH = "formal/KUOS/DependentOriginationForwardEndpointInducedCompatibilityV1_120.lean"
BLOB = "597f4ff8c082965f28c675365ce1564b1ad5f01a"
SHA256 = "b2174e653f0059bad9e81963c1b46a903598336c9b28e9a590f18b5e02021ac1"
OLD_BLOB = "0c64c99920158fe7f9707002bd24208167a2de26"
PRED_PATH = "formal/KUOS/DependentOriginationForwardEndpointDirectRLPObstructionV1_118.lean"
PRED_BLOB = "69196f47f1a925b76c2e8d0519a463e8c4762e69"
V112_PATH = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112.lean"
V112_BLOB = "c9977fe0144e922da23eddde1d6eba2ec2f51e65"
MEMORY = "memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v120_round3_v1.json"
SELECTED = "round3-congrArg-transport"
EXPECTED = {
    "round3-congrArg-transport": (BLOB,"SUCCESS",0),
    "round3-eq-substitution": ("9d1910b5b9ec56936b7c82a794a221914c6ce695","SUCCESS",0),
    "round3-simpa-transport": ("e97d6d4a2d3f1dec251a1666471882b6c00399a4","FAILURE",1),
    "round3-eqndrec-transport": ("ca3512857f05b82ec45d93f37727afe4f93afebe","SUCCESS",0),
}
DEST = Path("/tmp/kuuos-v120-independent")

def require(ok: bool, what: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V120_INDEPENDENT_NO_AUTHORITY: "+what)

def blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def github(path: str) -> dict:
    token=os.environ.get("GITHUB_TOKEN")
    require(bool(token),"missing GitHub observation token")
    request=urllib.request.Request(
        "https://api.github.com/repos/"+REPO+"/"+path,
        headers={"Authorization":"Bearer "+token,
          "Accept":"application/vnd.github+json",
          "User-Agent":"KuuOS-v120-exact-source-independent"})
    with urllib.request.urlopen(request,timeout=45) as response:
        return json.load(response)

def load_one(root: Path, name: str) -> dict:
    paths=list(root.rglob(name))
    require(len(paths)==1,"unique exact artifact "+name)
    return json.loads(paths[0].read_text(encoding="utf-8"))

def read_pinned_blob(sha: str) -> bytes:
    data=github("git/blobs/"+sha)
    require(data.get("sha")==sha and data.get("encoding")=="base64",
            "immutable original source blob unavailable")
    raw=base64.b64decode(data["content"],validate=False)
    require(blob(raw)==sha,"immutable original Git blob mismatch")
    return raw

def theorem_signatures(source: str) -> list[str]:
    signatures=re.findall(r"(?ms)^theorem\s+.*?\s*:= by",source)
    require(len(signatures)==4, "exact four proof declarations")
    return signatures

def main() -> None:
    root=Path(os.environ["GITHUB_WORKSPACE"])
    evidence=Path(os.environ["EVIDENCE_DIR"])
    event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pr=event.get("pull_request") or {}
    head,base=pr.get("head") or {},pr.get("base") or {}
    promoted=os.environ["PROMOTED_HEAD"]
    require(event.get("repository",{}).get("full_name")==REPO
        and event.get("number")==PR_NUMBER and pr.get("draft") is True
        and head.get("ref")==BRANCH and base.get("ref")==BASE
        and base.get("sha")==BASE_SHA
        and head.get("sha")==promoted
        and re.fullmatch(r"[0-9a-f]{40}",promoted) is not None,
        "wrong PR/base/checkout/lease")
    actual=github("pulls/3560")
    require((actual.get("head") or {}).get("sha")==promoted
        and (actual.get("base") or {}).get("sha")==BASE_SHA
        and actual.get("draft") is True
        and actual.get("state")=="open"
        and actual.get("merged") is False,
        "PR HEAD/base/state drift while verifying source")
    producer=github("actions/runs/"+str(PRODUCER_RUN))
    require(producer.get("id")==PRODUCER_RUN
        and producer.get("head_sha")==PRODUCER_HEAD
        and producer.get("path")==PRODUCER_WORKFLOW
        and producer.get("status")=="completed"
        and producer.get("conclusion")=="success",
        "producer workflow not exact completed SUCCESS")
    producer_commit=github("git/commits/"+PRODUCER_HEAD)
    require(producer_commit.get("sha")==PRODUCER_HEAD
        and (producer_commit.get("tree") or {}).get("sha")==PRODUCER_TREE,
        "producer HEAD/tree mismatch")
    current=github("git/commits/"+promoted)
    tree=(current.get("tree") or {}).get("sha","")
    require(current.get("sha")==promoted
        and re.fullmatch(r"[0-9a-f]{40}",tree) is not None,
        "promoted HEAD/tree invalid")
    merge_ref=github("git/ref/pull/3560/merge")
    test_sha=(merge_ref.get("object") or {}).get("sha","")
    require(re.fullmatch(r"[0-9a-f]{40}",test_sha) is not None,
        "NO_DATA: test merge commit unavailable")
    test=github("git/commits/"+test_sha)
    require((test.get("tree") or {}).get("sha")==tree,
        "source/test-merge Git tree mismatch")
    portfolio=load_one(evidence,"portfolio.json")
    mcp=load_one(evidence,"receipt.json")
    require(portfolio.get("source_head")==PRODUCER_HEAD
        and portfolio.get("source_tree")==PRODUCER_TREE
        and portfolio.get("imported_v1103_blob")==PRED_BLOB
        and portfolio.get("candidate_count")==4
        and portfolio.get("source_restored") is True
        and portfolio.get("git_write_performed") is False
        and portfolio.get("independent_ci_certified") is False
        and portfolio.get("original_failed_blob")==OLD_BLOB,
        "source-bound CodeAI producer portfolio invalid")
    rows=portfolio.get("candidates")
    require(isinstance(rows,list) and len(rows)==4
        and {r.get("variant") for r in rows}==set(EXPECTED),
        "exact four candidate names missing")
    for row in rows:
        sha,status,error_count=EXPECTED[row["variant"]]
        require(row.get("candidate_blob")==sha
            and row.get("status")==status
            and row.get("error_count")==error_count
            and row.get("exit_code")== (0 if status=="SUCCESS" else 1)
            and row.get("olean_exists") is (status=="SUCCESS")
            and isinstance(row.get("errors"),list)
            and len(row["errors"])==error_count,
            "candidate result mismatch: "+row["variant"])
    fail=next(x for x in rows if x["variant"]=="round3-simpa-transport")
    require("Type mismatch" in fail["errors"][0],
            "missing exact simplifier failure observation")
    require(mcp.get("source_head")==PRODUCER_HEAD
        and mcp.get("candidate_count")==4
        and set(mcp.get("direct_lean_green",[]))==
            {"round3-congrArg-transport","round3-eq-substitution","round3-eqndrec-transport"}
        and mcp.get("selected")==SELECTED
        and mcp.get("selected_blob")==BLOB
        and mcp.get("status")=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI"
        and mcp.get("mcp_success") is True
        and mcp.get("mcp_errors")==0
        and mcp.get("second_direct_success") is True
        and mcp.get("second_direct_exit")==0
        and mcp.get("source_restored") is True
        and mcp.get("git_write_performed") is False
        and mcp.get("independent_ci_certified") is False,
        "selected direct Lean, actual MCP and second Lean receipts not all SUCCESS")
    candidates=list(evidence.rglob("candidate.lean"))
    require(len(candidates)==1, "selected candidate source artifact not unique")
    code=(root/PROOF_PATH).read_bytes()
    require(code==candidates[0].read_bytes() and blob(code)==BLOB
        and hashlib.sha256(code).hexdigest()==SHA256,
        "GitHub proof file not byte-identical with actual real MCP-selected proof")
    old=read_pinned_blob(OLD_BLOB)
    require(theorem_signatures(old.decode("utf-8"))==
            theorem_signatures(code.decode("utf-8")),
        "original four theorem statements/assumptions were weakened or changed")
    require(blob((root/PRED_PATH).read_bytes())==PRED_BLOB
        and blob((root/V112_PATH).read_bytes())==V112_BLOB,
        "imported certified proof blob drift")
    from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
    require(not forbidden_code_constructs(code.decode("utf-8")),
            "new axiom, sorry or other forbidden proof construct")
    from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed
    from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory
    recorded=read_observation_seed(root/MEMORY)
    all_cases=read_observation_directory(root/"memoryos/external/github/2026/11")
    require(len(recorded)==4 and len(all_cases)>=61
            and len({x["id"] for x in all_cases})==len(all_cases),
            "four append-only MemoryOS observations not validated")
    for case in recorded:
        status=EXPECTED[case["variant"]][1]
        require(case["source_head"]==PRODUCER_HEAD
            and case["source_tree"]==PRODUCER_TREE
            and case["imported_blob"]==PRED_BLOB
            and case["producer_run"]==PRODUCER_RUN
            and case["candidate_blob"]==EXPECTED[case["variant"]][0]
            and case["outcome"]==("DIRECT_LEAN_SUCCESS" if status=="SUCCESS"
                else "DIRECT_LEAN_FAILURE")
            and case["causal_status"]=="UNVERIFIED_HYPOTHESIS"
            and case["independent_run"] is None,
            "MemoryOS pointer cannot certify experimental source")
    require((root/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2",
        "Lean pin changed")
    manifest=json.loads((root/"lake-manifest.json").read_text())
    require([p.get("rev") for p in manifest["packages"] if p.get("name")=="mathlib"]==
        ["5450b53e5ddc75d46418fabb605edbf36bd0beb6"],
        "mathlib pin changed")
    DEST.mkdir(parents=True,exist_ok=True)
    receipt={
        "stage":"CODEAI_DIRECT_AND_REAL_MCP_ADMITTED_ONLY",
        "producer_run":PRODUCER_RUN,"producer_head":PRODUCER_HEAD,
        "producer_tree":PRODUCER_TREE,"promoted_head":promoted,
        "promoted_tree":tree,"test_merge_tree":test["tree"]["sha"],
        "selected_blob":BLOB,"selected_sha256":SHA256,
        "memory_cases":len(recorded),"direct_green":3,
        "real_mcp_success":True,"second_direct_success":True,
        "independent_ci_certified":False,"merge_authority":False,
        "scope":"induced source-admission and comparison-one non-factorization; not endpoint RLP"}
    (DEST/"admission.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V120_STAGE123_ADMISSION",json.dumps(receipt,sort_keys=True))

if __name__=="__main__":
    main()
