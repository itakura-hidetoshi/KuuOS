import Mathlib

namespace KUOS.CodeAI.SubtaskLevelVersionBoundMemoryV0_1

inductive SubtaskKind
  | localize
  | diagnose
  | edit
  | verify
  deriving DecidableEq, BEq

inductive MemoryOutcome
  | verifiedUseful
  | verifiedNotUseful
  | inconclusive
  deriving DecidableEq, BEq

structure Binding where
  repositoryVersion : Nat
  sourceTree : Nat
  temporalCorpus : Nat
  contextPack : Nat
  verifierEnsemble : Nat
  subtaskKind : SubtaskKind
  subtaskContract : Nat
  predecessorOutput : Nat
  dependencySlice : Nat
  toolchain : Nat
  environment : Nat
  memoryPolicy : Nat
  deriving DecidableEq

structure MemoryEntry where
  binding : Binding
  outcome : MemoryOutcome
  derivedFromHoldout : Bool
  superseded : Bool
  repositoryMutated : Bool
  candidateSelected : Bool
  repairExecuted : Bool
  executionAuthority : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  futureSuccessClaimed : Bool
  deriving DecidableEq

def BoundaryPreserved (entry : MemoryEntry) : Prop :=
  entry.repositoryMutated = false ∧
  entry.candidateSelected = false ∧
  entry.repairExecuted = false ∧
  entry.executionAuthority = false ∧
  entry.gitAuthority = false ∧
  entry.correctnessClaimed = false ∧
  entry.futureSuccessClaimed = false

def Eligible (query : Binding) (entry : MemoryEntry) : Prop :=
  entry.binding = query ∧
  entry.outcome = .verifiedUseful ∧
  entry.derivedFromHoldout = false ∧
  entry.superseded = false ∧
  BoundaryPreserved entry

theorem eligible_exact_binding
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    entry.binding = query := by
  exact h.1

theorem eligible_subtask_aligned
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    entry.binding.subtaskKind = query.subtaskKind := by
  simpa [eligible_exact_binding h]

theorem eligible_dependency_aligned
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    entry.binding.dependencySlice = query.dependencySlice := by
  simpa [eligible_exact_binding h]

theorem eligible_not_holdout_derived
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    entry.derivedFromHoldout = false := by
  exact h.2.2.1

theorem eligible_not_superseded
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    entry.superseded = false := by
  exact h.2.2.2.1

theorem eligible_boundary_preserved
    {query : Binding} {entry : MemoryEntry}
    (h : Eligible query entry) :
    BoundaryPreserved entry := by
  exact h.2.2.2.2

theorem repository_version_mismatch_forbids_transfer
    {query : Binding} {entry : MemoryEntry}
    (hMismatch : entry.binding.repositoryVersion ≠ query.repositoryVersion) :
    ¬ Eligible query entry := by
  intro h
  exact hMismatch (congrArg Binding.repositoryVersion h.1)

theorem subtask_mismatch_forbids_transfer
    {query : Binding} {entry : MemoryEntry}
    (hMismatch : entry.binding.subtaskKind ≠ query.subtaskKind) :
    ¬ Eligible query entry := by
  intro h
  exact hMismatch (congrArg Binding.subtaskKind h.1)

theorem dependency_mismatch_forbids_transfer
    {query : Binding} {entry : MemoryEntry}
    (hMismatch : entry.binding.dependencySlice ≠ query.dependencySlice) :
    ¬ Eligible query entry := by
  intro h
  exact hMismatch (congrArg Binding.dependencySlice h.1)

theorem holdout_derived_forbids_transfer
    {query : Binding} {entry : MemoryEntry}
    (hHoldout : entry.derivedFromHoldout = true) :
    ¬ Eligible query entry := by
  intro h
  have hFalse := eligible_not_holdout_derived h
  simp [hHoldout] at hFalse

def referenceQuery : Binding where
  repositoryVersion := 1330
  sourceTree := 230
  temporalCorpus := 1
  contextPack := 2
  verifierEnsemble := 3
  subtaskKind := .verify
  subtaskContract := 4
  predecessorOutput := 5
  dependencySlice := 6
  toolchain := 7
  environment := 8
  memoryPolicy := 9

def referenceCurrent : MemoryEntry where
  binding := referenceQuery
  outcome := .verifiedUseful
  derivedFromHoldout := false
  superseded := false
  repositoryMutated := false
  candidateSelected := false
  repairExecuted := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false
  futureSuccessClaimed := false

def referenceStale : MemoryEntry where
  binding := { referenceQuery with repositoryVersion := 1329 }
  outcome := .verifiedUseful
  derivedFromHoldout := false
  superseded := false
  repositoryMutated := false
  candidateSelected := false
  repairExecuted := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false
  futureSuccessClaimed := false

def referenceWrongSubtask : MemoryEntry where
  binding := { referenceQuery with subtaskKind := .edit }
  outcome := .verifiedUseful
  derivedFromHoldout := false
  superseded := false
  repositoryMutated := false
  candidateSelected := false
  repairExecuted := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false
  futureSuccessClaimed := false

def referenceHoldout : MemoryEntry where
  binding := referenceQuery
  outcome := .verifiedUseful
  derivedFromHoldout := true
  superseded := false
  repositoryMutated := false
  candidateSelected := false
  repairExecuted := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false
  futureSuccessClaimed := false

theorem referenceCurrent_eligible :
    Eligible referenceQuery referenceCurrent := by
  native_decide

theorem referenceStale_not_eligible :
    ¬ Eligible referenceQuery referenceStale := by
  native_decide

theorem referenceWrongSubtask_not_eligible :
    ¬ Eligible referenceQuery referenceWrongSubtask := by
  native_decide

theorem referenceHoldout_not_eligible :
    ¬ Eligible referenceQuery referenceHoldout := by
  native_decide

theorem referenceCurrent_preserves_boundary :
    BoundaryPreserved referenceCurrent := by
  exact eligible_boundary_preserved referenceCurrent_eligible

end KUOS.CodeAI.SubtaskLevelVersionBoundMemoryV0_1
