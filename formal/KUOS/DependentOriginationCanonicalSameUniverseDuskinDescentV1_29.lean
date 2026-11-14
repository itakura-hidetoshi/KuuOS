import KUOS.DependentOriginationCanonicalULiftHornPresentationBridgeV1_29
import KUOS.DependentOriginationLiftedDuskinCanonicalStrictDescentV1_29

/-!
# Canonical typed descent for two Duskin nerves in one universe

The original v1.29 theorem requires independently supplied E_B/E_C horn
presentation equivalences. This additive specialization constructs these
two bridges from the canonical same-universe ULift isomorphisms, keeping
the original families, scaled generators and theorem statements intact.

The bicategorical maps must still have a strict inverse on the lifted
carriers and preserve the precisely transported admissibility families.
Independent B/C universe-level changes are NOT claimed by this module.
-/

namespace KUOS.DependentOriginationCanonicalSameUniverseDuskinDescentV1_29

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30
open KUOS.DependentOriginationLiftedDuskinCanonicalStrictDescentV1_29
open KUOS.DependentOriginationCanonicalULiftHornPresentationBridgeV1_29

universe u v w

/-- The original (nonlifted) B Duskin horn presentation is canonically
equivalent to the actual normalized B/C source when the universes match. -/
theorem sourceFibrancy_iff_canonicalULift
    (B C : Type u) [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (HB₀ : GlobalDuskinScaledHornFamily B) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)
        (canonicalSameUniverseULiftFamily (duskinScaling B) HB₀) :=
  canonicalSameUniverseULift_fibrancy_iff (duskinScaling B) HB₀

/-- The same construction on the C side gives the canonical E_C descent. -/
theorem targetFibrancy_iff_canonicalULift
    (B C : Type u) [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (HC₀ : GlobalDuskinScaledHornFamily C) :
    HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ ↔
      HasScaledHornFillers
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)
        (canonicalSameUniverseULiftFamily (duskinScaling C) HC₀) :=
  canonicalSameUniverseULift_fibrancy_iff (duskinScaling C) HC₀

/-- Genuine unlifted Duskin fibrancy descent *without* externally supplied
E_B/E_C, for bicategories with matching universe levels. The remaining strict
inverse and lifted admissibility conditions are exactly those in the original
v1.29 theorem and have NOT been weakened or inferred unconditionally. -/
theorem unliftedFibrancy_iff_of_canonical_sameUniverse_strictInverse
    (B C : Type u) [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (hForward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (canonicalSameUniverseULiftFamily (duskinScaling B) HB₀)
      (canonicalSameUniverseULiftFamily (duskinScaling C) HC₀))
    (hBackward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (canonicalSameUniverseULiftFamily (duskinScaling C) HC₀)
      (canonicalSameUniverseULiftFamily (duskinScaling B) HB₀))
    (hSource : normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G =
      𝟙 (normalizedDuskinSource B C))
    (hTarget : normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F =
      𝟙 (normalizedDuskinTarget B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  exact unliftedFibrancy_iff_of_canonical_strictInverse
    F G HB₀ HC₀
    (canonicalSameUniverseULiftFamily (duskinScaling B) HB₀)
    (canonicalSameUniverseULiftFamily (duskinScaling C) HC₀)
    (canonicalSameUniverseULiftPresentationEquivalence (duskinScaling B) HB₀)
    (canonicalSameUniverseULiftPresentationEquivalence (duskinScaling C) HC₀)
    hForward hBackward hSource hTarget

#print axioms sourceFibrancy_iff_canonicalULift
#print axioms targetFibrancy_iff_canonicalULift
#print axioms unliftedFibrancy_iff_of_canonical_sameUniverse_strictInverse

end KUOS.DependentOriginationCanonicalSameUniverseDuskinDescentV1_29
