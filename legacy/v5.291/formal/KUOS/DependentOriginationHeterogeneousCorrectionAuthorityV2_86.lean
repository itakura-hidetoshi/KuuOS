import KUOS.DependentOriginationReflexiveAuthorityGapV2_85

namespace KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

universe u v₁ v₂ v₃ w uC vC uH vH

/-!
# Heterogeneous correction authority v2.86

The v2.83 correction-authority refinement assumes a shared parameter carrier.
That is sufficient for predicate restriction, but correction mechanisms in
different contexts may expose genuinely different parameter types.

This layer replaces same-carrier inclusion by an explicit authority morphism.
A source correction parameter is transported to a target parameter, admissible
source parameters remain admissible after transport, and the realized defect
is preserved.

Correctability therefore transports covariantly along authority morphisms,
while hard obstruction transports contravariantly.  Identity and composition
are explicit, so authority transport can be chained without identifying the
parameter carriers.

No equivalence of parameter spaces is assumed, and no inverse authority map is
constructed from one-way transport.
-/

/-- A heterogeneous morphism of correction authorities. -/
structure CorrectionAuthorityHom
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (Source : CorrectionRealization State Param₁ D)
    (Target : CorrectionRealization State Param₂ D) where
  mapParam : Param₁ → Param₂
  admissible_map :
    ∀ x p, Source.admissible x p → Target.admissible x (mapParam p)
  effect_map :
    ∀ x p, Target.effect x (mapParam p) = Source.effect x p

namespace CorrectionAuthorityHom

variable
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    {C₃ : CorrectionRealization State Param₃ D}

/-- Identity authority morphism. -/
def id (C : CorrectionRealization State Param₁ D) :
    CorrectionAuthorityHom C C where
  mapParam := fun p => p
  admissible_map := fun _ _ h => h
  effect_map := fun _ _ => rfl

/-- Composition of heterogeneous correction-authority morphisms. -/
def comp
    (A : CorrectionAuthorityHom C₁ C₂)
    (B : CorrectionAuthorityHom C₂ C₃) :
    CorrectionAuthorityHom C₁ C₃ where
  mapParam := fun p => B.mapParam (A.mapParam p)
  admissible_map := fun x p hp =>
    B.admissible_map x (A.mapParam p) (A.admissible_map x p hp)
  effect_map := fun x p => by
    calc
      C₃.effect x (B.mapParam (A.mapParam p))
          = C₂.effect x (A.mapParam p) :=
        B.effect_map x (A.mapParam p)
      _ = C₁.effect x p := A.effect_map x p

/-- Correctability transports covariantly along an authority morphism. -/
theorem correctable_map
    (A : CorrectionAuthorityHom C₁ C₂)
    {x : State} {d : D}
    (h : C₁.CorrectableAt x d) :
    C₂.CorrectableAt x d := by
  rcases h with ⟨p, hp, heffect⟩
  refine ⟨A.mapParam p, A.admissible_map x p hp, ?_⟩
  exact (A.effect_map x p).trans heffect

/-- Hard obstruction transports contravariantly: if the wider target authority
cannot realize a defect, neither can a source authority mapping into it. -/
theorem hardObstruction_antitone
    (A : CorrectionAuthorityHom C₁ C₂)
    {x : State} {d : D}
    (h : C₂.HardObstructionAt x d) :
    C₁.HardObstructionAt x d := by
  intro hsource
  exact h (A.correctable_map hsource)

/-- Every same-parameter refinement from v2.83 induces a heterogeneous
authority morphism by the identity parameter map. -/
def ofRefinement
    {Param : Type v₁}
    {Narrow Wide : CorrectionRealization State Param D}
    (A : CorrectionAuthorityRefinement Narrow Wide) :
    CorrectionAuthorityHom Narrow Wide where
  mapParam := fun p => p
  admissible_map := fun x p hp => A.admissible_mono x p hp
  effect_map := fun x p => (A.effect_eq x p).symm

end CorrectionAuthorityHom

/-- Generated-holonomy correctability transports across heterogeneous
correction parameter carriers. -/
theorem generatedHolonomy_correctable_map
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
    (A : CorrectionAuthorityHom Source Target)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyCorrectable W R P Source x gamma) :
    GeneratedHolonomyCorrectable W R P Target x gamma := by
  exact A.correctable_map h

/-- Generated-holonomy hard obstruction transports contravariantly across
heterogeneous correction parameter carriers. -/
theorem generatedHolonomy_hard_antitone
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
    (A : CorrectionAuthorityHom Source Target)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyHardObstruction W R P Target x gamma) :
    GeneratedHolonomyHardObstruction W R P Source x gamma := by
  exact A.hardObstruction_antitone h

/-- Heterogeneous authority gap: a defect is correctable in a target authority
but hard in a source authority, even when the parameter carriers differ. -/
def GeneratedHolonomyHeterogeneousAuthorityGap
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
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) : Prop :=
  GeneratedHolonomyCorrectable W R P Target x gamma ∧
    GeneratedHolonomyHardObstruction W R P Source x gamma

end KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86
