#!/usr/bin/env python3
"""v1.112 CodeAI round2: expose finite-index cases for 2/3 dimensions.

Round1 had direct Lean omega failures after Fin.ext at 2D and 3D indices;
these do NOT imply false theorem. Experiment with exact Fin enumeration and
simp_all before any actual source promotion. MemoryOS is an evidence pointer.
"""
from __future__ import annotations
import json
from pathlib import Path

from scripts import kuuos_v1112_codeai_typeA_all_dimensions_v1 as prior
from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts import kuuos_v1103_codeai_structural_candidates_v1 as v103
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

OUT=Path("/tmp/kuuos-v1112-codeai-round2")
MCP=Path("/tmp/kuuos-v1112-real-mcp-round2")
REPORT=Path("/tmp/kuuos-v1112-memoryos-round2/context.json")

TWO="""    have hIdx : i = (1 : Fin 3) := by
      apply Fin.ext
      omega"""
THREE="""    have hIdx : i = (1 : Fin 4) ∨ i = (2 : Fin 4) := by
      by_cases hOne : i.val = 1
      · left
        apply Fin.ext
        exact hOne
      · right
        apply Fin.ext
        omega"""
TWO_FIN="""    have hIdx : i = (1 : Fin 3) := by
      fin_cases i <;> simp_all"""
THREE_FIN="""    have hIdx : i = (1 : Fin 4) ∨ i = (2 : Fin 4) := by
      fin_cases i <;> simp_all"""
TWO_BOUNDS="""    have hIdx : i = (1 : Fin 3) := by
      have hsmall : i.val < 2 := by simpa using (Fin.lt_def).mp hiN
      have hpos : 0 < i.val := by simpa using (Fin.lt_def).mp hi0
      apply Fin.ext
      omega"""
THREE_BOUNDS="""    have hIdx : i = (1 : Fin 4) ∨ i = (2 : Fin 4) := by
      have hsmall : i.val < 3 := by simpa using (Fin.lt_def).mp hiN
      have hpos : 0 < i.val := by simpa using (Fin.lt_def).mp hi0
      by_cases hOne : i.val = 1
      · left
        apply Fin.ext
        exact hOne
      · right
        apply Fin.ext
        omega"""

def candidates() -> dict[str,str]:
    if prior.BODY.count(TWO)!=1 or prior.BODY.count(THREE)!=1:
        raise RuntimeError("v1.112 original finite-index proof source changed")
    primary=prior.BODY.replace(TWO,TWO_FIN).replace(THREE,THREE_FIN)
    typed=prior.BODY.replace(TWO,TWO_BOUNDS).replace(THREE,THREE_BOUNDS)
    # Proof/theorem declarations remain byte-identical across variants.
    versions={
      "round2-fin-cases-simp-all": prior.INTRO+primary+prior.AFTER,
      "round2-explicit-bounds": prior.INTRO+typed+prior.AFTER,
      "round2-fin-cases-nonempty": prior.INTRO+primary.replace(
          "    exact ⟨natTypeAFourCocycleCompletion i hi0 hiN f⟩",
          "    exact natTypeAFourCocycleCompletion_nonempty i hi0 hiN f"
        )+prior.AFTER,
      "round2-fin-cases-low-simpa": prior.INTRO+primary.replace(
          "    exact natTypeATwo_zero_cocycle_completion f",
          "    simpa [natTypeATwoIndex] using (natTypeATwo_zero_cocycle_completion f)"
        )+prior.AFTER,
    }
    head,branch,tree=prior.require_current_event()
    memory=read_observation_directory(prior.MEMORY)
    filtered,history=route_candidates(versions,memory,
                         source_head=head,source_tree=tree,
                         imported_blob=prior.PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("all source-bound candidate patterns previously failed; NO_DATA")
    history["diagnostics_are_observations"]=True
    history["causes_are_unverified"]=True
    history["independent_proof_authority"]=False
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(history,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1112_ROUND2_MEMORYOS "+json.dumps({
        "case_count":len(memory),"candidates":list(filtered),
        "quarantined":history.get("quarantined"),
        "hints":history.get("analogical_hints"),
        "authority":False},sort_keys=True))
    return filtered

def main() -> int:
    v103.require_event=prior.require_current_event
    harness.base.require_event=prior.require_current_event
    harness.V105=prior.PRIOR
    harness.V105_BLOB=prior.PRIOR_BLOB
    harness.base.TARGET=prior.TARGET
    harness.base.MODULE=prior.MODULE
    harness.base.PREDECESSOR=prior.PRIOR
    harness.base.ORIGINAL_V103_BLOB=prior.PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
