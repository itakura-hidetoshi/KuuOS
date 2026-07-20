import Mathlib.Data.Nat.Basic

namespace KUOS.CodeAI.TypedStructuredEditIRV0_1

inductive EditOperation where
  | createFile
  | replaceSymbol
  | insertBeforeSymbol
  | insertAfterSymbol
  | deleteSymbol
  deriving DecidableEq, Repr

inductive EditLanguage where
  | python
  | lean
  deriving DecidableEq, Repr

structure AnchorPrecondition where
  pathSelectedInContext : Bool
  fileDigestMatched : Bool
  symbolKindMatched : Bool
  symbolNameMatched : Bool
  anchorDigestMatched : Bool
  startLineMatched : Bool
  endLineMatched : Bool
  pathAbsent : Bool
  deriving Repr

structure TypedEdit where
  operation : EditOperation
  language : EditLanguage
  precondition : AnchorPrecondition
  newTextBytes : Nat
  deriving Repr

def IsExistingSymbolOperation : EditOperation → Prop
  | .createFile => False
  | .replaceSymbol => True
  | .insertBeforeSymbol => True
  | .insertAfterSymbol => True
  | .deleteSymbol => True

structure WellFormedExistingEdit (edit : TypedEdit) : Prop where
  isExistingSymbolOperation : IsExistingSymbolOperation edit.operation
  pathSelectedInContext :
    edit.precondition.pathSelectedInContext = true
  fileDigestMatched :
    edit.precondition.fileDigestMatched = true
  symbolKindMatched :
    edit.precondition.symbolKindMatched = true
  symbolNameMatched :
    edit.precondition.symbolNameMatched = true
  anchorDigestMatched :
    edit.precondition.anchorDigestMatched = true
  startLineMatched :
    edit.precondition.startLineMatched = true
  endLineMatched :
    edit.precondition.endLineMatched = true
  pathNotTreatedAsAbsent :
    edit.precondition.pathAbsent = false

structure WellFormedCreateEdit (edit : TypedEdit) : Prop where
  isCreateFile : edit.operation = .createFile
  pathAbsent : edit.precondition.pathAbsent = true
  noExistingContextRequirement :
    edit.precondition.pathSelectedInContext = false
  noFileDigestClaim :
    edit.precondition.fileDigestMatched = false
  noAnchorDigestClaim :
    edit.precondition.anchorDigestMatched = false

theorem existingEditHasSelectedContext
    (edit : TypedEdit)
    (h : WellFormedExistingEdit edit) :
    edit.precondition.pathSelectedInContext = true := by
  exact h.pathSelectedInContext

theorem existingEditHasExactFilePrecondition
    (edit : TypedEdit)
    (h : WellFormedExistingEdit edit) :
    edit.precondition.fileDigestMatched = true := by
  exact h.fileDigestMatched

theorem existingEditHasExactAnchorPrecondition
    (edit : TypedEdit)
    (h : WellFormedExistingEdit edit) :
    edit.precondition.anchorDigestMatched = true := by
  exact h.anchorDigestMatched

theorem existingEditHasExactLinePreconditions
    (edit : TypedEdit)
    (h : WellFormedExistingEdit edit) :
    edit.precondition.startLineMatched = true ∧
      edit.precondition.endLineMatched = true := by
  exact ⟨h.startLineMatched, h.endLineMatched⟩

theorem createEditRequiresAbsentPath
    (edit : TypedEdit)
    (h : WellFormedCreateEdit edit) :
    edit.precondition.pathAbsent = true := by
  exact h.pathAbsent

structure IRCounts where
  operationCount : Nat
  totalNewTextBytes : Nat
  maximumOperations : Nat
  maximumTotalNewTextBytes : Nat
  deriving Repr

structure WellFormedIRCounts (counts : IRCounts) : Prop where
  operationCountBounded :
    counts.operationCount ≤ counts.maximumOperations
  totalNewTextBytesBounded :
    counts.totalNewTextBytes ≤ counts.maximumTotalNewTextBytes

theorem operationCountIsBounded
    (counts : IRCounts)
    (h : WellFormedIRCounts counts) :
    counts.operationCount ≤ counts.maximumOperations := by
  exact h.operationCountBounded

theorem totalNewTextBytesAreBounded
    (counts : IRCounts)
    (h : WellFormedIRCounts counts) :
    counts.totalNewTextBytes ≤ counts.maximumTotalNewTextBytes := by
  exact h.totalNewTextBytesBounded

structure Receipt where
  routeReceiptRecorded : Bool
  typedStructuredEditIREmitted : Bool
  typedOperationsOnly : Bool
  wholeFileModifyAllowed : Bool
  symbolPreconditionsVerified : Bool
  contextLineageVerified : Bool
  repositorySnapshotReadOnly : Bool
  providerInvoked : Bool
  verificationRunnerInvoked : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  candidateSelectionAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  correctnessProofClaimed : Bool
  deriving Repr

structure GovernedReceipt (receipt : Receipt) : Prop where
  routeReceiptRecorded :
    receipt.routeReceiptRecorded = true
  typedStructuredEditIREmitted :
    receipt.typedStructuredEditIREmitted = true
  typedOperationsOnly :
    receipt.typedOperationsOnly = true
  wholeFileModifyProhibited :
    receipt.wholeFileModifyAllowed = false
  symbolPreconditionsVerified :
    receipt.symbolPreconditionsVerified = true
  contextLineageVerified :
    receipt.contextLineageVerified = true
  repositorySnapshotReadOnly :
    receipt.repositorySnapshotReadOnly = true
  providerNotInvoked :
    receipt.providerInvoked = false
  verificationRunnerNotInvoked :
    receipt.verificationRunnerInvoked = false
  repositoryNotMutated :
    receipt.repositoryMutationPerformed = false
  gitEffectNotPerformed :
    receipt.gitEffectPerformed = false
  candidateSelectionAuthorityNotGranted :
    receipt.candidateSelectionAuthorityGranted = false
  executionAuthorityNotGranted :
    receipt.executionAuthorityGranted = false
  correctnessProofNotClaimed :
    receipt.correctnessProofClaimed = false

theorem governedReceiptProhibitsWholeFileModify
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.wholeFileModifyAllowed = false := by
  exact h.wholeFileModifyProhibited

theorem governedReceiptVerifiesSymbolPreconditions
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.symbolPreconditionsVerified = true := by
  exact h.symbolPreconditionsVerified

theorem governedReceiptHasNoRepositoryMutation
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.repositoryMutationPerformed = false := by
  exact h.repositoryNotMutated

theorem governedReceiptHasNoGitEffect
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.gitEffectPerformed = false := by
  exact h.gitEffectNotPerformed

theorem governedReceiptGrantsNoCandidateSelectionAuthority
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.candidateSelectionAuthorityGranted = false := by
  exact h.candidateSelectionAuthorityNotGranted

theorem governedReceiptGrantsNoExecutionAuthority
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.executionAuthorityGranted = false := by
  exact h.executionAuthorityNotGranted

theorem governedReceiptClaimsNoCorrectnessProof
    (receipt : Receipt)
    (h : GovernedReceipt receipt) :
    receipt.correctnessProofClaimed = false := by
  exact h.correctnessProofNotClaimed

end KUOS.CodeAI.TypedStructuredEditIRV0_1
