#!/usr/bin/env python3
"""v1.105 four-dimensional actual horn-face cocycle CodeAI portfolio.

Stages: real CodeAI patch proposals -> pinned direct Lean on every proposal ->
real Lean MCP only on a direct-green candidate -> separate independent exact CI.
Adds a theorem about the image of an ACTUAL three-simplex in a type-A horn,
not a generalized RLP or assumption of the desired conclusion.
"""
from __future__ import annotations
from pathlib import Path
from scripts import kuuos_v1104_codeai_four_cocycle_v1 as base
from scripts import kuuos_v1103_codeai_structural_candidates_v1 as v103
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob

MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105.lean"
V104 = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104.lean"
V103 = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V104_BLOB = "6c4c3a2243796aa19d494c685b1b52796feeb2dd"
V103_BLOB = "ff2e6a09e2c064a23207ee1323bc14182c86d7cd"
base.TARGET = TARGET
base.MODULE = MODULE
base.PREDECESSOR = V104
base.ORIGINAL_V103_BLOB = V104_BLOB
base.OUT = Path("/tmp/kuuos-v1105-codeai-probes")
base.MCP_OUT = Path("/tmp/kuuos-v1105-real-mcp")

def observed_source(head: str, branch: str, tree: str, predecessor: bytes):
    # v1.103 source-observation envelope records actual on-disk v1.103 (and
    # v1.102); v1.104 is separately checked at its exact immutable Git blob
    # immediately below before ANY CodeAI candidate is generated.
    assert git_blob(predecessor) == V104_BLOB
    upstream = (base.ROOT/V103).read_bytes()
    assert git_blob(upstream) == V103_BLOB
    return v103.source_observation(head,branch,tree,upstream)
base.source_observation = observed_source

HEADER = """import KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103

/-!
An actual horn 3-simplex satisfies its tetrahedral additive equation after
transport through the given scaled simplicial horn map. This directly advances
the dimension-four geometric obligation. It does not infer missing-face RLP,
nor assume the equation as a new hypothesis.
-/

/-- The actual visible triangle label for any ordered three vertices in a
three-dimensional horn simplex. -/
def natHornTetraLabel
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (x : (Λ[g.n, g.i] : SSet).obj (op ⦋3⦌))
    (a b c : Fin 4) (hab : a ≤ b) (hbc : b ≤ c) : Nat :=
  natTypeAHornLabel g hn f
    (x.val a) (x.val b) (x.val c)
    ((SSet.stdSimplex.monotone_apply x.val) hab)
    ((SSet.stdSimplex.monotone_apply x.val) hbc)

/-- The ordinary tetrahedral equation holds on every actual horn 3-simplex
in dimensions >=4. No visibility assumption on that simplex is invented. -/
theorem natHornTetraLabel_additive_cocycle
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (x : (Λ[g.n, g.i] : SSet).obj (op ⦋3⦌)) :
    natHornTetraLabel g hn f x 0 1 2 (by decide) (by decide) +
        natHornTetraLabel g hn f x 0 2 3 (by decide) (by decide) =
      natHornTetraLabel g hn f x 1 2 3 (by decide) (by decide) +
        natHornTetraLabel g hn f x 0 1 3 (by decide) (by decide) := by
  let sigma : DuskinSimplex NatDoubleDelooping 3 :=
    f.map.app (op ⦋3⦌) x
  let e01 :
      LocallyDiscrete.mk (0 : Fin 4) ⟶ LocallyDiscrete.mk (1 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e12 :
      LocallyDiscrete.mk (1 : Fin 4) ⟶ LocallyDiscrete.mk (2 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e23 :
      LocallyDiscrete.mk (2 : Fin 4) ⟶ LocallyDiscrete.mk (3 : Fin 4) :=
    natOrdinalEdge (by decide)
  have hcoc := natDuskin_mapComp_additive_cocycle sigma e01 e12 e23
  have h012 := natTypeAHornMap_mapComp_eq_label g hn f x e01 e12
  have h023 := natTypeAHornMap_mapComp_eq_label g hn f x (e01 ≫ e12) e23
  have h123 := natTypeAHornMap_mapComp_eq_label g hn f x e12 e23
  have h013 := natTypeAHornMap_mapComp_eq_label g hn f x e01 (e12 ≫ e23)
  rw [h012, h023, h123, h013] at hcoc
"""
TAIL="""

/-- The actual standard type-(A) four-horn indexed by any inner vertex. -/
def natTypeAFourIndex
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4) :
    StandardTypeAHornGeneratorIndex where
  n := 4
  i := i
  inner_left := hi0
  inner_right := hi4

/-- Every literal visible codimension-one 3-face of a type-A four-horn
satisfies the additive cocycle equation after applying the given horn map. -/
theorem natTypeAFourVisibleFace_additive_cocycle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (j : Fin 5) (hj : j ≠ i) :
    let x : (Λ[4, i] : SSet).obj (op ⦋3⦌) :=
      SSet.horn.face i j hj
    natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (by decide) f x
          0 1 2 (by decide) (by decide) +
        natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (by decide) f x
          0 2 3 (by decide) (by decide) =
      natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (by decide) f x
          1 2 3 (by decide) (by decide) +
        natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (by decide) f x
          0 1 3 (by decide) (by decide) := by
  exact natHornTetraLabel_additive_cocycle
    (natTypeAFourIndex i hi0 hi4) (by decide) f (SSet.horn.face i j hj)

end KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
"""

def candidates() -> dict[str,str]:
    tactics={
       "round1-simpa": "  simpa [natHornTetraLabel, sigma, e01, e12, e23] using hcoc",
       "round1-simpa-only": "  simpa only [natHornTetraLabel, sigma, e01, e12, e23] using hcoc",
       "round1-simpa-reducible": "  simpa [natHornTetraLabel, sigma, e01, e12, e23, natOrdinalEdge] using hcoc",
    }
    return {n:HEADER + tactic + TAIL for n,tactic in tactics.items()}

def main():
    base.proposals = candidates
    return base.main()

if __name__ == "__main__":
    raise SystemExit(main())
