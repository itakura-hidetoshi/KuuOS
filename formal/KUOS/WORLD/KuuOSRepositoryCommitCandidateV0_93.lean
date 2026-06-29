import KUOS.WORLD.KuuOSRepositoryAtomicApplicationV0_92

namespace KUOS.WORLD.KuuOSRepositoryCommitCandidateV0_93

structure CommitCandidateWitness where
  applicationReceiptValid : Prop
  applicationApplied : Prop
  finalSnapshotBound : Prop
  singleParentBound : Prop
  blobsExact : Prop
  treesExact : Prop
  rootTreeExact : Prop
  identitiesValid : Prop
  messageValid : Prop
  commitPayloadExact : Prop
  candidateOIDExact : Prop
  deterministicCandidate : Prop
  objectDatabaseWritePerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  commitCreated : Bool
  referenceMutated : Bool
  signingPerformed : Bool

structure CommitCandidateWitness.Valid
    (witness : CommitCandidateWitness) : Prop where
  applicationReceiptValid : witness.applicationReceiptValid
  applicationApplied : witness.applicationApplied
  finalSnapshotBound : witness.finalSnapshotBound
  singleParentBound : witness.singleParentBound
  blobsExact : witness.blobsExact
  treesExact : witness.treesExact
  rootTreeExact : witness.rootTreeExact
  identitiesValid : witness.identitiesValid
  messageValid : witness.messageValid
  commitPayloadExact : witness.commitPayloadExact
  candidateOIDExact : witness.candidateOIDExact
  deterministicCandidate : witness.deterministicCandidate
  objectDatabaseWritePerformed :
    witness.objectDatabaseWritePerformed = false
  indexWritePerformed : witness.indexWritePerformed = false
  workingTreeWritePerformed : witness.workingTreeWritePerformed = false
  commitCreated : witness.commitCreated = false
  referenceMutated : witness.referenceMutated = false
  signingPerformed : witness.signingPerformed = false


theorem valid_candidate_binds_application_and_parent
    (witness : CommitCandidateWitness)
    (h : witness.Valid) :
    witness.applicationReceiptValid ∧ witness.applicationApplied ∧
      witness.finalSnapshotBound ∧ witness.singleParentBound := by
  exact ⟨h.applicationReceiptValid, h.applicationApplied,
    h.finalSnapshotBound, h.singleParentBound⟩


theorem valid_candidate_has_exact_object_description
    (witness : CommitCandidateWitness)
    (h : witness.Valid) :
    witness.blobsExact ∧ witness.treesExact ∧ witness.rootTreeExact ∧
      witness.commitPayloadExact ∧ witness.candidateOIDExact := by
  exact ⟨h.blobsExact, h.treesExact, h.rootTreeExact,
    h.commitPayloadExact, h.candidateOIDExact⟩


theorem valid_candidate_has_canonical_metadata
    (witness : CommitCandidateWitness)
    (h : witness.Valid) :
    witness.identitiesValid ∧ witness.messageValid ∧
      witness.deterministicCandidate := by
  exact ⟨h.identitiesValid, h.messageValid, h.deterministicCandidate⟩


theorem valid_candidate_performs_no_repository_write
    (witness : CommitCandidateWitness)
    (h : witness.Valid) :
    witness.objectDatabaseWritePerformed = false ∧
      witness.indexWritePerformed = false ∧
      witness.workingTreeWritePerformed = false := by
  exact ⟨h.objectDatabaseWritePerformed, h.indexWritePerformed,
    h.workingTreeWritePerformed⟩


theorem valid_candidate_grants_no_commit_or_reference_effect
    (witness : CommitCandidateWitness)
    (h : witness.Valid) :
    witness.commitCreated = false ∧ witness.referenceMutated = false ∧
      witness.signingPerformed = false := by
  exact ⟨h.commitCreated, h.referenceMutated, h.signingPerformed⟩


structure CandidateDerivation (Input OID : Type) where
  derive : Input → OID


theorem same_input_has_same_candidate_oid
    {Input OID : Type}
    (derivation : CandidateDerivation Input OID)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCommitCandidateV0_93
