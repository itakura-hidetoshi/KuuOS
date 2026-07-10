import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateSelectionAuthorizationGrantV0_71

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSelectionRequestSurface where
  sourceGrant : SubsequentCycleCandidateSelectionAuthorizationGrantSurface
  sourceGrantBound : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  eligibleCandidatesPreserved : Bool
  authorizationScopePreserved : Bool
  authorizationConstraintsPreserved : Bool
  selectionEligibleCount : Nat
  selectionScopeBound : Bool
  selectionCriteriaDigestBound : Bool
  authorizationRequested : Bool
  selectionAuthorityGranted : Bool
  candidateSelectionRequested : Bool
  candidateSelected : Bool
  admissionRequested : Bool
  sourceGrantRequired : sourceGrantBound = true
  candidateSetRequired : candidateSetDigestPreserved = true
  evaluationSetRequired : evaluationSetDigestPreserved = true
  reviewSetRequired : reviewSetDigestPreserved = true
  eligibleCandidatesRequired : eligibleCandidatesPreserved = true
  authorizationScopeRequired : authorizationScopePreserved = true
  authorizationConstraintsRequired : authorizationConstraintsPreserved = true
  eligibleCountPositive : 0 < selectionEligibleCount
  selectionScopeRequired : selectionScopeBound = true
  selectionCriteriaRequired : selectionCriteriaDigestBound = true
  authorizationRequestedRequired : authorizationRequested = true
  authorityGrantedRequired : selectionAuthorityGranted = true
  selectionRequestedRequired : candidateSelectionRequested = true
  candidateSelectionForbidden : candidateSelected = false
  admissionRequestForbidden : admissionRequested = false

structure SubsequentCycleCandidateSelectionRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceAuthorizationGrantPreserved : Bool
  selectionAuthorityGrantPreserved : Bool
  candidateSelectionRequestOnly : Bool
  authorizationRequested : Bool
  selectionAuthorityGranted : Bool
  candidateSelectionRequested : Bool
  candidateSelected : Bool
  admissionRequested : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourceGrantRequired : sourceAuthorizationGrantPreserved = true
  authorityPreservedRequired : selectionAuthorityGrantPreserved = true
  requestOnlyRequired : candidateSelectionRequestOnly = true
  authorizationRequestedRequired : authorizationRequested = true
  authorityGrantedRequired : selectionAuthorityGranted = true
  selectionRequestedRequired : candidateSelectionRequested = true
  candidateSelectionForbidden : candidateSelected = false
  admissionRequestForbidden : admissionRequested = false

structure PlanOSSubsequentCycleCandidateSelectionRequestBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateSelectionRequestSurface → SubsequentCycleCandidateSelectionRequestBoundary → Nat → Digest
  surface : SubsequentCycleCandidateSelectionRequestSurface
  boundary : SubsequentCycleCandidateSelectionRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex

namespace PlanOSSubsequentCycleCandidateSelectionRequestBridge

theorem request_is_authorized_bounded_and_nonselecting
    (b : PlanOSSubsequentCycleCandidateSelectionRequestBridge) :
    b.surface.sourceGrantBound = true ∧
      0 < b.surface.selectionEligibleCount ∧
      b.surface.selectionScopeBound = true ∧
      b.surface.selectionCriteriaDigestBound = true ∧
      b.surface.authorizationRequested = true ∧
      b.surface.selectionAuthorityGranted = true ∧
      b.surface.candidateSelectionRequested = true ∧
      b.surface.candidateSelected = false ∧
      b.surface.admissionRequested = false := by
  exact ⟨b.surface.sourceGrantRequired, b.surface.eligibleCountPositive,
    b.surface.selectionScopeRequired, b.surface.selectionCriteriaRequired,
    b.surface.authorizationRequestedRequired, b.surface.authorityGrantedRequired,
    b.surface.selectionRequestedRequired, b.surface.candidateSelectionForbidden,
    b.surface.admissionRequestForbidden⟩

theorem evidence_chain_is_preserved
    (b : PlanOSSubsequentCycleCandidateSelectionRequestBridge) :
    b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.reviewSetDigestPreserved = true ∧
      b.surface.eligibleCandidatesPreserved = true ∧
      b.surface.authorizationScopePreserved = true ∧
      b.surface.authorizationConstraintsPreserved = true := by
  exact ⟨b.surface.candidateSetRequired, b.surface.evaluationSetRequired,
    b.surface.reviewSetRequired, b.surface.eligibleCandidatesRequired,
    b.surface.authorizationScopeRequired, b.surface.authorizationConstraintsRequired⟩

theorem boundary_is_request_only
    (b : PlanOSSubsequentCycleCandidateSelectionRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceAuthorizationGrantPreserved = true ∧
      b.boundary.selectionAuthorityGrantPreserved = true ∧
      b.boundary.candidateSelectionRequestOnly = true ∧
      b.boundary.candidateSelectionRequested = true ∧
      b.boundary.candidateSelected = false ∧
      b.boundary.admissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceGrantRequired,
    b.boundary.authorityPreservedRequired, b.boundary.requestOnlyRequired,
    b.boundary.selectionRequestedRequired, b.boundary.candidateSelectionForbidden,
    b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_request
    (b : PlanOSSubsequentCycleCandidateSelectionRequestBridge) : b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateSelectionRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateSelectionRequestBridge
end PlanOS
end KUOS
