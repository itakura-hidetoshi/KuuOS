import KUOS.PlanOS.WeightedDecisionEvidenceHandoffV0_26

namespace KUOS.PlanOS.DecisionIntakeCandidateEnvelopeV0_27

structure WeightedDecisionEvidenceHandoffSurface where
  sourceVersion : String
  receiptDigest : String
  ready : Prop
  decisionEvidenceOnly : Prop
  selectionOwnedByDecisionOS : Prop
  grantsDecision : Prop
  grantsExecution : Prop
  grantsExternalCommit : Prop

structure DecisionIntakeCandidateEnvelopeBoundary where
  reviewCandidateOnly : Prop
  decisionMade : Prop
  selectedCandidateCommitted : Prop
  activationAuthorizationGranted : Prop
  actosInvoked : Prop
  executionGranted : Prop
  truthAuthorityGranted : Prop
  memoryOverwriteGranted : Prop
  blockerReleaseGranted : Prop
  externalCommitGranted : Prop

structure PlanOSDecisionIntakeCandidateEnvelopeBridge where
  source : WeightedDecisionEvidenceHandoffSurface
  boundary : DecisionIntakeCandidateEnvelopeBoundary
  historyBefore : List String
  historyAfter : List String
  envelopeDigest : String
  sourceDigest : String

axiom source_handoff_version_v0_26 :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.sourceVersion = "kuuos_planos_weighted_decision_evidence_handoff_v0_26"

axiom source_handoff_remains_evidence_only :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.ready → b.source.decisionEvidenceOnly

axiom source_selection_stays_owned_by_decisionos :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.ready → b.source.selectionOwnedByDecisionOS

axiom envelope_is_review_candidate_only :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.ready → b.boundary.reviewCandidateOnly

axiom envelope_grants_no_decision_activation_execution_or_truth :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.ready →
      ¬ b.boundary.decisionMade ∧
      ¬ b.boundary.selectedCandidateCommitted ∧
      ¬ b.boundary.activationAuthorizationGranted ∧
      ¬ b.boundary.actosInvoked ∧
      ¬ b.boundary.executionGranted ∧
      ¬ b.boundary.truthAuthorityGranted ∧
      ¬ b.boundary.memoryOverwriteGranted ∧
      ¬ b.boundary.blockerReleaseGranted ∧
      ¬ b.boundary.externalCommitGranted

axiom source_authority_not_promoted :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.source.ready → ¬ b.source.grantsDecision ∧ ¬ b.source.grantsExecution ∧ ¬ b.source.grantsExternalCommit

axiom history_appends_one_envelope_record :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.historyAfter.length = b.historyBefore.length + 1

axiom digest_binds_source_handoff :
  ∀ b : PlanOSDecisionIntakeCandidateEnvelopeBridge,
    b.sourceDigest = b.source.receiptDigest

end KUOS.PlanOS.DecisionIntakeCandidateEnvelopeV0_27
