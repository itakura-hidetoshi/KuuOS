import Mathlib

namespace KUOS.CodeAI.GeneratedPatchErrorReductionComparativeReplayEvaluationV0_1

/-- A bounded metric vector extracted from one completed replay evaluation. -/
structure ReplayMetrics where
  independentVerificationPassRateBasisPoints : Nat
  verifiedPatchCount : Nat
  typecheckFirstFailureCount : Nat
  repeatedErrorFingerprintCount : Nat
  casesWithRepeatedErrorFingerprint : Nat
  repairCyclesPerVerifiedPatchBasisPoints : Nat
  providerCallsPerVerifiedPatchBasisPoints : Nat
  generatedOutputBytesPerVerifiedPatchBasisPoints : Nat
  deriving DecidableEq, Repr

/-- Signed successor-minus-baseline delta. -/
def signedDelta (successor baseline : Nat) : Int :=
  Int.ofNat successor - Int.ofNat baseline

/-- Explicit signed threshold policy for comparative replay confirmation. -/
structure ReductionPolicy where
  minimumIndependentVerificationPassRateDeltaBasisPoints : Int
  minimumVerifiedPatchCountDelta : Int
  maximumTypecheckFirstFailureCountDelta : Int
  maximumRepeatedErrorFingerprintCountDelta : Int
  maximumCasesWithRepeatedErrorFingerprintDelta : Int
  maximumRepairCyclesPerVerifiedPatchDeltaBasisPoints : Int
  maximumProviderCallsPerVerifiedPatchDeltaBasisPoints : Int
  maximumGeneratedOutputBytesPerVerifiedPatchDeltaBasisPoints : Int
  deriving DecidableEq, Repr

/--
A comparison confirms bounded error reduction only when all eight explicit
successor-minus-baseline thresholds hold.
-/
def ReductionConfirmed
    (baseline successor : ReplayMetrics)
    (policy : ReductionPolicy) : Prop :=
  policy.minimumIndependentVerificationPassRateDeltaBasisPoints ≤
      signedDelta
        successor.independentVerificationPassRateBasisPoints
        baseline.independentVerificationPassRateBasisPoints ∧
  policy.minimumVerifiedPatchCountDelta ≤
      signedDelta successor.verifiedPatchCount baseline.verifiedPatchCount ∧
  signedDelta
      successor.typecheckFirstFailureCount
      baseline.typecheckFirstFailureCount ≤
    policy.maximumTypecheckFirstFailureCountDelta ∧
  signedDelta
      successor.repeatedErrorFingerprintCount
      baseline.repeatedErrorFingerprintCount ≤
    policy.maximumRepeatedErrorFingerprintCountDelta ∧
  signedDelta
      successor.casesWithRepeatedErrorFingerprint
      baseline.casesWithRepeatedErrorFingerprint ≤
    policy.maximumCasesWithRepeatedErrorFingerprintDelta ∧
  signedDelta
      successor.repairCyclesPerVerifiedPatchBasisPoints
      baseline.repairCyclesPerVerifiedPatchBasisPoints ≤
    policy.maximumRepairCyclesPerVerifiedPatchDeltaBasisPoints ∧
  signedDelta
      successor.providerCallsPerVerifiedPatchBasisPoints
      baseline.providerCallsPerVerifiedPatchBasisPoints ≤
    policy.maximumProviderCallsPerVerifiedPatchDeltaBasisPoints ∧
  signedDelta
      successor.generatedOutputBytesPerVerifiedPatchBasisPoints
      baseline.generatedOutputBytesPerVerifiedPatchBasisPoints ≤
    policy.maximumGeneratedOutputBytesPerVerifiedPatchDeltaBasisPoints

instance instDecidableReductionConfirmed
    (baseline successor : ReplayMetrics)
    (policy : ReductionPolicy) :
    Decidable (ReductionConfirmed baseline successor policy) := by
  unfold ReductionConfirmed signedDelta
  infer_instance

theorem confirmed_verification_rate_floor
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    policy.minimumIndependentVerificationPassRateDeltaBasisPoints ≤
      signedDelta
        successor.independentVerificationPassRateBasisPoints
        baseline.independentVerificationPassRateBasisPoints :=
  hConfirmed.1

theorem confirmed_verified_patch_floor
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    policy.minimumVerifiedPatchCountDelta ≤
      signedDelta successor.verifiedPatchCount baseline.verifiedPatchCount :=
  hConfirmed.2.1

theorem confirmed_typecheck_failure_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.typecheckFirstFailureCount
        baseline.typecheckFirstFailureCount ≤
      policy.maximumTypecheckFirstFailureCountDelta :=
  hConfirmed.2.2.1

theorem confirmed_repeated_fingerprint_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.repeatedErrorFingerprintCount
        baseline.repeatedErrorFingerprintCount ≤
      policy.maximumRepeatedErrorFingerprintCountDelta :=
  hConfirmed.2.2.2.1

theorem confirmed_repeated_case_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.casesWithRepeatedErrorFingerprint
        baseline.casesWithRepeatedErrorFingerprint ≤
      policy.maximumCasesWithRepeatedErrorFingerprintDelta :=
  hConfirmed.2.2.2.2.1

theorem confirmed_repair_efficiency_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.repairCyclesPerVerifiedPatchBasisPoints
        baseline.repairCyclesPerVerifiedPatchBasisPoints ≤
      policy.maximumRepairCyclesPerVerifiedPatchDeltaBasisPoints :=
  hConfirmed.2.2.2.2.2.1

theorem confirmed_provider_efficiency_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.providerCallsPerVerifiedPatchBasisPoints
        baseline.providerCallsPerVerifiedPatchBasisPoints ≤
      policy.maximumProviderCallsPerVerifiedPatchDeltaBasisPoints :=
  hConfirmed.2.2.2.2.2.2.1

