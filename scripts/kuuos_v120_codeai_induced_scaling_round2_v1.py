#!/usr/bin/env python3
"""CodeAI v1.120 round2: source-bound finite repair portfolio (non-certifying).
Generate multiple candidates; pinned direct Lean for all; real Lean MCP only
for direct-green; second direct Lean; restore original exact source always.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request

from scripts import kuuos_v1104_codeai_four_cocycle_v1 as harness
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates

ROOT=Path(__file__).resolve().parent.parent
REPO="itakura-hidetoshi/KuuOS"
BRANCH="research/kuuos-v120-induced-scaling-compatibility-20261116"
BASE="validation/kuuos-v118-forward-minimal-nonlifting-on-v112-20261116"
BASE_SHA="9632826b459f07175cc607a78db11f2349fbfc1f"
TARGET="formal/KUOS/DependentOriginationForwardEndpointInducedCompatibilityV1_120.lean"
ORIGINAL="0c64c99920158fe7f9707002bd24208167a2de26"
PRIOR="formal/KUOS/DependentOriginationForwardEndpointDirectRLPObstructionV1_118.lean"
PRIOR_BLOB="69196f47f1a925b76c2e8d0519a463e8c4762e69"
OUT=Path("/tmp/kuuos-v120-codeai-round2")
MCP=Path("/tmp/kuuos-v120-real-mcp-round2")
MEMORY=ROOT/"memoryos/external/github/2026/11"
ANCHOR="open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\n"
EXPR="    apply ScaledSSet.ScaledMap.ext\n    simp [minimalToInducedHornCylinderAttachment]"

def blob(b: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def check(ok: bool, what: str) -> None:
    if not ok: raise RuntimeError("KUUOS_V120_FAIL_CLOSED: "+what)

def current_event():
    e=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pr=e.get("pull_request") or {}
    h=pr.get("head") or {}
    b=pr.get("base") or {}
    check(e.get("repository",{}).get("full_name")==REPO
          and e.get("number")==3559 and pr.get("draft") is True
          and h.get("ref")==BRANCH and b.get("ref")==BASE
          and b.get("sha")==BASE_SHA,"wrong PR source/target/lease")
    sha=h.get("sha","")
    check(re.fullmatch(r"[0-9a-f]{40}",sha) is not None,"missing source HEAD")
    token=os.environ.get("GITHUB_TOKEN")
    check(bool(token),"GitHub proof-source observation token")
    def get(path):
        req=urllib.request.Request("https://api.github.com/repos/"+REPO+"/"+path,
            headers={"Accept":"application/vnd.github+json",
                     "Authorization":"Bearer "+token,
                     "User-Agent":"KuuOS-v120-CodeAI-round2"})
        with urllib.request.urlopen(req,timeout=45) as r: return json.load(r)
    actual=get("pulls/3559")
    check(actual["head"]["sha"]==sha and actual["base"]["sha"]==BASE_SHA
          and actual["draft"] is True,"concurrent source ref change")
    commit=get("git/commits/"+sha)
    tree=commit.get("tree",{}).get("sha","")
    check(commit.get("sha")==sha and re.fullmatch(r"[0-9a-f]{40}",tree),
          "unverified HEAD/tree")
    return sha,tree

def candidates(original: str):
    check(original.count(ANCHOR)==1 and original.count(EXPR)==1,
          "not exact original theorem proof")
    prefix=original.replace(ANCHOR,ANCHOR+
        "open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21\n"+
        "open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22\n",1)
    changed="    apply ScaledSSet.ScaledMap.ext\n"+(
        "    change (𝟙 (hornCylinderAttachment n i 0 : SSet.{u})) ≫ f.map = f.map\n")
    p={
        "round2-explicit-id-comp":prefix.replace(EXPR,changed+
            "    exact Category.id_comp f.map",1),
        "round2-explicit-id-simp":prefix.replace(EXPR,changed+
            "    simp only [Category.id_comp]",1),
        "round2-explicit-id-simp-general":prefix.replace(EXPR,changed+
            "    simp",1),
        "round2-namespace-only":prefix,
    }
    check(len({blob(x.encode()) for x in p.values()})==4,
          "non-distinct variants")
    for code in p.values():
        check(code.count("theorem ")==original.count("theorem ")
              and not forbidden_code_constructs(code),"forbidden proof change")
    return p

def run_direct(name: str, source: str):
    record={"variant":name,"candidate_blob":blob(source.encode()),
            "candidate_sha256":hashlib.sha256(source.encode()).hexdigest(),
            "status":"NO_DATA","errors":[]}
    try:
        (ROOT/TARGET).write_text(source,encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="v120-codeai-") as directory:
            olean=Path(directory)/"candidate.olean"
            try:
                proc=subprocess.run(["lake","env","lean",
                    "-DwarningAsError=true","-Dweak.sorryAsError=true",
                    "-o",str(olean),TARGET],cwd=ROOT,
                    capture_output=True,text=True,timeout=600)
                log=proc.stdout+"\n"+proc.stderr
                record["exit_code"]=proc.returncode
                record["olean_exists"]=olean.is_file()
                record["status"]="SUCCESS" if (proc.returncode==0 and
                    olean.is_file() and "sorryAx" not in log) else "FAILURE"
            except subprocess.TimeoutExpired as exc:
                log=str(exc.stdout or "")+"\n"+str(exc.stderr or "")
                record.update(status="TIMEOUT",exit_code=None,olean_exists=False)
            record["errors"]=[x[:700] for x in log.splitlines()
                    if "error:" in x or "error(" in x][:40]
            record["error_count"]=len(record["errors"])
            record["log_sha256"]=hashlib.sha256(log.encode()).hexdigest()
            (OUT/(name+".log")).write_text(log)
            if record["status"]=="SUCCESS" and record["error_count"]!=0:
                record["status"]="FAILURE"
    finally:
        # Source restored after each candidate, regardless of test result.
        (ROOT/TARGET).write_bytes(ORIGINAL_SOURCE)
    print("KUUOS_V120_DIRECT "+json.dumps(record,sort_keys=True))
    return record

ORIGINAL_SOURCE: bytes

def main():
    global ORIGINAL_SOURCE
    head,tree=current_event()
    require_pins(ROOT)
    target=ROOT/TARGET
    ORIGINAL_SOURCE=target.read_bytes()
    check(blob(ORIGINAL_SOURCE)==ORIGINAL,"original source blob altered")
    check(blob((ROOT/PRIOR).read_bytes())==PRIOR_BLOB,
          "certified dependency blob changed")
    memory=read_observation_directory(MEMORY)
    check(any(x["candidate_blob"]==ORIGINAL and x["producer_run"]==43781807526
              and x["outcome"]=="DIRECT_LEAN_FAILURE" for x in memory),
          "first failure must be retained")
    proposed,history=route_candidates(candidates(ORIGINAL_SOURCE.decode()),memory,
            source_head=head,source_tree=tree,imported_blob=PRIOR_BLOB)
    check(bool(proposed),"no admissible CodeAI candidates")
    OUT.mkdir(parents=True,exist_ok=False)
    (OUT/"memory_hints.json").write_text(json.dumps(history,sort_keys=True,indent=2)+"\n")
    results=[]
    try:
        for name,code in proposed.items():
            results.append(run_direct(name,code))
        harness.TARGET=TARGET
        harness.MCP_OUT=MCP
        result=harness.mcp_verify(head,results,proposed)
    finally:
        target.write_bytes(ORIGINAL_SOURCE)
        check(blob(target.read_bytes())==ORIGINAL,
              "original Git source not restored")
    result["source_restored"]=True
    MCP.mkdir(parents=True,exist_ok=True)
    (MCP/"receipt.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    receipt={"source_head":head,"source_tree":tree,
             "imported_v1103_blob":PRIOR_BLOB,
             "candidate_count":len(results),"candidates":results,
             "source_restored":True,"git_write_performed":False,
             "independent_ci_certified":False,
             "original_failed_blob":ORIGINAL}
    (OUT/"portfolio.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V120_REAL_MCP "+json.dumps(result,sort_keys=True))
    print("KUUOS_V120_SUMMARY "+json.dumps({
        "producer_head":head,"tested":len(results),
        "direct_green":sum(r["status"]=="SUCCESS" for r in results),
        "mcp_status":result["status"],"restored":True},sort_keys=True))
    return 0 if result["status"]=="LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__=="__main__":
    raise SystemExit(main())
