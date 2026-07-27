import KuuOSGitHubMCPServerBridgeV0_1.V0_7

namespace KuuOS.GitHubMCPServerBridgeV0_8

structure SubIssueBindingCanaryGate where
  writeAuthority : KuuOS.GitHubMCPServerBridgeV0_2.MCPWriteAuthority
  explicitConfirmation : Bool
  issueWriteToolWrite : Bool
  issueReadToolReadOnly : Bool
  subIssueWriteToolWrite : Bool
  exactRepository : Bool
  exactBaseSha : Bool
  nonceBound : Bool
  parentIssueIdentityExact : Bool
  parentSubIssuesInitiallyEmpty : Bool
  childCreateApplied : Bool
  childObservedExactOpen : Bool
  subIssueAddApplied : Bool
  addedChildObservedExact : Bool
  subIssueRemoveApplied : Bool
  removedChildObservedAbsent : Bool
  childCloseApplied : Bool
  childObservedExactClosed : Bool
  compensationUsed : Bool
  deriving DecidableEq, Repr

def SubIssueBindingCanaryGate.Admitted
    (gate : SubIssueBindingCanaryGate) : Prop :=
  gate.writeAuthority.Admitted ∧
  gate.explicitConfirmation = true ∧
  gate.issueWriteToolWrite = true ∧
  gate.issueReadToolReadOnly = true ∧
  gate.subIssueWriteToolWrite = true ∧
  gate.exactRepository = true ∧
  gate.exactBaseSha = true ∧
  gate.nonceBound = true ∧
  gate.parentIssueIdentityExact = true ∧
  gate.parentSubIssuesInitiallyEmpty = true ∧
  gate.childCreateApplied = true ∧
  gate.childObservedExactOpen = true ∧
  gate.subIssueAddApplied = true ∧
  gate.addedChildObservedExact = true ∧
  gate.subIssueRemoveApplied = true ∧
  gate.removedChildObservedAbsent = true ∧
  gate.childCloseApplied = true ∧
  gate.childObservedExactClosed = true ∧
  gate.compensationUsed = false

theorem admitted_implies_parent_sub_issues_initially_empty
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) : gate.parentSubIssuesInitiallyEmpty = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, hEmpty, _, _, _, _, _, _, _, _, _⟩
  exact hEmpty

theorem admitted_implies_added_child_observed_exact
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) : gate.addedChildObservedExact = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, hAdded, _, _, _, _, _⟩
  exact hAdded

theorem admitted_implies_removed_child_observed_absent
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) : gate.removedChildObservedAbsent = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, hRemoved, _, _, _⟩
  exact hRemoved

theorem admitted_implies_child_observed_exact_closed
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) : gate.childObservedExactClosed = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, hClosed, _⟩
  exact hClosed

theorem admitted_excludes_compensation
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) : gate.compensationUsed = false := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, hNoCompensation⟩
  exact hNoCompensation

@[simp] theorem preexisting_sub_issue_never_admits
    (gate : SubIssueBindingCanaryGate)
    (hPresent : gate.parentSubIssuesInitiallyEmpty = false) : ¬ gate.Admitted := by
  intro h
  have hEmpty := admitted_implies_parent_sub_issues_initially_empty gate h
  simp [hPresent] at hEmpty

@[simp] theorem unobserved_sub_issue_add_never_admits
    (gate : SubIssueBindingCanaryGate)
    (hUnobserved : gate.addedChildObservedExact = false) : ¬ gate.Admitted := by
  intro h
  have hAdded := admitted_implies_added_child_observed_exact gate h
  simp [hUnobserved] at hAdded

@[simp] theorem residual_sub_issue_binding_never_admits
    (gate : SubIssueBindingCanaryGate)
    (hResidual : gate.removedChildObservedAbsent = false) : ¬ gate.Admitted := by
  intro h
  have hRemoved := admitted_implies_removed_child_observed_absent gate h
  simp [hResidual] at hRemoved

@[simp] theorem open_child_never_admits
    (gate : SubIssueBindingCanaryGate)
    (hOpen : gate.childObservedExactClosed = false) : ¬ gate.Admitted := by
  intro h
  have hClosed := admitted_implies_child_observed_exact_closed gate h
  simp [hOpen] at hClosed

@[simp] theorem compensated_sub_issue_canary_never_admits
    (gate : SubIssueBindingCanaryGate)
    (hCompensated : gate.compensationUsed = true) : ¬ gate.Admitted := by
  intro h
  have hNoCompensation := admitted_excludes_compensation gate h
  simp [hCompensated] at hNoCompensation

theorem admitted_implies_complete_sub_issue_closeout
    (gate : SubIssueBindingCanaryGate)
    (h : gate.Admitted) :
    gate.writeAuthority.Admitted ∧
    gate.explicitConfirmation = true ∧
    gate.issueWriteToolWrite = true ∧
    gate.issueReadToolReadOnly = true ∧
    gate.subIssueWriteToolWrite = true ∧
    gate.exactRepository = true ∧
    gate.exactBaseSha = true ∧
    gate.nonceBound = true ∧
    gate.parentIssueIdentityExact = true ∧
    gate.parentSubIssuesInitiallyEmpty = true ∧
    gate.childCreateApplied = true ∧
    gate.childObservedExactOpen = true ∧
    gate.subIssueAddApplied = true ∧
    gate.addedChildObservedExact = true ∧
    gate.subIssueRemoveApplied = true ∧
    gate.removedChildObservedAbsent = true ∧
    gate.childCloseApplied = true ∧
    gate.childObservedExactClosed = true ∧
    gate.compensationUsed = false :=
  h

end KuuOS.GitHubMCPServerBridgeV0_8
