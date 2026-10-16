import KUOS.WORLD.KuuOSApoptosisObservationV0_1

namespace KUOS.WORLD.KuuOSApoptosisCandidateV0_2

inductive CandidateStatus where
  | proposed
  | rejected
  deriving DecidableEq, Repr

structure ApoptosisCandidateWitness where
  sourceRecomputedValid : Bool
  sourceReviewRecommended : Bool
  sourceNonProtected : Bool
  sourceNoHold : Bool
  sourceBindingValid : Bool
  issuerAllowed : Bool
  objectiveAllowed : Bool
  candidateDelayValid : Bool
  status : CandidateStatus
  dependencyReviewRequired : Bool
  authorityReviewRequired : Bool
  quiescenceReviewRequired : Bool
  externalReviewRequired : Bool
  independentAuthorizationRequired : Bool
  candidateArtifactIssued : Bool
  authorityRevocationPerformed : Bool
  quiescenceTransitionPerformed : Bool
  terminalTransitionPerformed : Bool
  tombstoneWritePerformed : Bool
  physicalDeletionPerformed : Bool
  liveGitExecutionPerformed : Bool
  repositoryMutationPerformed : Bool

structure ApoptosisCandidateWitness.ValidProposed
    (w : ApoptosisCandidateWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceReviewRecommended : w.sourceReviewRecommended = true
  sourceNonProtected : w.sourceNonProtected = true
  sourceNoHold : w.sourceNoHold = true
  sourceBindingValid : w.sourceBindingValid = true
  issuerAllowed : w.issuerAllowed = true
  objectiveAllowed : w.objectiveAllowed = true
  candidateDelayValid : w.candidateDelayValid = true
  statusProposed : w.status = CandidateStatus.proposed
  dependencyReviewRequired : w.dependencyReviewRequired = true
  authorityReviewRequired : w.authorityReviewRequired = true
  quiescenceReviewRequired : w.quiescenceReviewRequired = true
  externalReviewRequired : w.externalReviewRequired = true
  independentAuthorizationRequired :
    w.independentAuthorizationRequired = true
  candidateArtifactIssued : w.candidateArtifactIssued = true
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false

structure ApoptosisCandidateWitness.ValidRejected
    (w : ApoptosisCandidateWitness) : Prop where
  statusRejected : w.status = CandidateStatus.rejected
  candidateArtifactNotIssued : w.candidateArtifactIssued = false
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false


theorem proposed_candidate_requires_independent_reviews
    (w : ApoptosisCandidateWitness)
    (h : w.ValidProposed) :
    w.dependencyReviewRequired = true ∧
      w.authorityReviewRequired = true ∧
      w.quiescenceReviewRequired = true ∧
      w.externalReviewRequired = true ∧
      w.independentAuthorizationRequired = true := by
  exact ⟨h.dependencyReviewRequired, h.authorityReviewRequired,
    h.quiescenceReviewRequired, h.externalReviewRequired,
    h.independentAuthorizationRequired⟩


theorem proposed_candidate_performs_no_lifecycle_effect
    (w : ApoptosisCandidateWitness)
    (h : w.ValidProposed) :
    w.authorityRevocationPerformed = false ∧
      w.quiescenceTransitionPerformed = false ∧
      w.terminalTransitionPerformed = false ∧
      w.tombstoneWritePerformed = false ∧
      w.physicalDeletionPerformed = false ∧
      w.liveGitExecutionPerformed = false ∧
      w.repositoryMutationPerformed = false := by
  exact ⟨h.authorityRevocationNotPerformed,
    h.quiescenceTransitionNotPerformed,
    h.terminalTransitionNotPerformed,
    h.tombstoneWriteNotPerformed,
    h.physicalDeletionNotPerformed,
    h.liveGitExecutionNotPerformed,
    h.repositoryMutationNotPerformed⟩


theorem candidate_artifact_is_not_terminal_transition
    (w : ApoptosisCandidateWitness)
    (h : w.ValidProposed) :
    w.candidateArtifactIssued = true ∧
      w.terminalTransitionPerformed = false := by
  exact ⟨h.candidateArtifactIssued, h.terminalTransitionNotPerformed⟩


theorem valid_candidate_never_mutates_repository
    (w : ApoptosisCandidateWitness)
    (h : w.ValidProposed ∨ w.ValidRejected) :
    w.liveGitExecutionPerformed = false ∧
      w.repositoryMutationPerformed = false := by
  rcases h with h | h
  · exact ⟨h.liveGitExecutionNotPerformed,
      h.repositoryMutationNotPerformed⟩
  · exact ⟨h.liveGitExecutionNotPerformed,
      h.repositoryMutationNotPerformed⟩


structure ApoptosisCandidateDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_apoptosis_candidate
    {Input Output : Type}
    (derivation : ApoptosisCandidateDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSApoptosisCandidateV0_2
