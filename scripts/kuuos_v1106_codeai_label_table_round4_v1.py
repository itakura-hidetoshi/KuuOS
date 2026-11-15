#!/usr/bin/env python3
"""v1.106 CodeAI round 4: reveal numeric order hypotheses before Fin case splits.

Round 3 evidence: Fin.lt_def inside simp was unused; order contradictions
remained opaque after fin_cases. This study preserves theorem statements and
uses explicit typed Fin.val order hypotheses before structural elimination.
"""
from __future__ import annotations
from pathlib import Path
from scripts import kuuos_v1106_codeai_label_table_round2_v1 as round2
from scripts import kuuos_v1106_codeai_label_table_v1 as harness

ORIGINAL = round2.candidates
PROOF_BEFORE = (
    "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
    "    first\n"
    "    | (exfalso; omega)\n"
    "    | simp [natFourStrictLabel, natFourHornLabels]"
)
CASES = ("  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n")

def candidates() -> dict[str, str]:
    source = ORIGINAL()["round2-fin5-omega-simp"]
    if source.count(PROOF_BEFORE) != 1:
        raise RuntimeError("v1.106 round2 proof span drift")
    variants = {
        "round4-typed-val-simp":
            "  have habv : a.val < b.val := (Fin.lt_def).mp hab\n"
            "  have hbcv : b.val < c.val := (Fin.lt_def).mp hbc\n"
            CASES +
            "    simp_all [natFourStrictLabel, natFourHornLabels]",
        "round4-typed-val-omega":
            "  have habv : a.val < b.val := (Fin.lt_def).mp hab\n"
            "  have hbcv : b.val < c.val := (Fin.lt_def).mp hbc\n"
            CASES +
            "    simp_all [natFourStrictLabel, natFourHornLabels] <;>\n"
            "    omega",
        "round4-change-val-order":
            "  change a.val < b.val at hab\n"
            "  change b.val < c.val at hbc\n"
            CASES +
            "    simp_all [natFourStrictLabel, natFourHornLabels]",
        "round4-dsimp-orders":
            CASES +
            "    dsimp at hab hbc <;>\n"
            "    simp_all [natFourStrictLabel, natFourHornLabels]",
        "round4-norm-num-orders":
            CASES +
            "    norm_num at hab hbc <;>\n"
            "    simp_all [natFourStrictLabel, natFourHornLabels]",
    }
    return {name: source.replace(PROOF_BEFORE, proof) for name, proof in variants.items()}

def main() -> int:
    harness.candidates = candidates
    harness.base.OUT = Path("/tmp/kuuos-v1106-codeai-round4")
    harness.base.MCP_OUT = Path("/tmp/kuuos-v1106-real-mcp-round4")
    return harness.main()

if __name__ == "__main__":
    raise SystemExit(main())