theorem confirmed_output_efficiency_ceiling
    {baseline successor : ReplayMetrics}
    {policy : ReductionPolicy}
    (hConfirmed : ReductionConfirmed baseline successor policy) :
    signedDelta
        successor.generatedOutputBytesPerVerifiedPatchBasisPoints
        baseline.generatedOutputBytesPerVerifiedPatchBasisPoints ≤
      policy.maximumGeneratedOutputBytesPerVerifiedPatchDeltaBasisPoints :=
  hConfirmed.2.2.2.2.2.2.2

inductive ComparisonDecision where
  | confirmed
  | notConfirmed
  deriving DecidableEq, Repr

/-- A valid non-confirmation remains a measurement, not a rejection. -/
def treatedAsRejection : ComparisonDecision → Bool
  | .confirmed => false
  | .notConfirmed => false

theorem not_confirmed_is_not_rejection :
    treatedAsRejection .notConfirmed = false :=
  rfl

/-- Effects, authority, and epistemic overclaims remain outside comparison. -/
structure Boundary where
  historicalCodeReexecuted : Bool
  providerInvoked : Bool
  verificationRunnerInvoked : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  networkAccessed : Bool
  secretMaterialRead : Bool
  selectionAuthorityGranted : Bool
  successorStageAuthorityGranted : Bool
  correctnessProofClaimed : Bool
  probabilityClaimed : Bool
  datasetUnbiasednessClaimed : Bool
  deriving DecidableEq, Repr

def boundaryPreserved (boundary : Boundary) : Prop :=
  boundary.historicalCodeReexecuted = false ∧
  boundary.providerInvoked = false ∧
  boundary.verificationRunnerInvoked = false ∧
  boundary.repositoryMutationPerformed = false ∧
  boundary.gitEffectPerformed = false ∧
  boundary.networkAccessed = false ∧
  boundary.secretMaterialRead = false ∧
  boundary.selectionAuthorityGranted = false ∧
  boundary.successorStageAuthorityGranted = false ∧
  boundary.correctnessProofClaimed = false ∧
  boundary.probabilityClaimed = false ∧
  boundary.datasetUnbiasednessClaimed = false

instance instDecidableBoundaryPreserved (boundary : Boundary) :
    Decidable (boundaryPreserved boundary) := by
  unfold boundaryPreserved
  infer_instance

/-! ### Actual post-roadmap comparative replay specialization -/

def actualBaseline : ReplayMetrics :=
  {
    independentVerificationPassRateBasisPoints := 10000
    verifiedPatchCount := 2
    typecheckFirstFailureCount := 1
    repeatedErrorFingerprintCount := 1
    casesWithRepeatedErrorFingerprint := 2
    repairCyclesPerVerifiedPatchBasisPoints := 5000
    providerCallsPerVerifiedPatchBasisPoints := 30000
    generatedOutputBytesPerVerifiedPatchBasisPoints := 15000000
  }

def actualSuccessor : ReplayMetrics :=
  {
    independentVerificationPassRateBasisPoints := 10000
    verifiedPatchCount := 3
    typecheckFirstFailureCount := 0
    repeatedErrorFingerprintCount := 0
    casesWithRepeatedErrorFingerprint := 0
    repairCyclesPerVerifiedPatchBasisPoints := 3333
    providerCallsPerVerifiedPatchBasisPoints := 16666
    generatedOutputBytesPerVerifiedPatchBasisPoints := 8833333
  }

def actualPolicy : ReductionPolicy :=
  {
    minimumIndependentVerificationPassRateDeltaBasisPoints := 0
    minimumVerifiedPatchCountDelta := 1
    maximumTypecheckFirstFailureCountDelta := -1
    maximumRepeatedErrorFingerprintCountDelta := -1
    maximumCasesWithRepeatedErrorFingerprintDelta := -2
    maximumRepairCyclesPerVerifiedPatchDeltaBasisPoints := 0
    maximumProviderCallsPerVerifiedPatchDeltaBasisPoints := 0
    maximumGeneratedOutputBytesPerVerifiedPatchDeltaBasisPoints := 0
  }

theorem actual_verification_rate_delta :
    signedDelta
        actualSuccessor.independentVerificationPassRateBasisPoints
        actualBaseline.independentVerificationPassRateBasisPoints = 0 := by
  native_decide

theorem actual_verified_patch_delta :
    signedDelta actualSuccessor.verifiedPatchCount actualBaseline.verifiedPatchCount = 1 := by
  native_decide

theorem actual_typecheck_first_failure_delta :
    signedDelta
        actualSuccessor.typecheckFirstFailureCount
        actualBaseline.typecheckFirstFailureCount = -1 := by
  native_decide

theorem actual_repeated_error_case_delta :
    signedDelta
        actualSuccessor.casesWithRepeatedErrorFingerprint
        actualBaseline.casesWithRepeatedErrorFingerprint = -2 := by
  native_decide

theorem actual_generated_patch_error_reduction_confirmed :
    ReductionConfirmed actualBaseline actualSuccessor actualPolicy := by
  native_decide

def actualBoundary : Boundary :=
  {
    historicalCodeReexecuted := false
    providerInvoked := false
    verificationRunnerInvoked := false
    repositoryMutationPerformed := false
    gitEffectPerformed := false
    networkAccessed := false
    secretMaterialRead := false
    selectionAuthorityGranted := false
    successorStageAuthorityGranted := false
    correctnessProofClaimed := false
    probabilityClaimed := false
    datasetUnbiasednessClaimed := false
  }

theorem actual_boundary_preserved :
    boundaryPreserved actualBoundary := by
  native_decide

end KUOS.CodeAI.GeneratedPatchErrorReductionComparativeReplayEvaluationV0_1
