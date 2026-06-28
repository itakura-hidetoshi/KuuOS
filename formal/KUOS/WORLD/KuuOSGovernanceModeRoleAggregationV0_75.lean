import Mathlib
import KUOS.WORLD.KuuOSMemorySelectionReviewV0_74

/-!
# KuuOS governance mode and role aggregation v0.75

This layer makes development-stage role aggregation explicit without changing
v0.74 review semantics. Solo research permits one principal to hold evidence
review and bounded application-authority roles. Team research may remain
aggregated or tighten to separated roles. Production requires separation.
-/

namespace KUOS.WORLD.KuuOSGovernanceModeRoleAggregationV0_75

inductive GovernanceMode where
  | soloResearch
  | teamResearch
  | production
  deriving DecidableEq, Repr

structure GovernanceModePolicy where
  mode : GovernanceMode
  independentAuthorityApprovalRequired : Bool
  roleAggregationPermitted : Bool
  futureRoleSeparationSupported : Bool
  deriving DecidableEq, Repr

namespace GovernanceModePolicy


def Valid (policy : GovernanceModePolicy) : Prop :=
  policy.futureRoleSeparationSupported = true ∧
    match policy.mode with
    | GovernanceMode.soloResearch =>
        policy.independentAuthorityApprovalRequired = false ∧
          policy.roleAggregationPermitted = true
    | GovernanceMode.teamResearch =>
        policy.roleAggregationPermitted =
          !policy.independentAuthorityApprovalRequired
    | GovernanceMode.production =>
        policy.independentAuthorityApprovalRequired = true ∧
          policy.roleAggregationPermitted = false


def soloResearchPolicy : GovernanceModePolicy where
  mode := GovernanceMode.soloResearch
  independentAuthorityApprovalRequired := false
  roleAggregationPermitted := true
  futureRoleSeparationSupported := true


def teamResearchAggregatedPolicy : GovernanceModePolicy where
  mode := GovernanceMode.teamResearch
  independentAuthorityApprovalRequired := false
  roleAggregationPermitted := true
  futureRoleSeparationSupported := true


def teamResearchSeparatedPolicy : GovernanceModePolicy where
  mode := GovernanceMode.teamResearch
  independentAuthorityApprovalRequired := true
  roleAggregationPermitted := false
  futureRoleSeparationSupported := true


def productionPolicy : GovernanceModePolicy where
  mode := GovernanceMode.production
  independentAuthorityApprovalRequired := true
  roleAggregationPermitted := false
  futureRoleSeparationSupported := true


theorem solo_research_policy_valid : soloResearchPolicy.Valid := by
  simp [Valid, soloResearchPolicy]


theorem team_research_aggregated_policy_valid :
    teamResearchAggregatedPolicy.Valid := by
  simp [Valid, teamResearchAggregatedPolicy]


theorem team_research_separated_policy_valid :
    teamResearchSeparatedPolicy.Valid := by
  simp [Valid, teamResearchSeparatedPolicy]


theorem production_policy_valid : productionPolicy.Valid := by
  simp [Valid, productionPolicy]


theorem valid_solo_research_permits_role_aggregation
    (policy : GovernanceModePolicy)
    (hMode : policy.mode = GovernanceMode.soloResearch)
    (hValid : policy.Valid) :
    policy.independentAuthorityApprovalRequired = false ∧
      policy.roleAggregationPermitted = true := by
  rcases hValid with ⟨_, hModeValid⟩
  simpa [hMode] using hModeValid


theorem valid_team_research_policy_is_consistent
    (policy : GovernanceModePolicy)
    (hMode : policy.mode = GovernanceMode.teamResearch)
    (hValid : policy.Valid) :
    policy.roleAggregationPermitted =
      !policy.independentAuthorityApprovalRequired := by
  rcases hValid with ⟨_, hModeValid⟩
  simpa [hMode] using hModeValid


theorem valid_production_requires_role_separation
    (policy : GovernanceModePolicy)
    (hMode : policy.mode = GovernanceMode.production)
    (hValid : policy.Valid) :
    policy.independentAuthorityApprovalRequired = true ∧
      policy.roleAggregationPermitted = false := by
  rcases hValid with ⟨_, hModeValid⟩
  simpa [hMode] using hModeValid


theorem valid_policy_preserves_future_role_separation
    (policy : GovernanceModePolicy)
    (hValid : policy.Valid) :
    policy.futureRoleSeparationSupported = true := by
  exact hValid.1


end GovernanceModePolicy


theorem valid_review_remains_nonexecuting_under_governance_mode
    (request : KuuOSMemorySelectionReviewV0_74.ReviewRequest)
    (receipt : KuuOSMemorySelectionReviewV0_74.ReviewReceipt)
    (hReview : receipt.Valid request)
    (policy : GovernanceModePolicy)
    (hPolicy : policy.Valid) :
    policy.futureRoleSeparationSupported = true ∧
      receipt.writesDisabled ∧
      receipt.liveApplicationDisabled ∧
      receipt.permissionExpansionDisabled ∧
      receipt.rollbackTargetReplacementDisabled := by
  refine ⟨hPolicy.1, ?_⟩
  exact
    KuuOSMemorySelectionReviewV0_74.
      valid_review_has_no_immediate_application_effect request receipt hReview


end KUOS.WORLD.KuuOSGovernanceModeRoleAggregationV0_75
