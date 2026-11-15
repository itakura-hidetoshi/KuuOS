import KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109

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
  by_cases hAB : a = b
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
  apply KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.natDuskinSimplex_eq_of_mapComp_eq
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
  rw [natTypeAFourHornCocycle_ordered_label]
  exact natTypeAHornLabel_distinguished_zero
    (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4)
    f a b c hab hbc hbi ha hc

end KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110
