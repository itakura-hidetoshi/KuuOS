import KUOS.WORLD.KuuOSRepositoryCommitCandidateV0_93

namespace KUOS.WORLD.KuuOSRepositoryObjectMaterializationAuthorizationV0_94

structure ObjectMaterializationWitness where
  commitCandidateValid : Prop
  candidateObjectPayloadsExact : Prop
  candidateObjectsDeduplicated : Prop
  dependencyOrderDeterministic : Prop
  repositoryIdentityBound : Prop
  objectDatabaseObservationValid : Prop
  workingTreeIgnored : Prop
  sourceParentPresent : Prop
  queriedObjectSetExact : Prop
  existingObjectsCollisionFree : Prop
  exactExistingObjectsReused : Prop
  objectCountBounded : Prop
  payloadBytesBounded : Prop
  nonceScopeBound : Prop
  nonceFresh : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  authorizationNotExpired : Prop
  referenceNonmutationRequired : Prop
  objectDatabaseWriteAuthorityGranted : Bool
  commitObjectMaterializationAuthorityGranted : Bool
  objectDatabaseWritePerformed : Bool
  commitObjectWritten : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  referenceMutationAuthorityGranted : Bool
  referenceMutated : Bool
  signingPerformed : Bool

structure ObjectMaterializationWitness.Valid
    (witness : ObjectMaterializationWitness) : Prop where
  commitCandidateValid : witness.commitCandidateValid
  candidateObjectPayloadsExact : witness.candidateObjectPayloadsExact
  candidateObjectsDeduplicated : witness.candidateObjectsDeduplicated
  dependencyOrderDeterministic : witness.dependencyOrderDeterministic
  repositoryIdentityBound : witness.repositoryIdentityBound
  objectDatabaseObservationValid : witness.objectDatabaseObservationValid
  workingTreeIgnored : witness.workingTreeIgnored
  sourceParentPresent : witness.sourceParentPresent
  queriedObjectSetExact : witness.queriedObjectSetExact
  existingObjectsCollisionFree : witness.existingObjectsCollisionFree
  exactExistingObjectsReused : witness.exactExistingObjectsReused
  objectCountBounded : witness.objectCountBounded
  payloadBytesBounded : witness.payloadBytesBounded
  nonceScopeBound : witness.nonceScopeBound
  nonceFresh : witness.nonceFresh
  nonceUnused : witness.nonceUnused
  nonceNotRevoked : witness.nonceNotRevoked
  authorizationNotExpired : witness.authorizationNotExpired
  referenceNonmutationRequired : witness.referenceNonmutationRequired
  objectDatabaseWriteAuthorityGranted :
    witness.objectDatabaseWriteAuthorityGranted = true
  commitObjectMaterializationAuthorityGranted :
    witness.commitObjectMaterializationAuthorityGranted = true
  objectDatabaseWritePerformed :
    witness.objectDatabaseWritePerformed = false
  commitObjectWritten : witness.commitObjectWritten = false
  indexWritePerformed : witness.indexWritePerformed = false
  workingTreeWritePerformed : witness.workingTreeWritePerformed = false
  referenceMutationAuthorityGranted :
    witness.referenceMutationAuthorityGranted = false
  referenceMutated : witness.referenceMutated = false
  signingPerformed : witness.signingPerformed = false


theorem valid_materialization_binds_candidate_and_payloads
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.commitCandidateValid ∧
      witness.candidateObjectPayloadsExact ∧
      witness.candidateObjectsDeduplicated ∧
      witness.dependencyOrderDeterministic := by
  exact ⟨h.commitCandidateValid, h.candidateObjectPayloadsExact,
    h.candidateObjectsDeduplicated, h.dependencyOrderDeterministic⟩


theorem valid_materialization_binds_target_object_database
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.repositoryIdentityBound ∧
      witness.objectDatabaseObservationValid ∧
      witness.workingTreeIgnored ∧
      witness.sourceParentPresent ∧
      witness.queriedObjectSetExact := by
  exact ⟨h.repositoryIdentityBound, h.objectDatabaseObservationValid,
    h.workingTreeIgnored, h.sourceParentPresent, h.queriedObjectSetExact⟩


theorem valid_materialization_reuses_only_exact_existing_objects
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.existingObjectsCollisionFree ∧
      witness.exactExistingObjectsReused := by
  exact ⟨h.existingObjectsCollisionFree, h.exactExistingObjectsReused⟩


theorem valid_materialization_is_bounded_and_single_use
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.objectCountBounded ∧ witness.payloadBytesBounded ∧
      witness.nonceScopeBound ∧ witness.nonceFresh ∧
      witness.nonceUnused ∧ witness.nonceNotRevoked ∧
      witness.authorizationNotExpired := by
  exact ⟨h.objectCountBounded, h.payloadBytesBounded,
    h.nonceScopeBound, h.nonceFresh, h.nonceUnused,
    h.nonceNotRevoked, h.authorizationNotExpired⟩


theorem valid_materialization_grants_bounded_object_authority
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.objectDatabaseWriteAuthorityGranted = true ∧
      witness.commitObjectMaterializationAuthorityGranted = true := by
  exact ⟨h.objectDatabaseWriteAuthorityGranted,
    h.commitObjectMaterializationAuthorityGranted⟩


theorem valid_materialization_performs_no_write
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.objectDatabaseWritePerformed = false ∧
      witness.commitObjectWritten = false ∧
      witness.indexWritePerformed = false ∧
      witness.workingTreeWritePerformed = false := by
  exact ⟨h.objectDatabaseWritePerformed, h.commitObjectWritten,
    h.indexWritePerformed, h.workingTreeWritePerformed⟩


theorem valid_materialization_grants_no_reference_effect
    (witness : ObjectMaterializationWitness)
    (h : witness.Valid) :
    witness.referenceNonmutationRequired ∧
      witness.referenceMutationAuthorityGranted = false ∧
      witness.referenceMutated = false ∧ witness.signingPerformed = false := by
  exact ⟨h.referenceNonmutationRequired,
    h.referenceMutationAuthorityGranted, h.referenceMutated,
    h.signingPerformed⟩


structure MaterializationPlanDerivation (Input Plan : Type) where
  derive : Input → Plan


theorem same_input_has_same_materialization_plan
    {Input Plan : Type}
    (derivation : MaterializationPlanDerivation Input Plan)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryObjectMaterializationAuthorizationV0_94
