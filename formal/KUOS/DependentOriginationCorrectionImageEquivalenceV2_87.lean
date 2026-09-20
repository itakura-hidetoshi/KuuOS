import KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86

namespace KUOS.DependentOriginationCorrectionImageEquivalenceV2_87

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86

universe u v₁ v₂ v₃ w uC vC uH vH

/-!
# Correction-image equivalence v2.87

The v2.86 layer transports correction authority across genuinely different
parameter carriers.  Parameter representation itself should not change the
classification of a defect whenever the two authorities can transport
admissible realizations in both directions.

This layer therefore uses a weak image-equivalence notion: one authority
morphism in each direction.  No inverse law on parameters is required.  The
resulting theorem is extensional at the defect level:

* correctability is equivalent under mutual transport;
* hard obstruction is equivalent under mutual transport;
* a strict authority gap is impossible between image-equivalent authorities.

Thus obstruction classification depends on the reachable correction image,
not on a chosen presentation of correction parameters.
-/

/-- Two correction authorities are image-equivalent when admissible
realizations transport in both directions, possibly through different
parameter carriers. -/
structure CorrectionImageEquivalence
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) where
  forward : CorrectionAuthorityHom C₁ C₂
  backward : CorrectionAuthorityHom C₂ C₁

namespace CorrectionImageEquivalence

variable
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    {C₃ : CorrectionRealization State Param₃ D}

/-- Correctability depends only on the mutually reachable correction image. -/
theorem correctable_iff
    (E : CorrectionImageEquivalence C₁ C₂)
    {x : State} {d : D} :
    C₁.CorrectableAt x d ↔ C₂.CorrectableAt x d := by
  constructor
  · exact E.forward.correctable_map
  · exact E.backward.correctable_map

/-- Hard obstruction is invariant under correction-image equivalence. -/
theorem hardObstruction_iff
    (E : CorrectionImageEquivalence C₁ C₂)
    {x : State} {d : D} :
    C₁.HardObstructionAt x d ↔ C₂.HardObstructionAt x d := by
  constructor
  · exact E.backward.hardObstruction_antitone
  · exact E.forward.hardObstruction_antitone

/-- Every correction authority is image-equivalent to itself. -/
def refl (C : CorrectionRealization State Param₁ D) :
    CorrectionImageEquivalence C C where
  forward := CorrectionAuthorityHom.id C
  backward := CorrectionAuthorityHom.id C

/-- Correction-image equivalence is symmetric by exchanging the two authority
morphisms. -/
def symm
    (E : CorrectionImageEquivalence C₁ C₂) :
    CorrectionImageEquivalence C₂ C₁ where
  forward := E.backward
  backward := E.forward

/-- Correction-image equivalence composes. -/
def trans
    (E₁₂ : CorrectionImageEquivalence C₁ C₂)
    (E₂₃ : CorrectionImageEquivalence C₂ C₃) :
    CorrectionImageEquivalence C₁ C₃ where
  forward := CorrectionAuthorityHom.comp E₁₂.forward E₂₃.forward
  backward := CorrectionAuthorityHom.comp E₂₃.backward E₁₂.backward

end CorrectionImageEquivalence

/-- Generated-holonomy correctability is invariant under a change of correction
parameter presentation whenever the correction images are mutually
transportable. -/
theorem generatedHolonomy_correctable_iff_of_imageEquivalence
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂}
    (C₁ : CorrectionRealization State Param₁
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (C₂ : CorrectionRealization State Param₂
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (E : CorrectionImageEquivalence C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyCorrectable W R P C₁ x gamma ↔
      GeneratedHolonomyCorrectable W R P C₂ x gamma := by
  exact E.correctable_iff

/-- Generated-holonomy hard obstruction is likewise invariant under
correction-image equivalence. -/
theorem generatedHolonomy_hard_iff_of_imageEquivalence
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂}
    (C₁ : CorrectionRealization State Param₁
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (C₂ : CorrectionRealization State Param₂
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (E : CorrectionImageEquivalence C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyHardObstruction W R P C₁ x gamma ↔
      GeneratedHolonomyHardObstruction W R P C₂ x gamma := by
  exact E.hardObstruction_iff

/-- A strict heterogeneous authority gap cannot occur between authorities with
the same reachable correction image. -/
theorem no_generatedHolonomy_authorityGap_of_imageEquivalence
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂}
    (C₁ : CorrectionRealization State Param₁
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (C₂ : CorrectionRealization State Param₂
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (E : CorrectionImageEquivalence C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    ¬ GeneratedHolonomyHeterogeneousAuthorityGap
      W R P C₁ C₂ x gamma := by
  intro hgap
  have hsource :
      GeneratedHolonomyCorrectable W R P C₁ x gamma :=
    (generatedHolonomy_correctable_iff_of_imageEquivalence
      W R P C₁ C₂ E x gamma).2 hgap.1
  exact hgap.2 hsource

end KUOS.DependentOriginationCorrectionImageEquivalenceV2_87
