import KUOS.DependentOriginationGaugeObstructionV2_66
import KUOS.DependentOriginationCorrectionBooleanBoundaryV2_95

namespace KUOS.DependentOriginationCorrectionToFactorizationV2_96

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGaugeObstructionV2_66
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionProfileRealizationV2_91
open KUOS.DependentOriginationCorrectionBooleanBoundaryV2_95

universe u v uH vH s q₁ q₂

/-!
# Correction power returns to higher-localization factorization v2.96

The v2.69--v2.95 frontier separates nontrivial generated holonomy from hard
obstruction and develops presentation-free correction-power semantics.  The
remaining Stage-I question is not whether a defect is merely nontrivial, but
whether the available correction authority can reach coherent data.

This file makes the first direct return from correction power to the existing
v2.65--v2.66 factorization obstruction.

For fixed pointwise adjoint-equivalence data `D`, the relevant correction
target is the space of v2.61 pointwise general-W choices.  A correction
authority is factorization-reaching at a state when its reachable image
intersects the zero-five-defect locus:

```text
reachable correction image
        ∩
FiveCoherenceDefectsTrivial
        ≠ ∅.
```

This condition is extensional:

* it is monotone under `CorrectionPowerLE`;
* it is invariant under `CorrectionPowerEq`;
* it is unchanged by passage to the v2.91 semantic representative.

Most importantly, a reachable zero-defect choice lies in the unique v2.66
pointwise gauge orbit and therefore yields
`CanonicalGeneralWGaugeTrivializable`, hence the genuine v2.10
`HigherLocalizationFactorization`.

The theorem does not assert that arbitrary generated-holonomy correctability
already supplies such a coherent correction.  Constructing that lift is the
next mathematical obligation.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The pointwise-choice space on which the v2.65 five-defect obstruction is
defined. -/
abbrev GeneralWChoiceSpace
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :=
  PointwiseGeneralWChoiceData (W := W) R D

/-- A correction authority reaches the coherent zero-defect locus at state
`x` when it can realize some pointwise choice whose five v2.65 coherence
obstructions all vanish. -/
def FiveDefectCorrectionReachable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s} {Param : Type q₁}
    (C : CorrectionRealization State Param (GeneralWChoiceSpace W R D))
    (x : State) : Prop :=
  ∃ L : GeneralWChoiceSpace W R D,
    C.CorrectableAt x L ∧
      FiveCoherenceDefectsTrivial W R D L

/-- Reaching the zero-five-defect locus is monotone under extensional
correction-power inclusion. -/
theorem fiveDefectCorrectionReachable_mono_of_powerLE
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s}
    {Param₁ : Type q₁} {Param₂ : Type q₂}
    (C₁ : CorrectionRealization State Param₁ (GeneralWChoiceSpace W R D))
    (C₂ : CorrectionRealization State Param₂ (GeneralWChoiceSpace W R D))
    (hpow : CorrectionPowerLE C₁ C₂)
    (x : State)
    (h : FiveDefectCorrectionReachable W R D C₁ x) :
    FiveDefectCorrectionReachable W R D C₂ x := by
  rcases h with ⟨L, hreach, hzero⟩
  exact ⟨L, hpow x L hreach, hzero⟩

/-- Equality of extensional correction power preserves exactly whether the
authority reaches the zero-five-defect locus. -/
theorem fiveDefectCorrectionReachable_iff_of_powerEq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s}
    {Param₁ : Type q₁} {Param₂ : Type q₂}
    (C₁ : CorrectionRealization State Param₁ (GeneralWChoiceSpace W R D))
    (C₂ : CorrectionRealization State Param₂ (GeneralWChoiceSpace W R D))
    (hpow : CorrectionPowerEq C₁ C₂)
    (x : State) :
    FiveDefectCorrectionReachable W R D C₁ x ↔
      FiveDefectCorrectionReachable W R D C₂ x := by
  constructor
  · exact fiveDefectCorrectionReachable_mono_of_powerLE
      W R D C₁ C₂ hpow.1 x
  · exact fiveDefectCorrectionReachable_mono_of_powerLE
      W R D C₂ C₁ hpow.2 x

