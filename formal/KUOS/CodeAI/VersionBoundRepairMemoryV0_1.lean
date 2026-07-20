import Mathlib

namespace KUOS.CodeAI.VersionBoundRepairMemoryV0_1

/-- A repair-memory key is exact across repository, candidate, error, and environment. -/
structure VersionBinding where
  repositoryFullName : String
  sourceCommitSha : String
  sourceRepositorySnapshotDigest : String
  sourceCandidateDigest : String
  typedErrorDigest : String
  errorFingerprint : String
  classificationSchemaVersion : String
  toolchainDigest : String
  dependencyManifestDigest : String
  repairPolicyDigest : String
  deriving DecidableEq, Repr

/-- Historical repair outcomes remain evidence labels, not probabilities. -/
inductive RepairOutcome where
  | verifiedEffective
  | verifiedIneffective
  | inconclusive
  deriving DecidableEq, Repr

/-- One sealed historical repair-memory entry. -/
structure MemoryEntry where
  memoryEntryId : String
  binding : VersionBinding
  repairActionDigest : String
  verificationEvidenceDigest : String
  outcome : RepairOutcome
  deriving DecidableEq, Repr

/-- A query may consume only an exactly equal version binding. -/
def ExactMatch (entry : MemoryEntry) (query : VersionBinding) : Prop :=
  entry.binding = query

/-- A different source commit cannot be transferred as an exact repair hint. -/
theorem sourceCommitMismatchBlocksTransfer
    (entry : MemoryEntry) (query : VersionBinding)
    (h : entry.binding.sourceCommitSha ≠ query.sourceCommitSha) :
    ¬ ExactMatch entry query := by
  intro hMatch
  exact h (congrArg VersionBinding.sourceCommitSha hMatch)

/-- A different toolchain cannot be transferred as an exact repair hint. -/
theorem toolchainMismatchBlocksTransfer
    (entry : MemoryEntry) (query : VersionBinding)
    (h : entry.binding.toolchainDigest ≠ query.toolchainDigest) :
    ¬ ExactMatch entry query := by
  intro hMatch
  exact h (congrArg VersionBinding.toolchainDigest hMatch)

/-- A different dependency manifest cannot be transferred as an exact hint. -/
theorem dependencyMismatchBlocksTransfer
    (entry : MemoryEntry) (query : VersionBinding)
    (h : entry.binding.dependencyManifestDigest ≠ query.dependencyManifestDigest) :
    ¬ ExactMatch entry query := by
  intro hMatch
  exact h (congrArg VersionBinding.dependencyManifestDigest hMatch)

/-- A different repair policy cannot be transferred as an exact hint. -/
theorem repairPolicyMismatchBlocksTransfer
    (entry : MemoryEntry) (query : VersionBinding)
    (h : entry.binding.repairPolicyDigest ≠ query.repairPolicyDigest) :
    ¬ ExactMatch entry query := by
  intro hMatch
  exact h (congrArg VersionBinding.repairPolicyDigest hMatch)

/-- A different candidate or typed error cannot share an exact memory binding. -/
theorem candidateOrErrorMismatchBlocksTransfer
    (entry : MemoryEntry) (query : VersionBinding)
    (hCandidate : entry.binding.sourceCandidateDigest ≠ query.sourceCandidateDigest ∨
      entry.binding.typedErrorDigest ≠ query.typedErrorDigest) :
    ¬ ExactMatch entry query := by
  intro hMatch
  rcases hCandidate with h | h
  · exact h (congrArg VersionBinding.sourceCandidateDigest hMatch)
  · exact h (congrArg VersionBinding.typedErrorDigest hMatch)

/-- The memory receipt records lookup evidence while preserving all authority boundaries. -/
structure Receipt where
  entries : List MemoryEntry
  matchedEntries : List MemoryEntry
  exactVersionBindingVerified : Bool
  typedErrorCorrespondenceVerified : Bool
  independentVerificationVerified : Bool
  isolatedCandidateRepairVerified : Bool
  liveRepositoryUnchanged : Bool
  historyReadOnly : Bool
  memoryHintEmitted : Bool
  repairExecutedByMemory : Bool
  repositoryMutationPerformedByMemory : Bool
  gitEffectPerformedByMemory : Bool
  repairAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  historicalOutcomeTreatedAsProbability : Bool
  historicalSuccessTreatedAsFutureSuccessProof : Bool
  memoryHintTreatedAsCorrectnessProof : Bool
  versionMismatchTreatedAsTransferable : Bool
  deriving DecidableEq, Repr

