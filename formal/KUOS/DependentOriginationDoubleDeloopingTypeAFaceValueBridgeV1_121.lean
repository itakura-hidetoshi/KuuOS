import KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112

/-!
Exact four face-value equalities from the original v1.104 statements,
but independent of the currently failing v1.104 proof body. The original
is never overwritten or imported. Type-A right orthogonality is taken from
the independently CI-certified all-dimensional v1.112 proof; no new
fibrancy assumption, no sorry, no axiom.
-/

/-- Face `1` has ordered vertices `0234`. -/
theorem natTypeAFour_face1_val
    (i : Fin 5) (h : (1 : Fin 5) ≠ i) :
    (SSet.horn.face i (1 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 2 3 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `2` has ordered vertices `0134`. -/
theorem natTypeAFour_face2_val
    (i : Fin 5) (h : (2 : Fin 5) ≠ i) :
    (SSet.horn.face i (2 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 3 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `3` has ordered vertices `0124`. -/
theorem natTypeAFour_face3_val
    (i : Fin 5) (h : (3 : Fin 5) ≠ i) :
    (SSet.horn.face i (3 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 2 4 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Face `4` has ordered vertices `0123`. -/
theorem natTypeAFour_face4_val
    (i : Fin 5) (h : (4 : Fin 5) ≠ i) :
    (SSet.horn.face i (4 : Fin 5) h).val =
      natOrderedTetrahedron
        (0 : Fin 5) 1 2 3 (by decide) (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl


/-- The full standard type-(A) horn terminal RLP is the previously
independently certified v1.112 actual cocycle-completion result. -/
theorem natDoubleDelooping_standardTypeA_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_typeA_full_standard_rlp

end KUOS.DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121
