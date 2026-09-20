import KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

namespace KUOS.DependentOriginationRestrictedCorrectionAuthorityGapV2_84

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
open KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82
open KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

universe u

/-!
# Restricted correction authority gap v2.84

The identity realization from v2.82 is deliberately maximally permissive.
This layer restricts it by an explicit predicate on correction parameters.

The restricted mechanism keeps the same effect map but admits only parameters
satisfying the supplied predicate.  It therefore refines into the wider
identity authority.  A defect excluded by the predicate is a hard obstruction
for the restricted authority while remaining correctable for the identity
authority.

Applied to the octahedral generated loop, this gives a concrete authority gap
which can coexist with the already-proved non-flatness.  Thus the status
"hard obstruction" is formally authority-relative, not an intrinsic synonym
for non-flat generated holonomy.
-/

/-- Identity correction restricted by an explicit admissibility predicate. -/
def restrictedIdentityCorrectionRealization
    {D : Type u} (Allowed : D → Prop) :
    CorrectionRealization Unit D D where
  admissible := fun _ d => Allowed d
  effect := fun _ d => d

/-- The restricted identity mechanism is a narrow correction authority inside
the unrestricted identity mechanism. -/
def restrictedIdentity_refines_identity
    {D : Type u} (Allowed : D → Prop) :
    CorrectionAuthorityRefinement
      (restrictedIdentityCorrectionRealization Allowed)
      (identityCorrectionRealization D) where
  admissible_mono := fun _ _ _ => True.intro
  effect_eq := fun _ _ => rfl

/-- For the restricted identity mechanism, hard obstruction is exactly
exclusion by the supplied admissibility predicate. -/
theorem restrictedIdentity_hard_iff_not_allowed
    {D : Type u} (Allowed : D → Prop) (d : D) :
    (restrictedIdentityCorrectionRealization Allowed).HardObstructionAt () d ↔
      ¬ Allowed d := by
  change (¬ ∃ p, Allowed p ∧ p = d) ↔ ¬ Allowed d
  constructor
  · intro h hallowed
    exact h ⟨d, hallowed, rfl⟩
  · intro h ⟨p, hp, hpd⟩
    exact h (by simpa [hpd] using hp)

/-- If an explicit restricted authority excludes the concrete generated
holonomy, then the same defect is correctable under the wider identity
authority but hard under the restricted one. -/
theorem counterGeneratedLoop_authorityGap_of_not_allowed
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (Allowed : CounterHolonomyCarrier D → Prop)
    (hnot :
      ¬ Allowed
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop)) :
    GeneratedHolonomyAuthorityGap
      allMorphisms counterSystem D
      (restrictedIdentityCorrectionRealization Allowed)
      (identityCorrectionRealization (CounterHolonomyCarrier D))
      () counterGeneratedLoop := by
  constructor
  · exact counterGeneratedLoop_correctable_of_identity D
  · change
      (restrictedIdentityCorrectionRealization Allowed).HardObstructionAt ()
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop)
    exact
      (restrictedIdentity_hard_iff_not_allowed
        Allowed
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop)).2 hnot

/-- The restricted authority used above is formally included in the wider
identity authority. -/
theorem counterRestrictedAuthority_refines_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (Allowed : CounterHolonomyCarrier D → Prop) :
    CorrectionAuthorityRefinement
      (restrictedIdentityCorrectionRealization Allowed)
      (identityCorrectionRealization (CounterHolonomyCarrier D)) :=
  restrictedIdentity_refines_identity Allowed

/-- Concrete non-flat authority gap: separatedness supplies non-flatness, while
explicit exclusion by the restricted authority supplies hard obstruction only
for that authority. -/
theorem counterGeneratedLoop_nonflat_authorityGap_of_not_allowed
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _))
    (Allowed : CounterHolonomyCarrier D → Prop)
    (hnot :
      ¬ Allowed
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop)) :
    (¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop) ∧
      GeneratedHolonomyAuthorityGap
        allMorphisms counterSystem D
        (restrictedIdentityCorrectionRealization Allowed)
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop := by
  exact ⟨
    counterGeneratedLoop_not_flat_of_separated D F hsep,
    counterGeneratedLoop_authorityGap_of_not_allowed D Allowed hnot
  ⟩

end KUOS.DependentOriginationRestrictedCorrectionAuthorityGapV2_84
