import Mathlib

namespace KUOS.CodeAI.MaintainabilityTrajectoryGateV0_1

/-- A single lower-is-better maintainability observation. -/
structure AxisObservation where
  axis : String
  baselineValue : Nat
  candidateValue : Nat
  maximumAllowedIncrease : Nat
  deriving DecidableEq, Repr

/-- The bounded positive regression on one maintainability axis. -/
def regressionAmount (observation : AxisObservation) : Nat :=
  observation.candidateValue - observation.baselineValue

/-- An axis improves when the isolated candidate value is strictly lower. -/
def improved (observation : AxisObservation) : Prop :=
  observation.candidateValue < observation.baselineValue

instance instDecidableImproved (observation : AxisObservation) :
    Decidable (improved observation) := by
  unfold improved
  infer_instance

/-- A single axis remains inside its explicit regression allowance. -/
def withinAxisLimit (observation : AxisObservation) : Prop :=
  regressionAmount observation ≤ observation.maximumAllowedIncrease

instance instDecidableWithinAxisLimit (observation : AxisObservation) :
    Decidable (withinAxisLimit observation) := by
  unfold withinAxisLimit regressionAmount
  infer_instance

/--
A computable decision procedure for the finite bounded universal used by the
trajectory gate.  This preserves the proposition as stated while avoiding a
noncomputable decision procedure for an unrestricted universal quantifier.
-/
private def decideAllWithinAxisLimits :
    (observations : List AxisObservation) →
      Decidable (∀ observation ∈ observations, withinAxisLimit observation)
  | [] =>
      isTrue (by simp)
  | head :: tail =>
      match instDecidableWithinAxisLimit head, decideAllWithinAxisLimits tail with
      | isTrue hHead, isTrue hTail =>
          isTrue (by
            intro observation hMember
            rcases List.mem_cons.mp hMember with hEq | hMember
            · subst observation
              exact hHead
            · exact hTail observation hMember)
      | isFalse hHead, _ =>
          isFalse (by
            intro hAll
            exact hHead (hAll head (by simp)))
      | _, isFalse hTail =>
          isFalse (by
            intro hAll
            apply hTail
            intro observation hMember
            exact hAll observation (by simp [hMember]))

/-- The bounded aggregate policy for the maintainability gate. -/
structure TrajectoryPolicy where
  maximumTotalRegression : Nat
  minimumImprovedAxes : Nat
  deriving DecidableEq, Repr

/-- The gate input carries bounded observations and a read-only memory-hint flag. -/
structure GateInput where
  observations : List AxisObservation
  memoryHintAvailable : Bool
  deriving DecidableEq, Repr

/-- Sum of all positive maintainability regressions. -/
def totalRegression (input : GateInput) : Nat :=
  (input.observations.map regressionAmount).sum

/-- Count of axes that strictly improve. -/
def improvedAxisCount : List AxisObservation → Nat
  | [] => 0
  | observation :: observations =>
      (if improved observation then 1 else 0) + improvedAxisCount observations

/--
Generic gate admissibility: every axis is inside its own allowance, aggregate
regression is bounded, and enough axes improve.
-/
def GateAdmissible (input : GateInput) (policy : TrajectoryPolicy) : Prop :=
  (∀ observation ∈ input.observations, withinAxisLimit observation) ∧
  totalRegression input ≤ policy.maximumTotalRegression ∧
  policy.minimumImprovedAxes ≤ improvedAxisCount input.observations

instance instDecidableGateAdmissible (input : GateInput) (policy : TrajectoryPolicy) :
    Decidable (GateAdmissible input policy) := by
  unfold GateAdmissible
  letI : Decidable
      (∀ observation ∈ input.observations, withinAxisLimit observation) :=
    decideAllWithinAxisLimits input.observations
  infer_instance

theorem admitted_axis_bound
    {input : GateInput}
    {policy : TrajectoryPolicy}
    {observation : AxisObservation}
    (hAdmitted : GateAdmissible input policy)
    (hMember : observation ∈ input.observations) :
    regressionAmount observation ≤ observation.maximumAllowedIncrease :=
  hAdmitted.1 observation hMember

theorem admitted_total_regression_bound
    {input : GateInput}
    {policy : TrajectoryPolicy}
    (hAdmitted : GateAdmissible input policy) :
    totalRegression input ≤ policy.maximumTotalRegression :=
  hAdmitted.2.1

theorem admitted_improvement_floor
    {input : GateInput}
    {policy : TrajectoryPolicy}
    (hAdmitted : GateAdmissible input policy) :
    policy.minimumImprovedAxes ≤ improvedAxisCount input.observations :=
  hAdmitted.2.2

/-- A memory hint cannot override a failed per-axis maintainability bound. -/
theorem memory_hint_cannot_override_axis_limit
    {input : GateInput}
    {policy : TrajectoryPolicy}
    {observation : AxisObservation}
    (hMember : observation ∈ input.observations)
    (hExceeded : ¬ withinAxisLimit observation) :
    ¬ GateAdmissible input policy := by
  intro hAdmitted
  exact hExceeded (hAdmitted.1 observation hMember)

