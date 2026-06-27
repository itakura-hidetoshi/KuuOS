import KUOS.WORLD.KuuOSConnectionShadowV0_66

namespace KUOS.WORLD.KuuOSFiniteGaugeValidationV0_67

structure GaugeSample where
  sourceCurvatureInvariant : Prop
  shadowCurvatureInvariant : Prop
  sourceHolonomyInvariant : Prop
  shadowHolonomyInvariant : Prop
  relativeCurvatureNonincreasing : Prop
  relativeHolonomyPreserved : Prop
  fieldsSynchronized : Prop
  sourceBindingsSynchronized : Prop

structure GaugeSample.Valid (sample : GaugeSample) : Prop where
  sourceCurvatureInvariant : sample.sourceCurvatureInvariant
  shadowCurvatureInvariant : sample.shadowCurvatureInvariant
  sourceHolonomyInvariant : sample.sourceHolonomyInvariant
  shadowHolonomyInvariant : sample.shadowHolonomyInvariant
  relativeCurvatureNonincreasing : sample.relativeCurvatureNonincreasing
  relativeHolonomyPreserved : sample.relativeHolonomyPreserved
  fieldsSynchronized : sample.fieldsSynchronized
  sourceBindingsSynchronized : sample.sourceBindingsSynchronized

structure FiniteGaugeValidation where
  shadowReceiptBound : Prop
  allSamplesAdmissible : Prop
  rollbackReconstructionExact : Prop
  sourceUnchanged : Prop
  gaugeFamilyOnly : Prop
  productionApplyDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop

structure FiniteGaugeValidation.Valid (validation : FiniteGaugeValidation) : Prop where
  shadowReceiptBound : validation.shadowReceiptBound
  allSamplesAdmissible : validation.allSamplesAdmissible
  rollbackReconstructionExact : validation.rollbackReconstructionExact
  sourceUnchanged : validation.sourceUnchanged
  gaugeFamilyOnly : validation.gaugeFamilyOnly
  productionApplyDenied : validation.productionApplyDenied
  stateWriteDenied : validation.stateWriteDenied
  authorityWideningDenied : validation.authorityWideningDenied

theorem valid_sample_preserves_gauge_observables
    (sample : GaugeSample)
    (h : sample.Valid) :
    sample.sourceCurvatureInvariant ∧
      sample.shadowCurvatureInvariant ∧
      sample.sourceHolonomyInvariant ∧
      sample.shadowHolonomyInvariant := by
  exact ⟨h.sourceCurvatureInvariant, h.shadowCurvatureInvariant,
    h.sourceHolonomyInvariant, h.shadowHolonomyInvariant⟩

theorem valid_validation_reconstructs_source
    (validation : FiniteGaugeValidation)
    (h : validation.Valid) :
    validation.shadowReceiptBound ∧
      validation.allSamplesAdmissible ∧
      validation.rollbackReconstructionExact ∧
      validation.sourceUnchanged := by
  exact ⟨h.shadowReceiptBound, h.allSamplesAdmissible,
    h.rollbackReconstructionExact, h.sourceUnchanged⟩

theorem valid_validation_has_no_live_effect
    (validation : FiniteGaugeValidation)
    (h : validation.Valid) :
    validation.gaugeFamilyOnly ∧
      validation.productionApplyDenied ∧
      validation.stateWriteDenied ∧
      validation.authorityWideningDenied := by
  exact ⟨h.gaugeFamilyOnly, h.productionApplyDenied,
    h.stateWriteDenied, h.authorityWideningDenied⟩

end KUOS.WORLD.KuuOSFiniteGaugeValidationV0_67
