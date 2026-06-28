import Mathlib
import KUOS.WORLD.KuuOSAuthorizedMemoryApplicationV0_75

/-!
# KuuOS authority role topology v0.77

Independent approval is controlled by the explicit role topology, not by the
operating context. In role-aggregated solo operation, a valid v0.74 review
authority remains sufficient in both research and production contexts.
A separated topology may require an additional independent approval.
-/

namespace KUOS.WORLD.KuuOSAuthorityRoleTopologyV0_77

inductive OperatingContext where
  | research
  | production
  deriving DecidableEq

inductive RoleTopology where
  | aggregated
  | separated
  deriving DecidableEq

def RequiresIndependentApproval : RoleTopology → Prop
  | RoleTopology.aggregated => False
  | RoleTopology.separated => True

def RequiresIndependentApprovalIn
    (_context : OperatingContext)
    (topology : RoleTopology) : Prop :=
  RequiresIndependentApproval topology

def ApplicationAuthorized
    (topology : RoleTopology)
    (reviewAuthorized independentApproved : Prop) : Prop :=
  reviewAuthorized ∧
    (RequiresIndependentApproval topology → independentApproved)

theorem independent_requirement_is_context_invariant
    (first second : OperatingContext)
    (topology : RoleTopology) :
    RequiresIndependentApprovalIn first topology ↔
      RequiresIndependentApprovalIn second topology := by
  rfl

theorem aggregated_topology_never_requires_independent_approval
    (context : OperatingContext) :
    ¬ RequiresIndependentApprovalIn context RoleTopology.aggregated := by
  simp [RequiresIndependentApprovalIn, RequiresIndependentApproval]

theorem solo_research_review_authority_suffices
    (reviewAuthorized : Prop)
    (hReview : reviewAuthorized) :
    ApplicationAuthorized RoleTopology.aggregated reviewAuthorized False := by
  constructor
  · exact hReview
  · intro hRequired
    exact hRequired.elim

theorem solo_production_review_authority_suffices
    (reviewAuthorized : Prop)
    (hReview : reviewAuthorized) :
    ApplicationAuthorized RoleTopology.aggregated reviewAuthorized False := by
  constructor
  · exact hReview
  · intro hRequired
    exact hRequired.elim

theorem production_context_does_not_force_independent_approval :
    ¬ RequiresIndependentApprovalIn
      OperatingContext.production
      RoleTopology.aggregated := by
  simp [RequiresIndependentApprovalIn, RequiresIndependentApproval]

theorem separated_topology_requires_independent_approval
    (reviewAuthorized independentApproved : Prop)
    (hAuthorized :
      ApplicationAuthorized
        RoleTopology.separated
        reviewAuthorized
        independentApproved) :
    independentApproved := by
  exact hAuthorized.2 (by
    simp [RequiresIndependentApproval])

theorem authorization_requires_review_authority
    (topology : RoleTopology)
    (reviewAuthorized independentApproved : Prop)
    (hAuthorized :
      ApplicationAuthorized topology reviewAuthorized independentApproved) :
    reviewAuthorized := by
  exact hAuthorized.1

end KUOS.WORLD.KuuOSAuthorityRoleTopologyV0_77
