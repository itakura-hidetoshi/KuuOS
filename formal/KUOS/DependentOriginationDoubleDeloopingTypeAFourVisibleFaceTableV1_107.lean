import KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106

set_option maxHeartbeats 2000000

/-!
These theorems transport the additive equations of actual visible tetrahedra
through the given four-horn map to the ten labels already extracted in v1.106.
Each implication explicitly requires that the corresponding face is visible.
The missing face and the Yoneda realization are NOT assumed or proved here.
-/

/-- Real visible face 4 provides table equation eq0123. -/
theorem natFourHorn_visible_face4_eq0123
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (hj : (4 : Fin 5) ≠ i) :
    (natFourHornLabels i hi0 hi4 f).eq0123 := by
  exact natTypeAFourVisibleFace_additive_cocycle
    i hi0 hi4 f (4 : Fin 5) hj

/-- Real visible face 3 provides table equation eq0124. -/
theorem natFourHorn_visible_face3_eq0124
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (hj : (3 : Fin 5) ≠ i) :
    (natFourHornLabels i hi0 hi4 f).eq0124 := by
  exact natTypeAFourVisibleFace_additive_cocycle
    i hi0 hi4 f (3 : Fin 5) hj

/-- Real visible face 2 provides table equation eq0134. -/
theorem natFourHorn_visible_face2_eq0134
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (hj : (2 : Fin 5) ≠ i) :
    (natFourHornLabels i hi0 hi4 f).eq0134 := by
  exact natTypeAFourVisibleFace_additive_cocycle
    i hi0 hi4 f (2 : Fin 5) hj

/-- Real visible face 1 provides table equation eq0234. -/
theorem natFourHorn_visible_face1_eq0234
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (hj : (1 : Fin 5) ≠ i) :
    (natFourHornLabels i hi0 hi4 f).eq0234 := by
  exact natTypeAFourVisibleFace_additive_cocycle
    i hi0 hi4 f (1 : Fin 5) hj

/-- Real visible face 0 provides table equation eq1234. -/
theorem natFourHorn_visible_face0_eq1234
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (hj : (0 : Fin 5) ≠ i) :
    (natFourHornLabels i hi0 hi4 f).eq1234 := by
  exact natTypeAFourVisibleFace_additive_cocycle
    i hi0 hi4 f (0 : Fin 5) hj


end KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107
