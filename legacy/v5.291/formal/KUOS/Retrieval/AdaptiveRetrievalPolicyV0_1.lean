import Mathlib

namespace KUOS
namespace Retrieval

inductive RetrievalMode where
  | lexical
  | lexicalRewrite
  | semanticOnDemand
  | hybrid
  | preEmbedded
  | graphRelational
  deriving DecidableEq, Repr

namespace RetrievalMode

def rank : RetrievalMode → ℕ
  | lexical => 0
  | lexicalRewrite => 1
  | semanticOnDemand => 2
  | hybrid => 3
  | preEmbedded => 4
  | graphRelational => 5

end RetrievalMode

/--
A mode is least-sufficient when it is adequate and every strictly simpler mode
is inadequate. Adequacy itself is supplied by the deployment/evidence layer;
this contract does not hard-code engineering thresholds.
-/
def IsLeastSufficient
    (adequate : RetrievalMode → Prop)
    (selected : RetrievalMode) : Prop :=
  adequate selected ∧
    ∀ mode, RetrievalMode.rank mode < RetrievalMode.rank selected → ¬ adequate mode


theorem leastSufficient_is_adequate
    {adequate : RetrievalMode → Prop}
    {selected : RetrievalMode}
    (h : IsLeastSufficient adequate selected) :
    adequate selected := by
  exact h.1


theorem leastSufficient_rejects_simpler
    {adequate : RetrievalMode → Prop}
    {selected mode : RetrievalMode}
    (h : IsLeastSufficient adequate selected)
    (hsimpler : RetrievalMode.rank mode < RetrievalMode.rank selected) :
    ¬ adequate mode := by
  exact h.2 mode hsimpler


theorem noAdequate_no_leastSufficient
    {adequate : RetrievalMode → Prop}
    (h : ∀ mode, ¬ adequate mode)
    (selected : RetrievalMode) :
    ¬ IsLeastSufficient adequate selected := by
  intro hs
  exact h selected hs.1


theorem graphRelational_requires_lexical_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .lexical := by
  exact h.2 .lexical (by simp [RetrievalMode.rank])


theorem graphRelational_requires_lexicalRewrite_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .lexicalRewrite := by
  exact h.2 .lexicalRewrite (by simp [RetrievalMode.rank])


theorem graphRelational_requires_semanticOnDemand_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .semanticOnDemand := by
  exact h.2 .semanticOnDemand (by simp [RetrievalMode.rank])


theorem graphRelational_requires_hybrid_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .hybrid := by
  exact h.2 .hybrid (by simp [RetrievalMode.rank])


theorem graphRelational_requires_preEmbedded_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .preEmbedded := by
  exact h.2 .preEmbedded (by simp [RetrievalMode.rank])


theorem graphRelational_requires_all_simpler_inadequate
    {adequate : RetrievalMode → Prop}
    (h : IsLeastSufficient adequate .graphRelational) :
    ¬ adequate .lexical ∧
      ¬ adequate .lexicalRewrite ∧
      ¬ adequate .semanticOnDemand ∧
      ¬ adequate .hybrid ∧
      ¬ adequate .preEmbedded := by
  constructor
  · exact graphRelational_requires_lexical_inadequate h
  constructor
  · exact graphRelational_requires_lexicalRewrite_inadequate h
  constructor
  · exact graphRelational_requires_semanticOnDemand_inadequate h
  constructor
  · exact graphRelational_requires_hybrid_inadequate h
  · exact graphRelational_requires_preEmbedded_inadequate h


structure RetrievalAuthorityBoundary where
  truthAuthorityGranted : Bool
  worldCommitAuthorityGranted : Bool
  beliefAuthorityGranted : Bool
  decisionAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  clinicalAuthorityGranted : Bool
  theoremAuthorityGranted : Bool
  truthForbidden : truthAuthorityGranted = false
  worldCommitForbidden : worldCommitAuthorityGranted = false
  beliefForbidden : beliefAuthorityGranted = false
  decisionForbidden : decisionAuthorityGranted = false
  executionForbidden : executionAuthorityGranted = false
  clinicalForbidden : clinicalAuthorityGranted = false
  theoremForbidden : theoremAuthorityGranted = false


theorem retrievalBoundary_grants_no_truth_world_or_belief_authority
    (boundary : RetrievalAuthorityBoundary) :
    boundary.truthAuthorityGranted = false ∧
      boundary.worldCommitAuthorityGranted = false ∧
      boundary.beliefAuthorityGranted = false := by
  exact ⟨boundary.truthForbidden, boundary.worldCommitForbidden,
    boundary.beliefForbidden⟩


theorem retrievalBoundary_grants_no_decision_execution_clinical_or_theorem_authority
    (boundary : RetrievalAuthorityBoundary) :
    boundary.decisionAuthorityGranted = false ∧
      boundary.executionAuthorityGranted = false ∧
      boundary.clinicalAuthorityGranted = false ∧
      boundary.theoremAuthorityGranted = false := by
  exact ⟨boundary.decisionForbidden, boundary.executionForbidden,
    boundary.clinicalForbidden, boundary.theoremForbidden⟩


structure NoDataBoundary where
  anyAdequateMode : Bool
  selectedModePresent : Bool
  routeNoData : Bool
  noAdequateMode : anyAdequateMode = false
  noSelection : selectedModePresent = false
  noDataRequired : routeNoData = true


theorem noDataBoundary_has_no_selected_mode
    (boundary : NoDataBoundary) :
    boundary.selectedModePresent = false := by
  exact boundary.noSelection


theorem noDataBoundary_routes_noData
    (boundary : NoDataBoundary) :
    boundary.routeNoData = true := by
  exact boundary.noDataRequired

end Retrieval
end KUOS
