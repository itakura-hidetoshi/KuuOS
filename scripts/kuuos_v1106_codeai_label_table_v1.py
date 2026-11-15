#!/usr/bin/env python3
"""CodeAI v1.106 exact horn 10-label extraction: proposals, pinned Lean, MCP.

Predecessor v1.105 is required at its exact independently certified Git blob.
The generated Lean declares actual source labels, not a fabricated cocycle
condition or an unconditional four-horn filler. Never commits candidate code.
"""
from __future__ import annotations
from pathlib import Path
from scripts import kuuos_v1104_codeai_four_cocycle_v1 as base
from scripts import kuuos_v1103_codeai_structural_candidates_v1 as v103
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob

MODULE="KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106.lean"
V105="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105.lean"
V103="formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V105_BLOB="d6a8a8e2136c1a5601fa01c02f5f478fdd827520"
V103_BLOB="ff2e6a09e2c064a23207ee1323bc14182c86d7cd"
base.TARGET=TARGET
base.MODULE=MODULE
base.PREDECESSOR=V105
base.ORIGINAL_V103_BLOB=V105_BLOB
base.OUT=Path("/tmp/kuuos-v1106-codeai-label-table")
base.MCP_OUT=Path("/tmp/kuuos-v1106-real-mcp-label-table")

def source_observation(head,branch,tree,predecessor):
    assert git_blob(predecessor)==V105_BLOB
    upstream=(base.ROOT/V103).read_bytes()
    assert git_blob(upstream)==V103_BLOB
    return v103.source_observation(head,branch,tree,upstream)
base.source_observation=source_observation

LABELS=[
    ("a012","0","1","2"),("a013","0","1","3"),
    ("a014","0","1","4"),("a023","0","2","3"),
    ("a024","0","2","4"),("a034","0","3","4"),
    ("a123","1","2","3"),("a124","1","2","4"),
    ("a134","1","3","4"),("a234","2","3","4"),
]
INTRO = """import KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105

set_option maxHeartbeats 2000000

/-!
An actual type-A four-horn map prescribes all ten strict triangle comparison
labels. This theorem certifies their exact match with the finite ten-label
table. The remaining four visible tetrahedral equations and the final Yoneda
restriction are separate geometric obligations, not assumptions here.
-/

/-- Read precisely the ten strict triangle labels from the actual scaled
type-A four-horn map. -/
def natFourHornLabels
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    NatFourSimplexTriangleLabels where
"""
AFTER = """
/-- On every strictly ordered triple, the finite label table is definitionally
the literal comparison of the given horn map on the visible triangle. -/
theorem natFourHornLabels_strict
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a < b) (hbc : b < c) :
    natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c =
      natTypeAHornLabel (natTypeAFourIndex i hi0 hi4)
        (Nat.le_refl 4) f a b c (le_of_lt hab) (le_of_lt hbc) := by
"""
END="""

end KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
"""
def candidates() -> dict[str,str]:
    labels="".join(
        f"  {field} := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) " +
        f"(Nat.le_refl 4) f {a} {b} {c} (by decide) (by decide)\n"
        for field,a,b,c in LABELS)
    cases={
      "round1-table-simp":
         "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
         "    simp_all [natFourStrictLabel, natFourHornLabels]",
      "round1-table-simp-omega":
         "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
         "    simp_all [natFourStrictLabel, natFourHornLabels] <;>\n"
         "    all_goals omega",
      "round1-table-split":
         "  fin_cases a <;> fin_cases b <;> fin_cases c <;>\n"
         "    first\n"
         "    | simp_all [natFourStrictLabel, natFourHornLabels]\n"
         "    | omega",
    }
    return {n:INTRO+labels+AFTER+proof+END for n,proof in cases.items()}

def main():
    base.proposals=candidates
    return base.main()

if __name__=="__main__":
    raise SystemExit(main())
