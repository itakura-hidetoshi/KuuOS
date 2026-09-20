import KUOS.DependentOriginationCorrectionImageEquivalenceV2_87

namespace KUOS.DependentOriginationCorrectionPowerSemanticsV2_88

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86
open KUOS.DependentOriginationCorrectionImageEquivalenceV2_87

universe u v₁ v₂ v₃ w uC vC uH vH

/-!
# Correction-power semantics v2.88

The v2.86-v2.87 layers still retain explicit correction-parameter
presentations. For obstruction classification, the extensional observable is
smaller: at each state, which defect values are reachable by some admissible
correction?

This layer forgets the parameter presentation and keeps only that correction
power. The resulting relation is a preorder:

* CorrectionPowerLE C₁ C₂ means every defect correctable by C₁ is also
  correctable by C₂;
* heterogeneous authority morphisms induce this order;
* hard obstruction is antitone in this order;
* mutual power inclusion gives extensional equality of correctability and hard
  obstruction, without requiring explicit parameter maps.

Thus correction-image equivalence from v2.87 is sufficient but not necessary
for observational equivalence at the defect-classification level.
-/

/-- Extensional inclusion of correction power. Parameter carriers may differ
and no map between them is part of this semantic relation. -/
def CorrectionPowerLE
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) : Prop :=
  ∀ x d, C₁.CorrectableAt x d → C₂.CorrectableAt x d

namespace CorrectionPowerLE

variable
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    {C₃ : CorrectionRealization State Param₃ D}

/-- Correction power includes itself. -/
theorem refl (C : CorrectionRealization State Param₁ D) :
    CorrectionPowerLE C C :=
  fun _ _ h => h

/-- Extensional correction-power inclusion composes. -/
theorem trans
    (h₁₂ : CorrectionPowerLE C₁ C₂)
    (h₂₃ : CorrectionPowerLE C₂ C₃) :
    CorrectionPowerLE C₁ C₃ :=
  fun x d h => h₂₃ x d (h₁₂ x d h)

/-- Every heterogeneous authority morphism induces correction-power
inclusion. -/
theorem ofAuthorityHom
    (A : CorrectionAuthorityHom C₁ C₂) :
    CorrectionPowerLE C₁ C₂ :=
  fun _ _ h => A.correctable_map h

/-- Hard obstruction is antitone with respect to extensional correction
power. -/
theorem hardObstruction_antitone
    (hpow : CorrectionPowerLE C₁ C₂)
    {x : State} {d : D}
    (h : C₂.HardObstructionAt x d) :
    C₁.HardObstructionAt x d := by
  intro h₁
  exact h (hpow x d h₁)

end CorrectionPowerLE

/-- Two correction mechanisms have the same observable correction power when
each one's correctable defects are included in the other's. -/
def CorrectionPowerEq
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) : Prop :=
  CorrectionPowerLE C₁ C₂ ∧ CorrectionPowerLE C₂ C₁

namespace CorrectionPowerEq

variable
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    {C₃ : CorrectionRealization State Param₃ D}

/-- Equality of correction power is reflexive. -/
theorem refl (C : CorrectionRealization State Param₁ D) :
    CorrectionPowerEq C C :=
  ⟨CorrectionPowerLE.refl C, CorrectionPowerLE.refl C⟩

/-- Equality of correction power is symmetric. -/
theorem symm
    (h : CorrectionPowerEq C₁ C₂) :
    CorrectionPowerEq C₂ C₁ :=
  ⟨h.2, h.1⟩

/-- Equality of correction power is transitive. -/
theorem trans
    (h₁₂ : CorrectionPowerEq C₁ C₂)
    (h₂₃ : CorrectionPowerEq C₂ C₃) :
    CorrectionPowerEq C₁ C₃ :=
  ⟨
    CorrectionPowerLE.trans h₁₂.1 h₂₃.1,
    CorrectionPowerLE.trans h₂₃.2 h₁₂.2
  ⟩

/-- Explicit correction-image equivalence implies extensional equality of
correction power. -/
theorem ofImageEquivalence
    (E : CorrectionImageEquivalence C₁ C₂) :
    CorrectionPowerEq C₁ C₂ :=
  ⟨
    CorrectionPowerLE.ofAuthorityHom E.forward,
    CorrectionPowerLE.ofAuthorityHom E.backward
  ⟩

/-- Correctability is exactly invariant under equality of correction power. -/
theorem correctable_iff
    (hpow : CorrectionPowerEq C₁ C₂)
    {x : State} {d : D} :
    C₁.CorrectableAt x d ↔ C₂.CorrectableAt x d :=
  ⟨hpow.1 x d, hpow.2 x d⟩

/-- Hard obstruction is exactly invariant under equality of correction power. -/
theorem hardObstruction_iff
    (hpow : CorrectionPowerEq C₁ C₂)
    {x : State} {d : D} :
    C₁.HardObstructionAt x d ↔ C₂.HardObstructionAt x d := by
  constructor
  · exact CorrectionPowerLE.hardObstruction_antitone hpow.2
  · exact CorrectionPowerLE.hardObstruction_antitone hpow.1

end CorrectionPowerEq

/-- Generated-holonomy correctability is monotone under extensional correction
power inclusion, with no parameter map required. -/
theorem generatedHolonomy_correctable_mono_of_powerLE
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
    (hpow : CorrectionPowerLE C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyCorrectable W R P C₁ x gamma) :
    GeneratedHolonomyCorrectable W R P C₂ x gamma :=
  hpow x (generatedHolonomy W R P gamma) h

/-- Generated-holonomy hard obstruction is antitone under extensional
correction-power inclusion. -/
theorem generatedHolonomy_hard_antitone_of_powerLE
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
    (hpow : CorrectionPowerLE C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : GeneratedHolonomyHardObstruction W R P C₂ x gamma) :
    GeneratedHolonomyHardObstruction W R P C₁ x gamma :=
  CorrectionPowerLE.hardObstruction_antitone hpow h

/-- A strict heterogeneous authority gap is impossible when the two
authorities have equal extensional correction power. -/
theorem no_generatedHolonomy_authorityGap_of_powerEq
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
    (hpow : CorrectionPowerEq C₁ C₂)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) :
    ¬ GeneratedHolonomyHeterogeneousAuthorityGap
      W R P C₁ C₂ x gamma := by
  intro hgap
  exact hgap.2 (hpow.2 x
    (generatedHolonomy W R P gamma) hgap.1)

end KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
