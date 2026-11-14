#!/usr/bin/env python3
"""Assess sealed CodeAI + actual Lean MCP + pinned direct-Lean precommit evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime.kuuos_codeai_lean_mcp_precommit_gate_v0_1 import (
    STATUS_READY, evaluate,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--codeai-record", required=True, type=Path)
    p.add_argument("--mcp-precommit-record", required=True, type=Path)
    p.add_argument("--source", required=True, type=Path)
    p.add_argument("--candidate", required=True, type=Path)
    p.add_argument("--direct-lean-log", required=True, type=Path)
    p.add_argument("--target", required=True)
    p.add_argument("--source-head", required=True)
    p.add_argument("--source-git-tree", required=True)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    if args.out.exists():
        raise SystemExit("append-only: gate receipt path already exists")
    observed = evaluate(
        codeai_record=json.loads(args.codeai_record.read_text(encoding="utf-8")),
        mcp_precommit_record=json.loads(args.mcp_precommit_record.read_text(encoding="utf-8")),
        source=args.source.read_bytes(), candidate=args.candidate.read_bytes(),
        target=args.target, source_head=args.source_head,
        source_git_tree=args.source_git_tree,
        direct_lean_log=args.direct_lean_log.read_text(encoding="utf-8"),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(observed.receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KUUOS_CODEAI_LEAN_MCP_PRECOMMIT_GATE " + json.dumps({
        "status": observed.status, "issues": observed.issues,
        "receipt_digest": observed.receipt["codeai_lean_mcp_precommit_gate_receipt_digest"],
        "source_head": observed.receipt["source_head"],
        "candidate_git_blob": observed.receipt["candidate_git_blob"],
        "independent_ci_certified": False,
    }, sort_keys=True, ensure_ascii=False))
    return 0 if observed.status == STATUS_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
