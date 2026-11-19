import Mathlib
import KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43

/-!
# v0.44 — an actual finite conditional simulation witness

This theorem file instantiates v0.43 LocalSimulation for exactly three
evidence labels and the explicitly modeled Python string-level join.
It does NOT prove that an arbitrary Python interpreter, OS implementation,
source commit, receipt issuer or semantic transport has been verified.
A separate actual-Python exhaustive regression compares those nine cases.
-/

namespace KUOS.Architecture.LeanPythonFiniteEvidenceWitnessV0_44

open KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43

/-- Native Python names are modeled as exact literal strings. -/
def encodeStatus : EvidenceStatus → String
  | .noData => "NO_DATA"
  | .blocked => "BLOCKED"
  | .locallyChecked => "LOCALLY_CHECKED"

/-- Independent finite string-level operational model; invalid tokens block. -/
def pythonJoinModel (a b : String) : String :=
  if (a != "NO_DATA" && a != "BLOCKED" && a != "LOCALLY_CHECKED") ||
      (b != "NO_DATA" && b != "BLOCKED" && b != "LOCALLY_CHECKED") then
    "BLOCKED"
  else if a == "BLOCKED" || b == "BLOCKED" then "BLOCKED"
  else if a == "NO_DATA" || b == "NO_DATA" then "NO_DATA"
  else if a == "LOCALLY_CHECKED" && b == "LOCALLY_CHECKED" then
    "LOCALLY_CHECKED"
  else "BLOCKED"

/-- The three formal constructors have distinct modeled Python labels. -/
theorem encodeStatus_injective : Function.Injective encodeStatus := by
  intro a b h
  cases a <;> cases b <;> simp_all [encodeStatus]

/-- Concrete nine-case refinement of the *modeled* Python join table. -/
theorem encodedJoin_commutes (a b : EvidenceStatus) :
    encodeStatus (combineEvidence a b) =
      pythonJoinModel (encodeStatus a) (encodeStatus b) := by
  cases a <;> cases b <;> decide

/-- This standalone concrete simulation carries its own preservation proof. -/
def finiteEvidenceSimulation (incoming : EvidenceStatus) :
    LocalSimulation EvidenceStatus String EvidenceStatus String where
  sourceRelation := fun leanValue pyValue => encodeStatus leanValue = pyValue
  targetRelation := fun leanValue pyValue => encodeStatus leanValue = pyValue
  leanTransition := fun before after =>
    after = combineEvidence before incoming
  pythonTransition := fun before after =>
    after = pythonJoinModel before (encodeStatus incoming)
  admissible := fun _ _ => True
  overlapCompatible := fun _ _ => True
  preserves := by
    intro leanValue pyValue leanNext pyNext hSource _ hLean hPython _
    subst leanNext
    subst pyNext
    rw [← hSource]
    exact encodedJoin_commutes leanValue incoming

/-- This is an identity seam for one explicit, caller-supplied context key. -/
def finiteIdentitySeam (context : ContextKey)
    (firstIncoming secondIncoming : EvidenceStatus) :
    VerifiedSeam EvidenceStatus String
      (finiteEvidenceSimulation firstIncoming).targetRelation
      (finiteEvidenceSimulation secondIncoming).sourceRelation where
  leftContext := context
  rightContext := context
  sameContext := rfl
  transports := by
    intro leanValue pyValue h
    exact h

/-- Actually instantiate v0.43 twoStageConditionalTransport, not just quote it. -/
theorem finiteTwoStageSimulation
    (context : ContextKey) (initial firstIncoming secondIncoming : EvidenceStatus) :
    (finiteEvidenceSimulation secondIncoming).targetRelation
      (combineEvidence (combineEvidence initial firstIncoming) secondIncoming)
      (pythonJoinModel
        (pythonJoinModel (encodeStatus initial) (encodeStatus firstIncoming))
        (encodeStatus secondIncoming)) := by
  exact twoStageConditionalTransport
    (finiteEvidenceSimulation firstIncoming)
    (finiteEvidenceSimulation secondIncoming)
    (finiteIdentitySeam context firstIncoming secondIncoming)
    initial (encodeStatus initial)
    (combineEvidence initial firstIncoming)
    (pythonJoinModel (encodeStatus initial) (encodeStatus firstIncoming))
    (combineEvidence (combineEvidence initial firstIncoming) secondIncoming)
    (pythonJoinModel
      (pythonJoinModel (encodeStatus initial) (encodeStatus firstIncoming))
      (encodeStatus secondIncoming))
    rfl True.intro rfl rfl True.intro True.intro rfl rfl True.intro

/-- The full 27-case two-step modeled trace follows from the concrete witness. -/
theorem encodedTwoStage_commutes
    (context : ContextKey) (a b c : EvidenceStatus) :
    encodeStatus (combineEvidence (combineEvidence a b) c) =
      pythonJoinModel
        (pythonJoinModel (encodeStatus a) (encodeStatus b))
        (encodeStatus c) := by
  exact finiteTwoStageSimulation context a b c

/-- Local information order is associative on this finite evidence model. -/
theorem combineEvidence_assoc
    (a b c : EvidenceStatus) :
    combineEvidence (combineEvidence a b) c =
      combineEvidence a (combineEvidence b c) := by
  cases a <;> cases b <;> cases c <;> decide

/-- The encoded Python model also has associative triple evaluation. -/
theorem pythonJoinModel_assoc_on_encoded
    (a b c : EvidenceStatus) :
    pythonJoinModel
      (pythonJoinModel (encodeStatus a) (encodeStatus b))
      (encodeStatus c) =
    pythonJoinModel
      (encodeStatus a)
      (pythonJoinModel (encodeStatus b) (encodeStatus c)) := by
  cases a <;> cases b <;> cases c <;> decide

/-- An unsupported raw Python status must never be silently treated as pass. -/
theorem invalidPythonStatus_blocks :
    pythonJoinModel "PASS" "LOCALLY_CHECKED" = "BLOCKED" := by
  decide

/-- Invalid raw labels block even if paired with otherwise missing evidence. -/
theorem invalidPythonStatus_with_noData_blocks :
    pythonJoinModel "PASS" "NO_DATA" = "BLOCKED" := by
  decide

/-- A missing observation is not promoted by the other stage's success. -/
theorem unknownPythonStatus_is_not_success :
    pythonJoinModel "NO_DATA" "LOCALLY_CHECKED" = "NO_DATA" := by
  decide

/-- Even a concretely modeled checked status cannot issue execution rights. -/
theorem finiteCheckedWitness_grants_no_execution
    (status : EvidenceStatus) :
    ¬ CanExecute {
      evidence := status
      globalDescentCertified := false
      universalLeanPythonRefinementCertified := false
      executionLicensed := false
    } := by
  apply localCheck_does_not_grant_execution
  rfl

end KUOS.Architecture.LeanPythonFiniteEvidenceWitnessV0_44
