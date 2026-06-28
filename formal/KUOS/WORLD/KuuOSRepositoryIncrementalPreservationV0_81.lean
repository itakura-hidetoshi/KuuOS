import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryIncrementalPreservationV0_81

structure ScopeReuseWitness where
  previousScopeBound : Prop
  currentScopeBound : Prop
  scopeDigestEqual : Prop

structure ScopeReuseWitness.Valid (witness : ScopeReuseWitness) : Prop where
  previousScopeBound : witness.previousScopeBound
  currentScopeBound : witness.currentScopeBound
  scopeDigestEqual : witness.scopeDigestEqual

structure IncrementalPreservationWitness where
  previousNormalForm : Prop
  reusedScopesEqual : Prop
  recheckedScopesNormal : Prop
  globalScopeStableOrFullyRechecked : Prop
  currentScoreZero : Prop
  currentNormalForm : Prop

structure IncrementalPreservationWitness.Valid
    (witness : IncrementalPreservationWitness) : Prop where
  previousNormalForm : witness.previousNormalForm
  reusedScopesEqual : witness.reusedScopesEqual
  recheckedScopesNormal : witness.recheckedScopesNormal
  globalScopeStableOrFullyRechecked :
    witness.globalScopeStableOrFullyRechecked
  currentScoreZero : witness.currentScoreZero
  currentNormalForm : witness.currentNormalForm

theorem valid_scope_reuse_preserves_digest_equality
    (witness : ScopeReuseWitness)
    (h : witness.Valid) :
    witness.previousScopeBound ∧
      witness.currentScopeBound ∧
      witness.scopeDigestEqual := by
  exact ⟨h.previousScopeBound, h.currentScopeBound,
    h.scopeDigestEqual⟩

theorem valid_incremental_preservation
    (witness : IncrementalPreservationWitness)
    (h : witness.Valid) :
    witness.previousNormalForm ∧
      witness.reusedScopesEqual ∧
      witness.recheckedScopesNormal ∧
      witness.globalScopeStableOrFullyRechecked ∧
      witness.currentScoreZero ∧
      witness.currentNormalForm := by
  exact ⟨h.previousNormalForm, h.reusedScopesEqual,
    h.recheckedScopesNormal,
    h.globalScopeStableOrFullyRechecked,
    h.currentScoreZero, h.currentNormalForm⟩

end KUOS.WORLD.KuuOSRepositoryIncrementalPreservationV0_81
