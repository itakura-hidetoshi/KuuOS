import KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
open KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

set_option maxHeartbeats 2000000

/-!
For inner indices 1, 2, 3, the four visible 3-faces of an actual type-A
four-horn determine the fifth missing tetrahedral equation through v1.99.
The theorem does not yet construct the Yoneda restriction or terminal RLP.
-/

/-- All five exact ten-label tetrahedral equations are forced by the
given actual type-(A) four-horn map, including the missing one. -/
theorem natFourHorn_all_five_tetrahedra
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natFourHornLabels i hi0 hi4 f).eq0123 ∧
    (natFourHornLabels i hi0 hi4 f).eq0124 ∧
    (natFourHornLabels i hi0 hi4 f).eq0134 ∧
    (natFourHornLabels i hi0 hi4 f).eq0234 ∧
    (natFourHornLabels i hi0 hi4 f).eq1234 := by
  let L : NatFourSimplexTriangleLabels := natFourHornLabels i hi0 hi4 f
  change L.eq0123 ∧ L.eq0124 ∧ L.eq0134 ∧ L.eq0234 ∧ L.eq1234
  have h0 : (0 : Fin 5) ≠ i := by omega
  have h4 : (4 : Fin 5) ≠ i := by omega
  have h0123 : L.eq0123 :=
    natFourHorn_visible_face4_eq0123 i hi0 hi4 f h4
  have h1234 : L.eq1234 :=
    natFourHorn_visible_face0_eq1234 i hi0 hi4 f h0
  by_cases hi1 : i = (1 : Fin 5)
  · have h3 : (3 : Fin 5) ≠ i := by rw [hi1]; decide
    have h2 : (2 : Fin 5) ≠ i := by rw [hi1]; decide
    have h0124 : L.eq0124 :=
      natFourHorn_visible_face3_eq0124 i hi0 hi4 f h3
    have h0134 : L.eq0134 :=
      natFourHorn_visible_face2_eq0134 i hi0 hi4 f h2
    have h0234 : L.eq0234 :=
      natFour_typeA_index1_missing_face L h0123 h0124 h0134 h1234
    exact ⟨h0123, h0124, h0134, h0234, h1234⟩
  · by_cases hi2 : i = (2 : Fin 5)
    · have h3 : (3 : Fin 5) ≠ i := by rw [hi2]; decide
      have h1 : (1 : Fin 5) ≠ i := by rw [hi2]; decide
      have h0124 : L.eq0124 :=
        natFourHorn_visible_face3_eq0124 i hi0 hi4 f h3
      have h0234 : L.eq0234 :=
        natFourHorn_visible_face1_eq0234 i hi0 hi4 f h1
      have h0134 : L.eq0134 :=
        natFour_typeA_index2_missing_face L h0123 h0124 h0234 h1234
      exact ⟨h0123, h0124, h0134, h0234, h1234⟩
    · by_cases hi3 : i = (3 : Fin 5)
      · have h2 : (2 : Fin 5) ≠ i := by rw [hi3]; decide
        have h1 : (1 : Fin 5) ≠ i := by rw [hi3]; decide
        have h0134 : L.eq0134 :=
          natFourHorn_visible_face2_eq0134 i hi0 hi4 f h2
        have h0234 : L.eq0234 :=
          natFourHorn_visible_face1_eq0234 i hi0 hi4 f h1
        have h0124 : L.eq0124 :=
          natFour_typeA_index3_missing_face L h0123 h0134 h0234 h1234
        exact ⟨h0123, h0124, h0134, h0234, h1234⟩
      · have hv0 : 0 < i.val := (Fin.lt_def).mp hi0
        have hv4 : i.val < 4 := (Fin.lt_def).mp hi4
        have hn1 : i.val ≠ 1 := by
          intro h
          apply hi1
          apply Fin.ext
          simpa using h
        have hn2 : i.val ≠ 2 := by
          intro h
          apply hi2
          apply Fin.ext
          simpa using h
        have hn3 : i.val ≠ 3 := by
          intro h
          apply hi3
          apply Fin.ext
          simpa using h
        omega

end KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108
