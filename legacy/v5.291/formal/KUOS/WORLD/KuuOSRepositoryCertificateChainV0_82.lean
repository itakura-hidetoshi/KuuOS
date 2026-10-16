import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryCertificateChainV0_82

structure RevisionStepWitness where
  previousRecordBound : Prop
  sequenceIdentityBound : Prop
  parentRevisionBound : Prop
  previousSnapshotBound : Prop
  changedPathsExact : Prop
  currentRevisionFresh : Prop
  currentNormalFormPreserved : Prop

structure RevisionStepWitness.Valid
    (witness : RevisionStepWitness) : Prop where
  previousRecordBound : witness.previousRecordBound
  sequenceIdentityBound : witness.sequenceIdentityBound
  parentRevisionBound : witness.parentRevisionBound
  previousSnapshotBound : witness.previousSnapshotBound
  changedPathsExact : witness.changedPathsExact
  currentRevisionFresh : witness.currentRevisionFresh
  currentNormalFormPreserved : witness.currentNormalFormPreserved

structure CertificateSequenceWitness where
  finiteRevisionSequence : Prop
  boundedLength : Prop
  recordDigestsLinked : Prop
  revisionIdentifiersUnique : Prop
  allExtendedRecordsPreserveNormalForm : Prop

structure CertificateSequenceWitness.Valid
    (witness : CertificateSequenceWitness) : Prop where
  finiteRevisionSequence : witness.finiteRevisionSequence
  boundedLength : witness.boundedLength
  recordDigestsLinked : witness.recordDigestsLinked
  revisionIdentifiersUnique : witness.revisionIdentifiersUnique
  allExtendedRecordsPreserveNormalForm :
    witness.allExtendedRecordsPreserveNormalForm

theorem valid_revision_step_is_exactly_bound
    (witness : RevisionStepWitness)
    (h : witness.Valid) :
    witness.previousRecordBound ∧
      witness.sequenceIdentityBound ∧
      witness.parentRevisionBound ∧
      witness.previousSnapshotBound ∧
      witness.changedPathsExact ∧
      witness.currentRevisionFresh ∧
      witness.currentNormalFormPreserved := by
  exact ⟨h.previousRecordBound, h.sequenceIdentityBound,
    h.parentRevisionBound, h.previousSnapshotBound,
    h.changedPathsExact, h.currentRevisionFresh,
    h.currentNormalFormPreserved⟩

theorem valid_certificate_sequence_is_bounded_and_linked
    (witness : CertificateSequenceWitness)
    (h : witness.Valid) :
    witness.finiteRevisionSequence ∧
      witness.boundedLength ∧
      witness.recordDigestsLinked ∧
      witness.revisionIdentifiersUnique ∧
      witness.allExtendedRecordsPreserveNormalForm := by
  exact ⟨h.finiteRevisionSequence, h.boundedLength,
    h.recordDigestsLinked, h.revisionIdentifiersUnique,
    h.allExtendedRecordsPreserveNormalForm⟩

end KUOS.WORLD.KuuOSRepositoryCertificateChainV0_82
