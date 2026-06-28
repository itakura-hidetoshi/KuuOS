import Mathlib

/-!
# KuuOS self-organizing improvement loop v0.78

The primary path is observation, structural diagnosis, finite candidate
construction, isolated shadow comparison, and reobservation.  External
approval is not a premise of a valid cycle.
-/

namespace KUOS.WORLD.KuuOSSelfOrganizingImprovementLoopV0_78

inductive CycleOutcome where
  | adopted
  | rolledBack
  | noChange
  deriving DecidableEq

structure ImprovementCycle where
  outcome : CycleOutcome
  observationBound : Prop
  diagnosisDerived : Prop
  candidateFamilyFinite : Prop
  candidateFamilySourceBound : Prop
  protectedCoordinatesExcluded : Prop
  shadowComparisonFinite : Prop
  shadowSourceUnchanged : Prop
  selectionDeterministic : Prop
  reobservationPerformed : Prop
  protectedCoordinatesPreserved : Prop
  shadowSafe : Prop
  reobservationNonworsening : Prop
  sourceRestored : Prop
  sourcePreserved : Prop
  externalApprovalRequired : Prop
  authorityWidened : Prop
  hostStateWritten : Prop

structure ImprovementCycle.Valid (cycle : ImprovementCycle) : Prop where
  observationBound : cycle.observationBound
  diagnosisDerived : cycle.diagnosisDerived
  candidateFamilyFinite : cycle.candidateFamilyFinite
  candidateFamilySourceBound : cycle.candidateFamilySourceBound
  protectedCoordinatesExcluded : cycle.protectedCoordinatesExcluded
  shadowComparisonFinite : cycle.shadowComparisonFinite
  shadowSourceUnchanged : cycle.shadowSourceUnchanged
  selectionDeterministic : cycle.selectionDeterministic
  reobservationPerformed : cycle.reobservationPerformed
  protectedCoordinatesPreserved : cycle.protectedCoordinatesPreserved
  adoptedSafe :
    cycle.outcome = CycleOutcome.adopted →
      cycle.shadowSafe ∧ cycle.reobservationNonworsening
  rollbackExact :
    cycle.outcome = CycleOutcome.rolledBack → cycle.sourceRestored
  noChangePreservesSource :
    cycle.outcome = CycleOutcome.noChange → cycle.sourcePreserved
  noExternalApproval : ¬ cycle.externalApprovalRequired
  noAuthorityWidening : ¬ cycle.authorityWidened
  noHostStateWrite : ¬ cycle.hostStateWritten


theorem valid_cycle_is_finite_and_source_bound
    (cycle : ImprovementCycle)
    (h : cycle.Valid) :
    cycle.candidateFamilyFinite ∧
      cycle.candidateFamilySourceBound ∧
      cycle.shadowComparisonFinite ∧
      cycle.shadowSourceUnchanged := by
  exact ⟨h.candidateFamilyFinite, h.candidateFamilySourceBound,
    h.shadowComparisonFinite, h.shadowSourceUnchanged⟩


theorem valid_cycle_needs_no_external_approval
    (cycle : ImprovementCycle)
    (h : cycle.Valid) :
    ¬ cycle.externalApprovalRequired := by
  exact h.noExternalApproval


theorem valid_adoption_is_shadow_and_reobservation_safe
    (cycle : ImprovementCycle)
    (h : cycle.Valid)
    (hAdopted : cycle.outcome = CycleOutcome.adopted) :
    cycle.shadowSafe ∧
      cycle.reobservationNonworsening ∧
      cycle.protectedCoordinatesPreserved := by
  exact ⟨(h.adoptedSafe hAdopted).1,
    (h.adoptedSafe hAdopted).2,
    h.protectedCoordinatesPreserved⟩


theorem valid_rollback_restores_source
    (cycle : ImprovementCycle)
    (h : cycle.Valid)
    (hRollback : cycle.outcome = CycleOutcome.rolledBack) :
    cycle.sourceRestored := by
  exact h.rollbackExact hRollback


theorem valid_no_change_preserves_source
    (cycle : ImprovementCycle)
    (h : cycle.Valid)
    (hNoChange : cycle.outcome = CycleOutcome.noChange) :
    cycle.sourcePreserved := by
  exact h.noChangePreservesSource hNoChange


theorem valid_cycle_does_not_expand_authority_or_write_host
    (cycle : ImprovementCycle)
    (h : cycle.Valid) :
    ¬ cycle.authorityWidened ∧ ¬ cycle.hostStateWritten := by
  exact ⟨h.noAuthorityWidening, h.noHostStateWrite⟩

end KUOS.WORLD.KuuOSSelfOrganizingImprovementLoopV0_78
