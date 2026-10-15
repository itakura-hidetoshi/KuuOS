import KUOS.WORLD.KuuOSRepositoryCheckpointDiscrepancyReviewV1_06

namespace KUOS.WORLD.KuuOSRepositoryCheckpointRepairRoutingV1_07

inductive RepairRouteStatus where
  | noop
  | automatic
  | rejected
  deriving DecidableEq, Repr

inductive RepairPrimitive where
  | none
  | atomicCheckpointCreationV102
  | atomicReferenceUpdateV097
  deriving DecidableEq, Repr

structure RepairRouteWitness where
  upstreamReviewValid : Prop
  repositoryBindingExact : Prop
  reviewFresh : Prop
  status : RepairRouteStatus
  primitive : RepairPrimitive
  automaticRouteEligible : Bool
  humanReviewRequired : Bool
  repositoryChangeAuthorityGranted : Bool
  executionPerformed : Bool

structure RepairRouteWitness.ValidNoop
    (w : RepairRouteWitness) : Prop where
  upstreamReviewValid : w.upstreamReviewValid
  repositoryBindingExact : w.repositoryBindingExact
  reviewFresh : w.reviewFresh
  statusNoop : w.status = RepairRouteStatus.noop
  primitiveNone : w.primitive = RepairPrimitive.none
  automaticRouteEligible : w.automaticRouteEligible = false
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted :
    w.repositoryChangeAuthorityGranted = false
  executionPerformed : w.executionPerformed = false

structure RepairRouteWitness.ValidLostRoute
    (w : RepairRouteWitness) : Prop where
  upstreamReviewValid : w.upstreamReviewValid
  repositoryBindingExact : w.repositoryBindingExact
  reviewFresh : w.reviewFresh
  statusAutomatic : w.status = RepairRouteStatus.automatic
  primitiveCreation :
    w.primitive = RepairPrimitive.atomicCheckpointCreationV102
  automaticRouteEligible : w.automaticRouteEligible = true
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted :
    w.repositoryChangeAuthorityGranted = false
  executionPerformed : w.executionPerformed = false

structure RepairRouteWitness.ValidSubstitutedRoute
    (w : RepairRouteWitness) : Prop where
  upstreamReviewValid : w.upstreamReviewValid
  repositoryBindingExact : w.repositoryBindingExact
  reviewFresh : w.reviewFresh
  statusAutomatic : w.status = RepairRouteStatus.automatic
  primitiveUpdate :
    w.primitive = RepairPrimitive.atomicReferenceUpdateV097
  automaticRouteEligible : w.automaticRouteEligible = true
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted :
    w.repositoryChangeAuthorityGranted = false
  executionPerformed : w.executionPerformed = false

structure RepairRouteWitness.ValidRejected
    (w : RepairRouteWitness) : Prop where
  statusRejected : w.status = RepairRouteStatus.rejected
  primitiveNone : w.primitive = RepairPrimitive.none
  automaticRouteEligible : w.automaticRouteEligible = false
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted :
    w.repositoryChangeAuthorityGranted = false
  executionPerformed : w.executionPerformed = false


theorem lost_checkpoint_selects_atomic_creation
    (w : RepairRouteWitness)
    (h : w.ValidLostRoute) :
    w.status = RepairRouteStatus.automatic ∧
      w.primitive = RepairPrimitive.atomicCheckpointCreationV102 ∧
      w.automaticRouteEligible = true := by
  exact ⟨h.statusAutomatic, h.primitiveCreation,
    h.automaticRouteEligible⟩


theorem substituted_checkpoint_selects_atomic_update
    (w : RepairRouteWitness)
    (h : w.ValidSubstitutedRoute) :
    w.status = RepairRouteStatus.automatic ∧
      w.primitive = RepairPrimitive.atomicReferenceUpdateV097 ∧
      w.automaticRouteEligible = true := by
  exact ⟨h.statusAutomatic, h.primitiveUpdate,
    h.automaticRouteEligible⟩


theorem valid_route_needs_no_human_review
    (w : RepairRouteWitness)
    (h : w.ValidNoop ∨ w.ValidLostRoute ∨
      w.ValidSubstitutedRoute ∨ w.ValidRejected) :
    w.humanReviewRequired = false := by
  rcases h with h | h | h | h
  · exact h.humanReviewRequired
  · exact h.humanReviewRequired
  · exact h.humanReviewRequired
  · exact h.humanReviewRequired


theorem routing_grants_no_change_authority
    (w : RepairRouteWitness)
    (h : w.ValidLostRoute ∨ w.ValidSubstitutedRoute) :
    w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false := by
  rcases h with h | h
  · exact ⟨h.repositoryChangeAuthorityGranted, h.executionPerformed⟩
  · exact ⟨h.repositoryChangeAuthorityGranted, h.executionPerformed⟩


structure RepairRouteDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_repair_route
    {Input Output : Type}
    (derivation : RepairRouteDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointRepairRoutingV1_07