/-- Passing to the canonical v2.91 semantic representative preserves the
coherent correction-to-factorization criterion exactly. -/
theorem fiveDefectCorrectionReachable_semanticRepresentative_iff
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s} {Param : Type q₁}
    (C : CorrectionRealization State Param (GeneralWChoiceSpace W R D))
    (x : State) :
    FiveDefectCorrectionReachable W R D (semanticRepresentative C) x ↔
      FiveDefectCorrectionReachable W R D C x := by
  exact
    (fiveDefectCorrectionReachable_iff_of_powerEq
      W R D C (semanticRepresentative C)
      (semanticRepresentative_powerEq C) x).symm

/-- Maximal correction power reaches the zero-five-defect locus exactly when
some zero-defect pointwise choice exists. -/
theorem fiveDefectCorrectionReachable_top_iff_exists_fiveTrivialDefects
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s}
    (x : State) :
    FiveDefectCorrectionReachable W R D
        (topCorrectionRealization
          (State := State) (D := GeneralWChoiceSpace W R D)) x ↔
      ∃ L : GeneralWChoiceSpace W R D,
        FiveCoherenceDefectsTrivial W R D L := by
  constructor
  · rintro ⟨L, _, hzero⟩
    exact ⟨L, hzero⟩
  · rintro ⟨L, hzero⟩
    refine ⟨L, ?_, hzero⟩
    apply
      (functionalProfileCorrectionRealization_correctable_iff
        (topCorrectionProfile
          (State := State) (D := GeneralWChoiceSpace W R D)) x L).2
    exact True.intro

/-- Any correction authority whose reachable image meets the zero-five-defect
locus supplies the canonical v2.66 gauge trivialization.  The gauge itself does
not have to be added as correction data: v2.66 proves that every pair of
pointwise choices already lies in the same explicit gauge orbit. -/
theorem canonicalGaugeTrivializable_of_fiveDefectCorrectionReachable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s} {Param : Type q₁}
    (C : CorrectionRealization State Param (GeneralWChoiceSpace W R D))
    (x : State)
    (h : FiveDefectCorrectionReachable W R D C x) :
    CanonicalGeneralWGaugeTrivializable W R D := by
  rcases h with ⟨L, _, hzero⟩
  exact
    ⟨L,
      pointwiseChoicesGaugeEquivalent_all
        W R D (pointwiseGeneralWChoiceData W R D) L,
      hzero⟩

/-- First direct correction-to-factorization bridge: coherent reachability of
the zero-five-defect locus is sufficient for genuine higher-localization
factorization. -/
theorem hasHigherLocalizationFactorization_of_fiveDefectCorrectionReachable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {State : Type s} {Param : Type q₁}
    (C : CorrectionRealization State Param (GeneralWChoiceSpace W R D))
    (x : State)
    (h : FiveDefectCorrectionReachable W R D C x) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_canonicalGaugeTrivializable
    W R D
    (canonicalGaugeTrivializable_of_fiveDefectCorrectionReachable
      W R D C x h)

/-- Admissibility-shaped form. Weak W-admissibility supplies the pointwise
adjoint-equivalence data, while an explicit correction authority must still
reach a zero-five-defect choice. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiveDefectCorrectionReachable
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (hR : IsHigherWAdmissible W R)
    {State : Type s} {Param : Type q₁}
    (C : CorrectionRealization State Param
      (GeneralWChoiceSpace W R
        (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)))
    (x : State)
    (h :
      FiveDefectCorrectionReachable W R
        (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) C x) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiveDefectCorrectionReachable
    W R (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) C x h

/-!
## Boundary fixed by v2.96

The correction-power frontier now reconnects to Stage-I factorization through
an explicit extensional condition:

```text
correction authority C
        |
        | reachable image at x
        v
pointwise general-W choice L
        |
        | FiveCoherenceDefectsTrivial
        v
CanonicalGeneralWGaugeTrivializable
        |
        v
HigherLocalizationFactorization.
```

Because the condition is invariant under `CorrectionPowerEq` and under the
canonical semantic representative, parameter syntax is not theorem authority.

What remains genuinely open is the generated-holonomy lift:

```text
GeneratedHolonomyCorrectable
        ?
        v
FiveDefectCorrectionReachable.
```

That implication cannot be obtained from pointwise existence alone.  It must
encode compatibility of corrections with generated composition, symmetry, and
whiskering so that loop-level corrections assemble into one coherent
zero-defect pointwise choice.
-/

end KUOS.DependentOriginationCorrectionToFactorizationV2_96
