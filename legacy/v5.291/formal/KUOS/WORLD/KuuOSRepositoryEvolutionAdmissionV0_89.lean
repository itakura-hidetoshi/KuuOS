import KUOS.WORLD.KuuOSRepositorySelfEvolutionShadowV0_88

namespace KUOS.WORLD.KuuOSRepositoryEvolutionAdmissionV0_89

open KUOS.WORLD.KuuOSRepositorySelfEvolutionShadowV0_88


structure ReplaySignature (Candidate Source Snapshot NormalForm : Type*) where
  selectedCandidates : Finset Candidate
  sourceBindings : Finset (Source × Snapshot)
  shadowSnapshots : Finset Snapshot
  normalForms : Finset NormalForm


structure ShadowReplay
    (Candidate Source Snapshot NormalForm : Type*) where
  signature : ReplaySignature Candidate Source Snapshot NormalForm
  issuedAt : Nat
  shadowPass : Bool
  stableNoChange : Bool


def ShadowReplay.Fresh
    {Candidate Source Snapshot NormalForm : Type*}
    (replay : ShadowReplay Candidate Source Snapshot NormalForm)
    (evaluatedAt maxAge : Nat) : Prop :=
  replay.issuedAt ≤ evaluatedAt ∧ evaluatedAt - replay.issuedAt ≤ maxAge


structure AdmissionBatch
    (Candidate Source Snapshot NormalForm : Type*)
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm] where
  replays : List (ShadowReplay Candidate Source Snapshot NormalForm)
  reference : ReplaySignature Candidate Source Snapshot NormalForm
  requiredReplayCount : Nat
  evaluatedAt : Nat
  maxCertificateAge : Nat
  currentSourceBindings : Finset (Source × Snapshot)
  externalApprovalRequired : Bool
  externalApprovalGranted : Bool
  patchApplicationAuthority : Bool
  commitAuthority : Bool
  referenceMutationAuthority : Bool


def AdmissionBatch.Reproducible
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm) : Prop :=
  ∀ replay ∈ batch.replays, replay.signature = batch.reference


def AdmissionBatch.Admissible
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm) : Prop :=
  2 ≤ batch.requiredReplayCount ∧
    batch.requiredReplayCount ≤ batch.replays.length ∧
    (∀ replay ∈ batch.replays, replay.shadowPass = true) ∧
    batch.Reproducible ∧
    (∀ replay ∈ batch.replays,
      replay.Fresh batch.evaluatedAt batch.maxCertificateAge) ∧
    batch.currentSourceBindings = batch.reference.sourceBindings ∧
    batch.externalApprovalRequired = true ∧
    batch.externalApprovalGranted = false ∧
    batch.patchApplicationAuthority = false ∧
    batch.commitAuthority = false ∧
    batch.referenceMutationAuthority = false


structure StableAdmissionWitness where
  selectedCandidatesEmpty : Prop
  repeatedStableReceipts : Prop
  admissionProposalGenerated : Bool
  patchApplicationAuthority : Bool
  commitAuthority : Bool
  referenceMutationAuthority : Bool


structure StableAdmissionWitness.Valid
    (witness : StableAdmissionWitness) : Prop where
  selectedCandidatesEmpty : witness.selectedCandidatesEmpty
  repeatedStableReceipts : witness.repeatedStableReceipts
  admissionProposalGenerated : witness.admissionProposalGenerated = false
  patchApplicationAuthority : witness.patchApplicationAuthority = false
  commitAuthority : witness.commitAuthority = false
  referenceMutationAuthority : witness.referenceMutationAuthority = false


theorem admissible_batch_has_at_least_two_replays
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible) :
    2 ≤ batch.replays.length := by
  exact Nat.le_trans h.1 h.2.1


theorem admissible_replay_is_shadow_pass
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible)
    {replay : ShadowReplay Candidate Source Snapshot NormalForm}
    (hReplay : replay ∈ batch.replays) :
    replay.shadowPass = true := by
  exact h.2.2.1 replay hReplay


theorem admissible_replay_matches_reference
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible)
    {replay : ShadowReplay Candidate Source Snapshot NormalForm}
    (hReplay : replay ∈ batch.replays) :
    replay.signature = batch.reference := by
  exact h.2.2.2.1 replay hReplay


theorem admissible_replay_is_fresh
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible)
    {replay : ShadowReplay Candidate Source Snapshot NormalForm}
    (hReplay : replay ∈ batch.replays) :
    replay.Fresh batch.evaluatedAt batch.maxCertificateAge := by
  exact h.2.2.2.2.1 replay hReplay


theorem admissible_batch_preserves_source_bindings
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible) :
    batch.currentSourceBindings = batch.reference.sourceBindings := by
  exact h.2.2.2.2.2.1


theorem admissible_batch_still_requires_external_approval
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible) :
    batch.externalApprovalRequired = true ∧
      batch.externalApprovalGranted = false := by
  exact ⟨h.2.2.2.2.2.2.1, h.2.2.2.2.2.2.2.1⟩


theorem admissible_batch_grants_no_repository_authority
    {Candidate Source Snapshot NormalForm : Type*}
    [DecidableEq Candidate]
    [DecidableEq Source]
    [DecidableEq Snapshot]
    [DecidableEq NormalForm]
    (batch : AdmissionBatch Candidate Source Snapshot NormalForm)
    (h : batch.Admissible) :
    batch.patchApplicationAuthority = false ∧
      batch.commitAuthority = false ∧
      batch.referenceMutationAuthority = false := by
  exact ⟨h.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2⟩


theorem valid_stable_admission_generates_no_proposal
    (witness : StableAdmissionWitness)
    (h : witness.Valid) :
    witness.admissionProposalGenerated = false ∧
      witness.patchApplicationAuthority = false ∧
      witness.commitAuthority = false ∧
      witness.referenceMutationAuthority = false := by
  exact ⟨h.admissionProposalGenerated, h.patchApplicationAuthority,
    h.commitAuthority, h.referenceMutationAuthority⟩

end KUOS.WORLD.KuuOSRepositoryEvolutionAdmissionV0_89
