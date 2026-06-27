import KUOS.WORLD.KuuOSConnectionStagingV0_65

namespace KUOS.WORLD.KuuOSConnectionShadowV0_66

structure ShadowReceipt where
  packageBinding : Prop
  candidateBinding : Prop
  rollbackWitness : Prop
  sourceUnchanged : Prop
  curvatureNonincreasing : Prop
  memoryHolonomyPreserved : Prop
  fieldsPreserved : Prop
  sourceBindingsPreserved : Prop
  shadowOnly : Prop
  productionApplyDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop

structure ShadowReceipt.Valid (receipt : ShadowReceipt) : Prop where
  packageBinding : receipt.packageBinding
  candidateBinding : receipt.candidateBinding
  rollbackWitness : receipt.rollbackWitness
  sourceUnchanged : receipt.sourceUnchanged
  curvatureNonincreasing : receipt.curvatureNonincreasing
  memoryHolonomyPreserved : receipt.memoryHolonomyPreserved
  fieldsPreserved : receipt.fieldsPreserved
  sourceBindingsPreserved : receipt.sourceBindingsPreserved
  shadowOnly : receipt.shadowOnly
  productionApplyDenied : receipt.productionApplyDenied
  stateWriteDenied : receipt.stateWriteDenied
  authorityWideningDenied : receipt.authorityWideningDenied

theorem valid_shadow_preserves_source
    (receipt : ShadowReceipt)
    (h : receipt.Valid) :
    receipt.sourceUnchanged ∧
      receipt.rollbackWitness ∧
      receipt.packageBinding ∧
      receipt.candidateBinding := by
  exact ⟨h.sourceUnchanged, h.rollbackWitness,
    h.packageBinding, h.candidateBinding⟩

theorem valid_shadow_preserves_observables
    (receipt : ShadowReceipt)
    (h : receipt.Valid) :
    receipt.curvatureNonincreasing ∧
      receipt.memoryHolonomyPreserved ∧
      receipt.fieldsPreserved ∧
      receipt.sourceBindingsPreserved := by
  exact ⟨h.curvatureNonincreasing, h.memoryHolonomyPreserved,
    h.fieldsPreserved, h.sourceBindingsPreserved⟩

theorem valid_shadow_remains_isolated
    (receipt : ShadowReceipt)
    (h : receipt.Valid) :
    receipt.shadowOnly ∧
      receipt.productionApplyDenied ∧
      receipt.stateWriteDenied ∧
      receipt.authorityWideningDenied := by
  exact ⟨h.shadowOnly, h.productionApplyDenied,
    h.stateWriteDenied, h.authorityWideningDenied⟩

end KUOS.WORLD.KuuOSConnectionShadowV0_66
