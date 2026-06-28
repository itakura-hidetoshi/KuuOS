import KUOS.WORLD.KuuOSGovernanceRolePolicyV0_76

namespace KUOS.WORLD.KuuOSGovernanceRoleOrthogonalityV0_76

open KuuOSGovernanceRolePolicyV0_76


theorem every_context_has_shared_policy
    (context : OperatingContext) :
    ∃ policy : RolePolicy,
      policy.context = context ∧ policy.separateActor = false := by
  exact ⟨sharedPolicy context, rfl, rfl⟩


theorem every_context_has_separated_policy
    (context : OperatingContext) :
    ∃ policy : RolePolicy,
      policy.context = context ∧ policy.separateActor = true := by
  exact ⟨separatedPolicy context, rfl, rfl⟩


theorem context_and_role_topology_are_orthogonal
    (context : OperatingContext) :
    ∃ shared separated : RolePolicy,
      shared.context = context ∧
      separated.context = context ∧
      shared.separateActor = false ∧
      separated.separateActor = true := by
  exact ⟨sharedPolicy context, separatedPolicy context, rfl, rfl, rfl, rfl⟩

end KUOS.WORLD.KuuOSGovernanceRoleOrthogonalityV0_76
