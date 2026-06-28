import Mathlib
import KUOS.WORLD.KuuOSFiniteMemoryEvaluationV0_73

namespace KUOS.WORLD.KuuOSMemorySelectionReviewV0_74

inductive ReviewDecision where
  | approve
  | reject
  | requestReevaluation
  deriving DecidableEq

structure SelectionBinding where
  selectionRecordDigest : String
  sourceHistoryDigest : String
  sourceKernelDigest : String
  familyDigest : String
  selectedMemberDigest : String
  selectedDeformationDigest : String
  selectedKernelDigest : String
  selectedConnectionDigest : String
  deriving DecidableEq

structure ReviewRequest where
  binding : SelectionBinding
  rollbackTargetDigest : String
  reviewerAllowed : String → Prop
  validFromEpoch : ℕ
  validUntilEpoch : ℕ

structure ReviewReceipt where
  binding : SelectionBinding
  rollbackTargetDigest : String
  reviewerClass : String
  decision : ReviewDecision
  decidedAtEpoch : ℕ
  applicationAuthority : Prop
  writesDisabled : Prop
  liveApplicationDisabled : Prop
  permissionExpansionDisabled : Prop
  rollbackTargetReplacementDisabled : Prop

structure ReviewReceipt.Valid
    (request : ReviewRequest)
    (receipt : ReviewReceipt) : Prop where
  exactBinding : receipt.binding = request.binding
  exactRollbackTarget : receipt.rollbackTargetDigest = request.rollbackTargetDigest
  reviewerAllowed : request.reviewerAllowed receipt.reviewerClass
  withinValidityWindow :
    request.validFromEpoch ≤ receipt.decidedAtEpoch ∧
      receipt.decidedAtEpoch ≤ request.validUntilEpoch
  authorityIffApproved :
    receipt.applicationAuthority ↔ receipt.decision = ReviewDecision.approve
  writesDisabled : receipt.writesDisabled
  liveApplicationDisabled : receipt.liveApplicationDisabled
  permissionExpansionDisabled : receipt.permissionExpansionDisabled
  rollbackTargetReplacementDisabled : receipt.rollbackTargetReplacementDisabled

theorem approved_review_grants_application_authority
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request)
    (hApprove : receipt.decision = ReviewDecision.approve) :
    receipt.applicationAuthority := by
  exact hValid.authorityIffApproved.mpr hApprove

theorem nonapproved_review_denies_application_authority
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request)
    (hNotApprove : receipt.decision ≠ ReviewDecision.approve) :
    ¬ receipt.applicationAuthority := by
  intro hAuthority
  exact hNotApprove (hValid.authorityIffApproved.mp hAuthority)

theorem valid_review_preserves_exact_selection_binding
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request) :
    receipt.binding = request.binding := by
  exact hValid.exactBinding

theorem valid_review_preserves_rollback_target
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request) :
    receipt.rollbackTargetDigest = request.rollbackTargetDigest := by
  exact hValid.exactRollbackTarget

theorem valid_review_is_within_window
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request) :
    request.validFromEpoch ≤ receipt.decidedAtEpoch ∧
      receipt.decidedAtEpoch ≤ request.validUntilEpoch := by
  exact hValid.withinValidityWindow

theorem valid_review_has_no_immediate_application_effect
    (request : ReviewRequest)
    (receipt : ReviewReceipt)
    (hValid : receipt.Valid request) :
    receipt.writesDisabled ∧
      receipt.liveApplicationDisabled ∧
      receipt.permissionExpansionDisabled ∧
      receipt.rollbackTargetReplacementDisabled := by
  exact ⟨hValid.writesDisabled, hValid.liveApplicationDisabled,
    hValid.permissionExpansionDisabled,
    hValid.rollbackTargetReplacementDisabled⟩

end KUOS.WORLD.KuuOSMemorySelectionReviewV0_74
