import KUOS.WORLD.KuuOSRepositoryFrontierCertificateV0_86

namespace KUOS.WORLD.KuuOSRepositorySelfEvolutionPortfolioV0_87

open KUOS.WORLD.KuuOSRepositoryRevisionDagV0_85
open KUOS.WORLD.KuuOSRepositoryFrontierCertificateV0_86


structure EvolutionCandidate (Revision Path : Type*) where
  sourceTip : Revision
  changedPaths : Finset Path
  scoreBefore : Nat
  scoreAfter : Nat
  riskScore : Nat
  reversible : Bool
  protectedPathsPreserved : Bool
  normalFormPreserved : Bool
deriving DecidableEq


def EvolutionCandidate.Admissible
    {Revision Path : Type*}
    (candidate : EvolutionCandidate Revision Path) : Prop :=
  candidate.scoreAfter < candidate.scoreBefore ∧
    candidate.reversible = true ∧
    candidate.protectedPathsPreserved = true ∧
    candidate.normalFormPreserved = true


structure FrontierEvolutionPortfolio
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag) where
  candidates : Finset (EvolutionCandidate Revision Path)
  selected : Finset (EvolutionCandidate Revision Path)
  selectedSubset : selected ⊆ candidates
  sourceOnFrontier : ∀ candidate ∈ candidates,
    candidate.sourceTip ∈ frontier.tips
  selectedAdmissible : ∀ candidate ∈ selected,
    candidate.Admissible
  selectedPathDisjoint : ∀ first ∈ selected, ∀ second ∈ selected,
    first ≠ second → Disjoint first.changedPaths second.changedPaths
  onePerTip : ∀ first ∈ selected, ∀ second ∈ selected,
    first.sourceTip = second.sourceTip → first = second


structure SelfEvolutionWitness where
  sourceFrontierBound : Prop
  finiteCandidateBound : Prop
  finitePortfolioEnumeration : Prop
  strictScoreDescent : Prop
  protectedPathsPreserved : Prop
  reversibleSelection : Prop
  normalFormPreserved : Prop
  selectedPathsNonconflicting : Prop
  oneCandidatePerFrontier : Prop
  deterministicOptimum : Prop
  stableNoChangeFixedPoint : Prop


structure SelfEvolutionWitness.Valid (witness : SelfEvolutionWitness) : Prop where
  sourceFrontierBound : witness.sourceFrontierBound
  finiteCandidateBound : witness.finiteCandidateBound
  finitePortfolioEnumeration : witness.finitePortfolioEnumeration
  strictScoreDescent : witness.strictScoreDescent
  protectedPathsPreserved : witness.protectedPathsPreserved
  reversibleSelection : witness.reversibleSelection
  normalFormPreserved : witness.normalFormPreserved
  selectedPathsNonconflicting : witness.selectedPathsNonconflicting
  oneCandidatePerFrontier : witness.oneCandidatePerFrontier
  deterministicOptimum : witness.deterministicOptimum
  stableNoChangeFixedPoint : witness.stableNoChangeFixedPoint


theorem selected_card_le_candidate_card
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    {dag : RankedRevisionDag Revision}
    {frontier : RevisionFrontier dag}
    (portfolio : FrontierEvolutionPortfolio (Path := Path) dag frontier) :
    portfolio.selected.card ≤ portfolio.candidates.card := by
  exact Finset.card_le_card portfolio.selectedSubset


theorem selected_candidate_source_is_frontier
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    {dag : RankedRevisionDag Revision}
    {frontier : RevisionFrontier dag}
    (portfolio : FrontierEvolutionPortfolio (Path := Path) dag frontier)
    {candidate : EvolutionCandidate Revision Path}
    (hSelected : candidate ∈ portfolio.selected) :
    candidate.sourceTip ∈ frontier.tips := by
  exact portfolio.sourceOnFrontier candidate (portfolio.selectedSubset hSelected)


theorem selected_candidate_strictly_decreases_score
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    {dag : RankedRevisionDag Revision}
    {frontier : RevisionFrontier dag}
    (portfolio : FrontierEvolutionPortfolio (Path := Path) dag frontier)
    {candidate : EvolutionCandidate Revision Path}
    (hSelected : candidate ∈ portfolio.selected) :
    candidate.scoreAfter < candidate.scoreBefore := by
  exact (portfolio.selectedAdmissible candidate hSelected).1


theorem distinct_selected_candidates_have_disjoint_paths
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    {dag : RankedRevisionDag Revision}
    {frontier : RevisionFrontier dag}
    (portfolio : FrontierEvolutionPortfolio (Path := Path) dag frontier)
    {first second : EvolutionCandidate Revision Path}
    (hFirst : first ∈ portfolio.selected)
    (hSecond : second ∈ portfolio.selected)
    (hDistinct : first ≠ second) :
    Disjoint first.changedPaths second.changedPaths := by
  exact portfolio.selectedPathDisjoint first hFirst second hSecond hDistinct


theorem same_frontier_tip_forces_same_selected_candidate
    {Revision Path : Type*}
    [DecidableEq Revision]
    [DecidableEq Path]
    {dag : RankedRevisionDag Revision}
    {frontier : RevisionFrontier dag}
    (portfolio : FrontierEvolutionPortfolio (Path := Path) dag frontier)
    {first second : EvolutionCandidate Revision Path}
    (hFirst : first ∈ portfolio.selected)
    (hSecond : second ∈ portfolio.selected)
    (hSameTip : first.sourceTip = second.sourceTip) :
    first = second := by
  exact portfolio.onePerTip first hFirst second hSecond hSameTip


theorem strict_evolution_cannot_form_two_score_cycle
    {Revision Path : Type*}
    (candidate : EvolutionCandidate Revision Path)
    (hAdmissible : candidate.Admissible) :
    ¬ candidate.scoreBefore < candidate.scoreAfter := by
  exact Nat.lt_asymm hAdmissible.1


theorem two_step_self_evolution_strictly_descends
    {before middle after : Nat}
    (hFirst : middle < before)
    (hSecond : after < middle) :
    after < before := by
  exact Nat.lt_trans hSecond hFirst


theorem valid_self_evolution_certificate
    (witness : SelfEvolutionWitness)
    (h : witness.Valid) :
    witness.sourceFrontierBound ∧
      witness.finiteCandidateBound ∧
      witness.finitePortfolioEnumeration ∧
      witness.strictScoreDescent ∧
      witness.protectedPathsPreserved ∧
      witness.reversibleSelection ∧
      witness.normalFormPreserved ∧
      witness.selectedPathsNonconflicting ∧
      witness.oneCandidatePerFrontier ∧
      witness.deterministicOptimum ∧
      witness.stableNoChangeFixedPoint := by
  exact ⟨h.sourceFrontierBound, h.finiteCandidateBound,
    h.finitePortfolioEnumeration, h.strictScoreDescent,
    h.protectedPathsPreserved, h.reversibleSelection,
    h.normalFormPreserved, h.selectedPathsNonconflicting,
    h.oneCandidatePerFrontier, h.deterministicOptimum,
    h.stableNoChangeFixedPoint⟩

end KUOS.WORLD.KuuOSRepositorySelfEvolutionPortfolioV0_87
