import KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82

namespace KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

universe u v w uC vC uH vH

/-!
# Correction authority refinement v2.83

Hard obstruction is relative to a supplied correction mechanism. This layer
makes that authority boundary explicit.

A narrow correction authority refines into a wider one when every parameter
admissible for the narrow authority is also admissible for the wider authority,
and both mechanisms assign the same correction effect to each parameter.

Consequently:

* correctability is monotone from narrow authority to wide authority;
* hard obstruction is antitone from wide authority to narrow authority;
* these inclusions compose, giving a preorder-like transport structure.

The generated-holonomy wrappers inherit exactly the same monotonicity. No
claim identifies hard obstruction with an intrinsic property of a defect
independent of correction authority.
-/

/-- Inclusion of correction authority. Narrow may admit fewer parameters
than Wide, while the shared parameters have the same correction effect. -/
structure CorrectionAuthorityRefinement
    {State : Type u} {Param : Type v} {D : Type w}
    (Narrow Wide : CorrectionRealization State Param D) where
  admissible_mono :
    ∀ x p, Narrow.admissible x p → Wide.admissible x p
  effect_eq :
    ∀ x p, Narrow.effect x p = Wide.effect x p

namespace CorrectionAuthorityRefinement

variable
    {State : Type u} {Param : Type v} {D : Type w}
    {Narrow Mid Wide : CorrectionRealization State Param D}

/-- Every correction available under a narrow authority remains available
under a wider authority. -/
theorem correctable_mono
    (A : CorrectionAuthorityRefinement Narrow Wide)
    {x : State} {d : D}
    (h : Narrow.CorrectableAt x d) :
    Wide.CorrectableAt x d := by
  rcases h with ⟨p, hp, heffect⟩
  refine ⟨p, A.admissible_mono x p hp, ?_⟩
  calc
    Wide.effect x p = Narrow.effect x p := (A.effect_eq x p).symm
    _ = d := heffect

/-- If even the wider authority cannot correct a defect, then no narrower
authority can correct it either. -/
theorem hardObstruction_antitone
    (A : CorrectionAuthorityRefinement Narrow Wide)
    {x : State} {d : D}
    (h : Wide.HardObstructionAt x d) :
    Narrow.HardObstructionAt x d := by
  intro hnarrow
  exact h (A.correctable_mono hnarrow)

/-- Every correction authority refines itself. -/
def refl
    (C : CorrectionRealization State Param D) :
    CorrectionAuthorityRefinement C C where
  admissible_mono := fun _ _ h => h
  effect_eq := fun _ _ => rfl

/-- Correction-authority refinement is transitive. -/
def trans
    (A₁ : CorrectionAuthorityRefinement Narrow Mid)
    (A₂ : CorrectionAuthorityRefinement Mid Wide) :
    CorrectionAuthorityRefinement Narrow Wide where
  admissible_mono := fun x p h =>
    A₂.admissible_mono x p (A₁.admissible_mono x p h)
  effect_eq := fun x p =>
    (A₁.effect_eq x p).trans (A₂.effect_eq x p)

end CorrectionAuthorityRefinement

/-- Generated-holonomy correctability is monotone under widening of correction
authority. -/
theorem generatedHolonomy_correctable_mono
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u} {Param : Type v}
    (Narrow Wide : CorrectionRealization State Param
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (A : CorrectionAuthorityRefinement Narrow Wide)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyCorrectable W R P Narrow x gamma) :
    GeneratedHolonomyCorrectable W R P Wide x gamma := by
  exact A.correctable_mono h

/-- Generated-holonomy hard obstruction is antitone under widening of
correction authority. -/
theorem generatedHolonomy_hard_antitone
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u} {Param : Type v}
    (Narrow Wide : CorrectionRealization State Param
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (A : CorrectionAuthorityRefinement Narrow Wide)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyHardObstruction W R P Wide x gamma) :
    GeneratedHolonomyHardObstruction W R P Narrow x gamma := by
  exact A.hardObstruction_antitone h

/-- An authority gap records that a defect is correctable under a wider
mechanism but remains a hard obstruction under a narrower one. -/
def GeneratedHolonomyAuthorityGap
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u} {Param : Type v}
    (Narrow Wide : CorrectionRealization State Param
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) : Prop :=
  GeneratedHolonomyCorrectable W R P Wide x gamma ∧
    GeneratedHolonomyHardObstruction W R P Narrow x gamma

end KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83
