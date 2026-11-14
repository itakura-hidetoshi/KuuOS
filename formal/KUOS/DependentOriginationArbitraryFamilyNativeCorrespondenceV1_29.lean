import KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29
import KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29

/-!
# Native coherent quasi-inverse descent for independently chosen scaled horn families

Canonical ULift horn transport provides a typed bridge for each original family.
For an independently chosen lifted family the additional condition is
pointwise admissibility compatibility, not an equality of differently typed
horns. This file reuses the *existing* native global prism and strict
homotopy-filler rectification to construct the lifted B/C correspondence.
No strict inverse of the normalized nerves, arbitrary admissibility
identification, or unconditional homotopy rectification is asserted.
-/

namespace KUOS.DependentOriginationArbitraryFamilyNativeCorrespondenceV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29
open KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29
open KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29

universe u v u₁ u₂ v₁ v₂ w₁ w₂

/-- A pointwise, fully typed test for a CHOSEN lifted family's admissibility.
Both predicates are applied to actual same-universe horn problems after
explicitly un-lifting the chosen problem on the canonical side. -/
theorem admissibilityCompatible_canonical_iff
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX)
    (FY : ScaledHornFamily
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)) :
    AdmissibilityCompatible
      (canonicalLiftedHornFamily.{u, v} sX FX) FY ↔
      ∀ {n : Nat} {i : Fin (n + 1)}
        (Q : ScaledHornExtensionProblem
          ((SSet.uliftFunctor.{v, u}).obj X)
          (uliftScaling.{u, v} sX) n i),
        FY.admissible Q ↔
          FX.admissible (unliftScaledHornProblem.{u, v} Q) := by
  constructor
  · intro h n i Q
    constructor
    · intro hQ
      exact h.2 Q hQ
    · intro hFX
      exact h.1 Q hFX
  · intro h
    constructor
    · intro n i Q hCanonical
      exact (h Q).2 hCanonical
    · intro n i Q hQ
      exact (h Q).1 hQ

/-- Genuine B/C correspondence transports to arbitrary same-carrier families
when their admissibility is compatible with the certified canonical families.
The round-trip filler-reflection laws are geometric, hence unchanged by
relabeling which horn problems are admissible. -/
def liftedCorrespondence_of_compatible_families
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    {CB : ScaledHornFamily
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)}
    {CC : ScaledHornFamily
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)}
    (D : LiftedDuskinFamilyCorrespondence HF HG CB CC)
    (HB : ScaledHornFamily
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C))
    (hB : AdmissibilityCompatible CB HB)
    (hC : AdmissibilityCompatible CC HC) :
    LiftedDuskinFamilyCorrespondence HF HG HB HC where
  forward_admissible := by
    intro n i P hP
    exact hC.1 (transportGlobalDuskinHornProblem HF P)
      (D.forward_admissible P (hB.2 P hP))
  backward_admissible := by
    intro n i Q hQ
    exact hB.1 (transportGlobalDuskinHornProblem HG Q)
      (D.backward_admissible Q (hC.2 Q hQ))
  source_roundTrip_filler_reflect := D.source_roundTrip_filler_reflect
  target_roundTrip_filler_reflect := D.target_roundTrip_filler_reflect

/-- Actually BUILD the lifted family correspondence without assuming an
extra D witness. The native coherent quasi-inverse supplies a genuine
global Duskin prism by v1.36; strict filler rectification and canonical
family-map preservation remain independent geometric prerequisites. -/
noncomputable def arbitraryCorrespondence_of_nativeQuasiInverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (HB : ScaledHornFamily
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C))
    (hB : AdmissibilityCompatible
      (canonicalLiftedDuskinSourceFamily B C HB₀) HB)
    (hC : AdmissibilityCompatible
      (canonicalLiftedDuskinTargetFamily B C HC₀) HC)
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
      (canonicalLiftedFullScaledDuskinMapCertificate G) HB HC :=
  liftedCorrespondence_of_compatible_families
    (canonicalCorrespondence_of_nativeQuasiInverse
      B C F G HB₀ HC₀ hForward hBackward K RB RC)
    HB HC hB hC

/-- The ORIGINAL, UNLIFTED Duskin fibrancy conclusion for two independent
universe levels and independently chosen lifted horn families. Its proof
uses the constructed native quasi-inverse correspondence above; it does
not assert global fibrancy without admissibility and rectification data. -/
theorem unliftedFibrancy_iff_of_arbitrary_nativeQuasiInverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (HB : ScaledHornFamily
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C))
    (hB : AdmissibilityCompatible
      (canonicalLiftedDuskinSourceFamily B C HB₀) HB)
    (hC : AdmissibilityCompatible
      (canonicalLiftedDuskinTargetFamily B C HC₀) HC)
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
  unliftedFibrancy_iff_of_arbitrary_lifted_families
    B C F G HB₀ HC₀ HB HC hB hC
    (arbitraryCorrespondence_of_nativeQuasiInverse
      B C F G HB₀ HC₀ HB HC hB hC hForward hBackward K RB RC)

#print axioms admissibilityCompatible_canonical_iff
#print axioms liftedCorrespondence_of_compatible_families
#print axioms arbitraryCorrespondence_of_nativeQuasiInverse
#print axioms unliftedFibrancy_iff_of_arbitrary_nativeQuasiInverse

end KUOS.DependentOriginationArbitraryFamilyNativeCorrespondenceV1_29
