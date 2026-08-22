import KuuOSGitHubMCPServerBridgeV0_1.V1_0

namespace KuuOS.GitHubMCPServerBridgeV1_1

structure CICompletionReentryGate where
  completionEventObserved : Bool
  eventPacketValid : Bool
  eventUsedAsSuccessEvidence : Bool
  freshMcpReobservation : Bool
  exactRepository : Bool
  exactRunId : Bool
  exactWorkflow : Bool
  exactHeadSha : Bool
  workflowCompleted : Bool
  conclusionAgrees : Bool
  jobsReobserved : Bool
  requiredJobsCompleted : Bool
  requiredStepsReobserved : Bool
  requiredStepsCompleted : Bool
  mergeAuthorityGranted : Bool
  writeAuthorityGranted : Bool
  deriving DecidableEq, Repr

def CICompletionReentryGate.Admitted (gate : CICompletionReentryGate) : Prop :=
  gate.completionEventObserved = true ∧
  gate.eventPacketValid = true ∧
  gate.eventUsedAsSuccessEvidence = false ∧
  gate.freshMcpReobservation = true ∧
  gate.exactRepository = true ∧
  gate.exactRunId = true ∧
  gate.exactWorkflow = true ∧
  gate.exactHeadSha = true ∧
  gate.workflowCompleted = true ∧
  gate.conclusionAgrees = true ∧
  gate.jobsReobserved = true ∧
  gate.requiredJobsCompleted = true ∧
  gate.requiredStepsReobserved = true ∧
  gate.requiredStepsCompleted = true ∧
  gate.mergeAuthorityGranted = false ∧
  gate.writeAuthorityGranted = false

theorem admitted_implies_fresh_mcp_reobservation (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.freshMcpReobservation = true := by exact h.2.2.2.1
theorem admitted_implies_exact_head_sha (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.exactHeadSha = true := by exact h.2.2.2.2.2.2.2.1
theorem admitted_implies_workflow_completed (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.workflowCompleted = true := by exact h.2.2.2.2.2.2.2.2.1
theorem admitted_implies_required_steps_completed (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.requiredStepsCompleted = true := by exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.1
theorem admitted_preserves_no_merge_authority (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.mergeAuthorityGranted = false := by exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.1
theorem admitted_preserves_no_write_authority (gate : CICompletionReentryGate) (h : gate.Admitted) : gate.writeAuthorityGranted = false := by exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2

@[simp] theorem event_only_never_admits (gate : CICompletionReentryGate) (hNoFreshMcp : gate.freshMcpReobservation = false) : ¬ gate.Admitted := by
  intro h; have hFresh := admitted_implies_fresh_mcp_reobservation gate h; simp [hNoFreshMcp] at hFresh

@[simp] theorem wrong_head_never_admits (gate : CICompletionReentryGate) (hWrongHead : gate.exactHeadSha = false) : ¬ gate.Admitted := by
  intro h; have hExact := admitted_implies_exact_head_sha gate h; simp [hWrongHead] at hExact

@[simp] theorem pending_workflow_never_admits (gate : CICompletionReentryGate) (hPending : gate.workflowCompleted = false) : ¬ gate.Admitted := by
  intro h; have hCompleted := admitted_implies_workflow_completed gate h; simp [hPending] at hCompleted

@[simp] theorem pending_required_step_never_admits (gate : CICompletionReentryGate) (hPending : gate.requiredStepsCompleted = false) : ¬ gate.Admitted := by
  intro h; have hCompleted := admitted_implies_required_steps_completed gate h; simp [hPending] at hCompleted

@[simp] theorem event_as_success_evidence_never_admits (gate : CICompletionReentryGate) (hEventAuthority : gate.eventUsedAsSuccessEvidence = true) : ¬ gate.Admitted := by
  intro h; have hSignalOnly : gate.eventUsedAsSuccessEvidence = false := h.2.2.1; simp [hEventAuthority] at hSignalOnly

@[simp] theorem merge_authority_never_follows_from_reentry (gate : CICompletionReentryGate) (hMerge : gate.mergeAuthorityGranted = true) : ¬ gate.Admitted := by
  intro h; have hNoMerge := admitted_preserves_no_merge_authority gate h; simp [hMerge] at hNoMerge

@[simp] theorem write_authority_never_follows_from_reentry (gate : CICompletionReentryGate) (hWrite : gate.writeAuthorityGranted = true) : ¬ gate.Admitted := by
  intro h; have hNoWrite := admitted_preserves_no_write_authority gate h; simp [hWrite] at hNoWrite

end KuuOS.GitHubMCPServerBridgeV1_1
