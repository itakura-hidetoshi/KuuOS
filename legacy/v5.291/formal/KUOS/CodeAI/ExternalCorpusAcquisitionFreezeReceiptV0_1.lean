import Mathlib

namespace KUOS.CodeAI.ExternalCorpusAcquisitionFreezeReceiptV0_1

structure Binding where
  controllerVersion : Nat
  predecessorManifest : Nat
  predecessorPack : Nat
  predecessorReceipt : Nat
  datasetRevision : Nat
  artifactDigest : Nat
  artifactSize : Nat
  rowCount : Nat
  schemaDigest : Nat
  solverFieldsDigest : Nat
  restrictedFieldsDigest : Nat
  acquisitionContract : Nat
  freezePolicy : Nat
  deriving DecidableEq

structure CorpusContract where
  binding : Binding
  expectedArtifactSize : Nat
  expectedRowCount : Nat
  deriving DecidableEq

structure AcquisitionEvidence where
  binding : Binding
  fetchCompleted : Bool
  fetchPerformedByKernel : Bool
  externalNetworkObserved : Bool
  artifactObserved : Bool
  digestVerified : Bool
  sizeVerified : Bool
  rowCountVerified : Bool
  schemaVerified : Bool
  fieldPartitionVerified : Bool
  contentAddressed : Bool
  immutableFreeze : Bool
  artifactCommittedToRepository : Bool
  goldPatchExposed : Bool
  testPatchExposed : Bool
  labelsExposed : Bool
  harnessExecuted : Bool
  repositoryMutated : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  observedArtifactSize : Nat
  observedRowCount : Nat
  deriving DecidableEq


def ContractExact (contract : CorpusContract) (evidence : AcquisitionEvidence) : Prop :=
  evidence.binding = contract.binding ∧
  evidence.observedArtifactSize = contract.expectedArtifactSize ∧
  evidence.observedRowCount = contract.expectedRowCount


def AcquisitionVerified (evidence : AcquisitionEvidence) : Prop :=
  evidence.fetchCompleted = true ∧
  evidence.externalNetworkObserved = true ∧
  evidence.artifactObserved = true ∧
  evidence.digestVerified = true ∧
  evidence.sizeVerified = true ∧
  evidence.rowCountVerified = true ∧
  evidence.schemaVerified = true ∧
  evidence.fieldPartitionVerified = true ∧
  evidence.contentAddressed = true ∧
  evidence.immutableFreeze = true


def FieldIsolationPreserved (evidence : AcquisitionEvidence) : Prop :=
  evidence.goldPatchExposed = false ∧
  evidence.testPatchExposed = false ∧
  evidence.labelsExposed = false


def BoundaryPreserved (evidence : AcquisitionEvidence) : Prop :=
  evidence.fetchPerformedByKernel = false ∧
  evidence.artifactCommittedToRepository = false ∧
  evidence.harnessExecuted = false ∧
  evidence.repositoryMutated = false ∧
  evidence.gitAuthority = false ∧
  evidence.correctnessClaimed = false


def FreezeAdmitted (contract : CorpusContract) (evidence : AcquisitionEvidence) : Prop :=
  ContractExact contract evidence ∧
  AcquisitionVerified evidence ∧
  FieldIsolationPreserved evidence ∧
  BoundaryPreserved evidence


theorem admitted_exact_binding
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (h : FreezeAdmitted contract evidence) :
    evidence.binding = contract.binding := by
  exact h.1.1


theorem admitted_acquisition_verified
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (h : FreezeAdmitted contract evidence) :
    AcquisitionVerified evidence := by
  exact h.2.1


theorem admitted_field_isolation
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (h : FreezeAdmitted contract evidence) :
    FieldIsolationPreserved evidence := by
  exact h.2.2.1


theorem admitted_boundary_preserved
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (h : FreezeAdmitted contract evidence) :
    BoundaryPreserved evidence := by
  exact h.2.2.2


