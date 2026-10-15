import KUOS.WORLD.KuuOSRepositoryApplicationAuthorizationV0_91

namespace KUOS.WORLD.KuuOSRepositoryAtomicApplicationV0_92

structure AtomicApplicationWitness where
  authorizationValid : Prop
  authorizationScopeBound : Prop
  sourceCommitUnchanged : Prop
  sourceSnapshotUnchanged : Prop
  objectDatabaseSource : Prop
  workingTreeIgnored : Prop
  patchBundleBound : Prop
  patchPathsExact : Prop
  changedPathsExact : Prop
  resultNormalFormCertified : Prop
  rollbackMaterialExact : Prop
  nonceRegistryBound : Prop
  nonceUnusedBefore : Prop
  nonceNotRevoked : Prop
  applicationApplied : Bool
  snapshotCommitted : Bool
  nonceCommitted : Bool
  sourceRetained : Bool
  registryRetained : Bool
  isolatedSnapshotOnly : Bool
  liveRepositoryWritePerformed : Bool
  commitCreated : Bool
  referenceMutated : Bool

structure AtomicApplicationWitness.Valid
    (witness : AtomicApplicationWitness) : Prop where
  authorizationValid : witness.authorizationValid
  authorizationScopeBound : witness.authorizationScopeBound
  sourceCommitUnchanged : witness.sourceCommitUnchanged
  sourceSnapshotUnchanged : witness.sourceSnapshotUnchanged
  objectDatabaseSource : witness.objectDatabaseSource
  workingTreeIgnored : witness.workingTreeIgnored
  patchBundleBound : witness.patchBundleBound
  patchPathsExact : witness.patchPathsExact
  changedPathsExact : witness.changedPathsExact
  resultNormalFormCertified : witness.resultNormalFormCertified
  rollbackMaterialExact : witness.rollbackMaterialExact
  nonceRegistryBound : witness.nonceRegistryBound
  nonceUnusedBefore : witness.nonceUnusedBefore
  nonceNotRevoked : witness.nonceNotRevoked
  applicationMatchesSnapshotCommit :
    witness.applicationApplied = witness.snapshotCommitted
  snapshotAndNonceCommitTogether :
    witness.snapshotCommitted = witness.nonceCommitted
  abortRetainsSource :
    witness.applicationApplied = false -> witness.sourceRetained = true
  abortRetainsRegistry :
    witness.applicationApplied = false -> witness.registryRetained = true
  isolatedSnapshotOnly : witness.isolatedSnapshotOnly = true
  liveRepositoryWritePerformed :
    witness.liveRepositoryWritePerformed = false
  commitCreated : witness.commitCreated = false
  referenceMutated : witness.referenceMutated = false


theorem successful_application_commits_snapshot_and_nonce_together
    (witness : AtomicApplicationWitness)
    (h : witness.Valid)
    (applied : witness.applicationApplied = true) :
    witness.snapshotCommitted = true ∧ witness.nonceCommitted = true := by
  have snapshot : witness.snapshotCommitted = true := by
    rw [← h.applicationMatchesSnapshotCommit]
    exact applied
  have nonce : witness.nonceCommitted = true := by
    rw [← h.snapshotAndNonceCommitTogether]
    exact snapshot
  exact ⟨snapshot, nonce⟩


theorem aborted_application_has_no_state_effect
    (witness : AtomicApplicationWitness)
    (h : witness.Valid)
    (aborted : witness.applicationApplied = false) :
    witness.sourceRetained = true ∧ witness.registryRetained = true := by
  exact ⟨h.abortRetainsSource aborted, h.abortRetainsRegistry aborted⟩


theorem valid_application_rechecks_exact_source
    (witness : AtomicApplicationWitness)
    (h : witness.Valid) :
    witness.sourceCommitUnchanged ∧ witness.sourceSnapshotUnchanged ∧
      witness.objectDatabaseSource ∧ witness.workingTreeIgnored := by
  exact ⟨h.sourceCommitUnchanged, h.sourceSnapshotUnchanged,
    h.objectDatabaseSource, h.workingTreeIgnored⟩


theorem valid_application_preserves_exact_patch_scope
    (witness : AtomicApplicationWitness)
    (h : witness.Valid) :
    witness.patchBundleBound ∧ witness.patchPathsExact ∧
      witness.changedPathsExact ∧ witness.resultNormalFormCertified ∧
      witness.rollbackMaterialExact := by
  exact ⟨h.patchBundleBound, h.patchPathsExact, h.changedPathsExact,
    h.resultNormalFormCertified, h.rollbackMaterialExact⟩


theorem valid_application_requires_fresh_single_use_nonce
    (witness : AtomicApplicationWitness)
    (h : witness.Valid) :
    witness.nonceRegistryBound ∧ witness.nonceUnusedBefore ∧
      witness.nonceNotRevoked := by
  exact ⟨h.nonceRegistryBound, h.nonceUnusedBefore, h.nonceNotRevoked⟩


theorem valid_application_has_no_git_authority
    (witness : AtomicApplicationWitness)
    (h : witness.Valid) :
    witness.isolatedSnapshotOnly = true ∧
      witness.liveRepositoryWritePerformed = false ∧
      witness.commitCreated = false ∧
      witness.referenceMutated = false := by
  exact ⟨h.isolatedSnapshotOnly, h.liveRepositoryWritePerformed,
    h.commitCreated, h.referenceMutated⟩

end KUOS.WORLD.KuuOSRepositoryAtomicApplicationV0_92
