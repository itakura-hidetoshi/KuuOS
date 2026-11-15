import KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104

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
    (x : (Λ[g.n, g.i] : SSet.{0}).obj (op ⦋3⦌))
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
    (x : (Λ[g.n, g.i] : SSet.{0}).obj (op ⦋3⦌)) :
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
  simpa [natHornTetraLabel, sigma, e01, e12, e23] using hcoc

/-- The actual standard type-(A) four-horn indexed by any inner vertex. -/
def natTypeAFourIndex
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4) :
    StandardTypeAHornGeneratorIndex where
  n := 4
  i := i
  inner_left := hi0
  inner_right := hi4

/-- A concrete visible tetrahedron, with its source universe fixed to the
same universe as the scaled map in this fixed Lean/mathlib build. -/
def natTypeAFourFace
    (i j : Fin 5) (hj : j ≠ i) :
    (Λ[4, i] : SSet.{0}).obj (op ⦋3⦌) :=
  SSet.horn.face i j hj

/-- Every literal visible codimension-one 3-face of a type-A four-horn
satisfies the additive cocycle equation after applying the given horn map. -/
theorem natTypeAFourVisibleFace_additive_cocycle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (j : Fin 5) (hj : j ≠ i) :
    natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (natTypeAFourFace i j hj)
          0 1 2 (by decide) (by decide) +
        natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (natTypeAFourFace i j hj)
          0 2 3 (by decide) (by decide) =
      natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (natTypeAFourFace i j hj)
          1 2 3 (by decide) (by decide) +
        natHornTetraLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (natTypeAFourFace i j hj)
          0 1 3 (by decide) (by decide) := by
  exact natHornTetraLabel_additive_cocycle
    (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (natTypeAFourFace i j hj)

end KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
