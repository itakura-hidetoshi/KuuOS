import Mathlib

namespace KUOS.CodeAI

structure DurableResumptionExecutionInput where
  oneShot : Prop
  reusable : Prop
  activeNow : Prop
  loopExecutionAuthorized : Prop
  directGitEffectAuthorized : Prop
  automaticExecutionAuthorized : Prop
  generalGitAuthorityGranted : Prop

structure DurableResumptionExecutionPolicy where
  consumeExecutionInput : Prop
  invokeBoundedLoop : Prop
  requireExistingLifecycleEffectChain : Prop
  allowDirectGitEffect : Prop
  allowAutomaticExecution : Prop
  allowUnboundedExecution : Prop
  allowGeneralSuccessorAuthority : Prop

structure DurableResumptionExecutionRegistry where
  revision : ℕ
  successfulExecutionCount : ℕ
  consumedExecutionInputCount : ℕ
  consumedInvocationNonceCount : ℕ
  emittedLoopReceiptCount : ℕ


def DurableResumptionExecutionAdmissible
    (input : DurableResumptionExecutionInput)
    (policy : DurableResumptionExecutionPolicy) : Prop :=
  input.oneShot ∧
  ¬ input.reusable ∧
  input.activeNow ∧
  input.loopExecutionAuthorized ∧
  ¬ input.directGitEffectAuthorized ∧
  ¬ input.automaticExecutionAuthorized ∧
  ¬ input.generalGitAuthorityGranted ∧
  policy.consumeExecutionInput ∧
  policy.invokeBoundedLoop ∧
  policy.requireExistingLifecycleEffectChain ∧
  ¬ policy.allowDirectGitEffect ∧
  ¬ policy.allowAutomaticExecution ∧
  ¬ policy.allowUnboundedExecution ∧
  ¬ policy.allowGeneralSuccessorAuthority


def advanceDurableResumptionExecutionRegistry
    (registry : DurableResumptionExecutionRegistry) : DurableResumptionExecutionRegistry :=
  { revision := registry.revision + 1
    successfulExecutionCount := registry.successfulExecutionCount + 1
    consumedExecutionInputCount := registry.consumedExecutionInputCount + 1
    consumedInvocationNonceCount := registry.consumedInvocationNonceCount + 1
    emittedLoopReceiptCount := registry.emittedLoopReceiptCount + 1 }


theorem admissible_input_is_one_shot
    {input : DurableResumptionExecutionInput}
    {policy : DurableResumptionExecutionPolicy}
    (h : DurableResumptionExecutionAdmissible input policy) : input.oneShot := by
  exact h.1


theorem admissible_input_is_not_reusable
    {input : DurableResumptionExecutionInput}
    {policy : DurableResumptionExecutionPolicy}
    (h : DurableResumptionExecutionAdmissible input policy) : ¬ input.reusable := by
  exact h.2.1


theorem admissible_execution_has_no_direct_git_authority
    {input : DurableResumptionExecutionInput}
    {policy : DurableResumptionExecutionPolicy}
    (h : DurableResumptionExecutionAdmissible input policy) :
    ¬ input.directGitEffectAuthorized ∧ ¬ policy.allowDirectGitEffect := by
  rcases h with
    ⟨_, _, _, _, hInputDirect, _, _, _, _, _, hPolicyDirect, _, _, _⟩
  exact ⟨hInputDirect, hPolicyDirect⟩


theorem admissible_execution_requires_existing_effect_chain
    {input : DurableResumptionExecutionInput}
    {policy : DurableResumptionExecutionPolicy}
    (h : DurableResumptionExecutionAdmissible input policy) :
    policy.requireExistingLifecycleEffectChain := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, hChain, _, _, _, _⟩
  exact hChain


theorem registry_revision_advances_exactly_once
    (registry : DurableResumptionExecutionRegistry) :
    (advanceDurableResumptionExecutionRegistry registry).revision = registry.revision + 1 := by
  rfl


theorem registry_histories_advance_in_parallel
    (registry : DurableResumptionExecutionRegistry) :
    (advanceDurableResumptionExecutionRegistry registry).successfulExecutionCount =
        registry.successfulExecutionCount + 1 ∧
    (advanceDurableResumptionExecutionRegistry registry).consumedExecutionInputCount =
        registry.consumedExecutionInputCount + 1 ∧
    (advanceDurableResumptionExecutionRegistry registry).consumedInvocationNonceCount =
        registry.consumedInvocationNonceCount + 1 ∧
    (advanceDurableResumptionExecutionRegistry registry).emittedLoopReceiptCount =
        registry.emittedLoopReceiptCount + 1 := by
  simp [advanceDurableResumptionExecutionRegistry]

end KUOS.CodeAI
