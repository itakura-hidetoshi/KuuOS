import KUOS.WORLD.KuuOSRepositoryCheckpointRepairRoutingV1_07

namespace KUOS.WORLD.KuuOSRepositoryCheckpointNamespaceGateV1_08

inductive NamespaceGateStatus where
  | noop
  | accepted
  | rejected
  deriving DecidableEq, Repr

inductive RouteInterface where
  | none
  | checkpointCreationV102
  | branchReferenceUpdateV097
  deriving DecidableEq, Repr

structure NamespaceGateWitness where
  routeValid : Prop
  routeFresh : Prop
  checkpointNamespace : Prop
  status : NamespaceGateStatus
  routeInterface : RouteInterface
  compatible : Bool

structure NamespaceGateWitness.ValidNoop
    (w : NamespaceGateWitness) : Prop where
  routeValid : w.routeValid
  routeFresh : w.routeFresh
  checkpointNamespace : w.checkpointNamespace
  statusNoop : w.status = NamespaceGateStatus.noop
  interfaceNone : w.routeInterface = RouteInterface.none
  compatibleFalse : w.compatible = false

structure NamespaceGateWitness.ValidCreation
    (w : NamespaceGateWitness) : Prop where
  routeValid : w.routeValid
  routeFresh : w.routeFresh
  checkpointNamespace : w.checkpointNamespace
  statusAccepted : w.status = NamespaceGateStatus.accepted
  interfaceCreation :
    w.routeInterface = RouteInterface.checkpointCreationV102
  compatibleTrue : w.compatible = true

structure NamespaceGateWitness.ValidNamespaceMismatch
    (w : NamespaceGateWitness) : Prop where
  routeValid : w.routeValid
  routeFresh : w.routeFresh
  checkpointNamespace : w.checkpointNamespace
  statusRejected : w.status = NamespaceGateStatus.rejected
  interfaceBranch :
    w.routeInterface = RouteInterface.branchReferenceUpdateV097
  compatibleFalse : w.compatible = false

structure NamespaceGateWitness.ValidInvalid
    (w : NamespaceGateWitness) : Prop where
  statusRejected : w.status = NamespaceGateStatus.rejected
  compatibleFalse : w.compatible = false


theorem checkpoint_creation_route_is_compatible
    (w : NamespaceGateWitness)
    (h : w.ValidCreation) :
    w.status = NamespaceGateStatus.accepted ∧
      w.routeInterface = RouteInterface.checkpointCreationV102 ∧
      w.compatible = true := by
  exact ⟨h.statusAccepted, h.interfaceCreation, h.compatibleTrue⟩


theorem branch_update_route_is_not_checkpoint_compatible
    (w : NamespaceGateWitness)
    (h : w.ValidNamespaceMismatch) :
    w.status = NamespaceGateStatus.rejected ∧
      w.routeInterface = RouteInterface.branchReferenceUpdateV097 ∧
      w.compatible = false := by
  exact ⟨h.statusRejected, h.interfaceBranch, h.compatibleFalse⟩


theorem accepted_decision_uses_checkpoint_creation_interface
    (w : NamespaceGateWitness)
    (h : w.ValidCreation) :
    w.routeInterface = RouteInterface.checkpointCreationV102 := by
  exact h.interfaceCreation


theorem rejected_decision_has_no_compatibility_claim
    (w : NamespaceGateWitness)
    (h : w.ValidNamespaceMismatch ∨ w.ValidInvalid) :
    w.compatible = false := by
  rcases h with h | h
  · exact h.compatibleFalse
  · exact h.compatibleFalse


structure NamespaceGateDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_namespace_decision
    {Input Output : Type}
    (derivation : NamespaceGateDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointNamespaceGateV1_08
