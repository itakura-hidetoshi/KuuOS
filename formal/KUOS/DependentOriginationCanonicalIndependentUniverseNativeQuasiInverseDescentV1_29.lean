import KUOS.DependentOriginationCanonicalIndependentUniverseGlobalPrismDescentV1_29
import KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36

/-!
# Canonical Duskin fibrancy descent from native coherent quasi-inverses

The formally established v1.36 theorem
\`globalDuskinRoundTripPrismRealization\` constructs the source and target
global simplicial prisms directly from the native normalized coherent
bicategorical quasi-inverse. We therefore need not postulate either a
strict inverse of the nerve maps or a new global-prism witness.

The independent remaining conditions are the *actual* two-way
admissibility-preservation witnesses for the canonical lifted families
and the homotopy-to-strict horn filler rectification for each target.
No arbitrary family identification or unproved rectification is made.
-/

namespace KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseGlobalPrismDescentV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- Native coherent quasi-inverse plus explicit admissibility and rectification
canonically constructs a typed lifted-family correspondence at independent
universe levels, with the global simplicial prisms supplied by v1.36. -/
noncomputable def canonicalCorrespondence_of_nativeQuasiInverse
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
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀) :=
  canonicalCorrespondence_of_globalPrism
    B C F G HB₀ HC₀ hForward hBackward K
    (globalDuskinRoundTripPrismRealization K) RB RC

/-- The original (unlifted) Duskin nerve fibrancy is invariant under a
native coherent quasi-inverse, provided the *canonical* two-way family
admissibility and homotopy rectification conditions are established.
No strict inverse or global-prism witness is an extra hypothesis. -/
theorem unliftedFibrancy_iff_of_canonical_nativeQuasiInverse
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
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ :=
  unliftedFibrancy_iff_of_canonical_independentUniverse_globalPrism
    B C F G HB₀ HC₀ hForward hBackward K
    (globalDuskinRoundTripPrismRealization K) RB RC

#print axioms canonicalCorrespondence_of_nativeQuasiInverse
#print axioms unliftedFibrancy_iff_of_canonical_nativeQuasiInverse

end KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29
