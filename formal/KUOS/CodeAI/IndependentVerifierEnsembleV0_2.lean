import Mathlib

namespace KUOS.CodeAI.IndependentVerifierEnsembleV0_2

inductive Verdict
  | passed
  | failed
  | inconclusive
  deriving DecidableEq, BEq

inductive CheckFamily
  | typeAndFormal
  | behavioralAndRegression
  | adversarialAndFalsification
  | maintainabilityAndStatic
  deriving DecidableEq, BEq

structure VerifierEvidence where
  verifierId : Nat
  organizationId : Nat
  sessionId : Nat
  methodId : Nat
  family : CheckFamily
  verdict : Verdict
  critical : Bool
  producerIndependent : Bool
  peerIndependent : Bool
  promptIndependent : Bool
  memoryIndependent : Bool
  testGenerationIndependent : Bool
  kernelExecuted : Bool
  repositoryMutated : Bool
  candidateSelected : Bool
  executionAuthority : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq


def passCount (evidence : List VerifierEvidence) : Nat :=
  (evidence.filter fun item => item.verdict == .passed).length


def failCount (evidence : List VerifierEvidence) : Nat :=
  (evidence.filter fun item => item.verdict == .failed).length


def inconclusiveCount (evidence : List VerifierEvidence) : Nat :=
  (evidence.filter fun item => item.verdict == .inconclusive).length


def HasFamily (evidence : List VerifierEvidence) (family : CheckFamily) : Prop :=
  ∃ item ∈ evidence, item.family = family


def AllFamiliesCovered (evidence : List VerifierEvidence) : Prop :=
  HasFamily evidence .typeAndFormal ∧
  HasFamily evidence .behavioralAndRegression ∧
  HasFamily evidence .adversarialAndFalsification ∧
  HasFamily evidence .maintainabilityAndStatic


def UniqueProvenance (evidence : List VerifierEvidence) : Prop :=
  (evidence.map (fun item => item.verifierId)).Nodup ∧
  (evidence.map (fun item => item.organizationId)).Nodup ∧
  (evidence.map (fun item => item.sessionId)).Nodup ∧
  (evidence.map (fun item => item.methodId)).Nodup


def Independent (item : VerifierEvidence) : Prop :=
  item.producerIndependent = true ∧
  item.peerIndependent = true ∧
  item.promptIndependent = true ∧
  item.memoryIndependent = true ∧
  item.testGenerationIndependent = true


def BoundaryPreserved (item : VerifierEvidence) : Prop :=
  item.kernelExecuted = false ∧
  item.repositoryMutated = false ∧
  item.candidateSelected = false ∧
  item.executionAuthority = false ∧
  item.gitAuthority = false ∧
  item.correctnessClaimed = false


def CriticalFailure (evidence : List VerifierEvidence) : Prop :=
  ∃ item ∈ evidence, item.verdict = .failed ∧ item.critical = true


def ConflictDetected (evidence : List VerifierEvidence) : Prop :=
  passCount evidence > 0 ∧ failCount evidence > 0


def Accepted (evidence : List VerifierEvidence) (passQuorum : Nat) : Prop :=
  passQuorum ≤ passCount evidence ∧
  failCount evidence = 0 ∧
  inconclusiveCount evidence = 0 ∧
  AllFamiliesCovered evidence ∧
  UniqueProvenance evidence ∧
  (∀ item ∈ evidence, Independent item) ∧
  (∀ item ∈ evidence, BoundaryPreserved item) ∧
  ¬ CriticalFailure evidence


def DisagreementHeld (evidence : List VerifierEvidence) : Prop :=
  ConflictDetected evidence


theorem accepted_pass_quorum
    {evidence : List VerifierEvidence} {passQuorum : Nat}
    (h : Accepted evidence passQuorum) :
    passQuorum ≤ passCount evidence := by
  rcases h with ⟨hPass, _⟩
  exact hPass


