import KUOS.WORLD.KuuOSConnectionCandidateGaugeInvarianceV0_62

namespace KUOS.WORLD.KuuOSConnectionReviewCoreV0_63

inductive ReviewDecision where
  | approve
  | reject
  | defer
  deriving DecidableEq, Repr

structure ReviewEnvelope (Digest : Type*) where
  sourceBundleDigest : Digest
  proposalDigest : Digest
  selectedReceiptDigest : Digest
  candidateConnectionDigest : Digest
  rollbackDigest : Digest
  requestDigest : Digest
  licenseDigest : Digest
  decision : ReviewDecision
  exactRequestBinding : Prop
  exactSourceBinding : Prop
  exactReceiptBinding : Prop
  exactCandidateBinding : Prop
  exactRollbackBinding : Prop
  governedReviewer : Prop
  scopeBound : Prop
  withinValidity : Prop
  candidateOnly : Prop
  noProductionApply : Prop
  noStateWrite : Prop
  noAuthorityWidening : Prop

structure ReviewEnvelope.Approved
    {Digest : Type*}
    (envelope : ReviewEnvelope Digest) : Prop where
  decisionApprove : envelope.decision = ReviewDecision.approve
  exactRequestBinding : envelope.exactRequestBinding
  exactSourceBinding : envelope.exactSourceBinding
  exactReceiptBinding : envelope.exactReceiptBinding
  exactCandidateBinding : envelope.exactCandidateBinding
  exactRollbackBinding : envelope.exactRollbackBinding
  governedReviewer : envelope.governedReviewer
  scopeBound : envelope.scopeBound
  withinValidity : envelope.withinValidity
  candidateOnly : envelope.candidateOnly
  noProductionApply : envelope.noProductionApply
  noStateWrite : envelope.noStateWrite
  noAuthorityWidening : envelope.noAuthorityWidening

theorem approved_connection_remains_staging_only
    {Digest : Type*}
    (envelope : ReviewEnvelope Digest)
    (h : envelope.Approved) :
    envelope.candidateOnly ∧
      envelope.noProductionApply ∧
      envelope.noStateWrite ∧
      envelope.noAuthorityWidening := by
  exact ⟨h.candidateOnly, h.noProductionApply, h.noStateWrite,
    h.noAuthorityWidening⟩

theorem approved_connection_preserves_exact_bindings
    {Digest : Type*}
    (envelope : ReviewEnvelope Digest)
    (h : envelope.Approved) :
    envelope.exactRequestBinding ∧
      envelope.exactSourceBinding ∧
      envelope.exactReceiptBinding ∧
      envelope.exactCandidateBinding ∧
      envelope.exactRollbackBinding := by
  exact ⟨h.exactRequestBinding, h.exactSourceBinding,
    h.exactReceiptBinding, h.exactCandidateBinding,
    h.exactRollbackBinding⟩

end KUOS.WORLD.KuuOSConnectionReviewCoreV0_63