theorem revision_mismatch_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hMismatch : evidence.binding.datasetRevision ≠ contract.binding.datasetRevision) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  exact hMismatch (congrArg Binding.datasetRevision (admitted_exact_binding h))


theorem row_count_mismatch_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hMismatch : evidence.observedRowCount ≠ contract.expectedRowCount) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  exact hMismatch h.1.2.2


theorem gold_patch_exposure_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hExposed : evidence.goldPatchExposed = true) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  have hHidden := (admitted_field_isolation h).1
  rw [hExposed] at hHidden
  contradiction


theorem label_exposure_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hExposed : evidence.labelsExposed = true) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  have hHidden := (admitted_field_isolation h).2.2
  rw [hExposed] at hHidden
  contradiction


theorem kernel_fetch_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hFetch : evidence.fetchPerformedByKernel = true) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  have hNoFetch := (admitted_boundary_preserved h).1
  rw [hFetch] at hNoFetch
  contradiction


theorem harness_execution_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hExecuted : evidence.harnessExecuted = true) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  have hNoExecution := (admitted_boundary_preserved h).2.2.1
  rw [hExecuted] at hNoExecution
  contradiction


theorem repository_mutation_forbids_admission
    {contract : CorpusContract} {evidence : AcquisitionEvidence}
    (hMutated : evidence.repositoryMutated = true) :
    ¬ FreezeAdmitted contract evidence := by
  intro h
  have hNoMutation := (admitted_boundary_preserved h).2.2.2.1
  rw [hMutated] at hNoMutation
  contradiction


def referenceBinding : Binding where
  controllerVersion := 1335
  predecessorManifest := 1
  predecessorPack := 2
  predecessorReceipt := 3
  datasetRevision := 4
  artifactDigest := 5
  artifactSize := 2096679
  rowCount := 500
  schemaDigest := 6
  solverFieldsDigest := 7
  restrictedFieldsDigest := 8
  acquisitionContract := 9
  freezePolicy := 10


def referenceContract : CorpusContract where
  binding := referenceBinding
  expectedArtifactSize := 2096679
  expectedRowCount := 500


def referenceEvidence : AcquisitionEvidence where
  binding := referenceBinding
  fetchCompleted := true
  fetchPerformedByKernel := false
  externalNetworkObserved := true
  artifactObserved := true
  digestVerified := true
  sizeVerified := true
  rowCountVerified := true
  schemaVerified := true
  fieldPartitionVerified := true
  contentAddressed := true
  immutableFreeze := true
  artifactCommittedToRepository := false
  goldPatchExposed := false
  testPatchExposed := false
  labelsExposed := false
  harnessExecuted := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false
  observedArtifactSize := 2096679
  observedRowCount := 500


def referenceGoldExposed : AcquisitionEvidence :=
  { referenceEvidence with goldPatchExposed := true }


def referenceWrongRows : AcquisitionEvidence :=
  { referenceEvidence with observedRowCount := 499 }


def referenceHarnessExecuted : AcquisitionEvidence :=
  { referenceEvidence with harnessExecuted := true }


theorem reference_admitted : FreezeAdmitted referenceContract referenceEvidence := by
  simp [FreezeAdmitted, ContractExact, AcquisitionVerified, FieldIsolationPreserved,
    BoundaryPreserved, referenceContract, referenceEvidence, referenceBinding]


theorem reference_gold_exposed_not_admitted :
    ¬ FreezeAdmitted referenceContract referenceGoldExposed := by
  apply gold_patch_exposure_forbids_admission
  rfl


theorem reference_wrong_rows_not_admitted :
    ¬ FreezeAdmitted referenceContract referenceWrongRows := by
  apply row_count_mismatch_forbids_admission
  decide


theorem reference_harness_executed_not_admitted :
    ¬ FreezeAdmitted referenceContract referenceHarnessExecuted := by
  apply harness_execution_forbids_admission
  rfl

end KUOS.CodeAI.ExternalCorpusAcquisitionFreezeReceiptV0_1
