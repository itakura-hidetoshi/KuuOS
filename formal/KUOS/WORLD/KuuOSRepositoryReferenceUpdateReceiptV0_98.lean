import KUOS.WORLD.KuuOSRepositoryAtomicReferenceUpdateV0_97

namespace KUOS.WORLD.KuuOSRepositoryReferenceUpdateReceiptV0_98

structure ReferenceUpdateReceiptWitness where
  atomicUpdateValid : Prop
  atomicUpdateCommitted : Prop
  repositoryBound : Prop
  referenceBound : Prop
  oldOidBound : Prop
  newOidBound : Prop
  transactionBound : Prop
  executionReportBound : Prop
  postReferenceObservationBound : Prop
  nonceConsumptionReceiptBound : Prop
  referenceUpdateConfirmed : Prop
  nonceConsumptionConfirmed : Prop
  atomicReferenceNonceTransitionConfirmed : Prop
  receiptCommitted : Bool
  forceUpdateConfirmed : Bool
  referenceDeleteConfirmed : Bool
  headUpdateConfirmed : Bool
  tagUpdateConfirmed : Bool
  remoteReferenceUpdateConfirmed : Bool
  pushConfirmed : Bool
  indexWriteConfirmed : Bool
  workingTreeWriteConfirmed : Bool
  objectDatabaseWriteConfirmed : Bool
  signingConfirmed : Bool
  receiptPerformedReferenceMutation : Bool
  receiptPerformedNonceConsumption : Bool
  receiptPerformedPush : Bool

structure ReferenceUpdateReceiptWitness.ValidCommitted
    (w : ReferenceUpdateReceiptWitness) : Prop where
  atomicUpdateValid : w.atomicUpdateValid
  atomicUpdateCommitted : w.atomicUpdateCommitted
  repositoryBound : w.repositoryBound
  referenceBound : w.referenceBound
  oldOidBound : w.oldOidBound
  newOidBound : w.newOidBound
  transactionBound : w.transactionBound
  executionReportBound : w.executionReportBound
  postReferenceObservationBound : w.postReferenceObservationBound
  nonceConsumptionReceiptBound : w.nonceConsumptionReceiptBound
  referenceUpdateConfirmed : w.referenceUpdateConfirmed
  nonceConsumptionConfirmed : w.nonceConsumptionConfirmed
  atomicReferenceNonceTransitionConfirmed :
    w.atomicReferenceNonceTransitionConfirmed
  receiptCommitted : w.receiptCommitted = true
  forceUpdateConfirmed : w.forceUpdateConfirmed = false
  referenceDeleteConfirmed : w.referenceDeleteConfirmed = false
  headUpdateConfirmed : w.headUpdateConfirmed = false
  tagUpdateConfirmed : w.tagUpdateConfirmed = false
  remoteReferenceUpdateConfirmed : w.remoteReferenceUpdateConfirmed = false
  pushConfirmed : w.pushConfirmed = false
  indexWriteConfirmed : w.indexWriteConfirmed = false
  workingTreeWriteConfirmed : w.workingTreeWriteConfirmed = false
  objectDatabaseWriteConfirmed : w.objectDatabaseWriteConfirmed = false
  signingConfirmed : w.signingConfirmed = false
  receiptPerformedReferenceMutation :
    w.receiptPerformedReferenceMutation = false
  receiptPerformedNonceConsumption :
    w.receiptPerformedNonceConsumption = false
  receiptPerformedPush : w.receiptPerformedPush = false


theorem valid_receipt_binds_repository_reference_and_oids
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.repositoryBound ∧ w.referenceBound ∧ w.oldOidBound ∧ w.newOidBound := by
  exact ⟨h.repositoryBound, h.referenceBound, h.oldOidBound, h.newOidBound⟩


theorem valid_receipt_requires_committed_atomic_update
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.atomicUpdateValid ∧ w.atomicUpdateCommitted := by
  exact ⟨h.atomicUpdateValid, h.atomicUpdateCommitted⟩


theorem valid_receipt_binds_all_post_execution_evidence
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.transactionBound ∧ w.executionReportBound ∧
      w.postReferenceObservationBound ∧
      w.nonceConsumptionReceiptBound := by
  exact ⟨h.transactionBound, h.executionReportBound,
    h.postReferenceObservationBound, h.nonceConsumptionReceiptBound⟩


theorem valid_receipt_confirms_atomic_reference_nonce_transition
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.referenceUpdateConfirmed ∧ w.nonceConsumptionConfirmed ∧
      w.atomicReferenceNonceTransitionConfirmed := by
  exact ⟨h.referenceUpdateConfirmed, h.nonceConsumptionConfirmed,
    h.atomicReferenceNonceTransitionConfirmed⟩


theorem valid_receipt_confirms_no_forbidden_effect
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.forceUpdateConfirmed = false ∧
      w.referenceDeleteConfirmed = false ∧
      w.headUpdateConfirmed = false ∧ w.tagUpdateConfirmed = false ∧
      w.remoteReferenceUpdateConfirmed = false ∧ w.pushConfirmed = false ∧
      w.indexWriteConfirmed = false ∧
      w.workingTreeWriteConfirmed = false ∧
      w.objectDatabaseWriteConfirmed = false ∧
      w.signingConfirmed = false := by
  exact ⟨h.forceUpdateConfirmed, h.referenceDeleteConfirmed,
    h.headUpdateConfirmed, h.tagUpdateConfirmed,
    h.remoteReferenceUpdateConfirmed, h.pushConfirmed,
    h.indexWriteConfirmed, h.workingTreeWriteConfirmed,
    h.objectDatabaseWriteConfirmed, h.signingConfirmed⟩


theorem receipt_verification_performs_no_effect
    (w : ReferenceUpdateReceiptWitness)
    (h : w.ValidCommitted) :
    w.receiptPerformedReferenceMutation = false ∧
      w.receiptPerformedNonceConsumption = false ∧
      w.receiptPerformedPush = false := by
  exact ⟨h.receiptPerformedReferenceMutation,
    h.receiptPerformedNonceConsumption, h.receiptPerformedPush⟩


structure ReferenceUpdateReceiptDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_reference_update_receipt
    {Input Output : Type}
    (derivation : ReferenceUpdateReceiptDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryReferenceUpdateReceiptV0_98
