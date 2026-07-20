import Mathlib

namespace KUOS.CodeAI.CandidateStaticAdmissibilityPreflightV0_1

/-- Generic four-way classification for an effect-free static preflight. -/
inductive Classification where
  | admissible
  | repairable
  | hold
  | rejected
  deriving DecidableEq, Repr

/-- Generic finding counts, independent of the concrete CodeAI runtime. -/
structure FindingCounts where
  repairable : Nat
  hold : Nat
  rejected : Nat
  deriving DecidableEq, Repr

/-- Reject dominates hold, which dominates repair, while zero findings are admissible. -/
def classify (counts : FindingCounts) : Classification :=
  if counts.rejected ≠ 0 then .rejected
  else if counts.hold ≠ 0 then .hold
  else if counts.repairable ≠ 0 then .repairable
  else .admissible

/-- Generic zero-finding predicate. -/
def NoFindings (counts : FindingCounts) : Prop :=
  counts.repairable = 0 ∧ counts.hold = 0 ∧ counts.rejected = 0

/-- Generic classification theorem: admissibility is exactly zero findings. -/
theorem classify_eq_admissible_iff (counts : FindingCounts) :
    classify counts = .admissible ↔ NoFindings counts := by
  unfold classify NoFindings
  by_cases hrejected : counts.rejected ≠ 0
  · simp [hrejected]
  · by_cases hhold : counts.hold ≠ 0
    · simp [hrejected, hhold]
    · by_cases hrepairable : counts.repairable ≠ 0
      · simp [hrejected, hhold, hrepairable]
      · simp [hrejected, hhold, hrepairable]

/-- Any repair finding prevents generic admissibility. -/
theorem classify_ne_admissible_of_repairable_ne_zero
    (counts : FindingCounts) (h : counts.repairable ≠ 0) :
    classify counts ≠ .admissible := by
  intro hadmissible
  exact h (classify_eq_admissible_iff counts |>.mp hadmissible).1

/-- Any hold finding prevents generic admissibility. -/
theorem classify_ne_admissible_of_hold_ne_zero
    (counts : FindingCounts) (h : counts.hold ≠ 0) :
    classify counts ≠ .admissible := by
  intro hadmissible
  exact h (classify_eq_admissible_iff counts |>.mp hadmissible).2.1

/-- Any reject finding prevents generic admissibility. -/
theorem classify_ne_admissible_of_rejected_ne_zero
    (counts : FindingCounts) (h : counts.rejected ≠ 0) :
    classify counts ≠ .admissible := by
  intro hadmissible
  exact h (classify_eq_admissible_iff counts |>.mp hadmissible).2.2

/-- Concrete KuuOS receipt model for the static preflight boundary. -/
structure Decision where
  findings : FindingCounts
  classification : Classification
  exactLineageVerified : Bool
  operationCollisionCheckCompleted : Bool
  inMemoryMaterializationCompleted : Bool
  materializedParseChecksCompleted : Bool
  dependencyCorrespondenceChecked : Bool
  testPlanCorrespondenceChecked : Bool
  materializedSnapshotEphemeral : Bool
  repositoryMutationPerformed : Bool
  candidateSelected : Bool
  executionAuthorityGranted : Bool
  treatedAsCorrectnessProof : Bool
  deriving DecidableEq, Repr

/-- A well-formed receipt preserves exact classification and all no-effect boundaries. -/
def Decision.WellFormed (decision : Decision) : Prop :=
  decision.classification = classify decision.findings ∧
  decision.exactLineageVerified = true ∧
  decision.operationCollisionCheckCompleted = true ∧
  decision.inMemoryMaterializationCompleted = true ∧
  decision.materializedParseChecksCompleted = true ∧
  decision.dependencyCorrespondenceChecked = true ∧
  decision.testPlanCorrespondenceChecked = true ∧
  decision.materializedSnapshotEphemeral = true ∧
  decision.repositoryMutationPerformed = false ∧
  decision.candidateSelected = false ∧
  decision.executionAuthorityGranted = false ∧
  decision.treatedAsCorrectnessProof = false

/-- A well-formed preflight never reports repository mutation. -/
theorem Decision.WellFormed.noRepositoryMutation
    {decision : Decision} (h : decision.WellFormed) :
    decision.repositoryMutationPerformed = false :=
  h.2.2.2.2.2.2.2.2.1

/-- A well-formed preflight never selects a candidate. -/
theorem Decision.WellFormed.noCandidateSelection
    {decision : Decision} (h : decision.WellFormed) :
    decision.candidateSelected = false :=
  h.2.2.2.2.2.2.2.2.2.1

/-- A well-formed preflight never grants execution authority. -/
theorem Decision.WellFormed.noExecutionAuthority
    {decision : Decision} (h : decision.WellFormed) :
    decision.executionAuthorityGranted = false :=
  h.2.2.2.2.2.2.2.2.2.2.1

/-- A well-formed preflight never treats static evidence as a correctness proof. -/
theorem Decision.WellFormed.notCorrectnessProof
    {decision : Decision} (h : decision.WellFormed) :
    decision.treatedAsCorrectnessProof = false :=
  h.2.2.2.2.2.2.2.2.2.2.2

/-- Concrete specialization: an admissible well-formed receipt has zero findings. -/
theorem Decision.WellFormed.noFindings_of_admissible
    {decision : Decision} (h : decision.WellFormed)
    (hadmissible : decision.classification = .admissible) :
    NoFindings decision.findings := by
  apply classify_eq_admissible_iff decision.findings |>.mp
  calc
    classify decision.findings = decision.classification := h.1.symm
    _ = .admissible := hadmissible

/-- Ephemeral materialization and no mutation remain separately recorded facts. -/
theorem Decision.WellFormed.ephemeral_and_noMutation
    {decision : Decision} (h : decision.WellFormed) :
    decision.materializedSnapshotEphemeral = true ∧
      decision.repositoryMutationPerformed = false :=
  ⟨h.2.2.2.2.2.2.2.1, h.noRepositoryMutation⟩

/-- Admissibility never upgrades the receipt into candidate-selection authority. -/
theorem Decision.WellFormed.admissible_does_not_select
    {decision : Decision} (h : decision.WellFormed)
    (_hadmissible : decision.classification = .admissible) :
    decision.candidateSelected = false :=
  h.noCandidateSelection

end KUOS.CodeAI.CandidateStaticAdmissibilityPreflightV0_1
