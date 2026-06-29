import KUOS.WORLD.KuuOSRepositoryObjectMaterializationAuthorizationV0_94

namespace KUOS.WORLD.KuuOSRepositoryObjectMaterializationReceiptV0_95

structure ObjectMaterializationReceiptWitness where
  authorizationValid : Prop
  authorizationGranted : Prop
  authorizationBound : Prop
  authorizationValidAtCompletion : Prop
  executorAuthorized : Prop
  durationBounded : Prop
  planItemSetExact : Prop
  planOrderExact : Prop
  writeSetExact : Prop
  reuseSetExact : Prop
  executionPayloadsExact : Prop
  postObservationObjectDatabaseSource : Prop
  postObservationWorkingTreeIgnored : Prop
  postQuerySetExact : Prop
  parentCommitPreserved : Prop
  allCandidateObjectsPresent : Prop
  allCandidatePayloadsExact : Prop
  reusedObjectsPreserved : Prop
  candidateCommitPresent : Prop
  nonceScopeBound : Prop
  nonceAuthorizationBound : Prop
  nonceUnusedBefore : Prop
  nonceConsumedAfter : Prop
  nonceNotRevoked : Prop
  nonceConsumptionCommitted : Prop
  nonceAtomicWithMaterialization : Prop
  objectDatabaseMaterializationCommitted : Bool
  commitObjectWritten : Bool
  atomicStateTransition : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  referenceMutated : Bool
  signingPerformed : Bool

structure ObjectMaterializationReceiptWitness.Valid
    (witness : ObjectMaterializationReceiptWitness) : Prop where
  authorizationValid : witness.authorizationValid
  authorizationGranted : witness.authorizationGranted
  authorizationBound : witness.authorizationBound
  authorizationValidAtCompletion : witness.authorizationValidAtCompletion
  executorAuthorized : witness.executorAuthorized
  durationBounded : witness.durationBounded
  planItemSetExact : witness.planItemSetExact
  planOrderExact : witness.planOrderExact
  writeSetExact : witness.writeSetExact
  reuseSetExact : witness.reuseSetExact
  executionPayloadsExact : witness.executionPayloadsExact
  postObservationObjectDatabaseSource :
    witness.postObservationObjectDatabaseSource
  postObservationWorkingTreeIgnored :
    witness.postObservationWorkingTreeIgnored
  postQuerySetExact : witness.postQuerySetExact
  parentCommitPreserved : witness.parentCommitPreserved
  allCandidateObjectsPresent : witness.allCandidateObjectsPresent
  allCandidatePayloadsExact : witness.allCandidatePayloadsExact
  reusedObjectsPreserved : witness.reusedObjectsPreserved
  candidateCommitPresent : witness.candidateCommitPresent
  nonceScopeBound : witness.nonceScopeBound
  nonceAuthorizationBound : witness.nonceAuthorizationBound
  nonceUnusedBefore : witness.nonceUnusedBefore
  nonceConsumedAfter : witness.nonceConsumedAfter
  nonceNotRevoked : witness.nonceNotRevoked
  nonceConsumptionCommitted : witness.nonceConsumptionCommitted
  nonceAtomicWithMaterialization : witness.nonceAtomicWithMaterialization
  objectDatabaseMaterializationCommitted :
    witness.objectDatabaseMaterializationCommitted = true
  atomicStateTransition : witness.atomicStateTransition = true
  indexWritePerformed : witness.indexWritePerformed = false
  workingTreeWritePerformed : witness.workingTreeWritePerformed = false
  referenceMutated : witness.referenceMutated = false
  signingPerformed : witness.signingPerformed = false


theorem valid_receipt_revalidates_authorization
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.authorizationValid ∧ witness.authorizationGranted ∧
      witness.authorizationBound ∧ witness.authorizationValidAtCompletion := by
  exact ⟨h.authorizationValid, h.authorizationGranted,
    h.authorizationBound, h.authorizationValidAtCompletion⟩


theorem valid_receipt_executes_exact_plan
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.planItemSetExact ∧ witness.planOrderExact ∧
      witness.writeSetExact ∧ witness.reuseSetExact ∧
      witness.executionPayloadsExact := by
  exact ⟨h.planItemSetExact, h.planOrderExact, h.writeSetExact,
    h.reuseSetExact, h.executionPayloadsExact⟩


theorem valid_receipt_verifies_post_object_database
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.postObservationObjectDatabaseSource ∧
      witness.postObservationWorkingTreeIgnored ∧
      witness.postQuerySetExact ∧ witness.parentCommitPreserved ∧
      witness.allCandidateObjectsPresent ∧
      witness.allCandidatePayloadsExact ∧ witness.reusedObjectsPreserved := by
  exact ⟨h.postObservationObjectDatabaseSource,
    h.postObservationWorkingTreeIgnored, h.postQuerySetExact,
    h.parentCommitPreserved, h.allCandidateObjectsPresent,
    h.allCandidatePayloadsExact, h.reusedObjectsPreserved⟩


theorem valid_receipt_contains_exact_candidate_commit
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) : witness.candidateCommitPresent := by
  exact h.candidateCommitPresent


theorem valid_receipt_consumes_nonce_atomically
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.nonceScopeBound ∧ witness.nonceAuthorizationBound ∧
      witness.nonceUnusedBefore ∧ witness.nonceConsumedAfter ∧
      witness.nonceNotRevoked ∧ witness.nonceConsumptionCommitted ∧
      witness.nonceAtomicWithMaterialization := by
  exact ⟨h.nonceScopeBound, h.nonceAuthorizationBound,
    h.nonceUnusedBefore, h.nonceConsumedAfter, h.nonceNotRevoked,
    h.nonceConsumptionCommitted, h.nonceAtomicWithMaterialization⟩


theorem valid_receipt_commits_object_database_transition
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.objectDatabaseMaterializationCommitted = true ∧
      witness.atomicStateTransition = true := by
  exact ⟨h.objectDatabaseMaterializationCommitted, h.atomicStateTransition⟩


theorem valid_receipt_does_not_mutate_reference
    (witness : ObjectMaterializationReceiptWitness)
    (h : witness.Valid) :
    witness.indexWritePerformed = false ∧
      witness.workingTreeWritePerformed = false ∧
      witness.referenceMutated = false ∧ witness.signingPerformed = false := by
  exact ⟨h.indexWritePerformed, h.workingTreeWritePerformed,
    h.referenceMutated, h.signingPerformed⟩


structure ReceiptDerivation (Input Receipt : Type) where
  derive : Input → Receipt


theorem same_input_has_same_materialization_receipt
    {Input Receipt : Type}
    (derivation : ReceiptDerivation Input Receipt)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryObjectMaterializationReceiptV0_95
