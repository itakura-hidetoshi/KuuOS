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

end KUOS.WORLD.KuuOSConnectionStagingV0_65
