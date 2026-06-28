import KUOS.WORLD.KuuOSGovernanceRolePolicyV0_77

namespace KUOS.WORLD.KuuOSGovernanceRoleDecisionV0_77

open KuuOSGovernanceRolePolicyV0_77

structure RoleDecision where
  reviewerId : String
  authorityActorId : String
  validReview : Prop
  applicationAuthority : Prop
  stateWritePerformed : Prop
  liveApplicationPerformed : Prop
  permissionExpansionPerformed : Prop


structure RoleDecision.Valid
    (decision : RoleDecision)
    (policy : RolePolicy) : Prop where
  validReview : decision.validReview
  applicationAuthority : decision.applicationAuthority
  separationWhenConfigured :
    policy.separateActor = true →
      decision.reviewerId ≠ decision.authorityActorId
  noImmediateStateWrite : ¬ decision.stateWritePerformed
  noImmediateLiveApplication : ¬ decision.liveApplicationPerformed
  noPermissionExpansion : ¬ decision.permissionExpansionPerformed


theorem valid_decision_requires_separation_only_when_configured
    (decision : RoleDecision)
    (policy : RolePolicy)
    (hValid : decision.Valid policy)
    (hConfigured : policy.separateActor = true) :
    decision.reviewerId ≠ decision.authorityActorId := by
  exact hValid.separationWhenConfigured hConfigured


theorem valid_decision_preserves_application_authority
    (decision : RoleDecision)
    (policy : RolePolicy)
    (hValid : decision.Valid policy) :
    decision.applicationAuthority := by
  exact hValid.applicationAuthority


theorem valid_decision_has_no_immediate_effect
    (decision : RoleDecision)
    (policy : RolePolicy)
    (hValid : decision.Valid policy) :
    ¬ decision.stateWritePerformed ∧
      ¬ decision.liveApplicationPerformed ∧
      ¬ decision.permissionExpansionPerformed := by
  exact ⟨hValid.noImmediateStateWrite,
    hValid.noImmediateLiveApplication,
    hValid.noPermissionExpansion⟩

end KUOS.WORLD.KuuOSGovernanceRoleDecisionV0_77
