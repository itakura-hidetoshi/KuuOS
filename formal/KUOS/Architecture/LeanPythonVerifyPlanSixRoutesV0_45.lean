import Mathlib
import KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43
import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# Conditional Lean/Python VerifyOS-to-PlanOS six-route bridge v0.45

This file proves a concrete two-stage LocalSimulation / VerifiedSeam instance
for a SIX-case abstract route model:
  TransitionKind → ConditionalValidityStatus → IntakeDisposition × Bool.

The Python string-level models below encode the source-mapped tables of
the existing KuuOS VerifyOS and PlanOS kernels, but the definitions here
are NOT an interpreter formalization of those actual Python modules.
Independently rerunning those original Python kernels and comparing their
certificates is a separate runtime validation obligation.

No host effects, world truth, universal semantic equivalence, source issuer
authentication, globally atomic state, or execution authority is inferred.
-/

namespace KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

open KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43
open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

def encodeTransition : TransitionKind → String
  | .retain => "retain"
  | .suspend => "suspend"
  | .requestRevision => "request_revision"
  | .supersedeWithLineage => "supersede_with_lineage"
  | .complete => "complete"
  | .terminate => "terminate"

def encodeValidity : ConditionalValidityStatus → String
  | .valid => "valid"
  | .suspended => "suspended"
  | .revisionRequired => "revision_required"
  | .superseded => "superseded"
  | .completed => "completed"
  | .terminated => "terminated"

def encodeIntake : IntakeDisposition → String
  | .boundedSynthesisIntakeReady => "bounded_synthesis_intake_ready"
  | .awaitConditionChange => "await_condition_change"
  | .returnToDecisionOSRevision => "return_to_decisionos_revision"
  | .successorLineageReverificationRequired =>
      "successor_lineage_reverification_required"
  | .closeWithoutSynthesis => "close_without_synthesis"
  | .terminateWithoutSynthesis => "terminate_without_synthesis"

/-- Exact string route model of the original VerifyOS six-entry constant. -/
def pythonVerifyModel : String → Option String
  | "retain" => some "valid"
  | "suspend" => some "suspended"
  | "request_revision" => some "revision_required"
  | "supersede_with_lineage" => some "superseded"
  | "complete" => some "completed"
  | "terminate" => some "terminated"
  | _ => none

/-- Exact string route model of the original PlanOS six-entry constant. -/
def pythonIntakeModel : String → Option (String × Bool)
  | "valid" => some ("bounded_synthesis_intake_ready", true)
  | "suspended" => some ("await_condition_change", false)
  | "revision_required" => some ("return_to_decisionos_revision", false)
  | "superseded" =>
      some ("successor_lineage_reverification_required", false)
  | "completed" => some ("close_without_synthesis", false)
  | "terminated" => some ("terminate_without_synthesis", false)
  | _ => none

/-- Formal VerifyOS status and the independent string table agree in six cases. -/
theorem encodedVerify_commutes (t : TransitionKind) :
    pythonVerifyModel (encodeTransition t) =
      some (encodeValidity (statusForTransition t)) := by
  cases t <;> rfl

/-- Formal PlanOS disposition AND admission agree with the six-entry string table. -/
theorem encodedIntake_commutes (s : ConditionalValidityStatus) :
    pythonIntakeModel (encodeValidity s) =
      some (encodeIntake (dispositionForStatus s), admittedForStatus s) := by
  cases s <;> rfl

/-- Actual concrete preservation witness for the modeled VerifyOS route. -/
def verifyRouteSimulation :
    LocalSimulation TransitionKind String ConditionalValidityStatus String where
  sourceRelation := fun t raw => encodeTransition t = raw
  targetRelation := fun s raw => encodeValidity s = raw
  leanTransition := fun t s => s = statusForTransition t
  pythonTransition := fun raw next => pythonVerifyModel raw = some next
  admissible := fun _ _ => True
  overlapCompatible := fun _ _ => True
  preserves := by
    intro t raw s rawNext hSource _ hLean hPython _
    subst s
    rw [← hSource] at hPython
    rw [encodedVerify_commutes t] at hPython
    exact Option.some.inj hPython

