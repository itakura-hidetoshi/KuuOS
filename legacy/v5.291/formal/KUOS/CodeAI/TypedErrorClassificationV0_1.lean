import Mathlib

namespace KUOS.CodeAI.TypedErrorClassificationV0_1

/-- Static-preflight severities remain distinct from downstream authority. -/
inductive Severity where
  | repairable
  | hold
  | reject
  deriving DecidableEq, Repr

/-- A typed route describes the next evidence requirement, not permission to act. -/
inductive RepairRoute where
  | localCandidateRepair
  | externalEvidenceRequired
  | currentIRUnmaterializable
  deriving DecidableEq, Repr

/-- The route is determined only by the sealed preflight severity. -/
def repairRoute : Severity → RepairRoute
  | .repairable => .localCandidateRepair
  | .hold => .externalEvidenceRequired
  | .reject => .currentIRUnmaterializable

/-- Distinct severities cannot collapse into one repair route. -/
theorem repairRoute_injective : Function.Injective repairRoute := by
  intro left right h
  cases left <;> cases right <;> simp [repairRoute] at h ⊢

/-- Typed error families are descriptive and do not encode correctness probabilities. -/
inductive ErrorFamily where
  | operationConflict
  | materialization
  | syntax
  | dependency
  | testing
  | policyMarker
  | semanticNoop
  deriving DecidableEq, Repr

/-- One normalized error retains its source severity and descriptive family. -/
structure TypedError where
  candidateId : String
  family : ErrorFamily
  severity : Severity
  baselineOccurrenceCount : Nat
  deriving DecidableEq, Repr

/-- Count errors routed to one descriptive repair route. -/
def routeCount (route : RepairRoute) (errors : List TypedError) : Nat :=
  (errors.filter fun error => repairRoute error.severity = route).length

/-- Every typed error belongs to exactly one of the three route classes. -/
theorem repair_route_partition (errors : List TypedError) :
    routeCount .localCandidateRepair errors +
        routeCount .externalEvidenceRequired errors +
        routeCount .currentIRUnmaterializable errors =
      errors.length := by
  induction errors with
  | nil =>
      simp [routeCount]
  | cons error errors ih =>
      rcases error with ⟨candidateId, family, severity, baselineOccurrenceCount⟩
      cases severity <;>
        simp [routeCount, repairRoute] at ih ⊢ <;>
        omega

/-- Count errors in one family without assigning a rank to any candidate. -/
def familyCount (family : ErrorFamily) (errors : List TypedError) : Nat :=
  (errors.filter fun error => error.family = family).length

/-- Aggregate evidence remains classification-only. -/
structure Receipt where
  errors : List TypedError
  typedErrorCount : Nat
  localRepairCount : Nat
  externalEvidenceCount : Nat
  currentIRUnmaterializableCount : Nat
  exactLineageVerified : Bool
  sourceFindingEvidencePreserved : Bool
  taxonomyComplete : Bool
  historicalBaselineReferenceOnly : Bool
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
  typedErrorTreatedAsCauseProof : Bool
  historicalFrequencyTreatedAsProbability : Bool
  zeroStaticErrorTreatedAsCorrectnessProof : Bool
  deriving DecidableEq, Repr

/-- Exact accounting and all no-authority boundaries define a valid receipt. -/
structure Receipt.WellFormed (receipt : Receipt) : Prop where
  typedErrorCountExact : receipt.typedErrorCount = receipt.errors.length
  localRepairCountExact :
    receipt.localRepairCount = routeCount .localCandidateRepair receipt.errors
  externalEvidenceCountExact :
    receipt.externalEvidenceCount = routeCount .externalEvidenceRequired receipt.errors
  currentIRCountExact :
    receipt.currentIRUnmaterializableCount =
      routeCount .currentIRUnmaterializable receipt.errors
  exactLineage : receipt.exactLineageVerified = true
  findingsPreserved : receipt.sourceFindingEvidencePreserved = true
  taxonomyCompleteRecorded : receipt.taxonomyComplete = true
  baselineReferenceOnly : receipt.historicalBaselineReferenceOnly = true
  noRanking : receipt.rankingPerformed = false
  noSelection : receipt.candidateSelected = false
  noVerification : receipt.verificationRunnerInvoked = false
  noRepair : receipt.repairExecuted = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitEffect : receipt.gitEffectPerformed = false
  noSelectionAuthority : receipt.selectionAuthorityGranted = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noRepairAuthority : receipt.repairAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noGitAuthority : receipt.gitAuthorityGranted = false
  noCauseProof : receipt.typedErrorTreatedAsCauseProof = false
  noProbabilityClaim : receipt.historicalFrequencyTreatedAsProbability = false
  noZeroErrorCorrectnessClaim : receipt.zeroStaticErrorTreatedAsCorrectnessProof = false

/-- The three route counts account for every typed error exactly once. -/
theorem Receipt.WellFormed.routeAccounting
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.localRepairCount +
        receipt.externalEvidenceCount +
        receipt.currentIRUnmaterializableCount =
      receipt.typedErrorCount := by
  rw [h.localRepairCountExact, h.externalEvidenceCountExact, h.currentIRCountExact,
    h.typedErrorCountExact]
  exact repair_route_partition receipt.errors

/-- A repair route remains descriptive and cannot execute a repair. -/
theorem Receipt.WellFormed.repairRouteDoesNotGrantRepair
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.repairAuthorityGranted = false ∧ receipt.repairExecuted = false :=
  ⟨h.noRepairAuthority, h.noRepair⟩

/-- Typed classification does not rank or select candidates. -/
theorem Receipt.WellFormed.selectionRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.rankingPerformed = false ∧
      receipt.candidateSelected = false ∧
      receipt.selectionAuthorityGranted = false :=
  ⟨h.noRanking, h.noSelection, h.noSelectionAuthority⟩

/-- Historical occurrence counts remain observations rather than probabilities. -/
theorem Receipt.WellFormed.historicalFrequencyIsNotProbability
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.historicalBaselineReferenceOnly = true ∧
      receipt.historicalFrequencyTreatedAsProbability = false :=
  ⟨h.baselineReferenceOnly, h.noProbabilityClaim⟩

/-- A typed-error receipt grants neither verification, execution, nor Git authority. -/
theorem Receipt.WellFormed.downstreamAuthorityRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.gitAuthorityGranted = false :=
  ⟨h.noVerificationAuthority, h.noExecutionAuthority, h.noGitAuthority⟩

/-- Preserved evidence and complete taxonomy do not assert a proven root cause. -/
theorem Receipt.WellFormed.evidenceWithoutCauseProof
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.exactLineageVerified = true ∧
      receipt.sourceFindingEvidencePreserved = true ∧
      receipt.taxonomyComplete = true ∧
      receipt.typedErrorTreatedAsCauseProof = false :=
  ⟨h.exactLineage, h.findingsPreserved, h.taxonomyCompleteRecorded, h.noCauseProof⟩

end KUOS.CodeAI.TypedErrorClassificationV0_1
