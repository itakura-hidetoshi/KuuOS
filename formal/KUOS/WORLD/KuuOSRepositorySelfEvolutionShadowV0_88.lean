import KUOS.WORLD.KuuOSRepositorySelfEvolutionPortfolioV0_87

namespace KUOS.WORLD.KuuOSRepositorySelfEvolutionShadowV0_88

open KUOS.WORLD.KuuOSRepositorySelfEvolutionPortfolioV0_87


structure ShadowAssessment (CandidateId : Type*) where
  candidateId : CandidateId
  baselineScore : Nat
  predictedScore : Nat
  observedScore : Nat
  predictionError : Nat
  predictionTolerance : Nat
  proposalBound : Prop
  sourceCommitBound : Prop
  sourceSnapshotBound : Prop
  sourceObservationBound : Prop
  changedPathsBound : Prop
  baselineScoreBound : Prop
  protectedPathsPreserved : Prop
  exactRollback : Prop
  normalFormCertified : Prop


def ShadowAssessment.Admissible
    {CandidateId : Type*}
    (assessment : ShadowAssessment CandidateId) : Prop :=
  assessment.observedScore < assessment.baselineScore ∧
    assessment.predictionError ≤ assessment.predictionTolerance ∧
    assessment.proposalBound ∧
    assessment.sourceCommitBound ∧
    assessment.sourceSnapshotBound ∧
    assessment.sourceObservationBound ∧
    assessment.changedPathsBound ∧
    assessment.baselineScoreBound ∧
    assessment.protectedPathsPreserved ∧
    assessment.exactRollback ∧
    assessment.normalFormCertified


structure ShadowPortfolio
    (CandidateId : Type*)
    [DecidableEq CandidateId] where
  selected : Finset CandidateId
  assessed : Finset CandidateId
  exactCoverage : assessed = selected
  assessmentFor : CandidateId → ShadowAssessment CandidateId
  assessmentIdentity : ∀ candidate ∈ assessed,
    (assessmentFor candidate).candidateId = candidate
  selectedAdmissible : ∀ candidate ∈ selected,
    (assessmentFor candidate).Admissible


structure ShadowAuthorityBoundary where
  patchApplicationAuthority : Bool
  commitAuthority : Bool
  referenceMutationAuthority : Bool


structure ShadowAuthorityBoundary.Valid
    (boundary : ShadowAuthorityBoundary) : Prop where
  patchApplicationAuthority : boundary.patchApplicationAuthority = false
  commitAuthority : boundary.commitAuthority = false
  referenceMutationAuthority : boundary.referenceMutationAuthority = false


structure ShadowWitness where
  exactSelectedCoverage : Prop
  objectDatabaseSourcesOnly : Prop
  workingTreeIgnored : Prop
  allBindingsExact : Prop
  strictScoreDescentObserved : Prop
  predictionsWithinTolerance : Prop
  protectedPathsPreserved : Prop
  exactShadowRollback : Prop
  normalFormCertified : Prop


structure ShadowWitness.Valid (witness : ShadowWitness) : Prop where
  exactSelectedCoverage : witness.exactSelectedCoverage
  objectDatabaseSourcesOnly : witness.objectDatabaseSourcesOnly
  workingTreeIgnored : witness.workingTreeIgnored
  allBindingsExact : witness.allBindingsExact
  strictScoreDescentObserved : witness.strictScoreDescentObserved
  predictionsWithinTolerance : witness.predictionsWithinTolerance
  protectedPathsPreserved : witness.protectedPathsPreserved
  exactShadowRollback : witness.exactShadowRollback
  normalFormCertified : witness.normalFormCertified


theorem assessed_card_eq_selected_card
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId) :
    portfolio.assessed.card = portfolio.selected.card := by
  rw [portfolio.exactCoverage]


theorem selected_shadow_strictly_decreases_score
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId)
    {candidate : CandidateId}
    (hSelected : candidate ∈ portfolio.selected) :
    (portfolio.assessmentFor candidate).observedScore <
      (portfolio.assessmentFor candidate).baselineScore := by
  exact (portfolio.selectedAdmissible candidate hSelected).1


theorem selected_prediction_error_is_bounded
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId)
    {candidate : CandidateId}
    (hSelected : candidate ∈ portfolio.selected) :
    (portfolio.assessmentFor candidate).predictionError ≤
      (portfolio.assessmentFor candidate).predictionTolerance := by
  exact (portfolio.selectedAdmissible candidate hSelected).2.1


theorem selected_shadow_restores_exact_source
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId)
    {candidate : CandidateId}
    (hSelected : candidate ∈ portfolio.selected) :
    (portfolio.assessmentFor candidate).exactRollback := by
  exact (portfolio.selectedAdmissible candidate hSelected).2.2.2.2.2.2.2.2.2.2.1


theorem selected_shadow_has_certified_normal_form
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId)
    {candidate : CandidateId}
    (hSelected : candidate ∈ portfolio.selected) :
    (portfolio.assessmentFor candidate).normalFormCertified := by
  exact (portfolio.selectedAdmissible candidate hSelected).2.2.2.2.2.2.2.2.2.2.2


theorem strict_shadow_replay_cannot_reverse_score_order
    {CandidateId : Type*}
    (assessment : ShadowAssessment CandidateId)
    (hAdmissible : assessment.Admissible) :
    ¬ assessment.baselineScore < assessment.observedScore := by
  exact Nat.lt_asymm hAdmissible.1


theorem stable_shadow_portfolio_has_no_assessments
    {CandidateId : Type*}
    [DecidableEq CandidateId]
    (portfolio : ShadowPortfolio CandidateId)
    (hStable : portfolio.selected = ∅) :
    portfolio.assessed = ∅ := by
  calc
    portfolio.assessed = portfolio.selected := portfolio.exactCoverage
    _ = ∅ := hStable


theorem valid_shadow_authority_boundary
    (boundary : ShadowAuthorityBoundary)
    (h : boundary.Valid) :
    boundary.patchApplicationAuthority = false ∧
      boundary.commitAuthority = false ∧
      boundary.referenceMutationAuthority = false := by
  exact ⟨h.patchApplicationAuthority, h.commitAuthority,
    h.referenceMutationAuthority⟩


theorem valid_shadow_witness
    (witness : ShadowWitness)
    (h : witness.Valid) :
    witness.exactSelectedCoverage ∧
      witness.objectDatabaseSourcesOnly ∧
      witness.workingTreeIgnored ∧
      witness.allBindingsExact ∧
      witness.strictScoreDescentObserved ∧
      witness.predictionsWithinTolerance ∧
      witness.protectedPathsPreserved ∧
      witness.exactShadowRollback ∧
      witness.normalFormCertified := by
  exact ⟨h.exactSelectedCoverage, h.objectDatabaseSourcesOnly,
    h.workingTreeIgnored, h.allBindingsExact,
    h.strictScoreDescentObserved, h.predictionsWithinTolerance,
    h.protectedPathsPreserved, h.exactShadowRollback,
    h.normalFormCertified⟩

end KUOS.WORLD.KuuOSRepositorySelfEvolutionShadowV0_88
