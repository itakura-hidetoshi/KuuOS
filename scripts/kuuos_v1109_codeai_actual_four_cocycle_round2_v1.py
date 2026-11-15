#!/usr/bin/env python3
"""v1.109 round2: MemoryOS-routed actual four-horn cocycle namespace repair.

Round1 observed unknown duskinComparison and an rcases-related rfl failure.
The proposed missing-open/qualified-identifier fixes are NOT causal facts:
verify each under pinned direct Lean, then real Lean MCP only for green.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import kuuos_v1109_codeai_actual_four_cocycle_v1 as prior
from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

PRIOR_BLOB=prior.PRIOR_BLOB
OUT=Path("/tmp/kuuos-v1109-codeai-round2")
MCP=Path("/tmp/kuuos-v1109-real-mcp-round2")
REPORT=Path("/tmp/kuuos-v1109-memoryos-round2/context.json")
MEMORY=prior.MEMORY
ORIGINAL_OPEN="open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95\n"
NEEDED_OPEN="open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21\n"
FULL_NAME="KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21.duskinComparison"

def candidates() -> dict[str,str]:
    if prior.INTRO.count(ORIGINAL_OPEN)!=1:
        raise RuntimeError("v1.109 original open statements changed")
    opened=prior.INTRO.replace(ORIGINAL_OPEN,ORIGINAL_OPEN+NEEDED_OPEN)
    if prior.AFTER.count("    duskinComparison\n")!=1:
        raise RuntimeError("v1.109 exact Yoneda comparison binding changed")
    qualified=prior.AFTER.replace(
      "    duskinComparison\n", "    "+FULL_NAME+"\n", 1)
    rcases_after=prior.AFTER.replace(
      "      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by\n  rfl\n",
      "      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by\n"
      "  simp [natTypeAFourHornCocycle, natFourCocycleOfLabels]\n",1)
    proposals={
       "round2-open-projection":opened+prior.HEADER+
         prior.VARIANTS["round1-projection-typed"]+prior.AFTER,
       "round2-open-let":opened+prior.HEADER+
         prior.VARIANTS["round1-let-five"]+prior.AFTER,
       "round2-qualified-projection":prior.INTRO+prior.HEADER+
         prior.VARIANTS["round1-projection-typed"]+qualified,
       "round2-qualified-let":prior.INTRO+prior.HEADER+
         prior.VARIANTS["round1-let-five"]+qualified,
       "round2-open-rcases-simp":opened+prior.HEADER+
         prior.VARIANTS["round1-rcases-five"]+rcases_after,
    }
    head,branch,tree=require_event()
    recorded=read_observation_directory(MEMORY)
    filtered,history=route_candidates(proposals,recorded,
                 source_head=head,source_tree=tree,imported_blob=PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("v1.109 all exact candidates blocked; retain NO_DATA")
    history["cause_status"]="UNVERIFIED_HYPOTHESIS"
    history["memory_grants_no_proof_authority"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(history,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1109_MEMORYOS_ROUND2_PREFLIGHT "+json.dumps({
       "case_count":len(recorded),"retained":list(filtered),
       "quarantined":history.get("quarantined"),
       "hints":history.get("analogical_hints"),
       "grants_proof_authority":False},sort_keys=True))
    return filtered

def main() -> int:
    harness.V105=prior.PRIOR
    harness.V105_BLOB=PRIOR_BLOB
    harness.base.TARGET=prior.TARGET
    harness.base.MODULE=prior.MODULE
    harness.base.PREDECESSOR=prior.PRIOR
    harness.base.ORIGINAL_V103_BLOB=PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