theorem accepted_has_no_failed_verifier
    {evidence : List VerifierEvidence} {passQuorum : Nat}
    (h : Accepted evidence passQuorum) :
    failCount evidence = 0 := by
  rcases h with ⟨_, hFail, _⟩
  exact hFail


theorem accepted_has_all_families
    {evidence : List VerifierEvidence} {passQuorum : Nat}
    (h : Accepted evidence passQuorum) :
    AllFamiliesCovered evidence := by
  rcases h with ⟨_, _, _, hFamilies, _⟩
  exact hFamilies


theorem accepted_preserves_boundary
    {evidence : List VerifierEvidence} {passQuorum : Nat}
    (h : Accepted evidence passQuorum) :
    ∀ item ∈ evidence, BoundaryPreserved item := by
  rcases h with ⟨_, _, _, _, _, _, hBoundary, _⟩
  exact hBoundary


theorem critical_failure_forbids_acceptance
    {evidence : List VerifierEvidence} {passQuorum : Nat}
    (hCritical : CriticalFailure evidence) :
    ¬ Accepted evidence passQuorum := by
  intro hAccepted
  rcases hAccepted with ⟨_, _, _, _, _, _, _, hNoCritical⟩
  exact hNoCritical hCritical


def referenceEvidence : List VerifierEvidence :=
  [
    {
      verifierId := 1
      organizationId := 11
      sessionId := 101
      methodId := 1001
      family := .typeAndFormal
      verdict := .passed
      critical := false
      producerIndependent := true
      peerIndependent := true
      promptIndependent := true
      memoryIndependent := true
      testGenerationIndependent := true
      kernelExecuted := false
      repositoryMutated := false
      candidateSelected := false
      executionAuthority := false
      gitAuthority := false
      correctnessClaimed := false
    },
    {
      verifierId := 2
      organizationId := 12
      sessionId := 102
      methodId := 1002
      family := .behavioralAndRegression
      verdict := .passed
      critical := false
      producerIndependent := true
      peerIndependent := true
      promptIndependent := true
      memoryIndependent := true
      testGenerationIndependent := true
      kernelExecuted := false
      repositoryMutated := false
      candidateSelected := false
      executionAuthority := false
      gitAuthority := false
      correctnessClaimed := false
    },
    {
      verifierId := 3
      organizationId := 13
      sessionId := 103
      methodId := 1003
      family := .adversarialAndFalsification
      verdict := .passed
      critical := false
      producerIndependent := true
      peerIndependent := true
      promptIndependent := true
      memoryIndependent := true
      testGenerationIndependent := true
      kernelExecuted := false
      repositoryMutated := false
      candidateSelected := false
      executionAuthority := false
      gitAuthority := false
      correctnessClaimed := false
    },
    {
      verifierId := 4
      organizationId := 14
      sessionId := 104
      methodId := 1004
      family := .maintainabilityAndStatic
      verdict := .passed
      critical := false
      producerIndependent := true
      peerIndependent := true
      promptIndependent := true
      memoryIndependent := true
      testGenerationIndependent := true
      kernelExecuted := false
      repositoryMutated := false
      candidateSelected := false
      executionAuthority := false
      gitAuthority := false
      correctnessClaimed := false
    }
  ]


theorem referenceEvidence_accepted : Accepted referenceEvidence 3 := by
  simp [Accepted, referenceEvidence, passCount, failCount, inconclusiveCount,
    AllFamiliesCovered, HasFamily, UniqueProvenance, Independent,
    BoundaryPreserved, CriticalFailure]


theorem referenceEvidence_has_four_passes : passCount referenceEvidence = 4 := by
  native_decide


theorem referenceEvidence_boundary_preserved :
    ∀ item ∈ referenceEvidence, BoundaryPreserved item := by
  exact accepted_preserves_boundary referenceEvidence_accepted

end KUOS.CodeAI.IndependentVerifierEnsembleV0_2
