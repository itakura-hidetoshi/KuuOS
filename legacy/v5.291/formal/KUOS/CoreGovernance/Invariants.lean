/-
KuuOS Core Governance Invariants v0.1

This file is a minimal public Lean spine for KuuOS governance invariants.
It is intentionally small and dependency-light.

The declarations are structural witnesses. They do not grant execution authority.
-/

namespace KUOS
namespace CoreGovernance

inductive AuthoritySurface where
  | candidate
  | observation
  | validation
  | belief
  | proof
  | decision
  | memoryTruth
  | execution
  deriving DecidableEq, Repr

inductive ValidationStatus where
  | pass
  | hold
  | repair
  | reject
  deriving DecidableEq, Repr

inductive WorldClaim where
  | localWorld
  | fourfoldCore
  | replacesCore
  deriving DecidableEq, Repr

inductive Visibility where
  | visible
  | hidden
  deriving DecidableEq, Repr

inductive ParamitaRole where
  | orientation
  | actionAuthorization
  deriving DecidableEq, Repr

inductive TwoTruthsGap where
  | preserved
  | collapsed
  deriving DecidableEq, Repr

structure GovernanceCheckResult where
  status : ValidationStatus
  surface : AuthoritySurface
  deriving Repr

structure DukkhaState where
  dukkhaVisibility : Visibility
  harmVisibility : Visibility
  deriving Repr

structure ParamitaSelection where
  role : ParamitaRole
  authority : AuthoritySurface
  deriving Repr

/-- A validation pass is still a validation surface, not execution authority. -/
def validation_pass_not_execution_authority
    (r : GovernanceCheckResult) : Prop :=
  r.status = ValidationStatus.pass -> r.surface ≠ AuthoritySurface.execution

/-- AI raw output remains candidate unless separately governed; candidate is not authority. -/
def raw_ai_output_candidate_not_authority
    (s : AuthoritySurface) : Prop :=
  s = AuthoritySurface.candidate -> s ≠ AuthoritySurface.execution

/-- Dukkha visibility is preserved when it remains visible. -/
def dukkha_visibility_preserved
    (d : DukkhaState) : Prop :=
  d.dukkhaVisibility = Visibility.visible

/-- Harm must remain visible and must not be hidden by emptiness, harmony, or Qi language. -/
def harm_visibility_preserved
    (d : DukkhaState) : Prop :=
  d.harmVisibility = Visibility.visible

/-- Paramita selection is repair orientation, not action authorization. -/
def paramita_orientation_not_action_authorization
    (p : ParamitaSelection) : Prop :=
  p.role = ParamitaRole.orientation -> p.authority ≠ AuthoritySurface.execution

/-- A local WORLD model must not replace the fourfold core. -/
def no_world_replaces_fourfold_core
    (w : WorldClaim) : Prop :=
  w ≠ WorldClaim.replacesCore

/-- The two truths gap must not collapse. -/
def two_truths_gap_not_collapsed
    (g : TwoTruthsGap) : Prop :=
  g = TwoTruthsGap.preserved

/-- Qi language must not be used as harm denial. -/
def qi_language_not_harm_denial
    (d : DukkhaState) : Prop :=
  d.harmVisibility = Visibility.visible

/-- Example theorem: a validation PASS on validation surface is not execution authority. -/
theorem validation_pass_validation_surface_not_execution :
    validation_pass_not_execution_authority
      { status := ValidationStatus.pass, surface := AuthoritySurface.validation } := by
  intro _
  decide

/-- Example theorem: candidate raw output is not execution authority. -/
theorem candidate_surface_not_execution :
    raw_ai_output_candidate_not_authority AuthoritySurface.candidate := by
  intro _
  decide

/-- Example theorem: Paramita orientation with candidate authority is not execution. -/
theorem paramita_orientation_candidate_not_execution :
    paramita_orientation_not_action_authorization
      { role := ParamitaRole.orientation, authority := AuthoritySurface.candidate } := by
  intro _
  decide

/-- Example theorem: local world does not replace the fourfold core. -/
theorem local_world_not_replacing_core :
    no_world_replaces_fourfold_core WorldClaim.localWorld := by
  decide

/-- Example theorem: preserved two-truths gap is not collapsed. -/
theorem preserved_two_truths_gap_ok :
    two_truths_gap_not_collapsed TwoTruthsGap.preserved := by
  rfl

end CoreGovernance
end KUOS
