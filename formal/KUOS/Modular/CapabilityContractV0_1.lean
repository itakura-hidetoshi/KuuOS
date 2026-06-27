namespace KUOS.Modular

/-- The authority class exposed by a capability module. -/
inductive AuthoritySurface where
  | candidateOnly
  | readOnly
  | advisory
  | boundedEffect
  deriving DecidableEq, Repr

/--
A minimal formal surface for the modular evolution mesh.

The Boolean fields represent authority claims that must remain explicit and
machine-checkable at module boundaries.
-/
structure ModuleContract where
  surface : AuthoritySurface
  ownsExecutionLicense : Bool
  ownsTruthAuthority : Bool
  mutatesPresentCyclePolicy : Bool
  disablesAudit : Bool
  erasesProvenance : Bool
  selfLicenses : Bool
  deriving DecidableEq, Repr

/-- Authority restrictions induced by each module surface. -/
def surfaceBoundary (contract : ModuleContract) : Prop :=
  match contract.surface with
  | .candidateOnly =>
      contract.ownsExecutionLicense = false ∧
      contract.ownsTruthAuthority = false ∧
      contract.mutatesPresentCyclePolicy = false
  | .readOnly =>
      contract.ownsExecutionLicense = false ∧
      contract.ownsTruthAuthority = false ∧
      contract.mutatesPresentCyclePolicy = false
  | .advisory =>
      contract.ownsExecutionLicense = false ∧
      contract.ownsTruthAuthority = false ∧
      contract.mutatesPresentCyclePolicy = false
  | .boundedEffect =>
      contract.ownsTruthAuthority = false ∧
      contract.disablesAudit = false ∧
      contract.erasesProvenance = false

/-- Constitutional admissibility is stronger than successful registration. -/
def constitutionallyAdmissible (contract : ModuleContract) : Prop :=
  contract.disablesAudit = false ∧
  contract.erasesProvenance = false ∧
  contract.selfLicenses = false ∧
  surfaceBoundary contract

/-- Discovery and registration cannot create a self-license. -/
theorem registry_discovery_does_not_grant_self_license
    (contract : ModuleContract)
    (h : constitutionallyAdmissible contract) :
    contract.selfLicenses = false := by
  rcases h with ⟨_, _, hSelfLicense, _⟩
  exact hSelfLicense

/-- A candidate-only module cannot acquire execution, truth, or activation authority. -/
theorem candidate_only_non_escalation
    (contract : ModuleContract)
    (hAdmissible : constitutionallyAdmissible contract)
    (hSurface : contract.surface = .candidateOnly) :
    contract.ownsExecutionLicense = false ∧
    contract.ownsTruthAuthority = false ∧
    contract.mutatesPresentCyclePolicy = false := by
  rcases hAdmissible with ⟨_, _, _, hBoundary⟩
  simpa [surfaceBoundary, hSurface] using hBoundary

/-- A read-only module cannot mutate the present-cycle policy. -/
theorem read_only_does_not_mutate_present_cycle
    (contract : ModuleContract)
    (hAdmissible : constitutionallyAdmissible contract)
    (hSurface : contract.surface = .readOnly) :
    contract.mutatesPresentCyclePolicy = false := by
  have hBoundary := hAdmissible.2.2.2
  have hReadOnly :
      contract.ownsExecutionLicense = false ∧
      contract.ownsTruthAuthority = false ∧
      contract.mutatesPresentCyclePolicy = false := by
    simpa [surfaceBoundary, hSurface] using hBoundary
  exact hReadOnly.2.2

end KUOS.Modular
