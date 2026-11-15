#!/usr/bin/env python3
"""MemoryOS-driven CodeAI v1.106 round4: do not replay source-bound Lean failures.

Retrieves curated GitHub pointer observations before generating new candidates.
Only exact same source HEAD+tree+imported blob+candidate Git blob is quarantined;
analogs are hints to generate different, explicit Fin-order proof candidates.
The pinned Lean -> green only MCP -> independent CI sequence is unchanged.
"""
from __future__ import annotations
import json
from pathlib import Path

from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from scripts import kuuos_v1106_codeai_label_table_v1 as initial
from scripts import kuuos_v1106_codeai_label_table_round3_v1 as third

SEED=Path("memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v1.json")
OUT=Path("/tmp/kuuos-v1106-codeai-memoryos-round4")
MCP=Path("/tmp/kuuos-v1106-real-mcp-memoryos-round4")
REPORT=Path("/tmp/kuuos-v1106-memoryos-preflight/context.json")

def candidates() -> dict[str,str]:
    before=third.candidates()["round3-fin-lt-def-simp"]
    anchor=(
        "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
        "    simp_all [Fin.lt_def, natFourStrictLabel, natFourHornLabels]"
    )
    if before.count(anchor)!=1:
        raise ValueError("CodeAI source-bound finite-order proof unexpectedly changed")
    proposals={
        "round4-memoryos-natural-order-simp":
            "  have hab_nat : a.val < b.val := hab\n"
            "  have hbc_nat : b.val < c.val := hbc\n"
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    simp_all [natFourStrictLabel, natFourHornLabels] <;> omega",
        "round4-memoryos-natural-order-first":
            "  have hab_nat : a.val < b.val := hab\n"
            "  have hbc_nat : b.val < c.val := hbc\n"
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    first\n"
            "    | (simp_all [natFourStrictLabel, natFourHornLabels])\n"
            "    | omega",
        "round4-memoryos-natural-order-prune":
            "  have hab_nat : a.val < b.val := hab\n"
            "  have hbc_nat : b.val < c.val := hbc\n"
            "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
            "    first\n"
            "    | omega\n"
            "    | simp_all [natFourStrictLabel, natFourHornLabels]",
    }
    raw={name:before.replace(anchor,proof) for name,proof in proposals.items()}
    head,branch,tree=require_event()
    memory=read_observation_seed(SEED)
    filtered,route=route_candidates(raw,memory,source_head=head,
        source_tree=tree,imported_blob=initial.V105_BLOB)
    route["git_commit_authority"]=False
    route["theorem_statement_changed"]=False
    route["historical_failures_as_hints_only"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(route,indent=2,sort_keys=True)+"\n")
    print("KUUOS_MEMORYOS_CODEAI_PREFLIGHT "+json.dumps(
        {"case_count":len(memory),"retained":list(filtered),
         "quarantined":route["quarantined"],
         "hints":route["analogical_hints"],
         "grants_proof_authority":False},sort_keys=True))
    return filtered

def main() -> int:
    initial.candidates=candidates
    initial.base.OUT=OUT
    initial.base.MCP_OUT=MCP
    return initial.main()

if __name__=="__main__":
    raise SystemExit(main())
