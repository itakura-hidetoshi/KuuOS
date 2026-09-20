import KUOS.DependentOriginationCorrectionProfileRealizationV2_91

namespace KUOS.DependentOriginationCorrectionSemanticReflectionV2_92

open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86
open KUOS.DependentOriginationCorrectionImageEquivalenceV2_87
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
open KUOS.DependentOriginationCorrectionProfileRealizationV2_91

universe u v₁ v₂ w

/-!
# Correction semantic reflection v2.92

The v2.91 functional representative realizes the presentation-free
reachability profile while preserving state-dependent effects.

This layer proves the converse structural bridge: extensional correction-power
inclusion can always be lifted to an explicit authority morphism after both
mechanisms are replaced by their semantic representatives.

Hence the semantic representatives reflect the correction-power preorder:

* C₁ ≤ C₂ iff there exists an authority morphism Rep(C₁) → Rep(C₂);
* C₁ and C₂ have equal correction power iff their representatives admit
  explicit authority morphisms in both directions.

The construction uses the identity map on function-valued parameters. This is
possible precisely because semantic representatives share the canonical
parameter carrier State → D.

No claim is made that a power inclusion lifts to a parameter map between the
original presentations.
-/

/-- Extensional correction-power inclusion lifts canonically to an explicit
authority morphism between semantic representatives. -/
def semanticRepresentativeHomOfPowerLE
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (hpow : CorrectionPowerLE C₁ C₂) :
    CorrectionAuthorityHom
      (semanticRepresentative C₁)
      (semanticRepresentative C₂) where
  mapParam := fun f => f
  admissible_map := by
    intro x f hf
    change C₁.CorrectableAt x (f x) at hf
    change C₂.CorrectableAt x (f x)
    exact hpow x (f x) hf
  effect_map := by
    intro x f
    rfl

/-- Equality of extensional correction power upgrades to explicit
correction-image equivalence between semantic representatives. -/
def semanticRepresentativeImageEquivalenceOfPowerEq
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (hpow : CorrectionPowerEq C₁ C₂) :
    CorrectionImageEquivalence
      (semanticRepresentative C₁)
      (semanticRepresentative C₂) where
  forward := semanticRepresentativeHomOfPowerLE hpow.1
  backward := semanticRepresentativeHomOfPowerLE hpow.2

/-- The correction-power preorder is exactly reflected by existence of an
authority morphism between canonical semantic representatives. -/
theorem correctionPowerLE_iff_nonempty_semanticRepresentativeHom
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE C₁ C₂ ↔
      Nonempty
        (CorrectionAuthorityHom
          (semanticRepresentative C₁)
          (semanticRepresentative C₂)) := by
  constructor
  · intro hpow
    exact ⟨semanticRepresentativeHomOfPowerLE hpow⟩
  · rintro ⟨A⟩
    have h₁ :
        CorrectionPowerLE C₁ (semanticRepresentative C₁) :=
      (semanticRepresentative_powerEq C₁).1
    have hA :
        CorrectionPowerLE
          (semanticRepresentative C₁)
          (semanticRepresentative C₂) :=
      CorrectionPowerLE.ofAuthorityHom A
    have h₂ :
        CorrectionPowerLE (semanticRepresentative C₂) C₂ :=
      (semanticRepresentative_powerEq C₂).2
    exact CorrectionPowerLE.trans h₁
      (CorrectionPowerLE.trans hA h₂)

/-- Equality of correction power is exactly reflected by explicit
correction-image equivalence between canonical semantic representatives. -/
theorem correctionPowerEq_iff_nonempty_semanticRepresentativeImageEquivalence
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerEq C₁ C₂ ↔
      Nonempty
        (CorrectionImageEquivalence
          (semanticRepresentative C₁)
          (semanticRepresentative C₂)) := by
  constructor
  · intro hpow
    exact ⟨semanticRepresentativeImageEquivalenceOfPowerEq hpow⟩
  · rintro ⟨E⟩
    have h₁ : CorrectionPowerEq C₁ (semanticRepresentative C₁) :=
      semanticRepresentative_powerEq C₁
    have hE :
        CorrectionPowerEq
          (semanticRepresentative C₁)
          (semanticRepresentative C₂) :=
      CorrectionPowerEq.ofImageEquivalence E
    have h₂ : CorrectionPowerEq (semanticRepresentative C₂) C₂ :=
      CorrectionPowerEq.symm (semanticRepresentative_powerEq C₂)
    exact CorrectionPowerEq.trans h₁
      (CorrectionPowerEq.trans hE h₂)

/-- An original heterogeneous authority morphism descends to a canonical
semantic-representative morphism through its induced correction-power
inclusion. -/
def semanticRepresentativeHomOfAuthorityHom
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (A : CorrectionAuthorityHom C₁ C₂) :
    CorrectionAuthorityHom
      (semanticRepresentative C₁)
      (semanticRepresentative C₂) :=
  semanticRepresentativeHomOfPowerLE
    (CorrectionPowerLE.ofAuthorityHom A)

end KUOS.DependentOriginationCorrectionSemanticReflectionV2_92
