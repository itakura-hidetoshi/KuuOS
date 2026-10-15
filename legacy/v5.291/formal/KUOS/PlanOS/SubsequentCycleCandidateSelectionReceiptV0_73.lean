import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateSelectionRequestV0_72

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSelectionReceiptSurface where
  sourceSelectionRequestBound : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  eligibleCandidateSetPreserved : Bool
  selectionScopePreserved : Bool
  selectionCriteriaDigestPreserved : Bool
  selectedCandidateEligible : Bool
  selectionRationaleDigestBound : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceSelectionRequestBound = true
  candidateDigestRequired : candidateSetDigestPreserved = true
  evaluationDigestRequired : evaluationSetDigestPreserved = true
  reviewDigestRequired : reviewSetDigestPreserved = true
  eligibleSetRequired : eligibleCandidateSetPreserved = true
  scopeRequired : selectionScopePreserved = true
  criteriaRequired : selectionCriteriaDigestPreserved = true
  eligibilityRequired : selectedCandidateEligible = true
  rationaleRequired : selectionRationaleDigestBound = true
  authorityRequired : subsequentCycleSelectionAuthorityGranted = true
  requestRequired : subsequentCycleCandidateSelectionRequested = true
  selectedRequired : subsequentCycleCandidateSelected = true
  admissionForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateSelectionReceiptBridge where
  surface : SubsequentCycleCandidateSelectionReceiptSurface
  historyDelta : Nat
  historyDeltaRequired : historyDelta = 1

namespace PlanOSSubsequentCycleCandidateSelectionReceiptBridge

theorem selection_is_authorized_eligible_and_admission_closed
    (b : PlanOSSubsequentCycleCandidateSelectionReceiptBridge) :
    b.surface.sourceSelectionRequestBound = true ∧
      b.surface.selectedCandidateEligible = true ∧
      b.surface.selectionRationaleDigestBound = true ∧
      b.surface.subsequentCycleSelectionAuthorityGranted = true ∧
      b.surface.subsequentCycleCandidateSelectionRequested = true ∧
      b.surface.subsequentCycleCandidateSelected = true ∧
      b.surface.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequired, b.surface.eligibilityRequired,
    b.surface.rationaleRequired, b.surface.authorityRequired,
    b.surface.requestRequired, b.surface.selectedRequired,
    b.surface.admissionForbidden⟩

theorem evidence_chain_is_preserved
    (b : PlanOSSubsequentCycleCandidateSelectionReceiptBridge) :
    b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.reviewSetDigestPreserved = true ∧
      b.surface.eligibleCandidateSetPreserved = true ∧
      b.surface.selectionScopePreserved = true ∧
      b.surface.selectionCriteriaDigestPreserved = true := by
  exact ⟨b.surface.candidateDigestRequired, b.surface.evaluationDigestRequired,
    b.surface.reviewDigestRequired, b.surface.eligibleSetRequired,
    b.surface.scopeRequired, b.surface.criteriaRequired⟩

theorem history_appends_one_selection_receipt
    (b : PlanOSSubsequentCycleCandidateSelectionReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

end PlanOSSubsequentCycleCandidateSelectionReceiptBridge
end PlanOS
end KUOS
