import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryMergeCertificateV0_84

structure MergeObservationWitness where
  leftParentBound : Prop
  rightParentBound : Prop
  parentOrderExact : Prop
  changedPathsInventoryBound : Prop
  changedPathsDisjoint : Prop
  mergeSnapshotObjectBound : Prop
  workingTreeExcluded : Prop

structure MergeObservationWitness.Valid
    (witness : MergeObservationWitness) : Prop where
  leftParentBound : witness.leftParentBound
  rightParentBound : witness.rightParentBound
  parentOrderExact : witness.parentOrderExact
  changedPathsInventoryBound : witness.changedPathsInventoryBound
  changedPathsDisjoint : witness.changedPathsDisjoint
  mergeSnapshotObjectBound : witness.mergeSnapshotObjectBound
  workingTreeExcluded : witness.workingTreeExcluded

structure MergeCertificateWitness where
  commonRoot : Prop
  commonPrefixNonempty : Prop
  branchSuffixesDisjoint : Prop
  parentRecordsBound : Prop
  mergeObservationBound : Prop
  mergeNormalForm : Prop

structure MergeCertificateWitness.Valid
    (witness : MergeCertificateWitness) : Prop where
  commonRoot : witness.commonRoot
  commonPrefixNonempty : witness.commonPrefixNonempty
  branchSuffixesDisjoint : witness.branchSuffixesDisjoint
  parentRecordsBound : witness.parentRecordsBound
  mergeObservationBound : witness.mergeObservationBound
  mergeNormalForm : witness.mergeNormalForm

theorem valid_merge_observation_is_exact
    (witness : MergeObservationWitness)
    (h : witness.Valid) :
    witness.leftParentBound ∧
      witness.rightParentBound ∧
      witness.parentOrderExact ∧
      witness.changedPathsInventoryBound ∧
      witness.changedPathsDisjoint ∧
      witness.mergeSnapshotObjectBound ∧
      witness.workingTreeExcluded := by
  exact ⟨h.leftParentBound, h.rightParentBound,
    h.parentOrderExact, h.changedPathsInventoryBound,
    h.changedPathsDisjoint, h.mergeSnapshotObjectBound,
    h.workingTreeExcluded⟩

theorem valid_merge_certificate_is_confluent_at_merge
    (witness : MergeCertificateWitness)
    (h : witness.Valid) :
    witness.commonRoot ∧
      witness.commonPrefixNonempty ∧
      witness.branchSuffixesDisjoint ∧
      witness.parentRecordsBound ∧
      witness.mergeObservationBound ∧
      witness.mergeNormalForm := by
  exact ⟨h.commonRoot, h.commonPrefixNonempty,
    h.branchSuffixesDisjoint, h.parentRecordsBound,
    h.mergeObservationBound, h.mergeNormalForm⟩

end KUOS.WORLD.KuuOSRepositoryMergeCertificateV0_84
