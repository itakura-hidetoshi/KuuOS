import Mathlib

namespace KUOS.CodeAI.IndependentTestStrengtheningV0_1

/-- Typed error families remain descriptive inputs to test planning. -/
inductive ErrorFamily where
  | operationConflict
  | materialization
  | syntax
  | dependency
  | testing
  | policyMarker
  | semanticNoop
  deriving DecidableEq, Repr

/-- Independent obligations describe evidence requirements rather than execution. -/
inductive CheckKind where
  | sourceLineageReplay
  | deterministicReconstruction
  | changedPathCoverage
  | operationCollisionReplay
  | materializationReplay
  | parseNegativeControl
  | dependencyClosure
  | testPlanCompleteness
  | policyMarkerScan
  | materialEffectAssertion
  | noveltyFalsification
  | errorFreeMutationProbe
  | localRepairRegression
  | externalEvidenceBinding
  | unmaterializabilityReproduction
  deriving DecidableEq, Repr

/-- Each typed family determines one distinct error-specific obligation. -/
def familyCheck : ErrorFamily → CheckKind
  | .operationConflict => .operationCollisionReplay
  | .materialization => .materializationReplay
  | .syntax => .parseNegativeControl
  | .dependency => .dependencyClosure
  | .testing => .testPlanCompleteness
  | .policyMarker => .policyMarkerScan
  | .semanticNoop => .materialEffectAssertion

theorem familyCheck_injective : Function.Injective familyCheck := by
  intro left right h
  cases left <;> cases right <;> simp [familyCheck] at h ⊢

/-- Descriptive repair routes remain disjoint. -/
inductive RepairRoute where
  | localCandidateRepair
  | externalEvidenceRequired
  | currentIRUnmaterializable
  deriving DecidableEq, Repr

/-- Every route determines one distinct route-specific obligation. -/
def routeCheck : RepairRoute → CheckKind
  | .localCandidateRepair => .localRepairRegression
  | .externalEvidenceRequired => .externalEvidenceBinding
  | .currentIRUnmaterializable => .unmaterializabilityReproduction

theorem routeCheck_injective : Function.Injective routeCheck := by
  intro left right h
  cases left <;> cases right <;> simp [routeCheck] at h ⊢

/-- Every candidate receives the same three baseline obligations. -/
def baselineChecks : List CheckKind :=
  [.sourceLineageReplay, .deterministicReconstruction, .changedPathCoverage]

theorem baselineChecks_length : baselineChecks.length = 3 := by
  rfl

/-- A strengthening receipt accounts for obligations while preserving no-authority boundaries. -/
structure Receipt where
  candidateCount : Nat
  typedErrorCount : Nat
  obligationCount : Nat
  baselineObligationCount : Nat
  errorSpecificObligationCount : Nat
  noveltyObligationCount : Nat
  routeObligationCount : Nat
  errorFreeObligationCount : Nat
  exactLineageVerified : Bool
  allCandidatesPreserved : Bool
  independentRunnerRequired : Bool
  isolatedExecutionRequired : Bool
  testGenerationPerformed : Bool
  testExecutionPerformed : Bool
  rankingPerformed : Bool
  candidateSelected : Bool
  verificationRunnerInvoked : Bool
  repairExecuted : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  selectionAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  repairAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  strengthenedPlanTreatedAsTestSuccess : Bool
  obligationCountTreatedAsCandidateQuality : Bool
  testCoverageTreatedAsCorrectnessProof : Bool
  deriving DecidableEq, Repr

/-- Exact accounting and effect separation define a well-formed strengthening receipt. -/
structure Receipt.WellFormed (receipt : Receipt) : Prop where
  obligationAccounting :
    receipt.baselineObligationCount +
        receipt.errorSpecificObligationCount +
        receipt.noveltyObligationCount +
        receipt.routeObligationCount +
        receipt.errorFreeObligationCount =
      receipt.obligationCount
  baselinePerCandidate :
    3 * receipt.candidateCount ≤ receipt.baselineObligationCount
  exactLineage : receipt.exactLineageVerified = true
  candidatesPreserved : receipt.allCandidatesPreserved = true
  independentRunner : receipt.independentRunnerRequired = true
  isolatedExecution : receipt.isolatedExecutionRequired = true
  noTestGeneration : receipt.testGenerationPerformed = false
  noTestExecution : receipt.testExecutionPerformed = false
  noRanking : receipt.rankingPerformed = false
  noSelection : receipt.candidateSelected = false
  noVerifierInvocation : receipt.verificationRunnerInvoked = false
  noRepair : receipt.repairExecuted = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitEffect : receipt.gitEffectPerformed = false
  noSelectionAuthority : receipt.selectionAuthorityGranted = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noRepairAuthority : receipt.repairAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noGitAuthority : receipt.gitAuthorityGranted = false
  noTestSuccessClaim : receipt.strengthenedPlanTreatedAsTestSuccess = false
  noQualityScore : receipt.obligationCountTreatedAsCandidateQuality = false
  noCorrectnessProof : receipt.testCoverageTreatedAsCorrectnessProof = false

/-- Every well-formed plan carries at least three baseline obligations per candidate. -/
theorem Receipt.WellFormed.minimumBaselineCoverage
    {receipt : Receipt} (h : receipt.WellFormed) :
    3 * receipt.candidateCount ≤ receipt.obligationCount := by
  calc
    3 * receipt.candidateCount ≤ receipt.baselineObligationCount := h.baselinePerCandidate
    _ ≤ receipt.obligationCount := by
      rw [← h.obligationAccounting]
      omega

/-- Strengthened planning neither generates nor executes tests. -/
theorem Receipt.WellFormed.planningDoesNotExecute
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.testGenerationPerformed = false ∧
      receipt.testExecutionPerformed = false ∧
      receipt.verificationRunnerInvoked = false :=
  ⟨h.noTestGeneration, h.noTestExecution, h.noVerifierInvocation⟩

/-- Strengthening remains separate from ranking and selection. -/
theorem Receipt.WellFormed.selectionRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.rankingPerformed = false ∧
      receipt.candidateSelected = false ∧
      receipt.selectionAuthorityGranted = false :=
  ⟨h.noRanking, h.noSelection, h.noSelectionAuthority⟩

/-- A strengthening receipt grants no downstream authority. -/
theorem Receipt.WellFormed.downstreamAuthorityRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.verificationAuthorityGranted = false ∧
      receipt.repairAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.gitAuthorityGranted = false :=
  ⟨h.noVerificationAuthority, h.noRepairAuthority, h.noExecutionAuthority, h.noGitAuthority⟩

/-- More obligations are not interpreted as a candidate-quality score. -/
theorem Receipt.WellFormed.obligationCountIsNotQuality
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.obligationCountTreatedAsCandidateQuality = false :=
  h.noQualityScore

/-- Planned coverage is not promoted into test success or correctness proof. -/
theorem Receipt.WellFormed.coverageIsNotCorrectness
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.strengthenedPlanTreatedAsTestSuccess = false ∧
      receipt.testCoverageTreatedAsCorrectnessProof = false :=
  ⟨h.noTestSuccessClaim, h.noCorrectnessProof⟩

end KUOS.CodeAI.IndependentTestStrengtheningV0_1
