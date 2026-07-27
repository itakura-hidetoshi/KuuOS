import KuuOSGitHubMCPServerBridgeV0_1.V0_5

namespace KuuOS.GitHubMCPServerBridgeV0_6

structure LabelCanaryGate where
  writeAuthority : KuuOS.GitHubMCPServerBridgeV0_2.MCPWriteAuthority
  explicitConfirmation : Bool
  labelWriteToolWrite : Bool
  getLabelToolReadOnly : Bool
  exactRepository : Bool
  exactBaseSha : Bool
  nonceBound : Bool
  preflightAbsent : Bool
  createApplied : Bool
  createdLabelObservedExact : Bool
  deleteApplied : Bool
  deletedLabelObservedAbsent : Bool
  compensationUsed : Bool
  deriving DecidableEq, Repr

def LabelCanaryGate.Admitted (gate : LabelCanaryGate) : Prop :=
  gate.writeAuthority.Admitted ∧
  gate.explicitConfirmation = true ∧
  gate.labelWriteToolWrite = true ∧
  gate.getLabelToolReadOnly = true ∧
  gate.exactRepository = true ∧
  gate.exactBaseSha = true ∧
  gate.nonceBound = true ∧
  gate.preflightAbsent = true ∧
  gate.createApplied = true ∧
  gate.createdLabelObservedExact = true ∧
  gate.deleteApplied = true ∧
  gate.deletedLabelObservedAbsent = true ∧
  gate.compensationUsed = false

theorem admitted_implies_write_authority
    (gate : LabelCanaryGate)
    (h : gate.Admitted) : gate.writeAuthority.Admitted := by
  rcases h with ⟨hWrite, _, _, _, _, _, _, _, _, _, _, _, _⟩
  exact hWrite

theorem admitted_implies_preflight_absent
    (gate : LabelCanaryGate)
    (h : gate.Admitted) : gate.preflightAbsent = true := by
  rcases h with ⟨_, _, _, _, _, _, _, hAbsent, _, _, _, _, _⟩
  exact hAbsent

theorem admitted_implies_created_label_observed_exact
    (gate : LabelCanaryGate)
    (h : gate.Admitted) : gate.createdLabelObservedExact = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, hObserved, _, _, _⟩
  exact hObserved

theorem admitted_implies_deleted_label_observed_absent
    (gate : LabelCanaryGate)
    (h : gate.Admitted) : gate.deletedLabelObservedAbsent = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, hAbsent, _⟩
  exact hAbsent

theorem admitted_excludes_compensation
    (gate : LabelCanaryGate)
    (h : gate.Admitted) : gate.compensationUsed = false := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, hNoCompensation⟩
  exact hNoCompensation

@[simp] theorem preexisting_label_never_admits
    (gate : LabelCanaryGate)
    (hPresent : gate.preflightAbsent = false) : ¬ gate.Admitted := by
  intro h
  have hAbsent : gate.preflightAbsent = true :=
    admitted_implies_preflight_absent gate h
  simp [hPresent] at hAbsent

@[simp] theorem unobserved_created_label_never_admits
    (gate : LabelCanaryGate)
    (hUnobserved : gate.createdLabelObservedExact = false) : ¬ gate.Admitted := by
  intro h
  have hObserved : gate.createdLabelObservedExact = true :=
    admitted_implies_created_label_observed_exact gate h
  simp [hUnobserved] at hObserved

@[simp] theorem residual_label_never_admits
    (gate : LabelCanaryGate)
    (hResidual : gate.deletedLabelObservedAbsent = false) : ¬ gate.Admitted := by
  intro h
  have hAbsent : gate.deletedLabelObservedAbsent = true :=
    admitted_implies_deleted_label_observed_absent gate h
  simp [hResidual] at hAbsent

@[simp] theorem compensated_label_canary_never_admits
    (gate : LabelCanaryGate)
    (hCompensated : gate.compensationUsed = true) : ¬ gate.Admitted := by
  intro h
  have hNoCompensation : gate.compensationUsed = false :=
    admitted_excludes_compensation gate h
  simp [hCompensated] at hNoCompensation

theorem admitted_implies_complete_label_closeout
    (gate : LabelCanaryGate)
    (h : gate.Admitted) :
    gate.writeAuthority.Admitted ∧
    gate.explicitConfirmation = true ∧
    gate.labelWriteToolWrite = true ∧
    gate.getLabelToolReadOnly = true ∧
    gate.exactRepository = true ∧
    gate.exactBaseSha = true ∧
    gate.nonceBound = true ∧
    gate.preflightAbsent = true ∧
    gate.createApplied = true ∧
    gate.createdLabelObservedExact = true ∧
    gate.deleteApplied = true ∧
    gate.deletedLabelObservedAbsent = true ∧
    gate.compensationUsed = false :=
  h

end KuuOS.GitHubMCPServerBridgeV0_6
