import KUOS.WORLD.KuuOSApoptosisQuiescenceReviewV0_5

namespace KUOS.WORLD.KuuOSApoptosisExternalReviewV0_6

inductive ExternalReviewStatus where
  | clearForIndependentAuthorization
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure ApoptosisExternalReviewWitness where
  sourceQuiescenceRecomputedValid : Bool
  sourceQuiescenceClear : Bool
  sourceBindingValid : Bool
  reviewerQualified : Bool
  reviewerIndependentFromPriorChain : Bool
  reviewerIndependentFromAuthorizationAuthority : Bool
  reviewerIndependentFromExecutionAuthority : Bool
  conflictDisclosureComplete : Bool
  materialConflictPresent : Bool
  reviewScopeComplete : Bool
  reviewMethodologyPresent : Bool
  evidenceReceiptComplete : Bool
  appealRoutePresent : Bool
  dissentRoutePresent : Bool
  protectedCoreExcluded : Bool
  institutionalHoldActive : Bool
  emergencyStateActive : Bool
  reviewFresh : Bool
  reviewNotExpired : Bool
  status : ExternalReviewStatus
  externalReviewRecordIssued : Bool
  externalClearForIndependentAuthorization : Bool
  independentAuthorizationRequiredNext : Bool
  authorizationRequestIssued : Bool
  authorizationDecisionMade : Bool
  authorityRevocationPerformed : Bool
  quiescenceTransitionPerformed : Bool
  terminalTransitionPerformed : Bool
  tombstoneWritePerformed : Bool
  physicalDeletionPerformed : Bool
  liveGitExecutionPerformed : Bool
  repositoryMutationPerformed : Bool


def ApoptosisExternalReviewWitness.IsClear
    (w : ApoptosisExternalReviewWitness) : Prop :=
  w.sourceQuiescenceRecomputedValid = true ∧
  w.sourceQuiescenceClear = true ∧
  w.sourceBindingValid = true ∧
  w.reviewerQualified = true ∧
  w.reviewerIndependentFromPriorChain = true ∧
  w.reviewerIndependentFromAuthorizationAuthority = true ∧
  w.reviewerIndependentFromExecutionAuthority = true ∧
  w.conflictDisclosureComplete = true ∧
  w.materialConflictPresent = false ∧
  w.reviewScopeComplete = true ∧
  w.reviewMethodologyPresent = true ∧
  w.evidenceReceiptComplete = true ∧
  w.appealRoutePresent = true ∧
  w.dissentRoutePresent = true ∧
  w.protectedCoreExcluded = true ∧
  w.institutionalHoldActive = false ∧
  w.emergencyStateActive = false ∧
  w.reviewFresh = true ∧
  w.reviewNotExpired = true ∧
  w.status = ExternalReviewStatus.clearForIndependentAuthorization ∧
  w.externalReviewRecordIssued = true ∧
  w.externalClearForIndependentAuthorization = true ∧
  w.independentAuthorizationRequiredNext = true


def ApoptosisExternalReviewWitness.IsBlocked
    (w : ApoptosisExternalReviewWitness) : Prop :=
  w.status = ExternalReviewStatus.blocked ∧
  w.externalReviewRecordIssued = true ∧
  w.externalClearForIndependentAuthorization = false ∧
  w.independentAuthorizationRequiredNext = false


def ApoptosisExternalReviewWitness.IsRejected
    (w : ApoptosisExternalReviewWitness) : Prop :=
  w.status = ExternalReviewStatus.rejected ∧
  w.externalReviewRecordIssued = false ∧
  w.externalClearForIndependentAuthorization = false ∧
  w.independentAuthorizationRequiredNext = false


def ApoptosisExternalReviewWitness.ReadOnly
    (w : ApoptosisExternalReviewWitness) : Prop :=
  w.authorizationRequestIssued = false ∧
  w.authorizationDecisionMade = false ∧
  w.authorityRevocationPerformed = false ∧
  w.quiescenceTransitionPerformed = false ∧
  w.terminalTransitionPerformed = false ∧
  w.tombstoneWritePerformed = false ∧
  w.physicalDeletionPerformed = false ∧
  w.liveGitExecutionPerformed = false ∧
  w.repositoryMutationPerformed = false


def ApoptosisExternalReviewWitness.Valid
    (w : ApoptosisExternalReviewWitness) : Prop :=
  (w.IsClear ∨ w.IsBlocked ∨ w.IsRejected) ∧ w.ReadOnly


theorem clear_requires_independent_authorization
    (w : ApoptosisExternalReviewWitness)
    (h : w.IsClear) :
    w.independentAuthorizationRequiredNext = true := by
  exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2


theorem blocked_does_not_advance
    (w : ApoptosisExternalReviewWitness)
    (h : w.IsBlocked) :
    w.externalClearForIndependentAuthorization = false ∧
      w.independentAuthorizationRequiredNext = false := by
  exact ⟨h.2.2.1, h.2.2.2⟩


theorem rejected_issues_no_valid_record
    (w : ApoptosisExternalReviewWitness)
    (h : w.IsRejected) :
    w.externalReviewRecordIssued = false := by
  exact h.2.1


theorem valid_external_review_performs_no_effect
    (w : ApoptosisExternalReviewWitness)
    (h : w.Valid) :
    w.ReadOnly := by
  exact h.2


structure ApoptosisExternalReviewDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_external_review
    {Input Output : Type}
    (derivation : ApoptosisExternalReviewDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSApoptosisExternalReviewV0_6
