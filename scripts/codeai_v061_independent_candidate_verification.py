#!/usr/bin/env python3
"""KuuOS CodeAI v0.61: exact-source independent fixed-Lean candidate verifier.

The inputs are three MODEL-SUPPLIED candidate complete-file texts already
processed by the actual KuuOS CodeAI Candidate Patch governance. None of them
is allowed to overwrite main or claim Git authority. A/B must independently
pass strict Lean with all eight direct #print axioms. C is kept as a NEGATIVE
observation, with its exact independent Lean diagnostics; it is NOT silently
repaired, dropped, treated as a typed preflight finding, or used as memory.

This script is the post-CodeAI independent formal verifier, not CodeAI's
proposal authority. Its result is evidence for a later distinct memory job.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

from scripts import codeai_v061_two_stage_proof_proposal as prior
from scripts import codeai_v061_multi_candidate_portfolio as portfolio
from scripts.kuuos_sandbox_lean_cycle_v1 import source_contract
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments, FORBIDDEN_NEW

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"artifacts/codeai-v061-independent-verification"
OUTPUT_FILE=EVIDENCE/"verified-candidates.json"
NS="KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61."
EXPECTED_SHA256={
    "model-a":"2a33b3acccf3d18aa4caedb15b95e546e2bd6bb8d25f601175f44abd507c9642",
    "model-b":"c33f470532d9757226f4e05bf3c0182beff8cf52c3c658bc1ec8aa346126643a",
    "model-c":"2d2a7ab6a42c6e73d6644b4eaa8facd8406d14bb8a6495d8fed3bf33350761de",
}
AXIOMS={"propext","Classical.choice","Quot.sound"}
PATTERN=re.compile(
    r"'"+re.escape(NS)+r"([A-Za-z0-9_]+)' (?:"
    r"does not depend on any axioms|depends on axioms: \[([^\]]*)\])",
    re.MULTILINE,
)
DIAG=re.compile(r"(?m)^.*?\.lean:\d+:\d+: error: (.*)$")


def require_proof_governance():
    originals=prior._read_pinned_snapshot()
    assert prior.CANDIDATE_PATH not in originals
    assert not (ROOT/prior.CANDIDATE_PATH).exists(), "no formal adoption before independent verification"
    sources={label:(ROOT/file).read_text(encoding="utf-8")
             for label,file in portfolio.INPUTS}
    for label,source in sources.items():
        assert hashlib.sha256(source.encode()).hexdigest()==EXPECTED_SHA256[label],label
        assert source.count("#print axioms ")==len(prior.AXIOM_NAMES)
        for name in prior.AXIOM_NAMES:
            assert "#print axioms "+NS+name in source
        assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)),label
        source_contract(sources["model-a"],source,{}, {})
    return sources


def compile_one(label: str, content: str, dest: Path) -> dict:
    dest.mkdir(parents=True,exist_ok=True)
    file=dest/"ProposedV061.lean"
    file.write_text(content,encoding="utf-8")
    olean=dest/"candidate.olean"
    cmd=["lake","env","lean","-DwarningAsError=true",
         "-Dweak.sorryAsError=true","-o",str(olean),str(file)]
    try:
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,
                         timeout=270,check=False)
        timed_out=False
    except subprocess.TimeoutExpired as ex:
        raise RuntimeError("NO_DATA_Lean_timeout:"+label) from ex
    log=p.stdout+"\n"+p.stderr
    (dest/"lean.log").write_text(log,encoding="utf-8")
    diagnostics=[x.strip() for x in DIAG.findall(log)]
    if "sorryAx" in log:
        raise AssertionError("forbidden_sorryAx:"+label)
    if label=="model-c":
        # This FAILED candidate stays in the historical log; it is not
        # supposed to pass and is never counted as a validated proof.
        expected="try 'simp' instead of 'simpa'"
        if p.returncode==0 or olean.is_file():
            raise AssertionError("expected_failure_disappeared_in_candidate_c")
        if len(diagnostics)!=2 or any(expected not in x for x in diagnostics):
            raise AssertionError(
                "unexpected_C_diagnostics:"+repr(diagnostics))
        return {
            "label":label,"status":"DIRECT_LEAN_REJECTED_TYPED_LINT_PENDING",
            "strict_lean_exit_code":p.returncode,"error_count":len(diagnostics),
            "diagnostics":diagnostics,
            "diagnostic_digest":hashlib.sha256(log.encode()).hexdigest(),
            "source_sha256":EXPECTED_SHA256[label],
            "proven_lean_declarations":0,
            "independent_repair_evidence_admitted":False,
            "reusable_repair_memory_admitted":False,
            "original_source_unchanged":True,
        }
    if p.returncode!=0 or diagnostics or not olean.is_file():
        raise AssertionError(
            "unexpected_Lean_failure:"+label+":"+str(p.returncode)+":"+repr(diagnostics))
    reports=PATTERN.findall(log)
    if len(reports)!=len(prior.AXIOM_NAMES):
        raise AssertionError("NO_DATA_axiom_inventory:"+label+":"+repr(reports))
    names=[name for name,_ in reports]
    if len(names)!=len(set(names)) or set(names)!=set(prior.AXIOM_NAMES):
        raise AssertionError("source_declaration_mismatch:"+label)
    used={axiom.strip()
          for _,raw in reports
          for axiom in raw.split(",") if axiom.strip()}
    if used-AXIOMS:
        raise AssertionError("UNAUTHORIZED_axiom:"+repr(used-AXIOMS))
    if re.search(r"(?m)^.*\bwarning:",log):
        raise AssertionError("strict_Lean_warning:"+label)
    return {
        "label":label,"status":"INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED",
        "source_sha256":EXPECTED_SHA256[label],
        "strict_lean_exit_code":0,
        "error_count":0,"axiom_declarations_checked":len(names),
        "axioms_used":sorted(used),
        "sorryAx":False,"log_sha256":hashlib.sha256(log.encode()).hexdigest(),
        "independent_repair_evidence_admitted":False,
        "reusable_repair_memory_admitted":False,
        "original_source_unchanged":True,
    }


def main() -> int:
    sources=require_proof_governance()
    source_portfolio=portfolio.run_portfolio()
    assert source_portfolio["candidate_count"]==3
    assert source_portfolio["attempts"]==["CANDIDATE"]*3+["REJECT"]
    # The exact CodeAI source-bound bytes and the baseline version pin are
    # rechecked before and after every independent direct Lean elaboration.
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    rows=[]
    for label in ("model-a","model-b","model-c"):
        rows.append(compile_one(label,sources[label],EVIDENCE/label))
        assert prior._read_pinned_snapshot()
        assert not (ROOT/prior.CANDIDATE_PATH).exists()
    assert [x["status"] for x in rows]==[
        "INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED",
        "INDEPENDENT_FIXED_LEAN_AND_AXIOM_PASSED",
        "DIRECT_LEAN_REJECTED_TYPED_LINT_PENDING",
    ]
    results={
        "schema":"kuuos.codeai.v061.independent-fixed-lean-evidence.v1",
        "repo":"itakura-hidetoshi/KuuOS",
        "canonical_parent_main":prior.MAIN_HEAD,
        "canonical_parent_tree_sha1":prior.MAIN_TREE,
        "toolchain":prior.TOOLCHAIN,
        "mathlib_commit":prior.MATHLIB,
        "source_candidate_portfolio":"model_supplied_proposals_governed_by_actual_codeai",
        "portfolio_digest":source_portfolio["codeai_synthesis_receipt_digest"],
        "attempts":source_portfolio["attempts"],
        "results":rows,
        "all_proposals_adopted":False,
        "candidate_selected":False,
        "github_write_performed_by_verifier":False,
        "actual_original_planos_executed":False,
        "external_repair_verifier_roles_verified":False,
        "typed_error_classification_c_admitted":False,
        "subtask_memory_update_performed":False,
        "holdout_learning_leak":False,
        "independent_global_ci_complete":False,
    }
    results["evidence_digest"]=hashlib.sha256(
        json.dumps(results,sort_keys=True,ensure_ascii=False,
                   separators=(",",":")).encode()).hexdigest()
    OUTPUT_FILE.write_text(json.dumps(results,ensure_ascii=False,
                                     sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("CODEAI_V061_INDEPENDENT_FIXED_LEAN_EVIDENCE",json.dumps({
        "source_commit_sha":prior.MAIN_HEAD,
        "candidate_statuses":[(x["label"],x["status"]) for x in rows],
        "candidate_ax_counts":[(x["label"],x.get("axiom_declarations_checked",0)) for x in rows],
        "evidence_digest":results["evidence_digest"],
        "independent_global_ci_complete":False,
        "memory_update_performed":False,
    },sort_keys=True))
    return 0


if __name__=="__main__":
    sys.exit(main())
