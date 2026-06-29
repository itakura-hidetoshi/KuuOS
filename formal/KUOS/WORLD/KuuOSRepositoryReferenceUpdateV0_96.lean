import KUOS.WORLD.KuuOSRepositoryObjectMaterializationReceiptV0_95

namespace KUOS.WORLD.KuuOSRepositoryReferenceUpdateV0_96

structure AuthorizationWitness where
  repositoryBound : Prop
  referenceBound : Prop
  oldOidBound : Prop
  newOidBound : Prop
  candidateCommitPresent : Prop
  fastForwardVerified : Prop
  compareAndSwapRequired : Prop
  nonceUnused : Prop
  singleUseEligible : Prop
  authorityGranted : Bool
  forceAuthorized : Bool
  deleteAuthorized : Bool
  referenceUpdatePerformed : Bool
  referenceMutated : Bool
  pushPerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  objectDatabaseWritePerformed : Bool
  signingPerformed : Bool

structure AuthorizationWitness.Valid (w : AuthorizationWitness) : Prop where
  repositoryBound : w.repositoryBound
  referenceBound : w.referenceBound
  oldOidBound : w.oldOidBound
  newOidBound : w.newOidBound
  candidateCommitPresent : w.candidateCommitPresent
  fastForwardVerified : w.fastForwardVerified
  compareAndSwapRequired : w.compareAndSwapRequired
  nonceUnused : w.nonceUnused
  singleUseEligible : w.singleUseEligible
  authorityGranted : w.authorityGranted = true
  forceAuthorized : w.forceAuthorized = false
  deleteAuthorized : w.deleteAuthorized = false
  referenceUpdatePerformed : w.referenceUpdatePerformed = false
  referenceMutated : w.referenceMutated = false
  pushPerformed : w.pushPerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  signingPerformed : w.signingPerformed = false

 theorem valid_binds_exact_repository_reference_and_oids
    (w : AuthorizationWitness) (h : w.Valid) :
    w.repositoryBound ∧ w.referenceBound ∧ w.oldOidBound ∧ w.newOidBound := by
  exact ⟨h.repositoryBound, h.referenceBound, h.oldOidBound, h.newOidBound⟩

 theorem valid_requires_candidate_fast_forward_and_cas
    (w : AuthorizationWitness) (h : w.Valid) :
    w.candidateCommitPresent ∧ w.fastForwardVerified ∧
      w.compareAndSwapRequired := by
  exact ⟨h.candidateCommitPresent, h.fastForwardVerified,
    h.compareAndSwapRequired⟩

 theorem valid_is_single_use
    (w : AuthorizationWitness) (h : w.Valid) :
    w.nonceUnused ∧ w.singleUseEligible := by
  exact ⟨h.nonceUnused, h.singleUseEligible⟩

 theorem valid_grants_no_force_or_delete
    (w : AuthorizationWitness) (h : w.Valid) :
    w.forceAuthorized = false ∧ w.deleteAuthorized = false := by
  exact ⟨h.forceAuthorized, h.deleteAuthorized⟩

 theorem valid_performs_no_reference_mutation
    (w : AuthorizationWitness) (h : w.Valid) :
    w.referenceUpdatePerformed = false ∧ w.referenceMutated = false := by
  exact ⟨h.referenceUpdatePerformed, h.referenceMutated⟩

 theorem valid_grants_no_push_or_other_effect
    (w : AuthorizationWitness) (h : w.Valid) :
    w.pushPerformed = false ∧ w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧ w.signingPerformed = false := by
  exact ⟨h.pushPerformed, h.indexWritePerformed,
    h.workingTreeWritePerformed, h.objectDatabaseWritePerformed,
    h.signingPerformed⟩

structure Derivation (Input Output : Type) where
  derive : Input → Output

 theorem same_input_has_same_authorization
    {Input Output : Type} (d : Derivation Input Output)
    (left right : Input) (h : left = right) :
    d.derive left = d.derive right := by
  exact congrArg d.derive h

end KUOS.WORLD.KuuOSRepositoryReferenceUpdateV0_96
