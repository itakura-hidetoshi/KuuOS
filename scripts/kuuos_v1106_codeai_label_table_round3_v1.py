#!/usr/bin/env python3
"""v1.106 CodeAI round 3: close impossible Fin 5 strict-order cases.

The second round leaves only contradictory, non-increasing vertex triples.
Compare alternative exact-order reduction tactics. The theorem, label table,
source import and hypotheses remain unchanged. Do not promote red candidates.
"""
from __future__ import annotations

from pathlib import Path
from scripts import kuuos_v1106_codeai_label_table_round2_v1 as prior

ORIGINAL = prior.candidates
PROOF_BEFORE = (
    "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
    "    first\n"
    "    | (exfalso; omega)\n"
    "    | simp [natFourStrictLabel, natFourHornLabels]"
)

def candidates() -> dict[str, str]:
    typed = ORIGINAL()["round2-fin5-omega-simp"]
    if typed.count(PROOF_BEFORE) != 1:
        raise RuntimeError("round2 certified source generator/proof span drift")
    variants = {
        "round3-fin-lt-def-simp":
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [Fin.lt_def, natFourStrictLabel, natFourHornLabels]",
        "round3-fin-lt-def-omega":
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [Fin.lt_def, natFourStrictLabel, natFourHornLabels] <;>\n"
            "    all_goals omega",
        "round3-fin-lt-def-norm-num":
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [Fin.lt_def, natFourStrictLabel, natFourHornLabels] <;>\n"
            "    all_goals norm_num at hab hbc",
        "round3-fin-lt-after-table":
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [natFourStrictLabel, natFourHornLabels] <;>\n"
            "    all_goals simp_all [Fin.lt_def]",
        "round3-fin-order-first":
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [Fin.lt_def] <;>\n"
            "    all_goals simp [natFourStrictLabel, natFourHornLabels]",
    }
    return {name: typed.replace(PROOF_BEFORE, proof) for name, proof in variants.items()}

def main() -> int:
    # Call the original fixed Lean/real MCP harness, not the round-2 wrapper.
    prior.prior.candidates = candidates
    prior.prior.base.OUT = Path("/tmp/kuuos-v1106-codeai-round3")
    prior.prior.base.MCP_OUT = Path("/tmp/kuuos-v1106-real-mcp-round3")
    return prior.prior.main()

if __name__ == "__main__":
    raise SystemExit(main())
