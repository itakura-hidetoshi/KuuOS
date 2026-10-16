import Mathlib

namespace KUOS.CodeAI.TemporalHoldoutReplayCorpusV0_1

inductive Split where
  | development
  | holdout
  deriving DecidableEq, Repr

structure ReplayEntry where
  observedEpoch : Nat
  split : Split
  labelsAvailableToCandidateGeneration : Bool
  usedForThresholdTuning : Bool
  usedForMemoryTraining : Bool
  usedForPromptSelection : Bool
  usedForModelSelection : Bool
  deriving DecidableEq, Repr

/-- Development entries precede the cutoff and holdout entries follow it. -/
def TemporallyOrdered (cutoff : Nat) (entry : ReplayEntry) : Prop :=
  match entry.split with
  | .development => entry.observedEpoch ≤ cutoff
  | .holdout => cutoff < entry.observedEpoch

/-- A holdout entry remains unavailable to all adaptation surfaces. -/
def HoldoutProtected (entry : ReplayEntry) : Prop :=
  entry.split = .holdout →
    entry.labelsAvailableToCandidateGeneration = false ∧
    entry.usedForThresholdTuning = false ∧
    entry.usedForMemoryTraining = false ∧
    entry.usedForPromptSelection = false ∧
    entry.usedForModelSelection = false

/-- Every entry in a sealed corpus respects time and holdout protection. -/
def CorpusValid (cutoff : Nat) (entries : List ReplayEntry) : Prop :=
  (∀ entry ∈ entries, TemporallyOrdered cutoff entry) ∧
  (∀ entry ∈ entries, HoldoutProtected entry)

instance instDecidableTemporallyOrdered (cutoff : Nat) (entry : ReplayEntry) :
    Decidable (TemporallyOrdered cutoff entry) := by
  unfold TemporallyOrdered
  split <;> infer_instance

instance instDecidableHoldoutProtected (entry : ReplayEntry) :
    Decidable (HoldoutProtected entry) := by
  unfold HoldoutProtected
  infer_instance

instance instDecidableCorpusValid (cutoff : Nat) (entries : List ReplayEntry) :
    Decidable (CorpusValid cutoff entries) := by
  unfold CorpusValid
  infer_instance

theorem holdout_after_cutoff
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hHoldout : entry.split = .holdout) :
    cutoff < entry.observedEpoch := by
  have hOrdered := hValid.1 entry hMember
  simp [TemporallyOrdered, hHoldout] at hOrdered
  exact hOrdered

theorem development_not_after_cutoff
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hDevelopment : entry.split = .development) :
    entry.observedEpoch ≤ cutoff := by
  have hOrdered := hValid.1 entry hMember
  simp [TemporallyOrdered, hDevelopment] at hOrdered
  exact hOrdered

theorem holdout_not_used_for_threshold_tuning
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hHoldout : entry.split = .holdout) :
    entry.usedForThresholdTuning = false := by
  exact (hValid.2 entry hMember hHoldout).2.1

theorem holdout_not_used_for_memory_training
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hHoldout : entry.split = .holdout) :
    entry.usedForMemoryTraining = false := by
  exact (hValid.2 entry hMember hHoldout).2.2.1

theorem holdout_not_used_for_prompt_selection
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hHoldout : entry.split = .holdout) :
    entry.usedForPromptSelection = false := by
  exact (hValid.2 entry hMember hHoldout).2.2.2.1

theorem holdout_not_used_for_model_selection
    {cutoff : Nat}
    {entries : List ReplayEntry}
    {entry : ReplayEntry}
    (hValid : CorpusValid cutoff entries)
    (hMember : entry ∈ entries)
    (hHoldout : entry.split = .holdout) :
    entry.usedForModelSelection = false := by
  exact (hValid.2 entry hMember hHoldout).2.2.2.2

structure SplitIdentity where
  developmentCaseIds : Finset Nat
  holdoutCaseIds : Finset Nat
  developmentIssueIds : Finset Nat
  holdoutIssueIds : Finset Nat
  developmentReplayIds : Finset Nat
  holdoutReplayIds : Finset Nat
  deriving DecidableEq

/-- No case, issue, or replay identity crosses the temporal split. -/
def SplitDisjoint (identity : SplitIdentity) : Prop :=
  Disjoint identity.developmentCaseIds identity.holdoutCaseIds ∧
  Disjoint identity.developmentIssueIds identity.holdoutIssueIds ∧
  Disjoint identity.developmentReplayIds identity.holdoutReplayIds

instance instDecidableSplitDisjoint (identity : SplitIdentity) :
    Decidable (SplitDisjoint identity) := by
  unfold SplitDisjoint
  infer_instance

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
  representativenessClaimed : Bool
  randomnessClaimed : Bool
  unbiasednessClaimed : Bool
  correctnessProofClaimed : Bool
  deriving DecidableEq, Repr

/-- Corpus sealing has no execution authority or statistical overclaim. -/
def BoundaryPreserved (boundary : Boundary) : Prop :=
  boundary.historicalCodeReexecuted = false ∧
  boundary.providerInvoked = false ∧
  boundary.verificationRunnerInvoked = false ∧
  boundary.repositoryMutationPerformed = false ∧
  boundary.gitEffectPerformed = false ∧
  boundary.networkAccessed = false ∧
  boundary.secretMaterialRead = false ∧
  boundary.selectionAuthorityGranted = false ∧
  boundary.successorStageAuthorityGranted = false ∧
  boundary.representativenessClaimed = false ∧
  boundary.randomnessClaimed = false ∧
  boundary.unbiasednessClaimed = false ∧
  boundary.correctnessProofClaimed = false

instance instDecidableBoundaryPreserved (boundary : Boundary) :
    Decidable (BoundaryPreserved boundary) := by
  unfold BoundaryPreserved
  infer_instance

/-! ### Actual reference temporal holdout corpus -/

def developmentEntry (epoch : Nat) : ReplayEntry :=
  {
    observedEpoch := epoch
    split := .development
    labelsAvailableToCandidateGeneration := true
    usedForThresholdTuning := true
    usedForMemoryTraining := true
    usedForPromptSelection := true
    usedForModelSelection := true
  }

def holdoutEntry (epoch : Nat) : ReplayEntry :=
  {
    observedEpoch := epoch
    split := .holdout
    labelsAvailableToCandidateGeneration := false
    usedForThresholdTuning := false
    usedForMemoryTraining := false
    usedForPromptSelection := false
    usedForModelSelection := false
  }

def actualEntries : List ReplayEntry :=
  [developmentEntry 80, developmentEntry 85, developmentEntry 90,
   holdoutEntry 110, holdoutEntry 115, holdoutEntry 120]

def actualSplitIdentity : SplitIdentity :=
  {
    developmentCaseIds := {1, 2, 3}
    holdoutCaseIds := {10, 11, 12}
    developmentIssueIds := {21, 22, 23}
    holdoutIssueIds := {30, 31, 32}
    developmentReplayIds := {41, 42, 43}
    holdoutReplayIds := {50, 51, 52}
  }

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
    representativenessClaimed := false
    randomnessClaimed := false
    unbiasednessClaimed := false
    correctnessProofClaimed := false
  }

theorem actual_temporal_holdout_corpus_valid :
    CorpusValid 100 actualEntries := by
  native_decide

theorem actual_split_disjoint :
    SplitDisjoint actualSplitIdentity := by
  native_decide

theorem actual_boundary_preserved :
    BoundaryPreserved actualBoundary := by
  native_decide

end KUOS.CodeAI.TemporalHoldoutReplayCorpusV0_1
