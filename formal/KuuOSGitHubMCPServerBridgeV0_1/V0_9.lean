import KuuOSGitHubMCPServerBridgeV0_1.V0_8

namespace KuuOS.GitHubMCPServerBridgeV0_9

structure SubIssueBidirectionalCanaryGate where
  downwardGate : KuuOS.GitHubMCPServerBridgeV0_8.SubIssueBindingCanaryGate
  childParentInitiallyAbsent : Bool
  childParentObservedExactWhileAttached : Bool
  childParentObservedAbsentAfterRemove : Bool
  compensationParentReobservationUsed : Bool
  deriving DecidableEq, Repr

def SubIssueBidirectionalCanaryGate.Admitted
    (gate : SubIssueBidirectionalCanaryGate) : Prop :=
  gate.downwardGate.Admitted ∧
  gate.childParentInitiallyAbsent = true ∧
  gate.childParentObservedExactWhileAttached = true ∧
  gate.childParentObservedAbsentAfterRemove = true ∧
  gate.compensationParentReobservationUsed = false

theorem admitted_implies_downward_gate
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) : gate.downwardGate.Admitted :=
  h.1

theorem admitted_implies_child_parent_initially_absent
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) : gate.childParentInitiallyAbsent = true :=
  h.2.1

theorem admitted_implies_child_parent_exact_while_attached
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) : gate.childParentObservedExactWhileAttached = true :=
  h.2.2.1

theorem admitted_implies_child_parent_absent_after_remove
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) : gate.childParentObservedAbsentAfterRemove = true :=
  h.2.2.2.1

theorem admitted_excludes_parent_compensation
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) : gate.compensationParentReobservationUsed = false :=
  h.2.2.2.2

@[simp] theorem preexisting_child_parent_never_admits
    (gate : SubIssueBidirectionalCanaryGate)
    (hPresent : gate.childParentInitiallyAbsent = false) : ¬ gate.Admitted := by
  intro h
  have hAbsent := admitted_implies_child_parent_initially_absent gate h
  simp [hPresent] at hAbsent

@[simp] theorem wrong_upward_parent_never_admits
    (gate : SubIssueBidirectionalCanaryGate)
    (hWrong : gate.childParentObservedExactWhileAttached = false) :
    ¬ gate.Admitted := by
  intro h
  have hExact := admitted_implies_child_parent_exact_while_attached gate h
  simp [hWrong] at hExact

@[simp] theorem residual_upward_parent_never_admits
    (gate : SubIssueBidirectionalCanaryGate)
    (hResidual : gate.childParentObservedAbsentAfterRemove = false) :
    ¬ gate.Admitted := by
  intro h
  have hAbsent := admitted_implies_child_parent_absent_after_remove gate h
  simp [hResidual] at hAbsent

@[simp] theorem compensated_parent_reobservation_never_admits
    (gate : SubIssueBidirectionalCanaryGate)
    (hCompensated : gate.compensationParentReobservationUsed = true) :
    ¬ gate.Admitted := by
  intro h
  have hNoCompensation := admitted_excludes_parent_compensation gate h
  simp [hCompensated] at hNoCompensation

theorem admitted_implies_complete_bidirectional_closeout
    (gate : SubIssueBidirectionalCanaryGate)
    (h : gate.Admitted) :
    gate.downwardGate.Admitted ∧
    gate.childParentInitiallyAbsent = true ∧
    gate.childParentObservedExactWhileAttached = true ∧
    gate.childParentObservedAbsentAfterRemove = true ∧
    gate.compensationParentReobservationUsed = false :=
  h

end KuuOS.GitHubMCPServerBridgeV0_9
