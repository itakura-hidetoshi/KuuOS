#!/usr/bin/env python3
"""KuuOS CodeAI Lean MemoryOS sidecar: read hints before generation, ingest after Lean.

This is non-authoritative; it does not create candidates, run Lean, promote
a Git ref, assert theorem truth, or independently certify an Actions run.
"""
from __future__ import annotations
import argparse
import importlib
import json
import os
from pathlib import Path
import urllib.request

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import (
    append_cases, cases_from_portfolio, query_cases, route_candidates,
)
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

def github_run_observation(run_id: int, head: str) -> dict:
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("MemoryOS requires GitHub run read capability")
    request=urllib.request.Request(
        f"https://api.github.com/repos/itakura-hidetoshi/KuuOS/actions/runs/{run_id}",
        headers={"Accept":"application/vnd.github+json",
                 "Authorization":"Bearer "+token,
                 "User-Agent":"KuuOS-CodeAI-MemoryOS-v1"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data=json.load(response)
    if (data.get("id") != run_id or data.get("head_sha") != head
        or data.get("status") != "completed"
        or data.get("conclusion") != "success"):
        raise ValueError("MemoryOS producer run not completed at exact source HEAD")
    return {"producer_run": run_id, "status": data["status"],
            "conclusion": data["conclusion"], "head_sha": head,
            "proof_authority": False}

def find_one(root: str, filename: str) -> Path:
    matches=list(Path(root).rglob(filename))
    if len(matches)!=1:
        raise ValueError(f"MemoryOS expected one {filename}, found {len(matches)}")
    return matches[0]

def preflight(args: argparse.Namespace) -> dict:
    if not args.source_head or not args.source_tree or not args.imported_blob:
        raise ValueError("MemoryOS preflight needs pinned source/tree/import blob")
    module=importlib.import_module(args.candidates_module)
    generator=getattr(module,"candidates",None)
    if not callable(generator):
        raise ValueError("MemoryOS CodeAI candidate provider missing")
    candidates=generator()
    if not isinstance(candidates, dict) or not candidates:
        raise ValueError("MemoryOS no generated candidate portfolio")
    cases=read_observation_seed(args.seed)
    filtered,hints=route_candidates(candidates,cases,source_head=args.source_head,
        source_tree=args.source_tree, imported_blob=args.imported_blob)
    receipt={
        "status":"READ_ONLY_MEMORYOS_CANDIDATE_FEEDBACK",
        "repository":"itakura-hidetoshi/KuuOS",
        "source_head":args.source_head,"source_tree":args.source_tree,
        "imported_blob":args.imported_blob,
        "seed_cases":len(cases),
        "candidate_count_before":len(candidates),
        "candidate_count_after":len(filtered),
        "candidate_names_kept":list(filtered),
        "memory_feedback":hints,
        "memory_is_proof_authority":False,
        "gives_git_effect_authority":False,
    }
    return receipt

def ingest(args: argparse.Namespace) -> dict:
    portfolio=json.loads(find_one(args.evidence_dir,"portfolio.json").read_text())
    mcp=json.loads(find_one(args.evidence_dir,"receipt.json").read_text())
    if args.producer_run <= 0:
        raise ValueError("MemoryOS producer run id required")
    observation=github_run_observation(args.producer_run,portfolio.get("source_head"))
    cases=cases_from_portfolio(portfolio,mcp,args.producer_run)
    status=append_cases(args.journal,cases)
    return {"status":"MEMORYOS_APPEND_ONLY_OBSERVATIONS_RECORDED",
            "github_observation":observation,
            "case_count":len(cases),"journal":status,
            "codeai_generates_from_hints_not_proof":True,
            "independent_CI_certified":False}

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("mode", choices=["preflight","ingest"])
    parser.add_argument("--seed",default="memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v1.json")
    parser.add_argument("--source-head",default="")
    parser.add_argument("--source-tree",default="")
    parser.add_argument("--imported-blob",default="")
    parser.add_argument("--candidates-module",default="scripts.kuuos_v1106_codeai_label_table_round3_v1")
    parser.add_argument("--evidence-dir",default="")
    parser.add_argument("--producer-run",type=int,default=0)
    parser.add_argument("--journal",default="/tmp/kuuos-codeai-memoryos/observations.jsonl")
    parser.add_argument("--output",default="/tmp/kuuos-codeai-memoryos/result.json")
    args=parser.parse_args()
    result=preflight(args) if args.mode=="preflight" else ingest(args)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("KUUOS_CODEAI_MEMORYOS_RECEIPT "+json.dumps(result,sort_keys=True,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
