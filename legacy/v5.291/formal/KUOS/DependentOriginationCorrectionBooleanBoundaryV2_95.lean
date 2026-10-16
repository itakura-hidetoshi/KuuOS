import KUOS.DependentOriginationCompleteCorrectionPowerV2_94

namespace KUOS.DependentOriginationCorrectionBooleanBoundaryV2_95

open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
open KUOS.DependentOriginationCorrectionProfileRealizationV2_91
open KUOS.DependentOriginationCorrectionPowerLatticeV2_93

universe u v w

/-!
# Correction Boolean boundary v2.95

The v2.94 semantic completion supplies arbitrary suprema and infima of
correction power. This layer studies the complementary obstruction profile.

For a correction mechanism C, its complement profile reaches exactly the
defects that are hard obstructions for C. Since arbitrary profiles admit the
canonical functional realization from v2.91, this obstruction complement is
again a correction mechanism.

The logical boundary is explicit:

* bottom, top, complement reachability, antitonicity, and
  meet-with-complement = bottom are constructive;
* join-with-complement = top and double-complement recovery use classical
  excluded middle.

Thus Boolean behavior is not silently folded into the constructive
correction-power lattice.
-/

/-- Empty correction power: no defect is reachable at any state. -/
def bottomCorrectionProfile
    {State : Type u} {D : Type w} :
    State → D → Prop :=
  fun _ _ => False

/-- Maximal correction power: every defect is reachable at every state. -/
def topCorrectionProfile
    {State : Type u} {D : Type w} :
    State → D → Prop :=
  fun _ _ => True

/-- Canonical realization of empty correction power. -/
def bottomCorrectionRealization
    {State : Type u} {D : Type w} :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization bottomCorrectionProfile

/-- Canonical realization of maximal correction power. -/
def topCorrectionRealization
    {State : Type u} {D : Type w} :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization topCorrectionProfile

/-- Empty correction power is below every correction mechanism. -/
theorem bottom_le
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerLE bottomCorrectionRealization C := by
  intro x d hbot
  have hfalse : False :=
    (functionalProfileCorrectionRealization_correctable_iff
      (bottomCorrectionProfile (State := State) (D := D)) x d).1 hbot
  exact hfalse.elim

/-- Every correction mechanism is below maximal correction power. -/
theorem le_top
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerLE C topCorrectionRealization := by
  intro x d _
  apply (functionalProfileCorrectionRealization_correctable_iff
    (topCorrectionProfile (State := State) (D := D)) x d).2
  exact True.intro

/-- The obstruction complement reaches exactly the defects that are hard for
the original correction mechanism. -/
def complementCorrectionProfile
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    State → D → Prop :=
  fun x d => C.HardObstructionAt x d

/-- Canonical realization of the obstruction-complement profile. -/
def complementCorrectionRealization
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (complementCorrectionProfile C)

/-- Complement correctability is definitionally the original hard-obstruction
predicate, after passage through the canonical profile realization. -/
theorem complement_correctable_iff_hard
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) :
    (complementCorrectionRealization C).CorrectableAt x d ↔
      C.HardObstructionAt x d := by
  exact functionalProfileCorrectionRealization_correctable_iff
    (complementCorrectionProfile C) x d

/-- Complement reverses correction-power inclusion constructively. -/
theorem complement_antitone
    {State : Type u}
    {Param₁ : Type v} {Param₂ : Type v} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (hpow : CorrectionPowerLE C₁ C₂) :
    CorrectionPowerLE
      (complementCorrectionRealization C₂)
      (complementCorrectionRealization C₁) := by
  intro x d h₂
  have hhard₂ : C₂.HardObstructionAt x d :=
    (complement_correctable_iff_hard C₂ x d).1 h₂
  have hhard₁ : C₁.HardObstructionAt x d :=
    CorrectionPowerLE.hardObstruction_antitone hpow hhard₂
  exact (complement_correctable_iff_hard C₁ x d).2 hhard₁

/-- Constructively, a correction mechanism and its obstruction complement have
no common reachable defect. -/
theorem meet_complement_powerEq_bottom
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerEq
      (meetCorrectionRealization C (complementCorrectionRealization C))
      (bottomCorrectionRealization (State := State) (D := D)) := by
  apply (correctionPowerEq_iff_reachability_iff
    (meetCorrectionRealization C (complementCorrectionRealization C))
    (bottomCorrectionRealization (State := State) (D := D))).2
  intro x d
  constructor
  · intro hmeet
    have hboth :
        C.CorrectableAt x d ∧
          (complementCorrectionRealization C).CorrectableAt x d :=
      (meet_correctable_iff
        C (complementCorrectionRealization C) x d).1 hmeet
    have hhard : C.HardObstructionAt x d :=
      (complement_correctable_iff_hard C x d).1 hboth.2
    exact (hhard hboth.1).elim
  · intro hbot
    have hfalse : False :=
      (functionalProfileCorrectionRealization_correctable_iff
        (bottomCorrectionProfile (State := State) (D := D)) x d).1 hbot
    exact hfalse.elim

/-- Classically, a correction mechanism together with its obstruction
complement reaches every defect. -/
theorem join_complement_powerEq_top
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerEq
      (joinCorrectionRealization C (complementCorrectionRealization C))
      (topCorrectionRealization (State := State) (D := D)) := by
  classical
  apply (correctionPowerEq_iff_reachability_iff
    (joinCorrectionRealization C (complementCorrectionRealization C))
    (topCorrectionRealization (State := State) (D := D))).2
  intro x d
  constructor
  · intro _
    apply (functionalProfileCorrectionRealization_correctable_iff
      (topCorrectionProfile (State := State) (D := D)) x d).2
    exact True.intro
  · intro _
    by_cases hC : C.CorrectableAt x d
    · exact le_join_left C (complementCorrectionRealization C) x d hC
    · have hcomp :
          (complementCorrectionRealization C).CorrectableAt x d :=
        (complement_correctable_iff_hard C x d).2 hC
      exact le_join_right C (complementCorrectionRealization C) x d hcomp

/-- Classically, taking the obstruction complement twice recovers the original
correction power, even though the parameter presentation changes. -/
theorem doubleComplement_powerEq
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerEq
      (complementCorrectionRealization
        (complementCorrectionRealization C))
      C := by
  classical
  apply (correctionPowerEq_iff_reachability_iff
    (complementCorrectionRealization
      (complementCorrectionRealization C))
    C).2
  intro x d
  constructor
  · intro hdouble
    have hhardComp :
        (complementCorrectionRealization C).HardObstructionAt x d :=
      (complement_correctable_iff_hard
        (complementCorrectionRealization C) x d).1 hdouble
    by_contra hC
    have hcomp :
        (complementCorrectionRealization C).CorrectableAt x d :=
      (complement_correctable_iff_hard C x d).2 hC
    exact hhardComp hcomp
  · intro hC
    apply (complement_correctable_iff_hard
      (complementCorrectionRealization C) x d).2
    intro hcomp
    have hhardC : C.HardObstructionAt x d :=
      (complement_correctable_iff_hard C x d).1 hcomp
    exact hhardC hC

end KUOS.DependentOriginationCorrectionBooleanBoundaryV2_95
