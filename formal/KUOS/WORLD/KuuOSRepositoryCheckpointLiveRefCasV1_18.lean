import KUOS.WORLD.KuuOSRepositoryCheckpointLiveGitPreflightV1_17

namespace KUOS.WORLD.KuuOSRepositoryCheckpointLiveRefCasV1_18

inductive LiveRefCasStatus where
  | committed
  | aborted
  | rejected
  | error
  deriving DecidableEq, Repr

structure LiveRefCasWitness where
  policyValid : Prop
  requestValid : Prop
  requestBindingExact : Prop
  executorAuthorized : Prop
  repositoryPathAllowed : Prop
  preflightReady : Prop
  preflightFresh : Prop
  preflightRecomputed : Prop
  preflightReceiptExact : Prop
  sandboxMarkerPresent : Prop
  sandboxMarkerExact : Prop
  checkpointReferenceValid : Prop
  checkpointReferenceDirect : Prop
  targetReflogAbsentBefore : Prop
  targetReflogAbsentAfter : Prop
  currentOidMatchesExpected : Prop
  proposedObjectExists : Prop
  status : LiveRefCasStatus
  updateRefAttempted : Bool
  updateRefSucceeded : Bool
  postUpdateVerified : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool
  checkpointReferenceWritePerformed : Bool
  objectDatabaseWritePerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  reflogWritePerformed : Bool
  forceUpdatePerformed : Bool
  referenceDeletePerformed : Bool
  headUpdated : Bool
  branchUpdated : Bool
  tagUpdated : Bool
  remoteReferenceUpdated : Bool
  pushPerformed : Bool
  signingPerformed : Bool

structure LiveRefCasWitness.ValidCommitted
    (w : LiveRefCasWitness) : Prop where
  policyValid : w.policyValid
  requestValid : w.requestValid
  requestBindingExact : w.requestBindingExact
  executorAuthorized : w.executorAuthorized
  repositoryPathAllowed : w.repositoryPathAllowed
  preflightReady : w.preflightReady
  preflightFresh : w.preflightFresh
  preflightRecomputed : w.preflightRecomputed
  preflightReceiptExact : w.preflightReceiptExact
  sandboxMarkerPresent : w.sandboxMarkerPresent
  sandboxMarkerExact : w.sandboxMarkerExact
  checkpointReferenceValid : w.checkpointReferenceValid
  checkpointReferenceDirect : w.checkpointReferenceDirect
  targetReflogAbsentBefore : w.targetReflogAbsentBefore
  targetReflogAbsentAfter : w.targetReflogAbsentAfter
  currentOidMatchesExpected : w.currentOidMatchesExpected
  proposedObjectExists : w.proposedObjectExists
  statusCommitted : w.status = LiveRefCasStatus.committed
  updateAttempted : w.updateRefAttempted = true
  updateSucceeded : w.updateRefSucceeded = true
  postVerified : w.postUpdateVerified = true
  liveGitInvoked : w.liveGitCommandInvoked = true
  liveRepositoryMutated : w.liveRepositoryMutated = true
  checkpointRefWritten : w.checkpointReferenceWritePerformed = true
  noObjectWrite : w.objectDatabaseWritePerformed = false
  noIndexWrite : w.indexWritePerformed = false
  noWorkingTreeWrite : w.workingTreeWritePerformed = false
  noReflogWrite : w.reflogWritePerformed = false
  noForce : w.forceUpdatePerformed = false
  noDelete : w.referenceDeletePerformed = false
  noHeadUpdate : w.headUpdated = false
  noBranchUpdate : w.branchUpdated = false
  noTagUpdate : w.tagUpdated = false
  noRemoteUpdate : w.remoteReferenceUpdated = false
  noPush : w.pushPerformed = false
  noSigning : w.signingPerformed = false

structure LiveRefCasWitness.ValidRejected
    (w : LiveRefCasWitness) : Prop where
  statusRejected : w.status = LiveRefCasStatus.rejected
  noUpdateAttempt : w.updateRefAttempted = false
  noUpdateSuccess : w.updateRefSucceeded = false
  noLiveMutation : w.liveRepositoryMutated = false
  noCheckpointWrite : w.checkpointReferenceWritePerformed = false
  noObjectWrite : w.objectDatabaseWritePerformed = false
  noIndexWrite : w.indexWritePerformed = false
  noWorkingTreeWrite : w.workingTreeWritePerformed = false
  noReflogWrite : w.reflogWritePerformed = false


theorem committed_live_ref_cas_has_complete_authority
    (w : LiveRefCasWitness)
    (h : w.ValidCommitted) :
    w.policyValid ∧ w.requestValid ∧ w.requestBindingExact ∧
      w.executorAuthorized ∧ w.repositoryPathAllowed ∧
      w.preflightReady ∧ w.preflightFresh ∧ w.preflightRecomputed ∧
      w.preflightReceiptExact ∧ w.sandboxMarkerPresent ∧
      w.sandboxMarkerExact ∧ w.checkpointReferenceValid ∧
      w.checkpointReferenceDirect ∧ w.targetReflogAbsentBefore ∧
      w.targetReflogAbsentAfter ∧ w.currentOidMatchesExpected ∧
      w.proposedObjectExists := by
  exact ⟨h.policyValid, h.requestValid, h.requestBindingExact,
    h.executorAuthorized, h.repositoryPathAllowed, h.preflightReady,
    h.preflightFresh, h.preflightRecomputed, h.preflightReceiptExact,
    h.sandboxMarkerPresent, h.sandboxMarkerExact,
    h.checkpointReferenceValid, h.checkpointReferenceDirect,
    h.targetReflogAbsentBefore, h.targetReflogAbsentAfter,
    h.currentOidMatchesExpected, h.proposedObjectExists⟩


theorem committed_live_ref_cas_has_one_scoped_write
    (w : LiveRefCasWitness)
    (h : w.ValidCommitted) :
    w.liveGitCommandInvoked = true ∧
      w.liveRepositoryMutated = true ∧
      w.checkpointReferenceWritePerformed = true ∧
      w.objectDatabaseWritePerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.reflogWritePerformed = false ∧
      w.forceUpdatePerformed = false ∧
      w.referenceDeletePerformed = false ∧
      w.headUpdated = false ∧
      w.branchUpdated = false ∧
      w.tagUpdated = false ∧
      w.remoteReferenceUpdated = false ∧
      w.pushPerformed = false ∧
      w.signingPerformed = false := by
  exact ⟨h.liveGitInvoked, h.liveRepositoryMutated,
    h.checkpointRefWritten, h.noObjectWrite, h.noIndexWrite,
    h.noWorkingTreeWrite, h.noReflogWrite, h.noForce, h.noDelete,
    h.noHeadUpdate, h.noBranchUpdate, h.noTagUpdate,
    h.noRemoteUpdate, h.noPush, h.noSigning⟩


theorem rejected_live_ref_cas_writes_nothing
    (w : LiveRefCasWitness)
    (h : w.ValidRejected) :
    w.updateRefAttempted = false ∧
      w.updateRefSucceeded = false ∧
      w.liveRepositoryMutated = false ∧
      w.checkpointReferenceWritePerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.reflogWritePerformed = false := by
  exact ⟨h.noUpdateAttempt, h.noUpdateSuccess, h.noLiveMutation,
    h.noCheckpointWrite, h.noObjectWrite, h.noIndexWrite,
    h.noWorkingTreeWrite, h.noReflogWrite⟩

end KUOS.WORLD.KuuOSRepositoryCheckpointLiveRefCasV1_18