/-- Well-formed memory may expose only exact matches and grants no downstream effect. -/
structure Receipt.WellFormed (receipt : Receipt) (query : VersionBinding) : Prop where
  exactBinding : receipt.exactVersionBindingVerified = true
  typedErrorCorrespondence : receipt.typedErrorCorrespondenceVerified = true
  independentVerification : receipt.independentVerificationVerified = true
  isolatedRepair : receipt.isolatedCandidateRepairVerified = true
  repositoryUnchanged : receipt.liveRepositoryUnchanged = true
  readOnlyHistory : receipt.historyReadOnly = true
  matchedExact : ∀ entry, entry ∈ receipt.matchedEntries → ExactMatch entry query
  matchedPreserved : ∀ entry, entry ∈ receipt.matchedEntries → entry ∈ receipt.entries
  noRepairExecution : receipt.repairExecutedByMemory = false
  noRepositoryMutation : receipt.repositoryMutationPerformedByMemory = false
  noGitEffect : receipt.gitEffectPerformedByMemory = false
  noRepairAuthority : receipt.repairAuthorityGranted = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noGitAuthority : receipt.gitAuthorityGranted = false
  noProbabilityClaim : receipt.historicalOutcomeTreatedAsProbability = false
  noFutureSuccessProof : receipt.historicalSuccessTreatedAsFutureSuccessProof = false
  noCorrectnessProof : receipt.memoryHintTreatedAsCorrectnessProof = false
  noMismatchTransfer : receipt.versionMismatchTreatedAsTransferable = false

/-- Every emitted memory hint is exactly version-bound. -/
theorem Receipt.WellFormed.matchedHintExact
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query)
    {entry : MemoryEntry}
    (hEntry : entry ∈ receipt.matchedEntries) :
    ExactMatch entry query :=
  h.matchedExact entry hEntry

/-- Matched history remains a preserved subset of the sealed memory entries. -/
theorem Receipt.WellFormed.matchedHintPreserved
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query)
    {entry : MemoryEntry}
    (hEntry : entry ∈ receipt.matchedEntries) :
    entry ∈ receipt.entries :=
  h.matchedPreserved entry hEntry

/-- Historical effectiveness is neither a probability nor a future-success theorem. -/
theorem Receipt.WellFormed.historicalTruthBoundary
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query) :
    receipt.historicalOutcomeTreatedAsProbability = false ∧
      receipt.historicalSuccessTreatedAsFutureSuccessProof = false ∧
      receipt.memoryHintTreatedAsCorrectnessProof = false :=
  ⟨h.noProbabilityClaim, h.noFutureSuccessProof, h.noCorrectnessProof⟩

/-- Version mismatch never becomes transferable by memory lookup. -/
theorem Receipt.WellFormed.versionMismatchBoundary
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query) :
    receipt.versionMismatchTreatedAsTransferable = false :=
  h.noMismatchTransfer

/-- Repair memory grants no repair, verification, execution, or Git authority. -/
theorem Receipt.WellFormed.authorityBoundary
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query) :
    receipt.repairAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.gitAuthorityGranted = false :=
  ⟨h.noRepairAuthority, h.noVerificationAuthority,
    h.noExecutionAuthority, h.noGitAuthority⟩

/-- Lookup is read-only and creates no repair, repository, or Git effect. -/
theorem Receipt.WellFormed.effectBoundary
    {receipt : Receipt} {query : VersionBinding}
    (h : receipt.WellFormed query) :
    receipt.historyReadOnly = true ∧
      receipt.repairExecutedByMemory = false ∧
      receipt.repositoryMutationPerformedByMemory = false ∧
      receipt.gitEffectPerformedByMemory = false :=
  ⟨h.readOnlyHistory, h.noRepairExecution,
    h.noRepositoryMutation, h.noGitEffect⟩

end KUOS.CodeAI.VersionBoundRepairMemoryV0_1