/-- Gate admissibility is definitionally independent of memory-hint presence. -/
theorem admissibility_independent_of_memory_hint
    (observations : List AxisObservation)
    (policy : TrajectoryPolicy) :
    GateAdmissible
        { observations := observations, memoryHintAvailable := true }
        policy ↔
      GateAdmissible
        { observations := observations, memoryHintAvailable := false }
        policy :=
  Iff.rfl

inductive GateDecision where
  | admitted
  | held
  deriving DecidableEq, Repr

/-- A hold is a bounded deferral, not rejection. -/
def treatedAsRejection : GateDecision → Bool
  | .admitted => false
  | .held => false

theorem held_is_not_rejection :
    treatedAsRejection .held = false :=
  rfl

/-- Downstream authorities and effects remain outside the gate. -/
structure AuthorityBoundary where
  selectionAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  repairAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  testExecutionPerformed : Bool
  repairExecuted : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  futureMaintainabilityProven : Bool
  correctnessProven : Bool
  probabilityClaimed : Bool
  deriving DecidableEq, Repr

def boundaryPreserved (boundary : AuthorityBoundary) : Prop :=
  boundary.selectionAuthorityGranted = false ∧
  boundary.verificationAuthorityGranted = false ∧
  boundary.repairAuthorityGranted = false ∧
  boundary.executionAuthorityGranted = false ∧
  boundary.gitAuthorityGranted = false ∧
  boundary.testExecutionPerformed = false ∧
  boundary.repairExecuted = false ∧
  boundary.repositoryMutationPerformed = false ∧
  boundary.gitEffectPerformed = false ∧
  boundary.futureMaintainabilityProven = false ∧
  boundary.correctnessProven = false ∧
  boundary.probabilityClaimed = false

instance instDecidableBoundaryPreserved (boundary : AuthorityBoundary) :
    Decidable (boundaryPreserved boundary) := by
  unfold boundaryPreserved
  infer_instance

theorem boundary_preserved_of_all_false
    (boundary : AuthorityBoundary)
    (hSelection : boundary.selectionAuthorityGranted = false)
    (hVerification : boundary.verificationAuthorityGranted = false)
    (hRepairAuthority : boundary.repairAuthorityGranted = false)
    (hExecution : boundary.executionAuthorityGranted = false)
    (hGitAuthority : boundary.gitAuthorityGranted = false)
    (hTest : boundary.testExecutionPerformed = false)
    (hRepair : boundary.repairExecuted = false)
    (hMutation : boundary.repositoryMutationPerformed = false)
    (hGitEffect : boundary.gitEffectPerformed = false)
    (hFuture : boundary.futureMaintainabilityProven = false)
    (hCorrectness : boundary.correctnessProven = false)
    (hProbability : boundary.probabilityClaimed = false) :
    boundaryPreserved boundary :=
  ⟨hSelection, hVerification, hRepairAuthority, hExecution, hGitAuthority,
   hTest, hRepair, hMutation, hGitEffect, hFuture, hCorrectness, hProbability⟩

/-! ### Actual CodeAI step-9 specialization -/

def actualObservations : List AxisObservation :=
  [
    {
      axis := "structural_complexity"
      baselineValue := 120
      candidateValue := 118
      maximumAllowedIncrease := 0
    },
    {
      axis := "dependency_surface"
      baselineValue := 40
      candidateValue := 41
      maximumAllowedIncrease := 1
    },
    {
      axis := "duplication"
      baselineValue := 15
      candidateValue := 12
      maximumAllowedIncrease := 0
    },
    {
      axis := "test_burden"
      baselineValue := 80
      candidateValue := 82
      maximumAllowedIncrease := 3
    },
    {
      axis := "proof_burden"
      baselineValue := 12
      candidateValue := 12
      maximumAllowedIncrease := 0
    },
    {
      axis := "repair_recurrence"
      baselineValue := 9
      candidateValue := 7
      maximumAllowedIncrease := 0
    }
  ]

def actualGateInput : GateInput :=
  {
    observations := actualObservations
    memoryHintAvailable := false
  }

def actualTrajectoryPolicy : TrajectoryPolicy :=
  {
    maximumTotalRegression := 4
    minimumImprovedAxes := 3
  }

theorem actual_total_regression :
    totalRegression actualGateInput = 3 := by
  native_decide

theorem actual_improved_axis_count :
    improvedAxisCount actualObservations = 3 := by
  native_decide

theorem actual_maintainability_trajectory_admitted :
    GateAdmissible actualGateInput actualTrajectoryPolicy := by
  native_decide

def actualAuthorityBoundary : AuthorityBoundary :=
  {
    selectionAuthorityGranted := false
    verificationAuthorityGranted := false
    repairAuthorityGranted := false
    executionAuthorityGranted := false
    gitAuthorityGranted := false
    testExecutionPerformed := false
    repairExecuted := false
    repositoryMutationPerformed := false
    gitEffectPerformed := false
    futureMaintainabilityProven := false
    correctnessProven := false
    probabilityClaimed := false
  }

theorem actual_authority_boundary_preserved :
    boundaryPreserved actualAuthorityBoundary := by
  native_decide

end KUOS.CodeAI.MaintainabilityTrajectoryGateV0_1
