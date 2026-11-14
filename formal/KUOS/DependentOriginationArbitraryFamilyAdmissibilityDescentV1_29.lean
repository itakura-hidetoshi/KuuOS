import KUOS.DependentOriginationCanonicalIndependentUniverseFamilyCorrespondenceV1_29

/-!
# Arbitrary-family admissibility conditions for genuine unlifted Duskin descent

The canonical ULift presentation already reflects every scaled horn problem and
filler across independent universes. That does NOT identify the admissibility
predicate of an unrelated lifted family with the canonical predicate.

Here we make the missing condition precise: inclusion of admissible horn
problems suffices for one-way fibrancy descent, while two-way inclusion supplies
an actual same-carrier presentation equivalence. The final Duskin result
combines these proved bridges with an explicitly provided lifted B/C family
correspondence. Nothing here asserts that correspondence merely from F and G.
-/

namespace KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30
open KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29

universe u v u₁ u₂ v₁ v₂ w₁ w₂

/-- Every horn admissible for F is also admissible for G, on the SAME
scaled simplicial carrier, at every horn index. -/
def AdmissibilitySubfamily
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (F G : ScaledHornFamily X sX) : Prop :=
  ∀ {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i),
    F.admissible P → G.admissible P

/-- Two independent, explicitly checked inclusions; neither direction is
silently inferred from model equivalence or from filler existence. -/
def AdmissibilityCompatible
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (F G : ScaledHornFamily X sX) : Prop :=
  AdmissibilitySubfamily F G ∧ AdmissibilitySubfamily G F

/-- A weaker family of horn obligations inherits fibrancy from the stronger
one. The direction of inclusion is intentionally contravariant. -/
theorem hasScaledHornFillers_of_subfamily
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (F G : ScaledHornFamily X sX)
    (h : AdmissibilitySubfamily G F)
    (hF : HasScaledHornFillers X sX F) :
    HasScaledHornFillers X sX G := by
  refine ⟨?_⟩
  intro n i P hP h0 hi
  exact hF.fill P (h P hP) h0 hi

/-- A pointwise two-way admissibility certificate induces a full
same-carrier horn-presentation equivalence, with identity problem maps. -/
def sameCarrierPresentationEquivalence
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (F G : ScaledHornFamily X sX)
    (h : AdmissibilityCompatible F G) :
    ScaledHornPresentationEquivalence F G where
  forward := fun P => P
  backward := fun Q => Q
  forward_admissible := by
    intro n i P hP
    exact h.1 P hP
  backward_admissible := by
    intro n i Q hQ
    exact h.2 Q hQ
  forward_filler := by
    intro n i P hP
    exact hP
  backward_filler := by
    intro n i Q hQ
    exact hQ
  forward_backward_filler_equiv := by
    intro n i Q
    exact Iff.rfl
  backward_forward_filler_equiv := by
    intro n i P
    exact Iff.rfl

/-- A chosen family has exactly the same fibrancy obligations as the
canonical family when and only when the two inclusions are supplied. -/
theorem sameCarrierFibrancy_iff
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (F G : ScaledHornFamily X sX)
    (h : AdmissibilityCompatible F G) :
    HasScaledHornFillers X sX F ↔ HasScaledHornFillers X sX G :=
  hasScaledHornFillers_iff (sameCarrierPresentationEquivalence F G h)

/-- The independent-universe ULift bridge extends to an ARBITRARY chosen
lifted family provided its horn admissibility is checked in both directions
against the canonically transported original family. -/
theorem arbitraryCrossUniverseFibrancy_iff
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX)
    (FY : ScaledHornFamily ((SSet.uliftFunctor.{v, u}).obj X)
      (uliftScaling.{u, v} sX))
    (h : AdmissibilityCompatible
      (canonicalLiftedHornFamily.{u, v} sX FX) FY) :
    HasScaledHornFillers X sX FX ↔
      HasScaledHornFillers ((SSet.uliftFunctor.{v, u}).obj X)
        (uliftScaling.{u, v} sX) FY :=
  (canonicalCrossUniverseFibrancy_iff.{u, v} sX FX).trans
    (sameCarrierFibrancy_iff
      (canonicalLiftedHornFamily.{u, v} sX FX) FY h)

/-- Directional descent needs only two inclusions: lifted B may impose
fewer obligations than canonical B, while canonical C must impose no more
than lifted C. The bidirectional geometric B/C correspondence D is still
an independent hypothesis. -/
theorem unliftedFibrancy_forward_of_family_inclusions
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C))
    (hB : AdmissibilitySubfamily HB
      (canonicalLiftedDuskinSourceFamily B C HB₀))
    (hC : AdmissibilitySubfamily
      (canonicalLiftedDuskinTargetFamily B C HC₀) HC)
    (D : LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G) HB HC)
    (hOriginalB : HasScaledHornFillers (duskinNerve B)
      (duskinScaling B) HB₀) :
    HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  have hCanonicalB := 
    (sourceFibrancy_iff_canonicalCrossUniverse B C HB₀).mp hOriginalB
  have hLiftedB := hasScaledHornFillers_of_subfamily
    (canonicalLiftedDuskinSourceFamily B C HB₀) HB hB hCanonicalB
  have hLiftedC := (liftedFibrancy_iff D).mp hLiftedB
  have hCanonicalC := hasScaledHornFillers_of_subfamily
    HC (canonicalLiftedDuskinTargetFamily B C HC₀) hC hLiftedC
  exact (targetFibrancy_iff_canonicalCrossUniverse B C HC₀).mpr hCanonicalC

/-- General ORIGINAL, unlifted B/C fibrancy equivalence with independently
chosen lifted families. Pointwise admissibility compatibility on BOTH sides,
plus an actual lifted family correspondence, are the exposed hypotheses.
No canonical-family identification or missing rectification is assumed. -/
theorem unliftedFibrancy_iff_of_arbitrary_lifted_families
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C))
    (hB : AdmissibilityCompatible
      (canonicalLiftedDuskinSourceFamily B C HB₀) HB)
    (hC : AdmissibilityCompatible
      (canonicalLiftedDuskinTargetFamily B C HC₀) HC)
    (D : LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G) HB HC) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  have hSource :=
    (sourceFibrancy_iff_canonicalCrossUniverse B C HB₀).trans
      (sameCarrierFibrancy_iff
        (canonicalLiftedDuskinSourceFamily B C HB₀) HB hB)
  have hTarget :=
    (targetFibrancy_iff_canonicalCrossUniverse B C HC₀).trans
      (sameCarrierFibrancy_iff
        (canonicalLiftedDuskinTargetFamily B C HC₀) HC hC)
  exact hSource.trans ((liftedFibrancy_iff D).trans hTarget.symm)

#print axioms hasScaledHornFillers_of_subfamily
#print axioms sameCarrierPresentationEquivalence
#print axioms sameCarrierFibrancy_iff
#print axioms arbitraryCrossUniverseFibrancy_iff
#print axioms unliftedFibrancy_forward_of_family_inclusions
#print axioms unliftedFibrancy_iff_of_arbitrary_lifted_families

end KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29
