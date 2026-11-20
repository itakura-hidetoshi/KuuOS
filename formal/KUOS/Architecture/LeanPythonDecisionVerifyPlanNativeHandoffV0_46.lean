import Mathlib
import KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8
import KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

/-!
# DecisionOS → VerifyOS → PlanOS: conditional native-handoff witness v0.46

The original DecisionOS handoff validity certificate and the existing v0.45
finite six-route model are combined only under an explicitly supplied
whole-receipt seam. This file proves no Python evaluation theorem and does
not manufacture a proof of external source authenticity or host permission.

Original DecisionOS / VerifyOS / PlanOS kernel definitions are not changed.
-/

namespace KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46

open KUOS.DecisionOS
open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43
open KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

/-- The exact original DecisionOS certificate conditions required before a
    downstream read-only intake route can be considered. -/
def originalDecisionAuthorityBoundary
    (r : BoundedPlanSynthesisRequestHandoffReceipt) : Prop :=
  r.planSynthesisRequestIssued = true ∧
  r.selectionAuthorityTransferredToPlanOS = false ∧
  r.executionAuthorityGrantedToPlanOS = false ∧
  r.planSynthesisPerformed = false ∧
  r.executionPermission = false

/-- These conditions follow from the original DecisionOS validity witness;
    the structure itself is not automatically inhabited by Python output. -/
theorem originalDecisionAuthorityBoundary_of_valid
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (h : BoundedPlanSynthesisRequestHandoffValid r) :
    originalDecisionAuthorityBoundary r := by
  obtain ⟨hRequest, _, _, hSelection, hExecution⟩ :=
    planos_receives_bounded_request_without_selection_or_execution_authority r h
  exact ⟨hRequest, hSelection, hExecution,
    h.plan_synthesis_not_performed, h.execution_permission_false⟩

/-- Whole typed packet identity is a prerequisite of the seam. Equality of
    a digest alone is not substituted for this witness. -/
structure WholeReceiptSeam (Receipt : Type)
    (decisionOutput verifySource : Receipt) : Prop where
  exactPacket : decisionOutput = verifySource

/-- Three-stage *conditional* witness: original DecisionOS valid handoff,
    exact whole-packet seam, and the proved v0.45 VerifyOS/PlanOS route model.
    This does not prove that a CPython execution satisfies the premises. -/
theorem decisionVerifyPlanConditionalWitness
    {Receipt : Type}
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (decisionOutput verifySource : Receipt)
    (hDecision : BoundedPlanSynthesisRequestHandoffValid r)
    (hSeam : WholeReceiptSeam Receipt decisionOutput verifySource)
    (context : ContextKey) (transition : TransitionKind) :
    originalDecisionAuthorityBoundary r ∧
    decisionOutput = verifySource ∧
    intakeRouteSimulation.targetRelation
      (dispositionForStatus (statusForTransition transition),
        admittedForStatus (statusForTransition transition))
      (encodeIntake (dispositionForStatus (statusForTransition transition)),
        admittedForStatus (statusForTransition transition)) := by
  exact ⟨originalDecisionAuthorityBoundary_of_valid r hDecision,
    hSeam.exactPacket, sixRouteConditionalTwoStageWitness context transition⟩

/-- Even a bounded intake is admitted only in the retain route of this
    finite model; this statement does not license plan synthesis. -/
theorem decisionHandoff_onlyRetainIsBoundedIntake
    (transition : TransitionKind) :
    admittedForStatus (statusForTransition transition) = true ↔
      transition = .retain :=
  onlyRetainRouteAdmitted transition

/-- The original DecisionOS certificate and the local route both retain
    independent non-execution boundaries. -/
theorem decisionAndRouteCannotLicenseExecution
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (hDecision : BoundedPlanSynthesisRequestHandoffValid r)
    (transition : TransitionKind) :
    r.executionPermission = false ∧
    ¬ CanExecute {
      evidence := .locallyChecked
      globalDescentCertified := false
      universalLeanPythonRefinementCertified := false
      executionLicensed := false
    } := by
  exact ⟨hDecision.execution_permission_false,
    sixRouteCannotLicenseExecution transition⟩

end KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46
