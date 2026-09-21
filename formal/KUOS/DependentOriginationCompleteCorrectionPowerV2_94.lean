import KUOS.DependentOriginationCorrectionPowerLatticeV2_93

namespace KUOS.DependentOriginationCompleteCorrectionPowerV2_94

open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
open KUOS.DependentOriginationCorrectionProfileRealizationV2_91

universe i u v w

/-!
# Complete correction-power semantics v2.94

The v2.93 layer constructs binary join and meet at the reachability-profile
level. This file extends the same semantic construction to arbitrary indexed
families whose correction parameter carriers may vary with the index.

For a family C i:

* the supremum profile reaches a defect when some member reaches it;
* the infimum profile reaches a defect when every member reaches it.

Both profiles are realized canonically by the functional profile realization
from v2.91. The resulting mechanisms satisfy the expected arbitrary least
upper bound and greatest lower bound laws for CorrectionPowerLE.

This is a semantic completeness statement. It does not claim that arbitrary
joins or meets are represented by native operations on the original parameter
carriers.
-/

/-- Pointwise existential union of an indexed family of correction powers. -/
def familySupCorrectionProfile
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D) :
    State → D → Prop :=
  fun x d => ∃ j, CorrectionReachabilityProfile (C j) x d

/-- Pointwise universal intersection of an indexed family of correction
powers. -/
def familyInfCorrectionProfile
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D) :
    State → D → Prop :=
  fun x d => ∀ j, CorrectionReachabilityProfile (C j) x d

/-- Canonical realization of the arbitrary supremum correction power. -/
def familySupCorrectionRealization
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (familySupCorrectionProfile C)

/-- Canonical realization of the arbitrary infimum correction power. -/
def familyInfCorrectionRealization
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (familyInfCorrectionProfile C)

/-- Every family member embeds into the arbitrary supremum. -/
theorem family_le_sup
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (j : ι) :
    CorrectionPowerLE (C j) (familySupCorrectionRealization C) := by
  intro x d h
  apply (functionalProfileCorrectionRealization_correctable_iff
    (familySupCorrectionProfile C) x d).2
  exact ⟨j, h⟩

/-- The arbitrary supremum is the least upper bound. -/
theorem familySup_least
    {ι : Type i} {State : Type u} {Param : ι → Type v}
    {TargetParam : Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (T : CorrectionRealization State TargetParam D)
    (h : ∀ j, CorrectionPowerLE (C j) T) :
    CorrectionPowerLE (familySupCorrectionRealization C) T := by
  intro x d hsup
  have hex :
      ∃ j, CorrectionReachabilityProfile (C j) x d :=
    (functionalProfileCorrectionRealization_correctable_iff
      (familySupCorrectionProfile C) x d).1 hsup
  rcases hex with ⟨j, hj⟩
  exact h j x d hj

/-- The arbitrary infimum embeds into every family member. -/
theorem familyInf_le
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (j : ι) :
    CorrectionPowerLE (familyInfCorrectionRealization C) (C j) := by
  intro x d hinf
  have hall :
      ∀ k, CorrectionReachabilityProfile (C k) x d :=
    (functionalProfileCorrectionRealization_correctable_iff
      (familyInfCorrectionProfile C) x d).1 hinf
  exact hall j

/-- The arbitrary infimum is the greatest lower bound. -/
theorem familyInf_greatest
    {ι : Type i} {State : Type u} {Param : ι → Type v}
    {SourceParam : Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (S : CorrectionRealization State SourceParam D)
    (h : ∀ j, CorrectionPowerLE S (C j)) :
    CorrectionPowerLE S (familyInfCorrectionRealization C) := by
  intro x d hs
  apply (functionalProfileCorrectionRealization_correctable_iff
    (familyInfCorrectionProfile C) x d).2
  intro j
  exact h j x d hs

/-- Correctability for the arbitrary supremum is exactly existential
correctability by a family member. -/
theorem familySup_correctable_iff
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (x : State) (d : D) :
    (familySupCorrectionRealization C).CorrectableAt x d ↔
      ∃ j, (C j).CorrectableAt x d := by
  exact functionalProfileCorrectionRealization_correctable_iff
    (familySupCorrectionProfile C) x d

/-- Correctability for the arbitrary infimum is exactly simultaneous
correctability by every family member. -/
theorem familyInf_correctable_iff
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (x : State) (d : D) :
    (familyInfCorrectionRealization C).CorrectableAt x d ↔
      ∀ j, (C j).CorrectableAt x d := by
  exact functionalProfileCorrectionRealization_correctable_iff
    (familyInfCorrectionProfile C) x d

/-- A defect is hard for the arbitrary supremum exactly when it is hard for
every family member. This direction is constructive because it is just
negation of an existential. -/
theorem familySup_hardObstruction_iff
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (x : State) (d : D) :
    (familySupCorrectionRealization C).HardObstructionAt x d ↔
      ∀ j, (C j).HardObstructionAt x d := by
  constructor
  · intro hsup j hj
    exact hsup (family_le_sup C j x d hj)
  · intro hall hsup
    have hex :
        ∃ j, (C j).CorrectableAt x d :=
      (familySup_correctable_iff C x d).1 hsup
    rcases hex with ⟨j, hj⟩
    exact hall j hj

/-- Any member-level hard obstruction forces a hard obstruction for the
arbitrary infimum. No classical converse is assumed. -/
theorem familyInf_hardObstruction_of_member
    {ι : Type i} {State : Type u} {Param : ι → Type v} {D : Type w}
    (C : ∀ j, CorrectionRealization State (Param j) D)
    (x : State) (d : D)
    (j : ι)
    (hj : (C j).HardObstructionAt x d) :
    (familyInfCorrectionRealization C).HardObstructionAt x d := by
  intro hinf
  exact hj (familyInf_le C j x d hinf)

end KUOS.DependentOriginationCompleteCorrectionPowerV2_94
