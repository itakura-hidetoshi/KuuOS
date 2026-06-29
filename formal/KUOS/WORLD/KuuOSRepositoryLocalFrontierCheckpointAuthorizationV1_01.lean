import KUOS.WORLD.KuuOSRepositoryLocalFrontierFinalityV1_00

namespace KUOS.WORLD.KuuOSRepositoryLocalFrontierCheckpointAuthorizationV1_01

structure CheckpointAuthorizationWitness where
  finalityCertificateValid : Prop
  finalityCertificateCommitted : Prop
  repositoryBound : Prop
  checkpointReferenceBound : Prop
  checkpointNamespaceExact : Prop
  checkpointReferenceNormalized : Prop
  checkpointReferenceDirect : Prop
  checkpointReferenceNotSymbolic : Prop
  checkpointReferenceAbsent : Prop
  compareAndSwapZeroOidRequired : Prop
  exactFinalTipBound : Prop
  finalTipPresent : Prop
  policyBound : Prop
  nonceScopeBound : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  nonceStatusFresh : Prop
  authorizationLifetimeBounded : Prop
  authorizationNotExpired : Prop
  noFutureEvidence : Prop
  createRequested : Prop
  checkpointCreationAuthorized : Bool
  checkpointOverwriteAuthorized : Bool
  forceUpdateAuthorized : Bool
  referenceDeleteAuthorized : Bool
  tagCreationAuthorized : Bool
  pushAuthorized : Bool
  checkpointCreated : Bool
  checkpointReferenceMutated : Bool
  branchUpdated : Bool
  tagUpdated : Bool
  remoteReferenceUpdated : Bool
  pushPerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  objectDatabaseWritePerformed : Bool
  reflogWritePerformed : Bool
  signingPerformed : Bool

structure CheckpointAuthorizationWitness.ValidGranted
    (w : CheckpointAuthorizationWitness) : Prop where
  finalityCertificateValid : w.finalityCertificateValid
  finalityCertificateCommitted : w.finalityCertificateCommitted
  repositoryBound : w.repositoryBound
  checkpointReferenceBound : w.checkpointReferenceBound
  checkpointNamespaceExact : w.checkpointNamespaceExact
  checkpointReferenceNormalized : w.checkpointReferenceNormalized
  checkpointReferenceDirect : w.checkpointReferenceDirect
  checkpointReferenceNotSymbolic : w.checkpointReferenceNotSymbolic
  checkpointReferenceAbsent : w.checkpointReferenceAbsent
  compareAndSwapZeroOidRequired : w.compareAndSwapZeroOidRequired
  exactFinalTipBound : w.exactFinalTipBound
  finalTipPresent : w.finalTipPresent
  policyBound : w.policyBound
  nonceScopeBound : w.nonceScopeBound
  nonceUnused : w.nonceUnused
  nonceNotRevoked : w.nonceNotRevoked
  nonceStatusFresh : w.nonceStatusFresh
  authorizationLifetimeBounded : w.authorizationLifetimeBounded
  authorizationNotExpired : w.authorizationNotExpired
  noFutureEvidence : w.noFutureEvidence
  createRequested : w.createRequested
  checkpointCreationAuthorized : w.checkpointCreationAuthorized = true
  checkpointOverwriteAuthorized : w.checkpointOverwriteAuthorized = false
  forceUpdateAuthorized : w.forceUpdateAuthorized = false
  referenceDeleteAuthorized : w.referenceDeleteAuthorized = false
  tagCreationAuthorized : w.tagCreationAuthorized = false
  pushAuthorized : w.pushAuthorized = false
  checkpointCreated : w.checkpointCreated = false
  checkpointReferenceMutated : w.checkpointReferenceMutated = false
  branchUpdated : w.branchUpdated = false
  tagUpdated : w.tagUpdated = false
  remoteReferenceUpdated : w.remoteReferenceUpdated = false
  pushPerformed : w.pushPerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  reflogWritePerformed : w.reflogWritePerformed = false
  signingPerformed : w.signingPerformed = false


theorem valid_checkpoint_authorization_binds_finality_and_repository
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.finalityCertificateValid ∧ w.finalityCertificateCommitted ∧
      w.repositoryBound ∧ w.exactFinalTipBound ∧ w.finalTipPresent := by
  exact ⟨h.finalityCertificateValid, h.finalityCertificateCommitted,
    h.repositoryBound, h.exactFinalTipBound, h.finalTipPresent⟩


theorem valid_checkpoint_authorization_uses_separate_normalized_namespace
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.checkpointReferenceBound ∧ w.checkpointNamespaceExact ∧
      w.checkpointReferenceNormalized ∧ w.checkpointReferenceDirect ∧
      w.checkpointReferenceNotSymbolic := by
  exact ⟨h.checkpointReferenceBound, h.checkpointNamespaceExact,
    h.checkpointReferenceNormalized, h.checkpointReferenceDirect,
    h.checkpointReferenceNotSymbolic⟩


theorem valid_checkpoint_authorization_requires_absence_and_cas
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.checkpointReferenceAbsent ∧ w.compareAndSwapZeroOidRequired := by
  exact ⟨h.checkpointReferenceAbsent, h.compareAndSwapZeroOidRequired⟩


theorem valid_checkpoint_authorization_is_scope_bound_and_single_use
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.policyBound ∧ w.nonceScopeBound ∧ w.nonceUnused ∧
      w.nonceNotRevoked ∧ w.nonceStatusFresh ∧
      w.authorizationLifetimeBounded ∧ w.authorizationNotExpired ∧
      w.noFutureEvidence ∧ w.createRequested := by
  exact ⟨h.policyBound, h.nonceScopeBound, h.nonceUnused,
    h.nonceNotRevoked, h.nonceStatusFresh,
    h.authorizationLifetimeBounded, h.authorizationNotExpired,
    h.noFutureEvidence, h.createRequested⟩


theorem valid_checkpoint_authorization_grants_only_new_checkpoint_creation
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.checkpointCreationAuthorized = true ∧
      w.checkpointOverwriteAuthorized = false ∧
      w.forceUpdateAuthorized = false ∧
      w.referenceDeleteAuthorized = false ∧
      w.tagCreationAuthorized = false ∧
      w.pushAuthorized = false := by
  exact ⟨h.checkpointCreationAuthorized, h.checkpointOverwriteAuthorized,
    h.forceUpdateAuthorized, h.referenceDeleteAuthorized,
    h.tagCreationAuthorized, h.pushAuthorized⟩


theorem checkpoint_authorization_performs_no_repository_effect
    (w : CheckpointAuthorizationWitness)
    (h : w.ValidGranted) :
    w.checkpointCreated = false ∧
      w.checkpointReferenceMutated = false ∧
      w.branchUpdated = false ∧ w.tagUpdated = false ∧
      w.remoteReferenceUpdated = false ∧ w.pushPerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.reflogWritePerformed = false ∧ w.signingPerformed = false := by
  exact ⟨h.checkpointCreated, h.checkpointReferenceMutated,
    h.branchUpdated, h.tagUpdated, h.remoteReferenceUpdated,
    h.pushPerformed, h.indexWritePerformed,
    h.workingTreeWritePerformed, h.objectDatabaseWritePerformed,
    h.reflogWritePerformed, h.signingPerformed⟩


structure CheckpointAuthorizationDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_authorization
    {Input Output : Type}
    (derivation : CheckpointAuthorizationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryLocalFrontierCheckpointAuthorizationV1_01
