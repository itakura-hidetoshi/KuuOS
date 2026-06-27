import KUOS.WORLD.KuuOSConnectionEvaluationCoreV0_64

namespace KUOS.WORLD.KuuOSConnectionStagingV0_65

structure StagingPackage where
  packageDigestMatches : Prop
  sourceDigestMatches : Prop
  proposalDigestMatches : Prop
  admissionDigestMatches : Prop
  evaluationDigestMatches : Prop
  candidateDigestMatches : Prop
  rollbackDigestMatches : Prop
  shadowNamespace : Prop
  immutableEnvelope : Prop
  candidateOnly : Prop
  productionApplyDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop

structure StagingPackage.Valid (package : StagingPackage) : Prop where
  packageDigestMatches : package.packageDigestMatches
  sourceDigestMatches : package.sourceDigestMatches
  proposalDigestMatches : package.proposalDigestMatches
  admissionDigestMatches : package.admissionDigestMatches
  evaluationDigestMatches : package.evaluationDigestMatches
  candidateDigestMatches : package.candidateDigestMatches
  rollbackDigestMatches : package.rollbackDigestMatches
  shadowNamespace : package.shadowNamespace
  immutableEnvelope : package.immutableEnvelope
  candidateOnly : package.candidateOnly
  productionApplyDenied : package.productionApplyDenied
  stateWriteDenied : package.stateWriteDenied
  authorityWideningDenied : package.authorityWideningDenied

theorem valid_package_preserves_digest_chain
    (package : StagingPackage)
    (h : package.Valid) :
    package.packageDigestMatches ∧
      package.sourceDigestMatches ∧
      package.proposalDigestMatches ∧
      package.admissionDigestMatches ∧
      package.evaluationDigestMatches ∧
      package.candidateDigestMatches ∧
      package.rollbackDigestMatches := by
  exact ⟨h.packageDigestMatches, h.sourceDigestMatches,
    h.proposalDigestMatches, h.admissionDigestMatches,
    h.evaluationDigestMatches, h.candidateDigestMatches,
    h.rollbackDigestMatches⟩

theorem valid_package_remains_shadow_only
    (package : StagingPackage)
    (h : package.Valid) :
    package.shadowNamespace ∧
      package.immutableEnvelope ∧
      package.candidateOnly ∧
      package.productionApplyDenied ∧
      package.stateWriteDenied ∧
      package.authorityWideningDenied := by
  exact ⟨h.shadowNamespace, h.immutableEnvelope, h.candidateOnly,
    h.productionApplyDenied, h.stateWriteDenied,
    h.authorityWideningDenied⟩

end KUOS.WORLD.KuuOSConnectionStagingV0_65
