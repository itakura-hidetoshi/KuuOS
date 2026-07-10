import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateSelectionAuthorizationRequestV0_70

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSelectionAuthorizationGrantSurface where
  sourceRequest : SubsequentCycleCandidateSelectionAuthorizationRequestSurface
  sourceRequestBoundary : SubsequentCycleCandidateSelectionAuthorizationRequestBoundary
  sourceRequestBound : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  selectionEligibleCandidatesPreserved : Bool
  authorizationScopePreserved : Bool
  authorizationConstraintsDigestPreserved : Bool
  selectionEligibleCount : Nat
  authorizationGrantDigestBound : Bool
  subsequentCycleCandidateSelectionAuthorizationRequested : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequestRequired : sourceRequestBound = true
  candidateSetRequired : candidateSetDigestPreserved = true
  evaluationSetRequired : evaluationSetDigestPreserved = true
  reviewSetRequired : reviewSetDigestPreserved = true
  eligibleCandidatesRequired : selectionEligibleCandidatesPreserved = true
  authorizationScopeRequired : authorizationScopePreserved = true
  constraintsRequired : authorizationConstraintsDigestPreserved = true
  eligibleCountPositive : 0 < selectionEligibleCount
  grantDigestRequired : authorizationGrantDigestBound = true
  authorizationRequestedRequired : subsequentCycleCandidateSelectionAuthorizationRequested = true
  authorityGrantedRequired : subsequentCycleSelectionAuthorityGranted = true
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateSelectionAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceCandidateSelectionAuthorizationRequestPreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  selectionEligibleCandidatesPreserved : Bool
  authorizationScopePreserved : Bool
  authorizationConstraintsDigestPreserved : Bool
  subsequentCycleCandidateSelectionAuthorizationGrantOnly : Bool
  subsequentCycleCandidateSelectionAuthorizationRequested : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : grantOwnedByPlanOS = true
  sourceRequired : sourceCandidateSelectionAuthorizationRequestPreserved = true
  candidateSetRequired : candidateSetDigestPreserved = true
  evaluationSetRequired : evaluationSetDigestPreserved = true
  reviewSetRequired : reviewSetDigestPreserved = true
  eligibleCandidatesRequired : selectionEligibleCandidatesPreserved = true
  authorizationScopeRequired : authorizationScopePreserved = true
  constraintsRequired : authorizationConstraintsDigestPreserved = true
  grantOnlyRequired : subsequentCycleCandidateSelectionAuthorizationGrantOnly = true
  authorizationRequestedRequired : subsequentCycleCandidateSelectionAuthorizationRequested = true
  authorityGrantedRequired : subsequentCycleSelectionAuthorityGranted = true
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateSelectionAuthorizationGrantSurface →
    SubsequentCycleCandidateSelectionAuthorizationGrantBoundary → Nat → Digest
  surface : SubsequentCycleCandidateSelectionAuthorizationGrantSurface
  boundary : SubsequentCycleCandidateSelectionAuthorizationGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge

 theorem source_request_is_ready_without_prior_grant
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge) :
    b.surface.sourceRequest.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
      b.surface.sourceRequest.subsequentCycleSelectionAuthorityGranted = false ∧
      b.surface.sourceRequest.subsequentCycleCandidateSelectionRequested = false ∧
      b.surface.sourceRequest.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceRequest.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequest.authorizationRequestedRequired,
    b.surface.sourceRequest.selectionAuthorityForbidden,
    b.surface.sourceRequest.selectionRequestForbidden,
    b.surface.sourceRequest.candidateSelectionForbidden,
    b.surface.sourceRequest.admissionRequestForbidden⟩

 theorem grant_preserves_evidence_and_grants_authority_only
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.reviewSetDigestPreserved = true ∧
      b.surface.selectionEligibleCandidatesPreserved = true ∧
      b.surface.authorizationScopePreserved = true ∧
      b.surface.authorizationConstraintsDigestPreserved = true ∧
      0 < b.surface.selectionEligibleCount ∧
      b.surface.authorizationGrantDigestBound = true ∧
      b.surface.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
      b.surface.subsequentCycleSelectionAuthorityGranted = true ∧
      b.surface.subsequentCycleCandidateSelectionRequested = false ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequestRequired, b.surface.candidateSetRequired,
    b.surface.evaluationSetRequired, b.surface.reviewSetRequired,
    b.surface.eligibleCandidatesRequired, b.surface.authorizationScopeRequired,
    b.surface.constraintsRequired, b.surface.eligibleCountPositive,
    b.surface.grantDigestRequired, b.surface.authorizationRequestedRequired,
    b.surface.authorityGrantedRequired, b.surface.selectionRequestForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden⟩

 theorem boundary_is_authorization_grant_only
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateSelectionAuthorizationRequestPreserved = true ∧
      b.boundary.candidateSetDigestPreserved = true ∧
      b.boundary.evaluationSetDigestPreserved = true ∧
      b.boundary.reviewSetDigestPreserved = true ∧
      b.boundary.selectionEligibleCandidatesPreserved = true ∧
      b.boundary.authorizationScopePreserved = true ∧
      b.boundary.authorizationConstraintsDigestPreserved = true ∧
      b.boundary.subsequentCycleCandidateSelectionAuthorizationGrantOnly = true ∧
      b.boundary.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
      b.boundary.subsequentCycleSelectionAuthorityGranted = true ∧
      b.boundary.subsequentCycleCandidateSelectionRequested = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceRequired,
    b.boundary.candidateSetRequired, b.boundary.evaluationSetRequired,
    b.boundary.reviewSetRequired, b.boundary.eligibleCandidatesRequired,
    b.boundary.authorizationScopeRequired, b.boundary.constraintsRequired,
    b.boundary.grantOnlyRequired, b.boundary.authorizationRequestedRequired,
    b.boundary.authorityGrantedRequired, b.boundary.selectionRequestForbidden,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

 theorem history_appends_one_authorization_grant
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

 theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateSelectionAuthorizationGrantBridge
end PlanOS
end KUOS
