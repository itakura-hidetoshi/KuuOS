import KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86

namespace KUOS.DependentOriginationMutualCorrectionAuthorityV2_87

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86

universe u v₁ v₂ w uC vC uH vH

/-!
# Mutual correction-authority transport v2.87

One-way authority morphisms from v2.86 enlarge the available correction power:
correctability transports forward and hard obstruction transports backward.

This layer studies the exact boundary where two correction mechanisms can
transport admissible realizations in both directions. No inverse equations on
parameter maps are required. Mutual transport is weaker than an isomorphism
of parameter spaces, but it is already sufficient to force agreement on the
observable correctable and hard-obstruction predicates.

For generated holonomy, mutual transport therefore rules out an authority gap
between the two mechanisms.
-/

/-- Two correction authorities are mutually transportable when each maps
admissible defect realizations into the other. The parameter maps need not be
set-theoretic inverses. -/
structure MutualCorrectionAuthority
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) where
  forward : CorrectionAuthorityHom C₁ C₂
  backward : CorrectionAuthorityHom C₂ C₁

namespace MutualCorrectionAuthority

variable
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}

/-- Mutual authority transport makes correctability extensional between the
two mechanisms. -/
theorem correctable_iff
    (M : MutualCorrectionAuthority C₁ C₂)
    {x : State} {d : D} :
    C₁.CorrectableAt x d ↔ C₂.CorrectableAt x d := by
  constructor
  · exact fun h => M.forward.correctable_map h
  · exact fun h => M.backward.correctable_map h

/-- Mutual authority transport also makes hard-obstruction status extensional. -/
theorem hardObstruction_iff
    (M : MutualCorrectionAuthority C₁ C₂)
    {x : State} {d : D} :
    C₁.HardObstructionAt x d ↔ C₂.HardObstructionAt x d := by
  constructor
  · intro h₁
    exact M.backward.hardObstruction_antitone h₁
  · intro h₂
    exact M.forward.hardObstruction_antitone h₂

/-- Every authority is mutually transportable with itself. -/
def refl (C : CorrectionRealization State Param₁ D) :
    MutualCorrectionAuthority C C where
  forward := CorrectionAuthorityHom.id C
  backward := CorrectionAuthorityHom.id C

/-- Mutual transport is symmetric. -/
def symm
    (M : MutualCorrectionAuthority C₁ C₂) :
    MutualCorrectionAuthority C₂ C₁ where
  forward := M.backward
  backward := M.forward

end MutualCorrectionAuthority

/-- Generated-holonomy correctability agrees under mutual correction-authority
transport, even when the parameter carriers differ. -/
theorem generatedHolonomy_correctable_iff_of_mutual
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
    (M : MutualCorrectionAuthority C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyCorrectable W R P C₁ x gamma ↔
      GeneratedHolonomyCorrectable W R P C₂ x gamma := by
  exact M.correctable_iff

/-- Generated-holonomy hard-obstruction status agrees under mutual authority
transport. -/
theorem generatedHolonomy_hard_iff_of_mutual
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
    (M : MutualCorrectionAuthority C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyHardObstruction W R P C₁ x gamma ↔
      GeneratedHolonomyHardObstruction W R P C₂ x gamma := by
  exact M.hardObstruction_iff

/-- A heterogeneous authority gap cannot occur between mutually transportable
correction mechanisms. -/
theorem no_generatedHolonomy_authorityGap_of_mutual
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂}
    (Source : CorrectionRealization State Param₁
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (Target : CorrectionRealization State Param₂
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (M : MutualCorrectionAuthority Source Target)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    ¬ GeneratedHolonomyHeterogeneousAuthorityGap
      W R P Source Target x gamma := by
  intro hgap
  have hsource :
      GeneratedHolonomyCorrectable W R P Source x gamma :=
    M.backward.correctable_map hgap.1
  exact hgap.2 hsource

end KUOS.DependentOriginationMutualCorrectionAuthorityV2_87
