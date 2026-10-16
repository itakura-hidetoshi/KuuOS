import KUOS.DependentOriginationCorrectionSemanticReflectionV2_92

namespace KUOS.DependentOriginationCorrectionPowerLatticeV2_93

open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
open KUOS.DependentOriginationStrictCorrectionPowerV2_90
open KUOS.DependentOriginationCorrectionProfileRealizationV2_91

universe u v₁ v₂ v₃ w

/-!
# Correction-power lattice v2.93

Once correction authority has descended to its reachability profile, finite
combinations of authorities become ordinary logical operations on reachable
defects.

This layer realizes the pointwise disjunction and conjunction of two
reachability profiles as canonical correction mechanisms. They satisfy the
expected universal properties for the correction-power preorder:

* join is the least authority power containing both inputs;
* meet is the greatest authority power contained in both inputs.

No parameter-level coproduct or product is required. The construction occurs
entirely at the semantic reachability level and is then realized by the
functional representative from v2.91.
-/

/-- Pointwise union of the reachable defects of two correction mechanisms. -/
def joinCorrectionProfile
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    State → D → Prop :=
  fun x d =>
    CorrectionReachabilityProfile C₁ x d ∨
      CorrectionReachabilityProfile C₂ x d

/-- Pointwise intersection of the reachable defects of two correction
mechanisms. -/
def meetCorrectionProfile
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    State → D → Prop :=
  fun x d =>
    CorrectionReachabilityProfile C₁ x d ∧
      CorrectionReachabilityProfile C₂ x d

/-- Canonical realization of the join correction power. -/
def joinCorrectionRealization
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (joinCorrectionProfile C₁ C₂)

/-- Canonical realization of the meet correction power. -/
def meetCorrectionRealization
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (meetCorrectionProfile C₁ C₂)

/-- Left input embeds into the join correction power. -/
theorem le_join_left
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE C₁ (joinCorrectionRealization C₁ C₂) := by
  intro x d h
  apply (functionalProfileCorrectionRealization_correctable_iff
    (joinCorrectionProfile C₁ C₂) x d).2
  exact Or.inl h

/-- Right input embeds into the join correction power. -/
theorem le_join_right
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE C₂ (joinCorrectionRealization C₁ C₂) := by
  intro x d h
  apply (functionalProfileCorrectionRealization_correctable_iff
    (joinCorrectionProfile C₁ C₂) x d).2
  exact Or.inr h

/-- The semantic join is the least upper bound for correction power. -/
theorem join_least
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D)
    (C₃ : CorrectionRealization State Param₃ D)
    (h₁ : CorrectionPowerLE C₁ C₃)
    (h₂ : CorrectionPowerLE C₂ C₃) :
    CorrectionPowerLE (joinCorrectionRealization C₁ C₂) C₃ := by
  intro x d hjoin
  have hor :
      CorrectionReachabilityProfile C₁ x d ∨
        CorrectionReachabilityProfile C₂ x d :=
    (functionalProfileCorrectionRealization_correctable_iff
      (joinCorrectionProfile C₁ C₂) x d).1 hjoin
  rcases hor with h | h
  · exact h₁ x d h
  · exact h₂ x d h

/-- The meet correction power embeds into the left input. -/
theorem meet_le_left
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE (meetCorrectionRealization C₁ C₂) C₁ := by
  intro x d hmeet
  have hand :
      CorrectionReachabilityProfile C₁ x d ∧
        CorrectionReachabilityProfile C₂ x d :=
    (functionalProfileCorrectionRealization_correctable_iff
      (meetCorrectionProfile C₁ C₂) x d).1 hmeet
  exact hand.1

/-- The meet correction power embeds into the right input. -/
theorem meet_le_right
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) :
    CorrectionPowerLE (meetCorrectionRealization C₁ C₂) C₂ := by
  intro x d hmeet
  have hand :
      CorrectionReachabilityProfile C₁ x d ∧
        CorrectionReachabilityProfile C₂ x d :=
    (functionalProfileCorrectionRealization_correctable_iff
      (meetCorrectionProfile C₁ C₂) x d).1 hmeet
  exact hand.2

/-- The semantic meet is the greatest lower bound for correction power. -/
theorem meet_greatest
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂} {Param₃ : Type v₃}
    {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D)
    (C₃ : CorrectionRealization State Param₃ D)
    (h₁ : CorrectionPowerLE C₃ C₁)
    (h₂ : CorrectionPowerLE C₃ C₂) :
    CorrectionPowerLE C₃ (meetCorrectionRealization C₁ C₂) := by
  intro x d h
  apply (functionalProfileCorrectionRealization_correctable_iff
    (meetCorrectionProfile C₁ C₂) x d).2
  exact ⟨h₁ x d h, h₂ x d h⟩

/-- Correctability for the meet is exactly simultaneous correctability by both
input authorities. -/
theorem meet_correctable_iff
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D)
    (x : State) (d : D) :
    (meetCorrectionRealization C₁ C₂).CorrectableAt x d ↔
      C₁.CorrectableAt x d ∧ C₂.CorrectableAt x d := by
  exact functionalProfileCorrectionRealization_correctable_iff
    (meetCorrectionProfile C₁ C₂) x d

/-- A defect is hard for the join exactly when it is hard for both input
authorities. -/
theorem join_hardObstruction_iff
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D)
    (x : State) (d : D) :
    (joinCorrectionRealization C₁ C₂).HardObstructionAt x d ↔
      C₁.HardObstructionAt x d ∧ C₂.HardObstructionAt x d := by
  constructor
  · intro hjoin
    constructor
    · intro h₁
      exact hjoin (le_join_left C₁ C₂ x d h₁)
    · intro h₂
      exact hjoin (le_join_right C₁ C₂ x d h₂)
  · rintro ⟨h₁, h₂⟩ hjoin
    have hor :
        CorrectionReachabilityProfile C₁ x d ∨
          CorrectionReachabilityProfile C₂ x d :=
      (functionalProfileCorrectionRealization_correctable_iff
        (joinCorrectionProfile C₁ C₂) x d).1 hjoin
    rcases hor with h | h
    · exact h₁ h
    · exact h₂ h

/-- If the right authority reaches a defect that is hard for the left
authority, then adjoining the right authority strictly increases correction
power over the left authority. -/
theorem left_lt_join_of_right_witness
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D)
    {x : State} {d : D}
    (h₂ : C₂.CorrectableAt x d)
    (h₁ : C₁.HardObstructionAt x d) :
    CorrectionPowerLT C₁ (joinCorrectionRealization C₁ C₂) := by
  exact correctionPowerLT_of_le_of_witness
    (le_join_left C₁ C₂)
    (le_join_right C₁ C₂ x d h₂)
    h₁

end KUOS.DependentOriginationCorrectionPowerLatticeV2_93
