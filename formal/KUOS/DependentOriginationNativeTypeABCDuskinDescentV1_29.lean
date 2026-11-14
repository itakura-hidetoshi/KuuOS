import KUOS.DependentOriginationNativeTypeAUniverseGeometryV1_29
import KUOS.DependentOriginationForwardHornRectificationV1_29
import KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29

/-!
# Native type-(A) B/C correspondence from true scaled maps and directed RLP

Both native type-(A) horn predicates remember the exact scaled simplex
and scaled horn structures.  The certified normalized Duskin map retains
these structures under mapScaledHornProblem.  After exact type-(A)
universe descent (v1.29), a native normalized coherent quasi-inverse
supplies genuine global prisms, and endpoint-zero cylinder RLP on each
lifted carrier converts the resulting homotopy fillers to strict fillers.

No extra family-map / abstract lifted-D correspondence is assumed.
The two forward-endpoint RLP inputs remain INDEPENDENT obligations,
and no unconditional fibrancy of an arbitrary Duskin nerve is claimed.
-/

namespace KUOS.DependentOriginationNativeTypeABCDuskinDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34
open KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationIndependentAdmissibilityRectificationV1_29
open KUOS.DependentOriginationForwardHornRectificationV1_29
open KUOS.DependentOriginationNativeTypeAUniverseGeometryV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- The real normalized B-to-C map preserves the entire native
type-(A) admissibility predicate, including the two scaling identities. -/
def nativeTypeAForwardFamilyMap
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (standardTypeAScaledHornFamily
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
      (standardTypeAScaledHornFamily
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :=
  standardTypeAFamilyMap_of_scaledMap
    (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled

/-- Genuine reverse C-to-B preservation is constructed independently,
without assuming strict inverse equations for the two nerve maps. -/
def nativeTypeABackwardFamilyMap
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) :
    ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (standardTypeAScaledHornFamily
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C))
      (standardTypeAScaledHornFamily
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)) :=
  standardTypeAFamilyMap_of_scaledMap
    (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled

/-- A genuine lifted B/C family correspondence is BUILT from the
native coherent quasi-inverse, the constructed type-(A) family maps,
the certified global prisms, and forward-only directed rectification.
The homotopy/rectification proof is for ALL horn problems, so it does
not use admissibility to hide a missing round-trip filler. -/
noncomputable def nativeTypeACorrespondence_of_forwardRLP
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ForwardEndpointScaledHornRLP
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ForwardEndpointScaledHornRLP
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (standardTypeAScaledHornFamily
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
      (standardTypeAScaledHornFamily
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) where
  forward_admissible :=
    (nativeTypeAForwardFamilyMap B C F).admissible_preserved
  backward_admissible :=
    (nativeTypeABackwardFamilyMap B C G).admissible_preserved
  source_roundTrip_filler_reflect := by
    intro n i P
    let H := (globalDuskinRoundTripPrismRealization K).toRoundTripBoundaryHomotopy
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
    constructor
    · intro h
      exact (homotopyRectification_of_forwardEndpointRLP RB).rectify P
        (sourceRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty
        (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
        (mapScaledHornFiller_nonempty
          (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled h)
  target_roundTrip_filler_reflect := by
    intro n i Q
    let H := (globalDuskinRoundTripPrismRealization K).toRoundTripBoundaryHomotopy
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
    constructor
    · intro h
      exact (homotopyRectification_of_forwardEndpointRLP RC).rectify Q
        (targetRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty
        (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
        (mapScaledHornFiller_nonempty
          (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled h)

/-- On the normalized lifted carriers, the native type-(A) fibrancy
predicates coincide under a native coherent quasi-inverse plus two
independently provided endpoint-zero horn-cylinder lifting properties. -/
theorem liftedNativeTypeAFibrancy_iff_of_forwardRLP
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ForwardEndpointScaledHornRLP
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ForwardEndpointScaledHornRLP
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C)
      (standardTypeAScaledHornFamily
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)) ↔
    HasScaledHornFillers (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C)
      (standardTypeAScaledHornFamily
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :=
  liftedFibrancy_iff
    (nativeTypeACorrespondence_of_forwardRLP B C F G K RB RC)

/-- Final ORIGINAL, UNLIFTED native type-(A) horn-fibrancy equivalence.
Neither the B/C family maps, the lifted D correspondence, nor the native
ULift family identifications are hypotheses: all are actually
constructed. Only the genuine native quasi-inverse and the two directed
endpoint RLP properties remain as conditions. -/
theorem unliftedNativeTypeAFibrancy_iff_of_forwardRLP
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ForwardEndpointScaledHornRLP
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ForwardEndpointScaledHornRLP
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B)
      (standardTypeAScaledHornFamily (duskinNerve B) (duskinScaling B)) ↔
    HasScaledHornFillers (duskinNerve C) (duskinScaling C)
      (standardTypeAScaledHornFamily (duskinNerve C) (duskinScaling C)) := by
  have hSource :=
    nativeTypeA_fibrancy_iff.{
      max (max w₁ v₁) u₁, max (max w₂ v₂) u₂} (duskinScaling B)
  have hTarget :=
    nativeTypeA_fibrancy_iff.{
      max (max w₂ v₂) u₂, max (max w₁ v₁) u₁} (duskinScaling C)
  exact hSource.trans
    ((liftedNativeTypeAFibrancy_iff_of_forwardRLP
      B C F G K RB RC).trans hTarget.symm)

#print axioms nativeTypeAForwardFamilyMap
#print axioms nativeTypeABackwardFamilyMap
#print axioms nativeTypeACorrespondence_of_forwardRLP
#print axioms liftedNativeTypeAFibrancy_iff_of_forwardRLP
#print axioms unliftedNativeTypeAFibrancy_iff_of_forwardRLP

end KUOS.DependentOriginationNativeTypeABCDuskinDescentV1_29
