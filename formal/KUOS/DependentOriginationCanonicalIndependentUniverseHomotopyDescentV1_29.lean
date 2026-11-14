import KUOS.DependentOriginationCanonicalIndependentUniverseFamilyCorrespondenceV1_29
import KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

/-!
# Independent-universe Duskin descent from homotopy and rectification

A coherent bicategorical quasi-inverse is not generally a strict inverse
of normalized Duskin simplicial maps. This additive result replaces
that overly strong condition with actual hornwise round-trip homotopies
and explicit homotopy-to-strict filler rectification on the lifted carriers.

The cross-universe E_B and E_C bridges are the exact canonical
constructions, not extra hypotheses. Model-map admissibility
preservation remains an explicit condition; hornwise homotopy and
rectification are genuine additional geometric obligations.
-/

namespace KUOS.DependentOriginationCanonicalIndependentUniverseHomotopyDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseFamilyCorrespondenceV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- For the actual canonical lifted horn families, hornwise homotopy and
rectification supply the two round-trip filler-reflection laws. -/
def canonicalCorrespondence_of_homotopy_rectification
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (hForward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀))
    (hBackward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (canonicalLiftedDuskinTargetFamily B C HC₀)
      (canonicalLiftedDuskinSourceFamily B C HB₀))
    (H : ScaledHornRoundTripBoundaryHomotopy F G
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G))
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀) where
  forward_admissible := hForward.admissible_preserved
  backward_admissible := hBackward.admissible_preserved
  source_roundTrip_filler_reflect := by
    intro n i P
    constructor
    · intro h
      exact RB.rectify P (sourceRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty
        (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
        (mapScaledHornFiller_nonempty
          (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled h)
  target_roundTrip_filler_reflect := by
    intro n i Q
    constructor
    · intro h
      exact RC.rectify Q (targetRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty
        (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
        (mapScaledHornFiller_nonempty
          (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled h)

/-- Actual original unlifted Duskin fibrancy is equivalent across independent
universe levels without any *strict inverse* equation, when the specified
hornwise homotopies, rectification and admissibility data are provided. -/
theorem unliftedFibrancy_iff_of_canonical_independentUniverse_homotopy
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (hForward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀))
    (hBackward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (canonicalLiftedDuskinTargetFamily B C HC₀)
      (canonicalLiftedDuskinSourceFamily B C HB₀))
    (H : ScaledHornRoundTripBoundaryHomotopy F G
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G))
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ :=
  unliftedFibrancy_iff_of_canonical_independentUniverse_correspondence
    B C F G HB₀ HC₀
    (canonicalCorrespondence_of_homotopy_rectification
      B C F G HB₀ HC₀ hForward hBackward H RB RC)

#print axioms canonicalCorrespondence_of_homotopy_rectification
#print axioms unliftedFibrancy_iff_of_canonical_independentUniverse_homotopy

end KUOS.DependentOriginationCanonicalIndependentUniverseHomotopyDescentV1_29
