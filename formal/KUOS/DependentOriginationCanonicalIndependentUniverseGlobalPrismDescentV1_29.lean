import KUOS.DependentOriginationCanonicalIndependentUniverseHomotopyDescentV1_29
import KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34

/-!
# Canonical independent-universe Duskin descent from one global prism

The canonical universe comparison already gives actual, proof-certified
E_B/E_C bridges without identifying independent chosen admissibility
predicates. This file replaces a horn-indexed homotopy hypothesis by one
global source and one global target Duskin prism. Their restrictions give
the already proved per-horn homotopies.

Global-prism realization, both rectification properties and two-way family
admissibility remain explicit prerequisites. In particular, a native strong
transformation is not silently identified with a simplicial homotopy.
-/

namespace KUOS.DependentOriginationCanonicalIndependentUniverseGlobalPrismDescentV1_29

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
open KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseHomotopyDescentV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- A *single global prism pair* supplies the actual family correspondence
needed for two independent universe levels, provided the two explicit
homotopy-rectification certificates hold. -/
noncomputable def canonicalCorrespondence_of_globalPrism
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
    (R : GlobalDuskinRoundTripPrismRealization K)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀) :=
  canonicalCorrespondence_of_homotopy_rectification
    B C F G HB₀ HC₀ hForward hBackward
    (R.toRoundTripBoundaryHomotopy
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G))
    RB RC

/-- The original *unlifted* Duskin fibrancy equivalence follows from a
global simplicial prism plus explicit rectification and admissibility,
without assuming literal inverse equations for normalized nerve maps. -/
theorem unliftedFibrancy_iff_of_canonical_independentUniverse_globalPrism
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
    (R : GlobalDuskinRoundTripPrismRealization K)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ :=
  unliftedFibrancy_iff_of_canonical_independentUniverse_homotopy
    B C F G HB₀ HC₀ hForward hBackward
    (R.toRoundTripBoundaryHomotopy
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G))
    RB RC

#print axioms canonicalCorrespondence_of_globalPrism
#print axioms unliftedFibrancy_iff_of_canonical_independentUniverse_globalPrism

end KUOS.DependentOriginationCanonicalIndependentUniverseGlobalPrismDescentV1_29
