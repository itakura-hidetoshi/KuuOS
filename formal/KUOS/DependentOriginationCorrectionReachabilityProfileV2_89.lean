import KUOS.DependentOriginationCorrectionPowerSemanticsV2_88

namespace KUOS.DependentOriginationCorrectionReachabilityProfileV2_89

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88

universe u v₁ v₂ w uC vC uH vH

/-!
# Correction reachability profile v2.89

The v2.88 preorder is already extensional, but it is useful to expose the
actual semantic object on which that preorder acts.

For a correction mechanism C, its reachability profile records, for every
state x and defect d, whether d lies in the admissible correction image at x.
This profile forgets the parameter carrier completely.

The main identification is exact:

* correction-power inclusion is pointwise implication of reachability;
* equality of correction power is equality of reachability profiles;
* hard obstruction is simply non-reachability.

This gives a presentation-free semantic carrier for the authority theory
developed in v2.83-v2.88.
-/

/-- Presentation-free observable correction image at every state. -/
def CorrectionReachabilityProfile
    {State : Type u} {Param : Type v₁} {D : Type w}
    (C : CorrectionRealization State Param D) :
    State → D → Prop :=
  fun x d => C.CorrectableAt x d

/-- Correction-power inclusion is exactly pointwise implication between
reachability profiles. -/
theorem correctionPowerLE_iff_reachability
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE C₁ C₂ ↔
      ∀ x d,
        CorrectionReachabilityProfile C₁ x d →
        CorrectionReachabilityProfile C₂ x d :=
  Iff.rfl

/-- Equality of correction power is equivalent to pointwise logical
equivalence of reachability. -/
theorem correctionPowerEq_iff_reachability_iff
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerEq C₁ C₂ ↔
      ∀ x d,
        CorrectionReachabilityProfile C₁ x d ↔
        CorrectionReachabilityProfile C₂ x d := by
  constructor
  · intro hpow x d
    exact CorrectionPowerEq.correctable_iff hpow
  · intro h
    constructor
    · intro x d hd
      exact (h x d).1 hd
    · intro x d hd
      exact (h x d).2 hd

/-- Equality of correction power is exactly equality of the presentation-free
reachability profiles. -/
theorem correctionPowerEq_iff_profile_eq
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerEq C₁ C₂ ↔
      CorrectionReachabilityProfile C₁ =
        CorrectionReachabilityProfile C₂ := by
  constructor
  · intro hpow
    funext x d
    apply propext
    exact CorrectionPowerEq.correctable_iff hpow
  · intro hprofile
    apply (correctionPowerEq_iff_reachability_iff C₁ C₂).2
    intro x d
    have hxd :
        CorrectionReachabilityProfile C₁ x d =
          CorrectionReachabilityProfile C₂ x d :=
      congrFun (congrFun hprofile x) d
    exact Iff.of_eq hxd

/-- A heterogeneous authority morphism induces pointwise inclusion of the
presentation-free reachability profiles. -/
theorem reachability_mono_of_authorityHom
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (A :
      KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86.CorrectionAuthorityHom
        C₁ C₂)
    {x : State} {d : D}
    (h : CorrectionReachabilityProfile C₁ x d) :
    CorrectionReachabilityProfile C₂ x d :=
  A.correctable_map h

/-- Hard obstruction is exactly the complement of the reachability profile. -/
theorem hardObstruction_iff_not_reachable
    {State : Type u} {Param : Type v₁} {D : Type w}
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) :
    C.HardObstructionAt x d ↔
      ¬ CorrectionReachabilityProfile C x d :=
  Iff.rfl

/-- Reachability of an evaluated generated holonomy is definitionally the
generated-holonomy correctability predicate. -/
theorem generatedHolonomy_correctable_iff_reachable
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u} {Param : Type v₁}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyCorrectable W R P C x gamma ↔
      CorrectionReachabilityProfile C x
        (generatedHolonomy W R P gamma) :=
  Iff.rfl

/-- Generated-holonomy hard obstruction is exactly exclusion of its evaluated
holonomy from the reachability profile. -/
theorem generatedHolonomy_hard_iff_not_reachable
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u} {Param : Type v₁}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    GeneratedHolonomyHardObstruction W R P C x gamma ↔
      ¬ CorrectionReachabilityProfile C x
        (generatedHolonomy W R P gamma) :=
  Iff.rfl

end KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
