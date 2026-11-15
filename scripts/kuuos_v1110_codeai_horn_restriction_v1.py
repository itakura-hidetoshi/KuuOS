#!/usr/bin/env python3
"""v1.110 CodeAI x MemoryOS: non-strict triangle labels, real horn restriction.

Use the independently certified exact v1.109 cocycle, its label equality,
existing v1.103 simplicial naturality/normalization and v1.101 zero
comparison. Every proposed theorem has the original actual horn map as input.
No existential filler or RLP is inferred before the Lean proof closes.
"""
from __future__ import annotations
import json
from pathlib import Path

from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110.lean"
MODULE="KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109.lean"
PRIOR_BLOB="e703d406b303a8dd51178ca26ee227473509e76d"
OUT=Path("/tmp/kuuos-v1110-codeai-horn-restriction")
MCP=Path("/tmp/kuuos-v1110-real-mcp-horn-restriction")
REPORT=Path("/tmp/kuuos-v1110-memoryos/context.json")
MEMORY=Path("memoryos/external/github/2026/11")

INTRO="""import KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
open KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108
open KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109

set_option maxHeartbeats 2000000

/-!
A real four-dimensional type-A horn map determines the normalized cocycle
certified in v1.109. This module proves exact equality of labels even when
vertices repeat, the literal all-degree Yoneda restriction to the given horn
map, and zero comparison on the distinguished type-A triangle. These are
geometric proof obligations, not new premises. A terminal RLP certificate
is not asserted here.
-/

/-- Compare the realized cocycle with the given horn map on ALL ordered
triples, including degenerate triangles. -/
theorem natTypeAFourHornCocycle_ordered_label
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a ≤ b) (hbc : b ≤ c) :
    (natTypeAFourHornCocycle i hi0 hi4 f).label a b c hab hbc =
      natTypeAHornLabel (natTypeAFourIndex i hi0 hi4)
        (Nat.le_refl 4) f a b c hab hbc := by
"""
VARIANTS={
  "round1-bycases-omega": """  by_cases hAB : a = b
  · subst b
    calc
      _ = 0 := (natTypeAFourHornCocycle i hi0 hi4 f).left_normalized a c hbc
      _ = _ := (natTypeAHornLabel_left_zero
        (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a c hbc).symm
  · by_cases hBC : b = c
    · subst c
      calc
        _ = 0 := (natTypeAFourHornCocycle i hi0 hi4 f).right_normalized a b hab
        _ = _ := (natTypeAHornLabel_right_zero
          (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a b hab).symm
    · have hablt : a < b := by omega
      have hbclt : b < c := by omega
      exact natTypeAFourHornCocycle_strict i hi0 hi4 f a b c hablt hbclt
""",
  "round1-bycases-ltne": """  by_cases hAB : a = b
  · subst b
    calc
      _ = 0 := (natTypeAFourHornCocycle i hi0 hi4 f).left_normalized a c hbc
      _ = _ := (natTypeAHornLabel_left_zero
        (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a c hbc).symm
  · by_cases hBC : b = c
    · subst c
      calc
        _ = 0 := (natTypeAFourHornCocycle i hi0 hi4 f).right_normalized a b hab
        _ = _ := (natTypeAHornLabel_right_zero
          (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a b hab).symm
    · have hablt : a < b := lt_of_le_of_ne hab hAB
      have hbclt : b < c := lt_of_le_of_ne hbc hBC
      exact natTypeAFourHornCocycle_strict i hi0 hi4 f a b c hablt hbclt
""",
  "round1-bycases-prop-equalities": """  by_cases hAB : a = b
  · subst b
    have hLeft := (natTypeAFourHornCocycle i hi0 hi4 f).left_normalized a c hbc
    have hHorn := natTypeAHornLabel_left_zero
      (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a c hbc
    exact hLeft.trans hHorn.symm
  · by_cases hBC : b = c
    · subst c
      have hRight := (natTypeAFourHornCocycle i hi0 hi4 f).right_normalized a b hab
      have hHorn := natTypeAHornLabel_right_zero
        (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f a b hab
      exact hRight.trans hHorn.symm
    · have hablt : a < b := by omega
      have hbclt : b < c := by omega
      exact natTypeAFourHornCocycle_strict i hi0 hi4 f a b c hablt hbclt
""",
}
AFTER="""
/-- The Yoneda realization of the actual four-horn cocycle restricts to the
given original simplicial horn map in EVERY simplicial degree. -/
theorem natTypeAFourHornCocycle_restrict
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (Λ[4, i].ι :
      (Λ[4, i] : SSet) ⟶ (Δ[4] : SSet)) ≫
        (natTypeAFourHornCocycle i hi0 hi4 f).toSimplexMap = f.map := by
  ext k x
  rcases k with ⟨⟨m⟩⟩
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c p q
  change
    ((natTypeAFourHornCocycle i hi0 hi4 f).toSimplexMap.app
      (op ⦋m⦌) x.val).mapComp p q =
        (f.map.app (op ⦋m⦌) x).mapComp p q
  rw [NatNormalizedDuskinCocycle.toSimplexMap_mapComp]
  rw [natTypeAFourHornCocycle_ordered_label]
  exact (natTypeAHornMap_mapComp_eq_label
    (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f x p q).symm

/-- The actual four-horn source has zero comparison on its distinguished
consecutive type-A triangle; hence so does the realized four-cocycle. -/
theorem natTypeAFourHornCocycle_distinguished_zero
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.NatNormalizedDuskinCocycle.TypeADistinguishedZero
      (natTypeAFourHornCocycle i hi0 hi4 f) i := by
  intro a b c hab hbc hbi ha hc
  change (natTypeAFourHornCocycle i hi0 hi4 f).label a b c hab hbc = 0
  rw [natTypeAFourHornCocycle_ordered_label]
  exact natTypeAHornLabel_distinguished_zero
    (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4)
    f a b c hab hbc hbi ha hc

end KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110
"""

def candidates() -> dict[str,str]:
    source={name:INTRO+proof+AFTER for name,proof in VARIANTS.items()}
    head,branch,tree=require_event()
    prior=read_observation_directory(MEMORY)
    retained,receipt=route_candidates(source,prior,
             source_head=head,source_tree=tree,imported_blob=PRIOR_BLOB)
    if not retained:
        raise RuntimeError("no admissible candidate; do not infer theorem false")
    receipt["causal_status"]="UNVERIFIED_HYPOTHESIS"
    receipt["grants_proof_authority"]=False
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1110_MEMORYOS_PREFLIGHT "+json.dumps({
      "cases":len(prior),"retained":list(retained),
      "quarantined":receipt.get("quarantined"),
      "hints":receipt.get("analogical_hints"),
      "proof_authority":False},sort_keys=True))
    return retained

def main() -> int:
    harness.V105=PRIOR
    harness.V105_BLOB=PRIOR_BLOB
    harness.base.TARGET=TARGET
    harness.base.MODULE=MODULE
    harness.base.PREDECESSOR=PRIOR
    harness.base.ORIGINAL_V103_BLOB=PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
