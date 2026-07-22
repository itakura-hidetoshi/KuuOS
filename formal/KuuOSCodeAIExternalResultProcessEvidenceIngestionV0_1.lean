import KUOS.CodeAI.ExternalResultProcessEvidenceIngestionV0_1

namespace KuuOSCodeAIExternalResultProcessEvidenceIngestionV0_1

open KUOS.CodeAI.ExternalResultProcessEvidenceIngestionV0_1

example : IngestionAdmitted referenceBinding referenceEvidence :=
  reference_unresolved_admitted

example : referenceEvidence.resultEvidence.resolved = false :=
  reference_admission_preserves_unresolved_outcome

example : ¬ IngestionAdmitted referenceBinding referenceRawNames :=
  reference_raw_names_not_admitted

example : ¬ IngestionAdmitted referenceBinding referenceRepairFeedback :=
  reference_repair_feedback_not_admitted

end KuuOSCodeAIExternalResultProcessEvidenceIngestionV0_1
