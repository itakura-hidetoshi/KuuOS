import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryGitRevisionAdapterV0_83

structure GitRevisionObservationWitness where
  parentRevisionResolved : Prop
  currentRevisionResolved : Prop
  uniqueParentRelation : Prop
  changedPathsDerived : Prop
  inventoryBound : Prop
  parentSnapshotObjectBound : Prop
  currentSnapshotObjectBound : Prop
  workingTreeExcluded : Prop

structure GitRevisionObservationWitness.Valid
    (witness : GitRevisionObservationWitness) : Prop where
  parentRevisionResolved : witness.parentRevisionResolved
  currentRevisionResolved : witness.currentRevisionResolved
  uniqueParentRelation : witness.uniqueParentRelation
  changedPathsDerived : witness.changedPathsDerived
  inventoryBound : witness.inventoryBound
  parentSnapshotObjectBound : witness.parentSnapshotObjectBound
  currentSnapshotObjectBound : witness.currentSnapshotObjectBound
  workingTreeExcluded : witness.workingTreeExcluded

structure GitAdapterChainWitness where
  gitObservationBound : Prop
  parentRecordBound : Prop
  changedPathsExact : Prop
  resultingRecordBound : Prop

structure GitAdapterChainWitness.Valid
    (witness : GitAdapterChainWitness) : Prop where
  gitObservationBound : witness.gitObservationBound
  parentRecordBound : witness.parentRecordBound
  changedPathsExact : witness.changedPathsExact
  resultingRecordBound : witness.resultingRecordBound

theorem valid_git_observation_is_object_bound
    (witness : GitRevisionObservationWitness)
    (h : witness.Valid) :
    witness.parentRevisionResolved ∧
      witness.currentRevisionResolved ∧
      witness.uniqueParentRelation ∧
      witness.changedPathsDerived ∧
      witness.inventoryBound ∧
      witness.parentSnapshotObjectBound ∧
      witness.currentSnapshotObjectBound ∧
      witness.workingTreeExcluded := by
  exact ⟨h.parentRevisionResolved, h.currentRevisionResolved,
    h.uniqueParentRelation, h.changedPathsDerived,
    h.inventoryBound, h.parentSnapshotObjectBound,
    h.currentSnapshotObjectBound, h.workingTreeExcluded⟩

theorem valid_git_adapter_chain_is_exactly_bound
    (witness : GitAdapterChainWitness)
    (h : witness.Valid) :
    witness.gitObservationBound ∧
      witness.parentRecordBound ∧
      witness.changedPathsExact ∧
      witness.resultingRecordBound := by
  exact ⟨h.gitObservationBound, h.parentRecordBound,
    h.changedPathsExact, h.resultingRecordBound⟩

end KUOS.WORLD.KuuOSRepositoryGitRevisionAdapterV0_83
