#!/usr/bin/env python3
"""Read-only exact-source research preflight for CodeAI; no Lean execution."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import scan, assess

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--head", required=True, help="Fresh canonical SHA obtained via GitHub MCP")
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--term", action="append", default=[])
    p.add_argument("--receipt", type=Path)
    p.add_argument("--review", type=Path)
    args = p.parse_args()
    if args.review:
        if args.receipt is None or args.term:
            p.error("--review requires --receipt and no --term")
        receipt = json.loads(args.receipt.read_text())
        review = json.loads(args.review.read_text())
        result = assess(args.root, args.head, receipt, review)
    else:
        result = scan(args.root, args.head, args.term)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if args.review:
        return 0 if result["candidate_generation_hint"] or result["status"] == "REUSE_EXISTING" else 2
    return 0 if result["status"] == "REVIEW_REQUIRED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
