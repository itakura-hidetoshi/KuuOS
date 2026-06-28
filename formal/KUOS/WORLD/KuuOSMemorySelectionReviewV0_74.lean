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

end KUOS.WORLD.KuuOSMemorySelectionReviewV0_74
