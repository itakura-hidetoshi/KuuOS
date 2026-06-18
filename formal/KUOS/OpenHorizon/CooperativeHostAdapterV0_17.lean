import Mathlib

namespace KUOS
namespace OpenHorizon

structure HostProjection where
  bundleGenerationBefore : ℕ
  bundleGenerationAfter : ℕ
  readOnly : bundleGenerationAfter = bundleGenerationBefore


theorem hostProjection_readOnly (projection : HostProjection) :
    projection.bundleGenerationAfter = projection.bundleGenerationBefore := by
  exact projection.readOnly


structure HostInvocationBound where
  jobsClaimed : ℕ
  slicesRun : ℕ
  jobsBounded : jobsClaimed ≤ 1
  slicesBounded : slicesRun ≤ 1


theorem hostInvocation_claims_at_most_one_job (invocation : HostInvocationBound) :
    invocation.jobsClaimed ≤ 1 := by
  exact invocation.jobsBounded


theorem hostInvocation_runs_at_most_one_slice (invocation : HostInvocationBound) :
    invocation.slicesRun ≤ 1 := by
  exact invocation.slicesBounded


structure HostLicense where
  valid : Bool
  claimAllowed : Bool
  boundedSliceAllowed : Bool
  executionRequiresLicense : valid = true → claimAllowed = true ∧ boundedSliceAllowed = true


theorem validHostLicense_allows_claim_and_slice (license : HostLicense)
    (h : license.valid = true) :
    license.claimAllowed = true ∧ license.boundedSliceAllowed = true := by
  exact license.executionRequiresLicense h


def recordInvocation (processed : Finset ℕ) (digest : ℕ) : Finset ℕ :=
  insert digest processed


theorem recordInvocation_idempotent (processed : Finset ℕ) (digest : ℕ) :
    recordInvocation (recordInvocation processed digest) digest =
      recordInvocation processed digest := by
  simp [recordInvocation]


structure HostAdapterHistory where
  invocationRecords : ℕ
  receiptRecords : ℕ
  aligned : invocationRecords = receiptRecords


def appendHostInvocation (history : HostAdapterHistory) : HostAdapterHistory where
  invocationRecords := history.invocationRecords + 1
  receiptRecords := history.receiptRecords + 1
  aligned := by simp [history.aligned]


theorem hostInvocationHistory_strict (history : HostAdapterHistory) :
    history.invocationRecords < (appendHostInvocation history).invocationRecords := by
  simp [appendHostInvocation]


theorem hostReceiptHistory_strict (history : HostAdapterHistory) :
    history.receiptRecords < (appendHostInvocation history).receiptRecords := by
  simp [appendHostInvocation]


structure ConnectorBoundary where
  runtimeConnectorCalls : ℕ
  noInternalConnectorCall : runtimeConnectorCalls = 0


theorem runtimeConnectorCall_forbidden (boundary : ConnectorBoundary) :
    boundary.runtimeConnectorCalls = 0 := by
  exact boundary.noInternalConnectorCall

end OpenHorizon
end KUOS
