import KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105

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
  a012 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (1 : Fin 5) (2 : Fin 5)
    (show (0 : Fin 5) ≤ (1 : Fin 5) from by decide)
    (show (1 : Fin 5) ≤ (2 : Fin 5) from by decide)
  a013 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (1 : Fin 5) (3 : Fin 5)
    (show (0 : Fin 5) ≤ (1 : Fin 5) from by decide)
    (show (1 : Fin 5) ≤ (3 : Fin 5) from by decide)
  a014 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (1 : Fin 5) (4 : Fin 5)
    (show (0 : Fin 5) ≤ (1 : Fin 5) from by decide)
    (show (1 : Fin 5) ≤ (4 : Fin 5) from by decide)
  a023 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (2 : Fin 5) (3 : Fin 5)
    (show (0 : Fin 5) ≤ (2 : Fin 5) from by decide)
    (show (2 : Fin 5) ≤ (3 : Fin 5) from by decide)
  a024 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (2 : Fin 5) (4 : Fin 5)
    (show (0 : Fin 5) ≤ (2 : Fin 5) from by decide)
    (show (2 : Fin 5) ≤ (4 : Fin 5) from by decide)
  a034 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (0 : Fin 5) (3 : Fin 5) (4 : Fin 5)
    (show (0 : Fin 5) ≤ (3 : Fin 5) from by decide)
    (show (3 : Fin 5) ≤ (4 : Fin 5) from by decide)
  a123 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (1 : Fin 5) (2 : Fin 5) (3 : Fin 5)
    (show (1 : Fin 5) ≤ (2 : Fin 5) from by decide)
    (show (2 : Fin 5) ≤ (3 : Fin 5) from by decide)
  a124 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (1 : Fin 5) (2 : Fin 5) (4 : Fin 5)
    (show (1 : Fin 5) ≤ (2 : Fin 5) from by decide)
    (show (2 : Fin 5) ≤ (4 : Fin 5) from by decide)
  a134 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (1 : Fin 5) (3 : Fin 5) (4 : Fin 5)
    (show (1 : Fin 5) ≤ (3 : Fin 5) from by decide)
    (show (3 : Fin 5) ≤ (4 : Fin 5) from by decide)
  a234 := natTypeAHornLabel (natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4) f (2 : Fin 5) (3 : Fin 5) (4 : Fin 5)
    (show (2 : Fin 5) ≤ (3 : Fin 5) from by decide)
    (show (3 : Fin 5) ≤ (4 : Fin 5) from by decide)

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
  have habv : a.val < b.val := (Fin.lt_def).mp hab
  have hbcv : b.val < c.val := (Fin.lt_def).mp hbc
  fin_cases a <;> fin_cases b <;> fin_cases c <;>
    simp_all [natFourStrictLabel, natFourHornLabels]

end KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