/-- Actual concrete preservation witness for the modeled PlanOS intake. -/
def intakeRouteSimulation :
    LocalSimulation ConditionalValidityStatus String
      (IntakeDisposition × Bool) (String × Bool) where
  sourceRelation := fun s raw => encodeValidity s = raw
  targetRelation := fun outcome raw =>
    encodeIntake outcome.1 = raw.1 ∧ outcome.2 = raw.2
  leanTransition := fun s out =>
    out = (dispositionForStatus s, admittedForStatus s)
  pythonTransition := fun raw next => pythonIntakeModel raw = some next
  admissible := fun _ _ => True
  overlapCompatible := fun _ _ => True
  preserves := by
    intro s raw output rawNext hSource _ hLean hPython _
    subst output
    rw [← hSource] at hPython
    rw [encodedIntake_commutes s] at hPython
    have hPair : (encodeIntake (dispositionForStatus s),
        admittedForStatus s) = rawNext :=
      Option.some.inj hPython
    exact ⟨congrArg Prod.fst hPair, congrArg Prod.snd hPair⟩

/-- Both simulations have an identical intermediate relation, not merely labels. -/
def originalVerifyPlanIdentitySeam (context : ContextKey) :
    VerifiedSeam ConditionalValidityStatus String
      verifyRouteSimulation.targetRelation
      intakeRouteSimulation.sourceRelation where
  leftContext := context
  rightContext := context
  sameContext := rfl
  transports := by
    intro _ _ h
    exact h

/--
An ACTUAL instantiation of the original v0.43 two-stage transport theorem,
with two concrete route-table preservation proofs and a concrete seam witness.
-/
theorem sixRouteConditionalTwoStageWitness
    (context : ContextKey) (t : TransitionKind) :
    intakeRouteSimulation.targetRelation
      (dispositionForStatus (statusForTransition t),
        admittedForStatus (statusForTransition t))
      (encodeIntake (dispositionForStatus (statusForTransition t)),
        admittedForStatus (statusForTransition t)) := by
  exact twoStageConditionalTransport
    verifyRouteSimulation intakeRouteSimulation
    (originalVerifyPlanIdentitySeam context)
    t (encodeTransition t)
    (statusForTransition t) (encodeValidity (statusForTransition t))
    (dispositionForStatus (statusForTransition t),
      admittedForStatus (statusForTransition t))
    (encodeIntake (dispositionForStatus (statusForTransition t)),
      admittedForStatus (statusForTransition t))
    rfl True.intro rfl (encodedVerify_commutes t)
    True.intro True.intro rfl
    (encodedIntake_commutes (statusForTransition t)) True.intro

/-- Model-valued admission is possible for the retain/valid route only. -/
theorem onlyRetainRouteAdmitted (t : TransitionKind) :
    admittedForStatus (statusForTransition t) = true ↔ t = .retain := by
  cases t <;> decide

/-- Supersession cannot silently reuse a bounded synthesis intake. -/
theorem supersededRequiresReverification :
    pythonIntakeModel "superseded" =
      some ("successor_lineage_reverification_required", false) := by
  rfl

/-- The terminal two cases close or terminate without synthesis. -/
theorem completedAndTerminatedDoNotAdmit :
    pythonIntakeModel "completed" =
      some ("close_without_synthesis", false) ∧
    pythonIntakeModel "terminated" =
      some ("terminate_without_synthesis", false) := by
  exact ⟨rfl, rfl⟩

/-- Unknown raw VerifyOS transitions are not invented as valid routes. -/
theorem unknownVerifyRouteIsNone :
    pythonVerifyModel "unrecognized" = none := by
  rfl

/-- Unknown PlanOS statuses are not invented as eligible requests. -/
theorem unknownIntakeStatusIsNone :
    pythonIntakeModel "unrecognized" = none := by
  rfl

/-- A locally good route never supplies host execution permission. -/
theorem sixRouteCannotLicenseExecution (t : TransitionKind) :
    ¬ CanExecute {
      evidence := .locallyChecked
      globalDescentCertified := false
      universalLeanPythonRefinementCertified := false
      executionLicensed := false
    } := by
  exact localCheck_does_not_grant_execution _ rfl

end KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45
