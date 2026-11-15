import KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100

set_option maxHeartbeats 2000000

/-!
The normalized four-dimensional additive Duskin cocycle constructed from
the ten actual finite labels. This does not assert four-horn RLP:
the geometric transport of all four visible face equations from a
specified horn map remains an independent obligation.
-/

/-- Read a strict triangle from the exact ten-label table. -/
def natFourStrictLabel
    (L : NatFourSimplexTriangleLabels)
    (a b c : Fin 5) : Nat :=
  match a.val, b.val, c.val with
  | 0, 1, 2 => L.a012
  | 0, 1, 3 => L.a013
  | 0, 1, 4 => L.a014
  | 0, 2, 3 => L.a023
  | 0, 2, 4 => L.a024
  | 0, 3, 4 => L.a034
  | 1, 2, 3 => L.a123
  | 1, 2, 4 => L.a124
  | 1, 3, 4 => L.a134
  | 2, 3, 4 => L.a234
  | _, _, _ => 0

/-- All five ordinary tetrahedron equations induce a genuine,
normalized Duskin cocycle on the ordinal of length five. -/
def natFourCocycleOfLabels
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123) (h0124 : L.eq0124)
    (h0134 : L.eq0134) (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    NatNormalizedDuskinCocycle 4 where
  label a b c _ _ := natFourStrictLabel L a b c
  left_normalized := by
    intro a b hab
    fin_cases a <;> fin_cases b <;>
      simp [natFourStrictLabel]
  right_normalized := by
    intro a b hab
    fin_cases a <;> fin_cases b <;>
      simp [natFourStrictLabel]
  tetrahedron := by
    intro a b c d hab hbc hcd
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp_all [natFourStrictLabel,
        NatFourSimplexTriangleLabels.eq0123,
        NatFourSimplexTriangleLabels.eq0124,
        NatFourSimplexTriangleLabels.eq0134,
        NatFourSimplexTriangleLabels.eq0234,
        NatFourSimplexTriangleLabels.eq1234,
        NatTetrahedronEquation]

/-- The missing tetrahedron 0234 in type-A index 1 is forced by
the other four faces; the output is a genuine cocycle. -/
def natFourTypeAIndex1Cocycle
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123) (h0124 : L.eq0124)
    (h0134 : L.eq0134) (h1234 : L.eq1234) :
    NatNormalizedDuskinCocycle 4 :=
  natFourCocycleOfLabels L h0123 h0124 h0134
    (natFour_typeA_index1_missing_face L h0123 h0124 h0134 h1234) h1234

/-- The missing tetrahedron 0134 in type-A index 2 is forced by
the other four faces; the output is a genuine cocycle. -/
def natFourTypeAIndex2Cocycle
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123) (h0124 : L.eq0124)
    (h0234 : L.eq0234) (h1234 : L.eq1234) :
    NatNormalizedDuskinCocycle 4 :=
  natFourCocycleOfLabels L h0123 h0124
    (natFour_typeA_index2_missing_face L h0123 h0124 h0234 h1234)
    h0234 h1234

/-- The missing tetrahedron 0124 in type-A index 3 is forced by
the other four faces; the output is a genuine cocycle. -/
def natFourTypeAIndex3Cocycle
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123) (h0134 : L.eq0134)
    (h0234 : L.eq0234) (h1234 : L.eq1234) :
    NatNormalizedDuskinCocycle 4 :=
  natFourCocycleOfLabels L h0123
    (natFour_typeA_index3_missing_face L h0123 h0134 h0234 h1234)
    h0134 h0234 h1234

end KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
