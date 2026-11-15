#!/usr/bin/env python3
"""v1.106 CodeAI second round: typed Fin 5 order witnesses, finite contradictions.

The previous three direct-Lean candidates were all red. This repairs the 20
dependent decide elaboration failures and tries bounded case/omega proofs.
No source promotion before direct Lean, real MCP and independent strict CI.
"""
from __future__ import annotations
from pathlib import Path
import re
from scripts import kuuos_v1106_codeai_label_table_v1 as prior

ORIGINAL = prior.candidates
PROOF_BEFORE = (
    "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
    "    simp_all [natFourStrictLabel, natFourHornLabels]"
)

def typed_fields(text: str) -> str:
    marker=re.compile(r"f (\d) (\d) (\d) \(by decide\) \(by decide\)\n")
    def write(m):
        a,b,c=m.groups()
        return (
            f"f ({a} : Fin 5) ({b} : Fin 5) ({c} : Fin 5)\n"
            f"    (show ({a} : Fin 5) ≤ ({b} : Fin 5) from by decide)\n"
            f"    (show ({b} : Fin 5) ≤ ({c} : Fin 5) from by decide)\n"
        )
    result,n=marker.subn(write,text)
    if n!=10:
        raise RuntimeError("v1.106 10 exact strict triple order witnesses drift: "+str(n))
    return result

def candidates() -> dict[str,str]:
    original=ORIGINAL()["round1-table-simp"]
    typed=typed_fields(original)
    if typed.count(PROOF_BEFORE)!=1:
        raise RuntimeError("v1.106 original theorem proof span drift")
    variants={
        "round2-fin5-omega-rfl":
           "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
           "    first\n"
           "    | (exfalso; omega)\n"
           "    | rfl",
        "round2-fin5-omega-simp":
           "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
           "    first\n"
           "    | (exfalso; omega)\n"
           "    | simp [natFourStrictLabel, natFourHornLabels]",
        "round2-fin5-simp-omega":
           "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
           "    simp_all [natFourStrictLabel, natFourHornLabels] <;>\n"
           "    all_goals omega",
    }
    return {name:typed.replace(PROOF_BEFORE,proof) for name,proof in variants.items()}

def main() -> int:
    prior.candidates=candidates
    prior.base.OUT=Path("/tmp/kuuos-v1106-codeai-round2")
    prior.base.MCP_OUT=Path("/tmp/kuuos-v1106-real-mcp-round2")
    return prior.main()

if __name__=="__main__":
    raise SystemExit(main())
