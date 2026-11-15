import KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornRestrictionV1_110

set_option maxHeartbeats 2000000

/-!
This is the literal four-dimensional type-(A) RLP proof for the concrete
additive double delooping. The completion is not postulated: its normalized
cocycle, all-degree restriction and distinguished-zero proof come directly
from the original horn map in v1.109-v1.110. A scaled lifting witness and
actual commuting-triangle equation are explicitly constructed.
-/

/-- The specified actual type-(A) four-horn map has a concrete complete
normalized Duskin cocycle, with the exact source restriction. -/
def natTypeAFourCocycleCompletion
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    NatTypeAHornCocycleCompletion (natTypeAFourIndex i hi0 hi4) f where
  cocycle := natTypeAFourHornCocycle i hi0 hi4 f
  restrict := natTypeAFourHornCocycle_restrict i hi0 hi4 f
  distinguished_zero := natTypeAFourHornCocycle_distinguished_zero i hi0 hi4 f

/-- An explicit source-bound cocycle-completion witness, not an added
hypothesis or an abstract RLP assertion. -/
theorem natTypeAFourCocycleCompletion_nonempty
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion (natTypeAFourIndex i hi0 hi4) f) :=
  ⟨natTypeAFourCocycleCompletion i hi0 hi4 f⟩

/-- Actual scaled simplex lift of the given type-(A) four-horn map. -/
def natTypeAFourLift
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    standardTypeAScaledSimplex (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin :=
  (natTypeAFourCocycleCompletion i hi0 hi4 f).toLift

/-- The concrete scaled simplex lift composes back to the input horn map. -/
theorem natTypeAFourLift_fac
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    standardTypeAScaledHornGeneratorHom (natTypeAFourIndex i hi0 hi4) ≫
      natTypeAFourLift i hi0 hi4 f = f := by
  exact (natTypeAFourCocycleCompletion i hi0 hi4 f).toLift_fac

/-- Concrete four-dimensional type-(A) horn RLP for the additive Duskin
scaled nerve at every inner vertex 1, 2, or 3. -/
theorem natDoubleDelooping_hasLiftingProperty_typeAFour
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4) :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom (natTypeAFourIndex i hi0 hi4))
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  apply natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
  intro f
  exact ⟨natTypeAFourCocycleCompletion i hi0 hi4 f⟩

end KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111
