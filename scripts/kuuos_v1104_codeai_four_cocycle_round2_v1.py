#!/usr/bin/env python3
"""v1.104 CodeAI second-round structural corrections, on isolated fixed Lean.

Corrects namespace resolution for the *new* strict label function, not any
pre-existing definition. Increases deterministic elaboration budget only.
All underlying source statements remain identical to the v1 portfolio.
"""
from __future__ import annotations

from pathlib import Path
from scripts import kuuos_v1104_codeai_four_cocycle_v1 as base

ORIGINAL_GENERATOR = base.source
OUT = Path("/tmp/kuuos-v1104-codeai-round2")
MCP = Path("/tmp/kuuos-v1104-round2-real-mcp")

def source_round2(tactic: str) -> str:
    result=ORIGINAL_GENERATOR(tactic)
    changes=[
        ("def NatFourSimplexTriangleLabels.strictLabel",
         "def natFourStrictLabel"),
        ("L.strictLabel a b c",
         "natFourStrictLabel L a b c"),
        ("NatFourSimplexTriangleLabels.strictLabel",
         "natFourStrictLabel"),
    ]
    for old,new in changes:
        count=result.count(old)
        if count < 1:
            raise RuntimeError(f"CodeAI round2 generator source drift: {old!r}: {count}")
        result=result.replace(old,new)
    anchor=(
        "open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100\n\n"
    )
    if result.count(anchor)!=1:
        raise RuntimeError("CodeAI round2 source namespace insertion ambiguous")
    result=result.replace(anchor,anchor+"set_option maxHeartbeats 2000000\n\n",1)
    return result

def main() -> int:
    base.source=source_round2
    base.OUT=OUT
    base.MCP_OUT=MCP
    return base.main()

if __name__ == "__main__":
    raise SystemExit(main())
