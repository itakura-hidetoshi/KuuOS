import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateSelectionReceiptV0_73

namespace KUOS
namespace PlanOS

structure SubsequentCycleAdmissionRequestSurface where
  sourceSelection : SubsequentCycleCandidateSelectionReceiptSurface
  sourceBound : Bool
  selectedCandidateIdentityPreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  admissionScopeBound : Bool
  admissionConstraintsDigestBound : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  subsequentCycleAdmissionGranted : Bool
  subsequentCycleStarted : Bool
  sourceRequired : sourceBound = true
  identityRequired : selectedCandidateIdentityPreserved = true
  candidateDigestRequired : candidateSetDigestPreserved = true
  evaluationDigestRequired : evaluationSetDigestPreserved = true
  reviewDigestRequired : reviewSetDigestPreserved = true
  scopeRequired : admissionScopeBound = true
  constraintsRequired : admissionConstraintsDigestBound = true
  authorityRequired : subsequentCycleSelectionAuthorityGranted = true
  selectionRequestRequired : subsequentCycleCandidateSelectionRequested = true
  selectedRequired : subsequentCycleCandidateSelected = true
  admissionRequestRequired : subsequentCycleAdmissionRequested = true
  admissionGrantForbidden : subsequentCycleAdmissionGranted = false
  startForbidden : subsequentCycleStarted = false

structure SubsequentCycleAdmissionRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceCandidateSelectionReceiptPreserved : Bool
  selectedCandidateIdentityPreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  admissionScopePreserved : Bool
  admissionConstraintsDigestPreserved : Bool
  subsequentCycleAdmissionRequestOnly : Bool
  subsequentCycleAdmissionRequested : Bool
  subsequentCycleAdmissionGranted : Bool
  subsequentCycleStarted : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourceRequired : sourceCandidateSelectionReceiptPreserved = true
  identityRequired : selectedCandidateIdentityPreserved = true
  candidateDigestRequired : candidateSetDigestPreserved = true
  evaluationDigestRequired : evaluationSetDigestPreserved = true
  reviewDigestRequired : reviewSetDigestPreserved = true
  scopeRequired : admissionScopePreserved = true
  constraintsRequired : admissionConstraintsDigestPreserved = true
  requestOnlyRequired : subsequentCycleAdmissionRequestOnly = true
  admissionRequestRequired : subsequentCycleAdmissionRequested = true
  admissionGrantForbidden : subsequentCycleAdmissionGranted = false
  startForbidden : subsequentCycleStarted = false

structure PlanOSSubsequentCycleAdmissionRequestBridge where
  Digest : Type
  digestOf : SubsequentCycleAdmissionRequestSurface → SubsequentCycleAdmissionRequestBoundary → Nat → Digest
  surface : SubsequentCycleAdmissionRequestSurface
  boundary : SubsequentCycleAdmissionRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex

namespace PlanOSSubsequentCycleAdmissionRequestBridge

theorem authorized_selected_candidate_requests_admission_without_start
    (b : PlanOSSubsequentCycleAdmissionRequestBridge) :
    b.surface.subsequentCycleSelectionAuthorityGranted = true ∧
      b.surface.subsequentCycleCandidateSelectionRequested = true ∧
      b.surface.subsequentCycleCandidateSelected = true ∧
      b.surface.subsequentCycleAdmissionRequested = true ∧
      b.surface.subsequentCycleAdmissionGranted = false ∧
      b.surface.subsequentCycleStarted = false := by
  exact ⟨b.surface.authorityRequired, b.surface.selectionRequestRequired,
    b.surface.selectedRequired, b.surface.admissionRequestRequired,
    b.surface.admissionGrantForbidden, b.surface.startForbidden⟩

theorem request_preserves_selected_candidate_evidence
    (b : PlanOSSubsequentCycleAdmissionRequestBridge) :
    b.surface.sourceBound = true ∧
      b.surface.selectedCandidateIdentityPreserved = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.reviewSetDigestPreserved = true ∧
      b.surface.admissionScopeBound = true ∧
      b.surface.admissionConstraintsDigestBound = true := by
  exact ⟨b.surface.sourceRequired, b.surface.identityRequired,
    b.surface.candidateDigestRequired, b.surface.evaluationDigestRequired,
    b.surface.reviewDigestRequired, b.surface.scopeRequired,
    b.surface.constraintsRequired⟩

theorem boundary_is_admission_request_only
    (b : PlanOSSubsequentCycleAdmissionRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateSelectionReceiptPreserved = true ∧
      b.boundary.selectedCandidateIdentityPreserved = true ∧
      b.boundary.subsequentCycleAdmissionRequestOnly = true ∧
      b.boundary.subsequentCycleAdmissionRequested = true ∧
      b.boundary.subsequentCycleAdmissionGranted = false ∧
      b.boundary.subsequentCycleStarted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceRequired,
    b.boundary.identityRequired, b.boundary.requestOnlyRequired,
    b.boundary.admissionRequestRequired, b.boundary.admissionGrantForbidden,
    b.boundary.startForbidden⟩

theorem history_appends_one_admission_request
    (b : PlanOSSubsequentCycleAdmissionRequestBridge) : b.historyDelta = 1 := by
  exact b.historyDeltaRequired

end PlanOSSubsequentCycleAdmissionRequestBridge
end PlanOS
end KUOS
