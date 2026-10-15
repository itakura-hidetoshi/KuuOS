import KUOS.WORLD.KuuOSOSAssociatedGaugeFieldsV0_61

namespace KUOS.WORLD.KuuOSConnectionCandidateCoreV0_62

structure ConnectionCandidate (R H : Type*) where
  sourceCurvature : R
  candidateCurvature : R
  sourceHolonomy : H
  candidateHolonomy : H
  connectionDomainPreserved : Prop
  groupPreserved : Prop
  fieldsPreserved : Prop
  sourceBindingsPreserved : Prop
  changeBudgetRespected : Prop
  rollbackBound : Prop
  candidateOnly : Prop
  noStateWrite : Prop

structure ConnectionCandidate.Admissible
    {R H : Type*} [LE R]
    (candidate : ConnectionCandidate R H) : Prop where
  curvatureNonincreasing :
    candidate.candidateCurvature ≤ candidate.sourceCurvature
  holonomyPreserved :
    candidate.candidateHolonomy = candidate.sourceHolonomy
  connectionDomainPreserved : candidate.connectionDomainPreserved
  groupPreserved : candidate.groupPreserved
  fieldsPreserved : candidate.fieldsPreserved
  sourceBindingsPreserved : candidate.sourceBindingsPreserved
  changeBudgetRespected : candidate.changeBudgetRespected
  rollbackBound : candidate.rollbackBound
  candidateOnly : candidate.candidateOnly
  noStateWrite : candidate.noStateWrite

def ConnectionCandidate.StrictlyImproves
    {R H : Type*} [LT R]
    (candidate : ConnectionCandidate R H) : Prop :=
  candidate.candidateCurvature < candidate.sourceCurvature

theorem admissible_candidate_cannot_write_state
    {R H : Type*} [LE R]
    (candidate : ConnectionCandidate R H)
    (h : candidate.Admissible) :
    candidate.candidateOnly ∧ candidate.noStateWrite :=
  ⟨h.candidateOnly, h.noStateWrite⟩

end KUOS.WORLD.KuuOSConnectionCandidateCoreV0_62
