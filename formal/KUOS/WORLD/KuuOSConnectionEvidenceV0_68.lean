import KUOS.WORLD.KuuOSFiniteGaugeValidationV0_67

namespace KUOS.WORLD.KuuOSConnectionEvidenceV0_68

structure EvidenceCapsule where
  sourceBinding : Prop
  shadowBinding : Prop
  stagingPackageBinding : Prop
  shadowReceiptBinding : Prop
  gaugeValidationBinding : Prop
  candidateBinding : Prop
  rollbackBinding : Prop
  sampleCountBinding : Prop
  withinValidity : Prop
  evidenceOnly : Prop
  candidateOnly : Prop
  liveEffectDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop

structure EvidenceCapsule.Valid (capsule : EvidenceCapsule) : Prop where
  sourceBinding : capsule.sourceBinding
  shadowBinding : capsule.shadowBinding
  stagingPackageBinding : capsule.stagingPackageBinding
  shadowReceiptBinding : capsule.shadowReceiptBinding
  gaugeValidationBinding : capsule.gaugeValidationBinding
  candidateBinding : capsule.candidateBinding
  rollbackBinding : capsule.rollbackBinding
  sampleCountBinding : capsule.sampleCountBinding
  withinValidity : capsule.withinValidity
  evidenceOnly : capsule.evidenceOnly
  candidateOnly : capsule.candidateOnly
  liveEffectDenied : capsule.liveEffectDenied
  stateWriteDenied : capsule.stateWriteDenied
  authorityWideningDenied : capsule.authorityWideningDenied

theorem valid_evidence_preserves_chain
    (capsule : EvidenceCapsule)
    (h : capsule.Valid) :
    capsule.sourceBinding ∧
      capsule.shadowBinding ∧
      capsule.stagingPackageBinding ∧
      capsule.shadowReceiptBinding ∧
      capsule.gaugeValidationBinding ∧
      capsule.candidateBinding ∧
      capsule.rollbackBinding ∧
      capsule.sampleCountBinding := by
  exact ⟨h.sourceBinding, h.shadowBinding,
    h.stagingPackageBinding, h.shadowReceiptBinding,
    h.gaugeValidationBinding, h.candidateBinding,
    h.rollbackBinding, h.sampleCountBinding⟩

theorem valid_evidence_is_review_only
    (capsule : EvidenceCapsule)
    (h : capsule.Valid) :
    capsule.withinValidity ∧
      capsule.evidenceOnly ∧
      capsule.candidateOnly ∧
      capsule.liveEffectDenied ∧
      capsule.stateWriteDenied ∧
      capsule.authorityWideningDenied := by
  exact ⟨h.withinValidity, h.evidenceOnly, h.candidateOnly,
    h.liveEffectDenied, h.stateWriteDenied,
    h.authorityWideningDenied⟩

end KUOS.WORLD.KuuOSConnectionEvidenceV0_68
