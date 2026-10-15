import KUOS.WORLD.KuuOSConnectionReviewCoreV0_63

namespace KUOS.WORLD.KuuOSConnectionEvaluationCoreV0_64

structure EvaluationCase where
  curvatureNonincreasing : Prop
  curvatureStrictlyDecreased : Prop
  memoryHolonomyPreserved : Prop
  fieldsPreserved : Prop
  sourceBindingsPreserved : Prop

structure EvaluationCase.Admissible (evaluationCase : EvaluationCase) : Prop where
  curvatureNonincreasing : evaluationCase.curvatureNonincreasing
  memoryHolonomyPreserved : evaluationCase.memoryHolonomyPreserved
  fieldsPreserved : evaluationCase.fieldsPreserved
  sourceBindingsPreserved : evaluationCase.sourceBindingsPreserved

structure FiniteEvaluation where
  allCasesAdmissible : Prop
  strictImprovementObserved : Prop
  exactAdmissionBinding : Prop
  exactSourceBinding : Prop
  exactProposalBinding : Prop
  exactCandidateBinding : Prop
  exactRollbackBinding : Prop
  stagingReviewOnly : Prop
  noProductionApply : Prop
  noStateWrite : Prop
  noAuthorityWidening : Prop

structure FiniteEvaluation.Safe (evaluation : FiniteEvaluation) : Prop where
  allCasesAdmissible : evaluation.allCasesAdmissible
  strictImprovementObserved : evaluation.strictImprovementObserved
  exactAdmissionBinding : evaluation.exactAdmissionBinding
  exactSourceBinding : evaluation.exactSourceBinding
  exactProposalBinding : evaluation.exactProposalBinding
  exactCandidateBinding : evaluation.exactCandidateBinding
  exactRollbackBinding : evaluation.exactRollbackBinding
  stagingReviewOnly : evaluation.stagingReviewOnly
  noProductionApply : evaluation.noProductionApply
  noStateWrite : evaluation.noStateWrite
  noAuthorityWidening : evaluation.noAuthorityWidening

theorem safe_evaluation_preserves_all_bindings
    (evaluation : FiniteEvaluation)
    (h : evaluation.Safe) :
    evaluation.exactAdmissionBinding ∧
      evaluation.exactSourceBinding ∧
      evaluation.exactProposalBinding ∧
      evaluation.exactCandidateBinding ∧
      evaluation.exactRollbackBinding := by
  exact ⟨h.exactAdmissionBinding, h.exactSourceBinding,
    h.exactProposalBinding, h.exactCandidateBinding,
    h.exactRollbackBinding⟩

theorem safe_evaluation_remains_review_only
    (evaluation : FiniteEvaluation)
    (h : evaluation.Safe) :
    evaluation.stagingReviewOnly ∧
      evaluation.noProductionApply ∧
      evaluation.noStateWrite ∧
      evaluation.noAuthorityWidening := by
  exact ⟨h.stagingReviewOnly, h.noProductionApply,
    h.noStateWrite, h.noAuthorityWidening⟩

end KUOS.WORLD.KuuOSConnectionEvaluationCoreV0_64
