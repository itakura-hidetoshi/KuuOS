import KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
open KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107
open KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

set_option maxHeartbeats 2000000

/-!
The original scaled four-horn map, not arbitrary assumed tetrahedral laws,
induces a genuine normalized Nat Duskin cocycle on Delta[4]. By construction
its strict triangle labels and their Yoneda-realized comparisons agree
with the actual visible horn labels. Literal all-degree restriction and
distinguished-triangle scaledness remain independent future obligations.
-/

/-- Construct a normalized Duskin four-cocycle from the actual scaled
four-horn map, using v1.108 to prove all five equations. -/
def natTypeAFourHornCocycle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) : NatNormalizedDuskinCocycle 4  := by
  let L : NatFourSimplexTriangleLabels := natFourHornLabels i hi0 hi4 f
  have h : L.eq0123 ∧ L.eq0124 ∧ L.eq0134 ∧ L.eq0234 ∧ L.eq1234 :=
    natFourHorn_all_five_tetrahedra i hi0 hi4 f
  exact natFourCocycleOfLabels L h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

/-- The constructed normalized cocycle reads the same ten-label table
on every ordered triple, with repeated-vertex normalization included. -/
theorem natTypeAFourHornCocycle_label
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a ≤ b) (hbc : b ≤ c) :
    (natTypeAFourHornCocycle i hi0 hi4 f).label a b c hab hbc =
      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by
  rfl

/-- On strictly ordered triangles of the actual source horn, the cocycle
comparison is the original horn map's actual comparison label. -/
theorem natTypeAFourHornCocycle_strict
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a < b) (hbc : b < c) :
    (natTypeAFourHornCocycle i hi0 hi4 f).label a b c
        (le_of_lt hab) (le_of_lt hbc) =
      natTypeAHornLabel (natTypeAFourIndex i hi0 hi4)
        (Nat.le_refl 4) f a b c (le_of_lt hab) (le_of_lt hbc) := by
  exact (natTypeAFourHornCocycle_label i hi0 hi4 f a b c
    (le_of_lt hab) (le_of_lt hbc)).trans
    (natFourHornLabels_strict i hi0 hi4 f a b c hab hbc)

/-- The Yoneda-realized comparison of every ordered triangle is precisely
the original horn's already-certified ten-label table, including degeneracies.
This does not itself assert equality of full simplicial horn maps. -/
theorem natTypeAFourHornCocycle_realized_triangle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a ≤ b) (hbc : b ≤ c) :
    KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21.duskinComparison
        ((natTypeAFourHornCocycle i hi0 hi4 f).toSimplexMap.app
          (op ⦋2⦌) (SSet.stdSimplex.triangle a b c hab hbc)) =
      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by
  exact (NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison
    (natTypeAFourHornCocycle i hi0 hi4 f) a b c hab hbc).trans
    (natTypeAFourHornCocycle_label i hi0 hi4 f a b c hab hbc)

end KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109
