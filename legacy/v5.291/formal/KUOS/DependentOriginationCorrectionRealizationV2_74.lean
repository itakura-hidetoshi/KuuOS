import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationCorrectionRealizationV2_74

universe u v w m

/-!
# Explicit correction realization v2.74

This layer separates present residual order from the independent question of
whether a defect lies in the image of an admissible correction mechanism.

In particular, `CorrectableAt` is not identified with `Flat`, and
`HardObstructionAt` means absence of an explicit admissible realization
witness rather than mere nontriviality or non-flatness.
-/

/-- Explicit admissible correction parameters and the defect value they
realize at a state. -/
structure CorrectionRealization
    (State : Type u) (Param : Type v) (D : Type w) where
  admissible : State → Param → Prop
  effect : State → Param → D

namespace CorrectionRealization

variable {State : Type u} {Param : Type v} {D : Type w}

/-- A defect is correctable at a state exactly when some admissible parameter
realizes that defect value. -/
def CorrectableAt
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) : Prop :=
  ∃ p, C.admissible x p ∧ C.effect x p = d

/-- A hard obstruction at a state is absence of an admissible correction
parameter realizing that defect. -/
def HardObstructionAt
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) : Prop :=
  ¬ C.CorrectableAt x d

theorem correctableAt_iff
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) :
    C.CorrectableAt x d ↔
      ∃ p, C.admissible x p ∧ C.effect x p = d :=
  Iff.rfl

end CorrectionRealization

/-- Robust correctability is supplied as explicit ordered-margin data.
The generic layer does not invent a norm, cone, topology, or interior notion
on an arbitrary defect carrier. Larger margins are stronger witnesses. -/
structure RobustCorrectionData
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D)
    (Margin : Type m) [Preorder Margin] where
  robustAt : Margin → State → D → Prop
  robust_implies_correctable :
    ∀ μ x d, robustAt μ x d → C.CorrectableAt x d
  robust_monotone :
    ∀ {μ₁ μ₂ x d},
      μ₂ ≤ μ₁ →
      robustAt μ₁ x d →
      robustAt μ₂ x d

namespace RobustCorrectionData

variable
    {State : Type u} {Param : Type v} {D : Type w}
    {C : CorrectionRealization State Param D}
    {Margin : Type m} [Preorder Margin]

/-- Every robust correction witness is, in particular, an exact correction
image witness. -/
theorem correctableAt
    (R : RobustCorrectionData C Margin)
    {μ : Margin} {x : State} {d : D}
    (h : R.robustAt μ x d) :
    C.CorrectableAt x d :=
  R.robust_implies_correctable μ x d h

/-- A witness at a stronger margin restricts to every weaker margin. -/
theorem weaken_margin
    (R : RobustCorrectionData C Margin)
    {μ₁ μ₂ : Margin} {x : State} {d : D}
    (hμ : μ₂ ≤ μ₁)
    (h : R.robustAt μ₁ x d) :
    R.robustAt μ₂ x d :=
  R.robust_monotone hμ h

end RobustCorrectionData

end KUOS.DependentOriginationCorrectionRealizationV2_74
